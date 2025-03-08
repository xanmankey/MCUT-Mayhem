from models import sqlalchemy_db

# from sqlalchemy import Column, Integer, String


class Player(sqlalchemy_db.Model):
    __tablename__ = "players"

    id = sqlalchemy_db.Column(
        sqlalchemy_db.Integer, primary_key=True, autoincrement=True
    )
    username = sqlalchemy_db.Column(sqlalchemy_db.String, nullable=False, unique=True)
    score = sqlalchemy_db.Column(sqlalchemy_db.Integer, default=0)
    response = sqlalchemy_db.Column(sqlalchemy_db.String, nullable=False, default="")

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
