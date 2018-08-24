# application/matkustajat/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, validators, ValidationError

from application import db
from application.matkustajat.models import Matkustaja
from application.utils.myvalidators import SocialSecCheck



class PassengerForm(FlaskForm):
    fname = StringField("Etunimi", [validators.required(), validators.Length(max=24, message="max. 24 merkkiä")])
    lname = StringField("Sukunimi", [validators.required(), validators.Length(max=24, message="max. 24 merkkiä")])
    socialsec = StringField("Sotu", [validators.required(), validators.Length(min=11, max=11, message="Pituus 11 merkkiä"),
                                     SocialSecCheck()])

    

    class Meta:
        csrf = False

