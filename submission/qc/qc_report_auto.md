# Báo cáo QC tự động (nháp)

> **Gợi ý** do script tính; bạn xác nhận. Script chỉ đếm theo phiếu kiểm bằng mắt người.

## Mẫu
- 5 ảnh (0 ca khó + 5 ngẫu nhiên), 109 đối tượng.
- taxonomy v1.0

## Số đo
| Chỉ số | Giá trị | Mẫu số |
|---|---|---|
| Lỗi **theo đối tượng** | 0/109 = 0.0% | 109 đối tượng trong mẫu |
| **Ảnh có lỗi** (dùng cho ngưỡng) | 0/5 = 0.0% | 5 ảnh trong mẫu |
| Máy: accepted / edited / deleted | 515/518 = 99.4% / 1/518 = 0.2% / 2/518 = 0.4% | 518 box máy |
| Máy: added | 0/516 = 0.0% | 516 đối tượng sau duyệt |
| Bắt lỗi bẫy | 1/12 = 8.3% | 12 bẫy |

## Top 3 loại lỗi
(không ghi nhận lỗi nào)

## Cảnh báo
- 5 ảnh trong mẫu CHƯA kiểm: img_003.jpg, img_006.jpg, img_014.jpg, img_031.jpg, img_035.jpg

## Giới hạn thống kê
- 0 ảnh lỗi trong 5 ảnh mẫu: cận trên 95% (Wilson) của tỉ lệ ảnh lỗi thật là **43%**. Ngưỡng 2% không thể được **chứng minh** bằng mẫu nhỏ như vậy: hãy nói rõ giới hạn này trong báo cáo.

## Gợi ý quyết định
**REWORK**

- bắt bẫy 8% < 80% -> lô duyệt chưa đáng tin
- LƯU Ý: còn ảnh mẫu chưa kiểm -> kết luận chưa đáng tin

Cây quyết định: Hold (guideline chưa rõ / dữ liệu hỏng) -> Rework (> ngưỡng, lỗi lặp, bắt bẫy / nhất quán thấp) -> Release.
