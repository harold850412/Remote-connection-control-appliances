import uuid
from bluetooth import *
import RPi.GPIO as GPIO
import pigpio
import time


LED_4 = 4 
LED_5 = 17
LED_1 = 18
LED_6 = 27
LED_7 = 22
LED_2 = 24
LED_3 = 25
LED_8 = 5
DOOR_1 = 12
DOOR_2 = 13
chan_list = (4,5,17,18,22,24,25,27,12,13,19)
PWM_FREQ = 800
DOOR_FREQ = 50

pi = pigpio.pi()

GPIO.setmode(GPIO.BCM)
GPIO.setup(chan_list, GPIO.OUT)
p = GPIO.PWM(DOOR_1,DOOR_FREQ)
p.start(15)
p2 = GPIO.PWM(DOOR_2,DOOR_FREQ)
p2.start(5)
 
server_socket=BluetoothSocket(RFCOMM)
server_socket.bind(("", PORT_ANY))
server_socket.listen(1)
port = server_socket.getsockname()[1]
service_id = str(uuid.uuid4())
 
advertise_service(server_socket, "LEDServer",
                  service_id = service_id,
                  service_classes = [service_id, SERIAL_PORT_CLASS],
                  profiles = [SERIAL_PORT_PROFILE])
 
try:
    print('連接 Bluetooth 來遠端控制 LED')
    while True:
        print('等待藍芽{} 的連線'.format(port))
        client_socket, client_info = server_socket.accept()
        print('接受來自 {} 的連線'.format(client_info))
        try:
            while True :
                data = client_socket.recv(1024).decode().lower()
                if len(data) == 0:
                    break
                if data == 'on':
                    GPIO.output(chan_list, GPIO.HIGH)
                    print('開燈')
                elif data == 'off':
                    GPIO.output(chan_list, GPIO.LOW)
                    print('關燈')
                elif data == 'breathe':
                    
                    try:
                        print('呼吸燈')
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
                elif data == 'run':  
                    print('跑馬燈')
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
                elif data =='open':
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
                elif data =='close':
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
                else:
                    print('未知的指令: {}'.format(data))
        except IOError:
            pass
        client_socket.close()
        print('中斷連線')
except KeyboardInterrupt:
    print('中斷程式')
finally:
    if 'client_socket' in vars():
        client_socket.close()
        server_socket.close()
        GPIO.cleanup()
        print('中斷連線')