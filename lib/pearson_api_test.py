import urllib2

appKey = 'ee031c87dcfd97c3ab60ad494ea9a488'
url = 'http://api.pearson.com/kitchen-manager/v1/recipes.json?apikey=' + appKey
try:
 data = urllib2.urlopen(url).read()
 print data
except urllib2.HTTPError, e:
 print "HTTP error: %d" % e.code
except urllib2.URLError, e:
 print "Network error: %s" % e.reason.args[1]
