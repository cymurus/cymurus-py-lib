# import requests
import warnings
import urllib.request
import urllib.parse

warnings.filterwarnings("ignore")

'''
  disposable http post request
  when not 200, return false
'''
def post(url, data={}, headers={}):
  req = urllib.request.Request(url)

  for k,v in headers.items():
    req.add_header(k, v)
  # for headers

  if data: data = json.dumps(data).encode('utf-8')

  res = urllib.request.urlopen(
    req,
    data = data,
  )

  if res.code == 200:
    res = res.read().decode('utf-8')
  else:
    res = False
  # res code

  return res
# post

'''
  disposable http get request
  when not 200, return false
'''
def get(url, data={}, headers={}):
  if data:
    params = urllib.parse.urlencode(data)
  else:
    params = ''
  # data

  if params:
    params = '?' + params
  url = '{}{}'.format(url, params)

  try:
    
    res = urllib.request.urlopen(url)
  except Exception as e:
    res = urllib.request.urlopen('http://' + url)

  if res.code == 200:
    res = res.read().decode('utf-8')
  else:
    res = False
  # res code

  return res
# get