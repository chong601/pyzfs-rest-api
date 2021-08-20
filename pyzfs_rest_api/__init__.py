from flask import Flask
from flask_restx import Api

app = Flask('__main__')
# Flask-RESTX: Disable X-Fields entry on Swagger
app.config['RESTX_MASK_SWAGGER'] = False
# Remove default message
app.config['ERROR_INCLUDE_MESSAGE'] = False
# Should I add a database here...
# HMMMMMMMM

# Create base Flask-RESTX API
api = Api(app, 'alpha', 'PyZFS REST API', 'A thin wrapper that extends ZFS filesystem through libzfs_core and PyZFS')


from pyzfs_rest_api.namespaces.zpool import api as zpool_api

api.add_namespace(zpool_api)
