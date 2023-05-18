from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List, Dict, Union
from threading import Thread
import asyncio
from pydantic import BaseModel
from starlette.websockets import WebSocket, WebSocketState
from w2.utils.websocket import ConnectionManager
from w2.utils.response_model import ProcessStatus
from w2.utils.database import DB

app = FastAPI()
manager = ConnectionManager()

# start an asynchronous task that will keep broadcasting the process status to all the connected clients
broadcast_continuous = Thread(
    target=asyncio.run, args=(manager.broadcast_all(),))
broadcast_continuous.start()


# The below endpoint is used to create websocket connection
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # create a websocket connection for a client and assign it to a room
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast message to all the connections/clients in a chatroom
            await websocket.send_text(f"Websocket connection established Connected")

    except WebSocketDisconnect:
        print("Client disconnected")


# health check API
@app.get("/health")
async def get() -> Dict:
    """
    should send a JSON response in the below format:
    {"status": "ok"}
    """

    ######################################## YOUR CODE HERE ##################################################
    return {"status": "ok"}
    ######################################## YOUR CODE HERE ##################################################


# Below endpoint renders an HTML page
@app.get("/")
async def get() -> HTMLResponse:
    """
    should render the HTML file - indsex.html when a user goes to http://127.0.0.1:8000/
    """
    ######################################## YOUR CODE HERE ##################################################
    with open('./index.html', 'r') as f:
        html = f.read()

    # Render an HTML page
    return HTMLResponse(html)
    ######################################## YOUR CODE HERE ##################################################


# Below endpoint to get the initial data
@app.get("/processes")
async def get() -> List[ProcessStatus]:
    """
    Get all the records from the process table and return it using the pydantic model ProcessStatus
    """
    ######################################## YOUR CODE HERE ##################################################
    db = DB()
    processes = db.read_all()
    print(processes)
    # create table if not exists TableName (col1 typ1, ..., colN typN)# create a table
    return [ProcessStatus(**proc) for proc in processes]

    ######################################## YOUR CODE HERE ##################################################
