# application/hotellit/views.py
from flask import redirect, render_template, request, url_for
from flask_login import login_required

from application import app, db
from application.hotellit.models import Hotelli
from application.hotellit.forms import HotelForm
from application.matkakohteet.models import Matkakohde

# Hotellien listaussivu
@app.route("/hotellit/", methods=["GET"])
@login_required
def hotellit_index():
    hotellit=Hotelli.query.all()
    return render_template("hotellit/list.html", hotellit=hotellit)

#  Hakee näytille uusien hotellien lisäämiseen käytettävän lomakkeen ja lähettää uuden hotellin tiedot eteenpäin.
@app.route("/hotellit/uusi", methods=["GET","POST"])
@login_required
def hotellit_create():
    
    form = HotelForm(request.form)
    form.destination.choices = [(dest.id, dest.name) for dest in Matkakohde.query.all()]

    if request.method == "POST":
        hotel_name = form.name.data
        hotel_destination = form.destination.data
        hotel_address = form.address.data
        hotel_phone_number = form.phone_number.data
        hotel_small_rooms = form.small_rooms.data
        hotel_large_rooms = form.large_rooms.data
        hotel_price_small = form.price_small.data
        hotel_price_large = form.price_large.data
        hotel_star_rating = form.star_rating.data
        hotel_email = form.email.data
        hotel_introduction = form.introduction.data

        if form.validate_on_submit():
            if not hotel_introduction: # Jos ei hotellille lisätty esittelyä, käytetään modelsissa määriteltyä vakio viestiä 
                hotel = Hotelli(hotel_name.title(), hotel_address.title(), hotel_phone_number, 
                                hotel_star_rating, hotel_small_rooms, hotel_large_rooms, 
                                hotel_price_small, hotel_price_large, hotel_email, hotel_destination)
            else:
                hotel = Hotelli(hotel_name.title(), hotel_address.title(), hotel_phone_number, 
                                hotel_star_rating, hotel_small_rooms, hotel_large_rooms, 
                                hotel_price_small, hotel_price_large, hotel_email, hotel_destination, hotel_introduction)

            db.session().add(hotel)
            db.session().commit()

            return redirect(url_for("hotellit_index"))  

    return render_template("hotellit/hotelli.html", form=form, hotel_add=True)

# Editointi lomakkeen haku, sekä lähetys toiminnaliisuus
@app.route('/hotellit/edit/<hotelli_id>', methods=['GET', 'POST'])
@login_required
def hotellit_edit_form(hotelli_id):

    hotel = Hotelli.query.get_or_404(hotelli_id)
    form = HotelForm(obj=hotel) # Täytetään lomake tietokannasta löytyvillä hotellin tiedoilla
    form.destination.choices = [(dest.id, dest.name) for dest in Matkakohde.query.all()]

    if request.method == 'POST' and form.validate(): 
        hotel.name = form.name.data
        hotel.address = form.address.data
        hotel.destination = form.destination.data
        hotel.phone_number = form.phone_number.data
        hotel.small_rooms = form.small_rooms.data
        hotel.large_rooms = form.large_rooms.data
        hotel.price_small = form.price_small.data
        hotel.price_large = form.price_large.data
        hotel.star_rating = form.star_rating.data
        hotel.email = form.email.data

        if hotel.introduction: # Jos esittelyn yrittää pyyhkiä kokonaan pois, sitä ei tallenneta
            hotel.introduction = form.introduction.data

        db.session().commit()

        return redirect(url_for("hotellit_index"))

    return render_template("hotellit/hotelli.html", form=form, hotelli=hotel, hotelli_id=hotel.id, hotel_add=False)
# Hotellien poisto. Ei muuta.
@app.route("/hotellit/delete/<hotelli_id>", methods=["GET", "POST"])
@login_required
def hotellit_delete(hotelli_id):

    Hotel = Hotelli.query.get_or_404(hotelli_id)

    db.session.delete(Hotel)
    db.session.commit()

    return redirect(url_for("hotellit_index"))
