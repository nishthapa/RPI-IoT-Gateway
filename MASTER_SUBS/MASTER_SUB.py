import paho.mqtt.client as mqttClient
import time

received = ""
 
def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")
 
def on_message(client, userdata, message):
    print ("Message received: "  + message.payload)
    received = message.payload
    
 
Connected = False   #global variable for the state of the connection

QoS = 2
BROKER_ADDRESS= "localhost"  #Broker address
PORT_NUMBER = 1883                         #Broker port
 
nrf_client = mqttClient.Client("MASTER_SUB")               #create new instance

nrf_client.on_connect= on_connect                      #attach function to callback
nrf_client.on_message= on_message                      #attach function to callback
 
nrf_client.connect(BROKER_ADDRESS, PORT_NUMBER)          #connect to broker
 
nrf_client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
nrf_client.subscribe([("rpi_gateway/nrf", QoS), ("rpi_gateway/esp8266", QoS), ("rpi_gateway/test_topic_1", QoS), ("rpi_gateway/test_topic_2", QoS)])
time.sleep(1)

try:
    while True:
        time.sleep(1)
 
except KeyboardInterrupt:
    print ("exiting")
    nrf_client.disconnect()
    nrf_client.loop_stop()