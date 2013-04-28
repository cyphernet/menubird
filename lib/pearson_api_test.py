import urllib2
import urlib
appKey = 'ee031c87dcfd97c3ab60ad494ea9a488'
food = 'french onion sout'
food_str = urlib.urlencode(food)
url = 'http://api.pearson.com/kitchen-manager/v1/recipes.json?apikey=' + appKey + '&q='+ food_str + '&requirePictures=true'

try:
 data = urllib2.urlopen(url).read()
 print data
except urllib2.HTTPError, e:
 print "HTTP error: %d" % e.code
except urllib2.URLError, e:
 print "Network error: %s" % e.reason.args[1]
