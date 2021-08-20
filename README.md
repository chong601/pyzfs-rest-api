# pyzfs-rest-api
REST API for ZFS zpool and ZFS, because ZFS is *awesome*. It just needs more pizzaz and automation love.

pyzfs-rest-api is based on [OpenZFS `pyzfs`](https://github.com/openzfs/zfs/tree/master/contrib/pyzfs) implementation with custom implementation for unimplemented calls.

# Goals
pyzfs-rest-api is intended to be (almost) feature-parity with upstream OpenZFS, as long the implementation is clear enough.

API implementation will be considered stable if the interface is at least compatible with all currently supported versions of ZFS (subject to change)

ABI support between pyzfs-rest-api and libzfs_core will depend on how complicated pyzfs is (might need to learn cffi *shudders*)

# Plans
TBD.

# License
I'm currently undecided on how to license this code. Do provide a recommended license if you're expert in this field!
pyzfs is ©️ ClusterHQ 2015 and ©️ OpenZFS 2018-current and is licensed under Apache License 2.0
