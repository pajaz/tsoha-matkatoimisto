# application/matkakohteet/views.py
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required

from application import app, db
from application.matkakohteet.models import Matkakohde
from application.matkakohteet.forms import DestinationForm
from application.utils.tools import next_weekdays

import datetime

# Hakee kohteiden listaussivun esille
@app.route("/matkakohteet/", methods=["GET"])
def matkakohteet_index():
    return render_template("matkakohteet/list.html", matkakohteet=Matkakohde.query.all())

# Hakee uuden kohteen lisäyssivun näkyville. Parametri dest_add kertoo html-templatelle, että kyseessä kohteen lisäys
@app.route("/matkakohteet/uusi")
@login_required
def matkakohteet_form():
    return render_template("matkakohteet/matkakohde.html", form=DestinationForm(), dest_add=True)

# Lisäyslomakkeen postaus.
@app.route("/matkakohteet/", methods=["POST"])
@login_required
def matkakohteet_create():
    
    form = DestinationForm(request.form)

    dest_name = form.name.data.title()
    dest_country = form.country.data.title()
    dest_depart = form.depart.data.title()
    dest_day_out = form.day_out.data.title()
    dest_price = form.price.data
    dest_intro = form.intro.data

    if form.validate_on_submit():
        if not dest_intro: # Jos ei esittelyä määritelty käytetään valmiiksi määriteltyä.
            dest = Matkakohde(dest_name, dest_country, dest_depart, dest_day_out, dest_price)
        else:
            dest = Matkakohde(dest_name, dest_country, dest_depart, dest_day_out, dest_price, dest_intro)

        db.session().add(dest)
        db.session().commit()

        return redirect(url_for("matkakohteet_index"))
    
    return render_template("matkakohteet/matkakohde.html", form=form, dest_add=True)

@app.route('/matkakohteet/<matkakohde_id>', methods=['GET'])
def matkakohde_intro(matkakohde_id):
    
    destination = Matkakohde.query.get_or_404(matkakohde_id)
    day = datetime.datetime.now()
    travel_days = next_weekdays(day, destination.depart, 4)


    return render_template("matkakohteet/intropage.html", traveldays = travel_days, matkakohde = destination)

# Editointilomakkeen haku ja lomakkeen lähetys. dest_add lopussa kertoo että kyseessä muokkaus
@app.route('/matkakohteet/edit/<matkakohde_id>', methods=['GET', 'POST'])
@login_required
def matkakohteet_edit_form(matkakohde_id):

    destination = Matkakohde.query.get_or_404(matkakohde_id)
    form = DestinationForm(obj=destination) # Lomakkeen esitäyttö tietokannasta löytyvillä tiedoilla

    if request.method == 'POST' and form.validate():

        destination.name = form.name.data.title()
        destination.country = form.country.data.title()
        destination.depart = form.depart.data.title()
        destination.day_out = form.day_out.data.title()
        destination.price = form.price.data

        if destination.intro: # Jos kohteen esittelyn yrittää pyyhkiä kokonaan pois, sitä ei tallenneta
            destination.intro = form.intro.data

        db.session().commit()

        return redirect(url_for("matkakohteet_index"))

    return render_template("matkakohteet/matkakohde.html", form=form, matkakohde=destination, 
                            matkakohde_id=destination.id, dest_add=False)

# Kohteiden poisto
@app.route("/matkakohteet/delete/<matkakohde_id>", methods=["GET", "POST"])
@login_required
def matkakohteet_delete(matkakohde_id):

    destination = Matkakohde.query.get_or_404(matkakohde_id)

    db.session.delete(destination)
    db.session.commit()

    return redirect(url_for("matkakohteet_index"))
