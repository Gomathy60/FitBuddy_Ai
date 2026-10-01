from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import init_db
from app.config import settings
from app.routes import r
@asynccontextmanager
async def lifespan(app): init_db(); yield
app=FastAPI(title=settings.APP_NAME,version='1.0.0',lifespan=lifespan)
app.mount('/static',StaticFiles(directory='app/static'),name='static'); app.include_router(r)
