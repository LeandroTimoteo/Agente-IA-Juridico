import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# 🔐 Carrega variáveis do .env
load_dotenv()

# ⚙️ Configuração da página
st.set_page_config(page_title="Agente de IA Jurídico", page_icon="⚖️")
st.title("⚖️ Agente de IA Jurídico")

# 🔑 Chave de API e modelo
api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
modelo_escolhido = os.getenv("DEFAULT_MODEL", "tngtech/deepseek-r1t2-chimera:free")

# 🚫 Verifica se a chave está presente
if not api_key:
    st.error("❌ Nenhuma chave de API encontrada. Configure OPENROUTER_API_KEY ou OPENAI_API_KEY.")
    st.stop()

# 🧠 Cliente OpenRouter
client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

# 🧹 Botão para limpar conversa
if st.button("🧹 Limpar conversa"):
    st.session_state.messages = []
    st.experimental_rerun()

# 💬 Histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 💬 Entrada do usuário
if prompt := st.chat_input("Como posso ajudar com sua consulta jurídica?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            with st.spinner("🔎 Consultando o agente jurídico..."):
                stream = client.chat.completions.create(
                    model=modelo_escolhido,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Você é um assistente jurídico prestativo e experiente. "
                                "Forneça informações jurídicas precisas e concisas, mas sempre aconselhe o usuário "
                                "a consultar um advogado qualificado para aconselhamento legal específico."
                            )
                        }
                    ] + [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )

                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"Ocorreu um erro ao gerar a resposta: {e}")
            full_response = (
                "⚠️ Desculpe, não consegui processar sua solicitação no momento. "
                "Por favor, tente novamente mais tarde."
            )
            message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

