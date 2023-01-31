from msb_mqtt.MQTTnode import MQTTnode

if __name__ == "__main__":
    mqtt_node = MQTTnode()
    mqtt_node.wait_for_input_and_publish()
