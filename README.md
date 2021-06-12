# Detecting-Key-Needs-in-Crisis
NLP - Machine Leaning - Twitter API -Flask Webapp

Requirements:

Python Flask-
It is a web development framework used to create different routes for the web application.
	-- installation command : pip install Flask

Python Websocket-
It enables bi-directional communication from server to client and vice versa via websockets.
	-- installation command : pip install flask-socketio
Gevent
		pip install gevent
	
Tweepy-
It is a Python library for accessing the Twitter API.
	-- installation command : pip install tweepy
	
Files:

	app.py -
	
	This the main web backend containing different routes and what needs to be displayed for each route.
	Also the websocket routes are maintained in this file to respond to them with respective responses.
	It imports the ML model to classify the tweets
	
Folders:
	
	data - 
	This folder is used to store the generated excel file containing tweets.
	
	models-
	This folder is used to store the ML models.
	
	static-
	This folder as per the requirements of Flask framework stores static files like CSS, Javascript.
	
	templates-
	This folder as per the requirements of Flask framework is used to store HTML files for different routes.
	
Run command:

	Run the app.py from the terminal (for eg. CMD for windows)using following command-
		python app.py
		
	Open the location in a browser which is mentioned in the terminal.
Steps:

	1. On the home page there is a input bar for hashtag. Enter the hashtag in that input bar.
	2. Click on the search button to start real time analysis.
	3. The dashboard page open ups with real-time tweets slider and count of tweets under different classes.
	4. There are 2 buttons on dashoboard page viz., i) Download ii) Stop.
		i) Download button : click this to download the excel files of different classes containing tweets until that instant.
		ii) Stop button : click this to stop real-time tweet analysis and downlod the remaining classified tweets. 
