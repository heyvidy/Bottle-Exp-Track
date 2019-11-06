# runserver.py
from bottle import get, run, jinja2_view, post, request, redirect, response
from models import User, Expense, db
from datetime import datetime

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

@post("/login")
def login():
	username = request.forms.get('username')
	password = request.forms.get('password')

	try:
		user = User.get(User.username == username)
	except:
		return "User does not exist!"

	if user.password == password:
		response.set_cookie("user_id", str(user.id))
		return redirect("/dashboard")
	else:
		return "Invalid Credentials!!"


@get("/dashboard")
@jinja2_view("dashboard.html")
def dashboard():
	uid = request.get_cookie("user_id")
	user = User.get(User.id == uid)
	
	expenses = Expense.select().where(Expense.user == user)
	return {"username" : user.username, "allexpenses": expenses}


@post("/addexpense")
def add_expense():
	uid = request.get_cookie("user_id")
	user = User.get(User.id == uid)
	reason = request.forms.get("reason")
	amount = request.forms.get("amount")
	timestamp = datetime.now()

	Expense.create(user=user, reason=reason, amount=amount, timestamp=timestamp)
	return redirect("/dashboard")


@get("/delete/<expense_id>")
def delete_expense(expense_id):
	expense = Expense.get(Expense.id == expense_id)
	uid = request.get_cookie("user_id")
	user = User.get(User.id == uid)

	if expense.user == user:
		expense.delete_instance()
		return redirect("/dashboard")
	else:
		return "Operation Not Permitted!<br><a href='/dashboard'>Go to Dashbaord</a>"


@get("/edit/<expense_id>")
@jinja2_view("edit_expense.html")
def edit_expense(expense_id):
	expense = Expense.get(Expense.id == expense_id)
	uid = request.get_cookie("user_id")
	user = User.get(User.id == uid)

	if expense.user == user:
		return {"expense" : expense}
	else:
		return redirect("/dashbaord")


@post("/edit/<expense_id>")
def handle_edit_expense(expense_id):
	expense = Expense.get(Expense.id == expense_id)
	uid = request.get_cookie("user_id")
	user = User.get(User.id == uid)

	if expense.user == user:
		reason = request.forms.get("reason")
		amount = request.forms.get("amount")
		expense.reason = reason
		expense.amount = amount
		expense.save()
	
	return redirect("/dashboard")

run(host="localhost", 
	port="8080", 
	debug=True)

# open localhost:8080 in the browser
