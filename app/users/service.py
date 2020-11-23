from app import db
import sys
from werkzeug.security import generate_password_hash
from .model import User


class UserService():
    @staticmethod
    def get_all() -> list:
        return User.query.all()

    @staticmethod
    def get_by_args(**kwargs) -> User:
        user = User.query.filter_by(**kwargs).all()
        return user


    @staticmethod
    def create(attrs) -> User:
        user = User(
            mail_address=attrs["mail_address"],
            first_name = attrs["first_name"],
            last_name = attrs["last_name"],
            birthdate = attrs["birthdate"],
            role = attrs["role"],
            password = generate_password_hash(attrs["password"], method='sha256')
        )

        db.session.add(user)    
        db.session.commit()

        return user

    