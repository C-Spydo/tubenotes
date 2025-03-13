from flask import render_template, abort
from flask_mail import Message
from ..extensions import mail, session
from ..constants import *
from datetime import datetime 
from ..models import Email
from ..enums import EmailStatus
from ..helpers import add_record_to_database

def send_mail(recipients: list[str], email: Email):
    message = curate_cold_mail((email.title, email.message), recipients)
    try:
        mail.send(message)
        add_record_to_database(email)
    except Exception as e:
        email.status = EmailStatus.FAILED.value
        add_record_to_database(email)
        abort(500, 'Something is broken, pls try again later')

def resend_mail(email: Email):
    message = curate_cold_mail((email.title, email.message), [email.prospect.contact_email])

    try:
        mail.send(message)
        email.update_status(EmailStatus.SENT.value)
    except Exception as e:
        email.update_status(EmailStatus.FAILED.value)
        abort(500, 'Something is broken, pls try again later')


def curate_cold_mail(email: tuple[str, str], recipients: list[str]) -> Message:
    email_body_paragraphs = email[1].split("\n") 

    html_email_body = render_template('email.html', year=datetime.now().year, email_body=email_body_paragraphs)

    message = Message(email[0], sender=("Icebreaking Insurance", ICEBREAKER_EMAIL), recipients=recipients)
    
    message.html = html_email_body

    return message

   
