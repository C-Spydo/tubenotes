from app.constants import SUCCESS_MESSAGE
from app.enums.custom_status_code import CustomStatusCode
from app.error_handler import url_validation_error_handler
from app.helpers import create_response, token_required
from app.services import notebook
from app.repository import base
from app.models import Notebook
from flask_parameter_validation import ValidateParameters, Query, Route
from . import routes_blueprint

@routes_blueprint.route('/dashboard/<int:user_id>', methods=['GET'])
@ValidateParameters(url_validation_error_handler)
def get_note_from_query(user_id:int = Route()):
    data = notebook.get_note_from_query(user_id, query)
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, data), 200