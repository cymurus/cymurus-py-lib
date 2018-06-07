import json
import os

def call(interpreter, filepath, bejson=True, *args):
  ret = ''
  cmd = ' '.join([interpreter, filepath] + list(args))
  try:
    ret = os.popen(cmd).readlines()
    ret = ''.join(ret)
  except Exception as e:
    print('Error while executing: %s' % cmd)
    print(e)
  # try
  ret.replace('\'', '"')
  if bejson: ret = json.loads(ret)
  return ret
# call

if __name__ == '__main__':
  print(call('python', 'test.py', False))