# application/auth/models.py
from application import db
from sqlalchemy import text


roles = db.Table("roles",
                    db.Column('role_id', db.Integer, db.ForeignKey("role.id"), primary_key=True),
                    db.Column("kayttaja_id", db.Integer, db.ForeignKey("kayttaja.id"), primary_key=True))

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
    admin = db.Column(db.Integer, nullable=False) # admin = 1 user = 2
    roles = db.relationship('Role', secondary=roles, lazy='subquery',
                                     backref=db.backref('users', lazy=True))

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

    def roles(self):
        stmt = text("SELECT Role.name FROM Role"
                    " LEFT JOIN roles ON roles.role_id = role.id" 
                    " WHERE roles.kayttaja_id = :id").params(id=self.id)
        res = db.engine.execute(stmt)

        roolit = []
        for row in res:
            roolit.append(row[0])
       
        return roolit

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(10), nullable=False, unique=True)

    def __str__(self):
        return self.name



