import serial
import paho.mqtt.client as mqtt

ser = serial.Serial('COM7', 38400, timeout=0,
                     parity=serial.PARITY_EVEN, rtscts=1)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("paint")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_start()

while True:
    s = ser.readline()
    if s:
        print(s)
        client.publish("paint", payload=s)
