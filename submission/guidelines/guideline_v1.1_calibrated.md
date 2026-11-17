# Label contract — Phố châu Á — BỔ SUNG v1.1 — 03048 - Lâm Trung Hiếu

> **Chỉ viết phần thay đổi so với v1.0** (không copy cả file). Chốt các câu hỏi mở ở mục 6 của v1.0 (hoặc nói rõ câu nào chưa chốt, vì sao)
> và thêm quy tắc mới rút ra từ lỗi của máy / lỗi của bạn. Mỗi ca khó **có ảnh ví dụ** (`img_0xx`) và khớp một dòng trong `qc/calibration_decisions.csv`.

## 1. Câu hỏi mở đã chốt (từ mục 6 của v1.0)

| # | Câu hỏi | Quyết định | Ảnh ví dụ | `case_id` |
|---|---|---|---|---|
| 2 | Khối xe máy đỗ dày đặc gần camera: từng xe hay `ignore_region`? | Xe cao ≥ 20 px và thấy ≥ 50% thì vẽ box riêng; phần còn lại gom vào `ignore_region` | img_018 | CAL-03 |
| 6 | Box máy chồng nhau quá nhiều trên một vật: gộp hay giữ? | Giữ box khớp vật tốt nhất, xoá các box còn lại, không vẽ lại | img_003 | CAL-02 |

Câu 1, 3, 4, 5, 7 chưa chốt: trong lô không có đủ ca để quyết (chỉ duyệt 1/24 ảnh).

## 2. Ca khó mới (từ lỗi của máy, bẫy lọt, box `can_review`)

| Ảnh | Tình huống | Máy làm gì (model nào) | Quyết định của bạn | Quy tắc mới (vào mục nào của v1.0) |
|---|---|---|---|---|
| img_004 (và img_002) | Tuk-tuk có mui | YOLO26-m gọi tuk-tuk là `car` (0.37, 0.34) ở img_004, bỏ sót tuk-tuk ở img_002 | Luôn gán `three_wheeler`, đổi lớp box `car`/`truck` của máy | Mục 2: mọi xe ba bánh (tuk-tuk, xích lô, ba gác, có mui hay không) là `three_wheeler` (CAL-01) |

## 3. Lịch sử thay đổi

| Phiên bản | Thay đổi | Lý do (ca nào, `case_id`) |
|---|---|---|
| v1.0 | Bản giảng viên | — |
| v1.1 | Chốt câu mở 2 (xe đỗ dày gần camera) và 6 (box chồng nhau); thêm quy tắc xe ba bánh luôn là `three_wheeler` | CAL-01, CAL-02, CAL-03 |
