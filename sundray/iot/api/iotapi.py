#coding=utf-8

from apirequest import ApiRequest

class IotApi(object):

  def __init__(self, host, api_token):
    self.req = ApiRequest(host, api_token)
  #init

  def set_status(self, data):
    url = self.req.api_url('setStatus')
    res = self.req.post(url, data)
    return res
  # set status

  def get_status(self, data):
    url = self.req.api_url('getStatus')
    return self.req.post(url, data)
  # get status

  def get_group(self, data):
    url = self.req.api_url('getGroup')
    return self.req.post(url, data)
  # get group

  def get_type_by_tag(self, data):
    url = self.req.api_url('getAllDevType')
    return self.req.post(url, data)
  # get by tag

#class IotApi

if __name__ == '__main__':
  IotApi('10.156.163.51', '098f6bcd4621d373cade4e832627b4f6')