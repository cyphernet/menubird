from google.appengine.ext import db

class Food(db.Model):
	name = db.StringProperty(multiline=True)
	date = db.DateTimeProperty(auto_now_add=True)
	title = db.StringProperty()
	read_path = db.StringProperty()
	write_path = db.TextProperty()
	finalized = db.BooleanProperty()

def food_key(food_name=None):
	return db.Key.from_path('Food', food_name or 'default_food')