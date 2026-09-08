# -*- coding: utf-8 -*-
import os
OUT = '/home/claude/gpts-wireframe'
NAV = [
    ("index.html", "Tổng quan"),
    ("01-danh-sach-khach-hang.html", "Khách hàng"),
    ("02-tao-khach-hang.html", "· Tạo khách hàng"),
    ("04-danh-sach-hop-dong.html", "Hợp đồng cầm cố"),
    ("03-tao-hop-dong.html", "· Lên hợp đồng"),
    ("05-duyet-ho-so.html", "· Duyệt hồ sơ (B1)"),
    ("06-duyet-giai-ngan.html", "· Duyệt giải ngân (B2)"),
    ("07-luong-xuat-hoa-don.html", "Luồng xuất hóa đơn"),
]

def shell(fname, title, body, extra_js=""):
    nav = "\n".join(
        f'      <a href="{f}"{" class=\"on\"" if f == fname else ""}>{label}</a>'
        for f, label in NAV)
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · GPTS An Tín</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <aside class="side">
    <div class="logo">GPTS<small>Hệ thống cầm đồ An Tín — wireframe</small></div>
    <nav>
{nav}
    </nav>
    <div class="foot">Bản wireframe thao tác · số liệu minh họa</div>
  </aside>
  <main class="main">
{body}
  </main>
<script src="assets/app.js"></script>
{extra_js}
</body>
</html>"""

P = {}

# ============================================================ index
P['index.html'] = ("Tổng quan", """
    <div class="page-head"><div><h1>Wireframe GPTS — An Tín × Mona</h1>
      <div class="desc">Bấm vào từng màn để xem và thao tác thử. Mỗi màn là một file HTML riêng.</div></div></div>
    <div class="toc">
      <a class="card" href="01-danh-sach-khach-hang.html"><div class="num">Màn 01</div><h3>Quản lý danh sách khách hàng</h3><p>Bộ lọc theo nguồn/hạng/trạng thái, bảng KH với mã SAP tham chiếu, badge hạng Gold/Diamond.</p></a>
      <a class="card" href="02-tao-khach-hang.html"><div class="num">Màn 02</div><h3>Tạo tài khoản khách hàng</h3><p>CCCD tách riêng Passport, cảnh báo tuổi (không chặn), upload hình KH + CCCD, hạng KHTT tự sinh.</p></a>
      <a class="card" href="03-tao-hop-dong.html"><div class="num">Màn 03</div><h3>Lên hợp đồng cầm cố</h3><p>Chọn KH qua ô tìm kiếm (dropdown thao tác được), thêm nhiều TSCC qua modal 2 phương pháp định giá, thông tin vay với lãi 1.5 cố định.</p></a>
      <a class="card" href="04-danh-sach-hop-dong.html"><div class="num">Màn 04</div><h3>Danh sách hợp đồng cầm cố</h3><p>Vòng đời trạng thái HĐ + cột đề nghị thanh toán + bước tiếp theo của từng hồ sơ.</p></a>
      <a class="card" href="05-duyet-ho-so.html"><div class="num">Màn 05</div><h3>Duyệt hồ sơ — bước 1</h3><p>Banner diff thông tin đã sửa, panel Duyệt / Trả về / Từ chối (bấm thử được), mở nút in HĐCC sau duyệt.</p></a>
      <a class="card" href="06-duyet-giai-ngan.html"><div class="num">Màn 06</div><h3>Duyệt giải ngân — bước 2 &amp; ĐNTT</h3><p>Kiểm tra thụ hưởng, trả về chỉ mở sửa chi vay, bảng đề nghị thanh toán với export Vietinbank và xác nhận đã chi tiền.</p></a>
      <a class="card" href="07-luong-xuat-hoa-don.html"><div class="num">Màn 07</div><h3>Luồng thu tiền → xuất hóa đơn</h3><p>Pipeline từ thu lãi/phí (cutoff 17h) qua GPTS đến SAP (FI) xuất HĐĐT và đối soát hàng ngày.</p></a>
    </div>
""")

# ============================================================ 01
rows01 = [
    ("KH000123","Nguyễn Thị Hồng","0790xxxxxxxx","0903 xxx 111",'<span class="bg bg-gold">Gold</span>',"PNJ / CAF","BP1000021","2",'<span class="bg bg-green">Đang giao dịch</span>'),
    ("KH000124","Trần Văn Bảo","0480xxxxxxxx","0912 xxx 222",'<span class="bg bg-gray">Chuẩn</span>',"Vãng lai","BP1000022","1",'<span class="bg bg-green">Đang giao dịch</span>'),
    ("KH000125","Lê Minh Châu","P1234xxxx (Passport)","0938 xxx 333",'<span class="bg bg-blue">Diamond</span>',"Ngân hàng","BP1000023","3",'<span class="bg bg-green">Đang giao dịch</span>'),
    ("KH000126","Phạm Quốc Duy","0250xxxxxxxx","0905 xxx 444",'<span class="bg bg-gray">Chuẩn</span>',"Tiệm vàng","—","0",'<span class="bg bg-blue">Mới</span>'),
    ("KH000127","Võ Thúy An","0790xxxxxxxx","0907 xxx 555",'<span class="bg bg-gold">Gold</span>',"NV nội bộ PNJG","BP1000025","1",'<span class="bg bg-green">Đang giao dịch</span>'),
]
trs = "\n".join(
    f'          <tr><td class="link"><a href="02-tao-khach-hang.html">{r[0]}</a></td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td><td>{r[6]}</td><td>{r[7]}</td><td>{r[8]}</td><td>⋯</td></tr>'
    for r in rows01)
P['01-danh-sach-khach-hang.html'] = ("Quản lý khách hàng", f"""
    <div class="page-head">
      <div><h1>Quản lý khách hàng</h1><div class="desc">Danh sách khách hàng cầm cố · mã tham chiếu SAP đồng bộ cuối ngày</div></div>
      <div class="grow"></div>
      <button class="btn btn-line" onclick="toast('Đã xuất danh sách ra Excel (mô phỏng)')">⬇ Xuất Excel</button>
      <a class="btn btn-pri" href="02-tao-khach-hang.html">+ Tạo khách hàng</a>
    </div>
    <div class="stack">
      <div class="card" style="display:flex;gap:10px;flex-wrap:wrap;align-items:center">
        <div class="f" style="flex:2;min-width:240px"><input placeholder="🔍  Tìm theo tên / CCCD / SĐT / mã KH…"></div>
        <div class="f" style="width:170px"><select><option>Nguồn KH</option><option>PNJ / CAF</option><option>Ngân hàng</option><option>Doanh nghiệp / Sỉ</option><option>Tiệm vàng</option><option>NV nội bộ PNJG</option><option>Vãng lai</option></select></div>
        <div class="f" style="width:140px"><select><option>Hạng KH</option><option>Chuẩn</option><option>Gold</option><option>Diamond</option></select></div>
        <div class="f" style="width:150px"><select><option>Trạng thái</option><option>Mới</option><option>Đang giao dịch</option></select></div>
        <div class="f" style="width:150px"><select><option>Chi nhánh</option><option>CN Quận 1</option><option>CN Thủ Đức</option></select></div>
        <button class="btn btn-ghost" onclick="toast('Đã xóa toàn bộ bộ lọc')">Xóa lọc</button>
      </div>
      <div class="tbl-wrap">
        <table class="tbl">
          <thead><tr><th>Mã KH</th><th>Họ tên</th><th>CCCD / Passport</th><th>SĐT</th><th>Hạng</th><th>Nguồn KH</th><th>Mã SAP (BP)</th><th>Số HĐCC</th><th>Trạng thái</th><th></th></tr></thead>
          <tbody>
{trs}
          </tbody>
        </table>
        <div class="tbl-foot"><span>Hiển thị 1–5 / 1.248 khách hàng</span><span class="grow"></span>
          <button class="pg">‹</button><button class="pg on">1</button><button class="pg">2</button><button class="pg">3</button><span>…</span><button class="pg">250</button><button class="pg">›</button></div>
      </div>
    </div>
