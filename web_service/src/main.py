#!/usr/bin/env python
from flask import Flask
from flask_restful import Api

from web_service.src.resources.health_check import HealthCheck
from web_service.src.resources.black_box_grader import BlackBoxGrader
from web_service.src.resources.description import Description

import docker

client = docker.from_env()
IMAGE_NAME = "python:3.9-alpine"

app = Flask(__name__)
api = Api(app)

api.add_resource(HealthCheck, '/health-check')
api.add_resource(Description, '/description')
api.add_resource(BlackBoxGrader, '/grade')


if __name__ == '__main__':
    client.images.pull(IMAGE_NAME)
    app.run(host="0.0.0.0")
