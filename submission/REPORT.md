# Báo cáo Day 08 — 03048 - Lâm Trung Hiếu

> Một file duy nhất cho cả bài (đã gộp recipe, QC và ghi chú cá nhân). Mọi con số kèm **mẫu số** và nguồn (file nào). Viết bằng lời của bạn.

## 1. Model và recipe (Part 2–3)

| Lớp | Model + cỡ | Ngưỡng | Vì sao (dẫn `run_id` trong `model_log.csv`) |
|---|---|---|---|
| person / bicycle / motorbike / car / bus / truck | YOLO26m | mặc định 0.3 cho cả 6 lớp (`--conf 0.3`) | r01/r02: 0.5 làm mất nhiều person/motorbike nhỏ (person 131 -> 87 box trên pilot). Sweep: person, motorbike, car không ngưỡng nào <= 0.5 đạt recall 90% (tối đa 83% / 88% / 83%), và ở 0.3 recall bằng 0.15 nhưng ít FP hơn (person FP 20 so với 32; motorbike 6 so với 16). bicycle (1 vật), bus và truck (0 vật) quá ít mẫu gold nên không chọn ngưỡng riêng |
| three_wheeler | YOLOE-26s, prompt: `three_wheeler` | 0.15 (`--thr "three_wheeler=0.15"`) | r03: YOLOE tìm được tuk-tuk và xích lô mà YOLO26 bỏ sót hoặc gọi là car (r01, r04). Sweep: 0.15 cho recall 100% (6/6 vật gold), precision 67% (6/9); 0.3 tụt còn recall 67% (4/6) |

- Lệnh `merge_prelabels.py` đã dùng (dán nguyên): `python scripts/merge_prelabels.py work/prelabel/yoloe_all/pre.coco.json work/prelabel/y26_all/pre.coco.json --thr "three_wheeler=0.15" --conf 0.3 --iou 0.6 --split "batch,gold" --out work/prelabel/merged_review/pre.coco.json`
- **Phiên bản SAM bạn chọn** (SAM 1 / 2.1 / 3) và lý do: SAM 2.1 base (`sam2.1_b.pt`, r04). Mask bám sát người và thân tuk-tuk khi box đúng; chạy được trên CPU, RAM 15 GB (5.9 s/ảnh), không cần token HuggingFace như SAM 3.
- Lỗi nào **không sửa được bằng đổi ngưỡng** (ví dụ tuk-tuk bị gọi `car`)? Sửa thế nào? YOLO26 không có lớp tuk-tuk: ở img_002 tuk-tuk xanh bị bỏ sót hoàn toàn, ở img_004 tuk-tuk bị gọi `car` (0.37, 0.34). Hạ hay nâng ngưỡng đều không đổi được nhãn. Sửa bằng cách thêm YOLOE cho `three_wheeler` và khi ghép (`merge_prelabels.py`, IoU >= 0.6) cho `three_wheeler` thắng `car`/`truck`.
- Box **điểm cao mà sai** hoặc **điểm thấp mà đúng** (ảnh nào): điểm thấp mà đúng: img_011, xe 3 bánh bị cắt ở mép trái chỉ 0.28 (YOLOE). Điểm khá mà sai: img_002, YOLOE gọi xe máy/xe đẩy là three_wheeler (0.40) và gọi pickup là three_wheeler (0.37), trong khi YOLO26 đã ra pickup là truck 0.73.
- Giới hạn: chọn ngưỡng trên chính gold (4 ảnh) nên số đo máy trên gold là lạc quan: ngưỡng 0.15 của three_wheeler chỉ dựa trên 6 vật trong 4 ảnh, chọn và chấm trên cùng dữ liệu; bus/truck không có vật nào trong gold nên không đo được. Cần kiểm chứng lại trên 24 ảnh batch ở Part 4.

## 2. AI error profile (từ `qc/review_stats.md`)

| Trạng thái | Số | Tỉ lệ | Mẫu số |
|---|---|---|---|
| accepted | 515 | 99.4% | 518 box máy |
| edited | 1 | 0.2% | 518 box máy |
| deleted | 2 | 0.4% | 518 box máy |
| added | 0 | 0.0% | 516 đối tượng sau duyệt |

