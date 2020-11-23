from marshmallow import fields, Schema

class TrainingSchema(Schema):
    trainingID = fields.Number(attribute='id')
    date = fields.DateTime(attribute='date')
    athleteFeedback = fields.String(attribute='athlete_feeback')
    coachFeedback = fields.String(attribute='coach_feedback')
    athleteID = fields.Number(attribute='athletes_id')
    coachID = fields.Number(attribute='coaches_id')


class ExerciseSchema(Schema):
    exerciseID = fields.Number(attribute='id')
    exerciseName = fields.String(attribute='exercise')
    sets = fields.Number(attribute='sets')
    reps = fields.Number(attribute='reps')
    rpe = fields.Float(attribute='rpe')
    trainingID = fields.Number(attribute='trainings_id')
