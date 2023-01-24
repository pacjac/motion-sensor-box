import zmq


class Subscriber:
    def __init__(
        self,
        topic="",
        protocol="tcp",
        ip="localhost",
        port="5555",
        connect_to=None,
        debug=False,
    ):
        self.topic = topic.encode() if type(topic) != bytes else topic
        self.debug = debug

        if not connect_to:
            connect_to = f"{protocol}://{ip}:{port}"
            if self.debug:
                print(f"connecting to : {connect_to}")

        self.context = zmq.Context.instance()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(connect_to)
        self.socket.setsockopt(zmq.SUBSCRIBE, self.topic)
        if self.debug:
            print(f"Subscribed to {self.topic.decode()}")

    def __del__(self):
        self.socket.close()

    def receive(self):
        (topic, message) = self.socket.recv_multipart()
        if self.debug:
            print(f"Received data {message.decode()}")
        return (topic, message)
