import webapp2
from lib.filestore import *

class Ocr(webapp2.RequestHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'text/plain'

		# Store the image for laters
		storage = Filestore()
		storage.create(self.request.get("img"))
		
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