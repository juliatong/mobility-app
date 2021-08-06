from flask import Blueprint, request, json

backend = Blueprint('backend', __name__)

from . import views