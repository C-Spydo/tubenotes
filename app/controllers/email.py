from app.models.email import Email
from app.repository.base import get_record_by_field, get_list
from app.services.cold_mail import generate_cold_mail, resend_cold_mail, send_cold_mail
from . import routes_blueprint
from ..error_handler import url_validation_error_handler
from flask_parameter_validation import ValidateParameters, Route, Json
from ..helpers import create_response
from ..constants import SUCCESS_MESSAGE
from ..enums import CustomStatusCode

@routes_blueprint.route('/emails/generate/<int:prospect_id>', methods=['GET'])
@ValidateParameters(url_validation_error_handler)
def generate_email(prospect_id: int = Route()):
    data = generate_cold_mail(prospect_id)
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, data), 200

@routes_blueprint.route('/emails', methods=['GET'])
def get_cold_emails():
    emails = [email.serialize() for email in get_list(Email)]
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, {"emails": emails}), 200

@routes_blueprint.route('/emails/<int:id>', methods=['GET'])
@ValidateParameters(url_validation_error_handler)
def get_email(id:int = Route()):
    email = get_record_by_field(Email, 'id', id).serialize()
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, email), 200

@routes_blueprint.route('/emails', methods=['POST'])
@ValidateParameters(url_validation_error_handler)
def send_email(prospect_id:int = Json(), title:str = Json(), email_body:str = Json()):
    send_cold_mail(prospect_id, title, email_body)
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE), 200

@routes_blueprint.route('/emails/<int:id>/resend', methods=['POST'])
@ValidateParameters(url_validation_error_handler)
def resend_email(id:int = Route()):
    resend_cold_mail(id)
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE), 200
