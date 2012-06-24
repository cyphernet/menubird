import urllib2
import urllib
import json as simplejson

class GoogImageSearch():

	def search(self, term, ip):
		enc = urllib.quote_plus(term)
		url = ('https://ajax.googleapis.com/ajax/services/search/images?' +
			   'v=1.0&q='+enc+'&userip='+ip)

		request = urllib2.Request(url, None, {})
		response = urllib2.urlopen(request)

		# Process the JSON string.
		results = simplejson.load(response)

		return results[u'responseData'][u'results']