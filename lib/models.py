from google.appengine.ext import db

class Food(db.Model):
	name = db.StringProperty(multiline=True)
	date = db.DateTimeProperty(auto_now_add=True)
	filename = db.StringProperty()
	location = db.StringProperty()
	images = db.StringListProperty()
	info = db.StringListProperty()
	flavors = db.TextProperty()
	
def food_key(food_name=None):
	return db.Key.from_path('Food', food_name or 'default_food')