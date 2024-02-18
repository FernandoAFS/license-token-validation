
import typing as t
from Crypto.PublicKey import ECC

from src.token_val import crypt as token_crypt

def test_signature():
    msg = b"a msg"

    key = ECC.generate(curve='p256')

    signer = token_crypt.MsgSigner(key)
    validator = token_crypt.MsgValidator(key)


    signature = signer.sign(msg)
    validator.validate(msg, signature)



