

def say(name):
  # if @wrap,I can __wrapped__
  def wrapper(func):
    def inner(*args, **kwargs):
      print('%s: "' % name, end='')
      func(*args, **kwargs)
    return inner
  return wrapper

@say('Murus')
def depressed():
  print('te quierro')


depressed()



I_dont_give_a_fuck_about_who_love_me = depressed.__wrapped__

I_dont_give_a_fuck_about_who_love_me()