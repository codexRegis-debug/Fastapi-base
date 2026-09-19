from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from my_app.routers import auth
from my_app.data import my_base
from my_app.models import models

# models.Base.metadata.create_all(bind=database.engine)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

app = FastAPI(
    title = "My App",
    description="A multipurpose backend system",
)

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods =["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers =["Authorization", "Content-Type", "X-Requested-With"],
)

app.include_router(auth.router, prefix="/api")

@app.get('/api')
async def get_message():
    return {
        "message": "working",
        "enviroment": "production"
    }

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
