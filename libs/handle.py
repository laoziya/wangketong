from flask_restful import HTTPException
from libs.error_code import APIException

def default_error_handler(ex):
    if isinstance(ex, APIException):
        return ex
    if isinstance(ex, HTTPException):
        code = ex.code
        message = ex.description
        status_code = 10001
        return APIException(code = code, message=message, status_code=status_code)
    return APIException()