﻿import webapp2
from lib.filestore import *
from lib.models import *
from google.appengine.api import conversion

class Ocr(webapp2.RequestHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'text/plain'
		imageFile = self.request.get("img")
		fileupload = self.request.POST.get("img",None)
		contentType = getContentType( fileupload.filename )
		
		# Store the image for laters
		storage = Filestore()
		wp = storage.create(imageFile, fileupload.filename)
		
		# Create a conversion request from HTML to PNG.
		asset = conversion.Asset(contentType, imageFile, fileupload.filename)
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
			food.filename = fileupload.filename
			food.location = 'https://storage.cloud.google.com/menubird/'+fileupload.filename
			food.put()

			self.response.out.write(food_name)

		else:
		  handleError(result.error_code, result.error_text)

def getContentType( filename ): # lists and converts supported file extensions to MIME type
	ext = filename.split('.')[-1].lower()
	if ext == 'jpg' or ext == 'jpeg': return 'image/jpeg'
	if ext == 'png': return 'image/png'
	if ext == 'gif': return 'image/gif'
	if ext == 'svg': return 'image/svg+xml'
	return None
	
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