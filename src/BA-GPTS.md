# BA — GPTS: Hệ thống quản lý cầm đồ An Tín × Mona

> **Tài liệu này dành cho AI/developer đọc để code.** Nó tổng hợp toàn bộ điểm ĐÃ CHỐT với khách hàng
> (Công ty CP Giải pháp Tài sản An Tín) qua các buổi họp 12/08 → 20/08/2026 và các template đã trao đổi.
>
> **QUY ƯỚC BẮT BUỘC KHI ĐỌC:**
> - `[CHỐT]` = đã thống nhất với khách, code đúng theo mô tả, KHÔNG tự ý đổi.
> - `[CHỜ CHỐT]` = chưa có quyết định cuối. KHÔNG tự bịa giá trị/logic — code phải để dạng **cấu hình được**
>   hoặc để TODO kèm ghi chú, và hỏi lại con người trước khi hard-code.
> - `[VÊNH]` = hai nguồn thông tin mâu thuẫn nhau, đang chờ khách phân xử. Tuyệt đối không tự chọn một phía.
> - Wireframe tham chiếu UI: repo https://github.com/anhminh07102015/gpts-wireframe (8 file HTML, mỗi màn 1 file).

---

## 1. Tổng quan

- **Sản phẩm:** phần mềm quản lý nghiệp vụ cầm đồ (GPTS) cho chuỗi cửa hàng An Tín (hệ sinh thái PNJ).
  Tài sản cầm chủ yếu: vàng, nữ trang, kim cương.
- **Tích hợp:** SAP FI (kế toán An Tín) và Vietinbank (chi tiền UNC). GĐ1 qua file Excel, GĐ2 qua API.
- **Vận hành:** `[CHỐT]` app deploy trên hạ tầng do An Tín cấp (dự kiến AWS hoặc Viettel Cloud),
  An Tín KHÔNG nhận bàn giao source code. Mona nợ khách tài liệu kiến trúc + checklist an ninh (đầu mối info: Lê Văn Hiếu).
- **Stack dự kiến (nội bộ Mona, không phải cam kết với khách):** Golang (Gin) + PostgreSQL + Redis; RBAC lưu bảng DB.
  Kiểu dữ liệu trong file khai báo trường viết theo PostgreSQL.
- **Vai trò chính:** TVV (tư vấn viên, nhập liệu), Thợ kỹ thuật (kiểm định), BP.TĐVPD (duyệt hồ sơ bước 1),
  Người duyệt giải ngân (bước 2), Kế toán thanh toán (duyệt đề nghị thanh toán, chi tiền, đối soát),
  P.VHKD (duyệt giảm lãi/phí), Admin (cấu hình, sửa thông tin KH đã có HĐCC), P.TCKT (định giá kim cương rời — mới, xem §12).
- **Thuật ngữ:** HĐCC = hợp đồng cầm cố · TSCC = tài sản cầm cố · ĐNTT = đề nghị thanh toán ·
  TKTG = tài khoản tiền gửi · SBT = số bút toán · BP = Business Partner (mã KH bên SAP) ·
  GĐ1/GĐ2 = giai đoạn MVP / Custom · HĐĐT = hóa đơn điện tử.

## 2. Cấu trúc tổ chức & phân quyền

- `[CHỐT]` Đơn vị vận hành theo **chi nhánh**. Thợ kỹ thuật là user role "Thợ", cấu hình thuộc chi nhánh;
  mọi dropdown chọn thợ mặc định lọc theo chi nhánh hiện tại + có toggle "hiện thợ tất cả chi nhánh";
  hiển thị kèm email + chi nhánh + mã NV để phân biệt trùng tên (chốt 19/8).
- `[CHỜ CHỐT]` ⚠ Bộ template report mới (nhận 08/09) xuất hiện thêm cấp **CỬA HÀNG dưới CHI NHÁNH**
  (MÃ/TÊN CỬA HÀNG đứng đầu cả 4 template). Trước đó mọi tài liệu chỉ nói chi nhánh.
  → Data model nên thiết kế sẵn 2 cấp (branch → store) nhưng CHƯA hard-code nghiệp vụ nào theo cửa hàng
  cho tới khi khách xác nhận số cấp thực tế.
- `[CHỐT]` RBAC: duyệt hồ sơ và duyệt giải ngân là 2 quyền tách biệt; giảm lãi/phí cần phê duyệt đúng thẩm quyền
  (P.VHKD); kế toán thanh toán là vai trò riêng xử lý ĐNTT.
- GĐ2 (C5): phê duyệt tập trung theo hạn mức/lịch trực, nhiều cấp — GĐ1 chưa làm.

