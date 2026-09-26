# Individual contribution report

## Thông tin

- Họ và tên: Dương Hữu Đạt
- Mã học viên: 2A202602544
- Nhóm: sunset
- Repository/branch: main

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Data Collection (Legal) | Thu thập các văn bản pháp luật hiện hành (PDF, Docx) liên quan đến chủ đề của nhóm và thiết lập thư mục tự động lưu trữ tại `data/landing/legal`. | `src/task1_collect_legal_docs.py` | Done |
| Data Collection (News) | Xây dựng pipeline thu thập dữ liệu tự động cho các bài viết, tin tức từ web, trích xuất metadata và lưu dưới dạng JSONL tại `data/landing/news`. | `src/task2_crawl_news.py` | Done |
| Data Standardization | Viết logic bóc tách văn bản thô từ định dạng PDF, Docx và JSONL để chuẩn hóa toàn bộ thành định dạng Markdown thống nhất. Đưa dữ liệu đầu ra vào thư mục `data/standardized` để sẵn sàng cho quá trình Chunking. | `src/task3_convert_markdown.py` | Done |

## Quyết định kỹ thuật quan trọng

Mô tả tối đa hai quyết định mà bạn trực tiếp tham gia:

1. **Quyết định:** Thống nhất đưa toàn bộ định dạng (PDF, Docx, HTML) về duy nhất định dạng Markdown trước khi đi vào hệ thống RAG thay vì để dạng Plain text.
   **Lý do/evidence:** Markdown giúp bảo toàn các cấu trúc ngữ nghĩa quan trọng của văn bản pháp lý như Tiêu đề (Heading 1, 2, 3), Danh sách (List), và Bảng (Table). Điều này giúp LLM về sau đọc hiểu cấu trúc phân cấp của văn bản dễ dàng hơn nhiều so với văn bản thuần túy (Plain text).
   **Trade-off:** Mất thêm thời gian và công sức để tinh chỉnh logic parser (đặc biệt là lỗi vỡ format khi trích xuất PDF).

2. **Quyết định:** Ở Task 2, lưu dữ liệu cào được (Crawled data) dưới dạng `JSONL` thay vì từng file JSON rời rạc.
   **Lý do/evidence:** Chuẩn JSONL giúp dễ dàng quản lý hàng loạt bài báo (mỗi dòng là một bài). Cực kỳ tối ưu trong việc xử lý (Streaming) khi dữ liệu phình to vì không cần load toàn bộ file vào RAM cùng lúc.
   **Trade-off:** Khi dùng text editor thông thường để mở file và debug trực tiếp bằng mắt sẽ khó nhìn hơn một chút so với các file JSON được format thụt lề chuẩn.

## Kiểm thử và kết quả

- **Test hoặc query tôi đã dùng:** 
  - Chạy thử `python -m src.task1_collect_legal_docs` và `task2`.
  - Kiểm tra kết quả đầu ra của `task3` bằng cách đọc thử các file lưu trong `data/standardized/legal` và `data/standardized/news`.
- **Kết quả trước/sau nếu có:** Dữ liệu thô từ các bộ luật định dạng `.docx` và file `summary.jsonl` đều đã được gỡ bỏ rác HTML, đánh thẻ Heading `#`, `##` rõ ràng.
- **Lỗi đã phát hiện và cách xử lý:** Phát hiện lỗi các ký tự ẩn (newline rác) hoặc bảng biểu (tables) trong file Docx bị nối liền kề gây khó đọc. Đã viết logic regex để dọn dẹp các khoảng trắng thừa này.

## Điều còn hạn chế

- **Một hạn chế cụ thể của phần tôi làm:** Tool extract nội dung từ file PDF hiện tại đôi khi vẫn gặp khó khăn trong việc nhận diện chính xác các header/footer hoặc số trang, khiến phần rác này vẫn bị dính vào văn bản cuối cùng.
- **Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện:** Sử dụng các thư viện OCR chuyên dụng kết hợp LLM vision để phân tích và giữ lại chính xác 100% định dạng bảng biểu phức tạp trong các văn bản pháp luật (như bảng khung hình phạt, bảng mức hoàn tiền).

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 25/09/2026
- Tên thành viên: Dương Hữu Đạt
