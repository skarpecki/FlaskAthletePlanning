from app import db
from enum import Enum

class Role(Enum):
    athlete = 1
    coach = 2
    #without defining a str it is impossible for marshmallow to translate enum to json
    def __str__(self):
        return self.name


class User(db.Model):
    """User model class"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    mail_address = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class vCoachAthlete(db.Model):
    coach_id = db.Column(db.Integer)
