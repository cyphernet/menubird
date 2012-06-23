import webapp2
from google.appengine.api import conversion

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('Hello World!')

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
		  	self.response.out.write(asset.data)
		  	self.response.out.write(asset)
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