# application/hotellit/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, ValidationError, validators, IntegerField

from application import db
from application.hotellit.models import Hotelli
from application.matkakohteet.models import Matkakohde


class HotelForm(FlaskForm):
    # Luokka hotellien lisäämiseen ja muokkaamiseen. 
    # Sallii toistaiseksi duplikaattien lisäämisen.

    name = StringField("Nimi *", [validators.required(), validators.Length(max=30, message=('max. 30 merkkiä'))])
    destination = StringField("Matkakohde *", [validators.required(), validators.Length(max=30, 
                                               message=('max. 30 merkkiä'))])
    address = StringField("Osoite *", [validators.required(),validators.Length(min=10, max=50, message=('10-50 merkkiä'))])
    phone_number = StringField("Puhelinnumero *", [validators.required(),validators.Length(min=8, max=20, message=('10-20 merkkiä'))])
    email = StringField("Sähköposti", [validators.optional(), validators.email(message="Ei kunnollinen sähköpostiosoite")])
    small_rooms = IntegerField("Pieniä huoneita (max. 2 hlöä)", [validators.optional(), validators.NumberRange(min=0, max=10000, message="0-10000")])
    large_rooms = IntegerField("Suuria huoneita (max. 4 hlöä)", [validators.optional(), validators.NumberRange(min=0, max=10000, message="0-10000")])
    price_small = IntegerField("€/Viikko (Pieni)", [validators.optional(), validators.NumberRange(min=0, max=40000, message="0-40000")])
    price_large = IntegerField("€/Viikko (Suuri)", [validators.optional(), validators.NumberRange(min=0, max=40000, message="0-40000")])
    star_rating = IntegerField("Tähtiluokitus (1-5) *", [validators.required(), validators.NumberRange(min=1, max=5, message="1-5 tähteä")])
    introduction = TextAreaField("Esittely (0-500 merkkiä)", [validators.optional(), validators.Length(max=500, message="max. 500 merkkiä")])

    # Metodi tarkastaa hotellin lisäyksen yhteydessä, että Hotelliin liitettävä
    # Matkakohde on olemassa.
    def validate_destination(form, field):
        dest = db.session.query(Matkakohde).filter(Matkakohde.name==form.destination.data).first()
        if not dest:
            raise ValidationError("Kohdetta ei tietokannassa")


    class Meta:
        csrf = False