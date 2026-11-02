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
SHORT["desk_ceo2"]="모션데스크 #2 (대표 옆)"
CNOTE=dict(desk_ceo2="가격 확인 필요",bean="집에 있어요",proj="집에 미니 빔이 있어요",screen="빔 쓸 때만",cam="iPhone으로 해요",light="촬영할 때만",mic="촬영할 때만",lav="촬영할 때만")
NSHORT=dict(strip="전기 안전",doorsign="로고 인쇄물",nameplate="이름·로고 제작",router="이미 고른 모델",switch="네트워크 장비",cctv_cam="보안 장비",cctv_rec="저장장치")
GRPS={}
for i in DEF_USED: GRPS.setdefault(i["grp"],[]).append(i)
used_html='<div class="tiles">'+"".join(tile(SHORT[i["id"]],px(sub(dtier(i),10)),CNOTE.get(i["id"],"")) for i in DEF_USED)+'</div>'
new_html='<div class="tiles">'+"".join(tile(SHORT[i["id"]],px(sub(dtier(i),10)),NSHORT[i["id"]]) for i in DEF_NEW)+'</div>'
own_chips=["모션데스크 (대표 · 1대)","NAS","공유기 (집에 있는 것)","커피머신","iPhone","로봇청소기","서진이 책상","접이식 책상","빈백","미니 빔프로젝터","캠핑용품 (품목 확인 예정)","이케아 전등","34형 모니터"]
own_html='<div class="chips">'+"".join(f'<span class="chip">{E(x)}</span>' for x in own_chips)+'</div>'

def mcard(i,qn):
    t=i[i["rec"]]; s=sub(t,10)
    return (f'<article class="pc3"><div class="pimg"><img src="assets/img/{t["img"]}" alt="{E(t["n"])}" loading="lazy"></div>'
      f'<h3>{qn}</h3><p class="pn">{E(t["n"])}</p><p class="pp">{won_(t["p"])}원 × {q(t,10)}</p><p class="ps">{won_(s)}원</p>'
      +(f'<a class="lk" href="{t["u"]}" target="_blank" rel="noopener">판매 페이지 ›</a>' if t["u"] else '')+'</article>')
main_cards="".join(mcard(i,qn) for i,qn in zip(MAINI,["교육 책상 (멀티데스크)","학습자 의자","대표 의자"]))
def rcard(tag,title,line,total,imgs):
    ims="".join(f'<div class="pimg"><img src="assets/desks/{x}" alt="" loading="lazy"></div>' for x in imgs)
    return f'<article class="rc"><div class="rimgs">{ims}</div><span class="rtag">{tag}</span><h3>{title}</h3><p>{line}</p><p class="ps">{won_(total)}원</p></article>'
rec_cards=rcard("⭐ 추천 1","일룸 엘바 + 알렉스","책상 ×5 · 의자 ×10",REC1,["iloom-HSUD018.jpg","iloom-HVCH3900H.jpg"])
def cfgcard(tag,title,l1,l2,fit,fcls,total,imgs,rec=False):
    ims="".join(f'<div class="pimg"><img src="assets/{x if "/" in x else "desks/"+x}" alt="" loading="lazy"></div>' for x in imgs)
    b='<span class="rec-b">추천</span>' if rec else ''
    return (f'<article class="cfg{" rec" if rec else ""}">{b}<div class="rimgs">{ims}</div><span class="rtag">{tag}</span><h3>{title}</h3>'
      f'<p>{l1}</p><p>{l2}</p><p class="fit {fcls}">{fit}</p><p class="ps">{won_(total)}원</p></article>')
