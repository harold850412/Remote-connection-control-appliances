import pigpio
import time
 
LED_1 = 18
PWM_FREQ = 800
 
pi = pigpio.pi()
 
try:
    while True:
        for i in range(0, 30, 1):
            pi.hardware_PWM(LED_1, PWM_FREQ, i*10000)
            time.sleep(0.1)
        for i in range(29, -1, -1):
            pi.hardware_PWM(LED_1, PWM_FREQ, i*10000)
            time.sleep(0.1)
except KeyboardInterrupt:
    print('停止閃爍')
finally:
    pi.set_mode(LED_1, pigpio.INPUT)