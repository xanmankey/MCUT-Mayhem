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

questions = [
    Question(
        number=1,
        question="Who was McCutcheon Hall named after?",
        question_type=QuestionType.MULTIPLE_CHOICE.value,
        choices="A. John T McCutcheon,B. John D McCutcheon,C. John C McCutcheon,D. Bob",
        answer="A. John T McCutcheon",
        time=1,
    ),
    Question(
        number=2,
        question="Guess the Song",
        question_type=QuestionType.MULTIPLE_CHOICE.value,
        choices="A. Monday Night Football,B. Thursday Night Football,C. Sunday Night Football",
        answer="A. Monday Night Football",
        time=5,
    ),
    Question(
        number=3,
        question="What you'll be after reading the starts of the starred entries?",
        question_type=QuestionType.SHORT_ANSWER.value,
        answer="Rickrolled",
        time=1,
    ),
    Question(
        number=4,
        question="Guess the Flag",
        question_type=QuestionType.SHORT_ANSWER.value,
        answer="West Lafayette",
        time=5,
    ),
    Question(
        number=5,
        question="Who Said That?",
        question_type=QuestionType.SHORT_ANSWER.value,
        answer="Vizzini",
        weight=0.4,
        time=15,
    ),
    Question(
        number=6,
        question="Who Said That?",
        question_type=QuestionType.SHORT_ANSWER.value,
        answer="Fawful",
        weight=0.4,
        time=15,
    ),
    Question(
        number=7,
        question="Who Said That?",
        question_type=QuestionType.SHORT_ANSWER.value,
        answer="Homer Simpson",
        weight=0.4,
        time=15,
    ),
    Question(
        number=8,
        question="Who Said That?",
        question_type=QuestionType.SHORT_ANSWER.value,
        answer="Vito Corleone,Don Corleone,Don Vito Corleone,The Godfather",
        weight=0.4,
        time=15,
    ),
    Question(
        number=9,
        question="Who Said That?",
        question_type=QuestionType.SHORT_ANSWER.value,
        answer="Winnie the Pooh",
        weight=0.4,
        time=15,
    ),
    Question(
        number=10,
        question="Solve the Puzzle (Algebraic Chess Notation)",
        question_type=QuestionType.SHORT_ANSWER.value,
        answer="QB5+",
    ),
    Question(
        number=11,
        question="What DIDN’T happen during the marathon at the 1904 Summer Olympics?",
        question_type=QuestionType.MULTIPLE_CHOICE.value,
        choices="A. 5th place stopped for dinner,B. A racer hitched a ride in a car,C. 4th place took a nap,D. The winner was given rat poison",
        answer="A. 5th place stopped for dinner",
    ),
    Question(
        number=12,
        question="How many meters of Steel Chain did Michel Lotito consume?",
        question_type=QuestionType.NUMBERS.value,
        answer="500",
    ),
    Question(
        number=13,
        question="How many calories?",
        question_type=QuestionType.NUMBERS.value,
        answer="2100",
        weight=0.4,
        time=15,
    ),
    Question(
        number=14,
        question="How many calories?",
        question_type=QuestionType.NUMBERS.value,
        answer="2800",
        weight=0.4,
        time=15,
    ),
    Question(
        number=15,
        question="How many calories?",
        question_type=QuestionType.NUMBERS.value,
        answer="1000",
        weight=0.4,
        time=15,
    ),
    Question(
        number=16,
        question="How many calories?",
        question_type=QuestionType.NUMBERS.value,
        answer="1200",
        weight=0.4,
        time=15,
    ),
    Question(
        number=17,
        question="How many calories?",
        question_type=QuestionType.NUMBERS.value,
        answer="12000",
        weight=0.4,
        time=15,
    ),
    Question(
        number=18,
        question="How long was the longest hiccupping spree in history?",
        question_type=QuestionType.MULTIPLE_CHOICE.value,
        choices="A. 1 year,B. 2 years,C. 3 years,D. 68 years",
        answer="D. 68 years",
    ),
    Question(
        number=19,
        question="Approximately how many hiccups did Charles have?",
        question_type=QuestionType.NUMBERS.value,
        answer="430 million,430000000",
    ),
    Question(
        number=20,
        question="Which micronation is located in the US?",
        question_type=QuestionType.MULTIPLE_CHOICE.value,
        choices="A. Republic of Molossia,B. Kingdom of Talossa,C. The Conch Republic,D. All of the above",
        answer="D. All of the above",
    ),
    Question(
        number=21,
        question="How to kill?",
        question_type=QuestionType.MULTIPLE_CHOICE.value,
        choices="A. Flying,B. Electric,C. Fairy,D. Ice",
        answer="A. Flying",
    ),
    Question(
        number=22,
        question="Sigbovik or ACM TOSC?",
        question_type=QuestionType.THIS_OR_THAT.value,
        choices="Sigbovik, ACM TOSC",
        answer="Sigbovik",
        weight=0.4,
        time=15,
    ),
    Question(
        number=23,
        question="Sigbovik or ACM TOSC?",
        question_type=QuestionType.THIS_OR_THAT.value,
        choices="Sigbovik, ACM TOSC",
        answer="Sigbovik",
        weight=0.4,
        time=15,
    ),
    Question(
        number=24,
        question="Sigbovik or ACM TOSC?",
        question_type=QuestionType.THIS_OR_THAT.value,
        choices="Sigbovik, ACM TOSC",
        answer="ACM TOSC",
        weight=0.4,
        time=15,
    ),
    Question(
        number=25,
        question="Sigbovik or ACM TOSC?",
        question_type=QuestionType.THIS_OR_THAT.value,
        choices="Sigbovik, ACM TOSC",
        answer="Sigbovik",
        weight=0.4,
        time=15,
    ),
    Question(
        number=26,
        question="Sigbovik or ACM TOSC?",
        question_type=QuestionType.THIS_OR_THAT.value,
        choices="Sigbovik, ACM TOSC",
        answer="ACM TOSC",
        weight=0.4,
        time=15,
    ),
    Question(
        number=27,
        question="How long was the longest Ping Pong Rally of all time (in hours)?",
        question_type=QuestionType.NUMBERS.value,
        answer="13.6",
    ),
    Question(
        number=28,
        question="Who is the main character of Super Mario Bros 2?",
        question_type=QuestionType.SHORT_ANSWER.value,
        answer="Mario",
    ),
    Question(
        number=29,
        question="How well do you know the imperial system?",
        question_type=QuestionType.NUMBERS.value,
        answer="8",
        weight=0.4,
        time=15,
    ),
    Question(
        number=30,
        question="How well do you know the imperial system?",
        question_type=QuestionType.NUMBERS.value,
        answer="3",
        weight=0.4,
        time=15,
    ),
    Question(
        number=31,
        question="How well do you know the imperial system?",
        question_type=QuestionType.NUMBERS.value,
        answer="1760",
        weight=0.4,
        time=15,
    ),
    Question(
        number=32,
        question="How well do you know the imperial system?",
        question_type=QuestionType.NUMBERS.value,
        answer="4",
        weight=0.4,
        time=15,
    ),
    Question(
        number=33,
        question="How well do you know the imperial system?",
        question_type=QuestionType.NUMBERS.value,
        answer="14.2",
        weight=0.4,
        time=15,
    ),
    Question(
        number=34,
        question="How many words are in the title of “Zedler’s Encyclopedia” (considered the most important German encyclopedia of the 18th century)?",
        question_type=QuestionType.NUMBERS.value,
        answer="110",
    ),
    Question(
        number=35,
        question="How many times has the Gävle Goat been destroyed?",
        question_type=QuestionType.MULTIPLE_CHOICE.value,
        choices="A. 42/59,B. 35/59,C. 12/59,D. 60/59",
        answer="A. 42/59",
        weight=-2,
    ),
    Question(
        number=36,
        question="How many swear words off was South Park: Bigger, Longer, Uncut from being automatically rated NC-17 (400 swear words is the limit)?",
        question_type=QuestionType.NUMBERS.value,
        answer="1",
        weight=-2,
    ),
    Question(
        number=37,
        question="Which of these near death experiences did Frane Selak reportedly NOT have?",
        question_type=QuestionType.MULTIPLE_CHOICE.value,
        choices="A. Train derailing,B. Electrocution,C. Car accident,D. Fuel tank combusion",
        answer="B. Electrocution",
        weight=-2,
    ),
    Question(
        number=38,
        question="How many times has Roy Sullivan been struck by lightning?",
        question_type=QuestionType.NUMBERS.value,
        answer="7",
        weight=-2,
    ),
    Question(
        number=39,
        question="What color is spider blood?",
        question_type=QuestionType.MULTIPLE_CHOICE.value,
        choices="A. Red,B. Yellow,C. Blue,D. Clear",
        answer="D. Clear",
        weight=-2,
    ),
    Question(
        number=40,
        question="Which letter does not exist in the greek alphabet?",
        question_type=QuestionType.MULTIPLE_CHOICE.value,
        choices="A. B,B. Δ,C. A,D. C",
        answer="D. C",
        weight=-2,
    ),
]


def create_questions():
    for question in questions:
        sqlalchemy_db.session.add(question)
    sqlalchemy_db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        create_questions()
