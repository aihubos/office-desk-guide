(function(){
var els=document.querySelectorAll('.reveal');
if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('in')});}
else{var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}})},{threshold:.06,rootMargin:'0px 0px -30px 0px'});els.forEach(function(e){io.observe(e)});}
document.querySelectorAll('.grid').forEach(function(g){Array.prototype.forEach.call(g.children,function(c,i){c.style.transitionDelay=(i*60)+'ms'})});
var links=[].slice.call(document.querySelectorAll('.navin a'));
var secs=links.map(function(a){return document.querySelector(a.getAttribute('href'))});
function onScroll(){var y=window.scrollY+120,cur=-1;secs.forEach(function(s,i){if(s&&s.offsetTop<=y)cur=i});links.forEach(function(a,i){a.classList.toggle('on',i===cur)});
 if(cur>=0){var a=links[cur],n=a.parentNode;if(n.scrollTo)n.scrollTo({left:a.offsetLeft-n.clientWidth/2+a.clientWidth/2,behavior:'smooth'});}}
var t;window.addEventListener('scroll',function(){clearTimeout(t);t=setTimeout(onScroll,60)},{passive:true});onScroll();
})();

/* 비용 계산기: 가격은 각 상품 카드의 확인값(2026.11.01 KST). 의자·설치·배송 제외 */
(function(){
var D=window.DATA;if(!D)return;
var $=function(i){return document.getElementById(i)};
function won(n){return n.toLocaleString('ko-KR')+'원'}
function fill(sel,arr,lab,def){arr.forEach(function(x,i){var o=document.createElement('option');o.value=i;o.textContent=lab(x);if(x.id===def)o.selected=true;sel.appendChild(o)})}
fill($('cT'),D.tables,function(x){return x.brand+' '+x.name+' · '+(x.price?x.pl:'가격 미확인')},'gaia');
fill($('cD'),D.desks,function(x){return x.brand+' '+x.name+' ('+x.motor+') · '+won(x.price)},'d_prem');
fill($('cV'),D.tvs,function(x){return x.brand+' '+x.name+' · '+won(x.price)},'tv65w');
fill($('cSt'),D.stands,function(x){return x.name+(x.price?' · '+won(x.price):'')},'s_fs64');
function run(){
 var t=D.tables[+$('cT').value],d=D.desks[+$('cD').value],v=D.tvs[+$('cV').value],s=D.stands[+$('cSt').value],seats=+$('cSeats').value;
 var n=Math.ceil(seats/t.seats),warn=[],tt=0;
 if(t.price==null){warn.push(t.name+'은(는) 가격 미공개(견적)라 테이블 비용이 0원으로 계산돼요.')}else tt=n*t.price;
 var total=tt+d.price+v.price+s.price;
 $('cTotal').textContent=won(total);
 $('cList').innerHTML='<li><span>테이블 '+n+'개 ('+(n*t.seats)+'석)</span><span>'+(t.price==null?'견적 필요':won(tt))+'</span></li><li><span>모션데스크 1대</span><span>'+won(d.price)+'</span></li><li><span>TV</span><span>'+won(v.price)+'</span></li><li><span>스탠드/벽걸이</span><span>'+won(s.price)+'</span></li>';
 if(t.seats===2)warn.push('2인용 테이블이라 '+seats+'석에 '+n+'개가 필요해요.');
 if(t.id==='clecs')warn.push('리바트 가격은 "791,000원~" 최저 표시가예요.');
 if(/55형/.test(v.name)&&seats>12)warn.push('55형은 13명 이상이면 뒷자리 시청거리가 한계를 넘을 수 있어요.');
 if(s.id==='s_wall'||s.id==='s_none')warn.push('벽걸이 설치비·벽 보강은 포함되지 않았어요.');
 if(/스탠드형/.test(v.name)&&s.id==='s_fs64')warn.push('스탠드형 TV는 다리 분리 후 장착 가능한지 확인하세요.');
 $('cWarn').innerHTML=warn.join('<br>');
}
['cT','cSeats','cD','cV','cSt'].forEach(function(i){$(i).addEventListener('change',run)});run();
})();

/* 출처 목록 */
(function(){
var L=[['데스커 멀티테이블 DSTDA1808','https://www.desker.co.kr/product/detail/694'],['데스커 모션데스크 프리미엄 1600×800','https://www.desker.co.kr/product/detail/279'],['데스커 모션데스크 플러스 1600×700','https://www.desker.co.kr/product/detail/247'],['다나와 데스커 멀티테이블','https://prod.danawa.com/info/?pcode=93912152'],['동서가구 가이아 테이블','https://www.dongsuhfurniture.co.kr/goods/goods_view.php?goodsNo=37603'],['퍼스트사무용가구 가이아 테이블','https://www.1gagu.com/goods/goods_view.php?goodsNo=186800931'],['한샘오피스 LT-소프트','https://office.hanssem.com/products/meetingspaces/training/lt-soft'],['현대리바트 CLECS 폴딩테이블','https://www.hyundailivart.co.kr/p/P200203264'],['코아스 FOCUS KAFT1501 (ggif)','https://www.ggif.kr/goods/goods_view.php?goodsNo=1000002235'],['에누리 룸앤오피스 YWD6029','https://price.enuri.com/catalog/106739798'],['일룸 뉴트 모션데스크 1400','https://www.iloom.com/product/detail.do?productCd=IDM0012A'],['다나와 카멜마운트 핏쳐 E2','https://prod.danawa.com/info/?pcode=73695098'],['다나와 삼성 KU55UH8000FXKR (벽걸이)','https://prod.danawa.com/info/?pcode=122641079'],['다나와 삼성 KU65UH8000FXKR (벽걸이)','https://prod.danawa.com/info/?pcode=122641155'],['다나와 삼성 KU65UH8000FXKR (스탠드)','https://prod.danawa.com/info/?pcode=122641150'],['다나와 LG 65UA7500ENA','https://prod.danawa.com/info/?pcode=92376488'],['엔산마운트 FS-64B','https://www.nsan.co.kr/goods/goods_view.php?goodsNo=1000001322'],['아이존아이앤디 TV거치대 목록','https://eyezoneind.com/category/tv%EA%B1%B0%EC%B9%98%EB%8C%80/167/']];
var u=document.getElementById('srcs');if(!u)return;
u.innerHTML=L.map(function(x){return '<li><a href="'+x[1]+'" target="_blank" rel="noopener">'+x[0]+' ↗</a></li>'}).join('');
})();
