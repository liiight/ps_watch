from httpx import HTTPError
from pydantic import ValidationError


class PSWatchError(Exception):
    pass


class PSWatchAPIError(PSWatchError):
    def __init__(self, http_error: HTTPError):
        super().__init__(f"PSWatchAPIError error: {http_error}")


class PSWatchValidationError(PSWatchError):
    def __init__(self, validation_error: ValidationError, data: dict):
        super().__init__(f"PSWatchValidationError: {validation_error} with data {data}")
