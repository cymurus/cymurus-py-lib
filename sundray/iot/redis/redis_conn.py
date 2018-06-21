# coding=utf-8

import redis

class RedisClient(object):

  def __init__(self, host, port=6379, use_strict=False):
    pool = redis.ConnectionPool(host=host, port=int(port), decode_responses=True)
    if use_strict:
      self.client = redis.StrictRedis(connection_pool=pool)
    else:
      self.client = redis.Redis(connection_pool=pool)

  def __getattr__(self, name):
    return getattr(self.client, name)

# RedisClient


class IotRedis(RedisClient):

  '''
    确保平台 /iotp/3party/redis/57379.conf 中：
    1. 注释掉 bind 127.1.0.1
    2. protected-mode no
  '''
  def __init__(self, host, port=57379, use_strict=False):
    super().__init__(host, port, use_strict)

# IotRedis

if __name__ == '__main__':
  rds = IotRedis('10.156.163.51')
  # rds.hset('asqwerty0000001d3625bafa0da9ea:fd0324430000002af1314589f9a7534c:GEK0000001:statusVal', 'DEV_LORADBM', -666)
  print(rds.hget('asqwerty0000001d3625bafa0da9ea:fd0324430000002af1314589f9a7534c:GEK0000001:statusVal', 'DEV_LORADBM'))