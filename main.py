import argparse
import sys
from urllib.parse import urlparse

import requests

from settings import BITLY_BEARER_TOKEN


def get_shorten_link(token, link):
    bitlinks_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    data = {'long_url': link}
    response = requests.post(bitlinks_url, headers={'Authorization': token}, json=data)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, bitlink):
    bitlink = urlparse(bitlink).path[1:]
    summary_url = f'https://api-ssl.bitly.com/v4/bitlinks/bit.ly/{bitlink}/clicks/summary'
    payload = {'unit': 'day', 'units': -1}
    response = requests.get(summary_url, headers={'Authorization': token}, params=payload)
    response.raise_for_status()
    return response.json()


def is_bitlink(url):
    parsed = urlparse(url)
    return parsed.netloc == 'bit.ly'


def main():
    parser = argparse.ArgumentParser(description='Long links to bitlinks or quantity bitlinks clicks')
    parser.add_argument('link', type=str, help='Enter the link you want to shorten')
    args = parser.parse_args()

    if not is_bitlink(args.link):
        try:
            bitlink = get_shorten_link(BITLY_BEARER_TOKEN, args.link)
        except requests.exceptions.HTTPError as error:
            print(f'Enter correct link\n {error}')
            sys.exit()
        print('Битлинк: ', bitlink)

    else:
        try:
            clicks_count = count_clicks(BITLY_BEARER_TOKEN, args.link)
        except requests.exceptions.HTTPError as error:
            print(f'Enter correct bitlink\n {error}')
            sys.exit()
        print('Всего кликов: ', clicks_count['total_clicks'])


if __name__ == "__main__":
    main()
