from fastapi import APIRouter, WebSocket, status, WebSocketException, Depends
from core.crud.chats import is_user_in_chat
from core.auth import websocket_auth
from core.manager import ChatManager
from core.crud.messages import create_message
"""
websocket manager, endpoint
chat messages functional
"""


router = APIRouter()
chat_manager = ChatManager()


@router.websocket('/{chat_id}/connect/')
async def chat_endpoint(websocket: WebSocket,
                        chat_id: int,
                        user_id: int = Depends(websocket_auth)):

    user_in_chat = await is_user_in_chat(chat_id, user_id)

    if not user_in_chat:
        raise WebSocketException(code=status.WS_1000_NORMAL_CLOSURE,
                                 reason='user not in chat')
    chat_manager.connect(chat_id, user_id, websocket)
    try:
        while True:
            message = await websocket.receive_json()
            if not chat_manager.is_user_in_chat(chat_id, user_id):
                raise WebSocketException(code=1000, reason='user not in chat')

            #  save message
            await chat_manager.send_message(chat_id, message)
    finally:
        chat_manager.disconnect(chat_id, user_id)