## 3. Module Khách hàng (wireframe: 01, 02)

### 3.1 Trường dữ liệu & rule `[CHỐT]`
- **CCCD và Passport/CCCD quân đội tách 2 field riêng** (chốt 19/8). CCCD validate cấu trúc số
  (logic check hợp lệ: Mona sẽ trình buổi sau — `[CHỜ CHỐT]` chi tiết thuật toán), UNIQUE toàn hệ thống,
  là **khóa định danh duy nhất** (chốt 12-13/8). KH đưa passport: ưu tiên nhập số CCCD in trong passport vào trường CCCD.
  Căn cước quân đội (~1% KH): chấp nhận rủi ro có thể sinh 2 mã cho 1 người, xử lý sau nếu phát sinh nhiều.
- **Ngày sinh:** dưới 18 hoặc trên 70 tuổi → chỉ **CẢNH BÁO, không chặn** giao dịch (chốt 19/8).
- **Địa chỉ liên hệ:** bắt buộc (theo phản hồi template v2 của khách). Địa chỉ thường trú theo giấy tờ.
- **Nguồn KH** dropdown 6 nhóm: PNJ/CAF · Ngân hàng · Doanh nghiệp/Sỉ · Tiệm vàng · NV nội bộ PNJG · Vãng lai.
- **Mã KH An Tín:** hệ thống tự sinh. **Mã KH PNJ:** nhập tay, không bắt buộc.
- **Hạng KHTT (Gold/Diamond/…):** hệ thống tự phân hạng theo dư nợ; hạng **chỉ dùng để GIẢM PHÍ bảo quản**,
  KHÔNG bao giờ đổi lãi suất (chốt 19/8 — lãi luôn cố định 1.5, xem §7).
- **Hình KH + CCCD 2 mặt:** upload, lưu tại hồ sơ KH, cập nhật được khi KH đổi giấy tờ.
- **Nghề nghiệp:** `[CHỜ CHỐT]` có bắt buộc hay không.
- **Sửa thông tin KH** (chốt 19/8): KH **chưa có HĐCC** → TVV được sửa; KH **đã có HĐCC** → chỉ Admin sửa.
  Mọi lần điều chỉnh phải log lịch sử: thông tin trước/sau + user duyệt (phục vụ report TEMPLATE KH, §11).

### 3.2 Đồng bộ SAP `[CHỐT]` (MoM 12-13/8)
- Hai bên giữ bộ mã riêng, **tham chiếu 2 chiều** qua trường tham chiếu. SAP đã tạo dải mã riêng cho An Tín
  (không dùng chung dải PNJ).
- GĐ1 (MVP-6): sync Business Partner (KH + vendor) Mona → SAP. GĐ2: Mona gọi API tạo KH sang SAP,
  **mã KH SAP nằm trong response** → Mona lưu vào trường tham chiếu. KHÔNG cần SAP gọi API ngược lên Mona.
- Mona chặn trùng CCCD nên không phát sinh trùng khi đẩy xuống SAP.

## 4. Module Tài sản cầm cố (wireframe: modal trong 03)

### 4.1 Nguyên tắc `[CHỐT]`
- **1 HĐCC có thể nhiều TSCC** (chốt kick-off). Trị giá, tỷ lệ, quyền sở hữu, thợ… gắn theo TỪNG TSCC.
- **Loại TSCC:** danh mục 11 nhóm (bản cập nhật sheet 2.TSCC ngày 08/09): TSCN Ý có đá chính là KC ·
  TS đá màu · TS kim cương · Nữ trang trọng lượng · TS ngọc trai · Khác (Style by PNJ) · Nguyên liệu ·
  TS ECZ/CZ · TS KGĐ-dây-TSCN Ý · TS vỏ · **Kim cương rời (mới)**.
- **Tuổi vàng (%):** dropdown 41,6 / 58,5 / 61 / 68 / 75 / 90 / 95 / 99 / 99,9 / 99,99 + cho nhập giá trị khác.
- **Trọng lượng:** đơn vị **chỉ**, numeric(10,3) — trọng lượng vàng (đá) và trọng lượng tổng là 2 trường.
- **Quyền sở hữu TSCC:** chính chủ / không chính chủ — theo từng TSCC (chốt 19/8).
- **Thợ kỹ thuật:** xem §2. Hình thức kiểm định: Thợ cửa hàng / PNJL / Bên thứ ba / Cầm không thợ
  (danh mục cầm-không-thợ + tỷ lệ cầm cấu hình trước).
