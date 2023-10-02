import requests
import json
import os
import urllib
from urllib.parse import urlparse
from settings import bitly_api_token
import argparse


def shorten_link(user_url, bitly_api_token):
    url_for_short = 'https://api-ssl.bitly.com/v4/bitlinks'
    header = {'Authorization': 'Bearer {token}'.format(token=bitly_api_token)}
    payload = {"long_url": user_url}
    response = requests.post(url_for_short, json=payload, headers=header)
    response.raise_for_status()
    bitlink = response.json()['link']
    return bitlink


def count_clicks(short_bitlink, bitly_api_token):
    url_for_count = 'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    header = {'Authorization': 'Bearer {token}'.format(token=bitly_api_token)}
    response = requests.get(url_for_count.format(bitlink=short_bitlink), headers=header)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(short_bitlink, bitly_api_token):
    bitlink_url = 'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    header = {'Authorization': 'Bearer {token}'.format(token=bitly_api_token)}
    response = requests.get(bitlink_url.format(bitlink=short_bitlink), headers=header)
    return response.ok


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("user_url", help="Введённая ссылка")
    args = parser.parse_args()
    user_url = args.user_url
    parsed_link = urlparse(user_url)
    short_bitlink = '{}{}'.format(parsed_link.netloc, parsed_link.path)

    if is_bitlink(short_bitlink, bitly_api_token):
        print(count_clicks(short_bitlink, bitly_api_token))
    else:
        print(shorten_link(user_url, bitly_api_token))
