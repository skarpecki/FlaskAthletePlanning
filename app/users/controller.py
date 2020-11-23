from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from .service import UserService
from .schema import UserSchema
from .model import User

class Users(Resource):
    
    def get(self) -> dict:
        #if no args were passed return all users from database
        if not request.args:
            user = UserService.get_all()
        else:
            try:
                #translating fields from userSchema to User fields (e.g. firstName to first_name) as the former is morep popular in the internet
                result = UserSchema().load(dict(request.args.items()))
            except ValidationError as err:
                return err.messages
        #user = UserService.get_by_args(**dict(request.args.items()))
        user = UserService.get_by_args(**result)
        return UserSchema().dump(user, many=True)


    #TODO: ask whether user should be able to post a data like fields names, e.g. first_name instead of fisrtName
    def post(self) -> User:
        try:
            result = UserSchema().load(request.get_json(force=True))
            UserService.create(result)
            return UserSchema().dump(result)
        except ValidationError as err:
            return err.messages





