import RPi.GPIO as GPIO
import pigpio

DOOR_1 = 12
DOOR_2 = 13

DOOR_FREQ = 50

p = GPIO.PWM(DOOR_1,DOOR_FREQ)
p.start(15)
p2 = GPIO.PWM(DOOR_2,DOOR_FREQ)
p2.start(5)

while True:
    try:
        print('開門')
        p.ChangeDutyCycle(15)
        p2.ChangeDutyCycle(5)
        time.sleep(0.3)
        p.ChangeDutyCycle(10)
        p2.ChangeDutyCycle(10)
        time.sleep(0.3)
        p.ChangeDutyCycle(5)
        p2.ChangeDutyCycle(15)                        
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()

    try:
        print('關門')
        p.ChangeDutyCycle(5)
        p2.ChangeDutyCycle(15)
        time.sleep(0.3)
        p.ChangeDutyCycle(10)
        p2.ChangeDutyCycle(10)
        time.sleep(0.3)
        p.ChangeDutyCycle(15)
        p2.ChangeDutyCycle(5)     
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup() 