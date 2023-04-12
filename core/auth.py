from fastapi import Request, HTTPException
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
        return decode_id(token)
    except InvalidTokenError:
        raise HTTPException(status_code=401,
                            detail='invalid token')

