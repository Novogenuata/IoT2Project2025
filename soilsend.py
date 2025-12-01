from gpiozero import MCP3008
from time import sleep
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# ----------------------------
# AWS IoT MQTT settings
# ----------------------------
MQTT_CLIENT = "RaspberryPi5"
MQTT_TOPIC = "sensors/moisture"
MQTT_HOST = "d00635802ilkgd2p7rpxq-ats.iot.us-east-1.amazonaws.com"  # replace with lab-provided endpoint

# Certificates downloaded from AWS IoT
ROOT_CA = "/home/samanthajones/aws_iot_certs/AmazonRootCA1.pem"
PRIVATE_KEY = "/home/samanthajones/aws_iot_certs/private.pem.key"
CERT_FILE = "/home/samanthajones/aws_iot_certs/certificate.pem.crt"

# ----------------------------
# MQTT Client Setup
# ----------------------------
mqtt_client = AWSIoTMQTTClient(MQTT_CLIENT)
mqtt_client.configureEndpoint(MQTT_HOST, 8883)
mqtt_client.configureCredentials(ROOT_CA, PRIVATE_KEY, CERT_FILE)
mqtt_client.configureOfflinePublishQueueing(-1)
mqtt_client.configureDrainingFrequency(2)
mqtt_client.configureConnectDisconnectTimeout(10)
mqtt_client.configureMQTTOperationTimeout(5)
mqtt_client.connect()

# ----------------------------
# Moisture sensor setup
# ----------------------------
moisture = MCP3008(channel=0)

while True:
    value = moisture.value          # 0.0 to 1.0
    raw = int(value * 1023)
    raw = 1023 - raw               # reverse: air = dry, water = wet

    if raw < 300:
        status = "VERY dry"
    elif raw < 700:
        status = "MOIST"
    else:
        status = "WET"

    print(f"Analog value: {raw}")
    print(f"Soil is {status}")
    print("-------------------------")

    # Publish telemetry to AWS IoT
    payload = {
        "moisture": raw,
        "status": status
    }
    mqtt_client.publish(MQTT_TOPIC, json.dumps(payload), 1)

    sleep(5)