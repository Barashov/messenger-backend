from fastapi.testclient import TestClient
from main import app


client = TestClient(app)
token = None


def test_create_chat():
    global token
    token = client.post('/users/sign-up/', json={'username': 'Alex',
                                                 'password': 1234}).json()
    url = '/chats/create/'
    auth_header = {'Authorization': f'Token {token["token"]}'}

    # ok
    result = client.post(url, data={'name': 'chat'}, headers=auth_header)
    assert result.status_code == 201
    result_json = result.json()
    assert result_json['id'] == 1
    assert result_json['name'] == 'chat'

    # not auth
    result = client.post(url, data={'name': 'chat'})
    assert result.status_code == 401

    # invalid body
    result = client.post(url, data={'chat': 'chat'}, headers=auth_header)
    assert result.status_code == 422


