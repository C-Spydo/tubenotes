from app.constants import INDUSTRIES
from flask import abort

def get_industry_name(industry_id):
    for industry in INDUSTRIES:
        if industry["id"] == industry_id:
            return industry["name"]
        
    abort(404, 'Industry not found')