- **Niêm phong:** 1 hồ sơ gắn được nhiều tem (nhập tay v1, module kho tem = CR báo giá riêng);
  trường lý do tem hủy/rớt số; số lượng + trọng lượng hộp/túi niêm phong trên HĐCC.
  Hình bắt buộc: hình sản phẩm chi tiết, hình hộp/túi đã niêm phong (rõ số tem), hình giấy kiểm định 2 mặt.
- Trường bổ sung theo bản 08/09: **Mã SP theo hóa đơn** (bắt buộc khi cầm theo hóa đơn),
  **SIZE** (bắt buộc, chỉ hiện khi định giá theo thị trường), **NƯỚC**, **ĐỘ SẠCH**,
  **Giấy kiểm định GIA**, **Giấy kiểm định PNJLAB/khác** (2 trường giấy nhập cho cả 2 phương pháp).
  Trường "Đặc điểm nhận dạng" (bản cũ) đã bỏ.

### 4.2 Định giá — 2 phương pháp `[CHỐT]` + 1 nhánh mới `[CHỜ CHỐT]`
- Radio chọn phương pháp, UI chỉ hiện input của nhánh được chọn. **TVV không đổi được tỷ lệ nằm trong công thức.**
- **Theo hóa đơn:** nhập số hóa đơn (PNJ/CAO/DOJI/SJC…), mã SP theo hóa đơn, giá theo hóa đơn,
  giảm trừ + lý do. `Trị giá TSCC = (Giá theo hóa đơn − Giảm trừ) × Tỷ lệ thu lại`.
- **Theo thị trường:** giá bóng lấy từ **cấu hình theo thời kỳ** (admin cập nhật).
  `Trị giá TSCC = Trọng lượng vàng × Tuổi vàng × Giá bóng`.
- **Tỷ lệ thu lại:** cấu hình theo loại TSCC → hệ thống GỢI Ý khi chọn loại, **TVV được chỉnh tay** (chốt 19/8, khớp bản 08/09).
- **Tỷ lệ cầm:** cấu hình theo **nguồn gốc/thương hiệu**, gắn theo TSCC, **khóa không cho TVV sửa**.
  `Hạn mức tài sản = Trị giá TSCC × Tỷ lệ cầm`. Hạn mức HĐCC = tổng hạn mức các TSCC.
- `[CHỜ CHỐT]` **Kim cương rời**: có trường "Giá TSCC theo định giá (P.TCKT)" = kết quả định giá của
  Phòng Tài chính — tức nhánh định giá thứ 3. Luồng gửi P.TCKT (ai gửi, chờ bao lâu, ai nhập kết quả)
  và thuộc GĐ nào: chưa chốt. KHÔNG code luồng này khi chưa có mô tả.
- GĐ2 (C1): màn hình thẩm định/định giá nâng cao; (C5): định giá tự động.
- **Kho:** `[CHỐT]` SAP KHÔNG quản lý kho/nhập-xuất-tồn TSCC. Toàn bộ theo dõi trên GPTS (phiếu nhập/xuất kho — MVP-2);
  kế toán cần thì tra cứu trên GPTS.

## 5. Module HĐCC — tạo & duyệt (wireframe: 03, 04, 05, 06)

### 5.1 Tạo hợp đồng `[CHỐT]`
- Luồng: chọn KH (search theo CCCD/SĐT/tên/mã KH, hiện hạng + dư nợ hiện tại; không có thì tạo KH mới rồi quay lại)
  → thêm ≥1 TSCC → thông tin vay → upload chứng từ → gửi duyệt.
- **Số tiền cầm ≤ hạn mức** — không cho vay vượt (chốt kick-off; xem mục VÊNH §13.2).
  Hạn mức tính theo tiền vay, KHÔNG cộng lãi.
- **Mức sàn:** số tiền cầm ≥ 20% hạn mức và ≥ mức sàn tuyệt đối (`[CHỜ CHỐT]` 500k hay 1tr — anh Thọ/BP.KD quyết;
  cả 2 ngưỡng phải cấu hình được trong Admin).
- **Kỳ hạn GĐ1:** chỉ sản phẩm 30 ngày. Sản phẩm 60/90/180 ngày = GĐ2.
- **Chi vay:** chuyển khoản; tiền mặt xây sẵn UI nhưng TẮT tính năng. Nhập TK thụ hưởng (số TK, ngân hàng, chủ TK).
- **Chính sách ưu đãi** (chốt 19/8): "Chuẩn" = giảm phí theo hạng KH; "Ưu đãi đặc biệt 1/2" = mức phí cấu hình riêng.
  Nếu phí ưu đãi > phí theo chính sách chuẩn của KH đó → **cảnh báo** (không chặn).
