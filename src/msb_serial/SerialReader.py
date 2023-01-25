import re
import sys, os

from SerialConfig import SerialConfig

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from zmq_base.Publisher import Publisher

class SerialReader:
    def __init__(self, config_override={}):
        self.config = SerialConfig(override=config_override)
        self.publisher = Publisher()

    def extractFloats(self, text, isBytes=True):
        if isBytes:
            data_values = [
                float(match.group(0).decode("utf-8"))
                for match in re.finditer(b"-*\d*\.\d+", text)
            ]
        else:
            data_values = [float(match.group(0)) for match in re.finditer("-*\d*\.\d+", text)]

        return data_values
