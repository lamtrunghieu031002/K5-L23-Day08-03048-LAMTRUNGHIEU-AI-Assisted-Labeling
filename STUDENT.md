# Thông tin học viên

- Họ và tên: Lâm Trung Hiếu
- MSHV: 03048
- Lớp (L2 / L3 / khác): L23
- Tài khoản GitHub: lamtrunghieu031002
- Repo bài nộp (URL): https://github.com/lamtrunghieu031002/K5-L23-Day08-03048-LAMTRUNGHIEU-AI-Assisted-Labeling
- Commit chốt bài (hash): 5aaef9d
- Máy: Ubuntu Linux, không có GPU (chạy CPU), RAM 15 GB
- CVAT (Docker): v2.81.0 (API báo 2.74.1)

## Kết quả tóm tắt (điền cuối bài; số lấy từ `submission/qc/*`, kèm mẫu số)

- Máy: accepted / edited / deleted: 515 / 1 / 2 (mẫu số: 518 box máy); added: 0 (mẫu số: 516 đối tượng)
- So với gold: precision / recall của **máy** 44.6% / 84.6% (mẫu số: 39 đối tượng gold, 4 ảnh)
- Bắt bẫy: 1/12 = 8.3%
- Thời gian: gán tay 2.5 phút/ảnh (10 phút / 4 ảnh); duyệt có pre-label 20 phút nhưng chỉ duyệt xong 1/24 ảnh
- Lỗi QC: chưa kiểm (0/5 ảnh mẫu), không có số
- **Quyết định:** Rework — lý do một dòng: bắt bẫy 1/12 < 10/12, chỉ duyệt 1/24 ảnh, QC chưa kiểm
