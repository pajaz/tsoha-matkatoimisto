# application/auth/forms.py
from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, validators, ValidationError

from application.auth.models import Kayttaja

# Lomake siäänkirjautumiseen
class LoginForm(FlaskForm):
    username = StringField("Käyttäjätunnus", [validators.required()])
    password = PasswordField("Salasana", [validators.required()])

    class Meta:
        csrf = False

# Lomake jolla luodaan uusi käyttäjä
class NewUserForm(FlaskForm):
    firstname = StringField("Etunimi:", [validators.required(), validators.Length(max=24, message="max. 24 merkkiä")])
    lastname = StringField("Sukunimi:", [validators.required(), validators.Length(max=24, message="max. 24 merkkiä")])
    phone_number = StringField("Puhelinnumero:", [validators.required(), validators.Length(min=8, max=20, message="merkkien määrä 8-20")])
    email = StringField("Sähköpostiosoite (Vapaaehtoinen):", [validators.optional(), validators.Length(min=6, max=35, message="merkkien määrä 8-20")])
    username = StringField("Käyttäjätunnus:", [validators.required(), validators.Length(min=4, max=24, message="merkkien määrä 4-20")])
    password = PasswordField("Salasana:", [validators.required(), validators.Length(min=6, max=144, message="min. 6 merkkiä"),
                                           validators.EqualTo("confirm", message="Salasanojen tulee olla samat")])
    confirm = PasswordField("Salasana uudestaan:", [validators.required()])
    admin = SelectField("Rooli: ", choices=[(1, "Admin"), (2, "Käyttäjä")], default=2, coerce=int)

    # Tarkistaa, ettei käyttäjänimi ole jo käytössä
    def validate_username(self, field):
        if Kayttaja.query.filter_by(username=field.data).first():
            raise ValidationError("Käyttäjätunnus on jo käytössä")

    class Meta:
        csrf = False