import os

# Stores all configuration values
SECRET_KEY = os.getenv("SECRET_KEY") #b'\x020;yr\x91\x11\xbe"\x9d\xc1\x14\x91\xadf\xec'
MONGODB_HOST = os.getenv("MONGODB_HOST")

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_DEFAULT_SENDER = 'projectdiary388j@gmail.com'
MAIL_USERNAME = 'Project Diary'
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD") #'tasbcbuxdwulngpp' #cmscconfirm123