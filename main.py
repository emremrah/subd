"""Module for reading and processing domains from file."""
from typing import Generator


from app import db
from data_models import Domain, Subdomain
from utils import (find_subdomains_active, get_whois, read_domains,
                   read_subdomains)

SUBDOMAINS = read_subdomains()

DOMAINS = read_domains()


def process_domains() -> Generator[str, None, None]:
    """
    Find whois data for domains, find subdomains and save both to db.

    Returns
    ------
    Iterator of subdomains as strings.
    """
    for domain in DOMAINS:
        # check if domain is already in db. If not, add it
        if not db.session.query(Domain).filter_by(name=domain).first():
            domain_obj = get_whois(domain)
            db.session.add(domain_obj)

        # get inserted domain id
        domain_id = db.session.query(Domain).filter_by(name=domain).first().id

        # find subdomains
        subdomains = find_subdomains_active(
            domain, SUBDOMAINS, max_trials=3, search_random=False
        )

        # add subdomains to db
        for subdomain in subdomains:
            if not db.session.query(Subdomain).filter_by(name=subdomain, domain_id=domain_id).first():
                subdomain_obj = Subdomain(subdomain, domain_id)
                db.session.add(subdomain_obj)

        db.session.commit()

        yield subdomains


if __name__ == "__main__":
    for i, subdomains in enumerate(process_domains()):
        print(f"Found {subdomains} for {DOMAINS[i]}")
