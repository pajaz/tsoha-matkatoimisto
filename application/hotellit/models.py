from application import

class Hotelli(db.model):
    id = db.Colum(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    bookings = db.Column(db.Integer)
    small_rooms = db.Column(db.Integer) # max 2 hengen huoneet
    large_rooms = db.Column(db.Integer) # max 4 hengen huoneet
    price_small = db.Column(db.Integer) # hinta per yö
    price_large = db.Column(db.Integer)
    star_rating = db.Column(db.Integer, nullable=False) # 1-5 tähteä
    introduction = db.Column(db.String(500))

def __init__(self, name, star_rating, small_rooms = 0, large_rooms = 0,
             price_small = 0, price_large = 0, introduction = "Esittelyä ei ole vielä kirjoitettu"):
    self.name = name
    self.bookings = 0
    self.small_rooms = small_rooms
    self.large_rooms = large_rooms
    self.price_small = price_small
    self.price_large = price_large
    self.star_rating = star_rating
    self.introduction = introduction


