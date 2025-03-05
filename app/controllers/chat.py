from . import routes_blueprint
from ..services import chat
from ..services import stock_scraper
from flask import request
# from flask_parameter_validation import ValidateParameters, Query
from typing import Optional
from ..error_handler import url_validation_error_handler
from ..helpers import create_response
from ..constants import SUCCESS_MESSAGE
from ..enums import CustomStatusCode

@routes_blueprint.route('/start-chat', methods=['POST'])
def start_chat():
    response = chat.start_chat(request.get_json())
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, response), 200

@routes_blueprint.route('/prompt', methods=['POST'])
def prompt_bot():
    response = chat.prompt_bot(request.get_json())
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, response), 200

@routes_blueprint.route('/ping', methods=['GET'])
def ping():
    return create_response(CustomStatusCode.SUCCESS.value, "API is Awake"), 200


@routes_blueprint.route('/scrape', methods=['GET'])
def scrape():
    response = stock_scraper.scrape_stocks(["TSLA"])
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, response), 200

