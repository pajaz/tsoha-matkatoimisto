from wtforms import ValidationError

from application import db
from application.matkustajat.models import Matkustaja

# Seuraava luokka tarkistaa löytyykö tietokannasta samalla hlötunnuksella toisen niminen henkilö.
class SocialSecCheck(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        passenger = Matkustaja.query.filter_by(socialsec=form.socialsec.data).first()
        if passenger:
            print(form.fname.data)
            print(form.lname.data)
            if (form.fname.data != passenger.first_name) or (form.lname.data != passenger.last_name):
                raise ValidationError(message="Samalla henkilötunnuksella löytyy jo toisen niminen henkilö")
        return Truez