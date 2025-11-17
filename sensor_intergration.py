import lgpio
import time

A = 17
B = 27

chip = lgpio.gpiochip_open(0)

lgpio.gpio_claim_output(chip, A)
lgpio.gpio_claim_output(chip, B)

try:
    print("Motor forward")
    lgpio.gpio_write(chip, A, 1)
    lgpio.gpio_write(chip, B, 0)
    time.sleep(3)

    print("Stop")
    lgpio.gpio_write(chip, A, 0)
    lgpio.gpio_write(chip, B, 0)

finally:
    lgpio.gpiochip_close(chip)