from dotenv import load_dotenv
import os

load_dotenv()

HOST_USER = os.getenv('EMAIL_HOST_USER')
HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
HOST = os.getenv('EMAIL_HOST')

SUPER_USER = os.getenv('SUPER_USER')
SUPER_USER_FIRST_NAME = os.getenv('SUPER_USER_FIRST_NAME')
SUPER_USER_LAST_NAME = os.getenv('SUPER_USER_LAST_NAME')
SUPER_USER_PASSWORD = os.getenv('SUPER_USER_PASSWORD')

BD_NAME = os.getenv('BD_NAME')
BD_USER = os.getenv('BD_USER')
