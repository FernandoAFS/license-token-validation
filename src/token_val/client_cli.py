
import typer
import pathlib
import base64

from . import xml_rpc
from . import crypt
from . import io

app = typer.Typer()


@app.command()
def client(host: str, public_key_path: "pathlib.Path", token: str):
    key = io.import_key(public_key_path)
    validator = crypt.MsgValidator(key)

    cl = xml_rpc.Client(host, validator)

    d = base64.b64decode(token)
    signature = cl.validate_token(d)

    print("Successfull validation")


if __name__ == "__main__":
    app()
