from server import run, Server
from handlers import make_reg_handler
from store import get_client, store
import burnerconf


cache = get_client([burnerconf.CACHE_URL])
handle_registration = make_reg_handler(cache, store)
run(Server(register=handle_registration))
