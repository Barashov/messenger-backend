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


user_1_id = None
chat_id = None
user_2_auth = None  # user not in chat


def test_add_user_to_chat():
    global user_1_id, chat_id, user_2_auth
    # /chats/{chat_id}/add-user/{user_id}/ get request
    chat_admin = client.post('/users/sign-up/',
                             json={'username': 'chat-admin',
                                   'password': '1234'}).json()
    admin_auth = {'Authorization': f'Token {chat_admin["token"]}'}
    chat = client.post('/chats/create/',
                       data={'name': 'new_chat'},
                       headers={'Authorization': f'Token {chat_admin["token"]}'}).json()
    chat_id = chat['id']

    user_1 = client.post('/users/sign-up/',
                         json={'username': 'user_1',
                               'password': '1234'}).json()
    user_2 = client.post('/users/sign-up/',
                         json={'username': 'user_2',
                               'password': '1234'}).json()
    user_1_id = user_1['id']
    user_2_id = user_2['id']

    # ok
    result = client.get(f'/chats/{chat_id}/add-user/{user_1_id}/', headers=admin_auth)
    assert result.status_code == 200

    # user can't add another user to chat (user not in chat)
    user_2_auth = {'Authorization': f'Token {user_2["token"]}'}
    result = client.get(f'/chats/{chat_id}/add-user/{user_2_id}/', headers=user_2_auth)
    assert result.status_code == 403


def test_list_of_chat_users():
    # /chats/{chat_id}/users/
    chat_admin = client.post('/users/login/', json={'name': 'chat-admin',
                                                    'password': '1234'}).json()

    chat_admin_auth = {'Authorization': f'Token {chat_admin["token"]}'}

    result = client.get(f'/chats/{chat_id}/users/', headers=chat_admin_auth)
    assert result.status_code == 200
    assert len(result.json()) == 2

    #  user not in chat
    result = client.get(f'/chats/{chat_id}/users/', headers=user_2_auth)
    assert result.status_code == 403

