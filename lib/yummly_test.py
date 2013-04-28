import urllib2
import urllib
import pprint
import json

appKey = 'ee031c87dcfd97c3ab60ad494ea9a488'


yummly_key = 'b6998854&_app_key=e1bf1eeff4ea2aa5bb7d8fabebc27a67'
fs = 'q='+ urllib.quote('French onion soup');
url = 'http://api.yummly.com/v1/api/recipes?_app_id=b6998854&_app_key=' + yummly_key+'&'+fs +'&requirePictures=true';


try:
	data = urllib2.urlopen(url).read()
	data = json.loads(data)
	#pprint.pprint(data)
	#pprint.pprint(data['matches'])
	m = data['matches']
	pprint.pprint(data['matches'][0]['flavors'])
	pprint.pprint(data['matches'][0]['ingredients'])
	pprint.pprint(data['matches'][0]['smallImageUrls'])
except urllib2.HTTPError, e:
 print "HTTP error: %d" % e.code
except urllib2.URLError, e:
 print "Network error: %s" % e.reason.args[1]
