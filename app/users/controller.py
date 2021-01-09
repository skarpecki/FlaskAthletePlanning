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
from app.common.jwt_exceptions_handler import catch_jwt_exceptions



class Users(Resource):

    @catch_jwt_exceptions
    @jwt_required
    def get(self) -> dict:
        claims = get_jwt_claims()
        if claims["role"] != "coach":
            return make_response(jsonify({"error": "non authorized access"}), 401)
        # if no args were passed return all users from database
        if not request.args:
            users = UserService.get_all(claims["userID"])
        else:
            try:
                result = UserSchema().load(dict(request.args.items()))
                users = UserService.get_by_args(**result)
            except ValidationError as err:
                return make_response(err.messages, 400)
            except KeyError as err:
                return make_response(jsonify({"error": "wrong data provided"}), 400)
        status = 404 if len(users) == 0 else 200
        return make_response(jsonify(AthleteCoachSchema().dump(users, many=True)), status)


    def post(self) -> User:
        try:
            attrs = UserSchema().load(request.get_json(force=True))
            id = UserService.create(attrs)
            return make_response(jsonify({"User account created succesfully. ID of user": id}),201)
        except ValidationError as err:
            return make_response(err.messages, 400)
        except IntegrityError as err:
            response = {"error": "Provided mail address is already registered"}
            return make_response(jsonify(response), 400)

class Login(Resource):
    @jwt.user_claims_loader
    def add_claims_to_access_token(user):
        return {"userID": user['userID'],
                "role": user['role']}


    @catch_jwt_exceptions
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
            user = LoginService().authenticate(result["mail_address"])
            user = UserSchema().dump(user)
            #moving below code to service will require mapping "id" from database table
            #to "userID" what is here done by dumping user with UserSchema
            if bcrypt.verify(result['password'], user['password']):
                access_token = create_access_token(user)
                return make_response(jsonify(access_token), 200)
            else:
                return make_response(jsonify({"message": "wrong password"}), 400)
        except ValidationError as err:
            return make_response(err.messages, 400)
        # index error may be raised by UserSchema().dump(user[0]) if no user is returned by query
        except (IndexError, KeyError):
            return make_response(jsonify({"message": "wrong e-mail or password"}), 400)
