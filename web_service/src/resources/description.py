from http import HTTPStatus

from flask_restful import Resource

from web_service.src.utils.logz import create_logger
from web_service.src.utils.wrapper import get_response

class Description(Resource):
    def __init__(self):
        self.logger = create_logger()

    def get(self):
        self.logger.info("receiving description endpoint")
        responseData = {
            "imageName": "rixpl/python-black-box-autograder",
            "displayedName": "Python Black Box Autograder",
            "description": "Black Box Autograder for Python only",
        }
        return get_response(err=False, msg="success", data=responseData, status_code=HTTPStatus.ACCEPTED)
