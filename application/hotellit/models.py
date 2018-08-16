# application/hotellit/models.py
from application import db

from application.matkakohteet.models import Matkakohde

# Määritetään mallit tietokantataululle.
class Hotelli(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(60), nullable=False)      # Ei näytetä asiakkaalle
    phone_number = db.Column(db.String(20), nullable=False) # Ei näytetä asiakkaalle
    email = db.Column(db.String(30))                        # Ei näytetä asiakkaalle
    small_rooms = db.Column(db.Integer) # max 2 hengen huoneet
    large_rooms = db.Column(db.Integer) # max 4 hengen huoneet
    price_small = db.Column(db.Integer) # hinta / 
    price_large = db.Column(db.Integer) # viikko
    star_rating = db.Column(db.Integer, nullable=False) # 1-5 tähteä
    introduction = db.Column(db.String(500))

    # Liitetään jokaiseen luotuun hotelliin yksi Matkakohde.
    destination_id = db.Column(db.Integer, db.ForeignKey(Matkakohde.id), nullable=False)

    # Riippuvuussuhde varausten kanssa
    bookings = db.relationship("Varaus", backref="Hotel", cascade="all, delete-orphan", lazy=True)


    def __init__(self, name, address, phone_number, star_rating, small_rooms, 
             large_rooms, price_small, price_large, email, destination_id,
             introduction = "Esittelyä ei ole vielä kirjoitettu"):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.small_rooms = small_rooms
        self.large_rooms = large_rooms
        self.price_small = price_small
        self.price_large = price_large
        self.star_rating = star_rating
        self.destination_id = destination_id
        self.introduction = introduction


