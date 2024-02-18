
import pytest
import datetime as dt
from src.token_val import token_validate as tv
from src.token_val import exceptions as excp

def test_token_env():
    now_ = dt.datetime.now()
    td = dt.timedelta(minutes=10)

    token = b"hello world"
    st = tv.TokenStatus( token, now_ + td)
    val = tv.token_validator_factory([st])

    val.validate(token)


def test_token_env_expired():
    now_ = dt.datetime.now()
    td = dt.timedelta(minutes=10)

    token = b"hello world"
    st = tv.TokenStatus(token, now_ - td)
    val = tv.token_validator_factory([st])

    with pytest.raises(excp.ExpiredTokenException):
        val.validate(token)


def test_token_env_unreg():
    now_ = dt.datetime.now()
    td = dt.timedelta(minutes=10)

    token = b"hello world"
    token_ = b"hola mundo"
    st = tv.TokenStatus(token, now_ + td)
    val = tv.token_validator_factory([st])

    with pytest.raises(excp.UnregisteredTokenException):
        val.validate(token_)








