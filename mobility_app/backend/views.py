from flask import current_app, request, jsonify

from . import backend as backend_blueprint

@backend_blueprint.route('/regions')
def regions():
  geo_type = request.args['geoType']

  try:
    with current_app.config.mysql.get_db().cursor() as cursor:
      sql = "SELECT `id`, `name` FROM `regions` WHERE `geo_type` = %s"
      cursor.execute(sql, (geo_type,))

      regions_list = [dict(row) for row in cursor.fetchall()]
      return jsonify({'geoType': geo_type, 'regions': regions_list})
  except:
    return jsonify({'error': 'Unable to find regions'})


@backend_blueprint.route('/locations')
def locations():
  region_id = request.args['region_id']

  try:
    with current_app.config.mysql.get_db().cursor() as cursor:
      sql = "SELECT `locations`.`id`, `regions`.`name` as `region_name`, `regions`.`geo_type`, `locations`.`sub_region`, `locations`.`country`, `locations`.`alternative_name` FROM `locations` INNER JOIN `regions` ON `locations`.`region_id` = `regions`.`id` WHERE `locations`.`region_id` = %s"
      cursor.execute(sql, (int(region_id),))

      locations_list = [dict(row) for row in cursor.fetchall()]

    return jsonify({'locations': locations_list})
  except:
    return jsonify({'error': 'Unable to find locations'})


@backend_blueprint.route('/traffic', methods=['POST'])
def traffic():
  geo_type = request.form['geoType']
  region_id = request.form['region']
  # show_transit = request.form['showTransit']
  # show_driving = request.form['showDriving']
  # show_walking = request.args['showWalking']
  # traffic_filter_modifier = request.args['trafficFilterModifier']
  # traffic_filter_amt = request.args['trafficFilterAmt']

  try:
    if geo_type and region_id:
      with current_app.config.mysql.get_db().cursor() as cursor:
        sql = '''
          SELECT `locations`.`id`, `regions`.`name` as `region_name`, `regions`.`geo_type`, `locations`.`sub_region`, `locations`.`country`, `locations`.`alternative_name`
          FROM `locations` INNER JOIN `regions` ON `locations`.`region_id` = `regions`.`id`
          '''

        where_statements = []
        where_conditions = {}
        if (geo_type != 'all'):
          where_statements.append('`regions`.`geo_type` = %(geo_type)s')
          where_conditions['geo_type'] = geo_type

        if (region_id != 'all'):
          where_statements.append('`locations`.`region_id` = %(region_id)s')
          where_conditions['region_id'] = region_id

        if len(where_statements) > 0:
          sql += 'WHERE'
          sql += ' AND '.join(where_statements)

        cursor.execute(sql, where_conditions)

        locations_list = [dict(row) for row in cursor.fetchall()]

        return jsonify({'locations':locations_list})
    else:
      return jsonify({'error':'Enter the required fields'})
  except:
    return jsonify({'error': 'Unable to retrieve traffic data'})
