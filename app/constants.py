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



