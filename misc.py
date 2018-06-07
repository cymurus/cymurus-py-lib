from datetime import datetime
from datetime import timedelta

'''
  time
'''

def now():
  return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# now

def now_stamp():
  return datetime.now().strftime('%Y%m%d%H%M%S')
# now

'''
  collection
'''

# 2d dict add
def dict_add(m, key_1, key_2, val):
  if key_1 in m:
    m[key_1].update({key_2: val})
  else:
    m.update({key_1:{key_2: val}})
#dict add

def time_gen(start, delta, time_fmt='%Y-%m-%d %H:%M:%S', gen_type=str):
  time = start
  while True:
    yield time
    time = datetime.strptime(time, time_fmt)
    time = time + timedelta(**delta)
    if gen_type == str:
      time = datetime.strftime(time, time_fmt)
    elif gen_type == datetime:
      pass
    # type
  # while true
# time generator

if __name__ == '__main__':
  t = time_gen('2018-05-08 00:00:00', {
    'minutes': 1
  })
  import time
  while True:
    time.sleep(1)
    print(t.__next__())
