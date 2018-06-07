# python 自带库
from collections import deque
from datetime import datetime
import os

# 自己写的
from ytool import now_stamp

# 第三方库
import pygal

'''
  读取监听信息的结果
  cmd_name 读取的命令名称，即文件目录名
  mapper 对于读取到的数据预处理函数
  time_start 指定开始时间，格式如：20180423142800
  time_end 指定结束时间
  返回格式：[
    'x_labels': [],#横坐标，时间
    'data': {
      'cmd_name': []
    },#内容
  ]
'''
def get_one_sys_info(cmd_name, mapper=None, time_start='', time_end='99999999999999'):
  x_labels = []
  data = {}
  cmd_data = deque()
  # 遍历目录
  path = './data/%s' % cmd_name
  if not os.path.exists(path): 
    raise RuntimeError('No Such Directory.')
  # path not exist
  ress = os.listdir(path)
  for res in ress:

    if res < time_start or res > time_end:
      continue
    # out of time range

    x_labels.append(res)

    filename = './data/%s/%s' % (cmd_name, res)
    tmp = read(filename)

    if mapper:
      tmp = mapper(tmp)
    # mapper

    cmd_data.append(tmp)
  #for res
  data[cmd_name] = cmd_data
  return {
    'x_labels': [datetime.strftime(datetime.strptime(t, '%Y%m%d%H%M%S'), '%H:%M') for t in x_labels],
    'data': data,
  }
# get sys info


'''
  读取文件信息
'''
def read(filename):
  data = ''
  f = open(filename, 'r')

  if 0==os.path.getsize(filename):
    return data
  # 0 size

  data = f.read()
  f.close()
  return data
# read

'''
  绘制曲线图
  title 曲线图名称
  x_labels 曲线图横坐标字符串
  data get_one_sys_info返回对象的数组
  out_img 输出图象文件名
'''
def paint_line_chart(title='Untitled', x_labels=[], data=[], out_img=''):
  # 参数校验
  if not data:
    raise RuntimeError('Chart data cannot be empty.')
  if not x_labels:
    raise RuntimeError('Chart axis-x cannot be empty.')
  if not out_img:
    out_img = now_stamp() + '.svg'
  # 画图
  chart = pygal.Line()
  chart.title = title
  chart.x_labels = x_labels
  for _data in data:
    for cmd_name in _data:
      cmd_data = _data[cmd_name]
      chart.add(cmd_name, cmd_data)
    # for cmd_data
  # for data
  chart.render_to_file(out_img)
# line chart

if __name__ == '__main__':
  cpu_info = get_one_sys_info('cpu%', float)
  mem_info = get_one_sys_info('mem%', float)
  paint_line_chart(
    'CPU/MEM', 
    cpu_info['x_labels'], 
    [
      cpu_info['data'], 
      mem_info['data']
    ], 
    # './test.svg'
    ''
  )
#ifmain