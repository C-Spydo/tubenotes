from flask import Blueprint

routes_blueprint = Blueprint(
    'routes', __name__
)

from . import chat
from . import auth
from . import industry