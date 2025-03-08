from models import sqlalchemy_db
from utils import QuestionType


class Question(sqlalchemy_db.Model):
    __tablename__ = "questions"

    id = sqlalchemy_db.Column(
        sqlalchemy_db.Integer, primary_key=True, autoincrement=True
    )
    number = sqlalchemy_db.Column(sqlalchemy_db.Integer, nullable=False)  # Slide number
    question = sqlalchemy_db.Column(sqlalchemy_db.String, nullable=False)
    question_type = sqlalchemy_db.Column(sqlalchemy_db.String, nullable=False)
    # sub_questions = sqlalchemy_db.Column(sqlalchemy_db.Integer, ForeignKey("questions.id"), nullable=True)
    time = sqlalchemy_db.Column(sqlalchemy_db.Integer, nullable=False, default=30)
    choices = sqlalchemy_db.Column(
        sqlalchemy_db.String, nullable=True
    )  # Comma separated string
    answer = sqlalchemy_db.Column(
        sqlalchemy_db.String, nullable=False
    )  # Comma separated string
    weight = sqlalchemy_db.Column(sqlalchemy_db.Float, default=1.0)
    asked = sqlalchemy_db.Column(sqlalchemy_db.Boolean, default=False)

    def __repr__(self):
        string = "<{}(".format(self.__class__.__name__)
        for field in self.__dict__:
            string += f"{field}: {getattr(self, field)}, "
        string = string[:-2] + ")>"
        return string

    def __str__(self):
        string = "<{}(".format(self.__class__.__name__)
        for field in self.__dict__:
            string += f"{field}: {getattr(self, field)}, "
        string = string[:-2] + ")>"
        return string
