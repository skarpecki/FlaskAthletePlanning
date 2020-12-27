from functools import wraps
from jwt import ExpiredSignature, DecodeError
from flask import jsonify, make_response
from flask_jwt_extended.exceptions import NoAuthorizationError


def catch_jwt_exceptions(func):
    """
    Catch ExpiredSignature exception which is raised by @JWTRequireed decorator,
    and cannot be caught in body of function decorated by @JWTRequired. If Expired signature
    is caught, then returns message and 401 non authorized HTTP code
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ExpiredSignature:
            return make_response(jsonify({"message": "JWT Token is expired"}), 401)
        except DecodeError:
            return make_response(jsonify({"message": "JWT Token is invalid"}), 401)
        except NoAuthorizationError:
            return make_response(jsonify({"message": "JWT Token is missing"}), 401)

    return wrapper
