"""Data models for sqlalchemy."""
from app import db


class Domain(db.Model):
    __tablename__ = "domains"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    org = db.Column(db.String(255))
    creation_date = db.Column(db.DateTime())
    expiration_date = db.Column(db.DateTime())
    text = db.Column(db.Text())
    country_iso = db.Column(db.String(2))

    def __init__(self, name, org, creation_date, expiration_date, text, country, **kwargs):
        self.name = name
        self.org = org
        self.creation_date = creation_date
        self.expiration_date = expiration_date
        self.text = text
        self.country_iso = country

    def __repr__(self):
        return f"<Domain: {self.name}>"


class Subdomain(db.Model):
    __tablename__ = "subdomains"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    domain_id = db.Column(db.Integer, db.ForeignKey("domains.id"))

    def __init__(self, name, domain_id):
        self.name = name
        self.domain_id = domain_id

    def __repr__(self):
        return f"<Subdomain: {self.name}>"
