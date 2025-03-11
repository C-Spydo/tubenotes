from . import routes_blueprint
from .industry import industries
from ..error_handler import url_validation_error_handler
from flask_parameter_validation import ValidateParameters, Json, Route
from ..helpers import create_response
from ..constants import SUCCESS_MESSAGE
from ..enums import CustomStatusCode
from ..services.prospect import add_prospect, get_prospects, get_prospect_by_id
from flask import request
import random


@routes_blueprint.route('/prospects', methods=['GET'])
def list_prospects():
    prospects = get_prospects()
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, prospects), 200

@routes_blueprint.route('/prospects', methods=['POST'])
@ValidateParameters(url_validation_error_handler)
def create_prospect(industry_id:int = Json(), company_name:str = Json(), contact_name:str = Json(), contact_email:str = Json(), contact_phone:str = Json()):
    prospect = add_prospect(request.get_json())
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, prospect), 201

@routes_blueprint.route('/prospects/<int:id>', methods=['GET'])
@ValidateParameters(url_validation_error_handler)
def get_prospect(id: int = Route()):
    prospect = get_prospect_by_id(id)
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, prospect), 200