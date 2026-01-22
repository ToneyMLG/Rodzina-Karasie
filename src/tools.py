import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from duckduckgo_search import DDGS


def search_family_docs(query: str, vectorstore) -> str:
    """Search family document for information about lineage, ancestors, dates, events, etc."""
    results = vectorstore.similarity_search(query, k=3)
    if not results:
        return "No relevant information found in family documents."
    
    context = "\n---\n".join([doc.page_content for doc in results])
    return f"Found in family documents:\n{context}"

def search_web(query: str) -> str:
    """Search internet for historical/genealogical information to supplement family knowledge"""
    try:
        ddgs = DDGS()
        results = ddgs.text(query, max_results=5)
        
        if not results:
            return "No web results found."
        
        web_content = "\n---\n".join([
            f"Title: {r['title']}\nContent: {r['body'][:300]}..."
            for r in results
        ])
        return f"Found on web:\n{web_content}"
    except Exception as e:
        return f"Web search error: {str(e)}"