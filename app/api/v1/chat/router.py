"""Chat API router."""

from fastapi import APIRouter

from app.api.v1.chat.endpoints import chat
from app.schemas.chat import ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])

router.add_api_route(
    "",
    chat,
    methods=["POST"],
    response_model=ChatResponse,
    summary="Chat with UNINASSAU Agent",
    description="Send a message to the UNINASSAU customer service agent.",
)
