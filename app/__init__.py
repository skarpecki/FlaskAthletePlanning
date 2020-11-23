from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import sys


db = SQLAlchemy()

def create_app(test_config=None) -> 'Flask app':

    
    app = Flask(__name__)
    api = Api(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:user@localhost/athlete_planning'
    db.init_app(app)


    from app.users import controller as users_controller
    api.add_resource(users_controller.Users, '/users')

    from app.trainings import controller as trainings_controller
    api.add_resource(trainings_controller.Trainings, '/trainings')
    api.add_resource(trainings_controller.Exercises, '/exercises')


    

    # me = model.Athlete(id=1)
    # with app.app_context():
    #     db.session.add(me)
    #     db.session.commit()


    return app
