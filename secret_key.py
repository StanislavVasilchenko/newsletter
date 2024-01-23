from dotenv import load_dotenv
import os

load_dotenv()

HOST_USER = os.getenv('EMAIL_HOST_USER')
HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
HOST = os.getenv('EMAIL_HOST')