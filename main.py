import argparse
import os
import sys
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def shorten_link(token, link):
    api_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    long_link = {'long_url': link}
    response = requests.post(api_url, headers={'Authorization': f'Bearer {token}'}, json=long_link)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, bitlink):
    bitlink = urlparse(bitlink)
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink.netloc + bitlink.path}/clicks/summary'
    response = requests.get(api_url, headers={'Authorization': f'Bearer {token}'})
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(token, link):
    shorted_link = False
    parsed = urlparse(link)
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{parsed.netloc + parsed.path}'
    response = requests.get(api_url, headers={'Authorization': f'Bearer {token}'})
    if response.ok:
        shorted_link = True
    return shorted_link


def main():
    parser = argparse.ArgumentParser(description='Long links to bitlinks or quantity bitlinks clicks')
    parser.add_argument('link', type=str, help='Enter the link you want to shorten')
    args = parser.parse_args()

    bitly_bearer_token = os.environ['BITLY_BEARER_TOKEN']

    try:
        if not is_bitlink(bitly_bearer_token, args.link):
            bitlink = shorten_link(bitly_bearer_token, args.link)
            print('Битлинк: ', bitlink)
        else:
            clicks_count = count_clicks(bitly_bearer_token, args.link)
            print('Всего кликов: ', clicks_count)
    except requests.exceptions.HTTPError as error:
        print(f'Enter correct link\n {error}')
        sys.exit()


if __name__ == "__main__":
    load_dotenv()
    main()
