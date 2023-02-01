from paho.mqtt import client as mqtt_client
import ssl
import time
import pickle

from msb_mqtt.MQTTConfig import MQTTConfig
from zmq_base.Subscriber import Subscriber

class MQTTnode:
    def __init__(self, config_override={}, debug=False):
        self.debug = debug
        self.config = MQTTConfig(override=config_override)

        if self.debug: print(f"Subscribing to topics: {self.config.topics}")
        self.subscriber = Subscriber(connect_to=self.config.xpub_socketstring, topics=self.config.topics)
        self.connect_mqtt()


    '''
    Main loop: data comes in through zmq subscription socket, passed on to mqtt publish
    At the moment, Subscriber.receive() is blocking
    '''
    def wait_for_input_and_publish(self):
        # At which level to place the while loop?
        while True:
            # This is blocking
            try:
                # ZQM transports a pickled dict, with topic as key and value as value
                (zmq_topic, data) = self.subscriber.receive()

                # Deserialize data, assuming its a dict
                # Good place for a refactor, what if it is not a dict?
                data = pickle.loads(data)

                # Publish each key-value pair in the dict
                for topic, value in data.items():
                    self.publish(topic, value)


                # We comment this out for now, but I would like to replace this with an extra function
                # self.publish(zmq_topic.decode(), float(data.decode()))
            except Exception as e:
                print(e)


    '''
    Publish to MQTT broker. Message should look as follows (whitespace important!)
    measurement_name [tags] topic=value timestamp
    with 
    '''
    def publish(self, zmq_topic, data):
        now = int(time.time_ns())
        topic= self.create_topic_from_zmq(zmq_topic)
        msg = f"{self.config.measurement} {topic}={data} {now}"

        if self.debug: print(f"publishing to {topic} with msg : {msg}")

        result = self.client.publish(topic, msg, qos=self.config.qos)
        return result

    
    '''
    From a 3 character zmq topic create a hierarchical topic suitable for mqtt
    i.e. "imu" --> turbine1/blade2/flap4/imu
    '''
    def create_topic_from_zmq(self, zmq_topic : str):
        return f"turbine/{zmq_topic}"


    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                if self.debug: print(f'MQTT node connected to {self.config.mqtt_broker}:{self.config.mqtt_port}')
            else:
                print('Connection failed!')

        self.client = mqtt_client.Client()
        self.client.username_pw_set(self.config.user, self.config.passwd)
        self.client.on_connect = on_connect

        if self.config.ssl: 
            # By default, on Python 2.7.9+ or 3.4+, the default certification authority of the system is used.
            self.client.tls_set(tls_version=ssl.PROTOCOL_TLS_CLIENT) 

        self.client.connect(self.config.mqtt_broker, self.config.mqtt_port)
        self.client.loop_start()


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-r",
        "--run",
        action="store_true",
        help="Run in blocking mode, waiting for input and publishing via mqtt"
    )
    parser.add_argument(
        "-o",
        "--override",
        action="store_true",
    )
    parser.add_argument(
        "--data",
        type=float
    )
    args = parser.parse_args()

    if args.override:
        override = {"mqtt_broker" : "localhost", 
                    "mqtt_port" : 1883, 
                    "mqtt_user" : "felix",
                    "passwd" : "albatrozz",
                    "ssl" : False
                    }

        mqtt_tester = MQTTnode(override)
    else:
        mqtt_tester = MQTTnode(debug=True)

    if args.run:
        mqtt_tester.wait_for_input_and_publish()
    elif args.data:
        mqtt_tester.publish("tst", args.data)
