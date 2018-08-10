from flask import redirect, render_template, request, url_for
from flask_login import login_required

from application import app, db
from application.hotellit.models import Hotelli
from application.hotellit.forms import HotelForm

@app.route("/hotellit/", methods=["GET"])
def hotellit_index():
    return render_template("hotellit/list.html", hotellit=Hotelli.query.all())


@app.route("/hotellit/uusi")
#@login_required
def hotellit_form():
    return render_template("hotellit/hotelli.html", form=HotelForm(), hotel_add=True)


@app.route("/hotellit/", methods=["POST"])
#@login_required
def hotellit_create():
    
    form = HotelForm(request.form)

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

    if form.validate():
        if not hotel_introduction:
            hotel = Hotelli(hotel_name.title(), hotel_destination, hotel_address.title(), hotel_phone_number, 
                            hotel_star_rating, hotel_small_rooms, hotel_large_rooms, 
                            hotel_price_small, hotel_price_large, hotel_email)
        else:
            hotel = Hotelli(hotel_name.title(), hotel_destination, hotel_address.title(), hotel_phone_number, 
                            hotel_star_rating, hotel_small_rooms, hotel_large_rooms, 
                            hotel_price_small, hotel_price_large, hotel_email, hotel_introduction)

        db.session().add(hotel)
        db.session().commit()

        return redirect(url_for("hotellit_index"))
    
    return render_template("hotellit/hotelli.html", form=form, hotel_add=True)


@app.route('/hotellit/edit/<hotelli_id>', methods=['GET', 'POST'])
#@login_required
def hotellit_edit_form(hotelli_id):

    Hotel = Hotelli.query.get_or_404(hotelli_id)
    form = HotelForm(obj=Hotel)

    if request.method == 'POST' and form.validate(): 
        hotel_name = form.name.data
        hotel_address = form.address.data
        hotel_phone_number = form.phone_number.data
        hotel_small_rooms = form.small_rooms.data
        hotel_large_rooms = form.large_rooms.data
        hotel_price_small = form.price_small.data
        hotel_price_large = form.price_large.data
        hotel_star_rating = form.star_rating.data
        hotel_email = form.email.data
        hotel_introduction = form.introduction.data

        if hotel_introduction:
            Hotel.introduction = hotel_introduction

        db.session().commit()

        return redirect(url_for("hotellit_index"))

    return render_template("hotellit/hotelli.html", form=form, hotelli=Hotel, hotelli_id=Hotel.id, hotel_add=False)


@app.route("/hotellit/delete/<hotelli_id>", methods=["GET", "POST"])
#@login_required
def hotellit_delete(hotelli_id):

    Hotel = Hotelli.query.get_or_404(hotelli_id)

    db.session.delete(Hotel)
    db.session.commit()

    return redirect(url_for("hotellit_index"))
