# application/varaukset/views.py
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from wtforms import StringField
import datetime

from application import app, db, login_required
from application.varaukset.models import Varaus, matkustaja_varaus
from application.matkakohteet.models import Matkakohde
from application.matkustajat.models import Matkustaja
from application.hotellit.models import Hotelli
from application.varaukset.forms import BookingForm, ChooseHotelForm
from application.matkustajat.forms import PassengerForm

# Hakee varausten listaussivun esille
@app.route("/varaukset/", methods=["GET"])
@login_required(role="Admin")
def varaukset_index():
    bookings = Varaus.query.order_by(Varaus.dest_id).all()
    return render_template("/varaukset/list.html", varaukset=Varaus.query.all())

#  Hakee näytille uusien hotellien lisäämiseen käytettävän lomakkeen ja lähettää uuden hotellin tiedot eteenpäin.
@app.route("/varaukset/uusi", methods=["GET","POST"])
@login_required(role="User")
def varaus_create():
    dest = request.args.get("dest")
    date = request.args.get("date")
    hotel_id = request.args.get("hotel_id")
    destination = Matkakohde.query.get_or_404(dest)
    
    if hotel_id:   
        hotel = Hotelli.query.get_or_404(hotel_id)
    else:
        hotel = None
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
            if hotel_id:
                price = destination.price * passengers + small_rooms * hotel.price_small + large_rooms * hotel.price_large
            else:
                price = destination.price * passengers
            
            date_save = datetime.datetime.strptime(date, '%d.%m.%Y')
            if hotel_id:
                booking = Varaus(date_save, price, current_user.id, dest, passengers, hotel_id,
                                 small_rooms, large_rooms)
            else:
                booking = Varaus(date_save, price, current_user.id, dest, passengers,
                                 small_rooms, large_rooms)
          
            db.session().add(booking)
            db.session().commit()

            return redirect(url_for("varaus_info", varaus_id=booking.id)) 
    print(form.errors)    
    return render_template("/varaukset/varaus.html", form=form, book_add=True, dest=dest, date=date,
                           matkakohde=destination, hotel_id=hotel_id, hotel=hotel)

@app.route("/varaukset/uusi/valitsehotelli", methods=["GET"])
@login_required(role="User")
def varaus_hotelli():  
    dest = request.args.get("dest")
    date = request.args.get("date")
    form = ChooseHotelForm()

    
    hotels = Hotelli.query.filter_by(destination_id=dest)
    form.hotel.choices = [(hotel.id, hotel.name) for hotel in hotels]
    zipped = zip(form.hotel.choices, hotels)
    form.dest.data = dest
    form.date.data = date
        

    return render_template("/varaukset/destinationhotels.html", dest=dest, date=date, form=form, hotels=zipped)




@app.route("/varaukset/edit/<varaus_id>", methods=["GET","POST"])
@login_required(role="Admin")
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
@login_required(role="Admin")
def varaukset_delete(varaus_id):

    varaus = Varaus.query.get_or_404(varaus_id)

    db.session.delete(varaus)
    db.session.commit()

    return redirect(url_for("matkakohteet_index"))

# Varauksen tietojen katselu, sekä tehdyn varauksen tietojen vahvistus käyttäjälle
@app.route("/varaukset/<varaus_id>", methods=["GET", "POST"])
@login_required(role=("User"))
def varaus_info(varaus_id):
    
    varaus = Varaus.query.get_or_404(varaus_id)
    dest = Matkakohde.query.get_or_404(varaus.booking_dest()[0])
    if varaus.hotel_id:
        hotel = Hotelli.query.get_or_404(varaus.booking_hotel()[0])
    else:
        hotel = None
    passengers = varaus.booking_passengers()
    form = PassengerForm(request.form)

    if request.method == "POST" and form.validate_on_submit() and len(passengers) < varaus.passengers:
        fname = form.fname.data
        lname = form.lname.data
        socsec = form.socialsec.data

        pas = Matkustaja.query.filter_by(socialsec=socsec).first()
        if pas is None:
            passenger = Matkustaja(fname, lname, socsec)
            db.session.add(passenger)
            db.session.flush()
            pas_book = matkustaja_varaus.insert().values(matkustaja_id=passenger.id, varaus_id=varaus.id)

        else:
            pas_book = matkustaja_varaus.insert().values(matkustaja_id=pas.id, varaus_id=varaus.id)

       
        db.session.execute(pas_book)

        db.session.commit()

        return redirect(url_for("varaus_info", varaus_id=varaus.id))


    if request.method == "POST" and len(passengers) == varaus.passengers:
        varaus.confirmed = True
        db.session().commit()

        return redirect(url_for("varaus_info", varaus_id = varaus.id))

    
    return render_template("varaukset/varausinfo.html", form=form, varaus=varaus, matkakohde=dest, hotel=hotel, date = varaus.start_date,
                            matkustajat = passengers, lasku=varaus.bill_sent, maksettu=varaus.handled)




    