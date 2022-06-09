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
