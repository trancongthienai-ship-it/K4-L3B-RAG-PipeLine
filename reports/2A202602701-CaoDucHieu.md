# Individual Contribution Report

---

## Thông tin

- **Họ và tên:** Cao Đức Hiếu
- **Mã học viên:** 2A202602701
- **Nhóm:** Sunset
- **Repository/branch:** https://github.com/VinUni-AI20k/K4-L3B-RAG-Pipeline · branch `main`
- **Vai trò:** AI Engineer — Tối ưu tìm kiếm, Dự phòng & Sinh văn bản

---

## Phần việc đã thực hiện

| Module / Deliverable | Việc tôi trực tiếp làm | File / Commit / PR | Trạng thái |
|---|---|---|---|
| **Task 7 — RRF Reranking** | Viết thuật toán Reciprocal Rank Fusion gộp điểm từ dense + BM25, đặt `retrieval_method = "hybrid"`, dedup theo ID | [`src/task7_reranking.py`](../src/task7_reranking.py) | Done |
| **Task 8 — PageIndex Fallback** | Triển khai `pageindex_search()` gọi PageIndex Vectorless API, xử lý timeout/ImportError, cache doc IDs để tránh re-upload | [`src/task8_pageindex_vectorless.py`](../src/task8_pageindex_vectorless.py) | Done |
| **Task 9 — Retrieval Pipeline** | Viết hàm `retrieve()` điều phối dense → BM25 → RRF → so sánh `best_dense_score` với `score_threshold` → fallback PageIndex; graceful error handling khi fallback crash | [`src/task9_retrieval_pipeline.py`](../src/task9_retrieval_pipeline.py) | Done |
| **Task 10 — Generation với Citation** | Thiết kế System Prompt ép LLM trích dẫn nguồn; viết `reorder_for_llm()` (lost-in-the-middle mitigation), `format_context()` có title/source label, `generate_with_citation()` trả `GenerationResult` | [`src/task10_generation.py`](../src/task10_generation.py) | Done |
| **Contract tests (Task 7–10)** | Đảm bảo `rerank_rrf`, `retrieve`, `format_context`, `reorder_for_llm`, `generate_with_citation` pass toàn bộ contract tests | [`tests/test_contracts.py`](../tests/test_contracts.py) L156–L255 | Done |

---

## Quyết định kỹ thuật quan trọng

### 1. Dùng `best_dense_score` (cosine) để quyết định fallback, KHÔNG dùng RRF score

**Quyết định:** Trong `task9_retrieval_pipeline.py`, điều kiện trigger PageIndex fallback được tính từ `dense[0]["score"]` — tức cosine similarity gốc từ ChromaDB — thay vì dùng RRF score sau khi fuse.

**Lý do / Evidence:**
- RRF score = `∑ 1/(k + rank)` — là đơn vị thứ hạng, không phản ánh mức độ liên quan thực sự. Một query ngoài domain vẫn có thể có RRF score cao nếu BM25 match keyword ngẫu nhiên.
- Cosine score từ dense retrieval đo độ tương đồng ngữ nghĩa trực tiếp, là tín hiệu đáng tin cậy hơn để phát hiện query "out-of-domain".
- Contract test `test_retrieve_uses_dense_score_for_fallback` tường minh kiểm tra hành vi này.

**Trade-off:** Nếu embedding model yếu (không hiểu domain), dense score thấp cho cả query in-domain → trigger fallback sai. Cần calibrate `SCORE_THRESHOLD` trên tập query thực tế.

---

### 2. `reorder_for_llm()` — Lost-in-the-Middle Mitigation

**Quyết định:** Thay vì đưa chunks theo thứ tự RRF thẳng vào prompt, tôi interleave: chunks rank chẵn (0, 2, 4…) đặt đầu, chunks rank lẻ (1, 3, 5…) đặt cuối ngược chiều — để chunk quan trọng nhất và thứ hai quan trọng nằm ở đầu + cuối context.

**Lý do / Evidence:**
- Nghiên cứu "Lost in the Middle" (Liu et al., 2023) chỉ ra LLM bỏ sót thông tin nằm giữa context dài.
- Contract test `test_reorder_is_non_mutating_and_context_contains_source` xác nhận: `reorder_for_llm` không mutate list gốc, và context phải chứa source label.

**Trade-off:** Thứ tự không còn tuyến tính với RRF score, có thể gây khó đọc khi debug. Với top_k ≤ 5 thì tác động nhỏ.

---

## Kiểm thử và kết quả

**Tests tôi đã dùng:**

```bash
# Contract tests cho các task của tôi
pytest tests/test_contracts.py::test_rrf_uses_rank_deduplicates_and_marks_hybrid -v
pytest tests/test_contracts.py::test_reorder_is_non_mutating_and_context_contains_source -v
pytest tests/test_contracts.py::test_retrieve_uses_dense_score_for_fallback -v
pytest tests/test_contracts.py::test_retrieve_fuses_once_when_dense_is_confident -v
pytest tests/test_contracts.py::test_retrieve_survives_fallback_provider_error -v
pytest tests/test_contracts.py::test_generation_result_validator_accepts_safe_refusal -v
```

**Kết quả:**

| Test | Kết quả | Ghi chú |
|---|---|---|
| `test_rrf_uses_rank_deduplicates_and_marks_hybrid` | ✅ PASS | RRF score = `1/62 + 1/61`, chunk-1 đứng đầu |
| `test_reorder_is_non_mutating_and_context_contains_source` | ✅ PASS | List gốc không bị mutate, context có `tuition.md` |
| `test_retrieve_uses_dense_score_for_fallback` | ✅ PASS | Dense score 0.2 < threshold 0.5 → trả pageindex |
| `test_retrieve_fuses_once_when_dense_is_confident` | ✅ PASS | RRF chỉ gọi 1 lần, fallback không trigger |
| `test_retrieve_survives_fallback_provider_error` | ✅ PASS | RuntimeError từ pageindex → trả hybrid thay vì crash |
| `test_generation_result_validator_accepts_safe_refusal` | ✅ PASS | Safe refusal hợp lệ với `retrieval_source = "none"` |

**Lỗi đã phát hiện và xử lý:**
- **Bug `retrieval_source` sai type:** `generate_with_citation` ban đầu trả `chunks[0]["retrieval_method"]` có thể là `"dense"` — nhưng contract chỉ chấp nhận `"hybrid" | "pageindex" | "none"`. Đã xác định đây là điểm cần kiểm tra thêm trong tích hợp cuối.
- **PageIndex metadata thiếu `chunk_index`:** `pageindex_search()` trả metadata không có `chunk_index` → `validate_search_results` sẽ fail vì `require_chunk=True`. Đây là known limitation của fallback provider.

---

## Điều còn hạn chế

**Hạn chế cụ thể:** `task10_generation.py` hiện chỉ hỗ trợ `LLM_PROVIDER=openai`. Nhánh `else` trả về string lỗi thay vì gọi Gemini/Anthropic SDK. Nếu nhóm đổi provider, generation sẽ trả "Vui lòng chọn openai" thay vì câu trả lời thực.

**Nếu có thêm thời gian:** Implement đầy đủ Gemini (`google-genai`) và Anthropic (`anthropic`) trong `call_llm()`, đồng thời thêm retry logic với exponential backoff để xử lý rate-limit từ LLM provider.

---

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- **Ngày:** 26/09/2026
- **Tên thành viên:** Cao Đức Hiếu
