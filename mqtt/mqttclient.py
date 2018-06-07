import paho.mqtt.client as mqtt
# import ssl

class MqttClient(object):

  def __init__(self, host, port, username='', password='', keepalive=60, ca_certs=''):
    self.client = mqtt.Client()
    if username and password:
      self.client.username_pw_set(username, password=None)
    # user
    self.client.connect(host, int(port), keepalive)
    self.topics = []
    if ca_certs:
      self.tls_set()
  # init

  def tls_set(self):
    if not self.client:
      return
    if not self.ca_certs:
      return
    self.client.tls_set(
      ca_certs=self.ca_certs, 
      certfile=None, 
      keyfile=None, 
      cert_reqs=ssl.CERT_REQUIRED,
      tls_version=ssl.PROTOCOL_TLSv1_2, 
      ciphers=None
    )
  # tls_set

  def set_callback(self, cbname, cb):
    slots = [
      'on_message',
      'on_connect',
      'on_log',
      'on_disconnect',
      'on_publish',
      'on_subscribe',
      'on_unsubscribe',
      'on_message_print',
    ]
    if cbname not in slots:
      raise RuntimeError('Unsupported callback: %s' % cbname)
    # not slots
    setattr(self.client, cbname, cb)
  # set callback

  def subscribe(self, topic, qos=0):
    # subscribe(topic, qos=0)
    if topic not in self.topics:
      self.client.subscribe(topic, qos)
      self.topics.append(topic)
    else:
      pass
    # subed
  # subscribe

  def publish(self, topic, payload=None, qos=0, retain=False):
    # publish(topic, payload=None, qos=0, retain=False)
    self.client.publish(topic, payload, qos, retain)
  # publish

  def unsubscribe(self, topic):
    if topic in self.topics:
      self.client.unsubscribe(topic)
      self.topics.remove(topic)
    else:
      pass
    # subed
  # unsubscribe()

  def disconnect(self):
    self.client.disconnect()
    self.topics = []
  # disconnect

  def reconnect(self):
    self.client.reconnect()
    for topic in topics:
      self.client.subscribe(topic)
    # topics resub
  # disconnect

  def list_topics(self, echo=False):
    if echo:
      print(self.topics)
    # echo
    return self.topics
  # list topics

# MqttClient

if __name__ == '__main__':
  mc = MqttClient('iot.eclipse.org', 1883)
  mc.subscribe('topic/sub')
  def on_message(client, userdata, msg):
    print("TOPIC:%s PAYLOAD:%s" % (msg.topic, str(msg.payload)))
  mc.set_callback('on_message', on_message)