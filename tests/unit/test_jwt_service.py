from uuid import UUID

def test_encode_jwt(jwt_service):
    payload ={"sub": str(UUID('1b44ed96-5595-457a-b119-736e4c0fa163')), "role": 'ADMIN'}
    result = jwt_service.encode_jwt(payload)
    expected_header = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9'
    jwt = result.split('.')
    assert isinstance(result, str)
    assert  len(jwt) == 3
    assert expected_header == jwt[0]
    assert jwt[1] is not None
    assert jwt[2] is not None

def test_decode_jwt(jwt_service):
    payload = {"sub": str(UUID('1b44ed96-5595-457a-b119-736e4c0fa163')), "role": 'ADMIN'}
    token = jwt_service.encode_jwt(payload)
    result = jwt_service.decode_jwt(token)
    assert isinstance(result,dict)
    assert len(result) == 3
    assert result['sub'] == str(UUID('1b44ed96-5595-457a-b119-736e4c0fa163'))
    assert result['role'] == 'ADMIN'

