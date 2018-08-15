# application/matkakohteet/models.py
from application import db

# Määritetään mallit tietokantataululle.
class Matkakohde(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    country = db.Column(db.String(30), nullable=False)
    bookings = db.Column(db.Integer)
    depart = db.Column(db.String) # Viikonpäivä, jolloin kohteeseen lähdöt
    day_out = db.Column(db.String) # Viikonpäivä, jolloin kohteesta paluut
    price = db.Column(db.Integer) # Hinta joka sisältää matkat kohteeseen, sekä matkatoimiston palvelut
    intro = db.Column(db.String(500))                             
                                    
    # Määritellään riippuvuussuhde hotellien kanssa. Toistaiseksi poistettu!
    #hotels = db.relationship("Hotelli", backref="matkakohde", lazy=True)

    def __init__(self, name, country, depart = "Tyhjä", day_out = "Tyhjä", price = 0, intro = "Kohde-esittelyä ei ole vielä kirjoitettu", bookings = 0):
        self.name = name
        self.country = country
        self.bookings = 0
        self.depart = depart
        self.day_out = day_out
        self.price = price
        self.intro = intro

