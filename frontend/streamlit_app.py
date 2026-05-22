import streamlit as st
import requests
import json

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RAG Document Assistant",
    page_icon="📄",
    layout="wide",
)

BACKEND_URL = "http://backend:8000"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📄 RAG Document Assistant")
    st.markdown("---")
    st.markdown("### How it works")
    st.markdown(
        """
1. **Upload** a PDF document  
2. **Ask** any question about it  
3. **Get** AI-powered answers with source citations  
4. **Evaluate** answer quality with RAGAS  
        """
    )
    st.markdown("---")

    # Health check
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=3)
        if r.status_code == 200:
            st.success("✅ Backend connected")
        else:
            st.error("❌ Backend error")
    except Exception:
        st.error("❌ Backend not reachable")

    st.markdown("---")
    st.caption("Built with FastAPI · LangChain · ChromaDB · Ollama · RAGAS")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_upload, tab_chat, tab_eval = st.tabs(["📤 Upload Document", "💬 Ask Questions", "📊 Evaluate"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — UPLOAD
# ─────────────────────────────────────────────────────────────────────────────
with tab_upload:
    st.header("Upload a PDF Document")
    st.markdown("Upload any PDF — research papers, policies, reports, or books.")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Maximum file size: 50 MB",
    )

    if uploaded_file is not None:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"📎 **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")
        with col2:
            upload_btn = st.button("📤 Upload & Index", type="primary", use_container_width=True)

        if upload_btn:
            with st.spinner("Uploading and indexing PDF... This may take a moment."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post(f"{BACKEND_URL}/upload/", files=files, timeout=120)

                    if response.status_code == 200:
                        data = response.json()
                        st.success("✅ PDF uploaded and indexed successfully!")
                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric("File", data.get("filename", "—"))
                        col_b.metric("Pages Loaded", data.get("total_pages", 0))
                        col_c.metric("Chunks Stored", data.get("total_chunks", 0))
                    else:
                        error = response.json().get("detail", "Unknown error")
                        st.error(f"❌ Upload failed: {error}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend. Is Docker running?")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — CHAT
# ─────────────────────────────────────────────────────────────────────────────
with tab_chat:
    st.header("Ask Questions About Your Documents")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                with st.expander("📚 View Sources", expanded=False):
                    for i, src in enumerate(msg["sources"], 1):
                        meta = src.get("metadata", {})
                        file_name = meta.get("source", "Unknown file")
                        page = meta.get("page", "?")
                        st.markdown(f"**Source {i}** — `{file_name}` (page {page})")
                        st.caption(src.get("page_content", ""))
                        st.divider()

    # Input
    question = st.chat_input("Ask a question about your uploaded documents...")

    if question:
        # Show user message
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        # Get answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/chat/",
                        json={"question": question},
                        timeout=120,
                    )

                    if response.status_code == 200:
                        data = response.json()
                        answer = data.get("answer", "No answer generated.")
                        sources = data.get("sources", [])

                        st.markdown(answer)

                        if sources:
                            with st.expander("📚 View Sources", expanded=False):
                                for i, src in enumerate(sources, 1):
                                    meta = src.get("metadata", {})
                                    file_name = meta.get("source", "Unknown file")
                                    page = meta.get("page", "?")
                                    st.markdown(f"**Source {i}** — `{file_name}` (page {page})")
                                    st.caption(src.get("page_content", ""))
                                    st.divider()

                        # Save to history
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": answer,
                            "sources": sources,
                        })

                    else:
                        error = response.json().get("detail", "Unknown error")
                        st.error(f"❌ Error: {error}")
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": f"Error: {error}",
                        })

                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend.")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")

    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — EVALUATION
# ─────────────────────────────────────────────────────────────────────────────
with tab_eval:
    st.header("RAGAS Evaluation Pipeline")
    st.markdown(
        """
        Evaluate your RAG system using **RAGAS** metrics:
        - **Faithfulness** — Does the answer stay grounded in the retrieved context?
        - **Answer Relevancy** — Does the answer actually address the question?
        - **Context Precision** — Is the retrieved context useful and on-topic?
        """
    )

    eval_mode = st.radio("Evaluation mode", ["Demo (built-in sample)", "Custom (enter your own data)"])

    if eval_mode == "Demo (built-in sample)":
        if st.button("▶️ Run Demo Evaluation", type="primary"):
            with st.spinner("Running RAGAS evaluation..."):
                try:
                    response = requests.get(f"{BACKEND_URL}/evaluation/demo", timeout=180)
                    if response.status_code == 200:
                        data = response.json()
                        st.success("✅ Evaluation complete!")
                        scores = data.get("scores", [])
                        if scores:
                            st.dataframe(scores, use_container_width=True)
                    else:
                        st.error(f"❌ {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    else:
        with st.form("eval_form"):
            question_input = st.text_area("Question", "What is RAG?")
            answer_input = st.text_area(
                "Model Answer",
                "RAG stands for Retrieval-Augmented Generation.",
            )
            context_input = st.text_area(
                "Retrieved Context (one chunk per line)",
                "Retrieval-Augmented Generation is a framework combining retrieval and generation.",
            )
            ground_truth_input = st.text_area(
                "Ground Truth Answer",
                "RAG is Retrieval-Augmented Generation.",
            )
            submitted = st.form_submit_button("▶️ Run Evaluation", type="primary")

        if submitted:
            with st.spinner("Running RAGAS evaluation..."):
                try:
                    payload = {
                        "questions": [question_input],
                        "answers": [answer_input],
                        "contexts": [[c.strip() for c in context_input.splitlines() if c.strip()]],
                        "ground_truths": [ground_truth_input],
                    }
                    response = requests.post(
                        f"{BACKEND_URL}/evaluation/",
                        json=payload,
                        timeout=180,
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.success("✅ Evaluation complete!")
                        st.dataframe(data.get("scores", []), use_container_width=True)
                    else:
                        st.error(f"❌ {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
