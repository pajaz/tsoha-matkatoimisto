# application/auth/models.py
from application import db

# Määritellään tietokantataulun malli
class Kayttaja(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    first_name = db.Column(db.String(24), nullable=False)
    last_name = db.Column(db.String(24), nullable=False)
    username = db.Column(db.String(24), nullable=False)
    email = db.Column(db.String(48))
    phone_number = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    admin = db.Column(db.Boolean, nullable = False) # admin = True, user = False

    # Riippuvuussuhde varausten kanssa
    bookings = db.relationship("Varaus", backref="Kayttaja", cascade="all, delete-orphan", lazy=True)

    def __init__(self, fname, lname, uname, phone_number, password, role, email = "tyhjä"):
        self.first_name = fname
        self.last_name = lname
        self.username = uname
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.admin = role

    def get_id(self):
        return self.id
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True