from fastapi import WebSocket


class ChatManager:
    connections: dict[int, dict] = {}

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
