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
        return True

# Tarkistetaan löytyvätkö parametrina annetun kentän tiedot jo tietokannasta
# Käytössä Matkakohteille, Käyttäjänimille
class Unique(object):

    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = u'Kentän tiedot löytyvät jo tietokannasta'
        self.message = message

    def __call__(self, form, field):         

        check = self.model.query.filter(self.field == field.data).first()
        if 'id' in form:
            id = form.id.data
        else:
            id = None
        if check and (id is None or id != check.id):
            raise ValidationError(self.message)