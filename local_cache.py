from os.path import abspath, exists


MAX_SIZE = 10**8  # One hundred million lines max, a little safety.
CACHES = {}


def get_cache(path):
  path = abspath(path)
  try:
    return CACHES[path]
  except KeyError:
    CACHES[path] = cache = LocalCache(path)
    return cache


class LocalCache(dict):

  def __init__(self, path):
    path = abspath(path)
    self.path = path
    if exists(path):
      with open(path) as data:
        for line in data:
          try:
            tag, url = line.split()
          except:
            continue
          dict.__setattr__(self, tag, url)

  def __setattr__(self, tag, url):
    dict.__setattr__(self, tag, url)
    if len(self) < MAX_SIZE:
      with open(self.path, 'w') as data:
        print >> data, tag, url
