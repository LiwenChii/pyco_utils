import os
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
    if isinstance(receivers,str):
        receivers = receivers.strip(';').split(';')
    if isinstance(receivers,list):
        receivers = set(receivers)
        receivers = tuple(receivers)
    assert isinstance(receivers,tuple)
    return receivers


def make_attachment(file):
    filedata = file.get('data')
    filename = file.get('filename', 'SPM_REPORT')
    content_type = file.get('contentType', 'application/x-xls')
    sub_type = file.get('subType', 'base16')
    charset = file.get('charset', 'utf-8')
    att = MIMEText(filedata, sub_type, charset)
    att['Content-Type'] = content_type
    att['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)
    return att


def write_mail(content, subject=SUBJECT, files=None):
    msg = MIMEMultipart('related')
    msg['Subject'] = Header(subject, 'utf-8')
    body = MIMEText(content, _subtype='plain', _charset='utf-8')
    msg.attach(body)
    if files is not None and isinstance(files, list):
        for file in files:
            att = make_attachment(file)
            msg.attach(att)
    return msg


def send_email(content,
               subject=SUBJECT,
               host=SEND_HOST,
               port=SEND_PORT,
               sender=SENDER,
               password=PASSWORD,
               receivers=RECEIVERS,
               files=None):
    receivers = format_receivers(receivers)
    msg = write_mail(content, subject, files)
    msg['To'] = ",".join(receivers)
    msg['From'] = sender
    smtp = smtplib.SMTP()
    smtp.connect(host=host, port=port)
    smtp.starttls()
    smtp.login(user=sender, password=password)
    smtp.sendmail(from_addr=sender, to_addrs=receivers, msg=msg.as_string())
    smtp.quit()
