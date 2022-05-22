from flask import request
from flask_restful import Resource

from black_box_grader.src.black_box_grader import Grader
from web_service.src.utils.logz import create_logger
from web_service.src.utils.wrapper import *
from http import HTTPStatus

import base64


class BlackBoxGrader(Resource):
    def __init__(self):
        self.logger = create_logger()

    def post(self):
        request_json = request.get_json()
        if "submissionId" not in request_json:
            return get_response(err=True, msg='Submission id required', status_code=HTTPStatus.BAD_REQUEST)
        if "references" not in request_json:
            return get_response(err=True, msg='References required', status_code=HTTPStatus.BAD_REQUEST)
        if "solution" not in request_json:
            return get_response(err=True, msg='Source code submission required', status_code=HTTPStatus.BAD_REQUEST)

        submissionId = request_json["submissionId"]
        testcases = [base64.b64decode(tc) for tc in request_json["references"]]
        src = base64.b64decode(request_json["solution"])

        try:
            self.logger.info("Black box grading started...")
            # total, details = grade(testcases, src)    # TODO refactor black_box_grader
            total, details = 50, "temp"
            self.logger.info("Black box grading successfully done!")
            responsePayload = {
                "submissionId": submissionId,
                "grade": total,
                "extra": {
                    "feedback": details,
                },
            }
            return get_response_with_single_payload(HTTPStatus.OK, responsePayload)
        except Exception as e:
            self.logger.error("An error occurred", e)
            return get_response(err=True, msg='An error occurred', status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
