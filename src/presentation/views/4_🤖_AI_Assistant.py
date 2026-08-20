import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, project_root)

from src.application.ai_services.ai_service import AIService
from src.presentation.components.chat_interface import ChatVisualizer
import streamlit as st
from google.genai.errors import ServerError, ClientError
from dotenv import load_dotenv

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

def main():
    st.title("AI Finance Assistant 🤖")
    if not st.session_state.is_file_uploaded:
        st.error("Please upload your transaction file from '📁 Data Management'.")
        st.stop()

    load_dotenv()

    ## Since the process for obtaining an API key varies depending on the environment, it is stored using `session_state`.
    if "api_key" not in st.session_state: ## This condition means that the AI Assistant tab is being opened for the first time (regardless of the environment)
        current_api_key = os.getenv("GEMINI_API_KEY")
        if current_api_key: ## If an API key is found in the .env file, the process continues without any issues
            st.session_state.api_key = current_api_key
        else: ## If it cannot be found, you will be prompted to enter the API key manually
            col1, col2 = st.columns(2)
            with col1:
                st.info("You are running this app on a local environment."
                        " Please enter your Gemini API Key.")
                current_api_key = st.text_input("Your Gemini API Key: ", type="password")

            with col2:
                with st.container(border=False):
                    st.warning("If you don't have an API Key, you can get one for free from the link below:")
                    st.link_button("🔑 Get Gemini API Key", "https://aistudio.google.com/app/api-keys",
                                   use_container_width=True)

            if not current_api_key:
                st.stop()
            if current_api_key:
                st.session_state.api_key = current_api_key
                st.rerun()

    else: ## If this is not the first time accessing the AI Assistant tab (if the API key is stored in session_state)
        if st.session_state.api_key == os.getenv("GEMINI_API_KEY"):
            ai_service = AIService()
        else:
            ai_service = AIService(provided_api_key = st.session_state.api_key)

    ## Chat history is displayed here
    chat_vis = ChatVisualizer()

    if 'timeframe' not in st.session_state:
        st.session_state.timeframe = 'ALL'

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    chat_vis.render_chat_history(st.session_state.messages)

    ## User query is received and displayed here
    if user_query := st.chat_input("Ask something"):
        st.session_state.messages.append({'role':'user', 'content': user_query})
        with st.chat_message('user'):
            st.markdown(user_query)

        try: ## LLM response is received and displayed here
            response, timeframe = ai_service.get_financial_insight(user_query, st.session_state.timeframe)
            st.session_state.timeframe = timeframe
            st.session_state.messages.append({'role': 'assistant', 'content': response})
            with st.chat_message('assistant'):
                st.markdown(response)

        ## Various error checks are performed here.
        ## Since the source of the error is not always the user, accurate error messages are important.
        except ServerError:
            error_message = "AI Assistant is not available at this moment. Please try again a few minutes later."
            st.session_state.messages.append({'role': 'assistant', 'content': error_message})
            with st.chat_message('assistant'):
                st.markdown(error_message)

        except ClientError as e:
            error_str = str(e).lower()
            if "429" in error_str:
                if 'minute' in error_str:
                    error_message = "You hit the speed limit per minute. Please try again 1 minute later."
                elif 'day' in error_str or 'daily' in error_str:
                    error_message = "You have reached daily AI Assistant chat limit. Please try again tomorrow."
                else:
                    error_message = "Too many request! This Assistant is tired. Please wait a while and try again later."

            else:
                error_message = "Unexpected client error. Did you enter your API Key?"
            st.session_state.messages.append({'role': 'assistant', 'content': error_message})
            with st.chat_message('assistant'):
                st.markdown(error_message)

main()