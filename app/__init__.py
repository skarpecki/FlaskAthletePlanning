from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import sys


db = SQLAlchemy()
jwt = JWTManager()

def create_app(test_config=None) -> 'Flask app':

    
    app = Flask(__name__)
    api = Api(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:user@localhost/athlete_planning'
    app.config['JWT_SECRET_KEY'] = 'dev'
    db.init_app(app)
    jwt.init_app(app)


    from app.users import controller as users_controller
    api.add_resource(users_controller.Users, '/users')
    api.add_resource(users_controller.Login, '/users/login')

    from app.trainings import controller as trainings_controller
    api.add_resource(trainings_controller.TrainingsSearch, '/trainings')
    api.add_resource(trainings_controller.Trainings, '/trainings/<int:training_id>')
    #api.add_resource(trainings_controller.Exercises, '/exercises')
    api.add_resource(trainings_controller.Exercises, '/trainings/<int:training_id>/exercises')
    api.add_resource(trainings_controller.ExercisesWithID, '/trainings/<int:training_id>/exercises/<int:exercise_id>')


    

    # me = model.Athlete(id=1)
    # with app.app_context():
    #     db.session.add(me)
    #     db.session.commit()


    return app
