from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

username = 'Bob' # 409
password = '12345678'


def test_create_user():
    url = '/users/user/'
    data = {'username': username, 'password': password}
    result = client.post(url,
                         json=data)

    assert result.status_code == 200
    assert client.post(url, json=data).status_code == 409, 'username is already taken'

    # bad request
    assert client.post(url, json={'name': 'xx', 'pass': '334'}).status_code == 400, 'bad'

    # bad data
    data = {'username': 'ba', 'password': '1234423412'}
    assert client.post(url, json=data).status_code == 400, 'small username'
    data['password'] = '123'
    data['username'] = 'Bob'
    assert client.post(url, json=data).status_code == 400, 'small password'


def test_login_user():
    url = '/users/login/'
    data = {'username': username, 'password': password}

    # ok
    result = client.post(url, json=data)
    assert result.status_code == 200

    # bad data
    data = {'username': 'alexdfd', 'password': 'dafsd0'}
    result = client.post(url, json=data)
    assert result.status_code == 401

    # bad request
    data = {'name': 'ddf', 'pass': 'dfdf'}
    assert client.post(url, json=data).status_code == 400
