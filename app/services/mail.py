from flask import render_template
from flask_mail import Message
from ..extensions import mail
from ..constants import *

def send_mail(recipients: list[str]):
    message = curate_cold_mail(recipients)

    try:
        mail.send(message)
    except Exception as e:
        print(EMAIL_ERROR_MESSAGE.replace("XX", str(e)))

    

def curate_cold_mail(recipients: list[str]) -> Message:
    mail_title = 'Hi there!'

    email_body = 'Hola'
    # html_email_body = render_template('email_notification_template.html', water_quality_data = water_quality_data, location=location)

    message = Message(mail_title, sender=("Icebreaking Insurance", ICEBREAKER_EMAIL), recipients=recipients)
    
    # message.html = email_body?
    message.body = email_body

    return message

   