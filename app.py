import streamlit as st
from groq import Groq
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CodeSmith",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "api_key" not in st.session_state:
    st.session_state.api_key = "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"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "latest_answer" not in st.session_state:
    st.session_state.latest_answer = None

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## ⚙️ CodeSmith Options")

    answer_mode = st.selectbox(
        "Select Answer Type",
        ["Code Only", "Theory Only", "Code + Theory"]
    )

    if st.button("🗑️ Clear History"):
        st.session_state.chat_history = []
        st.session_state.latest_answer = None
        st.success("History Cleared")

    st.markdown("---")
    st.markdown("## 📜 Chat History")

    # Show all previous Q&A in sidebar
    for i, chat in enumerate(st.session_state.chat_history, 1):
        with st.expander(f"Q{i}: {chat['question'][:30]}"):
            st.code(chat["answer"])

    st.markdown("---")
    st.info("👨‍💻 Welcome to CodeSmith AI")

# ---------------- MAIN UI ----------------
st.title("🤖 CodeSmith AI")

query = st.text_area(
    "Enter your question:",
    height=100,
    placeholder="Type your question here..."
)

# ---------------- BUTTON ----------------
if st.button("Click here for search"):
    if not query.strip():
        st.warning("⚠️ Please enter a question first!")
    else:
        try:
            client = Groq(api_key=st.session_state.api_key)

            system_prompt = f"""
You are an expert AI like Gemini or ChatGPT.
Mode: {answer_mode}
"""

            with st.spinner("Generating response..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": query}
                    ]
                )

            answer = response.choices[0].message.content

            # Save to history
            st.session_state.chat_history.append({
                "question": query,
                "answer": answer
            })

            # Save latest answer for main display
            st.session_state.latest_answer = answer

            st.success("✅ Response Generated")

        except Exception as e:
            st.error(f"❌ Error: {e}")

# ---------------- LATEST ANSWER DISPLAY ----------------
if st.session_state.latest_answer:
    st.subheader("🧠 Latest Answer")

    # ---------------- Theory Only ----------------
    if answer_mode == "Theory Only":
        st.write(st.session_state.latest_answer)
        st.text_area("Copy Theory", value=st.session_state.latest_answer, height=150)

    # ---------------- Code Only ----------------
    elif answer_mode == "Code Only":
        st.code(st.session_state.latest_answer, language="python")
        st.text_area("Copy Code", value=st.session_state.latest_answer, height=150)

    # ---------------- Code + Theory ----------------
    else:
        answer_text = st.session_state.latest_answer

        # Detect code blocks using triple backticks
        code_blocks = re.findall(r"```(.*?)```", answer_text, flags=re.DOTALL)
        theory_text = re.sub(r"```.*?```", "", answer_text, flags=re.DOTALL).strip()

        # Display Theory
        if theory_text:
            st.write("**Theory:**")
            st.write(theory_text)
            st.text_area("Copy Theory", value=theory_text, height=150)

        # Display Code Blocks
        if code_blocks:
            for i, code in enumerate(code_blocks, 1):
                st.write(f"**Code Block {i}:**")
                st.code(code, language="python")
                st.text_area(f"Copy Code {i}", value=code, height=150)
