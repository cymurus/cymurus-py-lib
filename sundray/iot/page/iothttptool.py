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

  def gen_token(self):
    data = {
      'opr': 'product_api_token',
      'msg': ''
    }
    return json.loads(self.session.post('/iotp/go/third_service', data).text)['data']
  #gen_token

  def third_service(self, token=''):
    data = {
      "opr": "set_third_service",
      "msg":'{"api_token":"%s","api_enable":true,"data_enable":true,"address":"112.74.173.195","token":"dataforward","eid":"asqwerty0000001d3625bafa0da9ea"}' % token
    }
    # data = {
    #   "opr": "get_third_service",
    #   "msg":'{"eid":"asqwerty0000001d3625bafa0da9ea"}'
    # }
    print(self.session.post('/iotp/go/third_service', data).text)
  #third service

  '''
  new method here to extend
  def xxx(self):
  #end xxx
  '''

#end class IotHttpTool



if __name__ == '__main__':
  tool = IotHttpTool('10.156.163.51', 'admin', 'admin')