import unittest 

import paho.mqtt.client as mqtt
import time
import ssl

from msb_mqtt.MQTTnode import MQTTnode 
from msb_mqtt.MQTTConfig import MQTTConfig 

class PahoMQTTTester(unittest.TestCase):
    def setUp(self):
        self.client = mqtt.Client()
        self.client.username_pw_set("felix", "albatrozz")
        self.client.connect("localhost", 1883)

    def tearDown(self):
        self.client.disconnect()


class MQTTconnectionTester(unittest.TestCase):
    def setUp(self):
        self.client = mqtt.Client()
        self.client.username_pw_set("felix", "albatrozz")
        self.client.on_connect = self.on_connect
        # self.client.tls_set(tls_version=ssl.PROTOCOL_TLS_CLIENT) 
        self.client.connect("localhost", 1883)
        self.override = {"mqtt_broker" : "localhost",
                    "user" : "felix",
                    "passwd" : "albatrozz",
                    "qos" : 2,
                    "mqtt_port" : 1883,
                    "ssl" : False,
                    "topics" : ["test", "over"]}

        self.mqttnode = MQTTnode(self.override)


    def tearDown(self):
        self.client.disconnect()


    def test_publish(self):
        (result, mid) = self.mqttnode.publish("test/topic", "Hello, MQTT!")
        self.assertEqual(result, mqtt.MQTT_ERR_SUCCESS, "Failed to publish message")


    def test_subscribe(self):
        topic = "topic1"
        test_message = "1009.988"
        self.client.subscribe(f"turbine/{topic}")
        self.client.on_message = self.on_message
        self.client.loop_start()
        # self.client.publish(topic, message, qos=1)
        self.mqttnode.publish(topic, test_message)
        time.sleep(0.1)
        self.client.loop_stop()

        expected_return = f"test turbine/topic1={test_message} {time.time_ns()}"
        expected_return = self.strip_nanoseconds(expected_return)
        received_return = self.strip_nanoseconds(self.message)
        self.assertEqual(expected_return, received_return, "Incorrect message received")


    def strip_nanoseconds(self, text):
        return text[:-11]


    def on_message(self, client, userdata, msg):
        # print("received message")
        self.message = msg.payload.decode()


    def on_connect(self, lient, userdata, flags, rc):
        if rc == 0:
            # print('Test client connected to MQTT broker')
            self.client.is_connected = True
        else:
            self.fail("Could not connect")


class ConfigTester(unittest.TestCase):
    def test_reads_override_correctly(self):
        override = {"mqtt_broker" : "localhost",
                    "user" : "felix",
                    "passwd" : "albatrozz",
                    "qos" : 2,
                    "mqtt_port" : 1883,
                    "ssl" : False,
                    "topics" : ["test", "over"],
                }
        self.config = MQTTConfig(override=override)
        self.assertEqual(self.config.mqtt_broker, "localhost")
        self.assertEqual(self.config.user, "felix")
        self.assertEqual(self.config.mqtt_port, 1883)
        self.assertEqual(self.config.qos, 2)
        self.assertEqual(self.config.ssl, False)
        self.assertListEqual(sorted(["over", "test"]), sorted(self.config.topics))

    def no_test_reads_config_correctly(self):
        # self.mqttnode = MQTTnode()
        self.config = MQTTConfig()
        self.assertEqual(self.config.mqtt_broker, "fweiler.de")
        self.assertEqual(self.config.user, "albatrozz")
        self.assertEqual(self.config.mqtt_port, 8883)
        self.assertEqual(self.config.qos, 2)
        self.assertEqual(self.config.ssl, True)
        self.assertListEqual(sorted(["pow", "imu"]), sorted(self.config.topics))

