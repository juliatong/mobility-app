from flask import current_app, request, jsonify

from . import backend as backend_blueprint

@backend_blueprint.route('/regions')
def regions():
  geo_type = request.args['geoType']

  with current_app.config.mysql.get_db().cursor() as cursor:
    sql = "SELECT `id`, `name` FROM `regions` WHERE `geo_type` = %s"
    cursor.execute(sql, (geo_type,))

    regions_list = [dict((cursor.description[i][0], value)
                          for i, value in enumerate(row)) for row in cursor.fetchall()]

  return jsonify({'geoType': geo_type, 'regions': regions_list})


@backend_blueprint.route('/locations')
def locations():
  region_id = request.args['region_id']

  with current_app.config.mysql.get_db().cursor() as cursor:
    sql = "SELECT `locations`.`id`, `regions`.`name` as `region_name`, `regions`.`geo_type`, `locations`.`sub_region`, `locations`.`country`, `locations`.`alternative_name` FROM `locations` INNER JOIN `regions` ON `locations`.`region_id` = `regions`.`id` WHERE `locations`.`region_id` = %s"
    cursor.execute(sql, (int(region_id),))

    locations_list = [dict((cursor.description[i][0], value)
                          for i, value in enumerate(row)) for row in cursor.fetchall()]

  return jsonify({'locations': locations_list})