# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect

# -- Initialization section --
app = Flask(__name__)


# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

# The API route is what the client will contact to get its matches
@app.route('/api')
def api():
	# Request arguments, like players, are used by accessing:
	# www.example.com/api?players=X&time=X&age=X&difficulty=X&popularity=X
	# Note: there is currently no handling for URLs which do not
	# provide all of the arguments we are using
	players = request.args['players']
	time = request.args['time'] # in minutes
	age = request.args['age'] # player age in years
	difficulty = request.args['difficulty'] # from 1-5
	popularity = request.args['popularity'] # from 1-100,
			# 1 being most; corresponds to rank
	return "API OK for [players, time, age, difficulty, popularity] as [" + players + ", " + time + ", " + age + ", " + difficulty + ", " + popularity + "]"
