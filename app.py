from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from os import getenv
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:{getenv('POSTGRE_PW')}@localhost:5432/threat"

db = SQLAlchemy(app)
