from functools import wraps
from jwt import ExpiredSignature
from flask import jsonify, make_response


def catch_jwt_expired_token(func):
    """
    Catch ExpiredSignature exception which is raised by @JWTRequireed decorator,
    and cannot be caught in body of function decorated by @JWTRequired. If Expired signature
    is caught, then returns message and 401 non authorized HTTP code
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except ExpiredSignature:
            result = make_response(jsonify({"message ": "JWT Token is expired"}), 401)
        finally:
            return result
    return wrapper
