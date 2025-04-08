from usbrelay import RelayController
import time
import argparse
import sys

# Constants (adjust as needed)
VENDOR_ID = 0x0519
PRODUCT_ID = 0x2018


def main():
    parser = argparse.ArgumentParser(
        description="Control a USB HID relay from the terminal."
    )
    parser.add_argument(
        "action",
        choices=["on1", "off1", "toggle1", "on2", "off2", "toggle2", "on", "off", "test"],
        help="Action to perform.",
    )

    args = parser.parse_args()

    # Instantiate the relay controller
    controller = RelayController()

    # Attempt to open the device
    try:
        controller.open_device()
    except RuntimeError as ex:
        print(f"Error: {ex}")
        sys.exit(1)

    # Perform the requested action
    try:
        if args.action == "on1":
            controller.relay1_on()
            print("Relay 1 turned ON")
        elif args.action == "off1":
            controller.relay1_off()
            print("Relay 1 turned OFF")
        elif args.action == "toggle1":
            controller.relay1_toggle()
            print(
                f"Relay 1 toggled -> now {'ON' if controller.states['relay1'] else 'OFF'}"
            )

        elif args.action == "on2":
            controller.relay2_on()
            print("Relay 2 turned ON")
        elif args.action == "off2":
            controller.relay2_off()
            print("Relay 2 turned OFF")
        elif args.action == "toggle2":
            controller.relay2_toggle()
            print(
                f"Relay 2 toggled -> now {'ON' if controller.states['relay2'] else 'OFF'}"
            )

        elif args.action == "on":
            controller.relay1_toggle()
            controller.relay2_toggle()
            print(
                f"Relay 1 toggled -> now {'ON' if controller.states['relay1'] else 'OFF'}"
            )
            print(
                f"Relay 2 toggled -> now {'ON' if controller.states['relay2'] else 'OFF'}"
            )
        elif args.action == "off":
            controller.relay1_off()
            controller.relay2_off()
            print("Both relays turned OFF")

        elif args.action == "test":
            controller.test_sequence()
            print("Completed test sequence on both relays.")
    finally:
        # Close the device before exiting
        controller.close_device()


if __name__ == "__main__":
    main()
