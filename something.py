import json
import os
import time
import paho.mqtt.client as mqtt
from gpiozero import OutputDevice, LED

# ------------------------------------------------------
# GPIO SETUP (relay modules are usually ACTIVE-LOW)
# ------------------------------------------------------
# initial_value=False keeps relays OFF at startup
pump = OutputDevice(6, active_high=False, initial_value=False)
fanA = OutputDevice(17, active_high=True, initial_value=False)  # always LOW for your setup
fanB = OutputDevice(27, active_high=True, initial_value=False)  # controls ON/OFFinitial_value=False)


# If your grow lights are on a relay:
# light = OutputDevice(22, active_high=False, initial_value=False)

# If your grow lights are simple LEDs:
light = LED(26)
# (If they’re on a relay, use OutputDevice instead, like the others.)


# ------------------------------------------------------
# THINGSBOARD CONFIG
# ------------------------------------------------------
THINGSBOARD_HOST = "thingsboard.cloud"

ACCESS_TOKEN = os.getenv("TB_TOKEN", "X7Z5U1HQzuwnuf25H13I") 


# ------------------------------------------------------
# MQTT CALLBACKS
# ------------------------------------------------------
def on_connect(client, userdata, flags, rc):
    print("Connected to ThingsBoard with code:", rc)
    client.subscribe('v1/devices/me/rpc/request/+')
    print("Subscribed to RPC topic")


def on_message(client, userdata, msg):
    print("Incoming RPC:", msg.payload)
    payload = json.loads(msg.payload)
    method = payload.get("method")


    # --------------------------------------------------
    # PUMP CONTROL
    # --------------------------------------------------
    if method == "pump_on":
        print("Pump ON")
        pump.on()

    elif method == "pump_off":
        print("Pump OFF")
        pump.off()

    elif method == "water_5s":
        print("Watering for 5 seconds...")
        pump.on()
        time.sleep(5)
        pump.off()
        print("Done watering.")


    # --------------------------------------------------
    # FAN CONTROL
    # --------------------------------------------------
    elif method == "fan_on":
        print("Fan ON")
        fanA.off()   # GPIO17 = LOW
        fanB.on()    # GPIO27 = HIGH

    elif method == "fan_off":
        print("Fan OFF")
        fanA.off()   # GPIO17 = LOW
        fanB.off()   # GPIO27 = LOW



    # --------------------------------------------------
    # LIGHT CONTROL
    # --------------------------------------------------
    elif method == "light_on":
        print("Lights ON")
        light.on()

    elif method == "light_off":
        print("Lights OFF")
        light.off()


    else:
        print("Unknown RPC method:", method)

    # Optional: respond to RPC (needed for two-way RPC widgets)
    response = {"status": "OK", "method": method}
    client.publish(msg.topic.replace("request", "response"), json.dumps(response))


# ------------------------------------------------------
# MQTT CONNECTION
# ------------------------------------------------------
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)

print("Using token:", ACCESS_TOKEN)
print("Token length:", len(ACCESS_TOKEN))

client.on_connect = on_connect
client.on_message = on_message

print("Connecting to ThingsBoard at", THINGSBOARD_HOST)
client.connect(THINGSBOARD_HOST, 1883, 60)

print("Waiting for RPC commands...")
client.loop_forever()