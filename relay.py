import lgpio
import time
import sys

RELAY_PIN = 6   # GPIO pin for relay

chip = None

try:
    # Try opening the GPIO chip
    try:
        chip = lgpio.gpiochip_open(0)
    except Exception as e:
        print(f"ERROR: Could not open GPIO chip 0 → {e}")
        sys.exit(1)

    # Try to claim the pin
    try:
        lgpio.gpio_claim_output(chip, RELAY_PIN)
    except Exception as e:
        print(f"ERROR: Could not claim GPIO pin {RELAY_PIN} → {e}")
        sys.exit(1)

    print("Relay ON")
    try:
        lgpio.gpio_write(chip, RELAY_PIN, 0)  # Active LOW relay
    except Exception as e:
        print(f"ERROR writing to relay: {e}")

    time.sleep(2)

    print("Relay OFF")
    try:
        lgpio.gpio_write(chip, RELAY_PIN, 1)
    except Exception as e:
        print(f"ERROR writing to relay: {e}")

    time.sleep(2)

except KeyboardInterrupt:
    print("\nStopped by user.")

except Exception as e:
    print(f"Unexpected error: {e}")

finally:
    if chip is not None:
        try:
            lgpio.gpiochip_close(chip)
            print("GPIO cleaned up safely.")
        except Exception as e:
            print(f"ERROR during cleanup: {e}")
