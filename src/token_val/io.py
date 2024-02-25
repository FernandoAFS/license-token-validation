import base64
import datetime as dt
import json
import pathlib
import typing as t

from Crypto.PublicKey import ECC

from . import token_validate as tv


def token_info_hook(data, type_):
    ...


def token_eol_data(path: "pathlib.Path") -> t.Sequence["tv.TokenStatus"]:
    d = json.loads(path.read_text())

    def convert_(d) -> "tv.TokenStatus":
        token = base64.b64decode(d["token"])
        eol = dt.datetime.fromisoformat(d["eol"]).replace(tzinfo=None)
        return tv.TokenStatus(
            token=token,
            eol=eol,
        )

    return list(map(convert_, d))


def import_key(path: "pathlib.Path", pwd: "str | None" = None) -> "ECC.EccKey":
    d = path.read_text()
    if pwd is not None:
        return ECC.import_key(d, pwd)
    else:
        return ECC.import_key(d)
