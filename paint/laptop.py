import serial
import paho.mqtt.client as mqtt

ser = serial.Serial('COM3', 38400, timeout=0,
                     parity=serial.PARITY_EVEN, rtscts=1)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def start():
    client.connect("localhost", 1883, 60)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = start


while True:
    s = ser.readline()
    if s:
        print(s)
        client.publish("paint", payload=s)

