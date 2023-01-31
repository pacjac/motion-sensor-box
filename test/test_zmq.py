import unittest
import os,sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from zmq_base.Publisher import Publisher
from zmq_base.Subscriber import Subscriber

import zmq
import pickle
import time


class Test_Sender(unittest.TestCase):
    def setUp(self):
        port = 66665
        self.topic = "imu".encode()
        self.subscriber = Subscriber(port=port, topics=self.topic)
        self.publisher = Publisher(port=port)
        # We need a short
        time.sleep(0.1)

    def get_data(self):
        while True:
            (topic, data) = self.subscriber.receive()
            return topic.decode()

    def test_pub_sub_with_classes(self):
        data = "Test pub sub with classes"

        self.publisher.send("imu".encode(), data.encode())
        time.sleep(0.1)
        (topic_recv, message) = self.subscriber.receive()

        self.assertEqual(message.decode(), data)


if __name__ == "__main__":
    unittest.main()
