import webapp2
from lib.filestore import *
from lib.models import *
from lib.googimagesearch import *
from google.appengine.api import conversion
import json

class Ocr(webapp2.RequestHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'text/plain'
		imageFile = self.request.get("img")
		fileupload = self.request.POST.get("img",None)
		contentType = getContentType( fileupload.filename )
		
		# Store the image for laters
		storage = Filestore()
		wp = storage.create(imageFile, fileupload.filename, contentType)
		
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
			saved_food = food.put()
			
			# self.response.out.write(saved_food.id())
			# self.response.out.write('\r\n')
			ip = self.request.remote_addr
			#self.response.out.write(ip)
			goog = GoogImageSearch()
			res = goog.search(ocr_text, ip)
			resp_images = []
			for i in res:
				food_image = Food_image()
				food_image.name = i[u'titleNoFormatting']
				food_image.url = i[u'url']
				food_image.food = saved_food
				saved_food_image = food_image.put()
				resp_images.append(i[u'url'])
				
			self.response.out.write(json.dumps(dict(word=food_name, images=resp_images)))
			
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