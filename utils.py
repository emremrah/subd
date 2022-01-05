from random import shuffle
from typing import List

import requests
import whois
from tqdm import tqdm

from data_models import Domain

SUBDOMAIN_FILE = "./assets/subdomains-top1million-5000.txt"


def read_subdomains(file=SUBDOMAIN_FILE):
    """Read list of subdomains from seclists."""
    subdomains = []
    with open(file, "r") as f:
        for line in f:
            subdomains.append(line.strip())
    return subdomains


def read_domains():
    """Read list of domains from domains.txt."""
    domains = []
    with open("domains.txt", "r") as f:
        for line in f:
            domains.append(line.strip())
    return domains


def find_subdomains_active(domain: str, subdomains: List[str], max_trials=None, search_random=False) -> List[str]:
    """
    Find subdomains for a domain.

    Args
    ----
    domain: domain to find subdomains for
    subdomains: list of subdomains to search
    max_trials: maximum number of trials to make
    search_random: whether to search subdomains in random order

    Returns
    -------
    List of subdomains for domain.

    """
    found_subdomains = []

    if search_random:
        subdomains = subdomains.copy()
        shuffle(subdomains)

    if max_trials is not None:
        subdomains = subdomains[:max_trials]

    for subdomain in tqdm(subdomains):
        url = "http://" + subdomain + "." + domain
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                found_subdomains.append(subdomain)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            pass

    return found_subdomains


def get_whois(domain: str):
    """
    Get whois data for domain. The keys should be the same as the ones in the
    data_models.Domain model.

    Returns
    -------
    Domain object.

    """
    who = whois.whois(domain)

    who["name"] = who["domain_name"][0].lower() if isinstance(
        who["domain_name"], list) else who["domain_name"].lower()

    who["country"] = who["country"].lower() if who["country"] else None

    # sometimes dates are lists for some reason
    who["expiration_date"] = who["expiration_date"][-1] if isinstance(
        who["expiration_date"], list) else who["expiration_date"]
    who["creation_date"] = who["creation_date"][-1] if isinstance(
        who["creation_date"], list) else who["creation_date"]

    who["text"] = who.text

    return Domain(**who)
