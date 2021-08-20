import subprocess
# We import CSV, but we'll be doing TSV, really
import csv
from typing import List

def zfs_list(name=None, sort_ascending: tuple=None, depth: int=None, property: list=None, recursive=False, type=['filesystem']):
    
    # Force enable tab-delimited data
    cmdline = ['zfs', 'list', '-H', '-p']
    # Define default columns that ZFS has
    columns = ['name', 'used', 'avail', 'refer', 'mountpoint']
    # Handle sorting
    if sort_ascending:
        sort_prop, sort_order = sort_ascending
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
        cmdline.append('-o')
        cmdline.extend(property)
        columns = property
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
    print(cmdline)
    result = subprocess.run(cmdline, universal_newlines=True, capture_output=True)
    print(result.returncode)
    if result.returncode != 0:
        raise Exception(f'Error from zfs: {result.stderr}')
    if result.stdout.startswith('no'):
        raise Exception('No dataset found')
    result_arr = result.stdout.strip().split('\n')
    result_dict = csv.DictReader(result_arr, columns, delimiter='\t')
    for row in result_dict:
        print(row)

def zpool_list(name=None):
    
    # Force enable tab-delimited data
    cmdline = ['zpool', 'list', '-H', '-p']
    # Define default columns that ZFS has
    columns = ['name', 'size', 'allocated', 'free', 'checkpoint', 'expandsize', 'fragmentation', 'capacity', 'dedupratio', 'health', 'altroot']
    if name:
        cmdline.append(name)
    print(cmdline)
    result = subprocess.run(cmdline, universal_newlines=True, capture_output=True)
    print(result.returncode)
    if result.returncode != 0:
        return f'Error from zpool: {result.stderr}'
    result_arr = result.stdout.strip().split('\n')
    result_dict = csv.DictReader(result_arr, columns, delimiter='\t')
    
    final_result = []

    for row in result_dict:
        real_result_dict = {}
        for k, v in row.items():
            if k == 'expandsize' and v == '-':
                real_result_dict[k] = 0
            else:
                real_result_dict[k] = v
        final_result.append(real_result_dict)

    if len(final_result) > 1:
        return final_result
    else:
        return final_result[0]

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
            raise Exception('Cannot raise suspend or cancel with wait')
        cmdline.append('-w')
    if suspend:
        if cancel:
            raise Exception('Cannot invoke suspend and cancel at the same time')
        cmdline.append('-s')
    if cancel:
        if suspend:
            raise Exception('Cannot invoke suspend and cancel at the same time')
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
