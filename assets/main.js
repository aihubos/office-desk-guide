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

/* calculator */
(function(){
  var D=window.DATA; if(!D) return;
  var $=function(i){return document.getElementById(i)};
  var seats=$('cSeats'),tier=$('cTier'),ch=$('cCh'),lt=$('cLater');
  if(!seats) return;
  var won=function(n){return n.toLocaleString('ko-KR')+'원'};
  function run(){
    var m=seats.value, tr=tier.value, groups={}, total=0;
    D.items.forEach(function(it){
      if(it.chair && !ch.checked) return;
      var later=it.pri==='나중에';
      var k;
      if(tr==='R'){ if(!it.rec) return; if(later && !lt.checked) return; k=it.rec; }
      else { k=tr; if(later && !lt.checked) return; }
      var t=it[k], s=t.p*t.q[m];
      total+=s; groups[it.grp]=(groups[it.grp]||0)+s;
    });
    $('cTotal').textContent=won(total);
    $('cList').innerHTML=Object.keys(groups).map(function(g){return '<li><span>'+g+'</span><b>'+won(groups[g])+'</b></li>'}).join('');
    $('cWarn').textContent=(m==='15'?'15석: 의자·슬리퍼 수량이 늘어난 값이에요. ':m==='12'?'12석: 의자·슬리퍼 12개 기준이에요. ':'10석: 학습자 의자 10개·슬리퍼 10켤레 기준이에요(슬리퍼 가격 미정이라 합계에 없음). ')+'설치·배송·용달 비용은 제외, 보유 품목(모션데스크·NAS)은 0원이에요.';
  }
  [seats,tier,ch,lt].forEach(function(e){e.addEventListener('change',run)});
  run();
})();
