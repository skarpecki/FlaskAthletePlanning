from pytest import fixture
from .model import User
from .model import Role

@fixture
def user() -> User:
    return User(
        id = 1,
        mail_address = 'foo@foo.com',
        first_name = 'John',
        last_name = 'Doe',
        birthdate = '2000-01-11',
        role = Role.athlete,
        password = '!@#$1234'
    )

def test_User_create(user: User):
    assert user