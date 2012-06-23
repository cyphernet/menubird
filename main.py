import webapp2
import jinja2
import os
from lib.ocr import *

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		template = jinja_environment.get_template('index.html')
		output = template.render(template_values)
		self.response.out.write(output)

app = webapp2.WSGIApplication([('/', MainPage),
                              ('/app', Ocr),
                              ('/apptest', Apptest)],
                              debug=True)