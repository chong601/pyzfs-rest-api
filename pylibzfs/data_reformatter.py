"""
Used to reformat the output of zpool and zfs data as the cmdline output tend to use their shorthand
name rather than full property name
"""

# Dictionary to relabel zpool name returned column names to the full name
ZPOOL_LIST = {
    'cap': 'capacity',
    'replace': 'autoreplace',
    'listsnaps': 'listsnapshots',
    'expand': 'autoexpand',
    'dedup': 'dedupratio',
    'alloc': 'allocated',
    'rdonly': 'readonly',
    'expandsz': 'expandsize',
    'frag': 'fragmentation',
    'ckpoint': 'checkpoint'
}

# Dictionary to relabel zfs name returned column names to the full name
ZFS_LIST = {
    'avail': 'available',
    'ratio': 'compressratio',
    'encroot': 'encryptionroot',
    'fscount': 'filesystem_count',
    'lrefer': 'logicalreferenced',
    'lused': 'logicalused',
    'resumetok': 'receive_resume_token',
    'rsnaps': 'redact_snaps',
    'refratio': 'refcompressratio',
    'refer': 'referenced',
    'sscount': 'snapshot_count',
    'usedchild': 'usedbychildren',
    'usedds': 'usedbydataset',
    'usedrefreserv': 'usedbyrefreservation',
    'usedsnap': 'usedbysnapshots',
    'case': 'casesensitivity',
    'compress': 'compression',
    'dnsize': 'dnodesize',
    'fslimit': 'filesystem_limit',
    'rdonly': 'readonly',
    'recsize': 'recordsize',
    'redund_md': 'redundant_metadata',
    'refreserv': 'refreservation',
    'reserv': 'reservation',
    'sslimit': 'snapshot_limit',
    'volblock': 'volblocksize'
}