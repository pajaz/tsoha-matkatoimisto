from application import db

class Matkakohde(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    intro = db.Column(db.String(500))
    bookings = db.Column(db.Integer)

    def __init__(self, name, country, intro = "Kohde-esittelyä ei ole vielä kirjoitettu", bookings = 0):
        self.name = name
        self.country = country
        self.intro = intro
        self.bookings = 0
