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
from application.start_page import views
from application.admin import views
from application.auth import views

# Tietokantamallit
from application import models
from application.auth import models

# Kirjautuminen
from application.auth.models import Kayttaja
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Kirjaudu sisään käyttääksesi tätä toiminnallisuutta"

@login_manager.user_loader
def load_user(user_id):
    return Kayttaja.query.get(user_id)

db.create_all()