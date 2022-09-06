import os
import sys

from dotenv import load_dotenv

load_dotenv()

try:
    BITLY_BEARER_TOKEN = os.environ['BITLY_BEARER_TOKEN']
except KeyError as error:
    print('Missing authorization token')
    sys.exit()
