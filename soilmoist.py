from gpiozero import MCP3008
from time import sleep
import sys

try:
    try:
        # Try creating ADC object
        moisture = MCP3008(channel=0)
    except Exception as e:
        print(f"ERROR: Could not initialize MCP3008 on channel 0 → {e}")
        sys.exit(1)

    while True:
        try:
            # Attempt to read analog value
            value = moisture.value      # 0.0 to 1.0
        except Exception as e:
            print(f"ERROR: Failed to read from MCP3008 → {e}")
            sleep(1)
            continue  # skip this loop safely

        # Convert and reverse
        raw = int(value * 1023)
        raw = 1023 - raw

        print(f"Analog value: {raw}")

        # Soil condition interpretation
        try:
            if raw < 300:
                print("Soil is VERY WET")
            elif raw < 700:
                print("Soil is MOIST")
            else:
                print("Soil is DRY")
        except Exception as e:
            print(f"ERROR: Failed to interpret moisture value → {e}")

        print("-------------------------")
        sleep(1)

except KeyboardInterrupt:
    print("\nStopped by user (CTRL+C).")

except Exception as e:
    print(f"Unexpected error: {e}")

finally:
    try:
        moisture.close()
        print("MCP3008 closed safely.")
    except Exception:
        # If object didn't initialize or already closed
        pass
