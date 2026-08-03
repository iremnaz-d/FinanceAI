import streamlit as st

class ChatVisualizer:

    def render_chat_history(self, messages):
        for message in messages:
            with st.chat_message(message['role']):
                st.markdown(message['content'])

