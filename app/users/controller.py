from flask import request, jsonify, make_response
from flask_restful import Resource
from marshmallow import ValidationError
from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token, get_jwt_claims, jwt_required
from jwt import ExpiredSignature
from sqlalchemy.exc import IntegrityError

from app import jwt
from .service import UserService, LoginService
from .schema import UserSchema, AthleteCoachSchema, LoginSchema
from .model import User



class Users(Resource):

    @catch_jwt_expired_token
    @jwt_required
    def get(self) -> dict:
        claims = get_jwt_claims()
        if claims["role"] != "coach":
            return {"error": "non authorized access"}, 401
        # if no args were passed return all users from database
        if not request.args:
            user = UserService.get_all(claims["userID"])
        else:
            try:
                result = UserSchema().load(dict(request.args.items()))
                user = UserService.get_by_args(**result)
            except ValidationError as err:
                return err.messages
            except KeyError as err:
                return {"error": "wrong data provided"}

        return AthleteCoachSchema().dump(user, many=True)


    def post(self) -> User:
        try:
            attrs = UserSchema().load(request.get_json(force=True))
            id = UserService.create(attrs)
            return {"User account created succesfully. ID of user": id}
        except ValidationError as err:
            return err.messages
        except IntegrityError as err:
            return {"error": "Provided mail address already exists"}


class Login(Resource):
    @jwt.user_claims_loader
    def add_claims_to_access_token(user):
        return {"userID": user['userID'],
                "role": user['role']}


    @catch_jwt_expired_token
    @jwt_required
    def get(self):
        try:
            claims = get_jwt_claims()
            return jsonify({
                "userID": claims['userID'],
                "role": claims["role"]
            })
        except jwt.ExpiredSignature as err:
            print("exception")
            return {"message": err}


    def post(self):
        try:
            result = LoginSchema().load(request.get_json(force=True))
            user = LoginService().authenticate(result)
            user = UserSchema().dump(user)
            #moving below code to service will require mapping "id" from database table
            #to "userID" what is here done by dumping user with UserSchema
            if bcrypt.verify(result['password'], user['password']):
                access_token = create_access_token(user)
                return make_response(jsonify(access_token), 200)
            else:
                return {"message": "wrong password"}
        except ValidationError as err:
            return err.messages
        except KeyError as err:
            print(err)
            return {"error": "wrong data provided"}, 400
        # index error may be raised by UserSchema().dump(user[0]) if no user is returned by query
        except IndexError as err:
            print(err)
            return {"message": "wrong e-mail or password"}, 400
