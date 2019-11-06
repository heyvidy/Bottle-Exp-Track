# runserver.py
from bottle import get, run, jinja2_view, post, request, redirect
from models import User, Expense, db

db.connect()

@get("/")
@jinja2_view("home.html")
def home():
	return

@post("/signup")
def signup():
	username = request.forms.get('username')
	password = request.forms.get('password')

	users = User.select().where(User.username == username)

	if len(users) != 0:
		return "User already exists!"
	else:
		User.create(username=username, password=password)
	return redirect("/")


run(host="localhost", 
	port="8080", 
	debug=True)

# open localhost:8080 in the browser
