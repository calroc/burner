from urlparse import urlparse
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
  from store import get_client, store
  import pprint, burnerconf
  url = 'http://calroc.webfactional.com/00000000/00000000'
  cache = get_client([burnerconf.CACHE_URL])
  print register('http://dendritenetwork.com/', cache, store)
  print register(url, cache, store)
  print register('http://dendritenetwork.com/', cache, store)
  pprint.pprint(LOCAL_CACHE)
