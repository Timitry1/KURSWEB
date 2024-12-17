from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json

app = FastAPI()

# Статические файлы для фронтенда
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
async def get_root():
    return FileResponse("frontend/index.html")


# Подключенные клиенты
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data: str):
        for connection in self.active_connections:
            await connection.send_text(data)


manager = ConnectionManager()


# WebSocket для обмена данными о рисовании
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)  # Рассылаем данные всем клиентам
    except WebSocketDisconnect:
        manager.disconnect(websocket)
