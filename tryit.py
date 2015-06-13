from store import get_client, store, get


LOCAL_CACHE = {}
normalize_url = lambda url: url


def register(url, cache, store, local=LOCAL_CACHE):
  url = normalize_url(url)
  tag = local.get(url)
  if tag is None:
    print 'local cache miss', url
    tag = store(cache, url)
    local[url] = tag
  return tag


tag = 'ocs2levt5ke6futc2ng9bjn4ohq5sq3'
url = 'http://calroc.webfactional.com/00000000/00000000'


if __name__ == '__main__':
  import burnerconf
  cache = get_client([burnerconf.CACHE_URL])
  print register('http://dendritenetwork.com/', cache, store)
  print register(url, cache, store)
  print register('http://dendritenetwork.com/', cache, store)
  print LOCAL_CACHE


