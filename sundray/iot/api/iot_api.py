#coding=utf-8

from .api_request import ApiRequest

class IotApi(object):

  def __init__(self, host, api_token):
    self.req = ApiRequest(host, api_token)
  #init

  def set_status(self, data):
    url = self.req.marshal_api_url('setStatus')
    res = self.req.post(url, data)
    return res
  # set status

  def get_status(self, data):
    url = self.req.marshal_api_url('getStatus')
    return self.req.post(url, data)
  # get status

  def get_group(self, data):
    url = self.req.marshal_api_url('getGroup')
    return self.req.post(url, data)
  # get group

  def get_type_by_tag(self, data):
    url = self.req.marshal_api_url('getAllDevType')
    return self.req.post(url, data)
  # get by tag

#class IotApi

if __name__ == '__main__':
  api = IotApi('172.16.1.51', '098f6bcd4621d373cade4e832627b4f6')
  api.set_status({
    'LoRaPlug': {
      'device_ids': ['GEK8030318'],
      'data': {
        'DEV_SWITCH_STA': '1'
      }
    }
  })
  # IotApi('10.156.163.51', '098f6bcd4621d373cade4e832627b4f6')