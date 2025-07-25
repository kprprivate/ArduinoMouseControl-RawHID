import hid
import time
import struct


class ArduinoMouseController:
    def __init__(self):
        self.device = None
        self.write_format = "report_id"  # Default to report ID format
        self.find_arduino()

    def find_arduino(self):
        """Auto-locate Arduino by trying all HID devices"""
        print("Searching for Arduino...")

        # First, list all HID devices for debugging
        print("\nAll HID devices found:")
        all_devices = hid.enumerate()
        arduino_devices = []

        for i, device_info in enumerate(all_devices):
            print(f"{i}: VID:{device_info['vendor_id']:04X} PID:{device_info['product_id']:04X} "
                  f"Product: {device_info['product_string']} "
                  f"Manufacturer: {device_info['manufacturer_string']} "
                  f"Usage: {device_info.get('usage', 'N/A')} UsagePage: {device_info.get('usage_page', 'N/A')}")

            # Look for Arduino RawHID interface (Usage: 3072, UsagePage: 65472)
            if (device_info['vendor_id'] == 0x2341 and
                    device_info.get('usage_page') == 65472 and
                    device_info.get('usage') == 3072):
                arduino_devices.append((i, device_info))
                print(f"  *** This looks like the RawHID interface!")

        print(f"\nFound {len(arduino_devices)} RawHID Arduino interface(s)")

        # Try Arduino RawHID devices
        for i, device_info in arduino_devices:
            print(
                f"Testing RawHID Arduino device {i}: VID:{device_info['vendor_id']:04X} PID:{device_info['product_id']:04X}")
            try:
                device = hid.device()

                # Try opening by path first (more specific)
                if 'path' in device_info:
                    print(f"  Trying to open by path: {device_info['path']}")
                    device.open_path(device_info['path'])
                else:
                    print(f"  Opening by VID/PID")
                    device.open(device_info['vendor_id'], device_info['product_id'])

                device.set_nonblocking(1)
                print(f"  Opened successfully, sending discovery...")

                # Try different write formats
                formats_to_try = [
                    ([0x00, 0x01] + [0] * 62, "report ID + 63 bytes"),
                ]

                for data, desc in formats_to_try:
                    print(f"    Trying {desc}: {data[:5]}...")
                    result = device.write(data)
                    print(f"    Write result: {result}")

                    if result > 0:
                        print(f"    Success! Waiting for response...")
                        time.sleep(0.5)  # Increased wait time
                        response = device.read(64)
                        print(f"    Response: {response}")

                        if response and b"Arduino_Mouse" in bytes(response):
                            print(f"Found Arduino: {device_info['product_string']}")
                            self.device = device
                            # Arduino strips report ID, so command comes as first byte
                            self.write_format = "report_id"
                            return

                device.close()
                print(f"  No valid response, closed device")

            except Exception as e:
                print(f"  Error: {e}")
                try:
                    device.close()
                except:
                    pass
                continue

        raise Exception("Arduino RawHID interface not found!")

    def move(self, x, y):
        """Move mouse by x, y pixels (relative movement)"""
        if not self.device:
            return

        # Pack x, y as signed 16-bit integers
        x_bytes = struct.pack('<h', x)  # little-endian signed short
        y_bytes = struct.pack('<h', y)

        # Use report ID format: [0x00, command, data, padding...]
        data = [0x00, 0x02, x_bytes[0], x_bytes[1], y_bytes[0], y_bytes[1]] + [0] * 58
        self.device.write(data)

    def click_down(self):
        """Press left mouse button"""
        if self.device:
            data = [0x00, 0x03] + [0] * 62
            self.device.write(data)

    def click_up(self):
        """Release left mouse button"""
        if self.device:
            data = [0x00, 0x04] + [0] * 62
            self.device.write(data)

    def click(self):
        """Single left click"""
        self.click_down()
        time.sleep(0.01)
        self.click_up()

    def wheel(self, delta):
        """Scroll wheel (positive = up, negative = down)"""
        if self.device:
            # Convert to signed byte
            wheel_byte = delta & 0xFF if delta >= 0 else (256 + delta) & 0xFF
            data = [0x00, 0x05, wheel_byte] + [0] * 61
            self.device.write(data)

    def close(self):
        """Close connection"""
        if self.device:
            self.device.close()


# Example usage
if __name__ == "__main__":
    try:
        mouse = ArduinoMouseController()

        print("Testing mouse control...")

        # Move mouse in a small square
        for _ in range(1):
            mouse.move(10, 0)
            time.sleep(0.5)
            mouse.move(0, 10)
            time.sleep(0.5)
            mouse.move(-10, 0)
            time.sleep(0.5)
            mouse.move(0, -10)
            time.sleep(0.5)

        # Test click

        for _ in range(100):
            mouse.click()
            time.sleep(0.001)

        # Test wheel
        mouse.wheel(3)  # Scroll up
        time.sleep(0.5)
        mouse.wheel(-3)  # Scroll down

        mouse.close()

    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to install: pip install hidapi")