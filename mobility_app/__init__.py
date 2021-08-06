from flask import Flask

mobility_app = Flask(__name__, instance_relative_config=True)


from .backend import backend as backend_blueprint

mobility_app.register_blueprint(backend_blueprint, url_prefix='/api')

from mobility_app import views

mobility_app.config.from_object('config')

from flaskext.mysql import MySQL

mysql = MySQL()

mobility_app.config['MYSQL_DATABASE_USER'] = 'root'
mobility_app.config['MYSQL_DATABASE_PASSWORD'] = 'media1234'
mobility_app.config['MYSQL_DATABASE_DB'] = 'mobility_data'
mobility_app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(mobility_app)

mobility_app.config.mysql = mysql