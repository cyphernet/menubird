import webapp2
import jinja2
import os

from google.appengine.api import conversion
from google.appengine.ext import db

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Food(db.Model):
  name = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)

def food_key(food_name=None):
	return db.Key.from_path('Food', food_name or 'default_food')

class MainPage(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		template = jinja_environment.get_template('index.html')
		output = template.render(template_values)
		self.response.out.write(output)


class Ocr(webapp2.RequestHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'text/plain'

      # Create a conversion request from HTML to PNG.
		asset = conversion.Asset("image/png", self.request.get("img"), "image.PNG")
		conversion_obj = conversion.Conversion(asset, "text/plain", 1, 1, 1, "en-US")

		result = conversion.convert(conversion_obj)
		if result.assets:
		  # Note: in most cases, we will return data all in one asset.
		  # Except that we return multiple assets for multiple pages image.
		  for asset in result.assets:
			ocr_text = asset.data
		  	food_name = unicode(ocr_text, 'utf-8').lower()
			
			food = Food()
			food.name = food_name
			food.put()

			self.response.out.write(ocr_text)

		else:
		  handleError(result.error_code, result.error_text)

class Apptest(webapp2.RequestHandler):
    def get(self):
		self.response.out.write("""
			<html>
				<body>
		          <form action="/app" enctype="multipart/form-data" method="post">
		            <div><input type="file" name="img"/></div>
		            <div><input type="submit" value="test" /></div>
		          </form>
		        </body>
		      </html>""")

app = webapp2.WSGIApplication([('/', MainPage),
                              ('/app', Ocr),
                              ('/apptest', Apptest)],
                              debug=True)