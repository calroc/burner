from urlparse import urlparse
from local_cache import get_cache
from store import get_client, store, get


LOCAL_CACHE = get_cache('local_cache.txt')


def register(url, cache, store, local=LOCAL_CACHE):
  url = normalize_url(url)
  if not url:
    return
  tag = local.get(url)
  if tag is None:
    print 'local cache miss', url
    tag = store(cache, url)
    local[url] = tag
  return tag


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

if __name__ == '__main__':
  import pprint, burnerconf
  url = 'http://calroc.webfactional.com/00000000/00000000'
  cache = get_client([burnerconf.CACHE_URL])
  print register('http://dendritenetwork.com/', cache, store)
  print register(url, cache, store)
  print register('http://dendritenetwork.com/', cache, store)
  pprint.pprint(LOCAL_CACHE)
