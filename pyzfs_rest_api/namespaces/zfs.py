from flask_restx import Namespace, fields, Resource, abort
from flask_restx.marshalling import marshal_with
from flask import request
from pylibzfs.pyzfs import zfs_list
from pylibzfs.pylibzfs_core import lzc_exists
from urllib.parse import unquote

api = Namespace('zfs', 'Operations related to zfs')

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



