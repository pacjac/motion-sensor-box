import re
import sys, os
import serial

from msb_serial.SerialConfig import SerialConfig

# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))

from zmq_base.Publisher import MsbPublisher

class SerialReader:
    def __init__(self, config_override={}):
        self.config = SerialConfig()
        self.publisher = MsbPublisher()
        self.topic = self.config.topic


    def extractFloats(self, text, isBytes=True):
        if isBytes:
            data_values = [
                float(match.group(0).decode("utf-8"))
                for match in re.finditer(b"-*\d*\.\d+", text)
            ]
        else:
            data_values = [float(match.group(0)) for match in re.finditer("-*\d*\.\d+", text)]

        return data_values


    def read_message():
        with serial.Serial('/dev/serial0', baudrate=9600, timeout = 0.05) as serial_reader:
            while True:
                if serial_reader.in_waiting > 0 :
                    message = serial_reader.readline()
                    yield message.decode('utf-8')

if __name__ == "__main__":
    reader = SerialReader()
