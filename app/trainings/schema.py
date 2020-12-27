from marshmallow import fields, Schema

class TrainingSchema(Schema):
    trainingID = fields.Integer(attribute='id')
    date = fields.Date(attribute='date')
    athleteFeedback = fields.String(attribute='athlete_feedback')
    coachFeedback = fields.String(attribute='coach_feedback')
    athleteID = fields.Integer(attribute='athletes_id')
    coachID = fields.Integer(attribute='coaches_id')

class ExerciseSchema(Schema):
    exerciseID = fields.Integer(attribute='id')
    exerciseName = fields.String(attribute='exercise')
    sets = fields.Integer(attribute='sets')
    reps = fields.Integer(attribute='reps')
    rpe = fields.Number(attribute='rpe')
    trainingID = fields.Integer(attribute='trainings_id')

class ExerciseUpdateSchema(Schema):
    exerciseName = fields.String(attribute='exercise')
    sets = fields.Integer(attribute='sets')
    reps = fields.Integer(attribute='reps')
    rpe = fields.Number(attribute='rpe')

