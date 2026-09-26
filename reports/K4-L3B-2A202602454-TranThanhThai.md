# Báo cáo đóng góp cá nhân

## Thông tin

- Họ và tên: Trần Thanh Thái
- Mã học viên: 2A202602454
- Nhóm: K4-L3B
- Repository/branch: K4-L3B-RAG-PipeLine — `main`

> Nhóm phát triển dự án trực tiếp trên một máy dùng chung. Các thành viên cùng thảo luận, triển khai, kiểm thử và commit bằng một Git identity chung. Vì vậy, lịch sử commit không được dùng để xác định riêng đóng góp của từng thành viên. Phần đóng góp dưới đây được đối chiếu bằng module phụ trách, file liên quan, kết quả kiểm thử/evaluation và khả năng chạy lại trong buổi demo.

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Giao diện chatbot | Xây dựng giao diện Streamlit, lịch sử hội thoại, cấu hình `top_k`, trạng thái xử lý và thông báo lỗi | `app.py` | Done |
| Tích hợp RAG Pipeline | Gọi `generate_with_citation`; hiển thị câu trả lời, phương thức retrieval và nguồn gồm title, source, score, content | `app.py`, `src/task10_generation.py` | Done |
| Golden Dataset | Phụ trách xây dựng 15+ câu hỏi gồm câu dễ, khó, đánh lừa, trong miền và ngoài miền | `group_project/evaluation/golden_dataset.json` | Partial |
| Đánh giá A/B | Phụ trách so sánh dense-only với hybrid + RRF bằng Faithfulness, Answer relevance, Context recall và Context precision | `group_project/evaluation/RESULT.md` | Partial |
| Phân tích lỗi | Phụ trách tổng hợp worst performers, xác định nguyên nhân tại data, retrieval hoặc generation và đề xuất cải tiến | `group_project/evaluation/RESULT.md` | Partial |
| QA và demo | Phụ trách kiểm tra giao diện, citation, query đúng miền, query ngoài miền và kết quả A/B | `tests/test_contracts.py`, `tests/test_acceptance.py`, `app.py` | Partial |

Các commit được tạo trên máy dùng chung nên chỉ được dùng làm bằng chứng của nhóm, không được khai là commit cá nhân.

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Giao diện gọi `generate_with_citation` thay vì cài đặt lại retrieval và generation trong `app.py`.  
   **Lý do/evidence:** `app.py` nhận trực tiếp `answer`, `sources` và `retrieval_source` từ pipeline, giúp tách giao diện khỏi logic RAG.  
   **Trade-off:** Khi schema kết quả của `src/task10_generation.py` thay đổi, giao diện cũng phải cập nhật.

2. **Quyết định:** Hiển thị nguồn trong vùng mở rộng, gồm phương thức retrieval, title, source, score và đoạn nội dung tham chiếu.  
   **Lý do/evidence:** Người dùng có thể đối chiếu câu trả lời với tài liệu truy xuất ngay trên giao diện.  
   **Trade-off:** Giao diện chỉ hiển thị 300 ký tự đầu của mỗi đoạn để tránh quá dài.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng:
  - Kiểm tra giao diện với query đúng miền thuộc dữ liệu pháp luật/ngân hàng.
  - Kiểm tra query ngoài miền để quan sát fallback và safe refusal.
  - Các checkpoint của nhóm: `pytest tests/test_contracts.py -q`, `pytest tests/test_acceptance.py -q`, `pytest -q`.
- Kết quả trước/sau nếu có:
  - Giao diện đã có luồng nhập câu hỏi, gọi pipeline, hiển thị câu trả lời và nguồn tham khảo.
  - Kết quả test và A/B cuối cùng cần được cập nhật từ lần chạy trên bản commit nộp.
- Lỗi đã phát hiện và cách xử lý:
  - Bao bọc lời gọi pipeline bằng `try/except` để hiển thị lỗi thay vì làm dừng ứng dụng.
  - Lưu câu hỏi, câu trả lời và nguồn trong `st.session_state` để giữ lịch sử khi Streamlit chạy lại script.

## Điều còn hạn chế

- Golden Dataset và báo cáo evaluation chưa có đủ kết quả chạy thực tế để kết luận chất lượng bằng bốn metric.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện là hoàn thiện 15+ câu hỏi, chạy hai cấu hình trên cùng dữ liệu và điền đầy đủ số liệu cùng worst performers vào `group_project/evaluation/RESULT.md`.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 25/09/2026
- Tên thành viên: Trần Thanh Thái
