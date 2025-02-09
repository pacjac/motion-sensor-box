# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import asyncio
from azure.iot.device import Message
from azure.iot.device.aio import IoTHubDeviceClient
import json
import os
from socket import gethostname
import sys
import uuid

messages_to_send = 10

async def main():
    # The connection string for a device should never be stored in code. For the sake of simplicity we're using an environment variable here.
    conn_str = os.getenv("ACS")
    if not conn_str:
        print(f'empty connection string environment variable! please make sure, the correct environment variable containing the connecition string has been set')
        sys.exit()

    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the client.
    await device_client.connect()

    async def send_test_message(i):
        print(f"sending message #{i}")
        msg = Message(json.dumps({'data1' : 1234, 'data2' : 1234}))
        msg.message_id = uuid.uuid4()
        msg.correlation_id = ""
        msg.custom_properties["msb-sn"] = f"{gethostname()}"
        msg.content_encoding = "utf-8"
        msg.content_type = "application/json"
        await device_client.send_message(msg)
        print("done sending message #" + str(i))

    # send `messages_to_send` messages in parallel
    await asyncio.gather(*[send_test_message(i) for i in range(1, messages_to_send + 1)])

    # Finally, shut down the client
    await device_client.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

    # If using Python 3.6 use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
