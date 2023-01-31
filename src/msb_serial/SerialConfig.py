import argparse

from msb_config.MSBConfig import MSBConfig

class SerialConfig(MSBConfig):
    def __init__(self, subconf = "msb-serial", override=dict()):
        super().__init__()
        self.set_default_attributes()

        if override:
            self.load_override(override)
        else:
            self._load_conf(subconf=subconf)


    def set_default_attributes(self):
        self.regex = ""
        self.device = "/usb/TTY0"
        self.topic = "imu"

    def load_override(self, override):
        for att_name, att_value in override.items():
            setattr(self, att_name, att_value)


