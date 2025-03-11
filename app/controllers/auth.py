from flask import request, abort 
from app.constants import SUCCESS_MESSAGE, GOOGLE_CLIENT_ID
from app.enums.custom_status_code import CustomStatusCode
from app.error_handler import url_validation_error_handler
from app.helpers import create_response, get_record_by_field, add_record_to_database, generate_jwt_token, token_required
from app.models import User, UserSession
from flask_parameter_validation import ValidateParameters, Json
from . import routes_blueprint
from ..extensions.database import session


@routes_blueprint.route("/api/auth/google", methods=["POST"])
@ValidateParameters(url_validation_error_handler)
def google_login(name: str = Json(), email: str = Json(), google_id: str = Json()):
    # data = request.get_json()

    # name = data.get("name")
    # email = data.get("email")
    # google_id = data.get("google_id")

    # if not all([name, email, google_id]):
    #     return create_response(CustomStatusCode.BAD_REQUEST.value, "Missing required fields"), 400

    try:
        user = get_record_by_field(User, "google_id", google_id)

        if not user:
            user = User(username=name, email=email, google_id=google_id)
            add_record_to_database(user)

        token = generate_jwt_token(user)
        session = UserSession(user_id=user.id, token=token)
        add_record_to_database(session)

        return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, {"id": user.id, "token":token,
                                                                                 "email": email, "name": name}), 200

    except ValueError:
        return create_response(CustomStatusCode.BAD_REQUEST.value, "Invalid Token"), 400

@routes_blueprint.route('/logout', methods=['POST'])
@token_required
def logout(user_id):
    UserSession.query.filter_by(user_id=user_id).delete()
    session.commit()
    return create_response(CustomStatusCode.SUCCESS.value, "Logged out successfully!"), 200

@routes_blueprint.route('/ping', methods=['GET'])
def ping():
    return create_response(CustomStatusCode.SUCCESS.value, "API is Awake"), 200

@routes_blueprint.route('/dashboard', methods=['GET'])
def dashboard():
    data = {
        "total_emails": 1234,
        "total_prospects": 567,
        "total_cold_calls": 89,
        "api_status": "Alive"
    }
    return create_response(CustomStatusCode.SUCCESS.value, "Dashboard Data Retrieved", data), 200

