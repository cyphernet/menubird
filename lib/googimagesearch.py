import urllib2
import urllib
import json as simplejson

class GoogImageSearch():

	def search(self, term, ip):
		url = ('https://ajax.googleapis.com/ajax/services/search/images?' +
			   'v=1.0&q='+urllib.quote(term)+'&userip='+urllib.quote(ip))

		request = urllib2.Request(url, None, {})
		response = urllib2.urlopen(request)

		# Process the JSON string.
		results = simplejson.load(response)

		return results[u'responseData'][u'results']