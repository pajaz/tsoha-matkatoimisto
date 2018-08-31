# application/matkustajat/models.py
from application import db
from sqlalchemy.sql import text
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


    # Matkustajat ovat olemassa tietokannassa vain varausten kanssa
    # Seuraava metodi poistaa orvoksi jääneen matkustajan (kutsutaan, kun matkustaja poistetaan varauksesta)
    @staticmethod
    def delete_orphan(id):
        stmt = text("SELECT matkustaja_id FROM matkustaja_varaus"
                    " WHERE matkustaja_varaus.matkustaja_id = :id").params(id=id)
        res = db.engine.execute(stmt)
        t = []
        for row in res:
            t.append(row[0])
        if t:
            return "Ei poistettuja"

        stmt = text("DELETE FROM Matkustaja WHERE id = :id").params(id=id)
        db.engine.execute(stmt)
        return "Poistettu matkustaja id:llä " + id

    # Poistaa kaikki orvot matkustajat
    @staticmethod
    def delete_orphans():
        stmt = text("DELETE FROM Matkustaja WHERE Matkustaja.id IN"
                    " (SELECT matkustaja_id FROM matkustaja_varaus)")
        db.engine.execute(stmt)

        return "Poistettu orvot matkustajat"