- **Upload hình ảnh/chứng từ đính kèm HĐCC:** yêu cầu GĐ1 (khách đẩy từ Custom lên MVP tại kick-off).
- Bước 1–4 quy trình giấy làm ngoài hệ thống; **bước 5 nhập liệu lên hệ thống** — SLA xử lý tính từ bước 5.

### 5.2 Duyệt 2 bước `[CHỐT]` (họp nghiệp vụ + 19/8)
1. **Duyệt hồ sơ (bước 1)** — BP.TĐVPD. 3 nút: **Duyệt / Đề nghị chỉnh sửa (trả về) / Từ chối (hủy, có popup)**.
   - Trả về & từ chối: **bắt buộc nhập lý do**, người trả ghi rõ field cần sửa. Trả về → quay lại bước nhập liệu,
     TVV được sửa MỌI field (không giới hạn). Hồ sơ gửi lại: **chỉ hiển thị cho người duyệt cũ**
     (kèm bộ lọc dự phòng khi người đó nghỉ) và người duyệt **xem được DIFF các thông tin đã thay đổi**
     (không phải rà lại toàn bộ).
   - Từ chối/hủy: hồ sơ đóng, cho phép **Duplicate** thành hồ sơ mới.
2. Sau duyệt bước 1 → mở **In HĐCC + bảng lãi phí + biên nhận** (bộ mẫu in theo mẫu An Tín cung cấp).
   KH ký → TVV upload bản scan → chuyển bước 2.
3. **Duyệt giải ngân (bước 2)** — kiểm tra thông tin chi vay/thụ hưởng.
   Trả về do **sai thông tin thụ hưởng** → hồ sơ về TVV nhưng **CHỈ MỞ SỬA thông tin chi vay**, field khác khóa.
4. Duyệt giải ngân xong → tự tạo **Đề nghị thanh toán** chuyển kế toán. ĐNTT quản lý hoàn toàn trên hệ thống,
   hủy ĐNTT phải ghi lý do. Kế toán duyệt → **xuất file Excel import Vietinbank (UNC)** → tiền đi →
   kế toán bấm **Xác nhận đã chi tiền** (kèm SBT) → HĐ chuyển "Đang hiệu lực".
   Thời điểm FI ghi nhận phải thu = thời điểm KT thanh toán duyệt chi tiền (TH1).
5. **Sau giải ngân: khóa hồ sơ không cho sửa.** Chỉnh sửa sau duyệt (nếu có): An Tín sẽ làm rõ danh sách field
   + field nào đồng bộ SAP (SAP cung cấp API); TUYỆT ĐỐI không sửa thông tin tiền/lãi/phí/kế toán — `[CHỜ CHỐT]` danh sách field.

### 5.3 Trạng thái
- Trạng thái HĐ theo template report của khách: Nháp / Chờ phê duyệt / Đã phê duyệt / Chờ giải ngân / Đã giải ngân / …
  (+ nội bộ: Bị trả về, Đang hiệu lực, Quá hạn, Đã tất toán). Loại giao dịch: cầm mới / gia hạn thông thường /
  gia hạn vay thêm / gia hạn trả bớt.
- `[CHỜ CHỐT]` Sheet 2.TSCC ghi trường "Trạng thái HĐCC" nhưng danh mục là trạng thái TÀI SẢN
  (Chờ kiểm định / Đang cầm cố / Đã trả hàng / Thanh lý / Đóng hồ sơ…) — nghi lỗi đặt tên, cần khách xác nhận
  đó là Trạng thái TSCC.

## 6. Thu nợ / tất toán / chuộc (GĐ1: MVP-4)

- `[CHỐT]` **Báo có thủ công**: TVV in sổ phụ TKTG, đối chiếu và xác nhận tiền vào trên hệ thống (không tự động đối soát GĐ1;
  đối soát CK tự động = GĐ2/C5).
- `[CHỐT]` **Cutoff 17h**: tiền vào TKTG sau 17h → ghi nhận thu nợ vào NGÀY HÔM SAU. Ngày ghi nhận này kéo theo
  ngày tính lãi/phí, ngày dữ liệu đẩy FI và ngày SAP xuất HĐĐT.
- `[CHỐT]` Màn thu: 3 ô phải thu (nợ/lãi/phí) readonly + 3 ô thực thu; hệ thống **tự phân bổ theo thứ tự ưu tiên
  phí → lãi → nợ**, cho chỉnh tay. Giảm lãi / giảm phí là nghiệp vụ tách riêng và **phải có phê duyệt đúng thẩm quyền (P.VHKD)** —
  FI chỉ ghi nhận giảm theo dữ liệu đã duyệt trên GPTS.
