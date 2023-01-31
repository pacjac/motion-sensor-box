import unittest 
import sys
import zmq

from sysdmanager import SystemdManager


class TestBrokerAsBlackBox(unittest.TestCase):
    def test_can_connect(self):
        # Check that the environment variable $MSB_CONFIG_DIR is set and is a valid path
        env_var = "MSB_CONFIG_DIR"
        self.assertTrue(env_var in os.environ, f"Environment variable {env_var} is not set")
        
        # Check that the service "msb-broker" is running
        manager = SystemdManager()
        self.assertTrue(manager.is_active("msb-broker"), "Service msb-broker is not running")
        
        # Setup a ZMQ publisher socket and connect it to the broker
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.connect("tcp://localhost:5555")

        # Setup a ZMQ subscriber socket and connect it to the broker
        socket_sub = context.socket(zmq.SUB)
        socket_sub.connect("tcp://localhost:5556")

        # Subscribe socket to test topic
        socket_sub.setsockopt_string(zmq.SUBSCRIBE, "test")

        # Message and topic to send
        message = "Hello World"
        topic = "test"

        # Send message
        socket.send_multipart([topic.encode(), message.encode()])

        # Receive message
        received_topic, received_message = socket_sub.recv_multipart()

        # Check that the received message is the same as the sent message
        self.assertEqual(received_topic.decode(), topic)
        self.assertEqual(received_message.decode(), message)

        # Close sockets
        socket.close()
        socket_sub.close()


        


