from urlparse import urlparse
from werkzeug.wrappers import Request
from server import Error400
from tagger import tag_for
from db import write_datum, fetch
import local_cache


LOCAL_CACHE = local_cache.get_cache('local_cache.txt')


def normalize_url(url):
  try:
    result = urlparse(url.lower())
  except:
    return
  if (
    result.scheme in ('http', 'https')
    and not (result.params or result.query or result.fragment)
    ):
    url = result.geturl()
    return url if url.endswith('/') else url + '/'


class RegistrationHandler(object):

  def __init__(self, cache, table):
    self.cache = cache
    self.table = table

  def register(self, url):
    url = str(url)
    url = normalize_url(url)
    if not url:
      return
    tag = LOCAL_CACHE.get(url)
    if tag:
      return tag
    tag = tag_for(url)
    if self.cache.get(tag) is not None:
      return tag  # Already in cache, and db presumably.
    if write_datum(self.table, tag, url):
      LOCAL_CACHE[url] = tag
      self.cache.set(tag, url)
      return tag
    else:
      raise Error400('the db is cranky right now')

  def __call__(self, environ):
    request = Request(environ)
    url = request.args.get('urly')
    if not url:
      raise Error400('no urly')
    tag = self.register(url)
    if not tag:
      raise Error400('untaggable for some reason')
    return tag


class GetHandler(object):

  def __init__(self, cache, table):
    self.cache = cache
    self.table = table

  def lookup(tag):
    tag = str(tag)
    url = LOCAL_CACHE.inverted.get(tag)
    if url:
      return url
    url = self.cache.get(tag)
    if url:
      LOCAL_CACHE[url] = tag
      return url
    url = fetch(self.table, tag)
    if url:
      LOCAL_CACHE[url] = tag
      self.cache.set(tag, url)
      return url

  def __call__(self, environ):
    request = Request(environ)
    tag = request.args.get('tag')
    if not tag:
      raise Error400('no tag')
    url = self.lookup(tag)
    if not url:
      raise Error400('untagged for some reason')
    return url