- `[CHỐT]` GĐ1 chỉ có: trả đúng hạn hoặc **tất toán trước hạn TOÀN BỘ**. Thu tùy biến (trả một phần trong kỳ, TH5)
  và thu lãi/phí hàng tháng (TH7) = **GĐ2** (C2).
- `[CHỐT]` Thu đủ → hệ thống **tự động tất toán** HĐ.
- `[CHỐT]` **Tất toán tách riêng chuộc hàng**: KH chuyển khoản tất toán từ xa để DỪNG lãi/phí ngay;
  chuộc (nhận hàng) làm sau. **Phí bảo quản sau tất toán: miễn 3 ngày; từ ngày thứ 4 tính lại TỪ NGÀY TẤT TOÁN
  (tức tính trọn cả 4 ngày), chỉ tính PHÍ không tính lãi.**
- `[CHỐT]` Chuộc: upload hình KH + CCCD + biên bản ký (đối chiếu chữ ký với hồ sơ cầm ban đầu);
  nhận thay phải có ủy quyền; video ủy quyền chỉ dùng khi bất khả kháng (`[CHỜ CHỐT]` giới hạn dung lượng video).
  Chuộc nâng cao (cảnh báo quá hạn nhận, đối chiếu ảnh/chữ ký) = GĐ2 (C3).

## 7. Rule lãi – phí – VAT

- `[CHỐT]` **Lãi suất cố định 1.5** cho mọi KH, mọi hạng — hạng KH và ưu đãi chỉ tác động PHÍ.
  ⚠ `[CHỜ CHỐT]` **ĐƠN VỊ của 1.5** (%/tháng? ‰/ngày?) chưa được khách xác nhận bằng văn bản —
  code phải để tham số cấu hình `interest_rate`, KHÔNG hard-code đơn vị.
- `[CHỐT]` Lãi tính trên **nền số ngày thực tế** (số ngày cầm thực tế). `[CHỜ CHỐT]` cơ sở quy đổi năm 360/365
  (Mona đang dùng 365, An Tín còn tranh cãi nội bộ — Mona nợ gửi công thức tham khảo). Cách đếm đầu mút ngày: chưa chốt.
- `[CHỐT]` **Số ngày tính lãi tối thiểu: 15 ngày** (tất toán sớm hơn vẫn tính đủ 15 ngày).
- **Phí bảo quản 3 bậc theo dư nợ** (số trong template v2, `[CHỜ CHỐT]` đơn vị — template ghi "VNĐ/ngày" mâu thuẫn
  với giá trị dạng %): <50tr: 0.0205 · 50–300tr: 0.0177 · ≥300tr: 0.0123. Để bảng cấu hình `fee_tiers`.
- `[CHỐT]` **VAT 10% trên lãi + phí thực thu** — là căn cứ SAP xuất HĐĐT. Giá trị lãi/phí cấu hình là CHƯA gồm VAT.
  ⚠ `[VÊNH]` template report mới ghi cột "Lãi suất (đã bao gồm VAT)" — cần chốt cách trình bày trên report (§13).
- `[CHỐT]` Biên độ thu thiếu: thiếu ≤ ngưỡng (đang nói 1 ngày lãi) → chỉ **cảnh báo cho người duyệt** kèm số tiền thiếu,
  không chặn (mọi gia hạn đều qua duyệt nên người duyệt quyết). `[CHỜ CHỐT]` giá trị ngưỡng chính xác → cấu hình.

## 8. Gia hạn & vay thêm (GĐ1: MVP-5) `[CHỐT]`

- 3 loại **chung 1 màn hình**, chọn qua dropdown: gia hạn thông thường / gia hạn vay thêm / gia hạn trả bớt —
  nhưng tách rõ 3 loại trong module (data + report ghi loại giao dịch riêng).
- **Mọi gia hạn đều phải qua duyệt.** Điều kiện duyệt (MoM 12/8): thu hết lãi + phí phát sinh,
  KT xác nhận tiền đã vào TKTG, có điều khoản mặc nhiên gia hạn trong HĐCC hoặc tin nhắn xác nhận (SMS/Zalo).
- Gia hạn thông thường: cho tùy biến lãi suất + số ngày kỳ mới; không đổi gốc; xuất HĐĐT lãi/phí kỳ cũ (TH2).
- Vay thêm: chỉ trong hạn mức đã thẩm định, KHÔNG định giá lại, **KH phải tới quầy ký phụ lục**;
  phần giải ngân thêm chạy lại đủ luồng duyệt + ĐNTT + chi tiền (TH3).
