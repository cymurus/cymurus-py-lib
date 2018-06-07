# -*- coding: utf-8 -*-

# python 自带库
from threading import Thread
from sys import maxsize as MAXINT
from datetime import datetime
import time
import os
import re

# 第三方库
# import pygal

# 本地开发的库
from ytool.session.sshsession import SshSession
from ytool import now

'''
  每隔 interval 秒，执行一次 cmd，并记录到 out_dir 下的文件中
  cmd 监听的命令
  interval 监听的间隔，单位：s，默认 60
  sess ssh会话
  out_dir 输出目录
  mapper 如果要对 cmd 执行结果进行特殊处理时可以传入一个函数作为该参数
'''
def listen(cmd, interval=60, sess=None, out_dir='', mapper=None):
  # 参数校验
  if interval not in range(1, MAXINT):
    raise RuntimeError('interval should be an interger in [1, %s].' % str(MAXINT))
  if not sess:
    raise RuntimeError('SSH Session must be given.')
  if not out_dir:
    out_dir = now()
  # 监听循环
  while True:
    # 执行命令获取输出
    data = sess.exec(cmd)
    err = data['err']
    out = data['out']
    if err :
      if not out:
      # 只有错误流
        raise RuntimeError('Error exec %s, msg:%s' % (cmd, err))
      else:
        pass
      # if out
    # if err
    if mapper:
      out = mapper(out)
    # if mapper

    # 记录到文件
    dtime = datetime.now().strftime('%Y%m%d%H%M%S')
    record(out, out_dir, dtime)

    print(dtime, out_dir, out)

    time.sleep(interval)
  # while true
# listen

'''
  将数据记录到文件
'''
def record(data, path, filename):
  if not os.path.exists(path): 
    os.makedirs(path) 
  # path not exist
  filepath = '/'.join([path, filename])
  f = open(filepath, 'w')
  f.write(data)
  f.close()
# record

if __name__ == '__main__':
  host = '10.156.161.45'
  port = 22345
  username = 'admin'
  passwd = 'sangfor123sunwns'

  # windows 下不支持的文件名称
  # invalid_win_fname_reg = re.compile('[\/:*"<>|"]')
  # validate = lambda s: invalid_win_fname_reg.sub('_', s)

  # 需要监听记录的命令字典
  # cmd_name: cmd_str
  cmds = {
    'CPU%': "top -b -n 1 | grep '^Cpu0' | head -n 1 | awk '{print $3}'",
    'MEM%': "free | grep 'Mem' | awk '{print ($3/$2)*100}'",
  }

  sess = SshSession(host, port, username, passwd)

  print('start: %s' % now())
  ts = []
  for cmd_name in cmds:
    t = Thread(
      target=listen,
      args=(
        cmds[cmd_name], 
        60 * 15, sess, 
        './data/%s' % cmd_name, 
        lambda s: re.sub('[^\d.]', '', s)
      )
    )
    ts.append(t)
    t.start()
  # for cmds

  print('to stop, press CTRL + PAUSE/BREAK')

  # 想停止但是停不下来
  # try:
  #   while True: pass
  # except KeyboardInterrupt as ki:
  #   print(ki)
  #   for t in ts: t.stop()
  #   print('end: %s' % now())
  # # try
#  ifmain