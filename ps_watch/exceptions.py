from glom import glom
from glom import GlomError
from httpx import HTTPError
from pydantic import ValidationError


class PSWatchError(Exception):
    pass


class PSWatchAPIError(PSWatchError):
    def __init__(self, http_error: HTTPError):
        msg = f"PSWatchAPIError error:\n{http_error}"
        if glom(http_error, "response.status_code", default=None) == 401:
            msg = f"Unauthorized, session ID invalid or expired:\n{http_error}"
        super().__init__(msg)


class PSWatchValidationError(PSWatchError):
    def __init__(self, validation_error: ValidationError, data: dict):
        super().__init__(f"PSWatchValidationError: {validation_error} with data {data}")


class PSWatchDataError(PSWatchError):
    def __init__(self, glom_error: GlomError, data):
        super().__init__(f"PSWatchDataError: {glom_error} with data {data}")
