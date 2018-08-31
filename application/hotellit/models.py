# application/hotellit/models.py
from application import db
from application.matkakohteet.models import Matkakohde

from sqlalchemy.sql import text

import datetime

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
             large_rooms, destination_id, price_small = 0, price_large = 0, email = None,
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
    
    # Palauttaa hotellit joihin on tehty varauksia
    @staticmethod
    def hotels_with_bookings():
       

        stmt = text("SELECT Hotelli.id, Hotelli.name, Hotelli.destination_id FROM Hotelli"
                    " LEFT JOIN Varaus ON Varaus.hotel_id = Hotelli.id"
                    " WHERE (Varaus.hotel_id = Hotelli.id)"
                    " GROUP BY Hotelli.destination_id")
            
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "destination":row[2]})
        
        print(response)

    
    def get_destination(self):
        stmt = text("SELECT Matkakohde.name FROM Hotelli INNER JOIN"
                    " Matkakohde ON Hotelli.destination_id = Matkakohde.id"
                    " WHERE :id = Matkakohde.id").params(id=self.id)

        res = db.engine.execute(stmt)

        destination = []
        for row in res:
            destination.append({"name":row[0]})
      
        return destination

    @staticmethod
    def get_destinations(hotel="%",dest="%", show=6, n=0):
        if dest == "%":
            stmt = text("SELECT Hotelli.id, Hotelli.name, Matkakohde.name, Matkakohde.id, Hotelli.star_rating FROM Hotelli"
                        " LEFT JOIN Matkakohde ON Hotelli.destination_id = Matkakohde.id"
                        " WHERE lower(Hotelli.name) LIKE lower(:name) ORDER BY Matkakohde.id"
                        " LIMIT :show OFFSET :n").params(name=hotel, show=show, n=n)
        else:
            stmt = text("SELECT Hotelli.id, Hotelli.name, Matkakohde.name, Matkakohde.id, Hotelli.star_rating FROM Hotelli"
                        " LEFT JOIN Matkakohde ON Hotelli.destination_id = Matkakohde.id"
                        " WHERE Hotelli.destination_id = :dest"
                        " AND lower(Hotelli.name) LIKE lower(:name) ORDER BY Matkakohde.id"
                        " LIMIT :show OFFSET :n").params(name=hotel, dest=dest, show=show, n=n)

        res = db.engine.execute(stmt)

        response = []

        for row in res:
            print(row)
            response.append({"hotel_id":row[0], "hotel_name":row[1], "dest_name":row[2], "dest_id":row[3], "star_rating":row[4]})

        return response

