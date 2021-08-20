from flask_restx import Namespace, fields, Resource, abort
from flask_restx.marshalling import marshal_with
from pyzfs import zpool_list, zfs_get_running_version, zpool_list_model
from pylibzfs_core import lzc_exists

api = Namespace('zpool', 'Operations related to zpool')

zpool_list_model = api.model('zpool_list', {
    'name': fields.String(title='Pool name'),
    'allocated': fields.Integer(title='allocated', description='Amount of storage used within the pool'),
    'capacity': fields.Integer(title='capacity', description='Percentage of pool space used'),
    'expandsize': fields.Integer(title='expandsize', description='Amount of uninitialized space within the pool or device that can be used to increase the total capacity of the pool'),
    'fragmentation': fields.Integer(title='fragmentation', description='The amount of fragmentation in the pool'),
    'free': fields.Integer(title='free', description='The amount of free space on the pool'),
    'freeing': fields.String(title='freeing', description='Amount of space remaining to be reclaimed.'),
    'dedupratio': fields.Float(title='dedupratio', description='Pool dedup ratio'),
    'health': fields.String(title='health', description='The current health of the pool'),
    'guid': fields.Integer(title='guid', description='Permanent unique identifier for the pool'),
    'load_guid': fields.Integer(title='load_guid', description='Currently-loaded unique identifier for the pool.'),
    'size': fields.Integer(title='size', description='Total size of the pool'),
    'altroot': fields.String(title='altroot', description='Alternative root directory'),
    'readonly': fields.String(title='readonly', description='Pool read-only status'),
    'ashift': fields.Integer(title='ashift', description='Pool sector size exponent'),
    'autoexpand': fields.String(title='autoexpand', description='Controls automatic pool expansion when the underlying LUN is grown'),
    'autoreplace': fields.String(title='autoreplace', description='Controls automatic device replacement'),
    'autotrim': fields.String(title='autotrim', description='Pool auto-trim status'),
    'bootfs': fields.String(title='bootfs', description='Bootable dataset for the pool'),
    'cachefile': fields.String(title='cachefile', description='Location of the pool configuration is stored'),
    'comment': fields.String(title='comment', description='Pool comment'),
    'delegation': fields.String(title='delegation', description='Pool delegation setting'),
    'failmode': fields.String(title='failmode', description='Pool behavior when pool failure occurs'),
    # Skip feature for now.
    'listsnapshots': fields.String(title='listsnapshots', description='Whether to list snapshot on zfs list'),
    'multihost': fields.String(title='multihost', description='Whether the pool will be checked during import to prevent importing an active pool'),
    'version': fields.Integer(title='version', description='Version of the pool (legacy ZFS only)')
})


@api.route('/list')
class ZFSList(Resource):

    @api.marshal_with(zpool_list_model, as_list=True, skip_none=True)
    def get(self):
        return zpool_list()

@api.route('/list/<name>')
class ZFSListByName(Resource):

    @api.marshal_with(zpool_list_model, as_list=True, skip_none=True)
    
    def get(self, name):
        if not lzc_exists(name):
            abort(404, error=f"Pool '{name}' not found")
        return 
