from httpx import HTTPError


class PSWatchError(Exception):
    pass


class PSWatchAPIError(PSWatchError):
    def __init__(self, http_error: HTTPError):
        super().__init__(f"PSWatchAPIError error: {http_error}")
