# Số đo review (det)

- Ảnh tính: 24 (batch,gold); box máy: 518; đối tượng sau duyệt: 516; ngưỡng accepted: IoU >= 0.9
- Đã **loại 27 đối tượng nằm quanh các bẫy** khỏi bảng này: lỗi nhân tạo không phản ánh chất lượng máy.

## 1. Bốn trạng thái (AI error profile)
| Trạng thái | Số | Tỉ lệ | Mẫu số |
|---|---|---|---|
| accepted (giữ nguyên) | 515 | 515/518 = 99.4% | 518 box máy |
| edited (sửa) | 1 | 1/518 = 0.2% | 518 box máy |
| deleted (xoá) | 2 | 2/518 = 0.4% | 518 box máy |
| added (vẽ thêm) | 0 | 0/516 = 0.0% | 516 đối tượng sau duyệt |

Trong số deleted + added, **0 trường hợp là đổi lớp** (máy gán sai lớp, box đúng chỗ): đó không phải máy bỏ sót. Số vật máy **sót thật** ≈ added − đổi lớp = 0.

### Theo lớp
| Lớp | accepted | edited | deleted | added |
|---|---|---|---|---|
| person | 269 | 0 | 0 | 0 |
| bicycle | 8 | 0 | 0 | 0 |
| motorbike | 135 | 0 | 0 | 0 |
| car | 54 | 0 | 0 | 0 |
| bus | 3 | 0 | 0 | 0 |
| truck | 6 | 0 | 0 | 0 |
| three_wheeler | 40 | 1 | 2 | 0 |

## 2. So với gold (nhãn gán tay từ đầu)
Ảnh gold: 4; đối tượng gold: 39 (mẫu số của recall)
| | TP | FP | FN | Precision | Recall |
|---|---|---|---|---|---|
| Máy (pre-label) | 33 | 41 | 6 | 44.6% (KTC 95%: 34–56%) | 84.6% (KTC 95%: 70–93%) |

*Lạc quan: ngưỡng được chọn trên chính các ảnh gold này (in-sample), và chỉ có 4 ảnh. Đọc khoảng tin cậy, đừng đọc con số đơn.*


(Ảnh gold không nằm trong nhãn sau duyệt: không tính residual / new error. Đó là chủ ý: duyệt lại ảnh bạn vừa tự gán tay sẽ đo trí nhớ, không đo thiên kiến.)

## 3. Ảnh bẫy
- Bắt được 1/12 = 8.3% (KTC 95%: 1–35%) (ngưỡng đạt: 80%). Chỉ 12 bẫy nên khoảng tin cậy rất rộng: đọc cùng danh sách bẫy lọt, đừng kết luận chỉ từ %.
  - wrong_class: 0/3
  - extra: 1/3
  - missing: 0/3
  - loose: 0/3
  - lọt: img_026.jpg (wrong_class), img_034.jpg (missing), img_028.jpg (missing), img_014.jpg (loose), img_031.jpg (wrong_class), img_006.jpg (extra), img_025.jpg (extra), img_033.jpg (wrong_class), img_021.jpg (loose), img_013.jpg (loose), img_010.jpg (missing)

## Gợi ý đọc số
- `deleted` cao → ngưỡng thấp hoặc ánh xạ nhãn sai; `added` cao → máy bỏ sót (xem lớp nào);
- `accepted` thấp (< 50%) → sửa mỗi box lâu hơn vẽ mới: đổi model/ngưỡng hoặc vẽ tay;
- bắt bẫy < 80% → duyệt lại lô, siết checklist (quét ảnh TRƯỚC khi nhìn nhãn máy).
