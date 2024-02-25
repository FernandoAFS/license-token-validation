
import typing as t
import pathlib

import typer

from Crypto.PublicKey import ECC

app = typer.Typer()


@app.command()
def private_key(path: "pathlib.Path", passphrase: "t.Optional[str]" = None):
    key = ECC.generate(curve='p256')
    if passphrase is not None:
        export_key = key.export_key(
            format="PEM",
            passphrase=passphrase,
            protection='PBKDF2WithHMAC-SHA512AndAES256-CBC',
        )
    else:
        export_key = key.export_key(format="PEM")
    path.write_text(export_key)


@app.command()
def public_key(private_key_file: "pathlib.Path", passphrase: "t.Optional[str]" = None):
    exported_key = private_key_file.read_text()
    if passphrase is not None:
        key = ECC.import_key(exported_key, passphrase)
    else:
        key = ECC.import_key(exported_key)
    public = key.public_key()

    exported_public = public.export_key(format="PEM")
    print(exported_public)



if __name__ == "__main__":
    app()
