from .chains import get_cold_mail_chain
from ..repository.base import get_list, get_record_by_field
from ..models import Prospect

def generate_cold_mail(prospect_id: int):
    prospect = get_record_by_field(Prospect, 'id', prospect_id).serialize()

    chain = get_cold_mail_chain()

    email_data = chain.invoke({'name': prospect['contact_name'], 'industry': prospect['industry']})

    return {'email_body': email_data['branches']['email'], 'email_title': email_data['branches']['title']}