""")

# ============================================================ 02
P['02-tao-khach-hang.html'] = ("Tạo tài khoản khách hàng", """
    <div class="crumb"><a href="01-danh-sach-khach-hang.html">Khách hàng</a> › Tạo mới</div>
    <div class="page-head"><h1>Tạo tài khoản khách hàng</h1></div>
    <div class="stack">
      <div class="note note-warn" id="ageWarn" hidden>⚠ Khách hàng ngoài độ tuổi 18–70 — vui lòng kiểm tra kỹ trước khi tiếp tục (cảnh báo, không chặn giao dịch)</div>
      <div class="card"><h2>Thông tin cá nhân</h2>
        <div class="grid2">
          <div class="f"><label>Họ và tên <span class="req">*</span></label><input placeholder="Nhập họ tên đầy đủ"></div>
          <div class="f"><label>Ngày sinh <span class="req">*</span></label><input type="date" id="dob"><div class="hint">Cảnh báo nếu dưới 18 hoặc trên 70 tuổi — thử chọn năm 1950 để xem</div></div>
          <div class="f"><label>Giới tính <span class="req">*</span></label><select><option>Chọn</option><option>Nam</option><option>Nữ</option></select></div>
          <div class="f"><label>Nghề nghiệp</label><select><option>Chọn nghề nghiệp</option><option>Kinh doanh tự do</option><option>Nhân viên văn phòng</option><option>Khác</option></select><div class="hint">Đang chờ chốt bắt buộc hay không</div></div>
        </div>
      </div>
      <div class="card"><h2>Giấy tờ tùy thân</h2>
        <div class="grid2">
          <div class="f"><label>Số CCCD <span class="req">*</span></label><input placeholder="Nhập 12 số CCCD" maxlength="12"><div class="hint">Validate cấu trúc số CCCD · duy nhất trên hệ thống</div></div>
          <div class="f"><label>Số Passport / CCCD quân đội</label><input placeholder="Chỉ nhập khi không có CCCD"><div class="hint">Tách trường riêng — quy tắc kiểm tra khác CCCD</div></div>
          <div class="f"><label>Ngày cấp <span class="req">*</span></label><input type="date"></div>
          <div class="f"><label>Nơi cấp <span class="req">*</span></label><input placeholder="Nhập nơi cấp"></div>
        </div>
        <div class="grid3" style="margin-top:14px">
          <div class="upload" onclick="toast('Mở hộp thoại chọn ảnh (mô phỏng)')">⬆ Hình khách hàng<small>JPG, PNG · tối đa 10MB</small></div>
          <div class="upload" onclick="toast('Mở hộp thoại chọn ảnh (mô phỏng)')">⬆ CCCD mặt trước<small>JPG, PNG · tối đa 10MB</small></div>
          <div class="upload" onclick="toast('Mở hộp thoại chọn ảnh (mô phỏng)')">⬆ CCCD mặt sau<small>JPG, PNG · tối đa 10MB</small></div>
        </div>
        <div class="hint" style="margin-top:8px">Hình KH + CCCD lưu tại hồ sơ khách hàng, được cập nhật khi KH cũ đổi giấy tờ</div>
      </div>
      <div class="card"><h2>Thông tin liên hệ</h2>
        <div class="grid2">
          <div class="f"><label>Số điện thoại <span class="req">*</span></label><input placeholder="Nhập SĐT"></div>
          <div class="f"><label>Email</label><input placeholder="Nhập email (không bắt buộc)"></div>
          <div class="f"><label>Địa chỉ thường trú <span class="req">*</span></label><input placeholder="Theo giấy tờ tùy thân"></div>
          <div class="f"><label>Địa chỉ liên hệ <span class="req">*</span></label><input placeholder="Nhập địa chỉ liên hệ"><div class="hint">Bắt buộc (chốt theo phản hồi template v2)</div></div>
        </div>
      </div>
      <div class="card"><h2>Phân loại &amp; mã tham chiếu</h2>
        <div class="grid2">
          <div class="f"><label>Nguồn khách hàng <span class="req">*</span></label><select><option>Chọn nguồn</option><option>PNJ / CAF</option><option>Ngân hàng</option><option>Doanh nghiệp / Sỉ</option><option>Tiệm vàng</option><option>NV nội bộ PNJG</option><option>Vãng lai</option></select></div>
          <div class="f"><label>Mã KH PNJ</label><input placeholder="Nhập nếu có"></div>
          <div class="f"><label>Mã khách hàng (An Tín)</label><input readonly value="Hệ thống tự sinh"></div>
          <div class="f"><label>Hạng KHTT</label><input readonly value="Tự phân hạng theo dư nợ — ưu đãi giảm phí"></div>
          <div class="f"><label>Mã SAP (Business Partner)</label><input readonly value="Nhận từ response API khi đồng bộ SAP"></div>
          <div class="f"><label>Ghi chú</label><input placeholder="Ghi chú thêm về khách hàng"></div>
        </div>
      </div>
      <div style="display:flex;gap:10px;justify-content:flex-end">
        <a class="btn btn-line" href="01-danh-sach-khach-hang.html">Hủy</a>
        <button class="btn btn-pri" onclick="toast('Đã lưu khách hàng (mô phỏng) — mã KH000128')">Lưu khách hàng</button>
      </div>
    </div>
