import typing as t
import pathlib

import typer

from . import crypt, xml_rpc
from . import io as token_io
from . import token_validate as tv

app = typer.Typer()


@app.command()
def server(
    key_path: "pathlib.Path",
    token: "pathlib.Path",
    host: str = "0.0.0.0",
    port: int = 8000,
    passphrase: "t.Optional[str]" = None,
):
    token_eol = token_io.token_eol_data(token)
    key = token_io.import_key(key_path, passphrase)

    token_val = tv.token_validator_factory(token_eol)
    signer = crypt.MsgSigner(key)

    server_app = xml_rpc.ServerApp(
        token_val,
        signer,
    )
    server = xml_rpc.Server(server_app, host, port)
    server.serve()


if __name__ == "__main__":
    app()
