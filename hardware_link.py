import serial
import random
import time


class HardwareConnector:
    def __init__(self, port='COM3', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.connection = None
        self._connect()

    def _connect(self):
        try:
            self.connection = serial.Serial(self.port, self.baudrate, timeout=1)
        except serial.SerialException:
            # Silent fallback to mock data for development
            self.connection = None

    def read_live_power(self) -> float:
        """Reads live wattage from sensor, or generates realistic mock data."""
        if self.connection and self.connection.is_open:
            try:
                line = self.connection.readline().decode('utf-8').strip()
                if line:
                    return float(line)
            except (ValueError, serial.SerialException):
                pass

        # Fallback: Simulate live power between 100W and 3000W
        return round(random.uniform(100.0, 3000.0), 2)