# pyzfs-rest-api
REST API for ZFS zpool and ZFS, because ZFS is *awesome*. It just needs more pizzaz and automation love.

pyzfs-rest-api is based on [OpenZFS `libzfs_core`](https://github.com/openzfs/zfs/tree/master/contrib/pyzfs) implementation with custom implementation for unimplemented calls.

# Goals
pyzfs-rest-api is intended to be (almost) feature-parity with upstream OpenZFS, as long the implementation is clear enough.

API implementation will be considered stable if the interface is at least compatible with all currently supported versions of ZFS (subject to change)

ABI support between pyzfs-rest-api and libzfs_core will depend on how complicated pyzfs is (might need to learn cffi *shudders*)

# `libzfs_core` status
| Function name | Status | Notes|
| - | - | - |
lzc_create | Broken | Throws error during creation for non-root user|
lzc_clone | Broken | Throws error during creation for non-root user |
lzc_promote | Unknown | |
lzc_rename | Unknown | |
lzc_destroy | Unknown | |
lzc_snapshot | Unknown | |
lzc_destroy_snap | Unknown | |
lzc_snaprange_space | Unknown | |
lzc_exists | Unknown | |
lzc_sync | Unknown | |
lzc_hold | Unknown | |
lzc_release | Unknown | |
lzc_get_holds | Unknown | |
lzc_send | Unknown | |
lzc_send_redacted | Unknown | |
lzc_send_resume | Unknown | |
lzc_send_resume_redacted | Unknown | |
lzc_send_space_resume_redacted | Unknown | |
lzc_send_space | Unknown | |
lzc_receive | Unknown | |
lzc_receive_resumable | Unknown | |
lzc_receive_with_header | Unknown | |
lzc_receive_one | Unknown | |
lzc_receive_with_cmdprops | Unknown | |
lzc_rollback | Unknown | |
lzc_rollback_to | Unknown | |
lzc_bookmark | Unknown | |
lzc_get_bookmarks | Unknown | |
lzc_get_bookmark_props | Unknown | |
lzc_destroy_bookmarks | Unknown | |
lzc_channel_program_impl | Unknown | |
lzc_channel_program | Unknown | |
lzc_pool_checkpoint | Unknown | |
lzc_pool_checkpoint_discard | Unknown | |
lzc_channel_program_nosync | Unknown | |
lzc_load_key | Unknown | |
lzc_unload_key | Unknown | |
lzc_change_key | Unknown | |
lzc_reopen | Unknown | |
lzc_initialize | Unknown | |
lzc_trim | Unknown | |
lzc_redact | Unknown | |
lzc_wait | Unknown | |
lzc_wait_tag | Unknown | |
lzc_wait_fs | Unknown | |
lzc_set_bootenv | Unknown | |
lzc_get_bootenv | Unknown | |

# `pyzfs` implementation
| Function name | Status | Notes |
| - | - | - |
| zfs_list | Done | Pending unit tests|

# Why the split between libzfs_core and pyzfs?
Simple.

libzfs_core only implements subset of ZFS functions that is offered by ZFS (for now).

Anything that `libzfs_core` does not cover will be implemented on `pyzfs` until C function replacements is available.
# Plans
TBD.

# License
I'm currently undecided on how to license this code. Do provide a recommended license if you're expert in this field!
pyzfs is ©️ ClusterHQ 2015 and ©️ OpenZFS 2018-current and is licensed under Apache License 2.0
