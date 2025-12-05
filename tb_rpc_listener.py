# tb_rpc_listener.py
import json
import paho.mqtt.client as mqtt
from actuator import pump_on, fan_on, lights_on, lights_off

TB_HOST = "thingsboard.cloud"
TB_PORT = 1883
TB_TOKEN = "X7Z5U1HQzuwnuf25H13I"   # IMPORTANT

def on_connect(client, userdata, flags, rc):
    print("Connected to ThingsBoard")
    client.subscribe("v1/devices/me/rpc/request/+")
    print("Subscribed to RPC commands")

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    method = payload.get("method")
    params = payload.get("params")

    print("RPC Received:", method, params)

    if method == "water_now":
        pump_on(5)

    elif method == "fan_on":
        fan_on(5)

    elif method == "lights":
        if params == "on":
            lights_on()
        else:
            lights_off()

    # respond to TB
    response_topic = msg.topic.replace("request", "response")
    client.publish(response_topic, json.dumps({"status": "OK"}))

client = mqtt.Client()
client.username_pw_set(TB_TOKEN)

client.on_connect = on_connect
client.on_message = on_message

client.connect(TB_HOST, TB_PORT, 60)
client.loop_forever()