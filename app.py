import streamlit as st
from dotenv import load_dotenv
from src.task10_generation import generate_with_citation

load_dotenv()

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("⚙️ Cài đặt")
    st.caption("Cấu hình hệ thống tìm kiếm")
    top_k = st.slider("Số lượng tài liệu (Top K)", 1, 10, 5)

st.title("🤖 Chatbot Pháp Luật & Tin Tức")
st.caption("Hệ thống Hybrid RAG kết hợp Vector Search, BM25 và PageIndex Fallback")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("📚 Xem tài liệu tham khảo (Sources)"):
                st.caption(f"**Nguồn truy xuất (Retrieval Method):** {message.get('retrieval_source', 'Unknown')}")
                for idx, src in enumerate(message["sources"], 1):
                    meta = src.get("metadata", {})
                    st.markdown(f"**[{idx}] {meta.get('title', 'Unknown Title')}** (Score: {src.get('score', 0):.4f})")
                    st.markdown(f"*{meta.get('source', 'Unknown Source')}*")
                    st.text(src.get("content", "")[:300] + "...")

query = st.chat_input("Nhập câu hỏi của bạn (VD: Điều kiện vay vốn ngân hàng là gì?)...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Đang tìm kiếm tài liệu và tổng hợp câu trả lời..."):
            try:
                # Gọi RAG Pipeline từ Task 10
                result = generate_with_citation(query, top_k=top_k)
                answer = result["answer"]
                sources = result["sources"]
                retrieval_source = result["retrieval_source"]
                
                st.markdown(answer)
                
                if sources:
                    with st.expander("📚 Xem tài liệu tham khảo (Sources)"):
                        st.caption(f"**Nguồn truy xuất (Retrieval Method):** {retrieval_source}")
                        for idx, src in enumerate(sources, 1):
                            meta = src.get("metadata", {})
                            st.markdown(f"**[{idx}] {meta.get('title', 'Unknown Title')}** (Score: {src.get('score', 0):.4f})")
                            st.markdown(f"*{meta.get('source', 'Unknown Source')}*")
                            st.text(src.get("content", "")[:300] + "...")
                
                # Lưu vào session state
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "sources": sources,
                    "retrieval_source": retrieval_source
                })
            except Exception as e:
                st.error(f"Đã xảy ra lỗi hệ thống: {e}")
