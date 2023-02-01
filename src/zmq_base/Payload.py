from dataclasses import dataclass
import pickle
import datetime
import time
import uptime



@dataclass
class Payload:
    timestamp: datetime.datetime
    unix_epoch: float
    uptime: float
    data: dict


class PayloadFactory:
    def __init__(self):
        self.time = 0

    def create(self, data: dict) -> Payload:
        self.time = time.time()
        return Payload(
            timestamp=datetime.datetime.fromtimestamp(self.time,  tz=datetime.timezone.utc),
            unix_epoch=self.time,
            uptime=uptime.uptime(),
            data=data
        )








