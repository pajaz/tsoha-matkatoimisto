# application/matkakohteet/models.py
from application import db

from sqlalchemy.sql import text

# Määritetään mallit tietokantataululle.
class Matkakohde(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    country = db.Column(db.String(30), nullable=False)
    depart = db.Column(db.String) # Viikonpäivä, jolloin kohteeseen lähdöt
    day_out = db.Column(db.String) # Viikonpäivä, jolloin kohteesta paluut
    price = db.Column(db.Integer) # Hinta joka sisältää matkat kohteeseen, sekä matkatoimiston palvelut
    intro = db.Column(db.String(500))                             
                                    
    # Määritellään riippuvuussuhde hotellien ja varausten kanssa.
    hotels = db.relationship("Hotelli", backref="Matkakohde", cascade="all, delete-orphan",
                             lazy=True)
    bookings = db.relationship("Varaus", backref="Matkakohde", cascade="all, delete-orphan", lazy=True)

    def __init__(self, name, country, depart = "Tyhjä", day_out = "Tyhjä", price = 0, intro = "Kohde-esittelyä ei ole vielä kirjoitettu"):
        self.name = name
        self.country = country
        self.depart = depart
        self.day_out = day_out
        self.price = price
        self.intro = intro


    # Metodi matkakohteiden hakemiseen maan, nimen tai molempien perusteella
    @staticmethod
    def find_destinations_by_name(name="", country=""):
        if country == "":
            stmt = text("SELECT * FROM Matkakohde"
                    " WHERE lower(name) LIKE lower(:name)").params(name=name)
        else:            
            stmt = text("SELECT * FROM Matkakohde"
                    " WHERE country=:country AND lower(name) LIKE lower(:name)").params(name=name,country=country)

                   
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "country":row[2]})

        return response

    # Palauttaa edellisen metodin kohteiden määrän
    @staticmethod
    def count_destinations_by_name(name="", country=""):
        if country == "":
            stmt = text("SELECT Count(*) FROM Matkakohde"
                    " WHERE lower(name) LIKE lower(:name)").params(name=name)
        else:            
            stmt = text("SELECT Count(*) FROM Matkakohde"
                    " WHERE country=:country AND lower(name) LIKE lower(:name)").params(name=name,country=country)

                   
        res = db.engine.execute(stmt)
        count = 0
        for row in res:
            count = row[0]

        return count 

    # Palauttaa n suosituinta matkakohdetta
    @staticmethod
    def most_popular_destinations(n=4):
        stmt = text("SELECT Matkakohde.id, Matkakohde.name, Matkakohde.country, Matkakohde.intro"
                    " FROM Matkakohde INNER JOIN (SELECT dest_id, count(*) as cnt"
                    " FROM Varaus GROUP BY dest_id ORDER BY cnt DESC LIMIT :n) AS Varaus"
                    " ON Matkakohde.id = Varaus.dest_id").params(n=n)
        
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "country":row[2], "introduction":row[3]})

        return response

    # Palauttaa matkakohteet joihin on tehty varauksia
    @staticmethod
    def destinations_with_bookings():
       

        stmt = text("SELECT Matkakohde.id, Matkakohde.name FROM Matkakohde"
                    " INNER JOIN Varaus ON Varaus.dest_id = Matkakohde.id"
                    " WHERE (Varaus.dest_id = Matkakohde.id)"
                    " GROUP BY Matkakohde.id ORDER BY Matkakohde.name")
            
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1]})
        
        return response
