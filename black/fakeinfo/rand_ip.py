from random import randint


def rand_ip(reserved=['114.114.114.114', '8.8.8.8']):

  while True:
    res = []
    i = 4
    while i:
      res.append(str(randint(2, 254)))
      i -= 1
    #while
    res = '.'.join(res)

    if res not in reserved:
      break
    #if break

  #while True
  
#rand ip

def rand_port(reserved=[]):
  while True:
    res = str(randint(1, 65535))
    if res not in reserved:
      break
    #if break
  #while true
  return res
#rand port

def rand_host():
  return (rand_ip(), rand_port())
# host


if __name__ == '__main__':
  rand_host()
  # rand_port()