from traceback import format_exc
from wsgiref.simple_server import make_server


def posting(environ):
  return environ['REQUEST_METHOD'] == 'POST'


def start(start_response, message, mime_type):
  start_response(message, [('Content-type', mime_type)])


def err404(start_response, message):
  start(start_response, '404 huh?', 'text/plain')
  return [str(message)]


def err500(start_response, message):
  start(start_response, '500 Internal Server Error', 'text/plain')
  return [str(message)]


def ok200(start_response, response):
  start(start_response, '200 OK', 'text/plain')
  return response


class Server(object):

  def __init__(self):
    self.router = {
      'register': self.register,
      }

  def handle_request(self, environ, start_response):
    environ['path'] = path = self.pather(environ['PATH_INFO'])
    handler = self.router.get(path, self.default_handler)
    response = handler(environ)
    return ok200(start_response, response)

  def pather(self, path_info):
    return path_info.strip('/')

  def default_handler(self, environ):
    path = environ['path']
    return err404(start_response, path)

  def register(self, environ):
    return 'hi there!'

  def __call__(self, environ, start_response):
    try:
      return self.handle_request(environ, start_response)
    except:
      return err500(start_response, format_exc())


def run(app, host='', port=8000):
  httpd = make_server(host, port, app)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass


if __name__ == '__main__':
  run(Server())

