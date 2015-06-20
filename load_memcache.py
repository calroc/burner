from memcache import Client
import burnerconf, local_cache


mc = Client([burnerconf.CACHE_URL], debug=True)
with open('local_cache.txt') as data:
  for tag, url in local_cache.LocalCache.read(data):
    mc.set(tag, url)
    print tag, url
