from typing import Set
from fastapi import WebSocket
from enum import Enum
from app.db.models import Contact, ContactVersion, User

class WebSocketAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

class ConnectionManager:
    def __init__(self):
        # Maps user_id to WebSocket
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def broadcast_message(self, message: dict, user_id: int):
        for connected_user_id, websocket in self.active_connections.items():
            try:
                # Don't send the message to the user who made the action
                if connected_user_id == user_id:
                    continue
                await websocket.send_json(message)
            except Exception as e:
                print(f"Error broadcasting message: {e}")
                continue

    async def broadcast_create_contact(self, contact: Contact, user: User):
        message = {
            "action": WebSocketAction.CREATE,
            "contact": contact.to_dict(),
            "actionBy": user.username
        }
        await self.broadcast_message(message, user.id)
    
    async def broadcast_update_contact(self, contact_version: ContactVersion, user: User):
        message = {
            "action": WebSocketAction.UPDATE,
            "contactVersion": contact_version.to_dict(),
            "actionBy": user.username
        }
        await self.broadcast_message(message, user.id)

    async def broadcast_delete_contact(self, contact_id: int, first_name: str, last_name: str, user: User):
        message = {
            "action": WebSocketAction.DELETE,
            "contactId": contact_id,
            "firstName": first_name,
            "lastName": last_name,
            "actionBy": user.username
        }
        await self.broadcast_message(message, user.id)
    

# Global instance to be used across the application
manager = ConnectionManager() 