"""Module for reading and processing domains from file."""
import argparse
from typing import Generator

from app import db
from data_models import Domain, Subdomain
from utils import (find_subdomains_active, get_whois, read_domains,
                   read_subdomains)
from virustotal import find_subdomains_passive

SUBDOMAINS = read_subdomains()

DOMAINS = read_domains()


def process_domains(max_trials, search_random, method) -> Generator[str, None, None]:
    """
    Find whois data for domains, find subdomains and save both to db.

    Args
    ----
    max_trials: maximum number of trials to make for each domain.
    search_random: whether to search subdomains in random order.
    method: method to use for finding subdomains. Enum of 'active' or 'passive'.
    Returns
    ------
    Iterator of subdomains as strings.
    """
    if method not in ['active', 'passive']:
        raise ValueError(f"Invalid method: {method}")

    for domain in DOMAINS:
        # check if domain is already in db. If not, add it
        if not db.session.query(Domain).filter_by(name=domain).first():
            domain_obj = get_whois(domain)
            db.session.add(domain_obj)

        # get inserted domain id
        domain_id = db.session.query(Domain).filter_by(name=domain).first().id

        # find subdomains
        if method == 'active':
            subdomains = find_subdomains_active(
                domain, SUBDOMAINS, max_trials=max_trials, search_random=search_random)
        else:
            subdomains = find_subdomains_passive(domain)

        # add subdomains to db
        for subdomain in subdomains:
            if not db.session.query(Subdomain).filter_by(name=subdomain, domain_id=domain_id).first():
                subdomain_obj = Subdomain(subdomain, domain_id)
                db.session.add(subdomain_obj)

        db.session.commit()

        yield subdomains


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Find subdomains for domains.')
    parser.add_argument('--search_random', action='store_true', default=False,
                        help='whether to search subdomains in random order')
    parser.add_argument('--max_trials', type=int, default=None,
                        help='maximum number of trials to make')
    parser.add_argument('--method', type=str, required=True,
                        help='method to use for finding subdomains', choices=['active', 'passive'])
    args = parser.parse_args()

    for i, subdomains in enumerate(process_domains(args.max_trials, args.search_random, args.method)):
        print(f"Found {subdomains} for {DOMAINS[i]}")
