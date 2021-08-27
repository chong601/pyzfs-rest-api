from multiprocessing import pool
import libzfs_core
from .data_conv import handle_str_to_bytes, handle_bytes_to_str
import libzfs_core.exceptions

"""
pylibzfs_core is intended to be a "proxy" of sorts to the upstream libzfs_core.

This module is intended to bridge between pyzfs_rest_api with libzfs_core so that any quirks
on libzfs_core can be handled here without modifying the existing libzfs_core source code.
Or just to make sure that our code to not blow up C because blowing things up is a bad idea ;)
"""

def lzc_snapshot(snapshot_list:list, props={}):
    # Enhancement: Allow snapshots with different pool names
    for snapshot_name in snapshot_list:
        libzfs_core.lzc_snapshot([handle_str_to_bytes(snapshot_name)], props)

def lzc_clone(name: str, origin: str, props={}):
    return libzfs_core.lzc_clone(handle_str_to_bytes(name), handle_str_to_bytes(origin), props)
    
def lzc_promote(name):
    return libzfs_core.lzc_promote(handle_str_to_bytes(name))

def lzc_exists(name):
    return libzfs_core.lzc_exists(handle_str_to_bytes(name))

def lzc_rename(source, target):
    return libzfs_core.lzc_rename(handle_str_to_bytes(source), handle_str_to_bytes(target))

def lzc_destroy(name):
    return libzfs_core.lzc_destroy(handle_str_to_bytes(name))

def lzc_sync(poolname):
    return libzfs_core.lzc_sync(handle_str_to_bytes(poolname))

def lzc_rollback(name):
    return libzfs_core.lzc_rollback(handle_str_to_bytes(name))

def lzc_rollback(name, snap):
    return libzfs_core.lzc_rollback_to(handle_str_to_bytes(name), handle_str_to_bytes(snap))

def lzc_hold(holds: dict):
    # NOTE: holds dict must be in this format:
    # snapshot_name: tag
    # tag and snapshot_name must be normalized to bytes
    fixed_holds = {}
    for tag, snapshot in holds.items():
        if not isinstance(tag, bytes):
            tag = handle_str_to_bytes(tag)
        if not isinstance(snapshot, bytes):
            snapshot = handle_str_to_bytes(snapshot)
        fixed_holds[tag] = snapshot
        
    return libzfs_core.lzc_hold(fixed_holds)

def lzc_get_holds(snapname):
    # Maybe normalize the data into str?
    if not isinstance(snapname, bytes):
        snapname = handle_str_to_bytes(snapname)
    result_dict = libzfs_core.lzc_get_holds(snapname)
    final_result = {}
    for result in result_dict:
        temp_result = result_dict[result]
        final_result[handle_bytes_to_str(result)] = temp_result
    del result_dict
    return final_result

def lzc_release(holds):
    # holds format is snapshot_name:tag
    return libzfs_core.lzc_release(holds)