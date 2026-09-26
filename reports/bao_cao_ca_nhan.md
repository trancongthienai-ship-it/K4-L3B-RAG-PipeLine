# Individual contribution report

## Thông tin

- Họ và tên: Trần Công Thiện (Hãy sửa nếu không đúng)
- Mã học viên: [ĐIỀN MÃ HỌC VIÊN CỦA BẠN VÀO ĐÂY]
- Nhóm: [ĐIỀN TÊN NHÓM CỦA BẠN VÀO ĐÂY]
- Repository/branch: main

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Data Processing | Xử lý dữ liệu đầu vào dạng JSONL, chuyển đổi hàng loạt sang định dạng Markdown chuẩn để RAG có thể nạp vào hệ thống. | `src/task3_convert_markdown.py` | Done |
| Vectorless Fallback (PageIndex) | Khởi tạo PageIndexClient, thiết lập cơ chế upload dữ liệu hàng loạt và lấy doc_id. Xây dựng logic gọi reasoning API để đóng vai trò "cứu thua" cho Pipeline khi Vector Search gặp câu hỏi khó. | `src/task8_pageindex_vectorless.py` | Done |
| Giao diện Chatbot (UI) | Tích hợp toàn bộ Hybrid RAG Pipeline vào giao diện Streamlit. Viết logic hiển thị đoạn trích dẫn (Sources) và nhãn Phương pháp Tìm kiếm (Retrieval Method) dưới mỗi câu trả lời. | `app.py` | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Sử dụng PageIndex (Vectorless RAG) làm cơ chế Fallback (Dự phòng) thay vì chạy song song.
   **Lý do/evidence:** Việc gọi qua API của PageIndex tốn thêm thời gian mạng (latency). Nếu câu hỏi đơn giản, ChromaDB + BM25 đã đủ sức trả lời. Do đó, tôi đặt ngưỡng `SCORE_THRESHOLD`, nếu Vector Search tự tin thấp hơn ngưỡng thì mới kích hoạt PageIndex để tiết kiệm thời gian mà vẫn đảm bảo độ chính xác.
   **Trade-off:** Chấp nhận mất thêm vài giây chờ đợi API PageIndex phản hồi ở những câu hỏi hóc búa để đổi lấy độ chính xác tuyệt đối và khả năng suy luận mà Vector DB không làm được.

2. **Quyết định:** Ép LLM tuân thủ tuyệt đối System Prompt "Từ chối trả lời nếu thiếu evidence".
   **Lý do/evidence:** Trong lĩnh vực Pháp lý và Luật, tính chính xác là số 1. Việc cấm LLM sử dụng kiến thức bên ngoài giúp hệ thống không bao giờ bịa (hallucinate) ra Luật không có thật.
   **Trade-off:** LLM đôi lúc trả lời quá khô khan (copy nguyên văn tài liệu) thay vì tóm tắt mạch lạc. (Ví dụ: Khi hỏi "Ai ban hành Luật", thay vì trả lời "Quốc Hội", nó chỉ đọc đúng câu "Cơ quan có thẩm quyền ban hành" trong tài liệu).

## Kiểm thử và kết quả

- **Test hoặc query tôi đã dùng:** 
  - *"Thẻ SeASoul hoàn tiền bao nhiêu?"* (Test Vector RAG)
  - *"gần đây ca sỹ nào nghiện ma túy"* (Test sự trung thực / Fallback)
  - *"Ai là người ban hành Luật phòng chống ma túy?"* (Test giới hạn của LLM)
- **Kết quả trước/sau nếu có:** Giao diện hiển thị xuất sắc cả câu trả lời lẫn danh sách các nguồn (Sources) kèm điểm số tin cậy. 
- **Lỗi đã phát hiện và cách xử lý:** 
  - Lỗi `name 'OUTPUT_DIR' is not defined` ở Task 8 do gọi sai tên biến thư mục. Đã xử lý bằng cách đổi thành `STANDARDIZED_DIR`.
  - Lỗi `attempted relative import` khi chạy script ở dạng `__main__`. Đã xử lý bằng cách chạy qua giao diện Streamlit `app.py`.

## Điều còn hạn chế

- **Một hạn chế cụ thể của phần tôi làm:** Cơ chế Fallback sang PageIndex hiện tại mới chỉ bọc lại 1 chunk duy nhất thay vì toàn bộ tree-index, do giới hạn định dạng đầu ra của Pipeline.
- **Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện:** Tinh chỉnh lại trọng số thuật toán RRF (Reciprocal Rank Fusion) để cân bằng tốt hơn giữa Lexical (BM25) và Semantic (ChromaDB) sao cho phù hợp với đặc thù dữ liệu tiếng Việt.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: [ĐIỀN NGÀY HÔM NAY]
- Tên thành viên: Trần Công Thiện
