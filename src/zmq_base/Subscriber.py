import zmq


class Subscriber:
    def __init__(
        self,
        topics="",
        protocol="tcp",
        ip="localhost",
        port="5555",
        connect_to=None,
        debug=False,
    ):
        # self.topics = topics.encode() if type(topics) != bytes else topics
        self.topics = topics
        self.debug = debug

        if not connect_to:
            connect_to = f"{protocol}://{ip}:{port}"
            if self.debug:
                print(f"connecting to : {connect_to}")

        self.context = zmq.Context.instance()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(connect_to)

        # Subscribe to multiple topics 
        if type(self.topics) is list:
            for topic in topics:
                self.subscribe(topic)
        # Or single topic, depending on input
        else:
            self.subscribe(self.topics)



    def subscribe(self, topic):
        if not type(topic) is bytes:
            topic = topic.encode()
        self.socket.setsockopt(zmq.SUBSCRIBE, topic)
        if self.debug:
            print(f"Subscribed to {topic.decode()}")


    def __del__(self):
        self.socket.close()

    def receive(self):
        (topic, message) = self.socket.recv_multipart()
        if self.debug:
            print(f"Received data {message.decode()}")
        return (topic, message)
