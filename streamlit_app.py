import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load local environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="Legal AI Agent", page_icon="⚖️")
st.title("⚖️ Legal AI Agent")

# Keys and model (Cloud → st.secrets, Local → .env)
api_key = st.secrets.get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
chosen_model = st.secrets.get("DEFAULT_MODEL") or os.getenv("DEFAULT_MODEL", "tngtech/deepseek-r1t2-chimera:free")
admin_mode = st.secrets.get("ADMIN_MODE") or os.getenv("ADMIN_MODE", "false")

if not api_key:
    st.error("❌ No API key found. Please configure OPENROUTER_API_KEY or OPENAI_API_KEY.")
    st.stop()

# OpenRouter client
client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

# Button to clear conversation
if st.button("🧹 Clear conversation"):
    st.session_state.messages = []
    st.rerun()

# Conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("How can I assist with your legal inquiry?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            with st.spinner("🔎 Consulting the legal agent..."):
                stream = client.chat.completions.create(
                    model=chosen_model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a helpful and experienced legal assistant. "
                                "Provide accurate and concise legal information, but always advise the user "
                                "to consult a qualified lawyer for specific legal advice."
                            ),
                        }
                    ] + st.session_state.messages,
                    stream=True,
                )

                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")
            full_response = (
                "⚠️ Sorry, I couldn't process your request at the moment. Please try again later."
            )
            message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

