import unittest
import time
import signal, sys
import zmq

from src.broker.msb_broker import signal_handler, msb_broker
from src.broker.BrokerConfig import BrokerConfig

from src.zmq_base.Publisher import Publisher
from src.zmq_base.Subscriber import Subscriber

class ConnectPublisher(Publisher):
    def __init__(
        self, protocol="tcp", ip="127.0.0.1", port="5555", connect_to=None, debug=False
    ):
        self.debug = debug

        if not connect_to:
            connect_to = f"{protocol}://{ip}:{port}"
            if self.debug:
                print(f"binding to : {connect_to}")

        self.context = zmq.Context.instance()
        self.socket = self.context.socket(zmq.PUB)
        if self.debug: print(f"connecting via {connect_to}")

        try:
            self.socket.connect(connect_to)
        except Exception as e:
            print(f"failed to bind to zeromq socket: {e}")
            sys.exit(-1)


class BrokerTester(unittest.TestCase):
    def setUp(self):
        signal.signal(signal.SIGINT, signal_handler)
        self.config = BrokerConfig()

        self.topic = "imu".encode()
        self.subscriber = Subscriber(connect_to=self.config.xpub_socketstring, topics=self.topic)
        self.publisher = ConnectPublisher(connect_to=self.config.xsub_socketstring)
        # We need a short
        time.sleep(0.1)

    def test_can_publish_and_receive(self):
        test_topic = self.topic
        test_message = "Hello from publisher".encode()
        # self.subscriber = Subscriber(connect_to=self.config.xpub_socketstring, topics=test_topic)
        # time.sleep(1)
        # self.publisher = ConnectPublisher(connect_to=self.config.xsub_socketstring)
        
        time.sleep(1)

        self.publisher.send(test_topic, test_message)
        time.sleep(0.1)
        (topic_recv, message) = self.subscriber.receive()

        print(message)

        self.assertEqual(message.decode(), "Hello from publisher")
        self.assertEqual(topic_recv.decode(), "imu")


if __name__ == "__main__":
    unittest.main()
