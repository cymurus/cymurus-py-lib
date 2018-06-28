# coding=utf-8

import json


# mysql -Ns -e "select type_id, type_name, details, states from global.device_type;" > device_db
def get_device_info(file='./device_db'):

  db_file = open(file, 'r', encoding='UTF-8')

  lines = db_file.readlines()

  tmp = [line.split('\t') for line in lines]

  device_info = {}

  for d in tmp:
    details = json.loads(d[2])
    states = json.loads(d[3])
    device_info[details['displayName']] = {
      'type_id': d[0],
      'type_name': d[1],
      'sn': [st['idCode'] for st in [st for st in details['subTypes'] if 'idCode' in st]],
    }

  return device_info
# device_info


def get_interfacetp():
  interfacetp = {
    'CI': 1,
    'VI': 2,
    'DIDry': 3,
    'DIWet': 0,
    'modbus': 4,
    'RS485': 5,
    'SNMP': 6,
    'DO': 7,
  }
  return interfacetp