""", """<script>
document.getElementById('dob').addEventListener('change',e=>{
  const y=new Date(e.target.value).getFullYear(),age=new Date().getFullYear()-y;
  document.getElementById('ageWarn').hidden=!(age<18||age>70);
});
</script>""")

# ============================================================ 03
P['03-tao-hop-dong.html'] = ("Lên hợp đồng cầm cố", """
    <div class="crumb"><a href="04-danh-sach-hop-dong.html">Hợp đồng cầm cố</a> › Tạo mới</div>
    <div class="page-head"><h1>Lên hợp đồng cầm cố</h1></div>
    <div class="stack">
      <div class="card"><h2><span class="step-n">1</span> Khách hàng</h2>
        <div style="display:flex;gap:10px">
          <div class="dd" style="flex:1">
            <div class="f"><input data-dd-toggle placeholder="🔍  Tìm khách hàng theo CCCD / SĐT / tên / mã KH… (bấm để mở gợi ý)"></div>
            <div class="dd-menu">
              <button class="dd-item" onclick="pickKH(this)" data-kh="Nguyễn Thị Hồng|KH000123 · CCCD 0790xxxxxx01 · 0903 xxx 111 · Mã SAP BP1000021|Gold · giảm phí bảo quản|Dư nợ hiện tại: 15.000.000 đ (2 HĐCC hiệu lực)">
                <span class="av"></span><span><span class="nm">Nguyễn Thị Hồng <span class="bg bg-gold">Gold</span></span><br><span class="mt">KH000123 · CCCD 0790xxxxxx01 · 0903 xxx 111</span></span><span class="rt">Dư nợ 15.000.000 đ</span></button>
              <button class="dd-item" onclick="pickKH(this)" data-kh="Trần Hồng Phúc|KH000341 · CCCD 0790xxxxxx77 · 0918 xxx 662|Chuẩn|Không có dư nợ">
                <span class="av"></span><span><span class="nm">Trần Hồng Phúc <span class="bg bg-gray">Chuẩn</span></span><br><span class="mt">KH000341 · CCCD 0790xxxxxx77 · 0918 xxx 662</span></span><span class="rt">Không có dư nợ</span></button>
              <button class="dd-item" onclick="pickKH(this)" data-kh="Võ Thúy An|KH000127 · CCCD 0790xxxxxx45 · 0907 xxx 555|Gold · giảm phí bảo quản|Dư nợ hiện tại: 8.000.000 đ (1 HĐCC hiệu lực)">
                <span class="av"></span><span><span class="nm">Võ Thúy An <span class="bg bg-gold">Gold</span></span><br><span class="mt">KH000127 · CCCD 0790xxxxxx45 · 0907 xxx 555</span></span><span class="rt">Dư nợ 8.000.000 đ</span></button>
              <a class="dd-new" href="02-tao-khach-hang.html">+ Không tìm thấy? Tạo khách hàng mới — tạo xong quay lại tự chọn</a>
            </div>
          </div>
          <a class="btn btn-line" href="02-tao-khach-hang.html">+ Tạo KH mới</a>
        </div>
        <div id="khCard" class="note note-info" style="display:none;margin-top:12px">
          <strong id="khName"></strong> <span class="bg bg-gold" id="khHang"></span><br>
          <span id="khMeta" style="font-size:.82rem"></span><br>
          <strong id="khDuno" style="font-size:.84rem"></strong>
          <button class="btn btn-ghost" style="float:right" onclick="document.getElementById('khCard').style.display='none';toast('Chọn lại khách hàng')">Đổi KH</button>
        </div>
      </div>

      <div class="card"><h2><span class="step-n">2</span> Tài sản cầm cố <span style="font-weight:400;color:var(--sub);font-size:.82rem">(1 HĐCC có thể nhiều tài sản)</span></h2>
        <div class="tbl-wrap" style="border-radius:8px">
          <table class="tbl" id="tsccTbl">
            <thead><tr><th>#</th><th>Loại TSCC</th><th>TL vàng / tổng (chỉ)</th><th>Tuổi vàng</th><th>PP định giá</th><th>Trị giá (tự tính)</th><th>Tỷ lệ cầm</th><th>Thợ kỹ thuật</th><th></th></tr></thead>
            <tbody>
              <tr><td>1</td><td>Nữ trang trọng lượng (nhẫn)</td><td>2,500 / 2,850</td><td>75%</td><td>Theo thị trường</td><td>18.750.000 đ</td><td>80%</td><td>Trần Văn Thợ</td><td><button onclick="this.closest('tr').remove();toast('Đã xóa tài sản')">🗑</button></td></tr>
              <tr><td>2</td><td>Kim cương / KCR (bông tai)</td><td>— / 1,200</td><td>—</td><td>Theo hóa đơn</td><td>22.000.000 đ</td><td>75%</td><td>Trần Văn Thợ</td><td><button onclick="this.closest('tr').remove();toast('Đã xóa tài sản')">🗑</button></td></tr>
            </tbody>
          </table>
        </div>
        <div style="display:flex;gap:12px;align-items:center;margin-top:12px">
          <button class="btn btn-line" data-modal-open="#mdTscc" style="color:var(--navy-2);border-color:var(--navy-2)">+ Thêm tài sản</button>
          <span class="hint">Trị giá &amp; tỷ lệ theo từng TSCC · TVV không đổi được tỷ lệ trong công thức định giá</span>
        </div>
        <div class="note note-info" style="margin-top:12px;display:flex;gap:26px">
          <strong>Tổng trị giá TSCC: 40.750.000 đ</strong><strong style="color:var(--navy-2)">Hạn mức cầm (tự tính): 31.900.000 đ</strong>
        </div>
      </div>

      <div class="card"><h2><span class="step-n">3</span> Thông tin vay</h2>
        <div class="grid3">
          <div class="f"><label>Số tiền cầm <span class="req">*</span></label><input id="soTien" value="28.000.000"><div class="hint">≤ hạn mức 31.900.000 đ · không cho vay vượt hạn mức — thử nhập 35.000.000</div></div>
          <div class="f"><label>Kỳ hạn <span class="req">*</span></label><select><option>30 ngày</option></select><div class="hint">GĐ1 chỉ có sản phẩm 30 ngày</div></div>
          <div class="f"><label>Ngày giải ngân <span class="req">*</span></label><input type="date"></div>
          <div class="f"><label>Lãi suất</label><input readonly value="1.5 (cố định, chưa gồm VAT)"></div>
          <div class="f"><label>Phí bảo quản</label><input readonly value="Tự tính theo bậc dư nợ"></div>
          <div class="f"><label>Số ngày lãi tối thiểu</label><input readonly value="15 ngày"></div>
          <div class="f"><label>Chính sách ưu đãi <span class="req">*</span></label><select id="cs"><option value="chuan">Chuẩn (giảm phí theo hạng KH)</option><option value="ud1">Ưu đãi đặc biệt 1</option><option value="ud2">Ưu đãi đặc biệt 2</option></select></div>
          <div class="f"><label>Hình thức chi vay <span class="req">*</span></label><select><option>Chuyển khoản</option><option disabled>Tiền mặt (tắt tính năng)</option></select></div>
          <div class="f"><label>Tài khoản thụ hưởng <span class="req">*</span></label><input placeholder="Số TK · Ngân hàng · Chủ TK"></div>
        </div>
        <div class="note note-warn" id="udWarn" hidden style="margin-top:12px">⚠ Mức phí ưu đãi đang LỚN HƠN mức phí theo chính sách chuẩn của khách hàng này — vui lòng kiểm tra lại</div>
        <div class="note note-warn" id="hmWarn" hidden style="margin-top:12px">⚠ Số tiền cầm vượt hạn mức 31.900.000 đ — không thể gửi duyệt</div>
        <div class="note note-info" style="margin-top:12px;display:flex;gap:22px;flex-wrap:wrap">
          <span><strong>Lãi dự kiến (30 ngày):</strong> 345.205 đ</span>
          <span><strong>Phí bảo quản dự kiến:</strong> 172.200 đ</span>
          <span><strong>VAT 10% trên lãi + phí:</strong> 51.740 đ</span>
          <span style="color:var(--navy-2)"><strong>Tổng nghĩa vụ khi tất toán: 28.569.145 đ</strong></span>
        </div>
      </div>

      <div class="card"><h2><span class="step-n">4</span> Hình ảnh / chứng từ đính kèm <span style="font-weight:400;color:var(--sub);font-size:.82rem">(yêu cầu GĐ1)</span></h2>
        <div class="grid3">
          <div class="upload" onclick="toast('Chọn nhiều ảnh tài sản (mô phỏng)')">⬆ Hình tài sản<small>Nhiều ảnh</small></div>
          <div class="upload" onclick="toast('Chọn ảnh giấy kiểm định (mô phỏng)')">⬆ Giấy kiểm định 2 mặt<small>Nếu có</small></div>
          <div class="upload" onclick="toast('Chọn tệp chứng từ (mô phỏng)')">⬆ Chứng từ khác<small>Tờ trình, giải trình ưu đãi…</small></div>
        </div>
      </div>

      <div style="display:flex;gap:10px;align-items:center">
        <span class="hint">Sau khi gửi: duyệt hồ sơ (bước 1) → in HĐCC + bảng lãi phí → duyệt giải ngân (bước 2) → kế toán duyệt đề nghị thanh toán</span>
        <span style="flex:1"></span>
        <button class="btn btn-line" onclick="toast('Đã lưu nháp hợp đồng')">Lưu nháp</button>
        <a class="btn btn-pri" href="05-duyet-ho-so.html" onclick="toast('Đã gửi duyệt — chuyển sang màn duyệt hồ sơ')">Gửi duyệt hồ sơ</a>
      </div>
    </div>

    <!-- Modal thêm TSCC -->
    <div class="overlay" id="mdTscc">
      <div class="modal">
        <div class="m-head"><h3>Thêm tài sản cầm cố</h3><button data-modal-close>✕</button></div>
        <div class="grid3">
          <div class="f"><label>Loại TSCC <span class="req">*</span></label><select><option>Nữ trang trọng lượng</option><option>TSCN Ý</option><option>Đá màu</option><option>Kim cương / KCR</option><option>Ngọc trai</option><option>Style by PNJ</option><option>Nguyên liệu</option><option>ECZ / CZ</option><option>KGĐ - dây</option><option>Vỏ</option></select></div>
          <div class="f"><label>Nguồn gốc / thương hiệu <span class="req">*</span></label><select><option>PNJ</option><option>CAO</option><option>Thương hiệu B</option><option>Khác</option></select></div>
          <div class="f"><label>Quyền sở hữu <span class="req">*</span></label><select><option>Chính chủ</option><option>Không chính chủ</option></select></div>
          <div class="f"><label>Trọng lượng vàng (đá) — chỉ <span class="req">*</span></label><input value="2,500"></div>
          <div class="f"><label>Trọng lượng tổng — chỉ <span class="req">*</span></label><input value="2,850"></div>
          <div class="f"><label>Tuổi vàng (%) <span class="req">*</span></label><select><option>75</option><option>41,6</option><option>58,5</option><option>61</option><option>68</option><option>90</option><option>95</option><option>99</option><option>99,9</option><option>99,99</option><option>Khác (nhập tay)</option></select></div>
        </div>
        <div class="f" style="margin-top:12px"><label>Phương pháp xác định trị giá cầm <span class="req">*</span></label>
          <div class="radio-row">
            <label><input type="radio" name="pp" value="tt" checked> Theo thị trường</label>
            <label><input type="radio" name="pp" value="hd"> Theo hóa đơn</label>
          </div>
        </div>
        <div class="branch branch-on" id="br-tt">
          <div class="hint" style="margin-bottom:8px">Định giá theo thị trường</div>
          <div class="grid3">
            <div class="f"><label>Giá bóng (theo thời kỳ)</label><input readonly value="7.500.000 đ/lượng"></div>
            <div class="f"><label>Công thức</label><input readonly value="TL vàng × tuổi vàng × giá bóng"></div>
            <div class="f"><label>Trị giá TSCC (tự tính)</label><input readonly value="18.750.000 đ"></div>
            <div class="f"><label>Tỷ lệ thu lại (đề xuất theo loại)</label><input value="80%"><div class="hint">TVV được điều chỉnh</div></div>
            <div class="f"><label>Tỷ lệ cầm (theo thương hiệu)</label><input readonly value="80% — khóa"></div>
            <div class="f"><label>Hạn mức tài sản (tự tính)</label><input readonly value="15.000.000 đ"></div>
          </div>
        </div>
        <div class="branch branch-off" id="br-hd">
          <div class="hint" style="margin-bottom:8px">Định giá theo hóa đơn — chọn radio "Theo hóa đơn" để mở</div>
          <div class="grid3">
            <div class="f"><label>Số hóa đơn (PNJ/CAO/DOJI/SJC…)</label><input placeholder="Bắt buộc nếu cầm theo hóa đơn"></div>
            <div class="f"><label>Trị giá theo hóa đơn</label><input placeholder="Nhập trị giá"></div>
            <div class="f"><label>Giá trị giảm trừ + lý do</label><input placeholder="Nhập nếu có"></div>
          </div>
          <div class="hint" style="margin-top:8px">Trị giá TSCC = (Trị giá hóa đơn − Giảm trừ) × Tỷ lệ thu lại</div>
        </div>
        <div class="grid3" style="margin-top:12px">
          <div class="f"><label>Số hộp/túi niêm phong / 1 HĐCC</label><input value="1"></div>
          <div class="f"><label>Trọng lượng hộp/túi niêm phong</label><input placeholder="Nhập trọng lượng"></div>
          <div class="f dd"><label>Tên thợ kỹ thuật <span class="req">*</span></label>
            <input data-dd-toggle readonly value="Trần Văn Thợ (CN Quận 1)" style="cursor:pointer">
            <div class="dd-menu" style="min-width:330px">
              <div class="dd-head"><span class="bg bg-blue">CN Quận 1 ✓</span><span style="flex:1"></span>
                <label style="display:flex;gap:6px;align-items:center;cursor:pointer"><input type="checkbox" id="allCN"> Hiện thợ tất cả chi nhánh</label></div>
              <button class="dd-item"><span class="av"></span><span><span class="nm">Trần Văn Thợ · NV0231</span><br><span class="mt">CN Quận 1 · tho.tv@antin.vn</span></span></button>
              <button class="dd-item"><span class="av"></span><span><span class="nm">Ngô Thị Kim · NV0245</span><br><span class="mt">CN Quận 1 · kim.nt@antin.vn</span></span></button>
              <button class="dd-item dim cnKhac" hidden><span class="av"></span><span><span class="nm">Lê Hoàng Nam · NV0312</span><br><span class="mt">CN Thủ Đức · nam.lh@antin.vn</span></span></button>
            </div>
          </div>
        </div>
        <div class="grid2" style="margin-top:12px">
          <div class="upload" onclick="toast('Chọn ảnh tài sản (mô phỏng)')">⬆ Hình tài sản (nhiều ảnh)</div>
          <div class="upload" onclick="toast('Chọn ảnh giấy kiểm định (mô phỏng)')">⬆ Giấy kiểm định 2 mặt</div>
        </div>
        <div style="display:flex;gap:10px;justify-content:flex-end;margin-top:16px">
          <button class="btn btn-line" data-modal-close>Hủy</button>
          <button class="btn btn-pri" onclick="addTscc()">Thêm tài sản</button>
        </div>
      </div>
    </div>
