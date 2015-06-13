from os.path import abspath, exists


MAX_SIZE = 10**8  # One hundred million lines max, a little safety.
CACHES = {}


def get_cache(path):
  path = abspath(path)
  print 'get cache of', path
  try:
    return CACHES[path]
  except KeyError:
    CACHES[path] = cache = LocalCache(path)
    return cache


class LocalCache(dict):

  def __init__(self, path):
    path = abspath(path)
    self.path = path
    print 'making cache for', path
    if exists(path):
      with open(path) as data:
        for line in data:
          try:
            tag, url = line.split()
          except:
            continue
          dict.__setitem__(self, url, tag)

  def __setitem__(self, url, tag):
    print 'setting', url, tag
    dict.__setitem__(self, url, tag)
    if url not in self and len(self) < MAX_SIZE:
      print 'writing to disk', url, tag
      with open(self.path, 'a') as data:
        print >> data, tag, url
