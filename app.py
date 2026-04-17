import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="CodeSmith AI", page_icon="🤖")

client = OpenAI(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    mode = st.selectbox("Answer Type", ["Theory Only", "Code Only", "Code + Theory"])
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 CodeSmith AI")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and msg["mode"] == "Code Only":
            st.code(msg["content"])
        else:
            st.markdown(msg["content"])

prompt = st.chat_input("Ask anything...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            system_prompt = f"""
You are an intelligent AI assistant like ChatGPT.

Answer Mode: {mode}

Rules:
1. Give complete, accurate, and user-friendly answers.
2. If the user asks theory, explain clearly in simple language.
3. If the user asks code, provide correct and clean code.
4. If mode is Code + Theory, first explain then provide code.
5. Format answers properly like ChatGPT.
6. Keep answers detailed but easy to understand.
"""

            response = client.responses.create(
                model="gpt-5-nano",
                input=f"{system_prompt}\nUser: {prompt}"
            )

            reply = response.output_text.strip()

            if mode == "Code Only":
                st.code(reply)
            else:
                st.markdown(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "mode": mode
    })