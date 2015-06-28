import sys
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.task import deferLater
from twisted.python import log
from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET


def foo(request, deferred):
  deferred.callback((request, 'Hello World!'))


class Page(Resource):

  isLeaf = True

  def _fin(self, (req, response)):
    req.write(response)
    req.finish()
    log.msg('out')

  def render_GET(self, request):
    log.msg('in')
    self.get(request).addCallback(self._fin)
    return NOT_DONE_YET

  def get(self, request):
    '''
    Create and return a deferred that should be triggered with a two-
    tuple containing the request object and the text response.
    '''
    resp = str(dir(request)) + '\n\r'
    return deferLater(reactor, 5, lambda: (request, resp))


class AQA(Page):

  def get(self, request):
    d = Deferred()
    try:
      foo(request, d)
    except Exception, e:
      d.errback((request, e))
    return d


if __name__ == '__main__':
  log.startLogging(sys.stdout)
  factory = Site(AQA())
  reactor.listenTCP(8000, factory)
  reactor.run()
