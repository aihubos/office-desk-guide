# ---- 애플 스타일 페이지 조립 (old_html의 긴 내용은 접어서 보관) ----
import re
def inner(sid):
    m=re.search(r'<section class="sec[^"]*" id="%s"><div class="wrap">(.*?)</div></section>'%sid, old_html, re.S)
    assert m, sid
    s=m.group(1)
    s=re.sub(r'<div class="eyebrow">.*?</div>','',s,count=1,flags=re.S)
    s=re.sub(r'<h2>.*?</h2>','',s,count=1,flags=re.S)
    return s
def det(title,body,sub=""):
    return f'<details class="more"><summary><span>자세히 보기</span><em>{title}</em></summary><div class="mbody">{body}</div></details>'
def tile(name,price,note="",cls=""):
    n=f'<small>{note}</small>' if note else ''
    return f'<div class="tile {cls}"><b>{name}</b><span>{price}</span>{n}</div>'
def px(s): return f'{won_(s)}원' if s>0 else '가격 미정'

SHORT=dict(board="전자칠판 75형",slipper="슬리퍼 ×10",wb="이동식 화이트보드",f_desk="포커스 데스크",f_mon="포커스 모니터 27형",f_arm="모니터암",
 kid_corner="아지트 코너",shelf="책장 가벽 (빌리 ×3)",bean="빈백",sofa="소파 2인",tea="티테이블",dining="세라믹 식탁",speaker="마샬 스피커",
 humid="가습기",purifier="공기청정기",fridge="냉장고",coffee="커피머신",mfp="복합기",light="조명 (키 라이트)",mic="데스크 마이크",lav="무선 마이크",
 cam="카메라",tripod="삼각대",shelfled="책장 LED",foam="흡음재 ×6",stu_desk="촬영 책상",proj="빔프로젝터",screen="프로젝터 스크린",printer="별도 프린터",p3d="3D 프린터",
 doorsign="도어사인",nameplate="대표 책상 명패",router="공유기",switch="스위칭 허브",strip="멀티탭",cctv_cam="CCTV 카메라 ×2",cctv_rec="CCTV 녹화·저장")
CNOTE=dict(bean="집에 있어요",proj="집에 미니 빔이 있어요",screen="빔 쓸 때만",cam="iPhone으로 해요",light="촬영할 때만",mic="촬영할 때만",lav="촬영할 때만")
NSHORT=dict(strip="전기 안전",doorsign="로고 인쇄물",nameplate="이름·로고 제작",router="이미 고른 모델",switch="네트워크 장비",cctv_cam="보안 장비",cctv_rec="저장장치")
GRPS={}
for i in DEF_USED: GRPS.setdefault(i["grp"],[]).append(i)
used_html='<div class="tiles">'+"".join(tile(SHORT[i["id"]],px(sub(dtier(i),10)),CNOTE.get(i["id"],"")) for i in DEF_USED)+'</div>'
new_html='<div class="tiles">'+"".join(tile(SHORT[i["id"]],px(sub(dtier(i),10)),NSHORT[i["id"]]) for i in DEF_NEW)+'</div>'
own_chips=["모션데스크 (대표)","NAS","공유기 (집에 있는 것)","iPhone","로봇청소기","서진이 책상","접이식 책상","빈백","미니 빔프로젝터","캠핑용품 (품목 확인 예정)","이케아 전등","34형 모니터"]
own_html='<div class="chips">'+"".join(f'<span class="chip">{E(x)}</span>' for x in own_chips)+'</div>'

def mcard(i,qn):
    t=i[i["rec"]]; s=sub(t,10)
    return (f'<article class="pc3"><div class="pimg"><img src="assets/img/{t["img"]}" alt="{E(t["n"])}" loading="lazy"></div>'
      f'<h3>{qn}</h3><p class="pn">{E(t["n"])}</p><p class="pp">{won_(t["p"])}원 × {q(t,10)}</p><p class="ps">{won_(s)}원</p>'
      +(f'<a class="lk" href="{t["u"]}" target="_blank" rel="noopener">판매 페이지 ›</a>' if t["u"] else '')+'</article>')
