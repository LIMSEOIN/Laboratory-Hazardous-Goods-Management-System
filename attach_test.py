import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
smtp = smtplib.SMTP('smtp.gmail.com',587)
smtp.starttls()
smtp.login('test20184468@gmail.com','vdmg znzw cspv yjeo')
msg = MIMEMultipart()
msg['Subject'] = 'dfdfdfdfdf'
msg['To'] = 'gjw04054@naver.com'
text = MIMEText('asdfgda')
msg.attach(text)
file_name = 'test.jpg'
with open(file_name,'rb') as file_FD:
    etcPart = MIMEApplication(file_FD.read())
    etcPart.add_header('Content-Disposition','attachment', filename=file_name)
    msg.attach(etcPart)
    smtp.sendmail('test20184468@gmail.com','gjw04054@naver.com',msg.as_string())
smtp.quit()
