"""
Task 8 — PageIndex vectorless fallback.

Hướng dẫn:
    1. Đọc PAGEINDEX_API_KEY từ .env.
    2. Upload tài liệu ở định dạng PageIndex hỗ trợ.
    3. Cache document IDs để không upload lại.
    4. Parse kết quả thành SearchResult có method pageindex.

PageIndex là dịch vụ ngoài: cần timeout và xử lý lỗi để pipeline không crash.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")
STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"


def upload_documents() -> None:
    """Upload tài liệu và lưu document IDs để tái sử dụng."""
    if not PAGEINDEX_API_KEY:
        print("Chưa có PAGEINDEX_API_KEY")
        return
        
    try:
        from pageindex import PageIndexClient
        import json
        
        client = PageIndexClient(api_key=PAGEINDEX_API_KEY)
        doc_ids = []
        
        # Lặp qua tất cả file markdown đã chuẩn hóa
        for filepath in STANDARDIZED_DIR.rglob("*.md"):
            try:
                print(f"Đang upload {filepath.name} lên PageIndex...")
                # Nếu API SDK thay đổi, bạn có thể cần chỉnh lại method submit
                result = client.submit_document(str(filepath))
                if isinstance(result, dict) and "doc_id" in result:
                    doc_ids.append(result["doc_id"])
            except Exception as e:
                print(f"Lỗi upload {filepath.name}: {e}")
                
        # Lưu trữ danh sách document IDs để sau này truy vấn nếu cần
        with open("pageindex_doc_ids.json", "w", encoding="utf-8") as f:
            json.dump(doc_ids, f)
            
        print("Upload lên PageIndex hoàn tất.")
    except ImportError:
        print("Chưa cài đặt SDK pageindex. Hãy chạy: pip install pageindex")
    except Exception as e:
        print(f"Lỗi hệ thống PageIndex: {e}")


def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """Trả về pageindex SearchResult."""
    if not PAGEINDEX_API_KEY:
        return []
    
    print(f"[Fallback] Kích hoạt PageIndex Vectorless Search cho query: '{query}'")
    
    try:
        from pageindex import PageIndexClient
        client = PageIndexClient(api_key=PAGEINDEX_API_KEY)
        
        # Gọi chat / query để hệ thống Reasoning của PageIndex xử lý
        response = client.chat(query)
        
        # Format kết quả trả về dưới dạng 1 "Chunk" để Pipeline ở Task 9 có thể ghép vào RRF
        # hoặc gửi thẳng sang Task 10 cho LLM đọc lại.
        return [{
            "id": "pageindex_reasoning_result",
            "content": str(response),
            "score": 1.0, 
            "metadata": {"title": "Kết quả từ PageIndex Vectorless RAG", "source": "pageindex.ai"},
            "retrieval_method": "pageindex"
        }]
    except ImportError:
        print("Chưa cài đặt SDK pageindex. Hãy chạy: pip install pageindex")
        return []
    except Exception as e:
        print(f"Lỗi truy vấn PageIndex: {e}")
        return []


if __name__ == "__main__":
    upload_documents()
