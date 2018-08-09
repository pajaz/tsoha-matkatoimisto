from application import db

class Kayttaja(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50))
    phone_number = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(144), nullable=False)


    def __init__(self, fname, lname, uname, phone_number, password, email = "tyhjä"):
        self.first_name = fname
        self.last_name = lname
        self.username = uname
        self.email = email
        self.phone_number = phone_number
        self.password = password

    def get_id(self):
        return self.id
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True