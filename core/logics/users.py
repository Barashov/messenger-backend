import hashlib
from core.config import settings
from core.crud.users import get_user_by_email, get_user_by_username
from core.schemas import users as users_schemas
import jwt


def hash_password(password: str):
    return hashlib.pbkdf2_hmac('sha256',
                               password.encode('utf-8'),
                               settings.salt.encode('utf-8'),
                               10000)


def is_passwords_equal(password, hashed_password):
    return hash_password(password) == hashed_password


def encode_id(user_id):
    return jwt.encode({'id': user_id},
                      settings.key,
                      algorithm='HS256')


def decode_id(token):
    return jwt.decode(token, settings.key, algorithms='HS256')


async def authenticate(user_in: users_schemas.UserLogin):
    name = user_in.name
    if '@' in name:
        user = await get_user_by_email(name)

    else:
        user = await get_user_by_username(name)

    if user is not None and is_passwords_equal(user_in.password, user.password):
        return user

