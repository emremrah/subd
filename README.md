# Subdomain Finder

Find subdomains of a domain in active or passive manner.

## Usage

### Python Module

The domains to be scanned should be in a file named `./domains.txt`.

To scan the domains:

    $ python main.py --method active|passive
    Found <subdomains> for <domain>

### API

To run the API:

    python api.py

The API will run on port 5000. See swagger.yml for usage.

## Getting Started

Create a python environment and install the required packages:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Postgresql database is required.
