from threading import Lock, Thread
from time import sleep, time
from boto.dynamodb2.table import Table


BATCH_LIMIT = 25
SLEEP_SECONDS = 1
DONE = 'done'
APPENDERS = {}


def write_datum(appender, tag, url):
  appender({
    'tag': tag,
    'url': url,
    'when': time(),
    })


def get_appender(table_name):
  try:
    return APPENDERS[table_name]
  except KeyError:
    APPENDERS[table_name] = a = make_batcher_thread(table_name)
    return a


def make_batcher_thread(table_name):
  lock = Lock()
  buff = []
  thread = Thread(target=batcher, args=(lock, buff, table_name))
  thread.start()
  def enqueue_datum(datum):
    if not thread.is_alive():
      raise RuntimeError('thread is dead')
    append(lock, buff, datum)
  return enqueue_datum


def batcher(lock, data, table_name):
  table = Table(table_name)
  while True:
    local_data = grab(lock, data)
    if not batch_and_send(local_data, table):
      break


def grab(lock, data):
  lock.acquire()
  try:
    local_data, data[:] = data[:], []
  finally:
    lock.release()
  return local_data


def append(lock, data, item):
  lock.acquire()
  try:
    data.append(item)
  finally:
    lock.release()


def batch_and_send(local_data, table):
  try:
    i = local_data.index(DONE)
  except ValueError:
    res = True
  else:
    res = False  # Quit after this.
    del local_data[i:]  # Ignore data after None.
  send_all(table, local_data)
  return res


def send_all(table, data):
  for batch in chop(local_data):
    send_batch(batch, table)
    sleep(SLEEP_SECONDS)
  else:
    sleep(SLEEP_SECONDS)  # Sleep at least once per loop.


def chop(data, by=BATCH_LIMIT):
  while data:
    batch, data = data[:by], data[by:]
    yield batch


def send_batch(batch, table):
  with table.batch_write() as table_batch:
    for datum in batch:
      table_batch.put_item(data=datum)
  # Implicit send occurs here.
