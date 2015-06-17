from server import run, Server
from handlers import RegistrationHandler, GetHandler
from store import get_client, store as _store, get as _get
import burnerconf


cache = get_client([burnerconf.CACHE_URL])
def store(url): return _store(cache, url)
def get(tag): return _get(cache, tag)


server = Server(
  get=GetHandler(get),
  register=RegistrationHandler(store),
  )
run(server)
