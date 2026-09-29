// GPTS wireframe — tương tác dùng chung

/* === Auto-build sidebar nav === */
;(function(){
  var nav=document.querySelector('.side nav');
  if(!nav)return;
  var pg=(location.pathname.split('/').pop()||'index.html');
  /* sub-pages → parent highlight */
  var pm={'02-tao-khach-hang.html':'01-danh-sach-khach-hang.html',
    '03-tao-hop-dong.html':'04-danh-sach-hop-dong.html',
    '05-duyet-ho-so.html':'04-danh-sach-hop-dong.html',
    '05b-upload-hdcc.html':'04-danh-sach-hop-dong.html',
    '05c-chuyen-giai-ngan.html':'04-danh-sach-hop-dong.html',
    '06-duyet-giai-ngan.html':'14-giai-ngan.html'};
  var act=pm[pg]||pg;
  var menu=[
    {h:'index.html',t:'Tổng quan'},
    {h:'01-danh-sach-khach-hang.html',t:'Khách hàng'},
    {h:'04-danh-sach-hop-dong.html',t:'Hợp đồng cầm cố'},
    '-',
    {g:'Tạo giao dịch TT',c:[
      {h:'08-thu-no-tat-toan.html',t:'Thu nợ lãi phí'},
      {h:'08b-chuoc-do.html',t:'Chuộc đồ'}
    ]},
    {g:'Tạo giao dịch GH',c:[
      {h:'09-gia-han.html',t:'Gia hạn thường'},
      {h:'09-gia-han.html#tra-bot',t:'Gia hạn trả bớt'},
      {h:'09-gia-han.html#vay-them',t:'Gia hạn vay thêm'}
    ]},
    '-',
    {h:'14-giai-ngan.html',t:'Giải ngân'},
    {h:'07-luong-xuat-hoa-don.html',t:'Xuất hóa đơn'},
    '-',
    {h:'10-report.html',t:'Report / Truy xuất'},
    {h:'12-hop-dong-toi-han.html',t:'HĐ tới hạn / Quá hạn'},
    {h:'11-thanh-ly-nhac-no.html',t:'Thanh lý / Nhắc nợ'},
    '-',
    {h:'13-cau-hinh-admin.html',t:'Cấu hình Admin'}
  ];
  var s='',seen={};
  menu.forEach(function(m){
    if(m==='-'){s+='<div class="nav-sep"></div>';return;}
    if(m.g){
      var go=m.c.some(function(c){return c.h.split('#')[0]===act;});
      s+='<div class="nav-grp'+(go?' open':'')+'"><div class="nav-grp-toggle" onclick="this.parentElement.classList.toggle(\'open\')">'+m.g+'</div><div class="nav-grp-items">';
      m.c.forEach(function(c){
        var base=c.h.split('#')[0];
        var on=base===act&&!seen[base];
        if(on)seen[base]=1;
        s+='<a href="'+c.h+'"'+(on?' class="on"':'')+'>'+c.t+'</a>';
      });
      s+='</div></div>';return;
    }
    s+='<a href="'+m.h+'"'+(m.h===act?' class="on"':'')+'>'+m.t+'</a>';
  });
  nav.innerHTML=s;
})();
function toast(msg){
  let t=document.getElementById('toast');
  if(!t){t=document.createElement('div');t.id='toast';document.body.appendChild(t);}
  t.textContent=msg;t.classList.add('show');
  clearTimeout(t._h);t._h=setTimeout(()=>t.classList.remove('show'),2600);
}
// Dropdown: phần tử .dd chứa [data-dd-toggle] và .dd-menu
document.addEventListener('click',e=>{
  const tg=e.target.closest('[data-dd-toggle]');
  if(tg){const dd=tg.closest('.dd');document.querySelectorAll('.dd.open').forEach(d=>{if(d!==dd)d.classList.remove('open')});dd.classList.toggle('open');return;}
  if(!e.target.closest('.dd-menu'))document.querySelectorAll('.dd.open').forEach(d=>d.classList.remove('open'));
});
// Modal: [data-modal-open="#id"], [data-modal-close]
document.addEventListener('click',e=>{
  const op=e.target.closest('[data-modal-open]');
  if(op){document.querySelector(op.dataset.modalOpen).classList.add('open');return;}
  if(e.target.closest('[data-modal-close]')||e.target.classList.contains('overlay')){
    e.target.closest('.overlay')?.classList.remove('open');
    if(e.target.classList.contains('overlay'))e.target.classList.remove('open');
  }
});
document.addEventListener('keydown',e=>{if(e.key==='Escape')document.querySelectorAll('.overlay.open').forEach(o=>o.classList.remove('open'))});
// Toggle nhánh định giá: radio[name=pp]
document.addEventListener('change',e=>{
  if(e.target.name==='pp'){
    const tt=document.getElementById('br-tt'),hd=document.getElementById('br-hd');
    const isTT=e.target.value==='tt';
    tt.classList.toggle('branch-on',isTT);tt.classList.toggle('branch-off',!isTT);
    hd.classList.toggle('branch-on',!isTT);hd.classList.toggle('branch-off',isTT);
  }
});
