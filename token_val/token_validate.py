import datetime as dt
import operator as op
import typing as t

import attrs

from . import environment as env
from . import exceptions as excp


@attrs.frozen
class TokenStatus:
    token: bytes
    eol: "dt.datetime"


@attrs.frozen
class TokenValidator:
    token_info: t.Mapping[bytes, "TokenStatus"]

    def validate(self, token: bytes):
        if token not in self.token_info:
            raise excp.UnregisteredTokenException(f"Token {token.hex()} not registered")

        token_info = self.token_info[token]
        now_ = env.get_now()

        if now_ > token_info.eol:
            raise excp.ExpiredTokenException("Token expired")


def token_validator_factory(token_info: "t.Sequence[TokenStatus]") -> "TokenValidator":
    tokens = map(op.attrgetter("token"), token_info)
    map_ = dict(zip(tokens, token_info, strict=True))
    return TokenValidator(map_)
