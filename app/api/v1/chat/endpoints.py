"""Chat API endpoints."""

import logging

from langchain_core.messages import HumanMessage

from app.infrastructure.agents.uninassau import get_uninassau_agent
from app.schemas.chat import ChatInput, ChatResponse

logger = logging.getLogger(__name__)


async def chat(request: ChatInput) -> ChatResponse:
    """Chat with the UNINASSAU customer service agent (public endpoint).

    The agent will use its tools in priority order:
    1. search_knowledge_base (local KB) - FIRST
    2. search_uninassau_web (web search) - fallback
    3. fetch_uninassau_page (specific URLs)

    The agent can help with:
    - Course information
    - Admission process
    - Tuition and financial aid
    - Campus information
    - Contact details
    """
    agent = get_uninassau_agent()
    config = {"configurable": {"thread_id": request.thread_id}}

    # Pass message directly - agent decides which tools to use
    result = await agent.ainvoke(
        {"messages": [HumanMessage(content=request.message)]},
        config=config,
    )

    # Debug: log all messages and tool calls
    for i, msg in enumerate(result["messages"]):
        msg_type = type(msg).__name__
        tool_calls = getattr(msg, "tool_calls", None)
        if tool_calls:
            logger.info(f"[{i}] {msg_type}: tool_calls={[tc['name'] for tc in tool_calls]}")
        else:
            content_preview = str(getattr(msg, "content", ""))[:100]
            logger.info(f"[{i}] {msg_type}: {content_preview}")

    ai_message = result["messages"][-1]
    response_content = (
        ai_message.content if hasattr(ai_message, "content") else str(ai_message)
    )

    return ChatResponse(
        response=response_content,
        thread_id=request.thread_id,
    )
