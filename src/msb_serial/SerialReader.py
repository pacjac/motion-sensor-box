import re
import serial

from msb_serial.SerialConfig import SerialConfig

# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))

from zmq_base.Publisher import MsbPublisher

class SerialReader:
    def __init__(self):
        self.config = SerialConfig()
        self.publisher = MsbPublisher(connect_to=self.config.xpub_socketstring)
        self.topic = self.config.topic

        # Assert that device is connected to /dev/serial0
        try:
            with serial.Serial('/dev/serial0', baudrate=9600, timeout = 0.05) as serial_reader:
                pass
        except serial.serialutil.SerialException:
            raise Exception("Serial device not connected to /dev/serial0")



    def read_message_extract_and_publish(self):
        for message in self.read_message():
            data_values = self.extractFloats(message)
            self.publisher.send(self.topic, data_values)


    def extractFloats(self, text, isBytes=True):
        if isBytes:
            data_values = [
                float(match.group(0).decode("utf-8"))
                for match in re.finditer(b"-*\d*\.\d+", text)
            ]
        else:
            data_values = [float(match.group(0)) for match in re.finditer("-*\d*\.\d+", text)]

        return data_values


    def read_message(self):
        with serial.Serial('/dev/serial0', baudrate=9600, timeout = 0.05) as serial_reader:
            while True:
                if serial_reader.in_waiting > 0 :
                    message = serial_reader.readline()
                    if isinstance(message, bytes):
                        message = message.decode('utf-8')
                    yield message

if __name__ == "__main__":
    reader = SerialReader()
    # Run continuous loop
    reader.read_message_extract_and_publish()
