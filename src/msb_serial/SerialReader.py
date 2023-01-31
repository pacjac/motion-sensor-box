import re
import serial

from msb_serial.SerialConfig import SerialConfig

# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))

from zmq_base.Publisher import MsbPublisher

class SerialReader:
    def __init__(self):
        self.config = SerialConfig()
        self.publisher = MsbPublisher(connect_to=self.config.xsub_socketstring)
        self.topics = self.config.topic
        self.topics = ["pow", "gen", "rtr", "wnd", "pit"]

        self.pattern = re.compile(r"(\d*\.?\d+)kW\s*(\d*\.?\d+)rpm\s*(\d*\.?\d+)rpm\s*(\d*\.?\d+)m/s\s*(-?\d*\.?\d+)")

        # Assert that device is connected to /dev/serial0
        try:
            with serial.Serial('/dev/serial0', baudrate=9600, timeout = 0.05) as serial_reader:
                pass
        except serial.serialutil.SerialException:
            raise Exception("Serial device not connected to /dev/serial0")



    def read_message_extract_and_publish(self):
        for message in self.read_message():
            data_values = self.extractFloats(message)
            for topic, value in zip(self.topics, data_values):
                print(f"{topic}: {value}")
                self.publisher.send(topic.encode(), value.encode())


    def extractFloats(self, text, isBytes=True):
        # Match regex, return a tuple
        try:
            matching_tuple = re.findall(self.pattern, text)

            # Convert to float
            # return list(map(float, matching_tuple[0]))

            # Do not convert to float, because we send strings anyway
            return matching_tuple[0]
        except Exception as e:
            print(f"Could not find match on {text}")



    def read_message(self):
        with serial.Serial('/dev/serial0', baudrate=9600, timeout = 0.05) as serial_reader:
            while True:
                if serial_reader.in_waiting > 0 :
                    try:
                        message = serial_reader.readline()

                        # Make sure we always work with unicode or bytes, need to decide!
                        yield message.decode('utf-8')
                    except UnicodeError as e:
                        print(f"Could not decode: {text}")
                        print(e)

if __name__ == "__main__":
    reader = SerialReader()
    # Run continuous loop
    reader.read_message_extract_and_publish()