- Lớp nào máy tệ nhất? Vì sao (dẫn ảnh)? `person`: nhiều box person nhỏ chồng nhau ở đám đông (img_002); sweep trên gold: recall tối đa 83% (15/18), ở ngưỡng 0.3 có 20 FP.
- So với gold: precision / recall của **máy** 44.6% (KTC 95%: 34–56%) / 84.6% (KTC 95%: 70–93%); TP 33, FP 41, FN 6 (mẫu số: 39 đối tượng gold, 4 ảnh; nguồn `qc/review_stats.md`)

## 3. Thiên kiến tự động hóa và ảnh bẫy

- Bắt bẫy: 1/12 = 8.3% (KTC 95%: 1–35%); loại nào lọt: wrong_class 3/3, missing 3/3, loose 3/3, extra 2/3 (bắt được 1 bẫy extra); vì sao (bạn đã bỏ bước nào của checklist)? Tôi có xem các ảnh nhưng tin nhãn máy: không ẩn nhãn máy và không quét ảnh trước theo checklist, nên không thấy lỗi. Ngoài ra các chỉnh sửa sau img_003 không được lưu lên CVAT (job lưu lần cuối 18:04), nên bản export chỉ có thay đổi ở img_003.
- Accepted cao mà bắt bẫy thấp (hoặc ngược lại) nói gì về cách bạn duyệt? Theo tôi máy làm tốt phần lớn nên giữ nguyên là hợp lý, còn bẫy khó phát hiện.

## 4. Máy có đáng dùng không?

- Thời gian (từ `time_log.csv`): gán tay 2.5 phút/ảnh (10 phút / 4 ảnh) vs duyệt 20 phút nhưng chỉ duyệt xong 1/24 ảnh (img_003), nên không tính được phút/ảnh cho cả lô. Thiên lệch (bạn gán gold trước nên đã quen cảnh): <<>>
- Kết luận: có, dựa trên recall máy 84.6% (33/39 đối tượng gold): pre-label giúp không phải vẽ từ đầu.
- **Ba quy tắc giảm thiên kiến của bạn** (mỗi quy tắc kiểm tra được bằng số hoặc việc làm):
  1. Quét ảnh trước: ẩn nhãn máy, đếm vật bằng mắt rồi mới bật nhãn; kiểm được: 24/24 ảnh có ghi số vật đếm tay.
  2. Lưu sau mỗi ảnh: Ctrl+S sau mỗi ảnh và kiểm tra `updated_date` của job sau mỗi 5 ảnh.
  3. Box conf < 0.5 phải kiểm: mọi box máy conf < 0.5 phải được mở và xác nhận; kiểm được bằng tỉ lệ edited/deleted ở nhóm này.
  4. Bắt bẫy ≥ 10/12 mới nộp: chạy `review_stats.py` trước khi nộp; bắt bẫy < 10/12 thì duyệt lại lô.

## 5. Mask SAM cho 3 vật (Part 5)

| Ảnh | SAM (phiên bản) | Số click | Mask gồm người lái / hàng hoá? | Lỗi quan sát | File trong `masks/` |
|---|---|---|---|---|---|
| img_003 | SAM 2.1 base (`sam2.1_b.pt`) | 1 click dương + box YOLOE | có, gồm người lái | <<>> | `three_wheeler_img_003.jpg` |
| img_008 | SAM 2.1 base (`sam2.1_b.pt`) | 1 click dương + box YOLOE | có, gồm người lái | <<>> | `three_wheeler_img_008.jpg` |
| img_010 | SAM 2.1 base (`sam2.1_b.pt`) | 1 click dương + box YOLOE | có, gồm người lái | <<>> | `three_wheeler_img_010.jpg` |

- Đối chiếu guideline mục 4.2: quy tắc nào giúp, quy tắc nào thiếu? <<>>
- *(Tuỳ chọn)* Interactor SAM trong CVAT: làm được / không (lỗi gì, đã thử gì); khác gì offline: <<>>

## 6. Calibration (Part 6)

- Số quyết định: 3 (`calibration_decisions.csv`: CAL-01 `loi_may`, CAL-02 và CAL-03 `cau_hoi_mo`); quan trọng nhất (dẫn `CAL-xx`): CAL-01 (tuk-tuk bị gọi `car`).
- Quy tắc mới đã vào `guideline_v1.1_calibrated.md`: xe ba bánh luôn là `three_wheeler` (CAL-01); box chồng nhau giữ box tốt nhất (CAL-02); xe đỗ dày gần camera vẽ từng xe ≥ 20 px, thấy ≥ 50%, còn lại `ignore_region` (CAL-03).
- Nguyên nhân gốc: máy.

## 7. QC và quyết định (Part 6)

