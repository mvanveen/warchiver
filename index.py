from optparse import OptionParser
import os

import bottle
import bottle as app
from bottle import static_file
import requests

STATIC_PATH = os.path.abspath(
  os.path.join(os.path.abspath(__file__), '../')
)

def get_options():
  parser = OptionParser()
  parser.add_option(
    '--host', dest='hostname', help='source url hostname'
  )
  parser.add_option(
    '-f', '--filename', dest='filename', help='source url hostname',
    default='index.html'
  )
  (options, args) = parser.parse_args()
  return options, args


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
    response = requests.get('%s%s' % (options.hostname, path))
    print 'writing %s...' % (path,)
    file_obj.write(response.content)


options, args = get_options()
if __name__ == '__main__':

  if not options.hostname:
    raise ValueError('hostname is required')

  webapp = bottle.default_app()
  webapp.run(host='0.0.0.0', port=9999)
