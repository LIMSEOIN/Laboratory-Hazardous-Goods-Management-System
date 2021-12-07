import picamera
import RPi.GPIO as GPIO
import time
import datetime
import smtplib
import os

from email.mime.text import MIMEText #hangul(the attached file convert base64)
from email.mime.multipart import MIMEMultipart #(make text content)
from email.mime.application import MIMEApplication #(the image file convert base64)
from twilio.rest import Client

source_mail = '???'

#for sms
account_sid = '???'
auth_token = '???'


#camera
camera = picamera.PiCamera()
camera.resolution = (1048,768) #camera image quality
file_path = '/home/pi/'

#mail
client = Client(account_sid, auth_token)


def save_cam():
    #now = datetime.datetime.now()
    now = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    file_name = now
    #file_name = 'camera'
    time.sleep(2)
    camera.capture(file_name + '.jpg')
    test_path = '/home/pi/'+file_name+'.jpg'
    camera.close()
    return test_path;
        

def send_mail(title,message,destination,send_file):
    smtp = smtplib.SMTP('smtp.gmail.com',587)
    smtp.starttls()
    smtp.login(source_mail,'???')
    msg = MIMEMultipart()
    msg['Subject'] = title
    msg['To'] = destination
    text = MIMEText(message)
    msg.attach(text)
    
    with open(send_file,'rb') as file_FD:
        etcPart = MIMEApplication(file_FD.read())
        #mime header attached file addition
        etcPart.add_header('Content-Disposition','attachment', filename=send_file)
        msg.attach(etcPart)
        smtp.sendmail(source_mail,destination,msg.as_string())
        smtp.quit()

def send_sms(msg,phone):
    message = client.messages.create(
        body=msg,
        from_='???',
        to='???'
        )

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led_R = 4
buzzer = 18
trig = 23
echo = 24


GPIO.setup(led_R, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

def measure():
    GPIO.output(trig, True)
    time.sleep(0.1)
    GPIO.output(trig, False)
    start = time.time()

    while GPIO.input(echo)==0:
        start = time.time()
    while GPIO.input(echo)==1:
        stop = time.time()

    check_time = stop - start
    distance = check_time * 17000
    distance = round(distance,2)

    return distance

    
try:
    GPIO.output(led_R, 0)
    GPIO.output(buzzer,0)
    while True:
        distance = measure()
        #print("distance : %.1f",distance)

        if distance <= 10:
            print("Detected")
            GPIO.output(led_R,1)
            GPIO.output(buzzer, 1)
            send_file = save_cam()
            cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            title = '경고: 침입자가 발생했습니다!!'
            send_mail(title, cur_time+'에 촬영되었습니다.','???',send_file)
            send_sms(title,'???')
            time.sleep(1)
            GPIO.output(led_R,0)
            GPIO.output(buzzer,0)
                

        else:
            GPIO.output(buzzer,0)
            time.sleep(0.3)
            GPIO.output(led_R, 0)
                                     
        

except KeyboardInterrupt:
    GPIO.cleanup()
    
