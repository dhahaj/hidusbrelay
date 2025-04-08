import pywinusb.hid as hid
import time
import argparse
import sys

# Constants (adjust as needed)
VENDOR_ID = 0x0519
PRODUCT_ID = 0x2018

CMD_RELAY1_ON = 0xF1
CMD_RELAY1_OFF = 0x01
CMD_RELAY2_ON = 0xF2
CMD_RELAY2_OFF = 0x02


class RelayController:
    """Controls a 2-channel HID USB relay and tracks relay states (software-only)."""

    def __init__(self, vendor_id=VENDOR_ID, product_id=PRODUCT_ID):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.device = None
        self.states = {
            "relay1": False,
            "relay2": False,
        }

    def open_device(self):
        """Find and open the USB relay device."""
        filtered = hid.HidDeviceFilter(
            vendor_id=self.vendor_id, product_id=self.product_id
        )
        devices = filtered.get_devices()
        if not devices:
            raise RuntimeError("USB Relay device not found.")
        self.device = devices[0]
        self.device.open()

    def close_device(self):
        """Close the USB relay device if open."""
        if self.device and self.device.is_opened():
            self.device.close()

    def send_command(self, cmd_val):
        """Send a single command byte in a 9-byte report."""
        out_report = self.device.find_output_reports()[0]
        raw_data = out_report.get_raw_data()
        buffer = [0] * len(raw_data)  # Typically 9 bytes

        # If byte[0] is the report ID (often 0), place commands at index 1:
        buffer[1] = cmd_val

        out_report.set_raw_data(buffer)
        out_report.send()

    def relay1_on(self):
        self.send_command(CMD_RELAY1_ON)
        self.states["relay1"] = True

    def relay1_off(self):
        self.send_command(CMD_RELAY1_OFF)
        self.states["relay1"] = False

    def relay2_on(self):
        self.send_command(CMD_RELAY2_ON)
        self.states["relay2"] = True

    def relay2_off(self):
        self.send_command(CMD_RELAY2_OFF)
        self.states["relay2"] = False

    def relay1_toggle(self):
        if self.states["relay1"]:
            self.relay1_off()
        else:
            self.relay1_on()

    def relay2_toggle(self):
        if self.states["relay2"]:
            self.relay2_off()
        else:
            self.relay2_on()

    def test_sequence(self):
        """Quick demo toggling both relays on/off."""
        self.relay1_on()
        time.sleep(0.5)
        self.relay1_off()
        time.sleep(0.5)
        self.relay2_on()
        time.sleep(0.5)
        self.relay2_off()
        time.sleep(0.5)


def main():
    parser = argparse.ArgumentParser(
        description="Control a USB HID relay from the terminal."
    )
    parser.add_argument(
        "action",
        choices=["on1", "off1", "toggle1", "on2", "off2", "toggle2", "toggle", "test"],
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
        elif args.action == "toggle":
            controller.relay1_toggle()
            controller.relay2_toggle()
            print(
                f"Relay 1 toggled -> now {'ON' if controller.states['relay1'] else 'OFF'}"
            )
            print(
                f"Relay 2 toggled -> now {'ON' if controller.states['relay2'] else 'OFF'}"
            )
        elif args.action == "test":
            controller.test_sequence()
            print("Completed test sequence on both relays.")
    finally:
        # Close the device before exiting
        controller.close_device()


if __name__ == "__main__":
    main()
