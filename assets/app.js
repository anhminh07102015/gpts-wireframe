// GPTS wireframe — tương tác dùng chung
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
