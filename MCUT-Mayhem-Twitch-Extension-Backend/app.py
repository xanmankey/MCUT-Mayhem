from gevent import monkey

monkey.patch_all()

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
    jsonify,
    Response,
)
import sqlite3
from dotenv import load_dotenv
from flask_cors import CORS
from models import sqlalchemy_db
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import random
from utils import Base, QuestionType
from flask_socketio import SocketIO, emit

# This will be running on Purdue Hackers Vulcan

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
CORS(app)

DB_PATH = "data.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"

# socketio = SocketIO(
#     app, async_mode="gevent", cors_allowed_origins="*", message_queue="redis://"
# )
# Hopefully don't need to run multiple workers/share state; I hope async mode with gevent will be enough
socketio = SocketIO(
    app,
    async_mode="gevent",
    cors_allowed_origins="*",
    ssl_context=("localhost.pem", "localhost-key.pem"),
)
sqlalchemy_db.init_app(app)

from models.questions import Question
from models.players import Player

with app.app_context():
    # Configure the sqlite3 db
    sqlalchemy_db.create_all()

# In theory, the figma REST API allows me to interface with slides
# Figma also supports SLIDE COMPONENTS; so what I can do is programmatically generate my presentations
# The problem is what if I want to add a new slide? Position?
# What about editing slides? I would need the db to be synced...

# I could run flask admin, so it can all be created through there, and it can take in images as well...
# Then Manoli's interface will just pull from the question db, which will correlate with the slides and he can just trigger a question, which will mark it as asked
# So when Manoli starts a question on the frontend, that will set the current question number, which will then propagate out to the viewers
# Then when the question is answered, the player's scores will be updated AUTOMATICALLY

# How does the escape room portion fit in? I have a deadline and other things to do, I can't take infinite time on this
# We could build it into the theming; Manoli can ONLY ask questions and edit scores, so it could be that each time something is figured out, a trivia question is unlocked,
# and the amount of points that people get is the corresponding combination
# The trivia questions will be labelled

# How would doing a challenge correspond to unlocking a trivia question though?
# Dhruv will just have the bounties for completion on him

# We don't need answer slides; instead, the graphs should clearly show the correct answer

# What if someone is doing a challenge and then someone unlocks a trivia question? Since it's 2 laptops, Manoli can just run the trivia question

# Manoli will also have the ability to access all of the player's scores and edit them as he sees fit

# For escape room, either manoli can just select the corresponding questions slide or we can make it that when manoli clicks the question it jumps to the slide

# At the end, we'll 0 out the top 3 players scores, and they'll answer trivia questions from the audience, each ? being worth 1 point
# Each person will get a shot at each question; the questions WON'T be verified ahead of time but they do have to be objective
# We'll run that for 10 min

# =============== Routes ===============


# Create player
@app.route("/create_player", methods=["POST"])
def create_player():
    username = request.form.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400

    player = Player(username=username)
    sqlalchemy_db.session.add(player)
    sqlalchemy_db.session.commit()

    return jsonify({"message": "User created successfully"}), 200


# Update player score
@app.route("/update_score", methods=["POST"])
def update_score():
    username = request.form.get("username")
    score = request.form.get("score")

    if not username or not score:
        return jsonify({"error": "Username and score are required"}), 400

    player = sqlalchemy_db.session.query(Player).filter_by(username=username).first()
    if not player:
        return jsonify({"error": "Player not found"}), 404

    player.score = score
    sqlalchemy_db.session.commit()

    return jsonify({"message": "Score updated successfully"}), 200


# Retrieve player response
@app.route("/response", methods=["POST"])
def response():
    username = request.form.get("username")
    response = request.form.get("response")
    print(username, response)

    if not username or not response:
        return jsonify({"error": "Username and response are required"}), 400

    player = sqlalchemy_db.session.query(Player).filter_by(username=username).first()
    if not player:
        return jsonify({"error": "Player not found"}), 404

    player.response = response
    sqlalchemy_db.session.commit()

    print("Response updated successfully")
    return jsonify({"message": "Response updated successfully"}), 200


# Get leaderboard
@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    players = sqlalchemy_db.session.query(Player).order_by(Player.score.desc()).all()
    leaderboard_data = [
        {"username": player.username, "score": player.score} for player in players
    ]
    return jsonify({"leaderboard": leaderboard_data})


# Streamer propagates question to viewers
@socketio.on("start_question")
def start_question(question):
    if not question:
        return jsonify({"error": "Question not found"}), 404

    # Viewer clients will listen for this event and display the question whenever it is emitted
    socketio.emit("new_question", {"question": question})


