import paramiko

class SshSession(object):

  def __init__(self, host, port, username, passwd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, port=int(port), username=username, password=passwd)
    self.conn = ssh
  #init

  def __del__(self):
    if hasattr(self, 'conn'):
      self.conn.close()
  #del

  def exec(self, cmd, stream=''):
    stdin, stdout, stderr = self.conn.exec_command(cmd)
    res = {
      # 'in': stdin.read().decode(),
      'out': stdout.read().decode(),
      'err': stderr.read().decode(),
    }
    if stream:
      if stream in res:
        return res[stream]
      else:
        raise RuntimeError('Error Stream: %s' % stream)
    else:
      return res
  #exec

#class

if __name__ == '__main__':
  s = SshSession('10.56.115.54', 22345, 'admin', 'sangfor123sunwns')
  print(s.exec('ls'))