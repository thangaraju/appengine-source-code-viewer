import os

# Google App Engine imports.
from google.appengine.ext.webapp import util
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class Sourcer(webapp.RequestHandler):
  def get(self):
    tpl_data = {'appname': 'Sourcer'}
    ROOT_PATH = os.path.dirname(__file__)
    name = self.request.get('name', '')
    request_path = os.path.join(ROOT_PATH, name)
    if not os.path.isdir(request_path):
      try:
        filepointer = open(request_path, 'r')
        self.response.out.write(filepointer.read())
      except Exception:
        self.response.out.write('Error occured while accessing file')
      return
    files = os.listdir(os.path.join(ROOT_PATH, request_path))
    items = []
    TPL_PATH = os.path.join(ROOT_PATH, 'tpl-sourcer/sourcer.html')
    for file in files:
      path = os.path.join(name, file)
      isdir = os.path.isdir(path)
      try:
        size = os.path.getsize(path)
      except Exception:
        size = ''
      item = {
          'path': path,
          'name': file,
          'size': size,
          'isdir': isdir,
          'type': ('file', 'dir')[isdir]
          }
      items.append(item)
    tpl_data['items'] = items
    tpl_data['list'] = 'The current folder'
    self.response.out.write(template.render(TPL_PATH, tpl_data))
 

application = webapp.WSGIApplication([('/s', Sourcer), ], debug=True)

def main():
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()


