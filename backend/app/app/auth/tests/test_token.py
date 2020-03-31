from app.auth import token, schemas


def test_hash():
    password = 'testpassword'

    hashed_pass = token.get_password_hash(password)
    assert hashed_pass != password, 'password is not hashed'
    assert token.verify_password(plain_password=password,
                                 hashed_password=hashed_pass), 'hash function is not compatible'


def test_jwt():
    data = {'username': 'test user'}

    token_data = schemas.TokenData(**data)
    jwt = token.add_access_token(token_data)
    assert isinstance(jwt, bytes)

    payload = token.validate_access_token(jwt)
    assert payload.get('exp')
    assert all(payload[key] == data[key] for key in data)
