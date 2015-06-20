from urlparse import urlparse
from werkzeug.wrappers import Request
from server import Error400
import local_cache


LOCAL_CACHE = local_cache.get_cache('local_cache.txt')


def register(url, store):
  url = normalize_url(url)
  if not url:
    return
  tag = LOCAL_CACHE.get(url)
  if tag is None:
    LOCAL_CACHE[url] = tag = store(url)
  return tag


def lookup(tag, get):
  url = LOCAL_CACHE.inverted.get(tag)
  if not url:
    url = get(tag)
    if not url:
      return
    LOCAL_CACHE[url] = tag
  return url


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

  def __init__(self, store):
    self.store = store

  def __call__(self, environ):
    request = Request(environ)
    url = request.args.get('urly')
    if not url:
      raise Error400('no urly')
    url = str(url)
    tag = register(url, self.store)
    if not tag:
      raise Error400('untaggable for some reason')
    return tag


class GetHandler(object):

  def __init__(self, get):
    self.get = get

  def __call__(self, environ):
    request = Request(environ)
    tag = request.args.get('tag')
    if not tag:
      raise Error400('no tag')
    tag = str(tag)
    url = lookup(tag, self.get)
    if not url:
      raise Error400('untagged for some reason')
    return url
