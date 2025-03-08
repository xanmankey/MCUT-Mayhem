# Creates a figma presentation with the corresponding questions
# This script just makes creating new presentations easier in the future
import os
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    request,
    render_template,
    url_for,
    g,
    session,
)
import sqlite3
from dotenv import load_dotenv
from models import sqlalchemy_db
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import random
from utils import Base, QuestionType

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

DB_PATH = "data.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"

sqlalchemy_db.init_app(app)

from models.questions import Question
from models.players import Player

with app.app_context():
    # Configure the sqlite3 db
    sqlalchemy_db.create_all()

# Link to a template with the corresponding figma slides components
TEMPLATE_WITH_COMPONENTS = ""

players = [
    Player(
        username="Player1",
        # score=random.randint(0, 100),
        score=0,
        response="B. John D McCutcheon",
    ),
    Player(
        username="Player2",
        # score=random.randint(0, 100),
        score=0,
        response="A. John T McCutcheon",
    ),
    Player(
        username="Player3",
        # score=random.randint(0, 100),
        score=0,
        response="A. John T McCutcheon",
    ),
    Player(
        username="Player4",
        # score=random.randint(0, 100),
        score=0,
        response="D. Bob",
    ),
    Player(
        username="Player5",
        # score=random.randint(0, 100),
        score=0,
        response="D. Bob",
    ),
    Player(
        username="Player6",
        # score=random.randint(0, 100),
        score=0,
        response="Rickrolled",
    ),
    Player(
        username="Player7",
        # score=random.randint(0, 100),
        score=0,
        response="20",
    ),
    Player(
        username="Player8",
        # score=random.randint(0, 100),
        score=0,
        response="D. Bob",
    ),
]


def create_players():
    for player in players:
        sqlalchemy_db.session.add(player)
    sqlalchemy_db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        create_players()
