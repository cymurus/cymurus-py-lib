# coding=utf-8

import json

# mysql -Ns -e "select type_id, type_name, details, states from global.device_type;" > device_db
db_file = open('./device_db', 'r', encoding='UTF-8')

lines = db_file.readlines()

tmp = [line.split('\t') for line in lines]

DEVICE_INFO = {}

for d in tmp:
  details = json.loads(d[2])
  states = json.loads(d[3])
  DEVICE_INFO[details['displayName']] = {
    'type_id': d[0],
    'type_name': d[1],
    'sn': [st['idCode'] for st in [st for st in details['subTypes'] if 'idCode' in st]],
  }