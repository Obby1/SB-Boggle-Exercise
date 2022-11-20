from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "fdfgkjtjkkg45yfdb"

boggle_game = Boggle()


@app.route("/")
def homepage():
    """Show board."""

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    return render_template("index.html", board=board,
                           highscore=highscore,
                           nplays=nplays)


@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

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

# Old Code Below for posterity 
# notes on possible errors:
# instance error? When adding OO in JS file things working well
# linking to wrong sheets? syntax in code?
# 

# @app.route("/")
# def homepage():
#     """Show board."""

#     board = boggle_game.make_board()
#     session['board'] = board
#     highscore = session.get("highscore", 0)
#     nplays = session.get("nplays", 0)

#     return render_template("home.html", board=board, highscore=highscore,nplays=nplays)


# @app.route("/check-word")
# def check_word():
#     """Check if word is in dictionary."""

#     word = request.args["word"]
#     board = session["board"]
#     response = boggle_game.check_valid_word(board, word)

#     return jsonify({'result': response})


# @app.route("/post-score", methods=["POST"])
# def post_score():
#     """Receive score, update nplays, update high score if appropriate."""

#     score = request.json["score"]
#     highscore = session.get("highscore", 0)
#     nplays = session.get("nplays", 0)

#     session['nplays'] = nplays + 1
#     session['highscore'] = max(score, highscore)

#     return jsonify(brokeRecord=score > highscore)







# from flask import Flask, request, render_template, flash, jsonify, session
# # from flask_debugtoolbar import DebugToolbarExtension
# from boggle import Boggle


# # make a session for each player?

# app = Flask(__name__)
# app.config['SECRET_KEY'] = "chickenzarecool21837"
# # app.debug = True
# # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# boggle_game = Boggle()

# # toolbar = DebugToolbarExtension(app)


# @app.route('/')
# def index():
#     """Show homepage."""
    
#     session["board"] = boggle_game.make_board()
#     boggle = session["board"]
#     return render_template("home.html", boggle=boggle)


# # Flask defaults to get for the views if no methods posted
# @app.route("/check-word", methods = ['POST', 'GET'])
# def check_word():
#     """Check if word is in dictionary."""
#     flash('just testing')
#     word = request.args["word"]
#     board = session["board"]
#     response = boggle_game.check_valid_word(board, word)

#     return jsonify({'result': response})


# # this route is not posting yet, flash is not showing up
# # error message - POST method not allowed 

# # @app.route("/check-word", methods = ['POST', 'GET'])
# # @app.route("/check-word")
# # def check_word():
# #     """Check if word is in dictionary."""
# #     # flash('just testing')
# #     word = request.args["guess"]
# #     board = session["game_board"]
# #     # flash('just testing2')
# #     response = boggle_game.check_valid_word(board, word)
# #     return jsonify({'result': response})


# # @app.route('/guess', methods=["POST"])
# # def make_guess():
# #     flash('made guess')
# #     return redirect('/')

# # @app.route('/fav-color', methods=['POST'])
# # def fav_color():
# #     """Show favorite color."""

# #     fav_color = request.form.get('color')

# #     return render_template("color.html", fav_color=fav_color)

# # @app.route('/')
# # def index():
# #     """Show homepage."""
# #     boggle = boggle_game
# #     return render_template("home.html", boggle=boggle)

# # # this route is not posting yet, flash is not showing up
# # # error message - POST method not allowed 
# # # below route is posting but board dissapears. Maybe better to put guess in query
# # # string, use string to check data in db, and return 

# # @app.route("/check-word", methods=["POST"])
# # def check_word():
# #     """Check if word is in dictionary."""
# #     flash('just testing')
# #     word = request.form["guess"]
# #     board = session["game_board"]
# #     response = boggle_game.check_valid_word(board, word)

# #     msg =  jsonify({'result': response})
# #     flash(msg)
# #     return render_template("home.html")