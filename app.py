import os
import streamlit as st
from openai import OpenAI

API_KEY = os.environ["PERPLEXITY_API_KEY"]

client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

# Set page config
st.set_page_config(
    page_title="Perplexity.ai API demo",
    page_icon="🤖",
)

st.title("Perplexity.ai API demo")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("Clear chat history"):
    st.session_state.messages = []
    st.rerun()

# Give user a text box to enter system prompt
system_prompt = st.text_area("(Optional) Customize the system prompt, then proceed to send your message at the bottom of the screen", value="You are a helpful assistant.")

# Main container area where the chat will be displayed
messages_container = st.container()

# Render past messages
with messages_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat prompt
if prompt := st.chat_input():
    with messages_container:
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get response from API call
        with st.chat_message("assistant"):
            response_stream = client.chat.completions.create(
                model="llama-3-sonar-large-32k-online",
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
                stream=True
            )
            response = st.write_stream(response_stream)

        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})