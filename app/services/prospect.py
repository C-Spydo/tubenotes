from ..models import Prospect
from ..helpers import add_record_to_database
from ..repository.base import get_list

def add_prospect(request: dict):
    prospect = Prospect(
        industry_id=request['industry_id'],
        company_name=request['company_name'],
        contact_name=request['contact_name'],
        contact_email=request['contact_email'],
        contact_phone=request['contact_phone']
    )

    add_record_to_database(prospect)
    return prospect.serialize()

def get_prospects():
    prospects = get_list(Prospect)

    serialized_prospects = [prospect.serialize() for prospect in prospects]

    return {'prospects': serialized_prospects}