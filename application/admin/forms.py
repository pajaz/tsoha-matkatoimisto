from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, ValidationError, validators

from ..models import Matkakohde



class DestinationForm(FlaskForm):
    name = StringField("Nimi", [validators.required(), validators.Length(max=30)])
    country = StringField("Maa", [validators.required(), validators.Length(max=30)])
    description = TextAreaField("Esittely (Vapaaehtoinen)", [validators.Length(max=500)])

    def validate_destination_name(self, field):
        if Matkakohde.query.filter_by(name=field.data).first():
            raise ValidationError("Kohde on jo listattu.")

    class Meta:
        csrf = False