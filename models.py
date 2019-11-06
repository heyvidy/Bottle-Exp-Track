from peewee import *

db = SqliteDatabase("exptrack.db")

class User(Model):
	username = CharField()
	password = CharField()

	class Meta:
		database = db

class Expense(Model):
	user = ForeignKeyField(User)
	amount = FloatField()
	reason = CharField()
	timestamp = DateTimeField()

	class Meta:
		database = db

if __name__ == '__main__': 
	db.connect()
	db.create_tables([User, Expense])
