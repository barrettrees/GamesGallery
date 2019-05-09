
# convertSheets.py
# author: Melanie Dickinson
# April 2019
# Python 2.7

# Given two CSV files, games.csv and authors.csv, generated from Google Sheets, 
# (1) 	Create a Javascript file with a 'games' variable for info about each game on the website,
# 		and an 'authors' variable for info about each author, and
# (2)	Create a new html page in this directory, for each game, called gamename.html

import csv

games_csv = open('games.csv', 'r')
authors_csv = open('authors.csv', 'r')
jsfile = open('data.js', 'w')

# Column names in each of the CSV files
# Last 3 columns named in this list aren't used; they're just for humans to make notes to themselves while compiling the games
gamefields = ("name", "platform", "author1", "author2", "author3", "dir", "description", "showSourceDownload", "haveGame", "todo", "notes") 
# Last column isn't used
authorfields = ("name", "website", "itch", "twitter", "instagram", "linkedin", "email", "youtube", "notes")


def writeGameHTML (game) : 

	try: 
		# File exists
		htmlfile = open( game['dir'] + '/index.html', 'w')
    	
	except IOError:
    	# File doesn't exist yet
		htmlfile = open( game['dir'] + '/index.html', 'w+')

	html = """
	<!DOCTYPE html>
	<html lang="en">
	
	  <head>
	    <meta charset="utf-8">
	    <meta http-equiv="X-UA-Compatible" content="IE=edge">
	    <!-- Helps scale the page better on smaller screens-->
	    <meta name="viewport" content="width=device-width, initial-scale=1">
	    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
	    <meta name="description" content="Info page for a game created in CMPM 80K at UCSC">
	    <meta name="author" content="Melanie Dickinson">
	
	    <link rel="icon" href="../icons/favicon.ico" sizes="16x16">
	
	    <!-- Fonts -->
        <link rel='stylesheet' type='text/css' href="https://fonts.googleapis.com/css?family=Wire+One">
	    <link rel='stylesheet' type='text/css' href='https://fonts.googleapis.com/css?family=Abel'>
	    <link rel='stylesheet' type='text/css' href="https://fonts.googleapis.com/css?family=Barlow+Condensed:300">
	    <link rel='stylesheet' type='text/css' href="https://fonts.googleapis.com/css?family=News+Cycle">
	  
	    <!-- CSS -->
	    <link rel="stylesheet" href="../style.css">
	    <link rel="stylesheet" href="../style-gamepage.css">
	
	    <!-- Libraries --> 
	    <script type="text/javascript" src="../lib/jquery-3.0.0.min.js"></script>
	    <script type="text/javascript" src="../lib/loki.js"></script>
	
	    <!-- JS -->
	    <script type="text/javascript" src="../data.js"></script>
	    <script type="text/javascript" src="../DataWrangler.js"></script>
	    <script type="text/javascript" src="../gamepage.js"></script>

	  </head>
	
	  <body onload="makeGamePage('""" + game['name'] + """')">
	
	    <div class="game-info">
	        
	        <img src="screenshot.png" class="game-img">
	
	        <h1 class="game-title"></h1>
	
	        <a class="button play" href="play.html" target="_blank">PLAY &#8250;</a>
	        <a download href='""" + game['dir'] + """.c3p' class="button download">Download Source (.c3p)</a> 
	
	        <div class="byline"></div>

	        <div id="game-description"></div>
	
	        <a href="../index.html" class="back">&#8249; Back</a>
	
	      </div>
	  </body>
	
	</html>
	"""
	htmlfile.write(html)

def makeAuthorsString (row) :
	
	# There's always at least one author
	return		( '"' + row["author1"] + '"' 
				+ ( ', "' + row["author2"] + '"' if row["author2"] != "" else "" )
				+ ( ', "' + row["author3"] + '"' if row["author3"] != "" else "" ))


