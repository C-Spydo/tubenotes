from . import routes_blueprint
from .industry import industries
from ..error_handler import url_validation_error_handler
from flask_parameter_validation import ValidateParameters, Json
from ..helpers import create_response
from ..constants import SUCCESS_MESSAGE
from ..enums import CustomStatusCode
from ..services.prospect import add_prospect
from flask import request
import random


@routes_blueprint.route('/prospects', methods=['GET'])
def list_prospects():
    industries_lookup = {industry["id"]: industry["name"] for industry in industries}  # Convert industries to a lookup dictionary

    prospects = []
    for i in range(1, 11):  # Generate 10 prospects
        industry_id = random.randint(1, 50)
        prospect = {
            "company_name": f"Company {i}",
            "industry_id": industry_id,
            "industry_name": industries_lookup.get(industry_id, "Unknown Industry"),
            "contact_name": f"Contact {i}",
            "contact_email": f"contact{i}@company{i}.com",
            "contact_phone": f"+123456789{i}"
        }
        prospects.append(prospect)

    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, prospects), 200

@routes_blueprint.route('/prospects', methods=['POST'])
@ValidateParameters(url_validation_error_handler)
def create_prospect(industry_id:int = Json(), company_name:str = Json(), contact_name:str = Json(), contact_email:str = Json(), contact_phone:str = Json()):
    prospect = add_prospect(request.json())
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, prospect), 201

