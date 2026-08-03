import sys
import os

from src.application.ai_services import AIService
from src.presentation.components.chat_interface import ChatVisualizer

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, project_root)
import streamlit as st

def main():
    ai_service = AIService()
    chat_vis = ChatVisualizer()

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    chat_vis.render_chat_history(st.session_state.messages)

    if user_query := st.chat_input("Ask something"):
        st.session_state.messages.append({'role':'user', 'content': user_query})
        with st.chat_message('user'):
            st.markdown(user_query)

        response = ai_service.get_financial_insight(user_query,'March', '2026')
        st.session_state.messages.append({'role': 'assistant', 'content': response})
        with st.chat_message('assistant'):
            st.markdown(response)

if __name__ == '__main__':
   main()
