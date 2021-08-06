from flask import request, json

from . import backend as backend_blueprint

@backend_blueprint.route('/regions')
def regions():
  geo_type = request.args['geoType']
  return json.dumps({'geoType': geo_type, 'regions': []})