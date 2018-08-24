# application/matkustajat/models.py
from application import db

# Tietokantataulun maääritys
class Matkustaja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    socialsec = db.Column(db.String(11), unique=True, nullable=False)

    def __init__(self, fname, lname, socsec):
        self.first_name = fname
        self.last_name = lname
        self.socialsec = socsec