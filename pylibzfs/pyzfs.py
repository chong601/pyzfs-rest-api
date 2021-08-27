import subprocess
# We import CSV, but we'll be doing TSV, really
import csv
from typing import List
from flask_restx.errors import abort

"""
pyzfs is the pure-Python implementation of interfacing with ZFS through userspace applications

Some extra functionalities that libzfs_core doesn't provide that can be implemented
will be done on this module.

The argument parser may not be perfect, but should cater most common simple tasks _for now_
"""

def zfs_list(name=None, sort_order:str=None, depth: int=None, property: list=None, recursive=False, type=None, detail=False):
    
    # No need for tab-delimited data, just YOLO parse it
    cmdline = ['zfs', 'list', '-p']
    # Handle sorting
    if sort_order:
        sort_prop, sort_order = sort_order.split(',',1)
        sort_order = bool(sort_order)
        sort_cmd = []
        if sort_order:
            sort_cmd.append('-s')
        else:
            sort_cmd.append('-S')
        if sort_prop is not None:
            sort_cmd.append(sort_prop)
        cmdline.extend(sort_cmd)
    # Handle recursion depth
    if depth:
        if isinstance(depth, int):
            cmdline.extend(['-d', str(depth)])
    # Handle property
    if property:
        property_list = ','.join(property)
        cmdline.extend(['-o', property_list])
    elif detail:
        cmdline.extend(['-o', 'all'])
    # Handle recursion
    if recursive:
        cmdline.append('-r')
    # Handle type
    if type:
        type_string = ','.join(type)
        cmdline.extend(['-t', type_string])
    # Handle name
    if name:
        cmdline.append(name)
    result = subprocess.run(cmdline, universal_newlines=True, capture_output=True)
    if result.returncode != 0:
        abort(404, **{'error': f'Error from zfs: {result.stderr.strip()}'})

    # BEGIN horrible code
    result_arr = result.stdout.strip().splitlines()
    result_header = result_arr[0].split(None)
    result_body = [row.split(None) for row in result_arr[1:]]
    final_result = []
    for row in result_body:
        data_dict = {}
        for idx, data in enumerate(row, 0):
            data_dict.update({result_header[idx]: data})
            
        final_result.append(data_dict)
    # TODO: Handle data conversion

    # END horrible code
    return final_result

def zpool_list(name=None, props=[], detail=False):
    
    # No need for tab-delimited data, just YOLO parse it
    cmdline = ['zpool', 'list', '-p']
    # Define default columns that ZFS has
    if props:
        prop_str = ','.join(props)
        cmdline.extend(['-o', prop_str])
    elif detail:
        cmdline.extend(['-o', 'all'])
    if name:
        cmdline.append(name)
    result = subprocess.run(cmdline, universal_newlines=True, capture_output=True)
    if result.returncode != 0:
        return f'Error from zpool: {result.stderr}'

    # BEGIN horrible code
    result_arr = result.stdout.strip().splitlines()
    result_header = result_arr[0].split(None)
    result_body = [row.split(None) for row in result_arr[1:]]
    final_result = []
    for row in result_body:
        data_dict = {}
        for idx, data in enumerate(row, 0):
            data_dict.update({result_header[idx]: data})

        final_result.append(data_dict)
    # TODO: Handle data conversion

    # END horrible code
    return final_result

def zpool_trim(pool: str, device: List[str]=None, secure: bool=False, rate: bool=None, wait: bool=False, suspend: bool=False, cancel: bool=False):
    cmdline = ['zpool', 'trim']
    if secure:
        if cancel:
            print('Ignoring cancel argument...')
            cancel=None
        if suspend:
            print('Ignoring suspend argument...')
            suspend=None
        cmdline.append(['-d'])
    if rate:
        if not isinstance(rate, int):
            raise TypeError
        cmdline.extend(['-r', rate])
    if wait:
        if suspend or cancel:
            abort(403, error='Cannot invoke suspend and cancel at the same time')
        cmdline.append('-w')
    if suspend:
        if cancel:
            abort(403, error='Cannot invoke suspend and cancel at the same time')
        cmdline.append('-s')
    if cancel:
        if suspend:
            abort(403, error='Cannot invoke suspend and cancel at the same time')
        cmdline.append('-c')
    cmdline.append(pool)
    if device:
        cmdline.extend(device)
    print(cmdline)
    result = subprocess.run(cmdline, universal_newlines=True, capture_output=True)
    print(result.returncode)
    if result.returncode != 0:
        raise Exception(f'Error from zfs: {result.stderr}')
    if result.stdout.startswith('no'):
        raise Exception('No dataset found')
    result_arr = result.stdout.strip().split('\n')

def zfs_get_running_version():
    result = subprocess.run(['zpool', '--version'], universal_newlines=True, capture_output=True)
    if result.returncode != 0:
        raise Exception(f'Error from zpool: {result.stderr}')
    version_data = result.stdout.strip().split('\n')
    return {'zpool_version': version_data[0], 'module_version': version_data[1]}
