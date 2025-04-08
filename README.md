## HIDUSBRelay

This is a simple Python script to control a USB relay board using the HID protocol. It allows you to turn on and off relays connected to the board.
The script uses the `hid` library to communicate with the relay board and provides a command-line interface for controlling the relays.

## Requirements
- Python 3.x
- `hid` library (install using `pip install hid`)
- `hidapi` library (install using `pip install hidapi`)

## Installation
1. Clone the repository or download the script.
2. Install the required libraries using pip:
   ```bash
   pip install hid hidapi
   ```
3. Connect your USB relay board to your computer.
4. Run the script using Python:
   ```bash
   python hidusbrelay.py
   ```

5. Use the command-line interface to control the relays.
   ```bash
   python hidusbrelay.py --help
   ```
    This will display the available commands and options for controlling the relays.
    You can use the `--on` and `--off` options to turn on or off specific relays, and the `--status` option to check the status of the relays.

    ```bash
    python hidusbrelay.py --on 1  # Turn on relay 1
    python hidusbrelay.py --off 2  # Turn off relay 2
    python hidusbrelay.py --status  # Check the status of all relays
    ```

## Usage
- To turn on a relay, use the `--on` option followed by the relay number (1-8).
- To turn off a relay, use the `--off` option followed by the relay number (1-8).
- To check the status of all relays, use the `--status` option.
- To check the status of a specific relay, use the `--status` option followed by the relay number (1-8).
- To turn on all relays, use the `--on` option with the value `all`.
- To turn off all relays, use the `--off` option with the value `all`.
