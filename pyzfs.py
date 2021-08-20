import subprocess
# We import CSV, but we'll be doing TSV, really
import csv

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
    

        
        

