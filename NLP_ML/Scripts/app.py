from flask import Flask 



app = Flask(__name__)
''' start coding for here'''

app.route('/login')
def login():
	return "hello"

if __name__ == '__main__':
    app.run(debug = True)