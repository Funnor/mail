#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import filetype
import smtplib

from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parsedate, formataddr

class Mail(object):

    def __init__(self, email, pwd):
        '''send email info:'''
        self.email = email
        self.pwd = pwd
    
    def get_file_info(self, file):
        '''
        file: file path
        return: filename, file's extension, file's mime 
        '''
        f = filetype.guess(file)
        if f is None:
            return None, None, None
        return os.path.basename(file), f.extension, f.mime

    def get_attach(self, file):
        if not os.path.exists(file):
            return None
        with open(file, 'rb') as f:
            file_name, file_extensino, file_mime = self.get_file_info(file)
            # # 设置附件的MIME和文件名
            mime = MIMEBase(file_mime, file_extensino, filename=file_name)
            # 加上必要的头信息
            mime.add_header('Content-Disposition', 'attachment', filename=file_name)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            # 用Base64编码:
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
        return mime

    def sen_mail(self, toemails, msg, subject, files=[]):
        print(','.join(toemails))
        # msg = MIMEText(msg, 'plain', 'utf-8')
        mail_msg = MIMEMultipart()
        mail_msg['From'] = self.email
        mail_msg['To'] = ','.join(toemails)
        mail_msg['Subject'] = Header(subject, 'utf-8').encode()
        mail_msg.attach(MIMEText(msg, 'plain', 'utf-8'))

        # 附件
        for file in files:
            mime = self.get_attach(file)
            if mime:
                mail_msg.attach(mime)

        server = smtplib.SMTP('smtp.163.com', 25)
        server.set_debuglevel(1)
        server.login(self.email, self.pwd)
        print('send to user: %s' % toemails)
        server.sendmail(self.email, toemails, mail_msg.as_string())
        server.quit()
        print('send over')


if __name__ == "__main__":
    mail = Mail('axx@163.com', 'xxx')    
    msg = ''''''

    mail.sen_mail(
        ['xxx@qq.com'], 
        msg, 
        'd', 
        [r'G:xxx\psb.jpg']
    )
