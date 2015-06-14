from server import run, Server
from handlers import make_reg_handler, make_get_handler
from store import get_client, store, get
import burnerconf


cache = get_client([burnerconf.CACHE_URL])
handle_registration = make_reg_handler(cache, store)
handle_lookup = make_get_handler(cache, get)
run(Server(
  get=handle_lookup,
  register=handle_registration,
  ))