# ---- 의자 후보 (서울대 의자) : 이미지는 assets/chairs/
CHAIR_CANDS=[
 dict(img="ible.webp",rec=True,tag="⭐ 선택 · 서울대 의자",n="시디즈 아이블 IBLE",u="https://kr.sidiz.com/products/ible",unit=189000,
  price="189,000원 (정가 199,000원 표시 · 높이조절형 199,000원)",src="시디즈 공식몰 2026-11-02",rate="★ 4.8 · 리뷰 3,231개 (오늘의집, 2026-11-02)",
  opt="헤드레스트 없음 · 팔걸이 있음(조절 기능은 공식 설명에 없음)",pro="서울대 의자(T501FE)의 현재 모델 · 가장 저렴 · 5년 품질보증",con="틸팅(등받이 젖힘) 없음 · 높이 고정형이 기본 · 공식 추천 키 150~175cm"),
 dict(img="ch2811.webp",rec=False,tag="연세대 의자",n="퍼시스 CH2811 (아이티스2)",u="https://fursysmall.com/shop/shopbrand.html?prize1=CH2811&search=",unit=217000,
  price="217,000원 (퍼시스몰 표시, 정가 248,600원)",src="퍼시스몰 2026-11-02 · 같은 날 다른 검색 결과엔 188,320원, 롯데홈쇼핑은 234,220원이라 판매처마다 달라요",rate="별점 5.0 (롯데홈쇼핑, 1건뿐이라 참고만)",
  opt="헤드레스트 없음 · 팔걸이 있음",pro="앞바퀴만 있어 밀리지 않아요 · ‘연세대 의자’로 불리는 모델이에요",con="높이 조절 안 됨 · 후기 수가 적어 비교가 어려워요 · 아이블보다 비싸요"),
 dict(img="t20.webp",rec=False,tag="한 단계 위",n="시디즈 T20 2세대",u="https://kr.sidiz.com/products/t20",unit=239000,
  price="239,000원 (정가 269,000원 표시)",src="시디즈 공식몰 2026-11-02",rate="★ 4.9 · 리뷰 약 1,463개 (오늘의집, 검색 결과 요약 기준이라 직접 확인 전)",
  opt="헤드레스트는 별도 27,000원(공식몰) · 팔걸이 높이 조절 없음(1세대 후기 기준)",pro="틸팅 있음 · 헤드레스트를 추가할 수 있어요",con="아이블보다 10개에 50만원 비싸요 · 2세대 팔걸이 사양은 직접 확인하지 못했어요"),
 dict(img="t50hf.webp",rec=False,tag="헤드레스트형",n="시디즈 T50 HF",u="https://kr.sidiz.com/products/t50hf",unit=309000,
  price="309,000원 (정가 329,000원 표시)",src="시디즈 공식몰 2026-11-02",rate="★ 4.88 · 리뷰 1,656개 (네이버 가격비교, 2026-11-01)",
  opt="헤드레스트 높이·각도 조절 있음 · 팔걸이 고정형",pro="헤드레스트와 틸팅이 있는 구성 · 후기 1,600개 이상 4.88점",con="10개에 약 309만원이라 예산이 커져요"),
]
def chair_item(c):
    t=f'<span class="ctag{" on" if c["rec"] else ""}">{c["tag"]}</span>'
    return (f'<article class="chi{" rec" if c["rec"] else ""}"><div class="chimg"><img src="assets/chairs/{c["img"]}" alt="{E(c["n"])}" loading="lazy"></div>'
      f'<div class="chtx">{t}<h4><a href="{c["u"]}" target="_blank" rel="noopener">{E(c["n"])} ›</a></h4>'
      f'<p class="chp"><b>{E(c["price"])}</b> · 10개 {won_(c["unit"]*10)}원</p>'
      f'<p>{E(c["rate"])}</p><p>{E(c["opt"])}</p><p class="pr"><b>좋은 점</b> {E(c["pro"])}</p><p class="co"><b>아쉬운 점</b> {E(c["con"])}</p>'
      f'<p class="src">출처 · {E(c["src"])}</p></div></article>')
chair_block=('<p class="note-s" style="margin-top:0">‘서울대 의자’는 공식 이름이 아니라 별칭이에요. 후기들은 시디즈 T501FE(지금 이름은 아이블)를 가리켜요. 퍼시스 CH2811은 ‘연세대 의자’로 불려요. 대학 납품 여부는 공식 확인을 못 했어요.</p>'
 '<div class="chlist">'+"".join(chair_item(c) for c in CHAIR_CANDS)+'</div>'
 f'<p class="note-s">고른 이유: 서울대 의자 그 자체이고, 후보 중 가장 싸며(10개 {won_(CHAIR_L*10)}원), 후기도 3,000개 넘게 4.8점이에요. 이전 선택이던 데스커 올라운드 HF(252,000원)보다 10개에 {won_(2520000-CHAIR_L*10)}원 줄어요. 대표 의자는 헤드레스트와 틸팅이 있는 시디즈 T50 2세대 419,000원 그대로예요(후기 ★4.88 · 715개, 네이버 가격비교 2026-11-01). 가격은 쿠폰·배송비를 뺀 표시값이고 후기 수는 쇼핑몰마다 달라요.</p>')
cfg_cards=(cfgcard("A · 협업형","멀티데스크 ×5","시디즈 아이블 의자 ×10","2인씩 나란히 앉아요","도면 반영 완료","ok",CFG_A,["desker-688.webp","chairs/ible.webp"],True)
 +cfgcard("B · 개인형","컴퓨터데스크 2.0 ×10","시디즈 아이블 의자 ×10","한 사람에 책상 하나","10대는 자리 부족","no",CFG_B,["desker-616.webp","chairs/ible.webp"])
 +cfgcard("C · 모션 믹스","컴퓨터데스크 ×7 + 모션데스크 ×3","시디즈 아이블 의자 ×10","3명은 서서도 일해요","10대는 자리 부족","no",CFG_C,["desker-239.webp","chairs/ible.webp"]))
