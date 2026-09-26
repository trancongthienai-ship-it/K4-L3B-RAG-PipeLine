# Author: DuongHuuDat
"""
Task 1 — Thu thập tài liệu chính sách/quy định.

Hướng dẫn:
    1. Chọn chủ đề của nhóm.
    2. Tìm tối thiểu 3 tài liệu PDF/DOCX từ nguồn công khai.
    3. Lưu file gốc vào data/landing/legal/.
    4. Đặt tên không dấu và thể hiện đúng nội dung.

Ví dụ tài liệu: học phí, học bổng, ký túc xá, quy trình đăng ký.
Nếu website chặn crawler, hãy chọn nguồn công khai khác; không vượt WAF.
"""

from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"


def setup_directory() -> None:
    """Tạo thư mục lưu tài liệu gốc."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Ready: {DATA_DIR}")


def download_documents() -> None:
    """Tải ít nhất 3 PDF/DOCX từ nguồn công khai."""
    import requests

    # Vì nhóm đã có sẵn file trong data/landing/legal/ nên ta bỏ qua bước tải đè để tránh mất dữ liệu
    existing_files = list(DATA_DIR.glob("*.*"))
    # Bỏ qua file ẩn .gitkeep
    existing_files = [f for f in existing_files if not f.name.startswith('.')]
    
    if existing_files:
        print(f"Đã có sẵn {len(existing_files)} tài liệu trong {DATA_DIR}, bỏ qua bước tải xuống.")
        return

    print("Thư mục trống, tiến hành tải file mẫu...")
    sources = {
        "Luat_Giao_duc_dai_hoc.pdf": "https://moj.gov.vn/vbpq/lists/vn%20bn%20php%20lut/attachments/28551/Luat%20Giao%20duc%20dai%20hoc.pdf",
    }
    for filename, url in sources.items():
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            (DATA_DIR / filename).write_bytes(response.content)
            print(f"Đã tải: {filename}")
        except Exception as e:
            print(f"Lỗi khi tải {url}: {e}")


if __name__ == "__main__":
    setup_directory()
    download_documents()
