
import attrs
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS


@attrs.frozen
class MsgSigner:
    key: "ECC.EccKey" # PRIVATE KEY
    mode: str = "fips-186-3"

    def sign(self, msg: bytes) -> bytes:
        hash_ = SHA256.new(data=msg)
        signer = DSS.new(self.key, self.mode)
        signature = signer.sign(hash_)
        return signature


@attrs.frozen
class MsgValidator:
    key: "ECC.EccKey"  # PUBLIC KEY
    mode: str = "fips-186-3"

    def validate(self, msg: bytes, signature: bytes) -> None:
        """
        Raises ValueError if the signature is not authentic
        """
        hash_ = SHA256.new(data=msg)
        verifier = DSS.new(self.key, 'fips-186-3')
        verifier.verify(hash_, signature)

