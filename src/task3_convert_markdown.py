"""
Task 3 — Chuẩn hóa dữ liệu sang Markdown.

Hướng dẫn:
    1. Dùng MarkItDown để convert PDF/DOCX.
    2. Đọc JSON và giữ metadata ở đầu file Markdown.
    3. Giữ cấu trúc thư mục legal/ và news/.
    4. Không tạo file rỗng hoặc file trùng khi chạy lại.

Cài đặt:
    Dependency MarkItDown đã được khai báo trong pyproject.toml.
    
-> Hoặc dùng công cụ nào bạn quen khác Markitdown
"""

from pathlib import Path


LANDING_DIR = Path(__file__).parent.parent / "data" / "landing"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "standardized"


def convert_legal_docs() -> None:
    from markitdown import MarkItDown
    legal_dir = LANDING_DIR / "legal"
    output_dir = OUTPUT_DIR / "legal"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        converter = MarkItDown()
    except Exception as e:
        print(f"Cảnh báo: Không thể khởi tạo MarkItDown. Bạn đã cài đặt đủ dependency chưa? ({e})")
        return
        
    for path in legal_dir.iterdir():
        if path.suffix.lower() in {".pdf", ".doc", ".docx"}:
            try:
                print(f"Đang convert {path.name}...")
                result = converter.convert(str(path))
                (output_dir / f"{path.stem}.md").write_text(
                    result.text_content, encoding="utf-8"
                )
            except Exception as e:
                print(f"Lỗi khi convert {path.name}: {e}")


def convert_news_articles() -> None:
    import json
    news_dir = LANDING_DIR / "news"
    output_dir = OUTPUT_DIR / "news"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Xử lý các file .json đơn lẻ (nếu có từ Task 2)
    for path in news_dir.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            
            title = data.get('title', 'Unknown Title')
            url = data.get('url', 'Unknown Source')
            crawled = data.get('date_crawled', 'Unknown Date')
            content = data.get('content_markdown', data.get('content', ''))
            
            header = f"# {title}\n\n**Source:** {url}\n\n**Crawled:** {crawled}\n\n---\n\n"
            (output_dir / f"{path.stem}.md").write_text(header + content, encoding="utf-8")
        except Exception as e:
            print(f"Lỗi xử lý JSON {path.name}: {e}")
            
    # 2. Xử lý các file .jsonl (dữ liệu cung cấp sẵn như summary.jsonl)
    for path in news_dir.glob("*.jsonl"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                for idx, line in enumerate(f):
                    if not line.strip(): continue
                    data = json.loads(line)
                    title = data.get('title', f'Article {idx}')
                    url = data.get('url', 'Unknown Source')
                    crawled = data.get('date_crawled', 'Unknown Date')
                    content = data.get('content_markdown', data.get('content', ''))
                    
                    header = f"# {title}\n\n**Source:** {url}\n\n**Crawled:** {crawled}\n\n---\n\n"
                    # Dùng index làm tên file để tránh trùng lặp
                    (output_dir / f"{path.stem}_{idx:03d}.md").write_text(header + content, encoding="utf-8")
            print(f"Đã convert xong file {path.name}")
        except Exception as e:
            print(f"Lỗi xử lý JSONL {path.name}: {e}")


def convert_all() -> None:
    """Convert toàn bộ dữ liệu landing."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    convert_legal_docs()
    convert_news_articles()
    print(f"Saved Markdown to: {OUTPUT_DIR}")


if __name__ == "__main__":
    convert_all()
