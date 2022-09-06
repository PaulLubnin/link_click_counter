import os

from dotenv import load_dotenv

load_dotenv()

BITLY_BEARER_TOKEN = os.environ.get('BITLY_BEARER_TOKEN')
