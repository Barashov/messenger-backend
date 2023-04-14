from fastapi import APIRouter, Request, Depends, Form

from core.crud.chats import create_chat
from core.logics.images import save_image
from core.auth import auth
from core.schemas.chats import ChatCreateOut


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
    return {'id': chat,
            'name': name,
            'image': image_path}
