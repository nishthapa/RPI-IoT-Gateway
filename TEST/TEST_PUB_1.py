import paho.mqtt.client as mqtt
import time
import random

topic_name = "rpi_gateway/"

CLIENT_NAME = "TEST_PUBLISHER_1"
BROKER_ADDRESS = "localhost"
PORT_NUMBER = 1883
TIMEOUT_DURATION = 60
CONNECTED_FLAG = False

DEV_ADDR = 4
DEST_ADDR = 0

message = " MESSAGE FROM TS1 "
final_msg = ""

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        CONNECTED_FLAG = True
        print("Connection Successful! Result Code: "+str(rc))
    else:
        print("Connection Unsuccessfull! Result Code: "+str(rc))
        client.loop_stop()

client = mqtt.Client(CLIENT_NAME)
client.on_connect = on_connect
client.connect(BROKER_ADDRESS, PORT_NUMBER)

time.sleep(2)

while True:
    try:
        topic_name = topic_name + "test_topic_1"
	DEST_ADDR = random.randint(1, 5)
	if DEST_ADDR == 4:
            DEST_ADDR = DEST_ADDR + 1
        final_msg = str(DEV_ADDR) + message + str(DEST_ADDR)
        print("TS1 TX (rpi_gateway/test_topic_1): " + final_msg)
        client.publish(topic_name, final_msg, 2)
        client.loop(2, 10)
        final_msg = ""
        topic_name = "rpi_gateway/";
        time.sleep(1)
        
    except:
            print("INVALID PACKET!")