- Mẫu: 5 ảnh (0 ảnh `can_review` + 5 ngẫu nhiên, seed 42: img_003, img_006, img_014, img_031, img_035); người kiểm: bạn (**hạn chế**: bạn vừa là người duyệt).
- Lỗi theo **đối tượng**: chưa kiểm (0/5 ảnh mẫu được kiểm, 109 đối tượng trong mẫu) · theo **ảnh**: chưa kiểm (ngưỡng Release ≤ 2%). `qc_review.csv` để trống, `qc_report_auto.md` ghi rõ "5 ảnh trong mẫu CHƯA kiểm".
- Top lỗi (trong: bỏ sót, thừa, sai lớp, sai vị trí/kích thước, sai thuộc tính, sai mask) + một ảnh ví dụ mỗi loại: không có số: mẫu QC chưa được kiểm (0/5 ảnh).
- **Giới hạn mẫu nhỏ** (cận trên 95% trong `qc_report_auto.md`): `qc_report_auto.md` tính cận trên 43% với 0 lỗi / 5 ảnh, nhưng con số này không dùng được vì 5 ảnh mẫu chưa được kiểm. Kể cả khi kiểm, 5 ảnh không đủ để chứng minh ngưỡng ≤ 2%.
- Script kiểm được / không kiểm được (ví dụ ôm sát, cùng bỏ sót với máy, theo checklist thật): <<>>

**Quyết định: Rework**, ngày 2026-11-17. Lý do (đi theo Hold → Rework → Release): không Hold vì guideline đủ rõ cho lô và dữ liệu không hỏng; Rework vì bắt bẫy 1/12 < 10/12, chỉ duyệt 1/24 ảnh và QC chưa kiểm.
Nếu Rework / Hold, việc cần làm tiếp: <<>>

## 8. Ghi chú cá nhân

- **Dùng AI để làm bài** (công cụ nào, việc gì, kiểm tra thế nào; "không dùng" nếu không): Claude Code (Claude) trong VS Code. Việc AI làm: cài môi trường và tải model; chạy các script `prelabel.py`, `threshold_sweep.py`, `merge_prelabels.py`, `inject_traps.py`, `review_stats.py`, `sam2_points.py`, `build_release.py`, `qc_sample.py`, `qc_report.py`; viết `scripts/cvat_create_review_task.py` để tạo Task `batch-review` qua API CVAT; commit / push. **AI đã xem 6 ảnh `viz/` ở Part 2** (gửi ảnh lên dịch vụ AI đám mây, trái RULES nếu chưa được phép) và **viết nháp nhận xét trong `model_log.csv` và mục 1 báo cáo này**. Ở Part 5, AI chọn 3 vật bằng box `three_wheeler` có điểm YOLOE cao nhất (không nhìn ảnh). AI không duyệt nhãn, không điền QC. Ở Part 6, AI gom các ca khó và đưa phương án cho 3 ca calibration; tôi chọn phương án, AI ghi vào `calibration_decisions.csv` và `guideline_v1.1_calibrated.md`. Tôi kiểm tra bằng: <<>>
- Gold có bị nhiễm không (bạn có nhìn pre-label hay hỏi AI trước khi gán xong)? có, như sau: tôi đã xem pre-label (nhãn máy) của ảnh gold trước khi gán xong. Gold bị nhiễm, nên precision / recall của máy trên gold và ngưỡng chọn ở Part 3 có thể lệch về phía máy.
- Máy / GPU / CVAT dùng; vướng mắc cài đặt: Ubuntu Linux, không GPU (CPU), RAM 15 GB; CVAT v2.81.0 bằng Docker Desktop. Thiếu gói `python3-venv` nên tạo venv bằng `virtualenv`. Ổ đĩa chỉ còn ~5 GB trống. Trang cài đặt không tải `yolo26m.pt` mà lab cần, phải tải thêm bằng `download_models.py --set core`.
- Dùng cache `data/cache/` thay vì tự chạy? không, tự chạy `prelabel.py` trên CPU.
- Lỗi / bug script đã gặp (nếu có): lần đầu chạy `cvat_create_review_task.py`, Task bị gắn vào Project cũ `project-day2` (thiếu nhãn `motorbike`) nên import lỗi; đã xoá Task đó và tạo Task độc lập với nhãn từ `cvat/labels_generated.json`. Khi duyệt, các lần Save sau 18:04 không tới server CVAT.
- Một điều bạn làm khác lần sau: <<>>
