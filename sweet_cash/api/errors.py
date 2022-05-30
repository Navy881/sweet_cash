from fastapi import HTTPException


class BaseError(HTTPException):
    status_code = 200
    description = None

    def __init__(self, message=None, status_code: int = None):
        if message:
            self.description = message
        if status_code:
            self.status_code = status_code
        super().__init__(status_code=self.status_code, detail=self.description)


class APIError(BaseError):
    """All custom API Exceptions"""
    status_code = 500
    description = "Something's wrong"


class APIAuthError(BaseError):
    """Custom Authentication Error Class."""
    status_code = 403
    description = "Authentication Error"


class APIParamError(BaseError):
    """Custom Request Parameters Error Class."""
    status_code = 400
    description = "Request parameters error"


class APIValueNotFound(BaseError):
    """Custom Request Parameters Error Class."""
    status_code = 404
    description = "Not found"


class APIConflict(BaseError):
    """Custom Request Parameters Error Class."""
    status_code = 409
    description = "Conflict"

# from datetime import datetime
#
# from typing import List
#
#
# class BaseError(Exception):
#     message = "Unexpected exception"
#
#     @property
#     def code(
#         self,
#     ) -> str:
#         return self.message.lower().replace(" ", "_")
#
#     def __repr__(self) -> str:
#         """Для отображения полного контекста ошибки в stderr"""
#         context = [f"{key}: {repr(value)}" for key, value in self.__dict__.items()]
#         context_repr = "\n".join(context)
#
#         return f"{self.message}\n{context_repr}"
#
#     __str__ = __repr__
#
#     def __init__(self) -> None:
#         super().__init__(self.message)
#
#
# class SweetCashError(BaseError):
#     pass
#
#
# class InternalError(SweetCashError):
#     pass
#
#
# class NotFoundError(SweetCashError):
#     status_code = 404
#     message = "Can not found entity"
#     code = "not_found"
#
#
# class NoHeaderError(SweetCashError):
#     message_template = "Header {header} is null"
#     code = "invalid_attribute"
#     status_code = 423
#
#     def __init__(self, header: str) -> None:
#         self.message = self.message_template.format(header=header)
#         super().__init__()
#
#
# class ValidateError(SweetCashError):
#     message_template = "Invalid {type_} value:'{value}'"
#     code = "invalid_attribute"
#     status_code = 423
#
#     def __init__(self, type_: str, value: str) -> None:
#         self.message = self.message_template.format(type_=type_, value=value)
#         super().__init__()
#
#
# class DownstreamServiceError(SweetCashError):
#     def __init__(self, message: str, code: str, status_code: int = 400) -> None:
#         self.message = message
#         self.status_code = status_code
#
#         super().__init__()
#
#
# class AlreadyConnectedError(SweetCashError):
#     status_code = 409
#     message_template = (
#         "Wave is already connected with compilation for period {start_date} - {end_date}, Binding ids: {binding_ids}"
#     )
#     code = "already_connected_error"
#
#     def __init__(self, start_date: datetime, end_date: datetime, binding_ids: List[int]):
#         self.message = self.message_template.format(start_date=start_date, end_date=end_date, binding_ids=binding_ids)
#         super().__init__()


# from flask import jsonify, Blueprint
#
#
# blueprint = Blueprint('error_handlers', __name__)
#
#
# class APIError(Exception):
#     """All custom API Exceptions"""
#     code = 500
#     description = "Something's wrong"
#
#
# class APIAuthError(APIError):
#     """Custom Authentication Error Class."""
#     code = 403
#     description = "Authentication Error"
#
#
# class APIParamError(APIError):
#     """Custom Request Parameters Error Class."""
#     code = 400
#     description = "Request parameters error"
#
#
# class APIValueNotFound(APIError):
#     """Custom Request Parameters Error Class."""
#     code = 404
#     description = "Not found"
#
#
# class APIConflict(APIError):
#     """Custom Request Parameters Error Class."""
#     code = 409
#     description = "Conflict"
#
#
# @blueprint.app_errorhandler(APIError)
# def handle_exception(err):
#     """Return custom JSON when APIError or its children are raised"""
#     response = {"error": err.description, "message": ""}
#     error_code = err.code
#     if len(err.args) > 0:
#         response["message"] = err.args[0]
#     if len(err.args) > 1:
#         error_code = err.args[1]
#     return jsonify(response), error_code
#
#
# class Error(object):
#
#     def __init__(self, msg, code=None, status=200, data=None):
#         self.code = code
#         self.status = status
#         self.data = data or {}
#         self.message = msg
#         self.response = None
#
#     @classmethod
#     def make(cls, cmessage=None, ccode=None, cstatus=None):
#         class Error(cls):
#             def __init__(self, message=None, code=None, status=None, data=None):
#                 cls.__init__(
#                     self, message or cmessage, code or ccode, status or cstatus, data
#                 )
#
#         return Error
#
#     def __call__(self, environ, start_response):
#         self.response = jsonify({
#             'status': self.status,
#             'error_code': self.code,
#             'message': self.message
#         })
#         self.response.status_code = self.status
#         return self.response(environ, start_response)
#
#
# NotFoundError = Error.make("Not found", "not-found", 404)
# BadParams = Error.make("Bad params", "bad-params", 400)
# Unauthorized = Error.make("Unauthorized", "unauthorized", 401)
# Forbidden = Error.make("Forbidden", "forbidden", 403)
# Conflict = Error.make("Conflict", "conflict", 409)
# MethodNotAllowed = Error.make("Method not allowed", "method-not-allowed", 405)
# InternalServerError = Error.make("Internal server error", "internal-server-error", 500)
# NotModified = Error.make("Not Modified", "not-modyfied", 304)
# TooManyRequests = Error.make("Too Many Requests", "too-many-requests", 429)
