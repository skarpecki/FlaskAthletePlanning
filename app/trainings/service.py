from app import db
from .model import Training
from .model import Exercise
from ..users.model import  User

class TrainingService():
    @staticmethod
    def get_all_coach(id) -> list:
        trainings = Training.query.filter_by(coaches_id=id).all()
        return trainings

    @staticmethod
    def get_all_athlete(id):
        trainings = Training.query.filter_by(athletes_id=id).all()
        return trainings

    @staticmethod
    def get_by_args_coach(user_id, **kwargs):
        #security - if user pass different id in query than in JWT then take the one from JWT
        #TODO: Inform user about this situation
        try:
            if kwargs['coaches_id'] != user_id:
                kwargs['coaches_id'] = user_id
                result = Training.query.filter_by(**kwargs).all()
            elif kwargs['coaches_id'] == user_id:
                result = Training.query.filter_by(**kwargs).all()
        except KeyError:
            result = Training.query.filter_by(coaches_id=user_id, **kwargs).all()
        finally:
            return result


    @staticmethod
    def get_by_args_athlete(user_id, **kwargs):
        try:
            if kwargs['athletes_id'] != user_id:
                kwargs['athletes_id'] = user_id
                result = Training.query.filter_by(**kwargs).all()
            if kwargs['athletes_id'] == user_id:
                result = Training.query.filter_by(**kwargs).all()
        except KeyError:
            result = Training.query.filter_by(athletes_id=user_id, **kwargs).all()
        finally:
            return result


    @staticmethod
    def get_by_id(id):
        result = Training.query.get(id)
        return result



class ExercisesService():
    @staticmethod
    def get_by_id(id):
        result = Exercise.query.filter_by(trainings_id=id).all()
        return result
