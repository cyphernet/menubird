from google.appengine.ext import db

class Food(db.Model):
	name = db.StringProperty(multiline=True)
	date = db.DateTimeProperty(auto_now_add=True)
	filename = db.StringProperty()
	location = db.StringProperty()

def food_key(food_name=None):
	return db.Key.from_path('Food', food_name or 'default_food')
	
class Food_image(db.Model):
	name = db.StringProperty(multiline=True)
	date = db.DateTimeProperty(auto_now_add=True)
	food = db.ReferenceProperty(Food)
	url = db.StringProperty()

def food_image_key(food_image_name=None):
	return db.Key.from_path('Food_image', food_image_name or 'default_food_images')	