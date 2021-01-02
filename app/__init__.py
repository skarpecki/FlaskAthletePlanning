from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from ssl import create_default_context

from app.common.messenger import EmailHandler

context = create_default_context()
handler = EmailHandler("localhost", 1025, "me@me.pl", context)
db = SQLAlchemy()
jwt = JWTManager()
app = Flask(__name__)


def create_app(test_config=None) -> 'Flask app':
    api = Api(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:user@localhost/athlete_planning'
    app.config['JWT_SECRET_KEY'] = 'dev'
    db.init_app(app)
    jwt.init_app(app)
    handler.init_db(db)

    from app.users import controller as users_controller
    api.add_resource(users_controller.Users, '/users')
    api.add_resource(users_controller.Login, '/users/login')

    from app.trainings import controller as trainings_controller
    api.add_resource(trainings_controller.TrainingsSearch, '/trainings')
    api.add_resource(trainings_controller.Trainings, '/trainings/<int:training_id>')
    # api.add_resource(trainings_controller.Exercises, '/exercises')
    api.add_resource(trainings_controller.Exercises, '/trainings/<int:training_id>/exercises')
    api.add_resource(trainings_controller.ExercisesWithID, '/trainings/<int:training_id>/exercises/<int:exercise_id>')

    # me = model.Athlete(id=1)
    # with app.app_context():
    #     db.session.add(me)
    #     db.session.commit()
    return app
