import pywinusb.hid as hid
import time

# Constants
VENDOR_ID = 0x0519
PRODUCT_ID = 0x2018

CMD_RELAY1_ON = 0xF1
CMD_RELAY1_OFF = 0x01
CMD_RELAY2_ON = 0xF2
CMD_RELAY2_OFF = 0x02


class RelayController:
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
        """Send a single command byte to the relay (with a 9-byte report)."""
        out_report = self.device.find_output_reports()[0]
        raw_data = out_report.get_raw_data()

        # Create a buffer with the same length (often 9 bytes), initialized to 0
        buffer = [0] * len(raw_data)

        # If the device uses the first byte for report ID (commonly 0),
        # the next byte(s) hold the command
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
        """Toggle Relay 1 state."""
        if self.states["relay1"]:
            self.relay1_off()
        else:
            self.relay1_on()

    def relay2_toggle(self):
        """Toggle Relay 2 state."""
        if self.states["relay2"]:
            self.relay2_off()
        else:
            self.relay2_on()

    def toggle_all(self):
        """Toggle both relays."""
        self.relay1_toggle()
        self.relay2_toggle()

    def get_relay_states(self):
        """Return the current states of the relays."""
        return self.states


    def test(self):
        """Demonstrate toggling both relays on/off."""
        if not self.device or not self.device.is_opened():
            self.open_device()

        self.relay1_on()
        time.sleep(0.5)
        self.relay1_off()
        time.sleep(0.5)
        self.relay2_on()
        time.sleep(0.5)
        self.relay2_off()
        time.sleep(0.5)

    def test_sequence(self):
        """Test sequence for both relays."""
        if not self.device or not self.device.is_opened():
            self.open_device()

        for _ in range(15):
            self.relay1_on()
            time.sleep(0.1)
            self.relay1_off()
            time.sleep(0.1)
            self.relay2_on()
            time.sleep(0.1)
            self.relay2_off()
            time.sleep(0.1)

if __name__ == "__main__":
    try:
        controller = RelayController()
        while True:
            controller.test()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        controller.close_device()
