import lgpio
import time

RELAY_PIN = 6   

chip = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(chip, RELAY_PIN)

try:
    print("Relay ON")
    lgpio.gpio_write(chip, RELAY_PIN, 0)  
    time.sleep(2)

    print("Relay OFF")
    lgpio.gpio_write(chip, RELAY_PIN, 1)
    time.sleep(2)

finally:
    lgpio.gpiochip_close(chip)