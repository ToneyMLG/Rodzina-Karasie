from typing import TypedDict, Annotated
import operator
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from config import  OPENAI_API_KEY, CHROMA_DB_DIR, CHUNK_SIZE, CHUNK_OVERLAP, LLM_MODEL, LLM_TEMPERATURE, VECTOR_SEARCH_K
from src.doc_processor import extract_text_from_doc, chunk_text
from src.tools import search_family_docs, search_web


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    query: str


class RAGAgent:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            api_key=OPENAI_API_KEY
        )
        self.vectorstore = None
        self.graph = None
        self._initialize_vectorstore()
        self._build_graph()
    
    def _initialize_vectorstore(self):
        """Load or create vector database"""
        try:
            self.vectorstore = Chroma(
                persist_directory=CHROMA_DB_DIR,
                embedding_function=self.embeddings
            )
            collection = self.vectorstore.get()
            if collection["ids"]:
                print("✓ Vector DB loaded from cache")
            else:
                raise Exception("Empty DB, rebuilding...")
        except:
            print("Building vector DB from DOC...")
            text = extract_text_from_doc()
            chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
            self.vectorstore = Chroma.from_texts(
                chunks,
                self.embeddings,
                persist_directory=CHROMA_DB_DIR
            )
            print("✓ Vector DB created and saved")
    
    def _build_graph(self):
        """Build LangGraph agent"""

        # System message dla RAG-a
        SYSTEM_MESSAGE = """Jesteś ekspertem genealogii rodziny Karasiów. 
        Odpowiadaj konkretnie, odwołując się do dokumentów rodzinnych.
        Jeśli czegość nie wiesz z dostępnych źródeł, powiedz to jasno."""
        
        # Stwórz Narzędzia
        def family_docs_search(query: str) -> str:
            """Search family documents for lineage information."""
            return search_family_docs(query, self.vectorstore)
        
        tools = [family_docs_search, search_web]
        
        # Bind Narzędzi
        self.llm_with_tools = self.llm.bind_tools(tools)
        
        # Agent
        def agent_node(state: AgentState):
        # Dodaj System Message na początek konwersacji
            messages = [SystemMessage(content=SYSTEM_MESSAGE)] + state["messages"]
            response = self.llm_with_tools.invoke(messages)
            return {"messages": [response]}
        
        # Tool node
        tool_node = ToolNode(tools)
        
        # Graph
        graph = StateGraph(AgentState)
        graph.add_node("agent", agent_node)
        graph.add_node("tools", tool_node)
        
        graph.set_entry_point("agent")
        
        # Route
        def should_continue(state: AgentState):
            messages = state["messages"]
            last_message = messages[-1]
            
            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                return "tools"
            return "__end__"
        
        graph.add_conditional_edges("agent", should_continue)
        graph.add_edge("tools", "agent")
        
        self.graph = graph.compile()
    
    def query(self, user_query: str) -> str:
        """Run RAG agent with user query"""
        result = self.graph.invoke({
            "messages": [HumanMessage(content=user_query)],
            "query": user_query
        })
        
        # Ekstrajtuj finalną Wiadomość
        last_message = result["messages"][-1]
        if isinstance(last_message, AIMessage):
            return last_message.content
        return str(last_message)