@socketio.on("end_question")
def end_question(data):
    print("beginning end question")
    question = (
        sqlalchemy_db.session.query(Question)
        .filter_by(number=data.get("question_number"))
        .first()
    )
    if not question:
        print("question not found; error")
        return jsonify({"error": "Question not found"}), 404

    question.asked = True

    # Retrieve player responses
    print("retrieving player responses")
    player_responses = retrieve_player_responses()

    # Update player scores
    answers = question.answer.split(",")
    print(player_responses)
    player_obj = None
    for player, response in player_responses.items():
        answered = False
        for answer in answers:
            if (
                question.question_type == QuestionType.MULTIPLE_CHOICE.value
                or question.question_type == QuestionType.THIS_OR_THAT.value
            ):
                # Response has to match exactly to score points
                if answer == response:
                    print("Multiple choice points scored")
                    player_obj = (
                        sqlalchemy_db.session.query(Player)
                        .filter_by(username=player)
                        .first()
                    )
                    player_obj.score += 10 * abs(question.weight)
                    sqlalchemy_db.session.commit()
                    if question.weight < 0:
                        answered = True
                    break
            elif question.question_type == QuestionType.NUMBERS.value:
                # Response has to be within a range to score points
                try:
                    try:
                        answer = int(answer)
                        response = int(response)
                        difference = abs(answer - response)
                        if difference == 0:
                            print("Exact number points scored")
                            player_obj = (
                                sqlalchemy_db.session.query(Player)
                                .filter_by(username=player)
                                .first()
                            )
                            player_obj.score += 20 * abs(question.weight)
                            sqlalchemy_db.session.commit()
                            if question.weight < 0:
                                answered = True
                            break
                        else:
                            print("Numbers points scored")
                            player_obj = (
                                sqlalchemy_db.session.query(Player)
                                .filter_by(username=player)
                                .first()
                            )
                            player_obj.score += max(
                                0,
                                int(
                                    (1 - difference / answer)
                                    * 15
                                    * abs(question.weight)
                                ),
                            )
                            sqlalchemy_db.session.commit()
                            if question.weight < 0:
                                answered = True
                            break
                    except ValueError:
                        continue
                except ValueError:
                    continue
            elif question.question_type == QuestionType.SHORT_ANSWER.value:
                if answer in response or response in answer:
                    print("Short answer points scored")
                    player_obj = (
                        sqlalchemy_db.session.query(Player)
                        .filter_by(username=player)
                        .first()
                    )
                    player_obj.score += 10 * abs(question.weight)
                    sqlalchemy_db.session.commit()
                    if question.weight < 0:
                        answered = True
                    break
        if not answered and question.weight == 0:
            player_obj = (
                sqlalchemy_db.session.query(Player).filter_by(username=player).first()
            )
            player_obj.score -= 5 * question.weight
            sqlalchemy_db.session.commit()

    # Update responses
    player_responses = retrieve_player_responses().copy()
    print(player_responses)
    # Reset players response (empty)
    for player, response in player_responses.items():
        player_obj = (
            sqlalchemy_db.session.query(Player).filter_by(username=player).first()
        )
        if player_obj != None:
            player_obj.response = ""
            sqlalchemy_db.session.commit()
    socketio.emit(
        "results",
        {
            "responses": player_responses,
            "question": question.question,
            "answer": question.answer,
            "question_type": question.question_type,
        },
    )


# End question; called when frontend timer expires
# @app.route("/end_question", methods=["GET"])
# def end_question():
#     question = (
#         sqlalchemy_db.session.query(Question)
#         .filter_by(number=request.args.get("question_number"))
#         .first()
#     )
#     if not question:
#         return jsonify({"error": "Question not found"}), 404

#     question.asked = True
#     sqlalchemy_db.session.commit()

#     # Retrieve player responses
#     player_responses = retrieve_player_responses()

#     # Update player scores
#     answers = question.answer.split(",")
#     for player, response in player_responses.items():
#         for answer in answers:
#             if answer in response:
#                 player_obj = (
#                     sqlalchemy_db.session.query(Player)
#                     .filter_by(username=player)
#                     .first()
#                 )
#                 player_obj.score += 1 * question.weight
#                 break

#     return jsonify(
#         {
#             "responses": player_responses,
#             "question": question.question,
#             "question_type": question.question_type,
#         }
#     )


@app.route("/get_questions", methods=["GET"])
def get_questions():
    questions = sqlalchemy_db.session.query(Question).filter_by(asked=False).all()
    question_data = [
        {
            "number": question.number,
            "question": question.question,
            "question_type": question.question_type,
            "time": question.time,
            "choices": question.choices,
            "answer": question.answer,
            "weight": question.weight,
            "asked": question.asked,
        }
        for question in questions
    ]
    return jsonify({"questions": question_data})


def retrieve_player_responses():
    players = sqlalchemy_db.session.query(Player).filter(Player.response != "").all()
    player_responses = {player.username: player.response for player in players}
    return player_responses


# TODO: need to make this call create player
@socketio.on("connect")
def handle_connect():
    # connected_clients.add(request.sid)
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    # connected_clients.remove(request.sid)
    print("Client disconnected")


if __name__ == "__main__":
    FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    FLASK_PORT = os.getenv("FLASK_PORT", "8080")
    socketio.run(app, debug=True, host=FLASK_HOST, port=FLASK_PORT)
