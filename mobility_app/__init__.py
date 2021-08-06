from flask import Flask

mobility_app = Flask(__name__, instance_relative_config=True)

from mobility_app import views

mobility_app.config.from_object('config')