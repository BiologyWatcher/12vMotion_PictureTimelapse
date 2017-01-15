#setup
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import os
from subprocess import call
import sys
import datetime

SigPin = 31
#OutPin = 32

current_dir = os.path.dirname(os.path.realpath(__file__))
#filename = "/home/pi/Documents/motionpic_temp.txt"
camera = PiCamera()
camera.rotation = 180
repeat = int(open(current_dir + "/config.txt","r").readlines()[0])
wait = int(open(current_dir + "/config.txt","r").readlines()[1])
timein = int(open(current_dir + "/config.txt","r").readlines()[2])

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SigPin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
#    GPIO.setup(OutPin,GPIO.OUT)
#    GPIO.output(OutPin,0)

def loop():
    while True:
        GPIO.wait_for_edge(SigPin, GPIO.RISING)
        recent()
        
def recent():
    localcount = timein
    motion()
    for i in range(0,localcount):
        if i == localcount:
            return 
        else:
            sleep(1)
def motion():
    uppath = current_dir + "/dropbox_uploader.sh upload "
    for i in range(0,repeat):
            date_time = datetime.datetime.strftime(datetime.datetime.now(),"%d-%m-%Y-%H:%M:%S")
            camera.annotate_text=str(i+1) + "/" + str(repeat) + " @ " + date_time
            picfile = '/home/pi/Desktop/Pictures/Security/%s.jpg' % date_time
            camera.capture(picfile)
            try:
                call([uppath + picfile + " " + date_time + ".jpg"],shell=True)
                sleep(wait)
            except:
                print "upload failed"
                destroy()

def destroy():
    GPIO.cleanup()
    sys.exit()

if __name__ == '__main__':
        setup()
        try:
                loop()
        except KeyboardInterrupt:
                destroy()
