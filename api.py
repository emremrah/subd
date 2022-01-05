import dotenv
from flask import make_response, request

from app import app, db
from data_models import Domain
from main import process_domains
from utils import read_subdomains

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
    method = request.args.get("method")
    domain = request.args.get("domain")

    if method is None or method not in ['active', 'passive']:
        make_response({"message": "Invalid method"}, 400)

    if domain is None:
        make_response({"message": "Invalid domain"}, 400)

    subdomains = process_domains(max_trials=request.args.get("maxTrials"),
                                 search_random=request.args.get(
                                     "searchRandom", False),
                                 method=method,
                                 domains=[domain])

    subdomains = next(subdomains)

    return make_response({"subdomains": subdomains}, 200)


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
