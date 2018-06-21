#coding=utf-8
import json
import urllib.request
import re
import time
import ssl

class ApiRequest(object):

  def __init__(self, host, api_token, auto_get_access_token=False):
    ssl._create_default_https_context = ssl._create_unverified_context
    self.host = host
    self.api_token = api_token
    self.auto_get_access_token = auto_get_access_token
    if auto_get_access_token: self.get_access_token()
  #init

  '''
    获取 access_token 的值，因更新 access_token 也会调用，故进行一层封装
  '''
  def get_access_token(self):
    self.access_token = self._get_access_token()['accessToken']
    return self.access_token
  # get token

  '''
    获取 access_token 的完整响应消息体，有时需要判断过期时间时需要用
  '''
  def get_access_token_response(self):
    return self._get_access_token()
  # get token response

  '''
    请求 access_token
  '''
  def _get_access_token(self):
    if not self.api_token:
      raise RuntimeError('api token cannot be empty.')
      return
    #if

    data = {
      'api_token': self.api_token
    }

    url = 'https://{}/api/v1/accessToken'.format(self.host)
    res = self._post(url, data)

    res = json.loads(res)

    if 'accessToken' in res:
      return res
    else:
      print(res)
      raise RuntimeError('is API enabled?')
      return
  #get access token

  '''
    access_token 过期之后重新获取 access_token 再请求
  '''
  def retry_request(self, url, data):
    new_url = re.sub('[0-9a-fA-F]{32}', url, self.get_access_token())
    res = self.post(new_url, data)
    return res
  # retry request

  '''
    请求 api 并处理返回失败的情况
  '''
  def post(self, url, data):
    res = self._post(url, data)
    res = json.loads(res)
    if not res['success']:
      if 'access token 非法' == res['msg']:
        pass
      elif 'access token 已过期' == res['msg']:
        res = self.retry_request(url, data)
      elif 'access token 非法' == res['msg']:
        pass
      else:
        pass
    # failed
    return res
  # post

  '''
    对 urllib.request 的封装
  '''
  def _post(self, url, data):
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/x-www-form')
    data = json.dumps(data).encode('utf-8')
    res = urllib.request.urlopen(
      req,
      data = data,
    )
    res = res.read().decode('utf-8')
    return res
  #req _post

  '''
    拼接 api 请求 url
  '''
  def marshal_api_url(self, opr, version='v1', use_https=True):
    if use_https:
      proto = 'https'
      port = '851'
    else:
      proto = 'http'
      port = '850'

    return '{proto}://{host}/api/{version}/device/{opr}?access_token={access_token}'.format(
      proto=proto,
      # port=port,
      host=self.host,
      version=version,
      # type_name=type_name,
      opr=opr,
      access_token=self.access_token,
    )
  #api url  

#class ApiRequest

if __name__ == '__main__':
  ApiRequest('10.156.163.51', '098f6bcd4621d373cade4e832627b4f6')