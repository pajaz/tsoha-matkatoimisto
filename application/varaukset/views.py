# application/varaukset/views.py
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from wtforms import StringField
import datetime
from math import ceil

from application import app, db, login_required
from application.varaukset.models import Varaus, matkustaja_varaus
from application.matkakohteet.models import Matkakohde
from application.matkustajat.models import Matkustaja
from application.hotellit.models import Hotelli
from application.varaukset.forms import BookingForm, ChooseHotelForm, BookingSearchForm
from application.matkustajat.forms import PassengerForm
from application.utils.tools import next_weekdays

# Hakee varausten listaussivun esille
@app.route("/varaukset/", methods=["GET", "POST"])
@login_required(role="User")
def varaukset_index():

    orderby = request.args.get("order", "id", type=str)
    show = 6
    page = request.args.get("page", 1, type=int)

    form = BookingSearchForm(request.form)
    
    dests_with_bookings = Matkakohde.destinations_with_bookings()
    
    choices = [(dest["id"], dest["name"]) for dest in dests_with_bookings]
    empty = [(0, "Kaikki")]
   
    form.destination.choices = empty + choices

    if request.method == "POST" and form.validate():
        bookings = Varaus.search_bookings(form.destination.data, form.handled.data, form.status.data)
        pages=1

        return render_template("varaukset/list.html", varaukset=bookings, form=form, page=page,
                                pages=pages, order=orderby)

    if current_user.admin == 1:
        bookings = Varaus.search_bookings(n = (page-1)*show)
        pages = ceil(Varaus.query.count()/show)
    else:
        bookings = Varaus.query.filter_by(user_id = current_user.id).paginate(page, show, False).items
        pages = 1
    

    return render_template("/varaukset/list.html", varaukset=bookings,form=form, page=page,
                            pages=pages, order=orderby)

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
            return_date = next_weekdays(date_save, destination.day_out, 0)
            return_save = datetime.datetime.strptime(return_date, "%d.%m.%Y")

            if hotel_id:
                booking = Varaus(date_save, return_save, price, current_user.id, dest, passengers, hotel_id,
                                 small_rooms, large_rooms)
            else:
                booking = Varaus(date_save, return_save, price, current_user.id, dest, passengers, None,
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

    form.hotel.choices = [(hotel.id, hotel.name) for hotel in hotels] + [(None, "Ei hotellia")]
    zipped = zip(form.hotel.choices, hotels)
    form.dest.data = dest
    form.date.data = date   

    return render_template("/varaukset/destinationhotels.html", dest=dest, date=date, form=form, hotels=zipped)


@app.route("/varaukset/delete/<varaus_id>", methods=["GET", "POST"])
@login_required(role="Admin")
def varaukset_delete(varaus_id):

    varaus = Varaus.query.get_or_404(varaus_id)

    db.session.delete(varaus)
    db.session.commit()

    return redirect(url_for("matkakohteet_index"))

# Käyttäjä voi tarkastella varauksen tietoja, vahvistaa varauksen ja lisätä/poistaa matkustajia varauksesta tämän sivun kautta
# Admin voi tämän lisäksi merkitä varauksen laskun lähetetyksi ja maksetuksi, sekä poistaa varauksen
@app.route("/varaukset/<varaus_id>", methods=["GET", "POST"])
@login_required(role=("User"))
def varaus_info(varaus_id):
    
    varaus = Varaus.query.get_or_404(varaus_id)
    
    
    if current_user.id == varaus.user_id or current_user.admin == 1:
        dest = Matkakohde.query.get_or_404(varaus.booking_dest()[0])
        if varaus.hotel_id:
            hotel = Hotelli.query.get_or_404(varaus.booking_hotel()[0])
        else:
            hotel = None
        passengers = varaus.booking_passengers()
        form = PassengerForm(request.form)
                                                                    # Jos kaikki matkustajia ei vielä ole syötetty
        if request.method == "POST" and form.validate_on_submit() and len(passengers) < varaus.passengers: 
            fname = form.fname.data
            lname = form.lname.data
            socsec = form.socialsec.data

            pas = Matkustaja.query.filter_by(socialsec=socsec).first()
            
            # Jos matkustajaa ei ole vielä luotu tietokantaan, luodaan se tässä
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

            if not varaus.confirmed:
                varaus.confirmed = True
            elif varaus.confirmed and not varaus.bill_sent:
                varaus.bill_sent = True
            elif varaus.bill_sent and varaus.handled == 0:
                varaus.handled = 1
            db.session().commit()

            return redirect(url_for("varaus_info", varaus_id = varaus.id))

    
        return render_template("varaukset/varausinfo.html", form=form, varaus=varaus, matkakohde=dest, hotel=hotel, date = varaus.start_date,
                            matkustajat = passengers, lasku=varaus.bill_sent, maksettu=varaus.handled)
    else:
        return render_template("varaukset/varausinfo.html", varaus=varaus)



    