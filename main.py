import webapp2
import jinja2
import os
import time

import json
import urllib
from google.appengine.api import urlfetch

from apiclient.discovery import build
from optparse import OptionParser



#for templates, later
jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname	   (__file__), 'templates')))

DEVELOPER_KEY = "AIzaSyBYnrYdbRZnpvoGfUblBdcOx9njmUL6lGY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MAX_RESULTS=48

LAST_QUERY = time.time()

def parseQuery(query):
  return query.split(',', 1)

def getVidIds(query, maxResults):
  vidIds = []
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

#  global LAST_QUERY
 # if (time.time()-LAST_QUERY < 1):
  #  time.sleep(1)
   # LAST_QUERY = time.time()

  search_response = youtube.search().list(q=query, part="id,snippet", maxResults=maxResults).execute()

  for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			vidIds.append(search_result["id"]["videoId"])
  return vidIds


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    
    def render_str(self, template, **params):
        t = jinja_environment.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):
  def get(self):
    query = parseQuery(self.request.get('query'))
    if len(query) == 3:
      query1 = getVidIds(query[0], MAX_RESULTS/2)
      query2 = getVidIds(query[1], MAX_RESULTS/2)
      query3 = getVidIds(query[2], MAX_RESULTS/2)
      vidIds = []
      for i, j, k in zip(query1, query2, query3):
        vidIds.append(i)
        vidIds.append(j)
        vidIds.append(k)
    if len(query) == 2:
      query1 = getVidIds(query[0], MAX_RESULTS/2)
      query2 = getVidIds(query[1], MAX_RESULTS/2)
      vidIds = []
      for i, j in zip(query1, query2):
        vidIds.append(i)
        vidIds.append(j)
    elif len(query) == 1:
      vidIds = getVidIds(query[0], MAX_RESULTS)
    else:
      vidIds = getVidIds('cats', MAX_RESULTS)

    zipped = zip(vidIds, range(len(vidIds)))
    self.render('index.html', data=zipped)
    #self.write(zipped)
  def post(self):
  	 self.redirect('/')



app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)