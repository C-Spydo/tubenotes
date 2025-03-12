from . import routes_blueprint
from ..error_handler import url_validation_error_handler
from ..helpers import create_response
from ..constants import SUCCESS_MESSAGE, INDUSTRIES
from ..enums import CustomStatusCode


@routes_blueprint.route('/industries', methods=['GET'])
def list_industries():
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, INDUSTRIES), 200


