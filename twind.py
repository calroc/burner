from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.task import deferLater
from twisted.python import log
from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET


def foo(request, deferred):
  #  resp = str(dir(request)) + '\n\r'
  resp = (request, 'Hello World!')
  d = deferLater(reactor, 2, lambda: 1 / 0 + deferred.callback(resp))
  d.addErrback(deferred.errback)


class Page(Resource):

  isLeaf = True

  def render_GET(self, request):
    log.msg('in')
    self.get(request).addCallback(self._fin)
    return NOT_DONE_YET

  def _fin(self, (req, response)):
    req.write(response)
    req.finish()
    log.msg('out')

  def _err(self, request):
    def err_(failure):
      self._fin((request, str(failure)))
    return err_

  def get(self, request):
    d = Deferred()
    d.addErrback(self._err(request))
    foo(request, d)
    return d


if __name__ == '__main__':
  import sys
  log.startLogging(sys.stdout)
  factory = Site(Page())
  reactor.listenTCP(8000, factory)
  reactor.run()
