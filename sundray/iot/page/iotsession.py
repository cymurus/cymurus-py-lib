#encoding=utf-8
import requests
import json
import warnings

warnings.filterwarnings("ignore")

'''
create a new IOT Session of a specifical user
Usage:
  session = IotSession('200.200.193.223', 'yuancf', 'sundray123')
  session.post(url, data)
'''
class IotSession:

  '''
  constuction
  @param username string
  @param passwd string
  @param admin_sess string 运维平台session
  '''
  def __init__(self, host, username, passwd, admin_sess=''):
    self.host = host
    self.username = username
    self.passwd = passwd
    self.session = requests.session()
    # self.cookies = self.login().cookies
    self.headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Encoding': 'gzip, deflate, sdch, br',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'Accept-Language': 'zh-CN,zh;q=0.8',
      'Connection': 'keep-alive',
      'Host': host,
      'Origin': 'https://%s' % host,
      'X-Requested-With': 'XMLHttpRequest',
      'Referer': 'https://%s/SPM/main-admin.php' % host if admin_sess else 'https://%s/SPM/main.php' % host
    }
    self.login(admin_sess)
  #end init

  '''
  login url path default to '/iotp/web/WebHome/login'
  '''
  def login(self, admin_sess=''):

    if admin_sess:
      path='/iotp/admin/Home/login'
      self.headers['Cookie'] = admin_sess
      return 
    else:
      path='/iotp/web/WebHome/login'

    host = self.host
    login_url = 'https://%s%s' % (host, path)

    login_headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Encoding': 'gzip, deflate, sdch, br',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'Accept-Language': 'zh-CN,zh;q=0.8',
      'Connection': 'keep-alive',
      'Host': host,
      'Origin': 'https://%s' % host,
      'X-Requested-With': 'XMLHttpRequest',
      'Referer': 'https://%s/SPM/index.php' % host
    }

    login_data = {
      'userid': self.username,
      'passwd': self.passwd
    }

    return self.session.post(
      login_url,
      data=login_data,
      headers=login_headers,
      verify=False
    )
  #end login

  '''
  the proxy method of self.session.post
  '''
  def _post(self, path, data, headless=False):
    return self.session.post(
      'https://%s%s' % (self.host, path),
      data=data,
      headers={} if headless else self.headers,
      verify=False
    )
  #end post

  def post(self, path, data, headless=False):
    res = self._post(path, data, headless)
    res = res.text
    res = json.loads(res)
    if res['success']:
      return res['data']
    else:
      pass
  # post

#end class IotSession

if __name__ == '__main__':
  # s = IotSession('200.200.193.222', 'admin', 'admin')
  s = IotSession('10.22.52.10', 'sundray', 'sundray')
  # c = s.cookies
  # print(c.keys()[0] + '=' + c.values()[0])
#endif