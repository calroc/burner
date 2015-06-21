from db import Table
from server import run, Server
from handlers import RegistrationHandler, GetHandler
from store import get_client, store as _store, get as _get
import burnerconf


cache = get_client([burnerconf.CACHE_URL])
regy = Table('regy')


server = Server(
  get=GetHandler(cache, regy),
  register=RegistrationHandler(cache, regy),
  )
run(server)
