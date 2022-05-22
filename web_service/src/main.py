#!/usr/bin/env python
from flask import Flask
from flask_restful import Api

from web_service.src.resources.health_check import HealthCheck
from web_service.src.resources.black_box_grader import BlackBoxGrader

app = Flask(__name__)
api = Api(app)

api.add_resource(HealthCheck, '/health-check')
api.add_resource(BlackBoxGrader, '/grade')


if __name__ == '__main__':
    app.run(host="0.0.0.0")
