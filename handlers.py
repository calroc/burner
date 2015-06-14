from werkzeug.wrappers import Request


def handle_registration(environ):
  request = Request(environ)
  return 'hi there! ' + str(request.args.get('urly'))
