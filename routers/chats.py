from fastapi import APIRouter, Request, Depends, Form, HTTPException

from core.crud.chats import create_chat, add_user_to_chat, is_user_in_chat
from core.crud.chats import delete_chat, delete_user_from_chat
from core.crud.chats import get_list_of_chat_users, get_user_chats
from core.logics.images import save_image
from core.logics.chats import is_user_chat_creator
from core.auth import auth
from core.schemas.chats import ChatCreateOut, FullChat
from core.schemas.users import UserInfo
from routers.chat import router as chat_router
from routers.chat import chat_manager

router = APIRouter()
router.include_router(chat_router)


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


@router.delete('/{chat_id}/delete-user/{user_id}/', status_code=200)
async def delete_user(chat_id: int,
                      user_id: int,
                      chat_creator_id: int = Depends(auth)):
    if user_id == chat_creator_id:
        raise HTTPException(status_code=403,
                            detail="chat creator can't delete himself")
    user_creator = await is_user_chat_creator(chat_id, chat_creator_id)
    if user_creator:
        await delete_user_from_chat(chat_id, user_id)
        chat_manager.disconnect(chat_id, user_id)
        return 200

    raise HTTPException(status_code=403, detail='user is not chat creator')


@router.post('/{chat_id}/exit/', status_code=200)
async def exit_from_chat(chat_id: int,
                         user_id: int = Depends(auth)):
    await delete_user_from_chat(chat_id, user_id)
    chat_manager.disconnect(chat_id, user_id)
    return 200


@router.delete('/{chat_id}/delete/', status_code=200)
async def delete(chat_id: int,
                 user_id: int = Depends(auth)):
    user_chat_creator = await is_user_chat_creator(chat_id, user_id)
    if user_chat_creator:
        await delete_chat(chat_id)
        return 200
    raise HTTPException(status_code=403)


@router.get('/', status_code=200, response_model=list[FullChat])
async def user_chats(user_id: int = Depends(auth)):
    chats = await get_user_chats(user_id)
    return chats
