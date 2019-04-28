#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Author:tom
Version:1.0
Date:201809
后台统一邮件发送模块
'''
import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.utils import parseaddr, formataddr


'''
定义默认变量 可替换值
'''
###邮件变量
send = '*****************'
passwd = '****************'
to_addr = ['*****************']
server = '*****************'
port = 465
###邮件主题部分
remark = u'运维Mail系统'
head = u'运维Mail系统'
text = u'''<p>运维Mail系统</p>
			<p>运维Mail系统</p>
			'''
###发送邮件部分

##格式化邮件地址及中文备注
def Format_Addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

##邮件发送主函数
def Smtp_To(send, passwd, server, port, to_addr, remark, head, text):
	###定义邮件标题内容
	msg = MIMEText(text, 'html', 'utf-8')
	msg['From'] = Format_Addr(u'%s <%s>' % (remark,send))
	msg['To'] = Format_Addr(to_addr)
	msg['Subject'] = Header(u'%s', 'utf-8').encode() % head
	###开始发送邮件
	server = smtplib.SMTP_SSL(server, port)
	server.set_debuglevel(1)
	server.login(send, passwd)
	server.sendmail(send, to_addr, msg.as_string())
	server.quit()

if __name__ == '__main__':
	Smtp_To(send, passwd, server, port, to_addr, remark, head, text)