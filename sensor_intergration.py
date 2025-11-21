import lgpio
import time
import sys

A = 17   # Motor pin A
B = 27   # Motor pin B

chip = None

try:
    # --- Open GPIO chip safely ---
    try:
        chip = lgpio.gpiochip_open(0)
    except Exception as e:
        print(f"ERROR: Could not open gpiochip0 → {e}")
        sys.exit(1)

    # --- Claim motor pins safely ---
    try:
        lgpio.gpio_claim_output(chip, A)
    except Exception as e:
        print(f"ERROR: Could not claim GPIO pin {A} → {e}")
        sys.exit(1)

    try:
        lgpio.gpio_claim_output(chip, B)
    except Exception as e:
        print(f"ERROR: Could not claim GPIO pin {B} → {e}")
        sys.exit(1)

    # --- Ensure pump is OFF at start ---
    print("Pump OFF at start")
    lgpio.gpio_write(chip, A, 0)
    lgpio.gpio_write(chip, B, 0)
    time.sleep(1)

    # --- Motor ON (reversed direction) ---
    print("Pump ON (reversed direction)")
    try:
        lgpio.gpio_write(chip, A, 0)   # reversed
        lgpio.gpio_write(chip, B, 1)
    except Exception as e:
        print(f"ERROR: Could not write motor state → {e}")

    time.sleep(3)

    # --- Stop motor ---
    print("Stopping pump")
    try:
        lgpio.gpio_write(chip, A, 0)
        lgpio.gpio_write(chip, B, 0)
    except Exception as e:
        print(f"ERROR: Could not stop motor → {e}")

except KeyboardInterrupt:
    print("\nStopped by user (CTRL+C).")

finally:
    # --- Safe shutdown ---
    if chip is not None:
        try:
            lgpio.gpio_write(chip, A, 0)
            lgpio.gpio_write(chip, B, 0)
        except:
            pass
        try:
            lgpio.gpiochip_close(chip)
            print("GPIO cleaned up safely.")
        except Exception as e:
            print(f"ERROR during GPIO cleanup → {e}")
