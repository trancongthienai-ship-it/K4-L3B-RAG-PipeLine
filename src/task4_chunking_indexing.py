"""
Task 4 — Chunking, embedding và indexing.

Hướng dẫn:
    1. Đọc toàn bộ Markdown trong data/standardized/.
    2. Chia văn bản bằng strategy đã chọn.
    3. Embed chunks bằng một provider duy nhất.
    4. Upsert vào ChromaDB với cosine distance.

Mỗi document/chunk phải theo docs/MODULE_CONTRACTS.md. ID cần ổn định để
chạy lại pipeline không tạo dữ liệu trùng. Task 5 phải dùng chung embed_texts().
"""

from pathlib import Path


STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"

# Giải thích lựa chọn tham số trong báo cáo nhóm.
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
CHUNKING_METHOD = "recursive"

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 1024

COLLECTION_NAME = "rag_documents"


def embed_texts(texts: list[str]) -> list[list[float]]:
    from langchain_openai import OpenAIEmbeddings
    from dotenv import load_dotenv
    
    # Load biến môi trường từ file .env (để lấy OPENAI_API_KEY)
    load_dotenv()
    
    # Sử dụng text-embedding-3-small với tham số dimensions=1024
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL, 
        dimensions=EMBEDDING_DIM
    )
    return embeddings.embed_documents(texts)


def get_collection():
    """Mở Chroma collection dùng cosine distance."""
    import chromadb
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def load_documents() -> list[dict]:
    """Đọc Markdown và trả về danh sách Document."""
    documents = []
    for path in STANDARDIZED_DIR.rglob("*.md"):
        doc_type = "legal" if "legal" in path.parts else "news"
        documents.append({
            "id": path.relative_to(STANDARDIZED_DIR).as_posix(),
            "content": path.read_text(encoding="utf-8"),
            "metadata": {
                "source": path.name,
                "title": path.stem,
                "doc_type": doc_type,
                "url": "", # Có thể bổ sung logic map URL nếu cần
            },
        })
    return documents


def chunk_documents(documents: list[dict]) -> list[dict]:
    """Chia Document thành chunks có id và chunk_index."""
    from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
    
    # 1. Splitter cho dữ liệu Legal (cấu trúc Markdown)
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    
    # 2. Splitter chung cho News và dùng để cắt nhỏ thêm nếu Legal chunk vẫn quá dài
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    
    chunks = []
    for document in documents:
        doc_type = document["metadata"]["doc_type"]
        
        if doc_type == "legal":
            # Bước 1: Chia theo phân cấp Chương, Điều (Markdown Headers)
            md_splits = markdown_splitter.split_text(document["content"])
            
            # Bước 2: Với các Điều khoản quá dài, tiếp tục chia nhỏ
            final_splits = recursive_splitter.split_documents(md_splits)
            
            for index, split in enumerate(final_splits):
                chunk_metadata = {**document["metadata"], "chunk_index": index}
                # Gộp thông tin Header (Chương, Điều) vào metadata
                for key, val in split.metadata.items():
                    chunk_metadata[key] = val
                    
                chunks.append({
                    "id": f"{document['id']}::chunk-{index}",
                    "content": split.page_content,
                    "metadata": chunk_metadata,
                })
        else:
            # Cho News: Dùng Recursive Splitter bình thường
            for index, text in enumerate(recursive_splitter.split_text(document["content"])):
                chunks.append({
                    "id": f"{document['id']}::chunk-{index}",
                    "content": text,
                    "metadata": {**document["metadata"], "chunk_index": index},
                })
                
    return chunks


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """Thêm embedding vào từng chunk."""
    # Embed theo batch để tránh quá tải RAM nếu số lượng chunks lớn
    batch_size = 32
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        texts = [chunk["content"] for chunk in batch]
        vectors = embed_texts(texts)
        for chunk, vector in zip(batch, vectors):
            chunk["embedding"] = vector
    return chunks


def index_to_vectorstore(chunks: list[dict]) -> None:
    """Upsert chunks vào ChromaDB."""
    collection = get_collection()
    
    # Upsert theo batch để ChromaDB không bị lỗi khi payload quá lớn
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        
        # Đảm bảo URL nếu None thì chuyển thành chuỗi rỗng để ChromaDB không báo lỗi
        metadatas = []
        for chunk in batch:
            meta = chunk["metadata"].copy()
            if meta.get("url") is None:
                meta["url"] = ""
            metadatas.append(meta)

        collection.upsert(
            ids=[chunk["id"] for chunk in batch],
            documents=[chunk["content"] for chunk in batch],
            embeddings=[chunk["embedding"] for chunk in batch],
            metadatas=metadatas,
        )


def run_pipeline() -> None:
    """Chạy load, chunk, embed và index."""
    documents = load_documents()
    chunks = chunk_documents(documents)
    embedded_chunks = embed_chunks(chunks)
    index_to_vectorstore(embedded_chunks)
    print(f"Indexed {len(embedded_chunks)} chunks")


if __name__ == "__main__":
    run_pipeline()
