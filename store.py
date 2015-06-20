from memcache import Client
from tagger import tag_for


def get_client(urls):
  return Client(urls, debug=True)


def store(cache, url):
  key = tag_for(url)
  cache.set(key, url)
  return key


def get(cache, key):
  return cache.get(key)


if __name__ == '__main__':
  url = 'http://calroc.webfactional.com/00000000/00000000/'
  CACHE_URL = 'localhost:11211'
  cache = get_client([CACHE_URL])
  tag = store(cache, url)
  print tag, get(cache, tag)
