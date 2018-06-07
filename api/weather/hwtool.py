#encoding=utf-8
import sys
sys.path.append('../../../')
# back to dir 'cymurus'

from cymurus.http import *
import json

class HWTool(object):

  def __init__(self, key):
    self.key = key
  #end init

  def get_hourly(self, city):
    data = get('https://free-api.heweather.com/v5/hourly?city=%s&key=%s' % (city, self.key))
    data = json.loads(data)
    data = data['HeWeather5'][0]

    res = {}

    res['temp'] = data['hourly_forecast'][0]['tmp']
    res['weather'] = data['hourly_forecast'][0]['cond']['txt']

    return res
  #end hourly

  def get_forecast(self, city):
    data = get('https://free-api.heweather.com/v5/forecast?city=%s&key=%s' % (city, self.key))
    data = json.loads(data)
    data = data['HeWeather5'][0]

    res = {}

    res['temp'] = data['daily_forecast'][1]['tmp']
    res['weather'] = data['daily_forecast'][1]['cond']

    return res
  #end hourly


if __name__ == '__main__':
  tool = HWTool('208745e21ad540e08546badf9b6418ab')
  # res = tool.get_hourly('CN101280604')
  res = tool.get_forecast('CN101280604')
  print(res)