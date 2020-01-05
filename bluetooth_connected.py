import uuid
from bluetooth import *
import RPi.GPIO as GPIO
 
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
        print('等待藍芽 {} 的連線'.format(port))
        client_socket, client_info = server_socket.accept()
        print('接受來自 {} 的連線'.format(client_info))
        try:
            while True:
                data = client_socket.recv(1024).decode().lower()
                if len(data) == 0:
                    break
                if data == 'on':
                    GPIO.output(chan_list, GPIO.HIGH)
                    print('開燈')
                elif data == 'off':
                    GPIO.output(chan_list, GPIO.LOW)
                    print('關燈')
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