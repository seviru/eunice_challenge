class RequestException(Exception):
    def __init__(self, status_code: int, headers: str, method: str, uri: str, response_body: str):
        super().__init__("An error occurred while sending request.")

        self.status_code = status_code
        self.headers = headers
        self.method = method
        self.uri = uri
        self.response_body = response_body

    def __str__(self):
        return (
            f"{super().__str__()} " 
            f"Status code: {self.status_code}. "
            f"Method: {self.method}. "
            f"URI: {self.uri}. "
            f"Response headers: {self.headers}. "
            f"Response body: {self.response_body}."
        )


class CoindeskRequestException(RequestException):
    @classmethod
    def from_request_exception(cls, e):
        return cls(
            status_code=e.status_code,
            headers=e.headers,
            method=e.method,
            uri=e.uri,
            response_body=e.response_body
        )
