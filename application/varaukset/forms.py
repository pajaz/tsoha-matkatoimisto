from flask_wtf import FlaskForm
from wtforms import DateField, HiddenField, IntegerField, RadioField, SelectField, StringField, ValidationError, validators

from application import db
from application.hotellit.models import Hotelli
from application.varaukset.models import Varaus

class BookingForm(FlaskForm):
    # Luokka varausten lisäämiseen ja muokkaamiseen. 
    # Sallii toistaiseksi duplikaattien lisäämisen.
    passengers = IntegerField("Matkustajia", [validators.required(), validators.NumberRange(min=1, max=12, message="1-12 matkustajaa, suuremmille ryhmille ota yhteyttä matkatoimistoon")])
    small_rooms = IntegerField("1-2 hengen huoneita", [validators.optional()])
    large_rooms = IntegerField("3-4 hengen huoneita", [validators.optional()])

    class Meta:
        csrf = False

class ChooseHotelForm(FlaskForm):
    dest = HiddenField("", [validators.required()])
    date = HiddenField("", [validators.required()])
    hotel = RadioField("Hotellit", [validators.required()], coerce=int, default=None)

    class Meta:
        csrf = False

class BookingSearchForm(FlaskForm):
    destination = SelectField("Matkakohde: ", [validators.optional()], coerce=int)
    handled = RadioField("Maksettu: ", [validators.optional()], choices=[(2, "Kaikki"), (1, "Kyllä"), (0, "Ei")], default=2, coerce=int)
    status = RadioField("Status: ", [validators.optional()], choices=[("", "Kaikki"), ("past", "Mennyt"), ("active", "Käynnissä"), ("future", "Tuleva")], default="", coerce=str)

    class Meta:
        csrf = False