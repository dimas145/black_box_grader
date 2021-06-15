#!/usr/bin/env python

import pika, sys, os
import time
import json
import os
import requests
from dotenv import load_dotenv
from extract import extractTarGz
from grader import Grader
import time

def callback(ch, method, properties, body):
    start_time = time.time()
    print(json.loads(body.decode()))
    data = json.loads(body.decode())["data"]

    sourceCodeBasePath = "tmp/src"
    extractTarGz(tarGzBase64=data["sourceCodeBase64"], basePath=sourceCodeBasePath)

    # start docker
    grade = Grader(tmpPath="tmp", entryPoint=data["entry"], testcases=data["testcases"])
    result =  grade.grade()
    result['user'] = {
        'projectId': data["projectId"],
        'userId': data["userId"],
        'courseId': data["courseId"],
        'activityId': data["activityId"]
    }
    headers = {'Content-Type': "application/json"}

    requests.post(f'{os.getenv("BRIDGE_SERVICE_URL")}/callback/',data=json.dumps(result), headers=headers)
    end_time = time.time() - start_time
    with open("execution_time.log", "a+") as f:
        f.write(f"{end_time}\n")
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