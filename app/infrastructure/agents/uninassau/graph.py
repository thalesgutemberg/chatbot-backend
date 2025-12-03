"""UNINASSAU Customer Service Agent graph using LangGraph ReAct pattern."""

from functools import lru_cache

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from app.config import settings
from app.infrastructure.agents.uninassau.prompts import get_uninassau_system_prompt
from app.infrastructure.agents.uninassau.tools import UNINASSAU_TOOLS


@lru_cache(maxsize=1)
def _get_llm() -> ChatOpenAI:
    """Get LLM instance for UNINASSAU agent."""
    return ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0,  # Deterministic for tool usage
    )


@lru_cache(maxsize=1)
def _get_memory() -> MemorySaver:
    """Get memory saver for agent conversations."""
    return MemorySaver()


def get_uninassau_agent():  # type: ignore[no-untyped-def]
    """Get compiled UNINASSAU customer service agent using ReAct pattern.

    Note: Not cached to ensure system prompt always has current date.
    LLM and memory are still cached for efficiency.

    Returns:
        Compiled ReAct agent with UNINASSAU tools and memory
    """
    return create_react_agent(
        model=_get_llm(),
        tools=UNINASSAU_TOOLS,
        prompt=get_uninassau_system_prompt(),
        checkpointer=_get_memory(),
    )
