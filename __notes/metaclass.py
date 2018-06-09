
AI = type('AI', (object,), {
  'destroy': lambda x: print('done.')
})

a = AI()

a.destroy()

class AIMetaClass(type):

  def fn(self):
    print('I\'m okay.')

  def __new__(cls, name, bases, attrs):
    attrs['perish'] = fn
    return super(AIMetaClass, cls).__new__(cls, name, bases, attrs)

class AI0():
  __metaclass__ = type(AIMetaClass)


ai0 = AI0()
ai0.perish()