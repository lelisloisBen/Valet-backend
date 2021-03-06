from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appID = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120) )
    password = db.Column(db.String(80), nullable=False, unique=True)
    birthdate = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    zipCode = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    admin = db.Column(db.Integer)

    def __repr__(self):
        return '<users %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "appID": self.appID,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zipCode": self.zipCode,
            "phone": self.phone,
            "admin": self.admin
        }