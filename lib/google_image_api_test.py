import urllib2
import json as simplejson

url = ('https://ajax.googleapis.com/ajax/services/search/images?' +
       'v=1.0&q=chicken+%20broccoli&userip=108.176.38.66')

request = urllib2.Request(url, None, {'Referer': 'http://hello.brightidea.com/bellybucket'})
response = urllib2.urlopen(request)

# Process the JSON string.
results = simplejson.load(response)

print results
