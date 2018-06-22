#encoding=utf-8
from iotsession import IotSession
import json
from datetime import datetime

'''
tool, fuck the unicode print
'''
def echo(data):
  if type(data) is str:
    res = data.encode('latin-1').decode('unicode_escape')
  elif type(data) is bytes:
    res = data.decode('unicode_escape')
  else:
    raise RuntimeError('%s???' % str(type(data)))
  print(res)
#echo

'''
some operations' encapsulation
Usage:
  session = IotSession('200.200.193.223', 'yuancf', 'sundray123')
  tool = IotHttpTool(session)

you can also extend this tool by defining new method，
using self.session.post() to encapsulate the reqeust path and params
'''
class IotHttpTool:

  '''
  @param session IotSession
  '''
  def __init__(self, host, username, passwd, admin_sess=''):
    self.session = IotSession(host, username, passwd, admin_sess)
  #end init

#end class IotHttpTool



if __name__ == '__main__':
  tool = IotHttpTool('10.156.163.51', 'admin', 'admin')