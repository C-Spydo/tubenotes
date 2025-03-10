from . import routes_blueprint
from ..error_handler import url_validation_error_handler
from ..helpers import create_response
from ..constants import SUCCESS_MESSAGE
from ..enums import CustomStatusCode


@routes_blueprint.route('/industries', methods=['GET'])
def list_industries():
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, industries), 200


industries = [
    {"id": 1, "name": "Engineering"},
    {"id": 2, "name": "Fashion"},
    {"id": 3, "name": "Commerce"},
    {"id": 4, "name": "Technology"},
    {"id": 5, "name": "Healthcare"},
    {"id": 6, "name": "Education"},
    {"id": 7, "name": "Finance"},
    {"id": 8, "name": "Real Estate"},
    {"id": 9, "name": "Marketing"},
    {"id": 10, "name": "Entertainment"},
    {"id": 11, "name": "Automotive"},
    {"id": 12, "name": "Manufacturing"},
    {"id": 13, "name": "Agriculture"},
    {"id": 14, "name": "Hospitality"},
    {"id": 15, "name": "Telecommunications"},
    {"id": 16, "name": "Retail"},
    {"id": 17, "name": "Legal"},
    {"id": 18, "name": "Construction"},
    {"id": 19, "name": "Energy"},
    {"id": 20, "name": "Aerospace"},
    {"id": 21, "name": "Pharmaceuticals"},
    {"id": 22, "name": "Biotechnology"},
    {"id": 23, "name": "Media & Journalism"},
    {"id": 24, "name": "Cybersecurity"},
    {"id": 25, "name": "Data Science & Analytics"},
    {"id": 26, "name": "Artificial Intelligence"},
    {"id": 27, "name": "Blockchain"},
    {"id": 28, "name": "E-commerce"},
    {"id": 29, "name": "Food & Beverage"},
    {"id": 30, "name": "Travel & Tourism"},
    {"id": 31, "name": "Sports & Recreation"},
    {"id": 32, "name": "Environmental Services"},
    {"id": 33, "name": "Logistics & Supply Chain"},
    {"id": 34, "name": "Government & Public Services"},
    {"id": 35, "name": "Non-Profit & NGOs"},
    {"id": 36, "name": "Event Management"},
    {"id": 37, "name": "Luxury Goods & Jewelry"},
    {"id": 38, "name": "Insurance"},
    {"id": 39, "name": "Human Resources & Recruitment"},
    {"id": 40, "name": "Printing & Publishing"},
    {"id": 41, "name": "Petroleum & Mining"},
    {"id": 42, "name": "Shipping & Maritime"},
    {"id": 43, "name": "Waste Management"},
    {"id": 44, "name": "Fitness & Wellness"},
    {"id": 45, "name": "Interior Design"},
    {"id": 46, "name": "Music & Performing Arts"},
    {"id": 47, "name": "Social Media & Influencing"},
    {"id": 48, "name": "Video Game Development"},
    {"id": 49, "name": "Tattoo & Body Art"},
    {"id": 50, "name": "Spiritual & Religious Services"}
]