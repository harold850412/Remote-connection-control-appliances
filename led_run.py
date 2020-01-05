import RPi.GPIO as GPIO
import time

LED_4 = 4 
LED_5 = 17
LED_1 = 18
LED_6 = 27
LED_7 = 22
LED_2 = 24
LED_3 = 25
LED_8 = 5
chan_list = (4,5,17,18,22,24,25,27,12,13)

GPIO.setmode(GPIO.BCM)
GPIO.setup(chan_list, GPIO.OUT)

while True:
    try:
        for i in range(5):
            GPIO.output(LED_1,True)  
            time.sleep(0.1)
            GPIO.output(LED_2,True)
            time.sleep(0.1)
            GPIO.output(LED_3,True)
            time.sleep(0.1)
            GPIO.output(LED_4,True)
            time.sleep(0.1)       
            GPIO.output(LED_5,True)
            time.sleep(0.1)      
            GPIO.output(LED_6,True)
            time.sleep(0.1)
            GPIO.output(LED_7,True)
            time.sleep(0.1)
            GPIO.output(LED_8,True)
            time.sleep(0.1)                            
            GPIO.output(LED_1,False)  
            time.sleep(0.1)
            GPIO.output(LED_2,False)
            time.sleep(0.1)
            GPIO.output(LED_3,False)
            time.sleep(0.1)
            GPIO.output(LED_4,False)
            time.sleep(0.1)       
            GPIO.output(LED_5,False)
            time.sleep(0.1)      
            GPIO.output(LED_6,False)
            time.sleep(0.1)
            GPIO.output(LED_7,False)
            time.sleep(0.1)
            GPIO.output(LED_8,False)
            time.sleep(0.1)           
    finally:
        GPIO.cleanup()
        print('中斷連線')