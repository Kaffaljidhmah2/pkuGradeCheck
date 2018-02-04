#coding:utf-8
import re;
import requests;
import os;
import smtplib;
import email;
import time;
import proc;
import random;
from email.mime.text import MIMEText;

### Main Parameters
sender=''
passcode=''
smtpserver=''
receiver=''
pku_username=''
pku_password=''
interval=60
###

iddd='';
for i in range(32):
	iddd+=random.choice('0123456789abcdef');
before=''
r=''
rept=0
state='login'


cookies=dict(PHPSESSID=iddd);

queryurl='http://dean.pku.edu.cn/student/new_grade.php'
authurl='http://dean.pku.edu.cn/student/authenticate.php'
valurl='http://dean.pku.edu.cn/student/yanzheng.php?act=init'

def GenerateTable(eee):
	global before
	global r
	global rept
	global state
	returnstr='';
	pattern=re.compile(r'<tr>.*?</tr>');
	res=pattern.findall(eee);
	for item in res:
		pn2=re.compile(r'<td>(.*?)</td>');
		tab=pn2.findall(item);
		if len(tab)>7:
			returnstr=returnstr+tab[3]+' '+tab[5]+' '+tab[7]+'\n';			
	return returnstr;

def SendEmail(t):
	global before
	global r
	global rept
	global state
	mailserver=smtplib.SMTP(smtpserver,25);
	mailserver.login(sender,passcode);
	mes=MIMEText(t,'plain','utf-8');
	mes['Subject']='您的成绩列表';
	mes['From']=sender;
	mes['To']=receiver;
	mailserver.sendmail(sender,[receiver],mes.as_string());
	mailserver.quit();

def Login():
	global before
	global r
	global rept
	global state
	with open('tmp.gif','wb') as f:
		getv=requests.get(valurl,cookies=cookies)
		f.write(getv.content)
	res=proc.autoget('tmp.gif')
	pay={'sno':pku_username,'password':pku_password,'captcha':res}	
	log=requests.post(authurl,data=pay,cookies=cookies)
	if 'alert' in log.text:
		pass
	else:
		state='query wait'

def Query():
	global before
	global r
	global rept
	global state
	r=requests.get(queryurl,cookies=cookies).text;
	if '绩点' not in r:
		print('no GPA data, timed_out suspected.')
		state='login'
	else:
		if before=='':
			before=r
		elif r==before:
			pass
		else:
			before=r
			state='send email'


while (1):
	try:
		rept+=1
		print(str(rept)+' '+state)
		if state=='login':
			Login()
		elif state=='query wait':
			time.sleep(interval)
			Query()
		elif state=='send email':
			t=GenerateTable(r)
			t+='\nauto sent'
			SendEmail(t)
			state='query wait'
	except KeyboardInterrupt:
		print('KeyboardInterrupted, Terminating...')
		break
	except Exception as e:
		if state=='query wait':
			print('Exception occurred, Connection timed_out suspected.')
			state='login'
