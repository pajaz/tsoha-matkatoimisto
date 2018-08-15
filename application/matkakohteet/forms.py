from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, ValidationError, validators

from application.matkakohteet.models import Matkakohde


#Lomake uusien matkakohteiden lisäämiseen ja muokkaamiseen
class DestinationForm(FlaskForm):
    name = StringField("Nimi *", [validators.required(), validators.Length(max=30, message=('max. 30 merkkiä'))])
    country = StringField("Maa *", [validators.required(), validators.Length(max=30, message=('max. 30 merkkiä'))])
    depart = StringField("Lähtöpäivä", [validators.optional()])
    day_out = StringField("Paluupäivä", [validators.optional()])
    price = IntegerField("Hinta", [validators.NumberRange(min=0, max=100000, message="0-100000")])
    intro = TextAreaField("Esittely (Vapaaehtoinen)", [validators.Length(max=500)])

    def validate_depart(self, field):
        weekdays = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai", "Sunnuntai"]
        if field.data.title() not in weekdays:
            raise ValidationError("Ei kunnollinen päivämäärä")

    def validate_day_out(self, field):
        weekdays = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai", "Sunnuntai"]
        if field.data.title() not in weekdays:
            raise ValidationError("Ei kunnollinen päivämäärä")

    class Meta:
        csrf = False