from fastapi import APIRouter, Request, Depends, Form, HTTPException

from core.crud.chats import create_chat, add_user_to_chat, is_user_in_chat
from core.crud.chats import get_list_of_chat_users
from core.logics.images import save_image
from core.auth import auth
from core.schemas.chats import ChatCreateOut
from core.schemas.users import UserInfo


router = APIRouter()


@router.post('/create/', status_code=201, response_model=ChatCreateOut)
async def create(request: Request,
                 user_id: int = Depends(auth),
                 name: str = Form()):

    form = await request.form()
    image = form.get('image')

    image_path = None

    if image:
        image_path = await save_image(image, 'chat_images')

    chat = await create_chat(name,
                             user_id,
                             image_path)

    await add_user_to_chat(chat, user_id)

    return {'id': chat,
            'name': name,
            'image': image_path}


@router.get('/{chat_id}/add-user/{adding_user_id}/', status_code=200)
async def add_user(chat_id: int,
                   adding_user_id: int,
                   user_id: int = Depends(auth)):
    user_in_chat = await is_user_in_chat(chat_id, user_id)
    if not user_in_chat:
        raise HTTPException(status_code=403, detail='user not in chat')
    is_adding_user_in_chat = await is_user_in_chat(chat_id, adding_user_id)
    if is_adding_user_in_chat:
        return 200
    await add_user_to_chat(chat_id, adding_user_id)
    return 200


@router.get('/{chat_id}/users', response_model=list[UserInfo])
async def users_of_chat(chat_id,
                        user_id: int = Depends(auth)):
    is_chat_user = await is_user_in_chat(chat_id, user_id)
    if not is_chat_user:
        raise HTTPException(status_code=403, detail='user not in chat')

    users = await get_list_of_chat_users(chat_id)
    return users
