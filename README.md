###### tags: `物聯網`
# 遠端控制系統
[hackMD教學文件](https://hackmd.io/@harold/Hy0rYskgI)
# 專案影片範例網址
[此連結為範例教學影片](https://www.youtube.com/watch?v=aaceCnIRCEU)
# 請先裝好 Raspberry pi 的環境
[安裝教學連結](https://drive.google.com/file/d/1VUlZtWC8SswSpZoP-LXKf7S2FR2fCVGy/view?usp=sharing)
# 1、藍芽連線相關套件安裝
* 先更新系統
```
sudo  apt-get  update
```
* 安裝藍芽功能函式庫
```
sudo apt-get install libbluetooth-dev
```
* 修改 bluetooth 服務
```
sudo nano /etc/systemd/system/dbus-org.bluez.service
```

原先

![](https://i.imgur.com/UWDBsRc.jpg)

修改為

![](https://i.imgur.com/8lVjwso.jpg)

* 重新載入設定檔
```
    sudo systemctl daemon-reload
```
* 重新啟動藍牙服務
```
    sudo systemctl restart bluetooth
```
* 安裝 pybluez 套件
```
    pip install pybluez
```
# 2、手機連接 raspberry pi 來進行操控
### 2-1-1 基礎的開關燈動作
* 在 raspberry pi 和手機裝置兩方都先進行配對

![](https://i.imgur.com/sHpEvw8.jpg)

(Galaxy J7 為已先配對好的手機裝置)

* 連接前先輸入以下指令來回應裝置的掃描訊號
```
    sudo hciconfig hci0 piscan
```
* 在手機端的部分按下建立連線

![](https://i.imgur.com/A7GGJuv.png)

* 接著會看到已經配對好的 raspberry pi

![](https://i.imgur.com/TQfEIci.png)

* 即可開始使用

### 2-1-2 程式碼解說

* 引入 python 套件，並設定要使用 GPIO 控制的腳位編號方式及腳位號碼。如果要多個角位一起設置必須使用群集的方式放入
```
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
```
* 定義藍芽功能需要的控制物件，並且綁定，來等待連線
```
    server_socket=BluetoothSocket(RFCOMM)
    server_socket.bind(("", PORT_ANY))
    server_socket.listen(1)
    port = server_socket.getsockname()[1]
    service_id = str(uuid.uuid4())

    advertise_service(server_socket, "LEDServer",
                      service_id = service_id,
                      service_classes = [service_id, SERIAL_PORT_CLASS],
                      profiles = [SERIAL_PORT_PROFILE])
```
* 當程式啟動後，先等待裝置的連線，並且接收到裝置傳來的參數來進行開燈或關燈的動作，最後將所有的 GPIO 口狀態恢復為初始化，使用`GPIO.cleanup()`來清除空間
```
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
```
### 2-2 用 raspberry pi 控制 LED 來實作跑馬燈
* 設定輸出的腳位，並利用`time.sleep()`來控制熄燈，因此營造出跑馬燈的感覺
```
    LED_4 = 4 
    LED_5 = 17
    LED_1 = 18
    LED_6 = 27
    LED_7 = 22
    LED_2 = 24
    LED_3 = 25
    LED_8 = 5

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
```
### 2-3 利用 raspbeerypi 來控制門的打開和關閉
* 首先要先設定使用 PWM 套件的腳位和其頻率，並透過變數的設置來初始化和啟動它
```
    DOOR_1 = 12
    DOOR_2 = 13

    DOOR_FREQ = 50

    p = GPIO.PWM(DOOR_1,DOOR_FREQ)
    p.start(15)
    p2 = GPIO.PWM(DOOR_2,DOOR_FREQ)
    p2.start(5)
```
* 當接收到的指令式開門時，會先查看要去的位子`p.ChangeDutyCycle(15)`和目前的位子(初始化的位子)`p.start(15)`是否一樣，如果相同則會進行下一個動作，如果不同就會到要去的進行下一動作，最後再將 GPIO 口狀態恢復為初始化
```
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
```

# 3、手機端介面
### 3-1 手機端使用 APP INVENTER 來進行簡單快速開發
* Google App Inventor是一個完全線上開發的Android程式環境，拋棄複雜的程式碼而使用樂高積木式的堆疊法來完成您的Android程式。除此之外它也正式支援樂高NXT機器人，對於Android初學者或是機器人開發者來說是一大福音。因為對於想要用手機控制機器人的使用者而言，他們不大需要太華麗的介 面，只要使用基本元件例如按鈕、文字輸入輸出即可。

* App Inventor的優點

    1. 操作概念很類似Scratch

    2. 全雲端，所有作業都在瀏覽器完成

* 因此使用這個簡單的開發工具目的主要是可以快速的傳值，來使 raspberry pi 端可以快速地接收。並且此工具以拼圖式的方式來進行邏輯設計，是一個快速好上手的開發介面

* 手機應用程式專案檔

    [此為專案檔連結](https://drive.google.com/file/d/1I2XKVXhxDyC-8X8gnfvxF2PnJSlC01tL/view?usp=sharing)
    
* 手機應用程式 apk 安裝檔

    [此為安裝檔連結](https://drive.google.com/file/d/1z8BLL3vNUVtcvC6DxpxNTkoVJdYUH7bZ/view?usp=sharing)
