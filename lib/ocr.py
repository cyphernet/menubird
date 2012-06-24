import webapp2
from lib.filestore import *
from lib.models import *
from lib.googimagesearch import *
from google.appengine.api import conversion
import json
import sys
import urllib2
from fatsecret import FatSecretClient, FatSecretApplication
from fatsecret import FatSecretError
from pprint import pprint

def compStr(food):
    return u' '.join(food.lower().split())   
	
class FatSecretTestApplication(FatSecretApplication):
    key = "cf3e497b0ae54b3b903b3a4a7844b36e"
    secret = "a9156b87ab3e4f809b6256309a200ad0"
	
class Ocr(webapp2.RequestHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'text/plain'
		imageFile = self.request.get("img")

		foodName = self.request.POST.get("word",'')
		fileupload = self.request.POST.get("img",None)
		try:
			filename = fileupload.filename
		except:
			filename = ''
		if len( foodName ) > 0 or len( filename ) == 0: 
			food_name = foodName
			ocr_text = foodName
			filename = ''
			contentType = 'text'
		else:
			contentType = getContentType( filename )

			# Create a conversion request from HTML to PNG.
			asset = conversion.Asset(contentType, imageFile, filename)
			conversion_obj = conversion.Conversion(asset, "text/plain", 1, 1, 1, "en-US")

			result = conversion.convert(conversion_obj)
			if result.assets:
			  # Note: in most cases, we will return data all in one asset.
			  # Except that we return multiple assets for multiple pages image.
			  for asset in result.assets:
				ocr_text = asset.data
				food_name = unicode(ocr_text, 'utf-8').lower()
			else:
				handleError(result.error_code, result.error_text)
		
		q = db.GqlQuery("SELECT * FROM Food " +
						"WHERE name = :1 " +
						"ORDER BY date DESC LIMIT 1",
						food_name)
		
		results = q.fetch(1)
		
		resp_images = []
		if results:
		  food_description = []
		  for x in results:
			resp_images.append(x.images)
			food_description.append(x.info)
			self.response.out.write(json.dumps(dict(word=food_name, images=resp_images, info=food_description)))
		else:
			# Store the image for laters
			food_description = {}
			storage = Filestore()
			wp = storage.create(imageFile, filename, contentType)
		
			# self.response.out.write(saved_food.id())
			# self.response.out.write('\r\n')
			client = FatSecretClient().connect().setApplication(FatSecretTestApplication)
			food = (client.foods.search(search_expression=ocr_text, max_results=3))
			if u'foods' in food:
				if u'food' in food[u'foods']:
					try:
						foodObj = food[u'foods'][u'food'][0]
					except:
						foodObj = ''
					if foodObj != '':
						for f in food[u'foods'][u'food']:
							if(compStr(f[u'food_name']) == food_name):
							   foodObj = f
						food_description['description'] = foodObj[u'food_description']
						food_description['food_id'] = foodObj[u'food_id']
						food_description['food_name'] = foodObj[u'food_name']
			ip = self.request.remote_addr
			#self.response.out.write(ip)
			goog = GoogImageSearch()
			search = food_description.get('food_name','')
			if search != '':
				res = goog.search(food_description['food_name'], ip)
				for i in res:
					resp_images.append(i[u'url'])
			else:
				resp_images = []
			self.response.out.write(json.dumps(dict(word=food_name, images=resp_images, info=food_description)))

			if 'food_id' in food_description:
				food = client.food.get(food_id=food_description['food_id'])
				if u'food' in food:
					if u'servings' in food[u'food']:
						if u'serving' in food[u'food'][u'servings']:
							food_description['serving'] = food[u'food'][u'servings'][u'serving']
			
			urlFoodName = urllib.quote_plus(foodName)
			appKey = 'ee031c87dcfd97c3ab60ad494ea9a488'
			url = 'http://api.pearson.com/kitchen-manager/v1/recipes?name-contains=' + urlFoodName  + '&apikey=' + appKey
			food_description['recipe'] = urllib2.urlopen(url).read()

			if u'results' in foodName:
				for r in foodName[u'results']:
					food_temp = {}
					for i in r:
						food_temp[r] = r[i]
					food_description[r]	= food_temp
			
			food = Food()
			food.name = food_name
			food.filename = filename
			food.location = 'https://storage.cloud.google.com/menubird/'+filename
			food.images = resp_images
			food.info = json.dumps(food_description)
			saved_food = food.put()
					

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
					 <div><input type="text" name="word"/></div>
		            <div><input type="submit" value="test" /></div>
		          </form>
		        </body>
		      </html>""")
