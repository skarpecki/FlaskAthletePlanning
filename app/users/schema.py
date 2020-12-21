from marshmallow import fields, Schema

class UserSchema(Schema):
    """User Schema"""

    userID = fields.Integer(attribute='id')
    mailAddress = fields.String(attribute='mail_address')
    firstName = fields.String(attribute='first_name')
    lastName = fields.String(attribute='last_name')
    birthdate = fields.Date(attribute='birthdate')
    role = fields.String(attribute='role')
    password = fields.String(attribute='password')

class AthleteCoachSchema(Schema):
    """Schema of coach and athlete - without password"""
    userID = fields.Integer(attribute='id')
    mailAddress = fields.String(attribute='mail_address')
    firstName = fields.String(attribute='first_name')
    lastName = fields.String(attribute='last_name')
    birthdate = fields.Date(attribute='birthdate')
    role = fields.String(attribute='role')


class LoginSchema(Schema):
    """Login Schema"""
    mailAddress = fields.String(attribute='mail_address')
    password = fields.String(attribute='password')
