from app import db
from datetime import datetime

class Logger(db.Model):
    __tablename__ = "logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    table = db.Column(db.String(45), nullable=False)
    column = db.Column(db.String(45), nullable=False)
    created_utc = db.Column(db.DateTime, nullable=False)
    old_value = db.Column(db.String(255), nullable=False)
    new_value = db.Column(db.String(255), nullable=False)

    @staticmethod
    def log_message(user_id, table, column, old_value, new_value, created_utc=datetime.utcnow()):
        logger = Logger(
            user_id=user_id,
            table=table,
            column=column,
            created_utc=created_utc,
            old_value=old_value,
            new_value=new_value
        )
        db.session.add(logger)
        db.session.commit()
        return logger.id

