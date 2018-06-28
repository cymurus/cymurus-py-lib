#encoding=utf-8
import json
from datetime import datetime

from .iotsession import IotSession
from .iot_info import get_device_info

class DeviceManager():

  def __init__(self, host, username, passwd, admin_sess=''):
    self.session = IotSession(host, username, passwd, admin_sess)
    self.refresh_cache()
    self.device_info = get_device_info('device_db')
  #end init

  def refresh_cache(self):
    self.group_cache = self.list_group()
    # self.device_cache = self.list_device()
  # refresh

#*************************************group begin*******************************#

  def get_group_id_by_name(self, group_name, key='id'):
    if isinstance(group_name, int): return group_name
    groups = self.group_cache
    for group in groups:
      if group['name'] == group_name:
        return group[key]
      # if
    # for
  # get_group_id_by_name

  def flatten_group(self, data, res=[], keys=['id', 'name', 'path', 'leaf']):
    data = data.values()
    for d in data:
      res.append({ k:d[k] for k in keys})
      if 'children' in d:
        return self.flatten_group(d['children'], res)
      # if
    # for
    return res
  # flatten_group

  def list_group(self):
    groups = []
    data = {
      'opr': 'listgroup',
      'msg': '{"typeID":"3351be9e00000028741a888be4f9867a"}'
    }
    res = self.session.post('/iotp/web/v2/DevicesManagement', data)
    res = self.flatten_group(res)
    return res
  # list_group

  def add_group(self, path):
    tmp = list(filter(lambda x:x, path.split('/')))
    if not len(tmp): return
    group_name = tmp[-1]
    if len(tmp) == 1 :
      parent_id = 1
    else:
      parent_id = self.get_group_id_by_name(tmp[-2])
    # if
    data = {
      'opr': 'addgroup',
      'msg': '{"parentGroupID":%d,"groupName":"%s","groupDesc":"%s"}' % (parent_id, group_name, group_name)
    }
    res = self.session.post('/iotp/web/v2/DevicesManagement', data)
    self.refresh_cache()
    return res
  # add_group

  def edit_group(self, old_name, new_name):
    group_id = self.get_group_id_by_name(old_name)
    parent_id = 1
    data = {
      'opr': 'editgroup',
      'msg': '{"parentGroupID":%d,"groupID":%d,"groupName":"%s","groupDesc":"%s","force":false}' % (parent_id, group_id, new_name, new_name)
    }
    res = self.session.post('/iotp/web/v2/DevicesManagement', data)
    self.refresh_cache()
    return res
  # edit_group

  def delete_group(self, group_name):
    group_id = self.get_group_id_by_name(group_name)
    data = {
      'opr': 'deletegroup',
      'msg': '{"groupID":%d}' % (group_id)
    }
    res = self.session.post('/iotp/web/v2/DevicesManagement', data)
    self.refresh_cache()
    return res
  # delete_group

#*************************************group end*******************************#

#*************************************device begin*******************************#

  def get_device_id_by_name(self, device_name):
    # TO-DO
    return device_name
  # get_device_id_by_name

  def get_type_id_by_sn(self, sn):
    tmp = sn[:3]
    for d in self.device_info.values():
      if tmp in d['sn']:
        return d['type_id']
  # get_type_id_by_sn

  def list_device(self, type_name, group_name='', keys=['deviceStat', 'deviceID', 'deviceName', 'groupID', 'groupName', 'onlinetime', 'reportTime']):
    devices = []
    type_id = self.device_info[type_name]['type_id']
    if not group_name:
      group_id = 1
    else:
      group_id = self.get_group_id_by_name(group_name)
    # 
    data = {
      'opr': 'devices_list',
      'msg': '{"current":1,"rowCount":5000,"search":null,"increase":false,"keyword":"","grepByStat":"","searchBy":"deviceName","operator":"getData","typeID":"%s","groupID":%d}' % (type_id, group_id)
    }
    res = self.session.post('/iotp/web/v2/DevicesManagement', data)
    res = res['rows']
    for d in res:
      devices.append({ k:d[k] for k in keys})
    return devices
  # list devices

  # move_info = [(device_name, group_name)]
  def move_device(self, move_info):
    if isinstance(move_info, str): move_info = [move_info]
    msg = json.loads('{"groups":null, "force":false}')
    msg_devices = []
    for d in move_info:
      device_id = self.get_device_id_by_name(d[0])
      type_id = self.get_type_id_by_sn(device_id)
      group_id = self.get_group_id_by_name(d[2]) if len(d) >=3 else 0
      new_name = d[0]
      msg_devices.append({
        'deviceID': device_id,
        'deviceName': new_name,
        'typeID': type_id,
        'groupID': group_id,
      })
    msg['devices'] = msg_devices
    msg = json.dumps(msg)
    data = {
      'opr': 'move',
      'msg': msg
    }
    res = self.session.post('/iotp/web/v2/DevicesManagement', data)
    return res
  # move_device

  def delete_device(self, device_names):
    if isinstance(device_names, str): device_names = [device_names]
    msg = json.loads('{}')
    msg_devices = []
    for d in device_names:
      device_id = self.get_device_id_by_name(d)
      type_id = self.get_type_id_by_sn(device_id)
      msg_devices.append({
        'deviceID': device_id,
        'typeID': type_id,
      })
    msg['devices'] = msg_devices
    msg = json.dumps(msg)
    data = {
      'opr': 'deletedevices',
      'msg': msg
    }
    res = self.session.post('/iotp/web/v2/DevicesManagement', data)
    return res
  # delete_device

  def list_device_imported(self, keys=['sn', 'captcha', 'groupName']):
    devices = []
    data = {
      'opr': 'list',
      'msg': '{"current":1,"rowCount":5000,"search":null,"increase":false,"grepBy":"","searchBy":""}'
    }
    res = self.session.post('/iotp/go/device/snlist', data)
    res = res['rows']
    for d in res:
      devices.append({ k:d[k] for k in keys})
    return devices
  # list_device_imported

  def delete_device_imported(self, device_names):
    if isinstance(device_names, str): device_names = [device_names]
    device_ids = [self.get_device_id_by_name(device_name) for device_name in device_names]
    msg = []
    for device_id in device_ids:
      type_id = self.get_type_id_by_sn(device_id)
      msg.append({
        'sn': device_id,
        'typeID': type_id,
      })
    msg = json.dumps(msg)
    data = {
      'opr': 'delete',
      'msg': msg,
    }
    res = self.session.post('/iotp/go/device/sn', data)
    return res
  # delete_device_imported

  # sn_info = [(sn, group_name, captcha)]
  def import_device(self, sn_info):
    if not isinstance(sn_info, list): sn_info = [sn_info]
    msg = []
    for d in sn_info:
      group_id = self.get_group_id_by_name(d[1]) if len(d) >= 3 else 1
      captcha = d[2] if len(d) >= 2 else 'ffffffffffff'
      msg.append({
        'groupID': group_id,
        'sn': d[0],
        'captcha': captcha,
        'loraPwd': '',
        'data_link': 'lora'
      })
    msg = json.dumps(msg)
    data = {
      'opr': 'check',
      'msg': msg
    }
    res = self.session.post('/iotp/go/device/sn', data)
    return res
  # import_device

