# -*- coding: utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


class MailSender(object):

  def __init__(self, host, port, username='', password='', use_ssl=False):
    self.host = host
    self.port = port
    if use_ssl:
      self.conn = smtplib.SMTP_SSL(host, int(port))
    else:
      self.conn = smtplib.SMTP(host, int(port))
    self.conn.set_debuglevel(1)
    if username and password:
      self.login(username, password)
    # user
  # init

  # i do not know why I cannot del self.conn
  # def __del__(self):
  #   if hasattr(self, 'conn'):
  #     self.conn.quit()
  #   # 
  # # del

  def login(self, username, password):
    # TODO login another user
    # self.conn.ehlo(self.host)
    self.username = username
    self.password = password
    self.conn.login(username, password)
  # login

  def send_mail(self, from_addr, to_addr, msg):

    # def _format_addr(s):
    #   name, addr = parseaddr(s)
    #   return formataddr((
    #     Header(name, 'utf-8').encode(), 
    #     addr.encode('utf-8')
    #   ))
    # # format addr

    # msg['From'] = _format_addr(from_addr)
    # msg['To'] = _format_addr(to_addr)
    msg['From'] = from_addr
    msg['To'] = to_addr
    if isinstance(to_addr, list):
      send_to = to_addr
    else:
      send_to = [to_addr]
    # to addrs
    self.conn.sendmail(from_addr, send_to, msg.as_string())
  # send mail

  @staticmethod
  def make_message(title='Untitled', body='', mime_type='plain', encoding='utf-8'):
    msg = MIMEText(body, mime_type, encoding)
    msg['Subject'] = Header(title, encoding)
    return msg
  # make message

# MailSender

if __name__ == '__main__':
  # ms = MailSender('smtp.qq.com', 465)
  # ms.login('cymurus@qq.com', '')
  # msg = ms.make_message('Test title', 'Test body')
  # ms.send_mail('cymurus@qq.com', 'cymurus@qq.com', msg)