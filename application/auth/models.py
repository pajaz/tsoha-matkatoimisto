# application/auth/models.py
from application import db
from sqlalchemy import text
import datetime

roles = db.Table("roles",
                    db.Column('role_id', db.Integer, db.ForeignKey("role.id"), primary_key=True),
                    db.Column("kayttaja_id", db.Integer, db.ForeignKey("kayttaja.id"), primary_key=True))

# Määritellään tietokantataulun malli
class Kayttaja(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    first_name = db.Column(db.String(24), nullable=False)
    last_name = db.Column(db.String(24), nullable=False)
    username = db.Column(db.String(24), nullable=False, unique=True)
    email = db.Column(db.String(48))
    phone_number = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    admin = db.Column(db.Integer, nullable=False) # admin = 1 user = 2
    roles = db.relationship('Role', secondary=roles, lazy='dynamic',
                                     backref=db.backref('users', lazy=True))

    # Riippuvuussuhde varausten kanssa
    bookings = db.relationship("Varaus", backref="Kayttaja", cascade="all, delete-orphan", lazy=True)

    def __init__(self, fname, lname, username, phone_number, password, role, email = "tyhjä"):
        self.first_name = fname
        self.last_name = lname
        self.username = username
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

    # Haetaan käyttäjälle asetetut roolit
    def roles(self):
        stmt = text("SELECT Role.name FROM Role"
                    " LEFT JOIN roles ON roles.role_id = role.id" 
                    " WHERE roles.kayttaja_id = :id").params(id=self.id)
        res = db.engine.execute(stmt)

        roolit = []
        for row in res:
            roolit.append(row[0])
       
        return roolit

    # Haetaan käyttäjän tekemien varausten tiedot
    def get_booking_infos(self):
        stmt = text("SELECT Varaus.id, Varaus.start_date, Matkakohde.name" 
                    " FROM Varaus INNER JOIN Matkakohde ON Varaus.dest_id = Matkakohde.id" 
                    " WHERE Varaus.user_id = :id").params(id=self.id)
        res = db.engine.execute(stmt)

        bookings = []
        for row in res:
            dt = datetime.datetime.strptime(row[1], "%Y-%m-%d")
            date = dt.strftime("%d.%m.%Y")
            bookings.append({"id":row[0], "start_date":date, "name":row[2]})

        return bookings


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(10), nullable=False, unique=True)

    def __str__(self):
        return self.name



