import os 

DATABASE_URL = os.getenv('DATABASE_URL')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

#Flask Config
APP_SECRET_KEY = os.getenv('APP_SECRET_KEY')

ICEBREAKER_EMAIL= os.getenv('ICEBREAKER_EMAIL')
ICEBREAKER_MAIL_PASSWORD= os.getenv('ICEBREAKER_MAIL_PASSWORD')
EMAIL_ERROR_MESSAGE = "Failed to send mail: \n\nError message 'XX'"

#Repsonse Messages
NOT_FOUND_MESSAGE = 'Not found'
SUCCESS_MESSAGE = 'Success'
INTERNAL_SERVER_ERROR_MESSAGE = 'Something went wrong'


DUMMY_EMAIL ="""Dear [Recipient's Name],

I hope you're doing well. I'm [Your Name] from [Your Insurance Company], and I wanted to reach out to see how we can help you secure your future with tailored insurance solutions.

Whether you're looking for [life, health, auto, home, or business insurance], we offer competitive plans designed to provide the best coverage at the right price. Our team takes pride in delivering personalized service, ensuring that you get a policy that truly meets your needs.

I'd love to schedule a quick call to discuss how we can help you. Are you available this week for a short chat?
"""



