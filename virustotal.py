"""Module to keep Virustotal API."""
import doctest
from os import getenv
from typing import List

import dotenv
import requests

dotenv.load_dotenv()

API_KEY = getenv('VT_API_KEY')

URL = "https://www.virustotal.com/api/v3/domains/{}/subdomains?limit=10"

HEADERS = {"Accept": "application/json",
           'X-Apikey': API_KEY}


def find_subdomains_passive(domain: str) -> List[str]:
    """
    Find subdomains of a domain in passive manner. Uses Virustotal API.

    >>> get_subdomains_passive('example.com')
    ['www', 'ns2', 'ns1', 'ftp', 'konferencje', 'sales', 'conference', 'nowhereatall', 'api', 'gate']
    """
    response = requests.request("GET", URL.format(domain), headers=HEADERS)

    if response.status_code != 200:
        return []

    response = response.json()

    found_subdomains = []
    for domain_obj in response['data']:
        subdomain = domain_obj['id'].split('.')[0]
        found_subdomains.append(subdomain)

    return found_subdomains


if __name__ == "__main__":
    doctest.testmod()
