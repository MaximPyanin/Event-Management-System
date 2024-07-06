import pytest

from app.utils.hash_service import HashService


def test_hash_password():
    password = 'dfdsfdfsd'
    hashed_password = HashService.hash_password(password)
    assert isinstance(hashed_password,bytes)

def test_check_password():
    password = 'dfdsfdfsd'
    hashed_password = HashService.hash_password(password)
    result = HashService.check_password(password,hashed_password)
    assert result is True

@pytest.mark.xfail
def test_check_password_incorrect_password():
    hashed_password = HashService.hash_password('noinio')
    result = HashService.check_password('random passwd', hashed_password)
    assert result is True