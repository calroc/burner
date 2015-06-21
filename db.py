from time import time
from boto.dynamodb2.table import Table
from boto.dynamodb2.exceptions import (
  ConditionalCheckFailedException,
  ItemNotFound,
  )


def T():
  return int(round(time(), 3) * 1000)


def fetch(table, tag):
  try:
    item = table.get_item(tag=tag)
  except ItemNotFound:
    pass
  else:
    return str(item['url'])


def write_datum(table, tag, url):
  try:
    return table.put_item(data={
      'tag': tag,
      'url': url,
      'when': T(),
      })
  except ConditionalCheckFailedException:
    return False
