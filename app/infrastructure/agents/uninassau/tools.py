"""UNINASSAU Customer Service tools using Tavily for web search."""

from datetime import datetime

from langchain_core.tools import tool
from tavily import TavilyClient

from app.config import settings
from app.infrastructure.agents.uninassau.rag import (
    search_knowledge_base as _search_kb,
)


def _get_tavily_client() -> TavilyClient:
    """Get Tavily client instance."""
    return TavilyClient(api_key=settings.tavily_api_key)


def _get_year_context() -> str:
    """Get current year for search queries."""
    return str(datetime.now().year)


def _format_search_results(results: list[dict[str, str]]) -> str:
    """Format Tavily search results into readable text."""
    if not results:
        return "Nenhum resultado encontrado."

    formatted = []
    for i, result in enumerate(results[:5], 1):
        title = result.get("title", "Sem titulo")
        content = result.get("content", "Sem descricao")
        url = result.get("url", "")
        formatted.append(f"{i}. **{title}**\n   {content}\n   Fonte: {url}")

    return "\n\n".join(formatted)


@tool
def search_uninassau_web(query: str) -> str:
    """Busca informacoes no site da UNINASSAU.

    Use para encontrar informacoes sobre cursos, vestibular, valores,
    campus, contato e outras informacoes institucionais.

    Args:
        query: Termo de busca (ex: "cursos de tecnologia", "vestibular 2025")

    Returns:
        Resultados formatados com informacoes da UNINASSAU
    """
    try:
        client = _get_tavily_client()
        year = _get_year_context()
        response = client.search(
            query=f"site:uninassau.edu.br {query} {year}",
            search_depth="basic",
            max_results=5,
            include_domains=["uninassau.edu.br"],
        )
        return _format_search_results(response.get("results", []))
    except Exception as e:
        return f"Nao foi possivel buscar informacoes: {e}"


@tool
def fetch_uninassau_page(url: str) -> str:
    """Busca conteudo de uma pagina especifica da UNINASSAU.

    Use quando precisar de informacoes detalhadas de uma URL conhecida.
    A URL DEVE ser do dominio uninassau.edu.br.

    Args:
        url: URL completa da pagina (ex: "https://www.uninassau.edu.br/cursos")

    Returns:
        Conteudo extraido da pagina
    """
    if "uninassau.edu.br" not in url:
        return "Erro: URL deve ser do dominio uninassau.edu.br"

    try:
        client = _get_tavily_client()
        response = client.extract(urls=[url])

        if response.get("results"):
            result = response["results"][0]
            content = result.get("raw_content", result.get("content", ""))
            if content:
                # Truncate if too long
                if len(content) > 3000:
                    content = content[:3000] + "... [conteudo truncado]"
                return f"Conteudo de {url}:\n\n{content}"

        return f"Nao foi possivel extrair conteudo de {url}"
    except Exception as e:
        return f"Erro ao buscar pagina: {e}"


@tool
def search_knowledge_base(query: str) -> str:
    """Busca na base de conhecimento local da UNINASSAU.

    IMPORTANTE: SEMPRE use esta ferramenta PRIMEIRO antes de qualquer outra busca.
    Esta e a fonte PRIMARIA e OFICIAL de informacoes da UNINASSAU.

    Contem informacoes sobre:
    - Telefones e contatos oficiais (0800, WhatsApp)
    - Enderecos dos campus
    - Cursos de graduacao e pos-graduacao
    - Vestibular e processo seletivo
    - Valores, bolsas e financiamento
    - Informacoes institucionais

    Args:
        query: Termo de busca (ex: "telefone geral", "cursos de engenharia")

    Returns:
        Documentos relevantes da base de conhecimento oficial.
        Se retornar "Nenhum documento relevante encontrado", entao use search_uninassau_web.
    """
    result = _search_kb(query)
    if result == "Nenhum documento relevante encontrado na base de conhecimento.":
        return "Nenhum documento relevante encontrado na base local. Use search_uninassau_web como alternativa."
    return f"[RESULTADO DA BASE OFICIAL]\n{result}\n[FIM DO RESULTADO]"


# Export all tools as a list for easy binding
# IMPORTANT: search_knowledge_base is FIRST - agent should use it before web search
UNINASSAU_TOOLS = [search_knowledge_base, search_uninassau_web, fetch_uninassau_page]
