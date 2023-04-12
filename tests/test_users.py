from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

username = 'Bob'
password = '12345678'
token = 'token'


def test_create_user():
    global token

    url = '/users/sign-up/'
    data = {'username': username, 'password': password}
    result = client.post(url,
                         json=data)

    assert result.status_code == 200
    token = result.json()['token']

    assert client.post(url, json=data).status_code == 401, 'username is already taken'

    # bad request
    assert client.post(url, json={'name': 'xx', 'pass': '334'}).status_code == 422, 'bad'

    # bad data
    data = {'username': 'ba', 'password': '1234423412'}
    assert client.post(url, json=data).status_code == 422, 'small username'
    data['password'] = '123'
    data['username'] = 'Bob'
    assert client.post(url, json=data).status_code == 422, 'small password'


def test_login_user():
    url = '/users/login/'
    data = {'name': username, 'password': password}

    # ok
    result = client.post(url, json=data)
    assert result.status_code == 200

    # bad data
    data = {'name': 'alexdfd', 'password': 'dafsd0'}
    result = client.post(url, json=data)
    assert result.status_code == 401

    # bad request
    data = {'name': 'ddf', 'pass': 'dfdf'}
    assert client.post(url, json=data).status_code == 422


def test_auth():
    url = '/users/is-auth/'

    # ok
    result = client.post(url, headers={'Authorization': f'Token {token}'})
    assert result.status_code == 200

    # invalid auth header
    result = client.post(url, headers={'Authorization': token})
    assert result.status_code == 401

    # auth header is empty
    result = client.post(url)
    assert result.status_code == 401

    # auth token is invalid
    result = client.post(url, headers={'Authorization': 'Token djfladsf'})
    assert result.status_code == 401
