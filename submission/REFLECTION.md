# Reflection — Lab 19

**Tên:** Nguyễn Lâm Tùng  
**Cohort:** A20  
**Path đã chạy:** lite

---

## Câu hỏi (≤ 200 chữ)

Trên golden set 50 queries, hybrid RRF thắng trung bình: BM25 đạt 77.8%, semantic đạt 73.2%, hybrid đạt 78.6%. Với `exact` queries, BM25 và hybrid cùng mạnh vì query chứa keyword kỹ thuật xuất hiện trực tiếp trong corpus. Với `mixed` queries, hybrid thắng rõ nhất vì nó cộng được cả tín hiệu lexical từ BM25 và tín hiệu semantic từ vector search. Với `paraphrase`, semantic chưa thắng trong lite path vì model `BAAI/bge-small-en-v1.5` không tối ưu cho tiếng Việt; dùng embedding multilingual như `bge-m3` có thể cải thiện nhóm này.

Tôi sẽ không dùng hybrid khi bài toán chỉ cần exact matching, filter có cấu trúc, hoặc keyword compliance/audit nơi BM25 dễ giải thích hơn. Tôi cũng tránh hybrid khi latency/cost rất chặt và một retriever đơn đã đủ tốt, hoặc khi embedding model chưa phù hợp domain/ngôn ngữ.

---

## Điều ngạc nhiên nhất khi làm lab này

Điều đáng chú ý là hybrid không cần mỗi retriever đều thắng ở mọi query type. Chỉ cần các retriever bù điểm yếu cho nhau, RRF đã làm kết quả tổng thể ổn định hơn.

---

## Evidence screenshots

### NB1 — Embeddings & Vector Index

![NB1 indexed vectors](screenshots/NB1_C4.png)

![NB1 keyword top-5](screenshots/NB1_C5.png)

![NB1 paraphrase query](screenshots/NB1_C6.png)

### NB2 — Hybrid Search & Precision@10

![NB2 precision table](screenshots/NB2_C4.png)

![NB2 query type slices](screenshots/NB2_C5.png)

### NB3 — FastAPI Search Benchmark

![NB3 API response](screenshots/NB3_C2.png)

![NB3 latency table](screenshots/NB3_C3.png)

![NB3 hybrid P99 assertion](screenshots/NB3_C4.png)

### NB4 — Feast Feature Store

![NB4 feast apply](screenshots/NB4_C2.png)

![NB4 materialize](screenshots/NB4_C3.png)

![NB4 online lookup latency](screenshots/NB4_C4.png)

![NB4 PIT join](screenshots/NB4_C5.png)

---

## Bonus challenge

- [ ] Đã làm bonus (xem `bonus/`)
- [ ] Pair work với: N/A
