import os
from flask import Flask

mobility_app = Flask(__name__, instance_relative_config=True)

from .backend import backend as backend_blueprint

mobility_app.register_blueprint(backend_blueprint, url_prefix='/api')

from mobility_app import views

from dotenv import load_dotenv

load_dotenv()

from flaskext.mysql import MySQL

mysql = MySQL()

mobility_app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER', 'root')
mobility_app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD', '')
mobility_app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE_DB', 'mobility_data')
mobility_app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DATABASE_HOST', 'localhost')

mysql.init_app(mobility_app)

mobility_app.config.mysql = mysql