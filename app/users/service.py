from app import db
import sys
from passlib.hash import bcrypt
from .model import User



class UserService():
    @staticmethod
    def get_all() -> list:
        return User.query.all()

    @staticmethod
    def get_by_args(**kwargs) -> User:
        print(kwargs)
        user = User.query.filter_by(**kwargs).all()
        return user


    @staticmethod
    def create(attrs) -> User:
        user = User(
            mail_address = attrs["mail_address"],
            first_name = attrs["first_name"],
            last_name = attrs["last_name"],
            birthdate = attrs["birthdate"],
            role = attrs["role"],
            password = bcrypt.hash(attrs["password"])
        )

        db.session.add(user)    
        db.session.commit()

        return user

class LoginService():
    @staticmethod
    def authenticate(mail_address, password) -> User:
        user = User.query.filter(User.mail_address == mail_address)
        return user
    