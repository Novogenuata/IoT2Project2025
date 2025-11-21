from gpiozero import MCP3008
from time import sleep

moisture = MCP3008(channel=0)

while True:
    value = moisture.value          # 0.0 to 1.0
    raw = int(value * 1023)

    raw = 1023 - raw   # reverse output so air = dry, water = wet

    print(f"Analog value: {raw}")

    if raw < 300:
        print("Soil is VERY dry")
    elif raw < 700:
        print("Soil is MOIST")
    else:
        print("Soil is wet")

    print("-------------------------")
    sleep(1)