- Trả bớt: dư nợ còn lại ≥ 20% HĐ ban đầu và ≥ mức sàn (cả 2 cấu hình Admin), vi phạm thì **chặn** (TH4).
- Hiển thị **số lần gia hạn**, không giới hạn tối đa. Có trường **tái định giá TSCC khi gia hạn** + lịch sử tái định giá
  (trị giá định giá lại, hạn mức sau tái định giá, ngày tái định giá — khớp TEMPLATE GIA HẠN).
- In phụ lục HĐ + bảng lãi/phí kỳ mới.
- `[CHỜ CHỐT]` hạn thông báo từ chối gia hạn: 5 ngày (nói trong họp) vs 3 ngày (quy trình gốc An Tín) → cấu hình.
- ⚠ `[VÊNH]` cú pháp chuyển khoản để nhận diện gia hạn thường/trả bớt: kick-off nói DÙNG, phản hồi template v2 nói BỎ (§13).

## 9. Thanh lý & nhắc nợ (GĐ2: C4) `[CHỐT]`

- Thanh lý 3 TH: KH tự chuộc / ủy quyền An Tín bán thay / bắt buộc — ủy quyền và bắt buộc chung luồng.
  Định hướng đã chốt: nhận ủy quyền từ khách bán thay (bỏ luồng "KH bán lại cho An Tín").
- GPTS **chỉ khai báo thông tin thanh lý** (giá bán, tờ trình, kết quả) + phí thanh lý (%) + report theo trạng thái.
  Kết nối bán hàng/FI phần thanh lý làm bên SAP — NGOÀI phạm vi Mona (lia ra tại kick-off, giữ gói khai báo).
- Tài sản chờ thanh lý **vẫn tính lãi + phí như đang cầm**.
- Nhắc nợ 3 lần: UI trải phẳng, DB log từng lần.

## 10. Tích hợp SAP (FI) & Vietinbank

### 10.1 Nguyên tắc `[CHỐT]` (MoM 12/08)
- SAP chỉ theo dõi **công nợ gốc + kỳ hạn công nợ** theo mã KH/HĐCC — KHÔNG theo dõi chi tiết lãi/phí từng KH.
- Lãi/phí chỉ đẩy về SAP theo **SỐ THỰC THU** để ghi nhận doanh thu và xuất HĐĐT.
- **HĐĐT lãi/phí xuất bên SAP, không xuất bên GPTS.** GPTS chịu trách nhiệm chuyển đúng-đủ-đúng ngày
  (phát sinh ngày nào bắn hóa đơn ngày đó, theo ngày ghi nhận cutoff 17h). Xem `[VÊNH]` HĐĐT §13.
- GĐ1: GPTS **xuất file Excel đúng format template** SAP/kế toán cung cấp, import thẳng không chỉnh sửa lại.
  GĐ2: API 2 chiều (Mona gọi, mã SAP trong response); spec API chốt ở buổi kỹ thuật riêng Mona × SAP.
- **Đối soát GPTS ↔ FI hàng ngày**: thu nợ / lãi / phí / giảm lãi phí / dư nợ cuối ngày.

### 10.2 Template import SAP (file khách gửi 08/09) — spec module export
**TEMPLATE HĐ SAP (KT)** — bút toán thu lãi/phí theo từng HĐCC. Mỗi chứng từ gồm 4 dòng (STT trùng nhau):
| Dòng | Account | Nội dung | Số tiền |
|---|---|---|---|
| 1 | (Customer/KUNNR) | dòng khách hàng | tổng tiền ĐÃ gồm thuế, **số ÂM** |
| 2 | 51131010 | doanh thu lãi | tiền lãi CHƯA thuế, số dương |
| 3 | 51511000 | doanh thu phí | tiền phí CHƯA thuế, số dương |
| 4 | 33311000 | thuế GTGT đầu ra | FWBAS = tổng lãi+phí chưa thuế |

Tham số cố định: Company `6000` · Currency `VND` · Doc type `DR` · Tax code `O3` · Auto tax `X` ·
Contract type `X` · Flow type `AT03` · Contract = số HĐCC · Quantity = số ngày lãi/phí, đơn vị `Day` ·
Ngày định dạng `dd.mm.yyyy` · Baseline date = ngày chứng từ · Header text ≤ 25 ký tự: `"DT lãi, phí HĐCC:"+Contract` ·
Line text: `"Tiền lãi, phí HĐCC số:"+Contract` · Profit Center: phiên từ Plant theo bảng khai báo.
⚠ `[VÊNH]` cột Customer (KUNNR) template ghi **"Mã KH PNJ"** — mâu thuẫn với chốt dùng mã BP SAP (§13.1, câu hỏi số 1).

