# application/varaukset/models.py
from sqlalchemy.sql import text

from application import db
import datetime
from application.matkakohteet.models import Matkakohde
from application.hotellit.models import Hotelli
from application.auth.models import Kayttaja
from application.matkustajat.models import Matkustaja


matkustaja_varaus = db.Table("matkustaja_varaus",
                             db.Column("matkustaja_id", db.Integer, db.ForeignKey("matkustaja.id"), primary_key=True),
                             db.Column("varaus_id", db.Integer, db.ForeignKey("varaus.id"), primary_key=True))


# Määritellään mallit tietokantataululle
class Varaus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    passengers = db.Column(db.Integer, nullable=False) # Matkustajien määrä
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
    matkustajat = db.relationship("Matkustaja", secondary=matkustaja_varaus, lazy="dynamic",
                                  backref=db.backref("varaukset", lazy=True))

    def __init__(self, start, end, price, user, dest, passengers, hotel, 
                 small_rooms = 0, large_rooms = 0):
        self.start_date = start
        self.end_date = end
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
  
    def booking_hotel(self):
        stmt = text("SELECT id FROM Hotelli"
                    " WHERE Hotelli.id = :id").params(id=self.hotel_id)
        res = db.engine.execute(stmt)
        hotel = []
        for row in res:
            hotel.append(row[0])
        return hotel
    
    def booking_dest(self):
        stmt = text("SELECT id FROM Matkakohde"
                    " WHERE Matkakohde.id = :id").params(id=self.dest_id)
        res = db.engine.execute(stmt)
        dest = []
        for row in res:
            print(row)
            dest.append(row[0])
        return dest
    
    def booking_user(self):
        stmt = text("SELECT id FROM Kayttaja"
                    " WHERE Kayttaja.id = :id").params(id=self.dest_id)
        res = db.engine.execute(stmt)
        dest = []
        for row in res:
            dest.append(row[0])
        return dest
  
    def booking_passengers(self):
        stmt = text("SELECT Matkustaja.first_name, Matkustaja.last_name, Matkustaja.socialsec, Matkustaja.id FROM Matkustaja"
                    " LEFT JOIN matkustaja_varaus mv ON mv.matkustaja_id = matkustaja.id" 
                    " WHERE mv.varaus_id = :id").params(id=self.id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append((row[0], row[1], row[2], row[3]))
        return response
    
    def delete_passenger_from_booking(self, pas_id):
        stmt = text("DELETE FROM matkustaja_varaus WHERE matkustaja_id=:m_id AND varaus_id=:v_id").params(m_id=pas_id, v_id=self.id)

        db.engine.execute(stmt)

        return "Done"

    # Metodi varausten hakuun kohteen perusteella.
    @staticmethod
    def find_bookings_by_dest(dest=""):
      
        stmt = text("SELECT id, dest_id, confirmed, bill_sent, handled FROM Varaus"
                    " WHERE dest_id = :dest").params(dest=dest)
                   
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "dest_id":row[1]})

        return response

    # Nyt on aika kääntää katseet pois, koska seuraavan saisi varmaan tehtyä helpomminkin.
    # Metodi palauttaa Varaus-sivun (varaukset/list.html) haun mukaisen tuloksen. Koska erilaisia tuloksia on 16kpl,
    # tässä 16 hieman toisistaan poikkeavaa statementtia
    @staticmethod
    def search_bookings(dest=0, handled=2, status="", n=0, show=6):
        today = datetime.datetime.today()
        if dest != 0:
            if handled == 2:
                if status == "past":
                    stmt = text("SELECT Varaus.id, Matkakohde.name, Varaus.start_date, Varaus.handled FROM Varaus"
                                " INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id"
                                " WHERE Varaus.dest_id = :dest"
                                " AND Varaus.end_date < :today ORDER BY Varaus.start_date").params(today=today, dest=dest)
                elif status == "future":
                    stmt = text("SELECT Varaus.id, Matkakohde.name, Varaus.start_date, Varaus.handled FROM Varaus"
                                " INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id"
                                " WHERE Varaus.dest_id = :dest"
                                " AND Varaus.start_date > :today ORDER BY Varaus.start_date").params(today=today, dest=dest)
                elif status == "active":
                    stmt = text("SELECT Varaus.id, Matkakohde.name, Varaus.start_date, Varaus.handled FROM Varaus"
                                " INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id"
                                " WHERE Varaus.dest_id = :dest"
                                " AND Varaus.start_date < :today AND Varaus.end_date > :today ORDER BY Varaus.start_date").params(today=today, dest=dest)   #101
                else:
                    stmt = text("SELECT Varaus.id, Matkakohde.name, Varaus.start_date, Varaus.handled FROM Varaus"
                                " INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id"
                                " AND Varaus.dest_id = :dest ORDER BY Varaus.start_date").params(dest=dest)                                                 #100
            else:
                if status == "past":
                    stmt = text("SELECT Varaus.id, Matkakohde.name, Varaus.start_date, Varaus.handled FROM Varaus"
                                " INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id"
                                " WHERE Varaus.dest_id = :dest"
                                " AND Varaus.end_date < :today AND handled=:handled ORDER BY Varaus.start_date").params(today=today, dest=dest, handled=handled)
                elif status == "future":
                    stmt = text("SELECT Varaus.id, Matkakohde.name, Varaus.start_date, Varaus.handled FROM Varaus"
                                " INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id"
                                " WHERE Varaus.dest_id = :dest"
                                " AND Varaus.start_date > :today AND handled=:handled ORDER BY Varaus.start_date").params(today=today, dest=dest, handled=handled)
                elif status == "active":
                    stmt = text("SELECT Varaus.id, Matkakohde.name, Varaus.start_date, Varaus.handled FROM Varaus"
                                " INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id"
                                " WHERE Varaus.dest_id = :dest"
                                " AND Varaus.start_date < :today AND Varaus.end_date > :today"
                                " AND handled=:handled ORDER BY Varaus.start_date").params(today=today, dest=dest, handled=handled)                         #111
                else:
                    stmt = text("SELECT Varaus.id, Matkakohde.name, Varaus.start_date, Varaus.handled FROM Varaus"
                                " INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id"
                                " WHERE Varaus.dest_id = :dest AND Varaus.handled = :handled"
                                " ORDER BY Varaus.start_date").params(dest=dest, handled=handled)                                                           #110
        elif dest == 0:
            if handled == 2:
                if status == "past":
                    stmt = text("SELECT Varaus.id, Matkakohde.name, Varaus.start_date, Varaus.handled FROM Varaus"
                                " INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id"
                                " WHERE Varaus.end_date < :today ORDER BY Varaus.start_date").params(today=today)
                elif status == "future":
                    stmt=text("SELECT Varaus.id, Matkakohde.name, Varaus.start_date, Varaus.handled FROM Varaus"
                                " INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id"
                                " WHERE Varaus.start_date > :today ORDER BY Varaus.start_date").params(today=today)
                elif status == "active":
                    stmt = text("SELECT Varaus.id, Matkakohde.name, Varaus.start_date, Varaus.handled FROM Varaus"
                                " INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id"
                                " AND Varaus.start_date < :today AND Varaus.end_date > :today ORDER BY Varaus.start_date").params(today=today)              #001
                else:
                    stmt = text("SELECT Varaus.id, Matkakohde.name, Varaus.start_date, Varaus.handled FROM Varaus"
                                " INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id ORDER BY Varaus.start_date"
                                " LIMIT :show OFFSET :n").params(n=n, show=show)                                      #000
            if handled != 2:
                if status == "past":
                    stmt = text("SELECT Varaus.id, Matkakohde.name, Varaus.start_date, Varaus.handled FROM Varaus"
                                " INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id"
                                " WHERE Varaus.end_date < :today AND Varaus.handled = :handled ORDER BY Varaus.start_date").params(today=today, handled=handled)
                elif status == "future":
                    stmt=text("SELECT Varaus.id, Matkakohde.name, Varaus.start_date, Varaus.handled FROM Varaus"
                                " INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id"
                                " WHERE Varaus.start_date > :today AND Varaus.handled = :handled ORDER BY Varaus.start_date").params(today=today, handled=handled)
                elif status == "active":
                    stmt = text("SELECT Varaus.id, Matkakohde.name, Varaus.start_date, Varaus.handled FROM Varaus"
                                " INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id"
                                " AND Varaus.start_date < :today AND Varaus.handled = :handled" 
                                " AND Varaus.end_date > :today ORDER BY Varaus.start_date").params(today=today, handled=handled)                            #011
                else:
                    stmt = text("SELECT Varaus.id, Matkakohde.name, Varaus.start_date, Varaus.handled FROM Varaus"
                                " INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id"
                                " WHERE Varaus.handled = :handled ORDER BY Varaus.start_date").params(handled=handled)                                      #010
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            if type(row[2]) == str: # String -check tässä, koska paikallisesti rivin tyyppi on str ja herokussa datetime.
                dt = datetime.datetime.strptime(row[2], "%Y-%m-%d")
            else:
                dt = row[2]
            date = dt.strftime("%d.%m.%Y") # Muutetaan päiväys eurooppalaisittain tutumpaan muotoon.
            response.append({"id":row[0], "dest_name":row[1], "start_date":date, "handled":row[3]})

        return response