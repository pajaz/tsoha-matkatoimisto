# application/varaukset/models.py
from application import db

from application.matkakohteet.models import Matkakohde
from application.hotellit.models import Hotelli
from application.auth.models import Kayttaja

# Määritellään mallit tietokantataululle
class Varaus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    #end_date = db.Column(db.Date, nullable=False)
    passengers = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    handled = db.Column(db.Boolean, nullable=False)    # Asiakas maksanut laskun ja saanut matkan dokumentit
    bill_sent = db.Column(db.Boolean, nullable=False)  # Asiakkaalle lähetetty lasku varauksesta
    small_rooms = db.Column(db.Integer, nullable=True) # Varaukseen liittyvät huoneet
    large_rooms = db.Column(db.Integer, nullable=True) 
    confirmed = db.Column(db.Boolean, nullable=False)

    # Riippuvuudet
    dest_id = db.Column(db.Integer, db.ForeignKey(Matkakohde.id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(Kayttaja.id), nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey(Hotelli.id), nullable=True)

    def __init__(self, start, price, user, dest, passengers, hotel = None, 
                 small_rooms = None, large_rooms = None):
        self.start_date = start
        self.price = price
        self.handled = False
        self.bill_sent = False
        self.user_id = user
        self.dest_id = dest
        self.passengers = passengers
        self.hotel_id = hotel
        self.small_rooms = small_rooms
        self.large_rooms = large_rooms
        self.confirmed = False