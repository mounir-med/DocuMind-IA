from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import chat, conversations, dashboard, documents, health, settings
from app.core.config import get_settings
from app.core.db import init_db
from app.core.exceptions import register_exception_handlers

settings_obj = get_settings()
app = FastAPI(
    title=settings_obj.app_name,
    version=settings_obj.app_version,
    description="API RAG locale pour interroger des documents PDF.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings_obj.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
init_db()

app.include_router(health.router)
app.include_router(documents.router)
app.include_router(conversations.router)
app.include_router(chat.router)
app.include_router(dashboard.router)
app.include_router(settings.router)
