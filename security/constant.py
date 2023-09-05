from os import environ
from dotenv import load_dotenv

load_dotenv()

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError('No SECRET_KEY set for FastAPI OAuth2 server. ' 
                     'Did you forget to set it in .env?')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30