# Write one row from the csv to the js file as a JSON object {}
# Without terminating comma to separate the next object
def writeOneGame (row) :

	jsfile.write('{\n\t\t') # Start this game's info with a '{', a newline, and two tabs before the first key-value pair

	# Construct a list of strings, where each string is a key-value pair in JSON format

	# Add the string values of the row: game name, platform, image filename, 
		# followed by the author array,
		# followed by the true/false values: showSourceDownload
	gameinfo = ( 'name : "' 				+ row['name'] + '"',
				 'platform : "' 			+ row['platform'] + '"',
				 'dir : "' 					+ row['dir'] + '"',
				 'authors : [ '				+ makeAuthorsString(row) + ' ]',
				 'showSourceDownload : ' 	+ ( 'true' if row['showSourceDownload'] == 'yes' else 'false' ), # no quotes around value
				 'description : "'			+ row['description'] + '"'
				)

	# Concatenate those strings with commas and newlines between them for pretty JSON file writing
	gameinfo = ",\n\t\t".join(gameinfo)

	jsfile.write (gameinfo)

	jsfile.write("\n\t}") # no comma, newline, closing bracket

	if row['dir'] :
		writeGameHTML (row)


def writeGames ():
	reader = csv.DictReader (games_csv, gamefields)
	
	# Start writing the games array of objects in data.js
	jsfile.write('var games = [ \n\t')
	
	# Skip the first line of csv (the header) -- use 'row' (previous row) instead of '_row' in loop
	next(reader)
	row = next(reader)
	
	# For each row in the csv, create a new JSON object 
	for _row in reader:
		
		writeOneGame (row)
		jsfile.write(',')
	
		row = _row
	
	# Things to do to the last item in reader (last row of csv)
	writeOneGame (row)
	# no comma
	
	jsfile.write('\n];\n\n')


# Write one row from the csv to the js file as a JSON object {}
# Without terminating comma to separate the next object
def writeOneAuthor (row) :

	jsfile.write('{') # Open this author's JSON object

	# Construct a string by concatenation, where each concatenation is a key-value pair in JSON format

	# Add the string values of the row: game name, platform, image filename, 
		# followed by the author array,
		# followed by the true/false values: showSourceDownload
	authorinfo = '\n\t\tname : "' + row['name'] + '"'
	authorinfo += ( ',\n\t\twebsite : "' + row["website"] + '"' if row["website"] else "" ) 
	authorinfo += ( ',\n\t\titch : "' + row["itch"] + '"' 		if row["itch"] else "" ) 
	authorinfo += ( ',\n\t\ttwitter : "' + row["twitter"] + '"' if row["twitter"] else "" ) 
	authorinfo += ( ',\n\t\tinstagram : "' + row["instagram"] + '"' if row["instagram"] else "" ) 
	authorinfo += ( ',\n\t\tlinkedin : "' + row["linkedin"] + '"' if row["linkedin"] else "" ) 
	authorinfo += ( ',\n\t\tyoutube : "' + row["youtube"] + '"' if row["youtube"] else "" ) 
	authorinfo += ( ',\n\t\temail : "' + row["email"] + '"' if row["email"] else "" ) 

	# Concatenate those strings with commas and newlines between them for pretty JSON file writing

	jsfile.write (authorinfo)

	jsfile.write("\n\t}") # no comma, newline, closing bracket


def writeAuthors ():
	reader = csv.DictReader (authors_csv, authorfields)
	
	# Start writing the authors array of objects in the data javascript file
	jsfile.write('var authors = [ \n\t')
	
	# Skip the first line of csv (the header) -- use 'row' (previous row) instead of '_row' in loop
	next(reader)
	row = next(reader)
	
	# For each row in the csv, create a new JSON object 
	for _row in reader:
		
		writeOneAuthor (row)
		jsfile.write(',') # add commas after each csv row except the last
	
		row = _row
	
	# Things to do to the last item in reader (last row of csv)
	writeOneAuthor (row)
	# no comma
	
	jsfile.write('\n];')


### Start ###

jsfile.write('\n')
writeGames()
writeAuthors()
jsfile.write('\n')


