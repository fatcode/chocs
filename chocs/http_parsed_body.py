import json
import yaml
from cgi import parse_header
from copy import copy
from io import BytesIO
from typing import Dict, Optional, Tuple

from .http_headers import HttpHeaders
from .http_message import (
    FormHttpMessage,
    HttpMessage,
    JsonHttpMessage,
    MultipartHttpMessage,
    YamlHttpMessage,
)


class HttpParsedBodyTrait:
    _body: BytesIO
    _headers: HttpHeaders
    _parsed_body: Optional[HttpMessage]
    _as_str: Optional[str]
    _as_dict: Optional[dict]

    @property
    def parsed_body(self) -> HttpMessage:
        if self._parsed_body:
            return copy(self._parsed_body)

        content_type: Tuple[str, Dict[str, str]] = parse_header(
            self._headers["Content-Type"]  # type: ignore
        )

        parsed_body: HttpMessage

        if content_type[0] == "multipart/form-data":
            parsed_body = MultipartHttpMessage.from_bytes(
                self._body, content_type[1].get("boundary", ""), content_type[1].get("charset", ""),
            )
        elif content_type[0] == "application/x-www-form-urlencoded":
            parsed_body = FormHttpMessage.from_bytes(self._body, content_type[1].get("charset", "utf8"))

        elif content_type[0] == "application/json":
            parsed_body = JsonHttpMessage.from_bytes(self._body, content_type[1].get("charset", "utf8"))
        elif content_type[0] in ("text/vnd.yaml", "text/yaml", "text/x-yaml", "application/x-yaml",):
            parsed_body = YamlHttpMessage.from_bytes(self._body, content_type[1].get("charset", "utf8"))
        else:
            self._body.seek(0)
            parsed_body = HttpMessage(self._body.read().decode(content_type[1].get("charset", "utf8")))

        self._parsed_body = parsed_body

        return copy(self._parsed_body)

    def as_str(self) -> str:
        if not self._as_str:
            self._body.seek(0)
            self._as_str = self._body.read().decode("utf8")

        return self._as_str

    def as_dict(self) -> dict:
        if self._as_dict is None:
            body_str = self.as_str()
            try:
                self._as_dict = json.loads(body_str)  # type: ignore

                return self._as_dict  # type: ignore
            except Exception:
                try:
                    self._as_dict = yaml.safe_load_all(body_str)  # type: ignore

                    return self._as_dict  # type: ignore
                except Exception:
                    self._as_dict = {}

        return self._as_dict