cfg_detail=f"""<table class="tbl"><thead><tr><th>구성</th><th>책상</th><th>의자</th><th>합계</th><th>자리</th></tr></thead><tbody>
<tr><td><b>A ⭐</b></td><td>멀티데스크 1800×800 × 5 = {won_(294000*5)}원</td><td>시디즈 아이블 × 10 = {won_(CHAIR_L*10)}원</td><td><b>{won_(CFG_A)}원</b></td><td>도면 반영 완료. 양팔 2개씩 + 입구 쪽 상석 1개(두 팔 가운데에 대칭)예요. 안쪽 통로 0.7m, 오른쪽 통로 약 1.03m예요. 대표 옆 모션데스크 1대는 가격 확인 필요라 합계에 안 들어 있어요.</td></tr>
<tr><td><b>B</b></td><td>컴퓨터데스크 2.0 1400×700 × 10 = {won_(207000*10)}원</td><td>시디즈 아이블 × 10 = {won_(CHAIR_L*10)}원</td><td><b>{won_(CFG_B)}원</b></td><td>책상+의자가 차지하는 면적 약 20㎡. 학습존은 약 14.6㎡라 10대는 안 들어가요. ㄷ자 팔에는 2대씩, 4~5석 정도예요.</td></tr>
<tr><td><b>C</b></td><td>컴퓨터데스크 × 7 = {won_(207000*7)}원 + 모션데스크 플러스 1400×700 × 3 = {won_(670000*3)}원</td><td>시디즈 아이블 × 10 = {won_(CHAIR_L*10)}원</td><td><b>{won_(CFG_C)}원</b></td><td>B와 같은 크기라 자리 문제도 같아요.</td></tr>
</tbody></table>
<p class="note-s">면적은 책상 + 의자 뒤 0.75m 기준 계산이에요. 1200×600 컴퓨터데스크(150,000원) 10대로 줄여도 약 16㎡라 안 들어가요.</p>
<p class="note-s">가격은 데스커 공식몰 2026-11-02 표시값이에요. 의자는 시디즈 공식몰 2026-11-02 표시값(아이블 189,000원)이에요. 이전 선택이던 데스커 올라운드 HF(252,000원)보다 10개에 {won_(2520000-CHAIR_L*10)}원 싸요. 책상 선택 링크: <a href="https://www.desker.co.kr/product/detail/688" target="_blank" rel="noopener">멀티데스크 ›</a> · <a href="https://www.desker.co.kr/product/detail/616" target="_blank" rel="noopener">컴퓨터데스크 2.0 ›</a> · <a href="https://www.desker.co.kr/product/detail/239" target="_blank" rel="noopener">모션데스크 플러스 ›</a> · </p>
<p class="note-s">의자 선택 링크: <a href="https://kr.sidiz.com/products/ible" target="_blank" rel="noopener">시디즈 아이블 ›</a></p>
<p class="note-s">멀티탭&클램프 세트(50,000원)는 합계에 넣지 않았어요.</p>"""

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
<meta property="og:description" content="새로 살 것 {won_(CFG_A)}원 · 데스커 구성 · 도면 · 할 일">
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
 <p class="big">{won_(CFG_A)}<small>원</small></p>
 <p class="sub">데스커 책상 5대와 시디즈 아이블 의자 10개. 대표 의자는 별도예요.</p>
 <p class="meta">전용 44.2㎡ (약 13.4평) · 10석 · 입주 11/10(화)</p>
 <p class="acts"><a href="#layout">도면 보기 ›</a><a href="3d/">3D로 보기 ›</a></p>
</div></header>
<main>

<section class="asec gray" id="layout"><div class="awrap">
 <h2>도면</h2>
 <p class="sub">ㄷ자 10석 · 데스커 멀티데스크 1800×800 ×5 · 대표실 모션데스크 ×2.</p>
 <figure class="plan"><a href="assets/img/layout-10.png" target="_blank" rel="noopener"><img src="assets/img/layout-10.png" alt="ㄷ자 10석 배치도 (상석이 양팔 가운데, ㄷ자 끝에 전자칠판, 오른쪽 벽 소파, 창 쪽 대표실에 모션데스크 2개와 복합기)" loading="lazy"></a></figure>
 <p class="acts"><a href="3d/">3D로 보기 ›</a><a href="assets/img/layout-10.png" target="_blank" rel="noopener">큰 이미지 ›</a></p>
 {det("배치 · 거리 · 통로 · 12석 · 15석",lay_i)}
 {det("가정한 것 · 요약",inner("summary"))}
</div></section>

<section class="asec" id="buy"><div class="awrap">
 <h2>데스커로 맞춘 구성</h2>
 <p class="sub">책상과 의자, 세 가지 중 골라요.</p>
 <div class="cgrid">{cfg_cards}</div>
 <p class="note-s">추천은 A예요. 가장 싸고, 학습존에 들어갈 수 있는 구성이에요. 대표 의자 시디즈 T50({won_(419000)}원)은 별도예요.</p>
 {det("구성 비교 · 자리 계산",cfg_detail)}
 {det("구매표 · 새로 사는 합계 (A + 대표 의자) · 12·15석",buy_a)}
 {det("의자 후보 · 서울대 의자",chair_block)}
 {det("다른 브랜드 후보",'<div class="rgrid">'+rec_cards+'</div>'+inner("premium"))}
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
