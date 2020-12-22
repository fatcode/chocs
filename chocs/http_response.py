import copy
from io import BytesIO
from typing import Dict, Optional, Sequence, Union

from .http_cookies import HttpCookieJar
from .http_headers import HttpHeaders
from .http_parsed_body import HttpParsedBodyTrait
from .http_status import HttpStatus


class HttpResponse(HttpParsedBodyTrait):
    def __init__(
        self,
        body: Union[bytes, bytearray, str, None] = None,
        status: Union[int, HttpStatus] = HttpStatus.OK,
        encoding: str = "utf-8",
        headers: Optional[Union[Dict[str, Union[str, Sequence[str]]], HttpHeaders]] = None,
    ):
        self._headers = headers if isinstance(headers, HttpHeaders) else HttpHeaders(headers)
        if isinstance(status, int):
            status = HttpStatus.from_int(status)
        self.status_code = status
        self.body: BytesIO = BytesIO()
        self.encoding = encoding
        self.cookies = HttpCookieJar()
        self._parsed_body = None
        self._as_dict = None
        self._as_str = None

        if body:
            self.write(body)

    @property
    def headers(self) -> HttpHeaders:
        headers: HttpHeaders = copy.copy(self._headers)
        for cookie in self.cookies.values():
            headers.set("Set-Cookie", cookie.serialise())
        return headers

    def write(self, body: Union[str, bytes, bytearray]) -> None:
        if isinstance(body, str):
            self.body.write(body.encode(self.encoding))
        else:
            self.body.write(body)

    @property
    def writable(self) -> bool:
        return not self.body.closed

    def close(self) -> None:
        self.body.close()

    def __str__(self) -> str:
        self.body.seek(0)
        return self.body.read().decode(self.encoding)

    def __eq__(self, other) -> bool:
        if not isinstance(other, HttpResponse):
            return False

        return (
            self.headers == other.headers
            and self.status_code == other.status_code
            and self.encoding == other.encoding
            and self.body.getbuffer().nbytes == other.body.getbuffer().nbytes
        )


__all__ = ["HttpResponse"]