main_cards="".join(mcard(i,qn) for i,qn in zip(MAINI,["교육 책상 1800×600","교육 책상 1200×600","학습자 의자","대표 의자"]))
def rcard(tag,title,line,total,imgs):
    ims="".join(f'<div class="pimg"><img src="assets/desks/{x}" alt="" loading="lazy"></div>' for x in imgs)
    return f'<article class="rc"><div class="rimgs">{ims}</div><span class="rtag">{tag}</span><h3>{title}</h3><p>{line}</p><p class="ps">{won_(total)}원</p></article>'
rec_cards=rcard("⭐ 추천 1","일룸 엘바 + 알렉스","책상 ×5 · 의자 ×10",REC1,["iloom-HSUD018.jpg","iloom-HVCH3900H.jpg"])+rcard("⭐ 추천 2","데스커 컴퓨터데스크 + 올라운드 HF","책상 ×10 · 의자 ×10",REC2,["desker-616.webp","desker-305.webp"])

TODO=[("11/5~11/7","용달 예약",True),("11/5까지","도어사인 주문",True),("입주 전","인터넷 개통 신청",False),("입주 전","정수기 설치 신청 · 급수 위치 확인",False),
 ("거래 전","전자칠판 당근 거래 확인",False),("입주 전","관리단 업종 확인",False),("입주 전","사업자 주소 이전",False),("이사 전","NAS 백업",False),("입주 전","실측",False)]
todo_html='<ul class="tdl">'+"".join(f'<li class="{"hot" if h else ""}"><i></i><b>{d}</b><span>{x}</span></li>' for d,x,h in TODO)+'</ul>'

buy_i=inner("buy"); k=buy_i.index('<h3 class="sub3">당근·중고가구점')
buy_a,buy_b=buy_i[:k],buy_i[k:]
lay_i=inner("layout")
lay_i=re.sub(r'<div class="lay1 reveal"><figure>.*?</figure></div>','',lay_i,count=1,flags=re.S)
lay_i=re.sub(r'<p style="margin-top:12px"><a href="3d/".*?</p>','',lay_i,count=1,flags=re.S)

html_out=f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#ffffff">
<title>AI Builders Lab · 동탄 사무실</title>
<meta name="description" content="동탄 사무실 10석: 새로 살 것 {won_(M10)}원. 도면, 구매, 집에서 가져올 것, 월 고정비, 할 일.">
<meta property="og:title" content="AI Builders Lab · 동탄 사무실">
<meta property="og:description" content="새로 살 것 {won_(M10)}원 · 도면 · 할 일">
<meta property="og:type" content="website">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='9' fill='%231d1d1f'/%3E%3Cpath d='M7 12h18M10 12v10M22 12v10' stroke='%23fff' stroke-width='3' fill='none' stroke-linecap='round'/%3E%3C/svg%3E">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="assets/apple.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body id="top">
<nav class="anav" aria-label="목차"><div class="anavin"><a class="brand" href="#top">동탄 사무실</a>
<div class="navin"><a href="#layout">도면</a><a href="#buy">새로 살 것</a><a href="#used">당근·중고</a><a href="#newrec">새제품</a><a href="#own">집에서</a><a href="#monthly">월 고정비</a><a href="#todo">할 일</a></div></div></nav>
<header class="ahero"><div class="awrap">
 <p class="eb">AI Builders Lab · 현대실리콘앨리 동탄 1529호</p>
 <h1>새로 살 것</h1>
 <p class="big">{won_(M10)}<small>원</small></p>
 <p class="sub">책상과 의자 10석. 이게 전부예요.</p>
 <p class="meta">전용 44.2㎡ (약 13.4평) · 10석 · 입주 11/10(화)</p>
 <p class="acts"><a href="#layout">도면 보기 ›</a><a href="3d/">3D로 보기 ›</a></p>
</div></header>
<main>

