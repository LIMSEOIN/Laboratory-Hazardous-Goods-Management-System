import smtplib
from email.mime.text import MIMEText

smtp = smtplib.SMTP('smtp.gmail.com',587)
smtp.starttls()
smtp.login('test20184468@gmail.com','vdmg znzw cspv yjeo')

msg = MIMEText('fdkfj')
msg['Subject'] = 'dfdfdfdfdf'
msg['To'] = 'gjw04054@naver.com'
smtp.sendmail('test20184468@gmail.com','gjw04054@naver.com',msg.as_string())

smtp.quit()
