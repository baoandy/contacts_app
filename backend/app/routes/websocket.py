from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket_connection_manager import manager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    print("New WebSocket connection attempt")
    await manager.connect(websocket, user_id)
    try:
        print(f"WebSocket connected from {websocket.client.host}")
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
    except WebSocketDisconnect:
        print(f"WebSocket disconnected from {websocket.client.host}")
        await manager.disconnect(user_id)
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        await manager.disconnect(user_id)


        