from random import randint, choice

def rand_phone(reserved=[]):
  prefix = ['13', '15', '18']
  while True:
    res = choice(prefix)
    res += str(randint(100000000, 999999999))

    if res not in reserved:
      break
    #if break
  #while true

  print('generate a phone number: %s' % res)
  return res
#rand phone no.

if __name__ == '__main__':
  rand_phoneno()