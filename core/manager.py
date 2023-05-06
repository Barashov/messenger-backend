from fastapi import WebSocket, WebSocketException


class ChatManager:
    connections: dict[int, dict[int, WebSocket]] = {}

    def connect(self,
                chat_id: int,
                user_id: int,
                websocket: WebSocket):

        if self.connections.get(chat_id) is None:
            self.connections[chat_id] = dict()
        self.connections[chat_id][user_id] = websocket

    def disconnect(self,
                   chat_id: int,
                   user_id: int):
        try:
            del self.connections[chat_id][user_id]
        except KeyError:
            pass

    def is_user_in_chat(self,
                        chat_id: int,
                        user_id: int):
        try:
            return bool(self.connections[chat_id][user_id])
        except KeyError:
            return False

    async def send_message(self, chat_id, message):
        websockets = self.connections[chat_id].values()
        for websocket in websockets:
            await self.send_message_to_websocket(websocket, message)

    @staticmethod
    async def send_message_to_websocket(websocket: WebSocket, message):
        await websocket.send_json(message)
