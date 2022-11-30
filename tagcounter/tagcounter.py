import argparse
import yaml
import pkg_resources
import logging
import urllib.request
import json
from html.parser import HTMLParser
from datetime import datetime
from . import db

logging.basicConfig(filename='requests.log', format='%(asctime)s %(message)s', level=logging.DEBUG)

file = pkg_resources.resource_stream(__name__, 'synonyms.yaml')
options = yaml.safe_load(file)


class Parser(HTMLParser):
    result_dict = {}

    def handle_starttag(self, tag, attrs):
        if tag in self.result_dict:
            self.result_dict[tag] += 1
        else:
            self.result_dict[tag] = 1


def get_site_name(address: str):
    return address.split('.')[0]


def get_address(link: str):
    return 'http://' + link


def parse_site(link: str):
    with urllib.request.urlopen(get_address(link)) as res:
        result_string = str(res.read())
        parser = Parser()
        parser.feed(result_string)
        parsed = parser.result_dict
        json_str = json.dumps(parsed)

    return json_str


def save(link: str):
    parsed = parse_site(link)
    db.add_info(get_address(link), get_site_name(link), str(datetime.now()), parsed)


def view(address: str):
    db.view_info(address)


def main():
    parser = argparse.ArgumentParser(description="Count tags on the site")
    parser.add_argument('--get', help="Command to run. Either 'get' or 'view'")
    parser.add_argument('--view', help="Command to run. Either 'get' or 'view'")

    args = parser.parse_args()

    arg = args.get or args.view

    address = options.get('synonyms').get(arg) or arg

    if args.get:
        logging.debug(address)
        save(address)

    if args.view:
        view(address)


if __name__ == '__main__':
    main()
