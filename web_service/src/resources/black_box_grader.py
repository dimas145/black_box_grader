from flask import request
from flask_restful import Resource

from black_box_grader.src.black_box_grader import *
from web_service.src.utils.logz import create_logger
from web_service.src.utils.wrapper import *
from http import HTTPStatus

import base64
import json


class BlackBoxGrader(Resource):
    def __init__(self):
        self.logger = create_logger()

    def post(self):
        request_json = request.get_json()
        if "references" not in request_json:
            return get_response(err=True, msg='References required', status_code=HTTPStatus.BAD_REQUEST)
        if "solution" not in request_json:
            return get_response(err=True, msg='Source code submission required', status_code=HTTPStatus.BAD_REQUEST)

        testcases = [json.loads(base64.b64decode(tc).decode("ascii")) for tc in request_json["references"]]
        base64Source = request_json["solution"] # decode when running the container

        try:
            points, details = grade(testcases, base64Source)
            responseData = {
                "grade": points,
                "feedback": details,
            }
            return get_response(err=False, msg="success", data=responseData, status_code=HTTPStatus.OK)
        except Exception as e:
            self.logger.error("An error occurred", e)
            return get_response(err=True, msg='An error occurred', status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
