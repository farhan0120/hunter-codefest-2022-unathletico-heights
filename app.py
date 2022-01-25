# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from googleImageAPI import *
import csv # for /api endpoint


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
	## Set up arguments
	# Request arguments, like players, are used by accessing:
	# www.example.com/api?playersmin=X&playersmax=X&time=X&age=X&difficulty=X&popularity=X&result=X
	# Note: there is currently no handling for URLs which do not
	# provide all of the arguments we are using
	# Definition : 	a strong argument is one that MUST be met in all results
	# 		a weak argument is one that we want to be as close as we can to
	if request.method == 'GET':
        return redirect(url_for("index"))

    else:
		form = request.form
		playersmin = int(form["min_players"])
		playersmax = int(form["max_player"])
		time = int(form["time"])
		age = int(form["age"])
		difficulty = form["difficulty"]
		popularity = form["popularity"]

		#playersmin = int(request.args['playersmin'])
		#playersmax = int(request.args['playersmax'])
		#time = int(request.args['time']) # in minutes
		#age = int(request.args['age']) # player age in years
		#difficulty = float(request.args['difficulty']) # from 0-1
		#popularity = float(request.args['popularity']) # from 0-1,
				# 0 being most; corresponds to rank
		result = int(request.args['result']) - 1 # which result, starts at 1;
				# present user with result=1, then if they decline, result=2, etc;
				# we subtract it from 1 here to compensate for 0-indexing

		## Set up CSV
		header = []
		rows = []
		with open('database.csv', newline='') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			header = next(csvreader)
			for row in csvreader:
				rows.append(row)

		## Start eliminating
		# By minutes (strong)
		toRemove = []
		for game in rows:
			minutesarray = game[2].split() # split "20 40 Min"
			if "Time:" not in minutesarray: # this means there is no time
				minutesarray.remove("Min")
				if len(minutesarray) == 1 and time != int(minutesarray[0]):
					toRemove.append(game)
				elif len(minutesarray) == 2 and (time < int(minutesarray[0]) or time > int(minutesarray[1])):
					toRemove.append(game)
			else:
				toRemove.append(game) # remove even if no time given, as we can't know if it matches user's request	
		for game in toRemove:
			rows.remove(game)
		
		# By players (strong)
		toRemove = []
		for game in rows:
			playersarray = game[1].split() # split "2 4 Players"
			playersarray.remove("Players")
			if len(playersarray) == 1 and (playersmin != int(playersarray[0]) or playersmax != int(playersarray[0])):
				toRemove.append(game)
			elif len(playersarray) == 2 and (playersmax < int(playersarray[0]) or playersmin > int(playersarray[1])):
				toRemove.append(game)
		for game in toRemove:
			rows.remove(game)

		# By age (strong)
		toRemove = []
		for game in rows:
			agearray = game[3].split("Age: ")[1][0:-1] # extract number
			if (agearray != ' ' and int(agearray) > age): # if age is nonempty and greater than given value
				toRemove.append(game)
		for game in toRemove:
			rows.remove(game)

		# By difficulty and popularity (weak)
		distancearray = []
		for game in rows:
			difficultyarray = game[4].split('/')
			gamediff = float(difficultyarray[0].replace(',', '')) / float(difficultyarray[1].replace(',', ''))
			popularityarray = game[5].split('/')
			gamepop = float(popularityarray[0].replace(',', '')) / float(popularityarray[1].replace(',', ''))
			distancearray.append(pow((difficulty - gamediff) + (popularity - gamepop), 2))
		
		# Sort weak results
		resultarray = [x for y, x in sorted(zip(distancearray, rows))]
			# zips together the two arrays (combines them)
			# sorts them (by the combined distance array)
			# and removes the distance values after sorting

		name = resultarray[result][0]
		players = resultarray[result][1]
		time = resultarray[result][2]
		age = resultarray[result][3]
		difficulty = resultarray[result][4]
		rank = resultarray[result][5]
		description = resultarray[result][6]
		image = getImageLink(name + " board game")
		# Return result
		if len(resultarray) > result: # if result exists
			return render_template("api.html", status="OK", name=name, players=players, time=time, age=age, difficulty=difficulty, rank=rank, description=description, image=image)
			output = ">>>>>".join(resultarray[result])
		else:
			return render_template("api.html", status="ERROR")
