from flask import Blueprint
from . import (
    json_response,
)

api = Blueprint('api', __name__)


class ApiException(Exception):
    code = 20400
    data = {}
    message = 'API Exception'

    def get_body(self):
        data = self.data
        data['error_code'] = self.code
        return json_response(False, data, message=self.message)


class ApiNotFound(ApiException):
    code = 20404

    def __init__(self, data):
        self.data = data
        self.message = 'Not Found.'


class ApiNotAuthorized(ApiException):
    code = 20401

    def __init__(self, data):
        self.data = data
        self.message = 'Not Authorized.'


@api.errorhandler(ApiException)
def api_exception(e):
    return e.get_body()
