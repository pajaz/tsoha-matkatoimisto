# application/varaukset/views.py
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
import datetime

from application import app, db
from application.varaukset.models import Varaus
from application.matkakohteet.models import Matkakohde
from application.hotellit.models import Hotelli
from application.varaukset.forms import BookingForm, ChooseHotelForm

# Hakee varausten listaussivun esille
@app.route("/varaukset/", methods=["GET"])
@login_required
def varaukset_index():
    bookings = Varaus.query.order_by(Varaus.dest_id).all()
    return render_template("/varaukset/list.html", varaukset=Varaus.query.all())

#  Hakee näytille uusien hotellien lisäämiseen käytettävän lomakkeen ja lähettää uuden hotellin tiedot eteenpäin.
@app.route("/varaukset/uusi", methods=["GET","POST"])
@login_required
def varaus_create():
    dest = request.args.get("dest")
    date = request.args.get("date")
    hotel_id = request.args.get("hotel_id")
    destination = Matkakohde.query.get_or_404(dest)
    hotel = Hotelli.query.get_or_404(hotel_id)
    form = BookingForm(request.form)

    if request.method == "POST":
        passengers = form.passengers.data
        small_rooms = form.small_rooms.data
        large_rooms = form.large_rooms.data

        if form.validate():
            if not small_rooms:
                small_rooms = 0
            if not large_rooms:
                large_rooms = 0
            price = destination.price * passengers + small_rooms * hotel.price_small + large_rooms * hotel.price_large
            
            date_save = datetime.datetime.strptime(date, '%d.%m.%Y')
            booking = Varaus(date_save, price, current_user.id, dest, passengers, hotel_id,
                                 small_rooms, large_rooms)
          
            db.session().add(booking)
            db.session().commit()

            return redirect(url_for("matkakohteet_index")) 
    print(form.errors)    
    return render_template("/varaukset/varaus.html", form=form, book_add=True, dest=dest, date=date,
                           matkakohde=destination, hotel=hotel, hotel_id=hotel_id)

@app.route("/varaukset/uusi/valitsehotelli", methods=["GET"])
@login_required
def varaus_hotelli():  
    dest = request.args.get("dest")
    date = request.args.get("date")
    form = ChooseHotelForm()
    hotel_count = db.session.query(Hotelli).filter(Hotelli.destination_id==dest).count()

    form.hotel.choices = [(hotel.id, hotel.name) for hotel in Hotelli.query.filter_by(destination_id=dest)]
    hotels = Hotelli.query.filter_by(destination_id=dest)
    zipped = zip(form.hotel.choices, hotels)
    Hotelli.hotels_with_bookings()

    form.dest.data = dest
    form.date.data = date

    return render_template("/varaukset/destinationhotels.html", dest=dest, date=date, form=form, hotels=zipped)




@app.route("/varaukset/edit/<varaus_id>", methods=["GET","POST"])
@login_required
def varaukset_edit_form(varaus_id):
    
    varaus = Varaus.query.get_or_404(varaus_id)
    form = BookingForm(obj=varaus)
    form.hotel.choices = [(hotel.id, hotel.name) for hotel in Hotelli.query.filter_by(dest_id=desti_id)]

    if request.method == "POST" and form.validate_on_submit():
        varaus.start = form.start.data
        varaus.destination = form.destination.data
        varaus.passengers = form.passengers.data
        varaus.hotel = form.hotel.data
        varaus.small_rooms = form.small_rooms.data
        varaus.large_rooms = form.large_rooms.data

        db.session().commit()
        return redirect(url_for("matkakohteet_index"))

    return render_template("/varaukset/varaus.html", form=form, varaus=varaus, varaus_id=varaus.id, book_add=False)

@app.route("/varaukset/delete/<varaus_id>", methods=["GET", "POST"])
@login_required
def varaukset_delete(varaus_id):

    varaus = Varaus.query.get_or_404(varaus_id)

    db.session.delete(varaus)
    db.session.commit()

    return redirect(url_for("matkakohteet_index"))