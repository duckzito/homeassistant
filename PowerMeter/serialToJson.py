import serial, sys, string, random, time
import http.client
import paho.mqtt.client as mqttClient

def on_connect(client, userdata, flags, rc):
     if rc == 0:
         print("Connected to broker")
         global Connected                #Use global variable
         Connected = True                #Signal connection
     else:
         print("Connection failed")

Connected = False #global variable for the state of the connection

broker_address= "192.168.1.221"
port = 1883
client = mqttClient.Client("PowerMeter")
client.username_pw_set(username="xxxxxx",password="xxxxxxxxxx")
client.on_connect= on_connect
client.connect(broker_address, port=port)
client.loop_start()

while Connected != True:    #Wait for connection
        time.sleep(0.1)


ser = serial.Serial('/dev/ttyACM0', 9600)

while 1:
  time.sleep(1)
  if(ser.in_waiting >0):
    line = ser.readline()
    data = ser.readline().decode().strip().split('  ')
    #b'301.8 VA   1.27 A   0.01 kWh\r\n'

    rawPower = dict(enumerate(data)).get(1, 0).strip()
    rawCurrent = dict(enumerate(data)).get(0,0).strip()
    rawDaily = dict(enumerate(data)).get(2,0).strip()

    current = rawCurrent.split(' ')[0]
    power = rawPower.split(' ')[0]
    daily = rawDaily.split(' ')[0]
    voltage = "230"

    print ('current:' + current)
    print ('voltage: ' + voltage)
    print ('power: ' + power)
    print ('daily power: ' + daily)

    client.publish("home/power","{\"current\":"+current+",\"voltage\":"+voltage+",\"power\":"+power+",\"daily\":"+daily+"}")

    print("data sent..")