from server import run, Server
from handlers import RegistrationHandler, GetHandler
from store import get_client, store, get
import burnerconf


cache = get_client([burnerconf.CACHE_URL])
server = Server(
  get=GetHandler(cache, get),
  register=RegistrationHandler(cache, store),
  )
run(server)
