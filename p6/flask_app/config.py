import os

# Stores all configuration values
SECRET_KEY = os.getenv("SECRET_KEY") 
MONGODB_HOST = os.getenv("MONGODB_HOST")

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_DEFAULT_SENDER = 'projectdiary388j@gmail.com'
MAIL_USERNAME = 'projectdiary388j@gmail.com'
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")