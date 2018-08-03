from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

# Otetaan käyttöön matkakohteet.db tietokanta
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///matkakohteet.db"
# SQL-kyselyiden tulostus
app.config["SQLALCHEMY_ECHO"] = True

# Tietokanta olion luonti
db = SQLAlchemy(app)

# näkymien lukeminen
from application import views

from application.matkakohteet import models

# Luodaan tietokantataulut
db.create_all()