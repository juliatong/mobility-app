from flask import Flask

mobility_app = Flask(__name__, instance_relative_config=True)

from .backend import backend as backend_blueprint
mobility_app.register_blueprint(backend_blueprint, url_prefix='/api')

from mobility_app import views

mobility_app.config.from_object('config')