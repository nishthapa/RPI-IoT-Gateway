import paho.mqtt.client as mqtt
import time

topic_name = "rpi_gateway/"

CLIENT_NAME = "TEST_PUBLISHER_1"
BROKER_ADDRESS = "localhost"
PORT_NUMBER = 1883
TIMEOUT_DURATION = 60
CONNECTED_FLAG = False

message = "XX Hello_World YY"

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
        print("Publishing "+message+" to topic "+topic_name)
        client.publish(topic_name, message, 2)
        client.loop(2, 10)
        topic_name = "rpi_gateway/";
        time.sleep(1)
    except:
            print("INVALID PACKET!")

