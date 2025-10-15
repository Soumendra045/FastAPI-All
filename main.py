from fastapi import FastAPI,Request
from router import blog_get,blog_post,user,article,product,file
from auth import authentication
from db.database import engine 
from db import models
from exceptions import StoryException
from fastapi import Request,status
from fastapi.responses import JSONResponse,HTMLResponse
from fastapi.staticfiles import StaticFiles
from template import template
import time
from client import html
from fastapi.websockets import WebSocket

app = FastAPI()
app.include_router(template.router)
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(product.router)

@app.exception_handler(StoryException)
def story_exception_handler(request: Request,exc: StoryException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={'details': exc.name}
    )

@app.get("/")
async def get():
    return HTMLResponse(html)

clients = []

@app.websocket('/chat')
async def websocket_endpoiont(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in clients:
            await client.send_text(data)


@app.middleware("http")
async def add_middleware(request: Request,call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time()- start_time
    response.headers['duration'] = str(duration)
    return response
# @app.exception_handler(HTTPException)
# def custom_handler(request: Request,exc: StoryException):
#     return PlainTextResponse(str(exc),status_code=status.HTTP_400_BAD_REQUEST)

models.Base.metadata.create_all(engine)

app.mount('/files',StaticFiles(directory='files'),name='files')
app.mount("/static", StaticFiles(directory="template/static"), name="static")