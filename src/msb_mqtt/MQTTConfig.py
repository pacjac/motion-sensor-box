import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from msb_config.MSBConfig import MSBConfig

class MQTTConfig(MSBConfig):
    def __init__(self, subconf = "msb-mqtt", override=dict()):
        super().__init__()
        self.set_default_attributes()

        if override:
            self.load_override(override)
        else:
            self._load_conf(subconf=subconf)

    def set_default_attributes(self):
        self.user = ""
        self.passwd = ""
        self.mqtt_broker = "localhost"
        self.mqtt_port = 1883
        self.topics = []
        self.measurement = "test"
        self.qos = 2
        self.ssl = True


    def load_override(self, override):
        for att_name, att_value in override.items():
            setattr(self, att_name, att_value)
