import streamlit as st
from openai import OpenAI

# Configuração da página Streamlit
st.set_page_config(page_title="Agente de IA Jurídico", page_icon="⚖️")
st.title("⚖️ Agente de IA Jurídico")

# Inicializa o cliente OpenAI
# A chave da API e a URL base são carregadas automaticamente do ambiente
client = OpenAI()

# Inicializa o histórico de chat no session_state do Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens anteriores do chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Lógica para nova entrada do usuário
if prompt := st.chat_input("Como posso ajudar com sua consulta jurídica?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            stream = client.chat.completions.create(
                model="gemini-2.5-flash", # Ou outro modelo disponível como gpt-4.1-mini, gpt-4.1-nano
                messages=[
                    {"role": "system", "content": "Você é um assistente jurídico prestativo e experiente. Forneça informações jurídicas precisas e concisas, mas sempre aconselhe o usuário a consultar um advogado qualificado para aconselhamento legal específico."}
                ] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            for chunk in stream:
                full_response += chunk.choices[0].delta.content or ""
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Ocorreu um erro ao gerar a resposta: {e}")
            full_response = "Desculpe, não consegui processar sua solicitação no momento. Por favor, tente novamente mais tarde."
            message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

