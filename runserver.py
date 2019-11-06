# runserver.py
from bottle import get, run, jinja2_view

@get("/")
@jinja2_view("home.html")
def home():
	return

run(host="localhost", 
	port="8080", 
	debug=True)

# open localhost:8080 in the browser