""", """<script>
function pickKH(btn){
  const [nm,meta,hang,duno]=btn.dataset.kh.split('|');
  document.getElementById('khName').textContent=nm;
  document.getElementById('khHang').textContent=hang;
  document.getElementById('khMeta').textContent=meta;
  document.getElementById('khDuno').textContent=duno;
  document.getElementById('khCard').style.display='block';
  btn.closest('.dd').classList.remove('open');
  toast('Đã chọn khách hàng: '+nm);
}
function addTscc(){
  const tb=document.querySelector('#tsccTbl tbody');
  const n=tb.rows.length+1;
  const tr=tb.insertRow();
  tr.innerHTML=`<td>${n}</td><td>Nữ trang trọng lượng</td><td>2,500 / 2,850</td><td>75%</td><td>Theo thị trường</td><td>18.750.000 đ</td><td>80%</td><td>Trần Văn Thợ</td><td><button onclick="this.closest('tr').remove();toast('Đã xóa tài sản')">🗑</button></td>`;
  document.getElementById('mdTscc').classList.remove('open');
  toast('Đã thêm tài sản vào hợp đồng');
}
document.getElementById('allCN')?.addEventListener('change',e=>{
  document.querySelectorAll('.cnKhac').forEach(x=>x.hidden=!e.target.checked);
});
document.getElementById('soTien').addEventListener('input',e=>{
  const v=parseInt(e.target.value.replace(/\\D/g,''))||0;
  document.getElementById('hmWarn').hidden=v<=31900000;
});
document.getElementById('cs').addEventListener('change',e=>{
  document.getElementById('udWarn').hidden=e.target.value==='chuan';
});
</script>""")

# ============================================================ 04
rows04 = [
    ("HD002211","Nguyễn Thị Hồng","28.000.000","—","—",'<span class="bg bg-warn">Chờ duyệt hồ sơ</span>','<span class="bg bg-gray">—</span>',"BP.TĐVPD duyệt (bước 1)","05-duyet-ho-so.html"),
    ("HD002208","Trần Văn Bảo","12.000.000","—","—",'<span class="bg bg-blue">Chờ duyệt giải ngân</span>','<span class="bg bg-warn">Chờ duyệt GN</span>',"Duyệt giải ngân (bước 2)","06-duyet-giai-ngan.html"),
    ("HD002205","Lê Minh Châu","45.000.000","22/08","21/09",'<span class="bg bg-blue">Đã duyệt giải ngân</span>','<span class="bg bg-blue">Đã duyệt GN</span>',"KT export Vietinbank + chi tiền","06-duyet-giai-ngan.html"),
    ("HD002199","Võ Thúy An","8.000.000","20/08","19/09",'<span class="bg bg-green">Đang hiệu lực</span>','<span class="bg bg-green">Đã chi tiền</span>',"Theo dõi thu lãi/phí","07-luong-xuat-hoa-don.html"),
    ("HD002150","Phạm Quốc Duy","15.000.000","10/07","09/08",'<span class="bg bg-red">Quá hạn</span>','<span class="bg bg-green">Đã chi tiền</span>',"Nhắc nợ lần 2/3","#"),
    ("HD002101","Đỗ Thu Trang","20.000.000","05/07","04/08",'<span class="bg bg-gray">Đã tất toán</span>','<span class="bg bg-green">Đã chi tiền</span>',"Đã đẩy SAP · HĐĐT đã xuất","07-luong-xuat-hoa-don.html"),
    ("HD002210","Ngô Văn Hùng","6.000.000","—","—",'<span class="bg bg-red">Bị trả về</span>','<span class="bg bg-gray">—</span>',"TVV sửa theo lý do trả về","03-tao-hop-dong.html"),
]
trs04 = "\n".join(
    f'          <tr><td class="link"><a href="05-duyet-ho-so.html">{r[0]}</a></td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td><td>{r[6]}</td><td><a class="link" href="{r[8]}">{r[7]}</a></td><td>⋯</td></tr>'
    for r in rows04)
P['04-danh-sach-hop-dong.html'] = ("Hợp đồng cầm cố", f"""
    <div class="page-head">
      <div><h1>Hợp đồng cầm cố</h1><div class="desc">Theo dõi trạng thái hợp đồng và tiến trình duyệt 2 bước — bấm cột "Bước tiếp theo" để nhảy tới màn xử lý</div></div>
      <div class="grow"></div>
      <a class="btn btn-pri" href="03-tao-hop-dong.html">+ Lên hợp đồng</a>
    </div>
    <div class="stack">
      <div class="card" style="display:flex;gap:10px;flex-wrap:wrap;align-items:center">
        <div class="f" style="flex:2;min-width:220px"><input placeholder="🔍  Mã HĐ / tên KH / CCCD…"></div>
        <div class="f" style="width:180px"><select><option>Trạng thái HĐ</option><option>Nháp</option><option>Chờ duyệt hồ sơ</option><option>Chờ duyệt giải ngân</option><option>Đang hiệu lực</option><option>Quá hạn</option><option>Đã tất toán</option><option>Bị trả về</option></select></div>
        <div class="f" style="width:190px"><select><option>Đề nghị thanh toán</option><option>Chờ duyệt GN</option><option>Đã duyệt GN</option><option>Đã chi tiền</option></select></div>
        <div class="f" style="width:150px"><select><option>Chi nhánh</option></select></div>
        <div class="f" style="width:170px"><input type="date"></div>
      </div>
      <div class="tbl-wrap">
        <table class="tbl">
          <thead><tr><th>Mã HĐCC</th><th>Khách hàng</th><th>Số tiền cầm</th><th>Giải ngân</th><th>Đến hạn</th><th>Trạng thái HĐ</th><th>Đề nghị thanh toán</th><th>Bước tiếp theo</th><th></th></tr></thead>
          <tbody>
{trs04}
          </tbody>
        </table>
      </div>
      <div class="hint">Vòng đời: Nháp → Chờ duyệt hồ sơ → Chờ duyệt giải ngân → Đã duyệt GN → Đang hiệu lực → Quá hạn / Đã tất toán · "Bị trả về" quay lại TVV sửa theo lý do</div>
    </div>
