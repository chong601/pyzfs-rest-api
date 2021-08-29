from flask_restx import Namespace, fields, Resource, abort
from flask_restx.marshalling import marshal_with
from flask import request
from pylibzfs.pyzfs import zfs_list
from pylibzfs.pylibzfs_core import lzc_exists
from urllib.parse import unquote

api = Namespace('zfs', 'Operations related to zfs')

zfs_list_model = api.model('zfs_list', {
    'type': fields.String(title='ZFS dataset type', example='filesystem | snapshot | volume'),
    'creation': fields.Integer(title='Creation timestamp'),
    'used': fields.Integer(title='Used space', description='Value in bytes'),
    'available': fields.Integer(title='Available space available to dataset and all its children', description='Value in bytes'),
    'referenced': fields.Integer(title='Referenced space', description='Value in bytes'),
    'compressratio': fields.Float(title='Compression ratio for dataset and the descendents'),
    'mounted': fields.Boolean(title='Mounted status'),
    'quota': fields.Integer(title='Amount the space the dataset and its descendents can use'),
    'reservation': fields.Integer(title='Minimum amount of space guaranteed to a dataset and its descendents'),
    'recordsize': fields.Integer('Dataset recordsize'),
    'mountpoint': fields.String(title='Mount point location for the dataset'),
    'sharenfs': fields.String(title='Indicates whether the dataset is shared over NFS', description='Valid values are on, off or NFS options'),
    'checksum': fields.String(title='Dataset checksum configuration'),
    'compression': fields.String(title='Dataset compression configuration'),
    'atime': fields.Boolean(title='atime configuration for dataset'),
    'devices': fields.Boolean(title='Dataset device node support', description='Equivalent to "dev" and "nodev" mount options'),
    'exec': fields.Boolean(title='Dataset process execution support', description='Equivalent to "exec" and "noexec" mount options'),
    'setuid': fields.String(title='Dataset setuid support', description='Equivalent to "suid" and "nosuid" mount options'),
    'readonly': fields.Boolean(title='Dataset read only status', description='Equivalent to "ro" and "rw" mount options'),
    'zoned': fields.Boolean(title='Whether this dataset is managed from Solaris zones.', description='Not relevant in non-Solaris systems'),
    'snapdir': fields.String(title='Visibility of .zfs directory on the root of the filesystem')
# zfs_list_model = api.model('zfs_list', {


#     'type'
#     'creation'
#     'used'
#     'available'
#     'referenced'
#     'compressratio'
#     'mounted'
#     'quota'
#     'reservation'
#     'recordsize'
#     'mountpoint'
#     'sharenfs'
#     'checksum'
#     'compression'
#     'atime'
#     'devices'
#     'exec'
#     'setuid'
#     'readonly'
#     'zoned'
#     'snapdir'
#     'aclmode'
#     'aclinherit'
#     'createtxg'
#     'canmount'
#     'xattr'
#     'copies'
#     'version'
#     'utf8only'
#     'normalization'
#     'casesensitivity'
#     'vscan'
#     'nbmand'
#     'sharesmb'
#     'refquota'
#     'refreservation'
#     'guid'
#     'primarycache'
#     'secondarycache'
#     'usedbysnapshots'
#     'usedbydataset'
#     'usedbychildren'
#     'usedbyrefreservation'
#     'logbias'
#     'objsetid'
#     'dedup'
#     'mlslabel'
#     'sync'
#     'dnodesize'
#     'refcompressratio'
#     'written'
#     'logicalused'
#     'logicalreferenced'
#     'volmode'
#     'filesystem_limit'
#     'snapshot_limit'
#     'filesystem_count'
#     'snapshot_count'
#     'snapdev'
#     'acltype'
#     'context'
#     'fscontext'
#     'defcontext'
#     'rootcontext'
#     'relatime'
#     'redundant_metadata'
#     'overlay'
#     'encryption'
#     'keylocation'
#     'keyformat'
#     'pbkdf2iters'
#     'special_small_blocks'

# })
})

"""
name=None, sort_ascending:str=None, depth: int=None, property: list=None, recursive=False, type=None, detail=False
"""
zfs_request_model = api.model('zfs_request', {
    'name': fields.String(title='Dataset name'),
    'sort_order': fields.String(title='Property sort order', description='Format is \<property name\>,<0/1>'),
    'depth': fields.Integer(title='ZFS list recursion depth'),
    'property': fields.List(fields.String(title='Property list', description='List of property to get')),
    'recursive': fields.Boolean(title='Recursively get all datasets', default=False),
    'type': fields.List(fields.String(title='List which ZFS vdev type'))
})

@api.route('/list')
class ZFSList(Resource):
    @api.expect(zfs_request_model)
    def post(self):
        if not request.is_json:
            abort(400, error='Must be JSON')
        kw_args = {}
        data = request.json
        if 'name' in data:
            kw_args['name'] = data['name']
        if 'sort_order' in data:
            kw_args['sort_order'] = data['sort_order']
        if 'depth' in data:
            kw_args['depth'] = data['depth']
        if 'property' in data:
            kw_args['property'] = data['property']
        if 'type' in data:
            kw_args['type'] = data['type']
        return zfs_list(**kw_args)
