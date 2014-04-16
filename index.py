import os

import bottle
import bottle as app
from bottle import static_file
import requests

STATIC_PATH = os.path.abspath(
  os.path.join(os.path.abspath(__file__), '../')
)

@app.route('/')
def serve_static():
  with open(os.path.join(STATIC_PATH, 'index.html'), 'r') as file_obj:
    return file_obj.read()


@app.route('/<path:path>')
def serve_static(path):
  if os.path.exists(path):
    return static_file(path, root=STATIC_PATH)

  if not path[0] == '/':
    path = '/%s' % (path,)

  folder = os.path.join(path, '../')
  folder = os.path.abspath(STATIC_PATH + folder)

  if not os.path.exists(folder):
    os.makedirs(folder)

  with open(os.path.abspath(STATIC_PATH + path), 'w') as file_obj:
    response = requests.get('%s%s' % (host, path))
    print 'writing %s...' % (path,)
    file_obj.write(response.content)
  #import pdb; pdb.set_trace()

webapp = bottle.default_app()
webapp.run(host='0.0.0.0', port=9999)
