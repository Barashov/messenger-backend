from fastapi import Request, HTTPException, WebSocket, WebSocketException, status
from core.logics.users import decode_id
from jwt import InvalidTokenError


async def auth(request: Request):
    """
    jwt auth
    """

    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        """ if headers is empty """
        raise HTTPException(status_code=401)
    auth_header = auth_header.split()

    if len(auth_header) != 2 or auth_header[0] != 'Token':
        raise HTTPException(status_code=401,
                            detail='invalid auth header')

    token = auth_header[1]

    try:
        return decode_id(token)['id']
    except InvalidTokenError:
        raise HTTPException(status_code=401,
                            detail='invalid token')


async def websocket_auth(websocket: WebSocket):
    await websocket.accept()
    token = await websocket.receive_text()
    if token is None:
        raise WebSocketException(code=1000, reason='token is none')

    if len(token.split()) != 2:
        raise WebSocketException(code=1000, reason='invalid token')

    try:
        return decode_id(token.split()[1])['id']
    except InvalidTokenError:
        raise WebSocketException(code=1000, reason='invalid token')
