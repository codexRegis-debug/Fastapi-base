# Main entrypoint
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from my_app.routers import auth
from my_app.data import my_base
from my_app.models import models
from my_app.core.users import fastapi_users, auth_backend
from my_app.services.realtime import manager, asyncpg
from fastapi import WebSocket

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

app = FastAPI(
    title = "My App",
    description="A multipurpose backend system",
)

origins = ["http://localhost:5173",]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods =["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers =["Authorization", "Content-Type", "X-Requested-With"],
)

@app.websocket("/realtime")   # Not sure if this should be here. Might migrate it to my_app.services.realtime.py later
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    conn = await asyncpg.connect(dsn = settings.DATABASE_URL.replace("+asyncpg", ""))
    await conn.add_listener('items', lambda *args: asyncio.create_task(manager.broadcast(args[2])))
    try:
        while True:
            await asyncio.sleep(1.5)
    finally:
        await conn.close()

app.include_router(auth.router, prefix="/api")

'''
app.include_router(
    fastapi_users.get_register_router(auth_backend),
    prefix = "/auth/jwt",
    tags = ["auth"],
)

app.include_router(
    fastapi_users.get_register_router(),
    prefix = "/auth",
    tags = ["auth"],
)

app.include_router(
    fastapi_users.get_users_register_router(),
    prefix = "/users",
    tags = ["users"],
)
'''

@app.get('/api')
async def get_message():
    return {
        "message": "working",
        "enviroment": "production"
    }

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