**TEMPLATE cuối tháng (KT)** — bút toán DỰ THU (TH9): ngày chứng từ/ghi sổ = ngày cuối tháng,
Customer = **"Mã SAP chung"** (mã đại diện), lãi/phí CHƯA thuế, **không có dòng thuế** (dự thu không VAT).
Đầu tháng sau kế toán bút toán đảo (nghiệp vụ bên SAP). GPTS phải chạy được **báo cáo dự thu**:
mọi HĐCC còn dư nợ + số lãi/phí phải-thu-chưa-thu tính đến ngày chạy (mặc định cuối tháng, GĐ2 chạy ngày bất kỳ).

### 10.3 Vietinbank `[CHỐT]`
- Xuất file Excel import Vietinbank (UNC) từ ĐNTT đã duyệt; sau khi tiền đi, kế toán xác nhận "đã chi tiền" + SBT.
- Nếu sau này có luồng đẩy thông tin thanh toán qua SAP: phải theo TỪNG mã KH trên SAP (lưu ý kế toán 12/8).

## 11. Report / truy xuất (template khách gửi 08/09) — `[CHỜ CHỐT]` thuộc GĐ nào

4 report export theo template, tất cả có option **Chi tiết** (mỗi TSCC/mỗi lần 1 dòng) / **Tổng hợp** (mỗi HĐCC/lần gần nhất 1 dòng)
và bộ lọc thời gian (từ ngày–đến ngày / ngày cụ thể):
1. **TEMPLATE KH**: hồ sơ KH + SL HĐCC, dư nợ đến ngày truy xuất, tổng lãi+phí phải thu/đã thu/chưa thu,
   và khối **lịch sử điều chỉnh** (thông tin + user duyệt trước/sau — khách còn phân vân gom 1 dòng hay tách;
   đề xuất của Mona: log tách mỗi lần 1 dòng, report gom khi xuất).
2. **TEMPLATE HĐCC** (~84 cột): toàn bộ vòng đời HĐ — lãi/phí phải thu/đã thu/còn phải thu, tăng-giảm lãi phí,
   hạn mức giải ngân còn lại, chuộc hàng (user đề xuất/duyệt, hình thức trả, chính chủ/ủy quyền, phí BQTS phát sinh thêm),
   tem niêm phong + **mã tem sau khi đổi** (`[CHỜ CHỐT]` nghiệp vụ đổi tem chưa được mô tả), SBT, hình thức thanh toán,
   cột "khung lãi & phí kỳ hạn gần nhất" (`[CHỜ CHỐT]` ý nghĩa).
3. **TEMPLATE TSCC**: chi tiết tài sản theo HĐ.
4. **TEMPLATE GIA HẠN**: dư nợ trước/sau, vay thêm, trả bớt, tái định giá, kỳ mới, SBT, lý do từ chối.
→ Các trường trong report là NGUỒN THAM CHIẾU cho data model: mọi trường xuất hiện ở đây phải lưu được trong DB.

## 12. Phạm vi & timeline (theo Master Planning bản khách đã xem, cập nhật 09/2026)

| GĐ | Nội dung chính | Từ | Đến | Mốc |
|---|---|---|---|---|
| MVP-0 | Kick-off, chốt đặc tả, ERD/API lõi, môi trường dev | 17/08 | 21/08 | M0 |
| MVP-1 | Nền tảng RBAC + tham số + Module KH | 24/08 | 09/09 | |
| MVP-2 | TSCC + định giá 2 phương pháp + kho + niêm phong | 07/09 | 17/09 | |
| MVP-3 | HĐCC cho vay đầy đủ: duyệt 2 bước, upload chứng từ, bộ mẫu in, hạn mức, ưu đãi, diff trả về | 14/09 | 25/09 | |
| MVP-4 | Thu nợ/lãi/phí + chuộc đồ + cutoff 17h + tự động tất toán | 14/09 | 02/10 | |
| MVP-5 | Gia hạn 3 loại + vay thêm + tái định giá | 21/09 | 16/10 | M1 |
| MVP-6 | Sync KH→SAP + export Excel SAP/Vietinbank + báo cáo dự thu | 09/10 | 26/10 | |
| MVP-7 | UAT MVP & nghiệm thu (vòng đời vay–thu–gia hạn–chuộc) | 26/10 | 30/10 | MVP |
| C1 | Thẩm định/định giá nâng cao | 02/11 | 13/11 | |
| C2 | Thu tùy biến (TH5) + hoàn thiện luồng HĐĐT | 09/11 | 27/11 | |
| C3 | Chuộc đồ nâng cao | 23/11 | 04/12 | |
| C4 | Thanh lý (khai báo) + nhắc nợ 3 lần | 30/11 | 11/12 | M2 |
| C5 | Phê duyệt nâng cao, định giá tự động, đối soát CK, in etiket | 14/12 | 25/12 | |
| C6 | Integration test (API Mona↔SAP), UAT tổng, nghiệm thu | 28/12 | 08/01/27 | M3 |

