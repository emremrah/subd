import dotenv
from flask import make_response, request

from app import app, db
from data_models import Domain, DomainSubdomain, Subdomain
from main import SUBDOMAINS
from utils import find_subdomains_active, get_whois, read_subdomains

dotenv.load_dotenv(".env")

SUBDOMAINS = read_subdomains()


@app.route("/")
def get_domains():
    domains = db.session.query(Domain).all()

    return {
        "domains": [
            {
                "name": domain.name,
            }
            for domain in domains
        ]
    }


@app.route("/find-subdomains")
def find_subdomains():
    domain = request.args.get("domain")
    if domain is None:
        return make_response({"message": "No domain provided"}, 400)

    # check if domain is already in db
    if not db.session.query(Domain).filter_by(name=domain).first():
        domain_obj = Domain(**get_whois(domain).dict())
        db.session.add(domain_obj)
    domain_id = db.session.query(Domain).filter_by(name=domain).first().id

    max_trials = request.args.get("maxTrials", None, int)
    search_random = request.args.get("searchRandom", False, type=lambda v: v == "true")

    found_subdomains = find_subdomains_active(
        domain, SUBDOMAINS, max_trials, search_random
    )

    for subdomain in found_subdomains:
        db.session.add(Subdomain(subdomain))

    subdomain_ids = (
        db.session.query(Subdomain).filter(Subdomain.name.in_(found_subdomains)).all()
    )

    for subdomain_id in subdomain_ids:
        db.session.add(
            DomainSubdomain(domain_id=domain_id, subdomain_id=subdomain_id.id)
        )

    db.session.commit()

    return make_response({"subdomains": found_subdomains}, 200)


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
