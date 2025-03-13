from app.services.smtp_mail import send_mail, resend_mail
from .chains import get_cold_mail_chain
from ..repository.base import get_list, get_record_by_field
from ..models import Prospect, Email
from ..enums import EmailStatus

def generate_cold_mail(prospect_id: int):
    prospect = get_record_by_field(Prospect, 'id', prospect_id).serialize()

    chain = get_cold_mail_chain()

    email_data = chain.invoke({'industry': prospect['industry']})

    return {'email_body': email_data['email'], 'email_title': email_data['title']}

def send_cold_mail(prospect_id: int, title: str, body:str):
    prospect = get_record_by_field(Prospect, 'id', prospect_id).serialize()

    email = Email(prospect_id=prospect_id, title=title, message=body, status=EmailStatus.SENT.value)

    send_mail([prospect['contact_email']], email)

def resend_cold_mail(id: int):
    email = get_record_by_field(Email, 'id', id)

    resend_mail(email)
