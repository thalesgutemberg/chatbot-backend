"""Simple RAG with BM25 search for knowledge base."""

from pathlib import Path

from rank_bm25 import BM25Okapi

# Path to knowledge base directory
KNOWLEDGE_BASE_PATH = Path(__file__).parents[4] / "knowledge_base"


def _load_documents() -> list[dict[str, str]]:
    """Load all markdown files from knowledge base."""
    documents: list[dict[str, str]] = []

    if not KNOWLEDGE_BASE_PATH.exists():
        return documents

    for md_file in KNOWLEDGE_BASE_PATH.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        documents.append({
            "source": md_file.stem,
            "content": content,
        })

    return documents


def _tokenize(text: str) -> list[str]:
    """Simple tokenization: lowercase and split by whitespace/punctuation."""
    # Remove common markdown chars and split
    text = text.lower()
    for char in ["#", "*", "-", "_", "`", "[", "]", "(", ")", ":"]:
        text = text.replace(char, " ")
    return text.split()


def search_knowledge_base(query: str, top_k: int = 3) -> str:
    """Search knowledge base using BM25 algorithm.

    Args:
        query: Search query
        top_k: Number of top results to return

    Returns:
        Formatted string with relevant document excerpts
    """
    documents = _load_documents()

    if not documents:
        return "Base de conhecimento vazia ou nao encontrada."

    # Tokenize all documents
    tokenized_docs = [_tokenize(doc["content"]) for doc in documents]

    # Create BM25 index
    bm25 = BM25Okapi(tokenized_docs)

    # Tokenize query and search
    query_tokens = _tokenize(query)
    scores = bm25.get_scores(query_tokens)

    # Get top-k results
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    top_indices = ranked_indices[:top_k]

    # Format results
    results: list[str] = []
    for idx in top_indices:
        if scores[idx] > 0:  # Only include if there's any match
            doc = documents[idx]
            # Truncate content if too long
            content = doc["content"][:2000]
            if len(doc["content"]) > 2000:
                content += "..."
            results.append(f"## Fonte: {doc['source']}\n\n{content}")

    if not results:
        return "Nenhum documento relevante encontrado na base de conhecimento."

    return "\n\n---\n\n".join(results)