<section class="asec gray" id="layout"><div class="awrap">
 <h2>도면</h2>
 <p class="sub">ㄷ자 10석, 한 장으로.</p>
 <figure class="plan"><a href="assets/img/layout-10.png" target="_blank" rel="noopener"><img src="assets/img/layout-10.png" alt="ㄷ자 10석 배치도 (상석이 입구 쪽, ㄷ자 끝에 전자칠판, 책장 가벽 뒤 소파·대표실)" loading="lazy"></a></figure>
 <p class="acts"><a href="3d/">3D로 보기 ›</a><a href="assets/img/layout-10.png" target="_blank" rel="noopener">큰 이미지 ›</a></p>
 {det("배치 · 거리 · 통로 · 12석 · 15석",lay_i)}
 {det("가정한 것 · 요약",inner("summary"))}
</div></section>

<section class="asec" id="buy"><div class="awrap">
 <h2>새로 살 것</h2>
 <p class="sub">책상과 의자만 새로 사요.</p>
 <div class="pgrid">{main_cards}</div>
 <p class="tot">10석 합계 <b>{won_(M10)}원</b></p>
 <h3 class="h3c">다른 후보</h3>
 <p class="sub s2">프리미엄 두 가지예요.</p>
 <div class="rgrid">{rec_cards}</div>
 {det("구매표 · 프리미엄 vs 가성비 · 12·15석",buy_a)}
 {det("프리미엄 책상·의자 후보 15종",inner("premium"))}
 {det("서울대 의자",inner("chairs"))}
 {det("책상·전자칠판 후보 · 시청거리",inner("ref"))}
 {det("체크리스트 · 새로 살 것",inner("checklist").split('<h3 class="sub3">집에서 가져올 물건')[0])}
</div></section>

<section class="asec gray" id="used"><div class="awrap">
 <h2>당근·중고로 사요</h2>
 <p class="sub">새제품 참고가예요. 합계엔 빠져요.</p>
 <p class="tot">참고가 합계 <b>{won_(DU10)}원</b></p>
 {used_html}
 {det("당근·중고 구매 예정 전체 표",buy_b)}
</div></section>

<section class="asec" id="newrec"><div class="awrap">
 <h2>이건 새제품으로</h2>
 <p class="sub">중고보다 새것이 안전해요.</p>
 <p class="tot">참고가 합계 <b>{won_(DN10)}원</b></p>
 {new_html}
</div></section>

<section class="asec gray" id="own"><div class="awrap">
 <h2>집에서 가져와요</h2>
 <p class="sub">이미 있는 건 사지 않아요.</p>
 {own_html}
 {det("가져올 물건 전체 목록",'<ul class="checks">'+OWN+'</ul>')}
</div></section>

<section class="asec" id="monthly"><div class="awrap">
 <h2>월 고정비</h2>
 <p class="sub">인터넷과 정수기예요.</p>
 <div class="mgrid">
  <div class="mc"><span>인터넷</span><b>월 55,000원</b><p>KT 오피스넷 2.5G · 3년 약정</p></div>
  <div class="mc"><span>정수기</span><b>월 35,900원</b><p>코웨이 아이콘3 · 방문관리 렌탈</p></div>
 </div>
 {det("인터넷 · 정수기 비교",inner("monthly"))}
</div></section>

<section class="asec gray" id="todo"><div class="awrap">
 <h2>할 일</h2>
 <p class="sub">입주는 11/10(화)예요.</p>
 {todo_html}
 {det("할 일 자세히",inner("todo"))}
</div></section>

<section class="asec" id="more"><div class="awrap">
 <h2>더 보기</h2>
 <p class="sub">필요할 때만 열어 보세요.</p>
 {det("계산기 · 합계",inner("cost"))}
 {det("촬영 코너 (선택)",inner("studio"))}
 {det("네트워크 · 전원",inner("network"))}
 {det("복합기 · 프린터 · 3D 프린터",inner("print"))}
 {det("확인하지 못한 것 · 출처",inner("sources"))}
</div></section>
</main>
<footer><div class="awrap">AI Builders Lab · 동탄 사무실 · {D}(KST) 기준 · 가격은 변동될 수 있어요</div></footer>
<script>window.DATA={json.dumps(data,ensure_ascii=False)};</script>
<script src="assets/main.js"></script>
</body></html>'''
open("../index.html","w",encoding="utf8").write(html_out)
