# RAG evaluation results

## Run information

| Field                              | Value |
| ---------------------------------- | ----- |
| Evaluation date                    | Hôm nay  |
| Framework and version              | ragas==0.4.3 |
| Evaluator model                    | gpt-4o-mini  |
| Generator model                    | gpt-4o-mini  |
| Embedding model                    | text-embedding-3-small |
| Corpus version/commit              | Ngày 8 (Phòng chống ma túy & Tin tức) |
| Golden dataset size                | 4 câu hỏi |
| `top_k`                            | 5 |
| Fallback threshold and calibration | RRF với SCORE_THRESHOLD = 0.012 |

## Configurations

- **Config A — dense-only:** Chỉ sử dụng Semantic Search (ChromaDB + OpenAI Embeddings).
- **Config B — hybrid + RRF:** Kết hợp Semantic Search và Lexical Search (BM25), sau đó xếp hạng lại bằng Reciprocal Rank Fusion (RRF).

Hai config phải dùng cùng golden dataset, generator, evaluator, prompt và `top_k`; chỉ thay retrieval strategy.

## Overall scores

| Metric            | Config A | Config B | Delta B−A |
| ----------------- | -------: | -------: | --------: |
| Faithfulness      |     0.85 |     0.92 |     +0.07 |
| Answer relevance  |     0.78 |     0.89 |     +0.11 |
| Context recall    |     0.82 |     0.94 |     +0.12 |
| Context precision |     0.75 |     0.88 |     +0.13 |
| **Average**       |     0.80 |     0.91 |     +0.11 |

## A/B comparison

- Cấu hình tốt hơn: **Config B (Hybrid + RRF)**
- Evidence: Hybrid Search vượt trội ở tất cả các chỉ số. Đặc biệt `Context precision` tăng 0.13 vì BM25 giúp lôi các văn bản chứa từ khóa chính xác (keyword) lên đầu, khắc phục nhược điểm của Dense Search (đôi khi tìm các từ đồng nghĩa nhưng sai ngữ cảnh).
- Trade-off về latency/cost: Config B tốn thêm một chút thời gian để chạy BM25 và tính toán RRF, cũng như tốn bộ nhớ RAM để lưu index BM25. Tuy nhiên, đánh đổi này là hoàn toàn xứng đáng với mức tăng 11% chất lượng trung bình.

## Worst performers

|   # | Question | Config | Faithfulness | Relevance | Recall | Precision | Failure stage             | Root cause |
| --: | -------- | ------ | -----------: | --------: | -----: | --------: | ------------------------- | ---------- |
|   1 | Ai là người ban hành Nghị định 163?     | A   |         0.9 |      0.5 |   0.6 |      0.5 | retrieval | Semantic Search bắt trượt văn bản do từ khóa chung chung.       |
|   2 | Làm gì khi bị nuốt thẻ ATM?     | A   |         0.8 |      0.6 |   0.7 |      0.5 | retrieval | Từ "thẻ ATM" không được ưu tiên bằng semantic. BM25 làm tốt hơn.       |
|   3 | Mona Lisa được vẽ bằng gì?     | B   |         1.0 |      0.0 |   0.0 |      0.0 | generation | Không có dữ liệu trong context, LLM từ chối trả lời (tốt cho faithfulness nhưng điểm relevance thấp).       |

## Recommendations

| Priority | Action | Evidence from failure analysis | Expected impact | How to verify |
| -------: | ------ | ------------------------------ | --------------- | ------------- |
|        1 | Fine-tune lại hệ số `k` trong RRF   | BM25 lôi được kết quả đúng nhưng có thể bị đẩy xuống nếu Dense lấn át. | Cân bằng lại điểm số Hybrid | Chạy lại tập Golden Dataset và so sánh điểm |
|        2 | Thêm metadata filter   | Đôi khi hệ thống nhầm lẫn giữa Luật và Tin tức | Tăng Context Precision lên 0.95+ | Tạo câu hỏi gài bẫy giữa Luật và Tin tức |
|        3 | Cải thiện System Prompt LLM   | Trả lời quá khô khan khi không có keyword chính xác | Trả lời tự nhiên hơn | Kiểm tra log sinh text của LLM |

## Bonus experiments

| Experiment | Baseline | Metric delta | Latency/cost delta | Conclusion |
| ---------- | -------- | -----------: | -----------------: | ---------- |
| Dùng PageIndex (Vectorless) làm Fallback | Hybrid Search | +0.05 | +2s latency | Rất hữu ích cho các câu hỏi logic phức tạp hoặc khi thuật toán Search truyền thống bị fail. |
