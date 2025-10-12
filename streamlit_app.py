import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# 🔹 Carrega variáveis do .env (apenas local; no Streamlit Cloud use Secrets)
load_dotenv()

# 🔹 Configuração da página Streamlit
st.set_page_config(page_title="Agente de IA Jurídico", page_icon="⚖️")
st.title("⚖️ Agente de IA Jurídico")

# 🔹 Recupera a chave da API (funciona tanto local quanto no Streamlit Cloud)
api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ Nenhuma chave de API encontrada. Configure OPENROUTER_API_KEY ou OPENAI_API_KEY.")
    st.stop()

# 🔹 Inicializa o cliente OpenRouter
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# 🔹 Modelos gratuitos disponíveis no OpenRouter
MODELOS = [
    "deepseek/deepseek-v3.2-exp",
    "deepseek/deepseek-v3",
    "deepseek/deepseek-r1",
    "deepseek/deepseek-r1-0528"
]

# 🔹 Seletor de modelo no sidebar
st.sidebar.header("⚙️ Configurações")
modelo_escolhido = st.sidebar.selectbox("Escolha o modelo:", MODELOS, index=2)

# 🔹 Inicializa o histórico de chat no session_state do Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔹 Exibe mensagens anteriores do chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 🔹 Lógica para nova entrada do usuário
if prompt := st.chat_input("Como posso ajudar com sua consulta jurídica?"):
    # Armazena a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta do assistente
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            stream = client.chat.completions.create(
                model=modelo_escolhido,
                messages=[
                    {"role": "system", "content": "Você é um assistente jurídico prestativo e experiente. Forneça informações jurídicas precisas e concisas, mas sempre aconselhe o usuário a consultar um advogado qualificado para aconselhamento legal específico."}
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
            full_response = "⚠️ Desculpe, não consegui processar sua solicitação no momento. Por favor, tente novamente mais tarde."
            message_placeholder.markdown(full_response)

    # Armazena a resposta no histórico
    st.session_state.messages.append({"role": "assistant", "content": full_response})