""")

# ============================================================ 05
P['05-duyet-ho-so.html'] = ("Duyệt hồ sơ (bước 1)", """
    <div class="crumb"><a href="04-danh-sach-hop-dong.html">Hợp đồng cầm cố</a> › HD002211 › Duyệt hồ sơ</div>
    <div class="page-head"><h1>Duyệt hồ sơ HD002211 (bước 1)</h1><span class="bg bg-warn" id="hsStatus">Chờ duyệt hồ sơ</span></div>
    <div class="split">
      <div class="stack">
        <div class="note note-info">
          <strong>ℹ Hồ sơ được gửi lại sau khi trả về — 3 thông tin đã thay đổi:</strong><br>
          • Số tiền cầm: 30.000.000 → <strong>28.000.000</strong> &nbsp; • Tỷ lệ thu lại TSCC #1: 85% → <strong>80%</strong> &nbsp; • Bổ sung hình tài sản (2 ảnh)<br>
          <span style="font-size:.78rem">Người duyệt chỉ cần rà các mục thay đổi, không phải xem lại toàn bộ hồ sơ</span>
        </div>
        <div class="card"><h2>Khách hàng</h2>
          <table class="tbl"><tbody>
            <tr><td style="color:var(--sub);width:180px">Họ tên / Hạng</td><td>Nguyễn Thị Hồng · <span class="bg bg-gold">Gold (giảm phí)</span></td></tr>
            <tr><td style="color:var(--sub)">CCCD / SĐT</td><td>0790xxxxxxxx · 0903 xxx 111</td></tr>
            <tr><td style="color:var(--sub)">Dư nợ hiện tại</td><td>15.000.000 đ (2 HĐCC hiệu lực)</td></tr>
          </tbody></table>
        </div>
        <div class="card"><h2>Tài sản cầm cố (2)</h2>
          <table class="tbl"><tbody>
            <tr><td style="color:var(--sub);width:180px">TSCC #1</td><td>Nữ trang trọng lượng · 2,5 chỉ · 75% · thị trường · 18.750.000 đ</td></tr>
            <tr><td style="color:var(--sub)">TSCC #2</td><td>Kim cương/KCR · theo hóa đơn PNJ · 22.000.000 đ</td></tr>
            <tr><td style="color:var(--sub)">Tổng trị giá / hạn mức</td><td><strong>40.750.000 đ / 31.900.000 đ</strong></td></tr>
          </tbody></table>
        </div>
        <div class="card"><h2>Thông tin vay</h2>
          <table class="tbl"><tbody>
            <tr><td style="color:var(--sub);width:180px">Số tiền cầm</td><td>28.000.000 đ (trong hạn mức)</td></tr>
            <tr><td style="color:var(--sub)">Kỳ hạn / lãi / phí</td><td>30 ngày · lãi 1.5 · phí bậc &lt;50tr</td></tr>
            <tr><td style="color:var(--sub)">Chính sách ưu đãi</td><td>Chuẩn — giảm phí theo hạng Gold</td></tr>
            <tr><td style="color:var(--sub)">Chi vay</td><td>Chuyển khoản · VCB 0071xxxx · Nguyễn Thị Hồng</td></tr>
            <tr><td style="color:var(--sub)">Chứng từ đính kèm</td><td>6 hình tài sản · 1 giấy kiểm định · 1 tờ trình</td></tr>
          </tbody></table>
        </div>
      </div>
      <div class="stack">
        <div class="card"><h2>Tiến trình hồ sơ</h2>
          <div class="steps">
            <div class="st done"><span class="ic">✓</span><span class="t">Tạo hồ sơ (TVV)<small>23/08 · 14:32</small></span></div>
            <div class="st now" id="st2"><span class="ic">●</span><span class="t">Duyệt hồ sơ — BP.TĐVPD<small>Đang chờ</small></span></div>
            <div class="st todo" id="st3"><span class="ic">○</span><span class="t">In HĐCC + bảng lãi phí<small>Sau duyệt bước 1</small></span></div>
            <div class="st todo"><span class="ic">○</span><span class="t">Duyệt giải ngân (bước 2)</span></div>
            <div class="st todo"><span class="ic">○</span><span class="t">Kế toán duyệt đề nghị TT</span></div>
            <div class="st todo"><span class="ic">○</span><span class="t">Chi tiền (Vietinbank)</span></div>
          </div>
        </div>
        <div class="card"><h2>Xử lý hồ sơ</h2>
          <div class="stack" style="gap:9px">
            <button class="btn btn-ok" style="justify-content:center" onclick="approve()">✓ Duyệt hồ sơ</button>
            <button class="btn btn-warn" style="justify-content:center" onclick="reject('Đã trả về — TVV được sửa mọi field, khi gửi lại sẽ hiện diff')">↩ Đề nghị chỉnh sửa (trả về)</button>
            <button class="btn btn-danger" style="justify-content:center" onclick="reject('Đã từ chối hồ sơ')">✕ Từ chối</button>
          </div>
          <div class="f" style="margin-top:12px"><label>Lý do trả về / từ chối <span class="req">*</span> (ghi rõ thông tin cần sửa)</label>
            <textarea id="reason" rows="3" placeholder="VD: sai số tài khoản thụ hưởng, bổ sung hình mặt sau tài sản…"></textarea>
            <div class="hint">Trả về: không giới hạn field TVV được sửa · sau sửa hiện diff cho người duyệt</div>
          </div>
        </div>
        <div class="note note-warn" id="printNote" hidden>🖨 Đã duyệt bước 1 — nút <a href="06-duyet-giai-ngan.html" style="text-decoration:underline"><strong>In HĐCC + bảng lãi phí</strong></a> đã mở. KH ký xong, TVV upload bản scan rồi chuyển duyệt giải ngân →</div>
      </div>
    </div>
