import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import streamlit as st
from config import FAMILY_PASSWORD
from src.rag_agent import RAGAgent

# Ustawienia Główne
st.set_page_config(
    page_title="Rodzina Karasi RAG Agent",
    page_icon='🌳',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# Custom CSS
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stChatMessage { margin: 1rem 0; }
    </style>
""", unsafe_allow_html=True)

# Autentykacja
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    
    if not st.session_state.password_correct:
        st.title("🔐 Rodzina Karasi Agent")
        password = st.text_input("Podaj Hasło:", type="password")
        
        if password:
            if password == FAMILY_PASSWORD:
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("❌ Nieprawidłowe Hasło")
        return False
    
    return True

# Main
if check_password():
    st.title("🌳 Rodzina Karasi Agent")
    st.write("Przeszukaj historię swojej rodziny - system analizuje zarówno prywatne dokumenty rodzinne, jak i zasoby internetu, aby znaleźć dodatkowy kontekst.")
    
    # Initialize RAG agent
    if "rag_agent" not in st.session_state:
        with st.spinner("Ładowanie Agenta..."):
            st.session_state.rag_agent = RAGAgent()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if user_input := st.chat_input("Zapytaj się..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Szukam..."):
                response = st.session_state.rag_agent.query(user_input)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})