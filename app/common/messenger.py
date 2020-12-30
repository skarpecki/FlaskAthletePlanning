import smtplib, ssl
from datetime import date, datetime


# command to start smtp local server to fetch messages
# python -m smtpd -c DebuggingServer -n localhost:1025



class EmailHandler:
    def __init__(self, smtp_server, port, sender, context):
        self.smtp_server = smtp_server
        self.port = port
        self.sender = sender
        self.context = context
        self.db = None

    def run_local(self):
        server = smtplib.SMTP(self.smtp_server, self.port)
        server.ehlo()
        return server

    def init_db(self, db):
        self.db = db

    def log_mail(self, addresse, subject, message):
        if self.db is not None:
            metadata = self.db.MetaData()
            metadata.bind = self.db.engine
            mail_logs = self.db.Table("mail_logs", metadata,
                                      self.db.Column("mail_addresse", self.db.String(100), nullable=False),
                                      self.db.Column("subject", self.db.String(100), nullable=False),
                                      self.db.Column("message", self.db.String(255), nullable=False),
                                      self.db.Column("created_utc", self.db.DateTime, nullable=False))
            ins = mail_logs.insert().values(mail_addresse=addresse,
                                           subject=subject,
                                           message=message,
                                           created_utc=datetime.utcnow())
            conn = self.db.engine.connect()
            result = conn.execute(ins)
        else:
            raise TypeError("Database was not initialized")

    def new_training_msg(self, addresse, training, coach):
        try:
            server = self.run_local()
            subject = "Subject: New training scheduled on {}\n\n".format(str(training.date))
            message = "New training of id {} scheduled on {} by coach {} {}".format(training.id, str(training.date),
                                                                                    str(coach.first_name),
                                                                                    str(coach.last_name))
            server.sendmail(self.sender, addresse, subject + message)
            self.log_mail(addresse, subject, message)
        except Exception as e:
            server = None
            print("new_training_msg: {}".format(str(e)))
        finally:
            if server is not None:
                server.close()

    def updated_train_date_msg(self, addresse, old_date: datetime, training):
        try:
            server = self.run_local()
            subject = "Subject: Training on {} rescheduled\n\n".format(str(old_date.date()))
            message = "Training of id {} rescheduled from {} to {}".format(training.id, str(old_date.date()),
                                                                           str(training.date.date()))
            server.sendmail(self.sender, addresse, subject + message)
            self.log_mail(addresse, subject, message)
        except Exception as e:
            server = None
            print("updated_train_date_msg: {}".format(str(e)))
        finally:
            if server is not None:
                server.close()

    def new_exercise_msg(self, addresse, _date, exercise):
        try:
            server = self.run_local()
            subject = "Subject: New exercise scheduled on {}\n\n".format(str(_date))
            message = "Details of exercise: \n{}".format(str(exercise))
            server.sendmail(self.sender, addresse, subject + message)
            self.log_mail(addresse, subject, message)
        except Exception as e:
            server = None
            print("new_exercise_msg: {}".format(str(e)))
        finally:
            if server is not None:
                server.close()

    def update_exercise_msg(self, addresse, _date, old_exercise, new_exercise):
        try:
            server = self.run_local()
            subject = "Subject: Exercise scheduled on {} was modified\n\n".format(str(_date))
            message = "Old exercise details:\n{}\n" \
                      "New exercise details:\n{}\n".format(str(old_exercise), str(new_exercise))
            server.sendmail(self.sender, addresse, subject + message)
            self.log_mail(addresse, subject, message)
        except Exception as e:
            server = None
            print("update_exercise_msg: {}".format(str(e)))
        finally:
            if server is not None:
                server.close()


if __name__ == "__main__":
    context = ssl.create_default_context()
    handler = EmailHandler("localhost", 1025, "me@me.pl", context)
    _fields = {
        "reps": 10,
        "exerciseName": "deadlift",
        "sets": 10,
        "rpe": 7.0
    }

    _new_fields = {
        "reps": 5,
        "exerciseName": "deadlift",
        "sets": 5,
        "rpe": 7.0
    }

    handler.new_exercise_msg("athlete@athlete.com", date(2020, 1, 1), _fields)
    handler.update_exercise_msg("athlete@athlete.com", date(2020, 1, 1), _fields, _new_fields)
