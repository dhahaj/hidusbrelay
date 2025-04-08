import tkinter as tk
from tkinter import ttk

from usbrelay import RelayController

class RelayGUI(tk.Tk):
    """A simple tkinter GUI to interact with the RelayController."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.title("USB Relay Control")
        self.geometry("400x340")
        self.resizable(False, False)

        # Style configuration
        style = ttk.Style()
        style.configure("TButton", padding=5, relief="flat")
        style.configure("TLabelFrame", padding=10)
        style.configure("TLabel", padding=5)
        style.configure("TFrame", padding=5)
        style.configure("TEntry", padding=5)
        

        # Frames
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Device Frame
        device_frame = ttk.LabelFrame(main_frame, text="Device Control")
        device_frame.pack(fill=tk.X, pady=5)

        self.open_button = ttk.Button(
            device_frame, text="Open Device", command=self.open_device
        )
        self.open_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.close_button = ttk.Button(
            device_frame, text="Close Device", command=self.close_device
        )
        self.close_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Relay Frame
        relay_frame = ttk.LabelFrame(main_frame, text="Relays")
        relay_frame.pack(fill=tk.X, pady=5)

        self.r1_on_btn = ttk.Button(
            relay_frame, text="Relay 1 ON", command=self.relay1_on
        )
        self.r1_on_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.r1_off_btn = ttk.Button(
            relay_frame, text="Relay 1 OFF", command=self.relay1_off
        )
        self.r1_off_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.r2_on_btn = ttk.Button(
            relay_frame, text="Relay 2 ON", command=self.relay2_on
        )
        self.r2_on_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.r2_off_btn = ttk.Button(
            relay_frame, text="Relay 2 OFF", command=self.relay2_off
        )
        self.r2_off_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Toggle Frame
        toggle_frame = ttk.LabelFrame(main_frame, text="Toggle")
        toggle_frame.pack(fill=tk.X, pady=5)

        self.toggle_r1_btn = ttk.Button(
            toggle_frame, text="Toggle Relay 1", command=self.toggle_relay1
        )
        self.toggle_r1_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.toggle_r2_btn = ttk.Button(
            toggle_frame, text="Toggle Relay 2", command=self.toggle_relay2
        )
        self.toggle_r2_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Test Frame
        test_frame = ttk.LabelFrame(main_frame, text="Tests")
        test_frame.pack(fill=tk.X, pady=5)

        self.test_btn = ttk.Button(
            test_frame, text="Test (On/Off)", command=self.run_test
        )
        self.test_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.test_seq_btn = ttk.Button(
            test_frame, text="Test Sequence", command=self.run_test_sequence
        )
        self.test_seq_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Status Label
        self.status_label = ttk.Label(main_frame, text="Status: Device Closed")
        self.status_label.pack(fill=tk.X, pady=5)

        # Schedule UI updates
        self.update_ui()

    def open_device(self):
        try:
            self.controller.open_device()
            self.set_status("Device opened successfully.")
        except RuntimeError as ex:
            self.set_status(f"Error: {ex}")

    def close_device(self):
        self.controller.close_device()
        self.set_status("Device closed.")

    def relay1_on(self):
        if not self.is_device_open():
            return
        self.controller.relay1_on()
        self.set_status("Relay 1 turned ON")

    def relay1_off(self):
        if not self.is_device_open():
            return
        self.controller.relay1_off()
        self.set_status("Relay 1 turned OFF")

    def relay2_on(self):
        if not self.is_device_open():
            return
        self.controller.relay2_on()
        self.set_status("Relay 2 turned ON")

    def relay2_off(self):
        if not self.is_device_open():
            return
        self.controller.relay2_off()
        self.set_status("Relay 2 turned OFF")

    def toggle_relay1(self):
        if not self.is_device_open():
            return
        self.controller.relay1_toggle()
        new_state = "ON" if self.controller.states["relay1"] else "OFF"
        self.set_status(f"Relay 1 toggled -> {new_state}")

    def toggle_relay2(self):
        if not self.is_device_open():
            return
        self.controller.relay2_toggle()
        new_state = "ON" if self.controller.states["relay2"] else "OFF"
        self.set_status(f"Relay 2 toggled -> {new_state}")

    def run_test(self):
        if not self.is_device_open():
            return
        self.controller.test()
        self.set_status("Ran test (on/off each relay).")

    def run_test_sequence(self):
        if not self.is_device_open():
            return
        self.controller.test_sequence()
        self.set_status("Ran 15-cycle test sequence on both relays.")

    def is_device_open(self):
        if not self.controller.device or not self.controller.device.is_opened():
            self.set_status("Device is not open.")
            return False
        return True

    def set_status(self, message):
        self.status_label.config(text=f"Status: {message}")

    def update_ui(self):
        """
        Periodically refresh the status display to show real-time relay states.
        """
        device_open = self.controller.device and self.controller.device.is_opened()
        d_status = "Open" if device_open else "Closed"

        r1_state = "ON" if self.controller.states["relay1"] else "OFF"
        r2_state = "ON" if self.controller.states["relay2"] else "OFF"

        self.status_label.config(
            text=f"Status: Device={d_status}, Relay1={r1_state}, Relay2={r2_state}"
        )

        # Update again in 500 ms
        self.after(500, self.update_ui)


if __name__ == "__main__":
    controller = RelayController()
    app = RelayGUI(controller)
    app.mainloop()
