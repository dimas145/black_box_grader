#!/usr/bin/env python

import pika, sys, os
import time
import json
import os
from dotenv import load_dotenv
from helper import extractTarGz


def callback(ch, method, properties, body):
    print(json.loads(body.decode()))
    data = json.loads(body.decode())["data"]
    extractTarGz(data["sourceCodeBase64"], data["assignmentId"], data["projectId"])

    # start docker

    print("finish process message")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    load_dotenv()
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.getenv("RABBITMQ_URL"))
    )
    channel = connection.channel()

    channel.queue_declare(queue=os.getenv("RABBITMQ_QUEUE_NAME"))
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=os.getenv("RABBITMQ_QUEUE_NAME"), on_message_callback=callback
    )

    print("Running forever :)")
    channel.start_consuming()


if __name__ == "__main__":
    main()