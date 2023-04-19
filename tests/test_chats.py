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


chat_id = None
user_2_auth = None


def test_add_user_to_chat():
    global chat_id, user_2_auth
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


def test_delete_users_from_chat():
    #  /chats/{chat_id}/delete-user/{user_id}/
    chat_admin = client.post('/users/login/', json={'name': 'chat-admin',
                                                    'password': '1234'}).json()
    chat_admin_auth = {'Authorization': f'Token {chat_admin["token"]}'}
    chat_admin_id = chat_admin['id']

    # user_1 in chat
    user_1 = client.post('/users/login/', json={'name': 'user_1',
                                                'password': '1234'}).json()
    user_1_id = user_1['id']
    user_1_auth = {'Authorization': f'Token {user_1["token"]}'}

    # user_2 not in chat
    user_2 = client.post('/users/login/', json={'name': 'user_2',
                                                'password': '1234'}).json()
    user_2_id = user_2['id']
    user_2_auth = {'Authorization': f'Token {user_2["token"]}'}

    #  user_1 delete admin
    result = client.delete(f'/chats/2/delete-user/{chat_admin_id}/', headers=user_1_auth)
    assert result.status_code == 403

    # user_2 delete admin
    result = client.delete(f'/chats/2/delete-user/{chat_admin_id}/', headers=user_2_auth)
    assert result.status_code == 403

    # admin delete user_2 (user_2 not in chat)
    result = client.delete(f'/chats/2/delete-user/{user_2_id}/', headers=chat_admin_auth)
    assert result.status_code == 200

    # admin delete user_1
    result = client.delete(f'/chats/2/delete-user/{user_1_id}/', headers=chat_admin_auth)
    assert result.status_code == 200

    result = client.get('/chats/2/users/', headers=chat_admin_auth).json()
    assert len(result) == 1

    # admin delete admin
    result = client.delete(f'/chats/2/delete-user/{chat_admin_id}/', headers=chat_admin_auth)
    assert result.status_code == 403


def test_exit_from_chat():
    #  /chats/2/exit/
    user_1 = client.post('/users/login/', json={'name': 'user_1',
                                                'password': '1234'}).json()
    user_1_auth = {'Authorization': f'Token {user_1["token"]}'}
    user_1_id = user_1['id']
    admin_chat = client.post('/users/login/', json={'name': 'chat-admin',
                                                    'password': '1234'}).json()
    admin_chat_auth = {'Authorization': f'Token {admin_chat["token"]}'}

    result = client.get(f'/chats/2/add-user/{user_1_id}/', headers=admin_chat_auth)

    assert result.status_code == 200

    result = client.get('/chats/2/users/', headers=admin_chat_auth).json()
    assert len(result) == 2

    #  user_1 exit from chat
    result = client.post('/chats/2/exit/', headers=user_1_auth)
    assert result.status_code == 200

    result = client.get('/chats/2/users/', headers=admin_chat_auth).json()
    assert len(result) == 1

    #  admin exit from chat
    result = client.post('/chats/2/exit/', headers=admin_chat_auth)
    assert result.status_code == 200


def test_delete_chat():
    #  /chats/{chat_id}/delete/
    user_1 = client.post('/users/login/', json={'name': 'user_1',
                                                'password': '1234'}).json()
    user_1_auth = {'Authorization': f'Token {user_1["token"]}'}

    admin_chat = client.post('/users/login/', json={'name': 'chat-admin',
                                                    'password': '1234'}).json()
    admin_chat_auth = {'Authorization': f'Token {admin_chat["token"]}'}

    chat = client.post('/chats/create/', data={'name': 'chat_11'}, headers=admin_chat_auth).json()
    chat__id = chat['id']

    #  user_1 delete chat (user_1 not chat creator)
    result = client.delete(f'/chats/{chat__id}/delete/', headers=user_1_auth)
    assert result.status_code == 403

    #  chat creator delete chat
    result = client.delete(f'/chats/{chat__id}/delete/', headers=admin_chat_auth)
    assert result.status_code == 200


def create_chat(admin_chat_auth, count) -> list[int]:
    """
    create {count} chats
    :return: list of id
    """
    id_list = []
    for i in range(count):
        chat = client.post('/chats/create/', data={'name': f'chat_{i}'}, headers=admin_chat_auth).json()
        id_list.append(chat['id'])

    return id_list


def add_user_to_chats(id_list: list[int], user_id, admin_chat_auth):
    for id in id_list:
        result = client.get(f'/chats/{id}/add-user/{user_id}', headers=admin_chat_auth)
        assert result.status_code == 200


def test_user_chats_list():
    user_1 = client.post('/users/login/', json={'name': 'user_1',
                                                'password': '1234'}).json()
    user_1_auth = {'Authorization': f'Token {user_1["token"]}'}

    admin_chat = client.post('/users/login/', json={'name': 'chat-admin',
                                                    'password': '1234'}).json()
    admin_chat_auth = {'Authorization': f'Token {admin_chat["token"]}'}

    #  create chats and add user to chats
    add_user_to_chats(create_chat(admin_chat_auth, 6), user_1['id'], admin_chat_auth)

    result = client.get('/chats/', headers=user_1_auth)
    assert result.status_code == 200
    assert len(result.json()) == 6
