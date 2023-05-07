import re
import serial
from serial.serialutil import SerialException
import pickle
import sys

from msb_serial.SerialConfig import SerialConfig

# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))

from zmq_base.Publisher import MsbPublisher


class SerialReader:
    def __init__(self):
        self.config = SerialConfig()
        self.publisher = MsbPublisher(connect_to=self.config.xsub_socketstring)
        self.topic = self.config.topic
        self.device = "/dev/ttyUSB0"

        self.topics = ["pow", "gen", "rtr", "wnd", "pit"]
        self.pattern = re.compile(
            r"(\d*\.?\d+)kW\s*(\d*\.?\d+)rpm\s*(\d*\.?\d+)rpm\s*(\d*\.?\d+)m/s\s*(-?\d*\.*\d*)"
        )

        # Assert that device is connected to /dev/serial0
        try:
            with serial.Serial(
                self.device, baudrate=9600, timeout=0.05
            ) as serial_reader:
                print(f"Serial device connected to {self.device}")
        except SerialException:
            print("Serial device not connected to {self.device}")
            sys.exit(1)

    def read_message_extract_and_publish(self):
        to_send = list()
        ptopic = "spy".encode()
        for message in self.read_message():
            data_values = self.extractFloats(message)
            for topic, value in zip(self.topics, data_values):
                # to_send[topic] = value
                to_send.append(value)

            self.publisher.send(ptopic, pickle.dumps(to_send))
            to_send = []

    def extractFloats(self, text) -> str:
        # Match regex, return a tuple
        try:
            matching_tuple = re.findall(self.pattern, text)

            # Convert to float
            # return list(map(float, matching_tuple[0]))

            # Do not convert to float, because we send strings anyway
            return matching_tuple[0]
        except Exception as e:
            print(f"Could not find match on {text}")
            return ""

    def read_message(self):
        # device = "/dev/serial0"
        timeout = 0.05
        baudrate = 9600
        with serial.Serial(
            self.device,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            timeout=timeout,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
        ) as serial_reader:
            # Set RTS to low and DTR to high
            # Required for a read-only connection to Vestas controller
            serial_reader.rts = False
            serial_reader.dtr = True

            buffer = ""

            while True:
                if serial_reader.in_waiting > 0:
                    try:
                        buffer = (
                            buffer
                            + serial_reader.read(serial_reader.in_waiting).decode()
                        )
                        # message = serial_reader.readline()

                        # Make sure we always work with unicode or bytes
                        # need to decide!
                        #     if not buffer.startswith("1:OVERVIEW"):
                        #         buffer = buffer[buffer.index("1:OVERVIEW"):]
                        #         continue
                        #     else:
                        if "1:OVERVIEW" in buffer:
                            message = buffer
                            buffer = ""
                            yield message
                    except UnicodeError as e:
                        # print(f"Could not decode: {message}")
                        # print(e)
                        continue


if __name__ == "__main__":
    reader = SerialReader()
    # Run continuous loop
    # for message in reader.read_message():
    # print(message)
    reader.read_message_extract_and_publish()
