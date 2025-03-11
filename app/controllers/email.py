from . import routes_blueprint
from .industry import industries
from ..error_handler import url_validation_error_handler
from flask_parameter_validation import ValidateParameters, Json
from ..helpers import create_response
from ..constants import SUCCESS_MESSAGE
from ..enums import CustomStatusCode

@routes_blueprint.route('/email', methods=['GET'])
def generate_email():
    email = """Dear [Recipient's Name],

    I hope you're doing well. I'm [Your Name] from [Your Insurance Company], and I wanted to reach out to see how we can help you secure your future with tailored insurance solutions.

    Whether you're looking for [life, health, auto, home, or business insurance], we offer competitive plans designed to provide the best coverage at the right price. Our team takes pride in delivering personalized service, ensuring that you get a policy that truly meets your needs.

    I'd love to schedule a quick call to discuss how we can help you. Are you available this week for a short chat?
    """
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, email), 200

@routes_blueprint.route('/emails', methods=['GET'])
def get_cold_emails():
    email = """Dear [Recipient's Name],

    I hope you're doing well. I'm [Your Name] from [Your Insurance Company], and I wanted to reach out to see how we can help you secure your future with tailored insurance solutions.

    Whether you're looking for [life, health, auto, home, or business insurance], we offer competitive plans designed to provide the best coverage at the right price. Our team takes pride in delivering personalized service, ensuring that you get a policy that truly meets your needs.

    I'd love to schedule a quick call to discuss how we can help you. Are you available this week for a short chat?
    """
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, email), 200