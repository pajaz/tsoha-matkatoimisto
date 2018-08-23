from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

# Kerrotaan sovellukselle missä ympäristössä toimitaan (Heroku / Paikallinen)
import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    # Otetaan käyttöön matkakohteet.db tietokanta
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///matkakohteet.db"
    # SQL-kyselyiden tulostus
    app.config["SQLALCHEMY_ECHO"] = True

# Tietokanta olion luonti
db = SQLAlchemy(app)

# Kirjautuminen
from application.auth.models import Kayttaja
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.setup_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Kirjaudu sisään käyttääksesi tätä toiminnallisuutta"

@login_manager.user_loader
def load_user(user_id):
    return Kayttaja.query.get(user_id)

# Määritelläään käyttäjän roolin tarkistus
from functools import wraps

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated():
                return login_manager.unauthorized()
            
            unauthorized = False

            if role != "ANY":
                unauthorized = True
                
                for user_role in current_user.roles():
                    if user_role == role:
                        unauthorized = False
                        break
            
            if unauthorized:
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


# näkymien lukeminen
Bootstrap(app)

from application.start_page import views
from application.matkakohteet import views
from application.hotellit import views
from application.auth import views
from application.varaukset import views

# Tietokantamallit
from application.matkakohteet import models
from application.hotellit import models
from application.auth import models
from application.varaukset import models


# Jos tarpeellista, luodaan tietokanta
try:
    db.create_all()
except:
    pass