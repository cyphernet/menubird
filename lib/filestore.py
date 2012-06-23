from __future__ import with_statement

import cgi
import urllib

from google.appengine.api import files
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

try:
  files.gs
except AttributeError:
  import gs
  files.gs = gs

class Filestore():
	READ_PATH = '/gs/menubird'

	def create(self, file, filename, mime):
		# Create a file that writes to Cloud Storage and is readable by everyone in the 
		# project.
		write_path = files.gs.create(self.READ_PATH + '/' + filename, mime_type=mime, 
                                                            acl='public-read')
		# Write to the file.
		with files.open(write_path, 'a') as fp:
			fp.write(file)

		# Finalize the file so it is readable in Google Cloud Storage.
		files.finalize(write_path)
		
		return write_path