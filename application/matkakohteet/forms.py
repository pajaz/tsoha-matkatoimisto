from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, ValidationError, validators

from application.matkakohteet.models import Matkakohde


#Lomake uusien matkakohteiden lisäämiseen ja muokkaamiseen
class DestinationForm(FlaskForm):
    name = StringField("Nimi", [validators.required(), validators.Length(max=30, message=('max. 30 merkkiä'))])
    country = StringField("Maa", [validators.required(), validators.Length(max=30, message=('max. 30 merkkiä'))])
    intro = TextAreaField("Esittely (Vapaaehtoinen)", [validators.Length(max=500)])

    def validate_name(self, field):
        if Matkakohde.query.filter_by(name=field.data).first():
            raise ValidationError("Kohde on jo listattu.")

    class Meta:
        csrf = False