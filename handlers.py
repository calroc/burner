from urlparse import urlparse
from werkzeug.wrappers import Request
import local_cache


LOCAL_CACHE = local_cache.get_cache('local_cache.txt')


def register(url, cache, store, local=LOCAL_CACHE):
  url = normalize_url(url)
  if not url:
    return
  tag = local.get(url)
  if tag is None:
    local[url] = tag = store(cache, url)
  return tag


def lookup(tag, cache, get, local=LOCAL_CACHE):
  url = local.inverted.get(tag)
  if not url:
    url = get(cache, tag)
    if not url:
      return
    local[url] = tag
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

  def __init__(self, cache, store):
    self.cache = cache
    self.store = store

  def __call__(self, environ):
    request = Request(environ)
    url = str(request.args.get('urly'))
    if not url:
      return 'no urly'
    tag = register(url, self.cache, self.store)
    if not tag:
      return 'untaggable for some reason'
    return tag


class GetHandler(object):

  def __init__(self, cache, get):
    self.cache = cache
    self.get = get

  def __call__(self, environ):
    request = Request(environ)
    tag = str(request.args.get('tag'))
    if not tag:
      return 'no tag'
    tag = str(tag)
    url = lookup(tag, self.cache, self.get)
    if not url:
      return 'untagged for some reason'
    return url
