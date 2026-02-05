import streamlit as st
from groq import Groq

# Page config
st.set_page_config(
    page_title="Groq AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 Groq AI Chatbot")
st.write("Ask anything 👇")

# --- Secure API Key ---
# Local run ke liye env var ya Streamlit Cloud Secrets
api_key = st.secrets.get("GROQ_API_KEY", None)

if not api_key:
    st.error("GROQ_API_KEY not found. Please add it in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# User input
user_input = st.text_input("Your question:")

if user_input:
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "user", "content": user_input}
            ]
        )

    st.success("Response:")
    st.write(response.choices[0].message.content)