""", """<script>
function approve(){
  const s=document.getElementById('hsStatus');
  s.textContent='Đã duyệt hồ sơ';s.className='bg bg-green';
  const st2=document.getElementById('st2');st2.className='st done';st2.querySelector('.ic').textContent='✓';st2.querySelector('small').textContent='Vừa xong';
  const st3=document.getElementById('st3');st3.className='st now';st3.querySelector('.ic').textContent='●';
  document.getElementById('printNote').hidden=false;
  toast('Đã duyệt hồ sơ — mở bước in chứng từ');
}
function reject(msg){
  const r=document.getElementById('reason');
  if(!r.value.trim()){toast('Bắt buộc nhập lý do trước khi trả về / từ chối');r.focus();return;}
  const s=document.getElementById('hsStatus');
  s.textContent='Bị trả về';s.className='bg bg-red';
  toast(msg);
}
</script>""")

# ============================================================ 06
P['06-duyet-giai-ngan.html'] = ("Duyệt giải ngân & ĐNTT", """
    <div class="crumb"><a href="04-danh-sach-hop-dong.html">Hợp đồng cầm cố</a> › HD002208 › Giải ngân</div>
    <div class="page-head"><h1>Duyệt giải ngân (bước 2) &amp; Đề nghị thanh toán</h1></div>
    <div class="stack">
      <div class="split">
        <div class="stack">
          <div class="card"><h2>Kiểm tra thông tin chi vay</h2>
            <table class="tbl"><tbody>
              <tr><td style="color:var(--sub);width:190px">Hợp đồng</td><td>HD002208 · Trần Văn Bảo · 12.000.000 đ · 30 ngày</td></tr>
              <tr><td style="color:var(--sub)">HĐCC đã ký</td><td>✔ Bản scan đã upload (in sau duyệt bước 1)</td></tr>
              <tr><td style="color:var(--sub)">Hình thức chi</td><td>Chuyển khoản</td></tr>
              <tr><td style="color:var(--sub)">TK thụ hưởng</td><td>0071 000 xxx 456 · Vietcombank · TRAN VAN BAO</td></tr>
              <tr><td style="color:var(--sub)">Đối chiếu chính chủ</td><td>✔ Tên TK trùng tên KH trên CCCD</td></tr>
            </tbody></table>
          </div>
          <div class="note note-warn">↩ Trả về do <strong>sai thông tin thụ hưởng</strong>: hồ sơ quay lại TVV nhưng <strong>chỉ mở sửa thông tin chi vay</strong> — các thông tin khác giữ khóa</div>
        </div>
        <div class="card"><h2>Xử lý</h2>
          <div class="stack" style="gap:9px">
            <button class="btn btn-ok" style="justify-content:center" onclick="approveGN()">✓ Duyệt giải ngân</button>
            <button class="btn btn-warn" style="justify-content:center" onclick="toast('Đã trả về — TVV chỉ được sửa thông tin chi vay')">↩ Trả về sửa thông tin chi vay</button>
          </div>
          <div class="hint" style="margin-top:10px">Duyệt xong → tạo đề nghị thanh toán, chuyển kế toán</div>
        </div>
      </div>
      <div class="tbl-wrap">
        <div style="padding:16px 18px 0;font-weight:600">Đề nghị thanh toán — kế toán xử lý</div>
        <table class="tbl" id="dntt">
          <thead><tr><th>Mã ĐNTT</th><th>HĐCC</th><th>Thụ hưởng</th><th>Số tiền</th><th>Trạng thái</th><th>Thao tác</th></tr></thead>
          <tbody>
            <tr id="dn812"><td>DN00812</td><td>HD002208</td><td>VCB · TRAN VAN BAO</td><td>12.000.000</td>
              <td><span class="bg bg-warn">Chờ duyệt GN</span></td><td>—</td></tr>
            <tr><td>DN00810</td><td>HD002205</td><td>ACB · LE MINH CHAU</td><td>45.000.000</td>
              <td><span class="bg bg-blue">Đã duyệt GN</span></td>
              <td><button class="btn btn-line" style="padding:5px 10px;font-size:.78rem" onclick="exportVTB(this)">⬇ Xuất Excel Vietinbank</button></td></tr>
            <tr><td>DN00807</td><td>HD002199</td><td>VTB · VO THUY AN</td><td>8.000.000</td>
              <td><span class="bg bg-green">Đã chi tiền</span></td><td style="font-size:.78rem;color:var(--sub)">SBT: UNC-0921 · 20/08 16:05</td></tr>
          </tbody>
        </table>
        <div class="tbl-foot">Kế toán duyệt → xuất Excel import Vietinbank (UNC) → tiền đi → Xác nhận đã chi tiền (kèm SBT) → HĐ chuyển "Đang hiệu lực"</div>
      </div>
    </div>
