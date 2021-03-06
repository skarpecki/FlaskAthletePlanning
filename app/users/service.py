from passlib.hash import bcrypt

from app import db
from .model import User
from app.common.logger import Logger
from datetime import datetime


class UserService:
    @staticmethod
    def get_all(coach_id) -> list:
        metadata = db.MetaData()
        metadata.bind = db.engine
        #create view table
        vUserCoach = db.Table("vcoaches_athletes", metadata,
                              db.Column("coach_id", db.Integer, primary_key=True),
                              db.Column("athlete_id", db.Integer, db.ForeignKey("users.id")),
                              autoload=True)
        coach_athlete = db.session.query(vUserCoach).filter(vUserCoach.columns.coach_id == coach_id).all()
        #coach_athlete is a list of tuples of (coach_id, athlete_id)
        athletes_ids = [t[1] for t in coach_athlete]
        athletes = User.query.filter(User.id.in_(athletes_ids)).all()
        return athletes

    @staticmethod
    def get_by_args(**kwargs) -> User:
        user = User.query.filter_by(**kwargs).all()
        return user


    @staticmethod
    def create(attrs):
        user = User(
            mail_address=attrs["mail_address"],
            first_name=attrs["first_name"],
            last_name=attrs["last_name"],
            birthdate=attrs["birthdate"],
            role=attrs["role"],
            password=bcrypt.using().hash(attrs["password"])
        )
        db.session.add(user)    
        db.session.commit()
        Logger.log_message(user.id, 'user', 'mail_address', 'null', user.mail_address)
        return user.id


class LoginService:
    @staticmethod
    def authenticate(mail_address) -> User:
        user = User.query.filter(User.mail_address == mail_address).first()
        return user
