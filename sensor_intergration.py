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

    # --- Motor forward ---
    print("Motor forward")
    try:
        lgpio.gpio_write(chip, A, 1)
        lgpio.gpio_write(chip, B, 0)
    except Exception as e:
        print(f"ERROR: Could not write motor forward state → {e}")

    time.sleep(3)

    # --- Stop motor ---
    print("Stop")
    try:
        lgpio.gpio_write(chip, A, 0)
        lgpio.gpio_write(chip, B, 0)
    except Exception as e:
        print(f"ERROR: Could not stop motor → {e}")

except KeyboardInterrupt:
    print("\nStopped by user (CTRL+C).")

except Exception as e:
    print(f"Unexpected error: {e}")

finally:
    # --- Safe shutdown ---
    if chip is not None:
        try:
            # Ensure motor is off before exiting
            lgpio.gpio_write(chip, A, 0)
            lgpio.gpio_write(chip, B, 0)
        except:
            pass  # worst case, ignore

        try:
            lgpio.gpiochip_close(chip)
            print("GPIO cleaned up safely.")
        except Exception as e:
            print(f"ERROR during GPIO cleanup → {e}")
