import os
import codecs
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


SEND_HOST     = 'localhost'
SEND_PORT     = 587
SUBJECT       = '[AutoEmail]'
PASSWORD      = os.environ.get('EMAIL_PASSWORD')
SENDER        = os.environ.get('EMAIL_SENDER')
RECEIVERS     = 'test@email.com;admin@email.com'


def format_receivers(receivers):
    if isinstance(receivers, str):
        receivers = receivers.strip(';').split(';')
    if isinstance(receivers, list):
        receivers = set(receivers)
        receivers = tuple(receivers)
    if isinstance(receivers, tuple):
        return receivers


def plain_text(content, charset='utf-8'):
    text = codecs.encode(content, encoding=charset).decode(charset)
    body = MIMEText(text, _subtype='plain', _charset=charset)
    return body


def plain_file(file, charset='utf-8'):
    # fs = codecs.open('x.log', 'r+', 'utf-8').read()
    fs = codecs.open(file, encoding=charset).read()
    body = MIMEText(fs, _subtype='plain', _charset=charset)
    return body


def attach_file(file):
    filedata = file.get('data')
    filename = file.get('filename')
    sub_type = file.get('subType', 'base16')
    charset = file.get('charset', 'utf-8')
    content_type = file.get('contentType', 'application/x-xls')

    att = MIMEText(filedata, sub_type, charset)
    att['Content-Type'] = content_type
    att['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)
    return att


# @celery.task
def send_email(content,
               receivers,
               subject='[邮件主题]',
               charset='gbk',
               host=SEND_HOST,
               port=SEND_PORT,
               sender=SENDER,
               password=PASSWORD,
               files=None):
    receivers = format_receivers(receivers)

    # 打包邮件
    msg = MIMEMultipart('related')
    msg['Subject'] = Header(subject, charset)
    msg['To'] = ",".join(receivers)
    msg['From'] = sender

    body = plain_text(content, charset)
    msg.attach(body)

    if files is not None:
        for file in files:
            att = attach_file(file)
            msg.attach(att)

    # 发送邮件
    data = msg.as_string()
    smtp = smtplib.SMTP()
    smtp.connect(host=host, port=port)
    smtp.starttls()
    smtp.login(user=sender, password=password)
    smtp.sendmail(from_addr=sender, to_addrs=receivers, msg=data)
    smtp.quit()
