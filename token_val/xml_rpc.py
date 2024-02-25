import traceback
import typing as t
import attrs
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer

if t.TYPE_CHECKING:
    from . import crypt
    from . import token_validate as tv

@attrs.frozen
class TokenValidation:
    token: bytes
    #signature: bytes


@attrs.frozen
class ServerApp:
    token_validtion: "tv.TokenValidator"
    signer: "crypt.MsgSigner"

    def validate_token(self, token: "xmlrpc.client.Binary") -> bytes:
        token_ = token.data
        try:
            self.token_validtion.validate(token_)
            signature = self.signer.sign(token_)
            return signature
        except Exception as e:
            print(traceback.format_exc())
            raise e


@attrs.frozen
class Server:
    server_app: "ServerApp"
    host: str = '0.0.0.0'
    port: int = 8000

    def serve(self):
        with SimpleXMLRPCServer((self.host, self.port)) as server:
            server.register_introspection_functions()
            server.register_instance(self.server_app)
            server.serve_forever()


@attrs.frozen
class Client:
    host: str
    validator: "crypt.MsgValidator"

    def validate_token(self, token: bytes):
        proxy = xmlrpc.client.ServerProxy(self.host)
        signature = proxy.validate_token(token)
        self.validator.validate(token, signature.data)  # type: ignore
