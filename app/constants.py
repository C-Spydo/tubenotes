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
INVALID_CREDENTIALS = 'Invalid Credentials'


DUMMY_EMAIL ="""Dear [Recipient's Name],

I hope you're doing well. I'm [Your Name] from [Your Insurance Company], and I wanted to reach out to see how we can help you secure your future with tailored insurance solutions.

Whether you're looking for [life, health, auto, home, or business insurance], we offer competitive plans designed to provide the best coverage at the right price. Our team takes pride in delivering personalized service, ensuring that you get a policy that truly meets your needs.

I'd love to schedule a quick call to discuss how we can help you. Are you available this week for a short chat?
"""

INDUSTRIES = [
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



