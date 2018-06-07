# coding=utf-8

import redis

class RedisClient(object):

  def __init__(self, host, port=6379, use_strict=False):
    pool = redis.ConnectionPool(host=host,port=int(port),decode_responses=True)
    if use_strict:
      self.client = redis.StrictRedis(connection_pool=pool)
    else:
      self.client = redis.Redis(connection_pool=pool)

  def __getattr__(self, name):
    return getattr(self.client, name)

# RedisClient