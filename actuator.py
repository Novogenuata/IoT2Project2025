# actuators.py
import time
import lgpio
from gpiozero import LED

# --------------------------
# GPIO Configuration
# --------------------------

# Pump relay (active LOW)
PUMP_PIN = 6

# Fan pins (motor / H-bridge)
FAN_A = 17
FAN_B = 27

# Grow lights (LED)
LIGHT_PIN = 26
lights = LED(LIGHT_PIN)

# Open GPIO chip
chip = lgpio.gpiochip_open(0)

# Claim pins
lgpio.gpio_claim_output(chip, PUMP_PIN)
lgpio.gpio_claim_output(chip, FAN_A)
lgpio.gpio_claim_output(chip, FAN_B)

# Ensure OFF states
lgpio.gpio_write(chip, PUMP_PIN, 1)
lgpio.gpio_write(chip, FAN_A, 0)
lgpio.gpio_write(chip, FAN_B, 0)


# --------------------------
# Pump Control
# --------------------------

def pump_on(seconds=5):
    print(f"Pump ON for {seconds} seconds")
    lgpio.gpio_write(chip, PUMP_PIN, 0)  # ACTIVE LOW
    time.sleep(seconds)
    lgpio.gpio_write(chip, PUMP_PIN, 1)
    print("Pump OFF")


# --------------------------
# Fan Control
# --------------------------

def fan_on(seconds=5):
    print(f"Fan ON for {seconds} seconds")
    lgpio.gpio_write(chip, FAN_A, 0)
    lgpio.gpio_write(chip, FAN_B, 1)
    time.sleep(seconds)
    lgpio.gpio_write(chip, FAN_A, 0)
    lgpio.gpio_write(chip, FAN_B, 0)
    print("Fan OFF")


# --------------------------
# Light Control
# --------------------------

def lights_on():
    print("Lights ON")
    lights.on()

def lights_off():
    print("Lights OFF")
    lights.off()