#*************************************device end*******************************#

#*************************************gateway start*******************************#

  def list_device_active(self, keys=['deviceStat', 'deviceID', 'onlinetime', 'typeName', 'ip', 'mac'], type_ids=['12dacaa9297efad0d3d2cfb2117eb83e', '3351be9e00000028741a888be4f9867a', '3351be9e00000028741a888be4f9867b', '3351be9e00000028741a888be4f9867c', '3965ba212cad84f9f4697f760bac540d', '82e9b2660000000a1b1a47e167bd8b49', 'c14bf866294f8add9d87f6509d39915c', 'fd0324430000002af1314589f9a75341', '9d6ef70e00000007911686740fd49eae']):
    devices = []
    msg = json.loads('{"current":1,"rowCount":5000,"search":null,"increase":false,"snKeyword":"","statusKeyword":"all"}')
    msg['typeIDKeyword'] = type_ids
    msg = json.dumps(msg)
    data = {
      'opr': 'list',
      'msg': msg
    }
    res = self.session.post('/iotp/web/v2/DevicesActivation', data)
    res = res['rows']
    for d in res:
      devices.append({ k:d[k] for k in keys})
    return devices
  # list_device_active

  def template(self):
    templates = []
    data = {
      'opr': 'selectCollector',
      'msg': '{}'
    }
    res = self.session.post('/iotp/go/device/template', data)
    res = res.values()
    for t in res:
      if not t: continue
      for tt in t.values():
        for ttt in tt:
          templates.append({
            'templateID': ttt['templateID'],
            'model': ttt['model']
          })
        # in tag
      # tags
    # channel
    return templates
  # template

  def get_network(self, keys=['deviceStat', 'deviceID', 'deviceName', 'groupID', 'groupName', 'GW_DNS_MASTER', 'GW_DNS_SLAVE', 'GW_GATEWAY', 'GW_IP', 'GW_MASK', ]):
    devices = []
    # 
    data = {
      'opr': 'devices_list',
      'msg': '{"current":1,"rowCount":5000,"search":null,"increase":false,"searchBy":"deviceName","keyword":"","grepByStat":"","operator":"getSNMPGateWay","groupID":1}'
    }
    res = self.session.post('/iotp/web/v2/DevicesManagement', data)
    res = res['rows']
    for d in res:
      devices.append({ k:d[k] for k in keys})
    return devices
  # get_network

  def get_lora_gateway_network(self, device_name):
    device_id = self.get_device_id_by_name(device_name)
    data = {
      'opr': 'get_config',
      'msg': ' {"typeID":"9d6ef70e00000007911686740fd49eae","deviceID":"%s","operator":"gatewayConfig"}' % device_id
    }
    res = self.session.post('/iotp/web/v2/DevicesManagement', data)
    return res
  # get_lora_gateway_network

  def config_lora_gateway(self, device_name, gateway_config={}):
    device_id = self.get_device_id_by_name(device_name)
    type_id = self.get_type_id_by_sn(device_id)
    msg = json.loads('{"devices":[{"typeID":"%s","deviceID":"%s"}]}' % (type_id, device_id))
    msg['config'] = gateway_config
    msg = json.dumps(msg)
    data = {
      'opr': 'set_config',
      'msg': msg
    }
    res = self.session.post('/iotp/web/v2/DevicesManagement', data)
    return res
  # config_lora_gateway

#*************************************gateway end*******************************#

#*************************************collector start*******************************#


#*************************************collector end*******************************#

#end class DeviceManager



if __name__ == '__main__':
  dm = DeviceManager('10.156.163.51', 'admin', 'admin')
  # print(dm.list_device('智能插座'))
  # print(dm.delete_device(['GIK0000003']))
  # print(dm.list_device('智能插座'))
  # print(dm.config_lora_gateway('GFG7380303', {'GW_IP': '200.200.157.50'}))
