from twisted.internet import reactor
from twisted.internet.task import deferLater
from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET


class Page(Resource):

  isLeaf = True

  def _fin(self, (req, response)):
    req.write(response)
    req.finish()

  def render_GET(self, request):
    d = deferLater(reactor, 5, lambda: (request, 'Hello there!'))
    d.addCallback(self._fin)
    return NOT_DONE_YET


factory = Site(Page())
reactor.listenTCP(8000, factory)
reactor.run()
