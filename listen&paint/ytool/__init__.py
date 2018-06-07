from datetime import datetime

'''
  时间类工具
'''

# 返回当前时间
def now():
  return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# now

def now_stamp():
  return datetime.now().strftime('%Y%m%d%H%M%S')
# now

'''
  集合类工具
'''

# 二维字典增加元素
def dict_add(m, key_1, key_2, val):
  if key_1 in m:
    m[key_1].update({key_2: val})
  else:
    m.update({key_1:{key_2: val}})
#dict_add