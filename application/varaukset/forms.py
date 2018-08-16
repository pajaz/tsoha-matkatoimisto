from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, SelectField, StringField, ValidationError, validators

from application import db
from application.hotellit.models import Hotelli
from application.varaukset.models import Varaus

class BookingForm(FlaskForm):
    # Luokka varausten lisäämiseen ja muokkaamiseen. 
    # Sallii toistaiseksi duplikaattien lisäämisen.
    start = DateField("Lähtöpäivä *", [validators.required()], format="%d.%m.%Y")
    #end = SelectField("Paluupäivä", [validators.required()])
    destination = StringField("Matkakohde", [validators.required()])
    passengers = IntegerField("Matkustajia", [validators.required()])
    hotel = SelectField("Hotelli", [validators.optional()], coerce=int)
    small_rooms = IntegerField("1-2 hengen huoneita", [validators.optional()])
    large_rooms = IntegerField("3-4 hengen huoneita", [validators.optional()])

    class Metal:
        csfr = False