Ngoài phạm vi (chốt kick-off): kết nối bán hàng thanh lý với FI (SAP làm), luồng PNJ → Mona.
Được đẩy lên GĐ1 tại kick-off: upload chứng từ HĐCC, sync KH → SAP, import dữ liệu cũ từ Excel nếu go-live trễ
(1-2 cửa hàng, dữ liệu ít). Họp định kỳ thứ 4 hàng tuần 13h30–14h30.

## 13. ⚠ DANH SÁCH VÊNH & CHƯA CHỐT — AI KHÔNG ĐƯỢC TỰ QUYẾT

### 13.1 Vênh giữa các nguồn (chờ khách phân xử)
1. **KUNNR trong template import SAP** ghi "Mã KH PNJ" ↔ mọi buổi họp chốt tham chiếu bằng **mã BP SAP**
   (và mã PNJ không bắt buộc — KH vãng lai không có). → Quan trọng nhất, chặn module export.
2. **Vượt hạn mức**: kick-off chốt KHÔNG cho vay vượt ↔ phản hồi template v2 có ý cho vượt theo user. → Code theo "không vượt", để flag cấu hình.
3. **Cú pháp chuyển khoản** nhận diện loại gia hạn: kick-off nói dùng ↔ template v2 nói bỏ.
4. **HĐĐT**: MoM 12-13/8 chốt xuất bên SAP ↔ kick-off nhắc Mona check API NCC "MCS". → Mặc định theo chốt SAP; không code tích hợp HĐĐT phía GPTS khi chưa có xác nhận.
5. **Lãi/phí "đã gồm VAT"** trên template report ↔ tham số cấu hình chưa gồm VAT. → Chốt cách trình bày report.

### 13.2 Chưa chốt (code thành cấu hình / TODO)
- Đơn vị lãi suất 1.5 và đơn vị phí 3 bậc (template ghi "VNĐ/ngày" nghi sai).
- Cơ sở quy đổi 360/365 + cách đếm đầu mút ngày + tương tác cutoff với ngày nghỉ/cuối tháng sau 17h.
- Mức sàn 500k hay 1tr; ngưỡng biên độ thu thiếu; hạn thông báo từ chối gia hạn 3 hay 5 ngày; dung lượng video ủy quyền.
- Logic validate CCCD chi tiết (Mona trình buổi sau).
- Cấp CỬA HÀNG dưới chi nhánh (mới xuất hiện trong template report).
- Kim cương rời qua P.TCKT: luồng + giai đoạn.
- Nghiệp vụ đổi tem niêm phong ("mã tem sau khi đổi").
- Danh sách field được sửa sau duyệt + field nào đồng bộ SAP.
- Cột "khung lãi & phí kỳ hạn gần nhất"; lịch sử điều chỉnh KH gom 1 dòng hay tách (đề xuất: tách).
- 4 report template thuộc GĐ1 hay GĐ2 (chưa có trong timeline).
- Nghề nghiệp KH bắt buộc hay không; số chứng từ thu gộp hay tách theo giao dịch.

## 14. Hướng dẫn cho AI khi code từ tài liệu này

1. Mọi tham số tài chính (lãi, phí, bậc, mức sàn, ngưỡng, cutoff, số ngày miễn phí bảo quản, tỷ lệ) → **bảng cấu hình**, không hard-code.
2. Gặp mục `[CHỜ CHỐT]`/`[VÊNH]` → dừng và hỏi, hoặc implement mặc định AN TOÀN nhất (chặn thay vì cho phép) kèm feature flag + comment `// TODO(BA §13.x)`.
3. Mọi hành động duyệt/trả về/hủy/giảm lãi phí/điều chỉnh thông tin → ghi audit log (user, thời điểm, trước/sau) — report §11 phụ thuộc vào log này.
4. Tiền tệ: VND, số nguyên (NUMERIC(15,0)); trọng lượng: chỉ, NUMERIC(10,3); ngày giao dịch tách khỏi ngày ghi nhận (cutoff 17h).
5. UI tham chiếu wireframe repo `gpts-wireframe` — tên màn/luồng trong tài liệu này khớp số file HTML.
