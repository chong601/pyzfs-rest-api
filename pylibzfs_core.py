from multiprocessing import pool
import libzfs_core

"""
pylibzfs_core is intended to be a "proxy" of sorts to the upstream libzfs_core.
Some extra functionalities that libzfs_core doesn't provide that can be implemented
will be done on this module.
"""

def lzc_snapshot(snapshot_list:list, props={}):
    # Enhancement: Allow snapshots with different pool names
    for snapshot_name in snapshot_list:
        libzfs_core.lzc_snap([bytes(snapshot_name, 'utf-8')], props)

def lzc_clone(name: str, origin: str, props={}):
    libzfs_core.lzc_clone(bytes(name, 'utf-8'), bytes(origin, 'utf-8'), props)
    
def lzc_promote(name):
    libzfs_core.lzc_promote(bytes(name, 'utf-8'))

def lzc_exists(name):
    return libzfs_core.lzc_exists(bytes(name, 'utf-8'))
    
def lzc_rename(source, target):
    libzfs_core.lzc_rename(bytes(source, 'utf-8'), bytes(target, 'utf-8'))

def lzc_destroy(name):
    libzfs_core.lzc_destroy(bytes(name, 'utf-8'))

def lzc_sync(poolname):
    libzfs_core.lzc_sync(bytes(poolname, 'utf-8'))

def lzc_rollback(name):
    libzfs_core.lzc_rollback(bytes(name, 'utf-8'))

def lzc_rollback(name, snap):
    libzfs_core.lzc_rollback_to(bytes(name, 'utf-8'), bytes(snap, 'utf-8'))

def lzc_trim():
    libzfs_core.lzc_trim