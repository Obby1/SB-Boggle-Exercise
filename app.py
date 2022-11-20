from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "fdfgkjtjkkg45yfdb"

boggle_game = Boggle()

# 
@app.route("/")
def homepage():
    """Show board."""
    # make boggle board
    board = boggle_game.make_board()
    # save board list to session
    session['board'] = board
    # retrieve high score from session or set to 0
    highscore = session.get("highscore", 0)
    # retrieve numberes of plays from session or set to 0
    nplays = session.get("nplays", 0)

    return render_template("index.html", board=board,
                           highscore=highscore,
                           nplays=nplays)


@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""
    # set word to word from query string
    word = request.args["word"]
    # set board to board variable from session
    board = session["board"]
    # check if valid word using check_valid_word method
    response = boggle_game.check_valid_word(board, word)
    # return string as JSON - Ask krunal to help explain format to you, why do we JSONIFY it?
    # is jsonify the most efficient way to communicate from web browser to server?
    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
