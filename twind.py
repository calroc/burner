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
    self.get(request).addCallback(self._fin)
    return NOT_DONE_YET

  def get(self, request):
    '''
    Create and return a deferred that should be triggered with a two-
    tuple containing the request object and the text response.
    '''
    return deferLater(reactor, 5, lambda: (request, 'Hello there!'))


factory = Site(Page())
reactor.listenTCP(8000, factory)
reactor.run()