""", """<script>
function approveGN(){
  const tr=document.getElementById('dn812');
  tr.cells[4].innerHTML='<span class="bg bg-blue">Đã duyệt GN</span>';
  tr.cells[5].innerHTML='<button class="btn btn-line" style="padding:5px 10px;font-size:.78rem" onclick="exportVTB(this)">⬇ Xuất Excel Vietinbank</button>';
  toast('Đã duyệt giải ngân — tạo đề nghị thanh toán DN00812');
}
function exportVTB(btn){
  const tr=btn.closest('tr');
  tr.cells[5].innerHTML='<button class="btn btn-ok" style="padding:5px 10px;font-size:.78rem" onclick="confirmPaid(this)">✓ Xác nhận đã chi tiền</button>';
  toast('Đã xuất file Excel import Vietinbank (UNC) — mô phỏng');
}
function confirmPaid(btn){
  const tr=btn.closest('tr');
  tr.cells[4].innerHTML='<span class="bg bg-green">Đã chi tiền</span>';
  tr.cells[5].innerHTML='<span style="font-size:.78rem;color:var(--sub)">SBT: UNC-'+(900+Math.floor(Math.random()*99))+' · hôm nay</span>';
  toast('Đã xác nhận chi tiền — HĐ chuyển "Đang hiệu lực"');
}
</script>""")

# ============================================================ 07
P['07-luong-xuat-hoa-don.html'] = ("Luồng thu tiền → xuất hóa đơn", """
    <div class="page-head"><div><h1>Luồng thu tiền → xuất hóa đơn điện tử</h1>
      <div class="desc">Hóa đơn lãi/phí xuất từ phía SAP — GPTS chỉ đẩy dữ liệu giao dịch đúng ngày (chốt họp 13/08)</div></div></div>
    <div class="stack">
      <div class="pipe">
        <div class="node gpts"><h3>1 · Thu lãi + phí</h3><p>Tất toán / gia hạn / thu định kỳ (GĐ2). Tiền vào TKTG trước 17h tính ngày hôm đó, sau 17h tính ngày hôm sau. TVV đối chiếu sổ phụ, xác nhận thủ công.</p></div>
        <div class="arr">→</div>
        <div class="node gpts"><h3>2 · GPTS ghi nhận</h3><p>Tách nợ / lãi / phí (ưu tiên phí → lãi → nợ), ghi nhận giảm lãi/phí theo phê duyệt, tính VAT 10% trên lãi + phí.</p></div>
        <div class="arr">→</div>
        <div class="node gpts"><h3>3 · Đẩy dữ liệu cuối ngày</h3><p>GĐ1: xuất file Excel theo template SAP cung cấp. GĐ2: API tự động. Giao dịch ngày nào nằm trong dữ liệu ngày đó.</p></div>
        <div class="arr">→</div>
        <div class="node sap"><h3>4 · SAP (FI) hạch toán</h3><p>Giảm công nợ phải thu theo mã KH (BP), ghi nhận doanh thu lãi vào TK lãi, phí vào TK phí.</p></div>
        <div class="arr">→</div>
        <div class="node sap"><h3>5 · SAP xuất HĐĐT</h3><p>Hóa đơn điện tử cho khoản lãi + phí thực thu (VAT 10%), theo ngày ghi nhận — không theo giờ tiền thực vào.</p></div>
        <div class="arr">→</div>
        <div class="node"><h3>6 · Đối soát hàng ngày</h3><p>Đối chiếu GPTS ↔ FI: tổng thu nợ / lãi / phí / giảm trừ theo ngày. Lệch số → điều chỉnh trước khi chốt sổ.</p></div>
      </div>
      <div class="legend"><span><i style="background:var(--navy-2)"></i>Bên GPTS (Mona)</span><span><i style="background:var(--gold)"></i>Bên SAP (An Tín)</span><span><i style="background:#c8d2dc"></i>Hai bên phối hợp</span></div>
      <div class="card"><h2>Dữ liệu GPTS đẩy sang FI mỗi giao dịch thu</h2>
        <div class="tbl-wrap" style="border:none">
        <table class="tbl">
          <thead><tr><th>Trường</th><th>Ví dụ</th><th>Ghi chú</th></tr></thead>
          <tbody>
            <tr><td>Mã KH (GPTS + mã SAP/BP)</td><td>KH000123 · BP1000021</td><td>Tham chiếu 2 chiều</td></tr>
            <tr><td>Mã HĐCC / mã giao dịch thu</td><td>HD002199 · GD-2026-08812</td><td>Số chứng từ thu — chờ chốt gộp hay tách</td></tr>
            <tr><td>Ngày ghi nhận</td><td>25/08/2026</td><td>Theo quy tắc cutoff 17h</td></tr>
            <tr><td>Số tiền thu nợ / lãi / phí</td><td>28.000.000 / 345.205 / 172.200</td><td>Đã tách 3 khoản</td></tr>
            <tr><td>Giảm lãi / giảm phí (nếu có)</td><td>0 / 15.000</td><td>Kèm phê duyệt đúng thẩm quyền</td></tr>
            <tr><td>VAT</td><td>51.740 (10% trên lãi + phí)</td><td>Căn cứ xuất HĐĐT</td></tr>
            <tr><td>Hình thức thanh toán · SBT</td><td>Chuyển khoản · BP cấp số</td><td>Tiền mặt: số chứng từ TM</td></tr>
          </tbody>
        </table>
        </div>
      </div>
      <div class="note note-info">Báo cáo dự thu cuối tháng: lãi + phí phải thu nhưng chưa thu của mọi HĐ còn dư nợ tính đến ngày cuối tháng — kế toán hạch toán bút toán tổng theo mã đại diện, đầu tháng sau bút toán đảo. GĐ2 chạy được ngày bất kỳ.</div>
    </div>
""")

for fname, (title, body, *rest) in P.items():
    html = shell(fname, title, body, rest[0] if rest else "")
    with open(os.path.join(OUT, fname), 'w', encoding='utf-8') as f:
        f.write(html)
    print("written", fname)
