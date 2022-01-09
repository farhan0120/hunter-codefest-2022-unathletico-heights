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
	# Request arguments, like id, are used by accessing:
	# www.example.com/api?id=X&num=Y
	# There is currently no handling for URLs which do not
	# provide all of the arguments we are using
	id = request.args['id']
	num = request.args['num']
	return "API Ok for id " + id + " and num " + num
