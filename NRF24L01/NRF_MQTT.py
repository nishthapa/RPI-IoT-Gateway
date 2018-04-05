import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BCM)

nrf_pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

# set up the mqtt client
mqttc = mqtt.Client("python_pub")

##### DEVICE ADDRESSES #####
NRF = "1"

XBEE = "3"

LoRa = "5"


msg_source_address = "0"
############################

topic_name = "rpi_gateway/"

CLIENT_NAME = "NRF_PUBLISHER"
BROKER_ADDRESS = "localhost"
PORT_NUMBER = 1883
TIMEOUT_DURATION = 60
CONNECTED_FLAG = False

########### NRF UTILITIES ##############
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()
radio.openWritingPipe(nrf_pipes[0])
radio.openReadingPipe(1, nrf_pipes[1])
radio.printDetails()
message = list("GETSTRING")
#######################################

while len(message) < 32:
    message.append(0)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        CONNECTED_FLAG = True
        print("Connection Successful! Result Code: "+str(rc))
    else:
        print("Connection Unsuccessfull! Result Code: "+str(rc))
        client.loop_stop()

#def on_disconnect(client, userdata, rc)
#    print("Client Disconnected! Result Code: "+str(rc))
    
#def on_publish(client, userdata, mid)
#    print("In on_pub callback mid = "+str(mid))
    
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")
    
# The callback for when a PUBLISH message is received from the server.
#def on_message(client, userdata, msg):
#    print(msg.topic+" "+str(msg.payload))
    
client = mqtt.Client(CLIENT_NAME)
client.on_connect = on_connect
#client.on_message = on_message
#client.on_disconnect = on_disconnect
#client.on_publish = on_publish

client.connect(BROKER_ADDRESS, PORT_NUMBER)
#client.loop_start()

#while not client.connected_flag:
#    print("No Client connected...")
#    time.sleep(1)
time.sleep(2)

while True:
    start = time.time()
    radio.write(message)
#DEBUG    print("Sent the message: {}".format(message))
    radio.startListening()

    while not radio.available(0):
        time.sleep(1 / 100)
        if time.time() - start > 2:
            print("Timed out.")
            break

    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
#DEBUG    print("Received: {}".format(receivedMessage))

#DEBUG    print("Translating the receivedMessage into unicode characters")
    string = ""
    for n in receivedMessage:
        # Decode into standard unicode set
        if (n >= 32 and n <= 126):
            string += chr(n)

#DEBUG    print("Publishing: {}".format(string))
#DEBUG        try:
#DEBUG            print(string[0])
#DEBUG        except:
#DEBUG            print("Packet Invalid!")
            
#DEBUG    print(len(string))

############# FORWARDING DATA FROM NRF ##############
    try:
        if string[0] == NRF:
#            if True:
#            print("Message received fromm NRF Node");
#            topic_name = topic_name + "nrf/incoming";
            topic_name = topic_name + "nrf";
#           print("Out received message decodes to: {}".format(string))
            print("Message received from NRF24L01 Node: {}".format(string)+" . . . . . . Publishing it to topic "+topic_name)
#            print("Message received from NRF24L01 Node: {}".format(string)+" . . . . . . Publishing it to topic rpi_gateway/nrf/incoming")
            client.publish(topic_name, string, 1)
#            client.publish("rpi_gateway/nrf/incoming", string, 1)
            client.loop(2, 10)
            topic_name = "rpi_gateway/";
    except:
            print("INVALID PACKET!")
            
#    client.loop_forever()
#####################################################
        
    radio.stopListening()
    time.sleep(1)
