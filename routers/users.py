from fastapi.routing import APIRouter
from fastapi import HTTPException, Depends
from core.schemas.users import UserCreate, UserLogin, UserOut
from core.crud import users as users_crud
from core.logics.users import hash_password, authenticate
from core.logics.users import encode_id
from core.auth import auth


router = APIRouter()


@router.post('/sign-up/', status_code=200, response_model=UserOut)
async def sign_up(user: UserCreate):

    is_username_taken = await users_crud.is_username_taken(user.username)
    if is_username_taken:
        raise HTTPException(status_code=401, detail='username is already taken')

    hashed_password = hash_password(user.password)
    db_user_id = await users_crud.create_user(username=user.username,
                                              hashed_password=hashed_password)
    return {'id': db_user_id,
            'username': user.username,
            'token': encode_id(db_user_id)}


@router.post('/login/', status_code=200, response_model=UserOut)
async def login(user: UserLogin):
    user = await authenticate(user)

    if user is None:
        raise HTTPException(status_code=401, detail='the name or password in incorrect')

    return {'id': user.id,
            'username': user.username,
            'token': encode_id(user.id)}


@router.post('/is-auth/', status_code=200)
async def is_auth(user_id: int = Depends(auth)):
    return user_id
