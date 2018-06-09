# coding=utf-8

def singleton(cls):
  instance = {}
  def get_instance(*args, **kwargs):
    if cls not in instance:
      instance[cls] = cls(*args, *kwargs)
    return instance[cls]
  return get_instance


import copy

def prototype(proto_method='clone'):
  def wrapper(cls):
    def clonablify(*args, **kwargs):
      setattr(cls, proto_method, lambda self: copy.deepcopy(self))
    return clonabify
  return wrapper