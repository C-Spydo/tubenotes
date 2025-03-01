from flask import request
from app.constants import SUCCESS_MESSAGE
from app.enums.custom_status_code import CustomStatusCode
from app.helpers import create_response
from app.services import user
from . import routes_blueprint

@routes_blueprint.route('/sign-in', methods=['POST'])
def sign_in():
    response = user.sign_in(request.get_json()["username"])
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, response), 200