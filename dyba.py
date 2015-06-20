from threading import Lock, Thread
from time import sleep
from boto.dynamodb2.table import Table


BATCH_LIMIT = 25
SLEEP_SECONDS = 1
DONE = 'done'


def make_batcher_thread(table_name):
  lock = Lock()
  buff = []
  regy = Table(table_name)
  thread = Thread(target=batcher, args=(lock, buff, regy))
  thread.start()
  def enqueue_datum(datum):
    append(lock, buff, datum)
  return enqueue_datum


def batcher(lock, data, table):
  while True:
    local_data = grab(lock, data)
    if not batch_and_send(local_data, table):
      print 'Done.'
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
  for batch in by_twenty_fives(local_data):
    send_batch(batch, table)
    sleep(SLEEP_SECONDS)
  else:
    sleep(SLEEP_SECONDS)  # Sleep at least once per loop.
  return res


def by_twenty_fives(data):
  while data:
    batch, data = data[:25], data[25:]
    yield batch


def send_batch(batch, table):
  with table.batch_write() as table_batch:
    for datum in batch:
      table_batch.put_item(data=datum)
      print 'sending', datum
  # Implicit send occurs here.


def example():
  a = make_batcher_thread('regy')
  for n in range(55):
    a(n)
  a(DONE)
  print 'Queued!'

