from hashlib import sha1
from string import digits, lowercase


STR = (digits + lowercase).__getitem__


def to36(i):
  acc = []
  while i:
    i, r = divmod(i, 36)
    acc.append(STR(r))
  return ''.join(acc[::-1])


def tag_for(s):
  return to36(int(sha1(s).hexdigest(), 16))


if __name__ == '__main__':
  url = 'http://calroc.webfactional.com/00000000/00000000'
  print url, tag_for(url)
