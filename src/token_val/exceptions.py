

class TokenException(Exception):
    ...

class UnregisteredTokenException(TokenException):
    ...

class ExpiredTokenException(TokenException):
    ...


