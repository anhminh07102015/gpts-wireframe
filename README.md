# GPTS An Tín — Wireframe HTML

Bộ wireframe thao tác được cho hệ thống quản lý cầm đồ GPTS (An Tín × Mona).
Mỗi màn hình là một file HTML tĩnh riêng, không cần build, mở trực tiếp hoặc host tĩnh đều chạy.

## Cấu trúc
```
index.html                      Mục lục các màn
01-danh-sach-khach-hang.html    Danh sách khách hàng
02-tao-khach-hang.html          Tạo khách hàng (cảnh báo tuổi, CCCD tách Passport)
03-tao-hop-dong.html            Lên HĐCC (chọn KH, modal thêm TSCC 2 phương pháp định giá)
04-danh-sach-hop-dong.html      Danh sách HĐCC (vòng đời trạng thái)
05-duyet-ho-so.html             Duyệt hồ sơ bước 1 (duyệt / trả về / từ chối)
06-duyet-giai-ngan.html         Duyệt giải ngân bước 2 + đề nghị thanh toán (export Vietinbank)
07-luong-xuat-hoa-don.html      Pipeline thu tiền → SAP xuất HĐĐT
assets/style.css, assets/app.js Style + tương tác dùng chung
gen.py                          Generator (sửa nội dung thì sửa ở đây rồi chạy `python gen.py`)
```

## Chạy local
Mở thẳng `index.html` bằng trình duyệt, hoặc:
```
python -m http.server 8000
```

## Deploy
Repo này là site tĩnh thuần — Vercel/Netlify/GitHub Pages nhận trực tiếp,
không cần cấu hình build (Framework preset: Other, Output: ./).

## Ghi chú
Số liệu trong wireframe là minh họa; đơn vị lãi suất 1.5 và phí bảo quản 3 bậc
đang chờ An Tín xác nhận chính thức.
