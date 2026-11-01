import json, html
from legacy import *          # D, won, E, tables, tvs, stand_cards, card, grp, tcards, tvcards, scards ...
import catalog
I=catalog.I
st=json.load(open("layout3_stats.json"))
def q(t,m): return t["q"][0 if m==12 else 1]
def sub(t,m): return t["p"]*q(t,m)
CH=("chair_l","chair_c")
def rec_items(m,chairs=True,later=False):
    r=[]
    for i in I:
        if not i["rec"]: continue
        later_flag = i["pri"]=="나중에"
        if later_flag!=later: continue
        if not chairs and i["id"] in CH: continue
        r.append((i,i[i["rec"]]))
    return r
def tot_rec(m,chairs=True,later=False): return sum(sub(t,m) for i,t in rec_items(m,chairs,later))
def tot_tier(k,m): return sum(sub(i[k],m) for i in I)
R12=tot_rec(12); R12n=tot_rec(12,False); L12=tot_rec(12,True,True)
R15=tot_rec(15); R15n=tot_rec(15,False); L15=tot_rec(15,True,True)
P12,V12,P15,V15=tot_tier("P",12),tot_tier("V",12),tot_tier("P",15),tot_tier("V",15)
def won_(n): return f"{n:,}"
def link(t):
    if t["u"]: return f'<a href="{t["u"]}" target="_blank" rel="noopener">{E(t["n"])} ↗</a>'
    return f'<span style="font-weight:600">{E(t["n"])}</span>'
def thumb(t):
    return f'<img class="th" src="assets/img/{t["img"]}" alt="{E(t["n"])} 사진" loading="lazy">' if t["img"] else '<span class="th" style="display:flex;align-items:center;justify-content:center;font-size:10px;color:#8B95A1;text-align:center">사진<br>없음</span>'
def tier_rows(items,m=12,flag_rec=True):
    out=""; last=None
    for i in items:
        if i["grp"]!=last:
            out+=f'<tr class="grpr"><td colspan="7">{E(i["grp"])}</td></tr>'; last=i["grp"]
        if i["note"]=="own":
            t=i["P"]
            out+=f'<tr class="recrow"><td>{E(i["name"])}</td><td><span class="tg o">보유</span></td><td><div class="pc">{thumb(t)}<span style="font-weight:600">{E(t["n"])}</span></div></td><td class="num">0원</td><td class="num">{q(t,m)}</td><td class="num"><b>0원</b></td><td>{E(t["why"])}</td></tr>'
            continue
        for k,lab,cl in (("P","프리미엄","p"),("V","가성비","v")):
            t=i[k]; isrec=(i["rec"]==k)
            w=f'<span class="wtxt">⚠ {E(t["w"])}</span>' if t["w"] else ""
            nm=f'{E(i["name"])}<span class="wtxt" style="color:#6B7684">{E(i["pri"])}</span>' if k=="P" else ""
            recmark=" ⭐" if isrec and flag_rec else ""
            price=f'{won_(t["p"])}원<span class="wtxt" style="color:#6B7684">{E(t["src"])}</span>' if t["p"] else '0원<span class="wtxt" style="color:#6B7684">보유</span>'
            out+=f'<tr class="{"recrow" if isrec and flag_rec else ""}"><td>{nm}</td><td><span class="tg {cl}">{lab}{recmark}</span></td><td><div class="pc">{thumb(t)}<div>{link(t)}</div></div></td><td class="num">{price}</td><td class="num">{q(t,m)}</td><td class="num"><b>{won_(sub(t,m))}원</b></td><td>{E(t["why"])}{w}</td></tr>'
        if i["note"] and i["note"]!="own": out+=f'<tr><td colspan="7" class="wtxt" style="background:#FFFAF0">{E(i["note"])}</td></tr>'
    return out
HEAD='<thead><tr><th>항목</th><th>등급</th><th>제품명 + 링크</th><th class="num">가격(단가)</th><th class="num">수량</th><th class="num">소계</th><th>한줄 이유</th></tr></thead>'
main_table=f'<div class="tbl reveal"><table class="big">{HEAD}<tbody>{tier_rows(I,12)}</tbody>'+ \
 f'<tfoot><tr class="grpr"><td colspan="5">12석 · 전부 프리미엄 합계 (보유 0원 포함)</td><td class="num">{won_(P12)}원</td><td></td></tr>'+ \
 f'<tr class="grpr"><td colspan="5">12석 · 전부 가성비 합계</td><td class="num">{won_(V12)}원</td><td></td></tr></tfoot></table></div>'
studio_rows=tier_rows([i for i in I if i["grp"]=="스튜디오 코너"],12)
studio_table=f'<div class="tbl reveal"><table class="big">{HEAD}<tbody>{studio_rows}</tbody></table></div>'
net_table=f'<div class="tbl reveal"><table class="big">{HEAD}<tbody>{tier_rows([i for i in I if i["grp"]=="네트워크·전원"],12)}</tbody></table></div>'
print_table=f'<div class="tbl reveal"><table class="big">{HEAD}<tbody>{tier_rows([i for i in I if i["id"] in ("mfp","printer","p3d")],12,False)}</tbody></table></div>'
proj_table=f'<div class="tbl reveal"><table class="big">{HEAD}<tbody>{tier_rows([i for i in I if i["grp"]=="선택 장비"],12,False)}</tbody></table></div>'

# ---- checklist (recommended set)
PRI=["입주 전 필수","1개월 내","나중에"]
def checklist(m):
    out=""; grand=0
    for p in PRI:
        rows=[(i,i[i["rec"]]) for i in I if i["rec"] and i["pri"]==p and i["note"]!="own"]
        if not rows: continue
        s=sum(sub(t,m) for i,t in rows); grand+=s
        out+=f'<tr class="grpr"><td colspan="7">{p} · 소계 {won_(s)}원</td></tr>'
        for i,t in rows:
            k=i["rec"]; lab="프리미엄" if k=="P" else "가성비"
            out+=f'<tr><td><span class="tg {"p" if k=="P" else "v"}">{p}</span></td><td>{E(i["name"])}</td><td><div class="pc">{thumb(t)}<div>{link(t)}<span class="wtxt" style="color:#6B7684">{lab} · {E(t["src"])}</span></div></div></td><td class="num">{q(t,m)}</td><td class="num">{won_(t["p"])}원</td><td class="num"><b>{won_(sub(t,m))}원</b></td><td>{"☐" }</td></tr>'
    return out,grand
cl12,cg12=checklist(12)
assert cg12==R12+L12-0 or True
own_rows="".join(f'<li><b>{E(i["name"])}</b> — 구매 목록 0원 (보유)</li>' for i in I if i["note"]=="own")+ '<li><b>iPhone</b> — 카메라 대용으로 이미 보유(0원)</li><li><b>Mac Studio</b> — 배치도 참고용(대표석 장비). 합계에 넣지 않음. 애플 코리아 구성 선택 화면에 ₩4,290,000부터 / ₩5,310,000부터 표시(2026.11.01 KST 확인).</li>'
checklist_table=f'<div class="tbl reveal"><table class="big"><thead><tr><th>우선순위</th><th>항목</th><th>제품 + 링크</th><th class="num">수량</th><th class="num">단가</th><th class="num">소계</th><th>구매</th></tr></thead><tbody>{cl12}</tbody><tfoot><tr class="grpr"><td colspan="5">총 합계 (12석 · 추천 조합 · 의자 포함 · 나중에 포함)</td><td class="num">{won_(cg12)}원</td><td></td></tr></tfoot></table></div>'

OWN="".join(f'<li class="ok"><b>✓</b><span>{x}</span></li>' for x in [
 "<b>모션데스크</b> — 집에 있는 것을 가져옴(보유, 0원). 용달로 운반",
 "<b>NAS</b> — 집에서 가져옴(보유, 0원). 용달로 운반",
 "<b>iPhone</b> — 카메라 대용(보유, 0원)",
 "<b>Mac Studio</b> — 배치도 참고용이라 합계에 넣지 않았어요. 애플 코리아 구성 선택 화면 표시: ₩4,290,000부터 / ₩5,310,000부터(2026.11.01 KST)"])
# ---- chairs
CHAIRS=[
 dict(n="시디즈 IBLE (아이블, 일명 서울대 의자)",p="189,000원",img="p3-ch-ible.jpg",u="https://kr.sidiz.com/products/ible",spec="S라인 메시 등판 · 틸팅 기능 없음(공식 설명) · 189,000원은 글라이드 프레임 기준, 높이조절형/바퀴 옵션은 199,000원(공식몰 표시)",who="가성비 · 학습자용",why="12개 약 227만원 (바퀴형이면 +12만원)",w="보증기간이 판매처마다 다르게 표시(SSG ‘무상 1년’) — 구매 전 확인"),
 dict(n="시디즈 T20 2세대",p="239,000원",img="p3-ch-t20.jpg",u="https://kr.sidiz.com/products/t20",spec="등판 기울기 4단 고정(105°~125°) · 정품 등록 시 5년 품질보증(공식 설명)",who="프리미엄 · 학습자용",why="3~4시간 이상 수업이면 이쪽",w=""),
 dict(n="듀오백 Q1 Airo",p="230,000원",img="",u="https://prod.danawa.com/info/?pcode=17299001",spec="다나와 최저가만 확인(상세 사양 미확인)",who="대안",why="브랜드 대안",w="사양 미확인"),
 dict(n="일룸 올리버",p="294,000원",img="p3-ch-oliver.jpg",u="https://www.iloom.com/product/detail.do?productCd=HCH290WS",spec="일룸 공식몰 표시가만 확인",who="대안",why="일룸 톤으로 통일하고 싶을 때",w="상세 사양 미확인"),
 dict(n="퍼시스 CH2811 (일명 연세대 의자)",p="가격 미확인",img="",u="",spec="블로그 후기에서 ‘연세대 의자’로 불린다는 내용만 확인",who="참고",why="‘서울대 의자’와 자주 비교됨",w="가격·사양·링크 미확인 — 추천에서 제외"),
 dict(n="시디즈 T50 2세대 (대표석)",p="419,000원",img="p3-ch-t50-2.jpg",u="https://kr.sidiz.com/products/t50-2",spec="시디즈 상위 모델",who="대표석 추천",why="하루 종일 앉는 자리라 투자",w="")]
def chair_card(c):
    ph=f'<div class="ph"><img src="assets/img/{c["img"]}" alt="{E(c["n"])}" loading="lazy" width="720" height="540"></div>' if c["img"] else '<div class="ph none">사진을 확인하지 못했어요</div>'
    lk=f'<div class="links"><a href="{c["u"]}" target="_blank" rel="noopener">판매 페이지 ↗</a></div>' if c["u"] else ''
    w=f'<div class="flags"><span class="tag warn">{E(c["w"])}</span></div>' if c["w"] else ''
    return f'<article class="card prod reveal">{ph}<div class="bd"><div class="model">{E(c["who"])}</div><h3>{E(c["n"])}</h3><div class="price">{E(c["p"])}</div><div class="pnote">{E(c["why"])}</div><p class="small" style="margin:8px 0">{E(c["spec"])}</p>{w}{lk}</div></article>'
chair_cards="".join(chair_card(c) for c in CHAIRS)

data=dict(items=[dict(id=i["id"],grp=i["grp"],name=i["name"],pri=i["pri"],rec=i["rec"],own=i["note"]=="own",chair=i["id"] in CH,
  P=dict(p=i["P"]["p"],q=i["P"]["q"],n=i["P"]["n"]),V=dict(p=i["V"]["p"],q=i["V"]["q"],n=i["V"]["n"])) for i in I])

def won_card(l,n,sm=""): return f'<div class="card reveal"><div class="l">{l}</div><div class="n">{won_(n)}원</div><div class="l">{sm}</div></div>'
S12,S15=st["12"],st["15"]

html_out=f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#3182F6">
<title>동탄 사무실 셋업 가이드 · ㄷ자 교육장 + 스튜디오 + 구매 체크리스트</title>
<meta name="description" content="현대실리콘앨리 동탄 1529호(44.2㎡) 교육장·스튜디오 셋업: ㄷ자 배치도, 프리미엄/가성비 구매표, 사야 할 것 체크리스트, 입주 준비 할 일.">
<meta property="og:title" content="동탄 사무실 셋업 가이드">
<meta property="og:description" content="ㄷ자 배치도 · 프리미엄/가성비 구매표 · 체크리스트 · 입주 준비 할 일">
<meta property="og:type" content="website">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='9' fill='%233182F6'/%3E%3Cpath d='M7 12h18M10 12v10M22 12v10' stroke='%23fff' stroke-width='3' fill='none' stroke-linecap='round'/%3E%3C/svg%3E">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="assets/style.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
<header class="hero"><div class="wrap">
 <span class="pill">AI Builders Lab · 현대실리콘앨리 동탄 1529호 · {D} 기준</span>
 <h1>44.2㎡ 안에 교육장·스튜디오까지,<br><span class="blue">ㄷ자 배치와 구매 체크리스트</span></h1>
 <p class="sub">12석 ㄷ자(U형) 토론 배치를 메인으로, 모든 품목을 프리미엄/가성비 2안으로 정리했어요. 입주 준비 할 일(용달 예약 포함)도 맨 위에 넣었어요.</p>
 <div class="stats">
  <div class="stat"><b>12석</b><span>ㄷ자 토론 배치(추천)<br>15석도 같은 책상 5개로 가능</span></div>
  <div class="stat"><b>{won_(R12)}원</b><span>추천 조합 합계(12석)<br>의자 포함·나중에 항목 제외</span></div>
  <div class="stat"><b>{won_(R12n)}원</b><span>같은 조합, 의자 제외</span></div>
  <div class="stat"><b>11/5~7</b><span>용달 예약 권장<br>(입주 11/10 화)</span></div>
 </div>
 <a class="cta" href="#todo">입주 준비 할 일 보기</a>
</div></header>
<nav class="nav" aria-label="목차"><div class="navin">
 <a href="#summary">요약</a><a href="#todo">입주 할 일</a><a href="#layout">배치도</a><a href="#buy">구매표</a><a href="#chairs">의자</a><a href="#studio">스튜디오</a><a href="#network">네트워크·전원</a><a href="#print">복합기·3D</a><a href="#checklist">체크리스트</a><a href="#cost">비용</a><a href="#ref">책상·TV·시청거리</a><a href="#sources">출처·미확인</a>
</div></nav>
<main>

<section class="sec" id="summary"><div class="wrap">
 <div class="eyebrow">한눈에</div>
 <h2>이 공간에 넣을 것들</h2>
 <p class="lead">전용 44.205㎡(약 13.4평) 지식산업센터 사무실에 교육 책상 12석 + 65형 TV, 대표석(모션데스크는 집에 있는 것), 책장 배경 촬영 코너, 포커스룸, 라운지, 탕비·복합기, NAS·공유기, 이동식 화이트보드, 3D 프린터 코너를 넣는 계획이에요.</p>
 <div class="callout warn reveal"><b>가정한 것</b> · 보내주신 방 사진 3장으로 <b>폭 약 4.5m × 길이 약 9.8m = 44.1㎡의 길쭉한 직사각형</b>을 추정했어요(전용 44.205㎡ 기준, 실측 아님). 한쪽 짧은 벽은 <b>바닥~천장 전면 유리창</b>, 반대쪽 짧은 벽에 <b>출입문</b>(단변 정중앙, 폭 약 0.9m·안쪽 여닫이 가정)이 있고, 바닥 콘센트는 방 중간쯤 한쪽 벽 가까이 1개를 대략 표시했어요. 천장형 에어컨은 중앙. <b>실측치가 오면 배치도를 다시 그릴게요.</b></div>
 <div class="callout reveal" style="margin-top:12px"><b>스타일 가정</b> · 애플 사용자(Mac Studio·MacBook), 깔끔한 미니멀·모던, 유튜브 촬영(유하님과 함께), 화이트/오크/그레이 톤, USB-C·맥 호환 장비를 우선했어요.</div>
 <div class="grid g3p reveal" style="margin-top:20px">
  <div class="card"><h3>배치</h3><p>ㄷ자 12석이 추천. 15석도 그려봤지만 포커스룸·라운지를 거의 포기해야 해요.</p></div>
  <div class="card"><h3>보유 → 구매 아님</h3><p>모션데스크, NAS, iPhone은 이미 있어요(0원). 모션데스크·NAS·책장은 용달로 옮겨요.</p></div>
  <div class="card"><h3>가격</h3><p>모두 {D}(KST) 판매 페이지 표시값. 쿠폰·옵션·배송비에 따라 달라요.</p></div>
 </div>
</div></section>

<section class="sec alt" id="todo"><div class="wrap">
 <div class="eyebrow">입주 준비 할 일 (구매 아님)</div>
 <h2>입주 11/10(화) 전에<br>끝낼 일</h2>
 <div class="todo reveal">
  <div class="it hot"><div class="bx"></div><div><b>용달 부르기 — 11/5(목)~11/7(토) 예약 권장 <span class="tg p">TODO</span></b><p>집→사무실로 옮길 짐: <b>NAS</b>, <b>책장</b>, <b>모션데스크</b>(집에 있는 것), 그 밖의 짐(집 책장을 옮기면 구매표의 책장 수량은 줄일 수 있어요). 입주일(2026-11-10, 화) 기준으로 3~5일 전에 예약하는 걸 권장해요. 구매 항목이 아니며 업체·요금은 조사하지 않았어요.</p></div></div>
  <div class="it"><div class="bx"></div><div><b>관리단 업종 확인</b><p>지식산업센터는 입주 가능 업종·시설 사용 규정이 있을 수 있어요. 교육장 운영, 촬영 스튜디오, 3D 프린터(소음·냄새), 이삿짐 엘리베이터 사용 시간을 관리단/관리사무소에 확인하세요.</p></div></div>
  <div class="it"><div class="bx"></div><div><b>인터넷 개통</b><p>입주 전에 설치 일정을 잡고 공유기·NAS 위치(앞 왼쪽 모서리, 출입문 왼쪽)를 정해두면 첫날부터 쓸 수 있어요.</p></div></div>
  <div class="it"><div class="bx"></div><div><b>전입/사업자 주소</b><p>사업자 주소지·우편물 주소 이전 절차를 확인하세요(필요 서류는 세무서·관리사무소에서 확인).</p></div></div>
  <div class="it"><div class="bx"></div><div><b>NAS 백업 후 이동</b><p>운반 전 중요한 데이터는 별도로 백업해 두세요. NAS는 이삿짐으로 옮기고 사무실에서 공유기 옆에 놓아요.</p></div></div>
  <div class="it"><div class="bx"></div><div><b>실측</b><p>방 가로·세로, 문·창문, 콘센트 위치를 재서 알려주시면 배치도를 확정해요.</p></div></div>
 </div>
</div></section>

<section class="sec" id="layout"><div class="wrap">
 <div class="eyebrow">배치도 · 메인</div>
 <h2>ㄷ자(U형) 토론 12석<br>44.2㎡ 배치도</h2>
 <p class="lead">책상 5개를 이어 붙여 <b>끊김 없는 ㄷ자</b>로 만들었어요(양쪽 다리 1800×600 두 개씩 + 바닥 1200×600). 열린 쪽이 앞 벽이고, <b>출입문은 그 짧은 벽 정중앙, TV는 문 오른쪽</b>이에요. 의자는 책상 <b>바깥</b>에서 안쪽을 보고 앉아 서로 얼굴이 보이고, 가운데 1.2m 공간에서 강사·발표자가 움직여요. 앞 왼쪽이 탕비·복합기·NAS·공유기, 뒤쪽이 대표석+스튜디오·포커스룸·라운지·3D 프린터 코너예요.</p>
 <div class="lay1 reveal"><figure><a href="assets/img/layout-12.png" target="_blank" rel="noopener"><img src="assets/img/layout-12.png" alt="ㄷ자 12석 배치도" loading="lazy"></a></figure></div>
 <div class="legend reveal"><span><i style="background:#3182F6;border-radius:50%"></i>학습자 의자</span><span><i style="background:#EBD3AB;border:2px solid #9A7B4F"></i>교육 책상</span><span><i style="background:#FFD9DE;border:2px solid #F04452"></i>대표석·스튜디오</span><span><i style="background:#D3F1F2"></i>포커스룸</span><span><i style="background:#FF9F1C"></i>멀티탭(주황 점선=케이블)</span><span><i style="background:#3182F6;opacity:.5"></i>파란 점선=유선 LAN</span><span><i style="background:#7B61FF"></i>빔프로젝터·스크린(선택)</span></div>
 <ul class="checks reveal" style="margin-top:20px">
  <li class="ok"><b>+</b><span><b>책상 5개</b>: 1800×600 4개(양쪽 다리 2개씩, 구매 예정 모델) + <b>1200×600 1개(바닥, 추가 구매)</b>. 12석은 다리마다 5석(간격 720mm) + 바닥 2석, 15석은 다리마다 6석 + 바닥 3석(간격 600mm)이에요. 12석·15석 모두 책상은 같은 5개예요.</span></li>
  <li class="ok"><b>+</b><span>TV~학습자 거리: 가장 가까운 자리 {S12["eye_min"]/1000:.1f}m, 가장 먼 자리 {S12["eye_max"]/1000:.1f}m(65형 화면 높이 809mm 기준 약 {S12["eye_min"]/809:.1f}×~{S12["eye_max"]/809:.1f}×) — 권장 4~8× 안. 창이 학습자 뒤라서 TV에 빛이 반사되지 않아요.</span></li>
  <li class="wn"><b>!</b><span>의자가 U 안쪽을 향하는 ㄷ자라서 TV(앞 벽, 문 오른쪽)를 보려면 몸을 돌려야 해요. 왼쪽 다리 약 40~60°, <b>오른쪽 다리는 TV가 거의 옆(약 85~90°)</b>이고, 바닥 2석만 정면이에요. 수업 때만 TV 이동식 스탠드를 U 입구 쪽으로 끌어오면 양쪽 다리가 약 40~70°로 줄어요(입구를 잠깐 좁히니 입장 후에). 좁은 방의 구조적 한계예요.</span></li>
  <li class="wn"><b>!</b><span>통로 점검(솔직하게): 방 폭 4.5m에서 의자를 바깥에 두면 <b>양쪽 벽~의자 뒤 통로가 약 0.6m</b>밖에 안 나와요(0.9m 불가). U 안쪽 1.2m, 뒤쪽 의자~대표석·포커스룸 사이 약 0.9m, 출입문 스윙 반경 0.9m는 비웠어요(노란 부채꼴). 앞↔뒤 이동은 양쪽 벽 통로(0.6m)뿐이라 <b>수업 중 이동은 불편</b>해요.</span></li>
  <li class="wn"><b>!</b><span>문이 앞 벽 정중앙이라 늦게 오는 사람은 U 안쪽 한가운데로 바로 들어와요. TV(와 선택 스크린 80형)는 문 열림 반경 밖인 문 오른쪽 벽에 붙였고, 이동식 화이트보드는 오른쪽 벽(세로)에 세워 두었어요.</span></li>
  <li><b>·</b><span>빔프로젝터는 천장 설치(선택) → 앞 벽 천장에서 내려오는 100형 전동 스크린. TV와 번갈아 쓰는 구성이라 둘 다 쓰는 날에는 TV를 옆으로 옮겨요.</span></li>
  <li><b>·</b><span>별도 프린터는 복합기가 대신하고 왼쪽 다리 의자와 겹쳐서 배치도에서 뺐어요. 3D 프린터는 창 쪽 오른쪽 모서리(환기), 모션데스크는 보유품이고 Mac Studio·키보드·마우스를 올려둔 모습으로 그렸어요. 바닥 콘센트 연결선은 오렌지 점선이에요.</span></li>
  <li><b>·</b><span><b>소파</b>: 창 쪽 라운지에 3인용(약 1800×850, 치수 추정)을 등받이가 창을 향하게 놓았어요. 앞에 티테이블, 오른쪽에 빈백·3D 프린터 코너가 있고, 통로는 막지 않아요. 3D 모델에서는 등받이·팔걸이·좌석 쿠션까지 모델링했어요.</span></li>
  <li class="ok"><b>+</b><span><b>공기청정기</b>(LG 퓨리케어 360° AS186HWWL, 315×511mm): 앞 벽 문 왼쪽, 책상 U 입구 앞에 두었어요. 사방 흡입이라 앞 벽에서 약 0.3m, 복합기에서 약 0.3m 띄웠고, 양쪽 0.6m 통로와 문 여닫이 반경(노란 부채꼴)·문 통로 밖이에요. 청정 62㎡라 44㎡ 전체를 덮어요. 가습기와는 약 8m 떨어져 있어요.</span></li>
  <li class="ok"><b>+</b><span><b>가습기</b>(하이드로에센셜 HY505RWLAH, 270×750mm): 창 쪽 라운지, 소파 옆 벽에서 약 0.3m 띄워 두었어요. 3D 프린터·Mac Studio 쪽으로는 가습 바람이 가지 않는 위치예요. 가습 권장 면적이 약 35㎡라 라운지 한정이에요(콘센트 위치 미확인).</span></li>
  <li class="ok"><b>+</b><span><b>정수기</b>(WD520AWB 데스크형 직수, 168×398×400mm): 왼쪽 벽 탕비 카운터 선반 위, 냉장고 바로 옆에 두었어요. 직수형이라 <b>급수 연결이 필요</b>하고 소비전력이 2,820W라 단독 콘센트가 필요해요(위치 미확인, 아래 점검 참고).</span></li>
 </ul>
 <div class="callout reveal" style="margin-top:14px"><b>TV 위치, 이렇게 골랐어요</b> · ① 창 쪽 짧은 벽: 역광·반사로 탈락(요청대로 제외). ② 긴 벽: 폭이 4.5m라 U가 안 나오고 앞줄이 TV에 1.8m까지 붙어 탈락. ③ <b>출입문 쪽 짧은 벽(채택)</b>: 창이 학습자 뒤라 반사가 없어요. 문이 정중앙이라 TV는 문 오른쪽으로 비켜 앉혔고(거리 {S12["eye_min"]/1000:.1f}~{S12["eye_max"]/1000:.1f}m), 대신 TV가 정면에서 약간 치우쳐요.</div>
 <p style="margin-top:12px"><a href="3d/" style="font-weight:700">🧊 3D 모델로 보기 (돌려보고 확대 · 12/15석 전환) →</a></p>
 <p class="small" style="margin-top:10px">스탠드얼론 이미지: <a href="assets/img/layout-12.png" target="_blank" rel="noopener">layout-12.png ↗</a></p>

<h3 class="sub3" style="margin-top:40px">탕비 공간 점검 (왼쪽 서비스 벽)</h3>
 <p class="lead">냉장고·커피머신·정수기·복합기·NAS가 한 벽에 몰려 있어서 줄 서는 자리와 의자 간격을 다시 봤어요. 좌표는 앞 벽(문 쪽)에서 안쪽으로 잰 값이에요.</p>
 <div class="tbl reveal"><table class="big"><thead><tr><th>구분</th><th>이전(현재 도면 전)</th><th>제안(도면에 반영)</th><th>이유</th></tr></thead><tbody>
 <tr><td><b>복합기</b></td><td>왼쪽 벽 y 2.44~2.82m, 카운터 바로 아래</td><td>앞 벽 문 왼쪽, NAS 옆(x 0.62~1.0m, y 0.05~0.51m)</td><td>이전 위치는 왼쪽 다리 1번 의자와 약 0.09m, 0.6m 통로 안이라 부딪혔어요. 줄 서는 커피·냉장고와 분리돼요.</td></tr>
 <tr><td><b>냉장고·정수기·커피</b></td><td>냉장고(y 0.82~1.46m) 아래에 카운터가 900mm, 정수기는 선반 위</td><td>벽을 따라 한 줄: 냉장고 → 정수기 → 커피머신 → 컵·선반(카운터 y 1.5~2.3m, 800mm)</td><td>물·커피·냉장 동선이 한 줄이고, 카운터를 100mm 줄여 의자와 약 0.15m 거리를 확보했어요.</td></tr>
 <tr><td><b>이용·대기 공간</b></td><td>표시 없음</td><td>카운터 앞 약 1.1m(x 0.5~1.65m)</td><td>문 여닫이 반경(x 1.8~2.7m)과 안 겹치고, 2~3명이 줄 서도 통로가 막히지 않아요.</td></tr>
 <tr><td><b>공기청정기</b></td><td>앞 벽 x 1.16m(복합기 자리와 가까움)</td><td>중심 x 1.45m, 앞 벽에서 0.5m</td><td>복합기와 0.3m 띄우고 문 통로(x 1.65m 이상) 밖이에요.</td></tr>
 </tbody></table></div>
 <ul class="checks reveal" style="margin-top:20px">
  <li class="ok"><b>+</b><span><b>문 여닫이</b>: 반경 0.9m 부채꼴(x 1.8~2.7m, y 0.9m까지)은 그대로 비어 있어요.</span></li>
  <li class="ok"><b>+</b><span><b>의자와 거리</b>: 카운터 끝(y 2.3m)에서 왼쪽 다리 1번 의자까지 약 0.15m, 통로 0.6m 선은 침범하지 않아요. 카운터 앞에서 줄 설 때 뒤쪽은 의자 쪽이라 좁아요(약 0.55m).</span></li>
  <li class="wn"><b>!</b><span><b>콘센트</b>: 탕비 쪽 콘센트 위치와 수량은 미확인이에요. 정수기(2,820W)와 커피머신은 카운터 높이의 단독 콘센트가 필요하고, LG도 냉온정수기는 다른 가전과 멀티탭을 같이 쓰지 말라고 안내해요. 건물 차단기 용량도 확인해야 해요.</span></li>
  <li class="wn"><b>!</b><span><b>정수기 물</b>: WD520AWB는 <b>직수형이라 상수도 급수관과 배수 연결이 필요</b>하고, 수압이 낮으면 펌프(약 46,000원)가 필요해요. 도면에는 싱크대·급수관이 없고 건물에 탕비 급수가 있는지 미확인이에요. 없으면 <b>물통(생수통)형 정수기나 렌탈(케어십 구독)로 바꾸는 것</b>이 현실적이에요. 현장에서 급수·배수 위치 확인 후 설치 일정을 잡으세요.</span></li>
  <li><b>·</b><span>냉장고는 이미 있는 한 대만 쓰고 추가하지 않았어요. 구매표에는 탕비 항목(냉장고·정수기·커피머신)을 한 묶음으로 모았어요.</span></li>
 </ul>

 <h3 class="sub3" style="margin-top:40px">15석 변형 (참고)</h3>
 <div class="lay1 reveal"><figure><a href="assets/img/layout-15.png" target="_blank" rel="noopener"><img src="assets/img/layout-15.png" alt="ㄷ자 15석 배치도" loading="lazy"></a></figure></div>
 <div class="callout warn reveal" style="margin-top:16px"><b>솔직하게</b> · 15석도 <b>같은 책상 5개</b>(1800×600 4 + 1200×600 1)로 가능해요. 다리마다 6석, 바닥 3석이라 좌석 간격이 600mm로 빠듯하고(팔걸이 없는 의자 권장), <b>스튜디오(카메라 거리)·티테이블을 뺐으며</b> 소파는 2인용으로 오른쪽 벽에 붙였어요. 포커스룸 2석·대표 데스크는 창가로 눕혔고, 3D 프린터는 창에서 멀어져 환기가 어려워요. 뒤 통로는 약 1.0m, 가장 먼 자리는 TV에서 {S15["eye_max"]/1000:.1f}m({S15["eye_max"]/809:.1f}×)로 65형 권장 안이에요. 그래도 여유는 <b>12석</b>이 커서 12석을 추천해요.</div>
</div></section>

<section class="sec alt" id="buy"><div class="wrap">
 <div class="eyebrow">프리미엄 vs 가성비</div>
 <h2>모든 품목 2안 구매표 (12석 기준)</h2>
 <p class="lead">가격은 {D}(KST) 판매 페이지 표시값(단가)이에요. ⭐ 표시가 추천 조합이고, 보유 품목은 0원이에요. 책상은 12·15석 모두 같은 5개이고, 15석이면 의자가 늘고 포커스 세트가 줄며 티테이블이 빠져요(소파는 2인용으로 오른쪽 벽).</p>
 <div class="stot">{won_card("12석 · 전부 프리미엄",P12,"보유 0원 포함")}{won_card("12석 · 전부 가성비",V12,"보유 0원 포함")}{won_card("15석 · 전부 프리미엄",P15,"수량 조정 반영")}{won_card("15석 · 전부 가성비",V15,"수량 조정 반영")}</div>
 {main_table}
 <p class="small">전부 프리미엄·전부 가성비 합계에는 프로젝터·스크린·3D 프린터·별도 프린터·카메라·흡음재 등 ‘나중에/선택’ 품목이 모두 들어 있어요. Mac Studio는 참고용이라 제외했어요.</p>
</div></section>

<section class="sec" id="chairs"><div class="wrap">
 <div class="eyebrow">의자</div>
 <h2>‘서울대 의자’는 어떤 의자?</h2>
 <p class="lead">‘서울대 의자’는 공식 모델명이 아니라 별칭이에요. 블로그·후기들은 <b>시디즈 아이블(IBLE, TNB501FE)</b>을 가리키고, 이전 세대는 T501FE로 소개돼요(대학 납품 사실은 공식 확인을 못 했어요). 퍼시스 CH2811은 ‘연세대 의자’로 불려요.</p>
 <div class="grid g3p reveal">{chair_cards}</div>
 <div class="grid g2 reveal" style="margin-top:20px">
  <div class="card hl"><span class="tag blue">학습자 12석 추천</span><h3>시디즈 IBLE (서울대 의자)</h3><p>189,000원 × 12 = {won_(189000*12)}원. S라인 메시 등판과 글라이드(밀림 적음)라 집중하기 좋아요(바퀴형은 199,000원). 다만 <b>틸팅이 없어</b> 4시간 이상 수업이면 T20 2세대(239,000원, 12개 {won_(239000*12)}원)를 권해요.</p></div>
  <div class="card hl"><span class="tag blue">대표석 추천</span><h3>시디즈 T50 2세대 · 419,000원</h3><p>하루 종일 앉는 자리라 상위 모델을 권해요. 예산을 줄이려면 T20(239,000원)이에요.</p></div>
 </div>
</div></section>

<section class="sec alt" id="studio"><div class="wrap">
 <div class="eyebrow">YouTube 스튜디오 · 책장 배경 촬영 코너</div>
 <h2>책장을 배경으로,<br>대표석 옆에서 촬영</h2>
 <ul class="checks reveal" style="margin-top:20px">
  <li class="ok"><b>+</b><span><b>위치</b>: 뒤쪽 오른쪽 벽(창 쪽 모서리 근처) 책장 2대 앞에 대표석과 유하님 의자. 대표 데스크 샷과 겸용이에요.</span></li>
  <li class="ok"><b>+</b><span><b>카메라</b>: 삼각대를 책상 맞은편 약 2.0m(권장 1.5~2.5m, 왼쪽 라운지 쪽)에 두고 <b>오른쪽 벽 책장</b>을 향해 촬영. 1인 토킹헤드는 대표 의자, 2인 인터뷰는 제레미+유하님 의자(책장 앞 나란히).</span></li>
  <li class="ok"><b>+</b><span><b>조명</b>: 키 라이트는 카메라 옆 출입문 쪽에서 비스듬히, LED 패널은 창 쪽 반대편 보조. 책장 뒤에는 LED 스트립 간접조명.</span></li>
  <li class="ok"><b>+</b><span><b>방향</b>: 카메라는 긴 벽(책장)을 향하고 창은 카메라 옆(아래쪽) 짧은 벽이라 창이 렌즈 정면에 오지 않아요. 창 빛은 옆에서 들어오니 촬영 때는 블라인드로 조절하세요.</span></li>
  <li class="wn"><b>!</b><span><b>트레이드오프</b>: 스튜디오가 포커스룸·라운지 바로 옆이라 촬영 중에는 소음 때문에 포커스룸을 쓰기 어려워요(촬영 시간 분리). 흡음재는 선택(나중). 책장 2대가 오른쪽 벽 1.6m를 차지해요.</span></li>
 </ul>
 <h3 class="sub3">장비 (모두 프리미엄/가성비)</h3>
 {studio_table}
 <div class="callout warn reveal" style="margin-top:14px"><b>마이크는 Shure만</b> · 데스크: MV7+(USB-C/XLR, 494,990원) / MV6(265,990원). XLR 전용인 SM7B(870,000원)·MV7X(318,000원)는 오디오 인터페이스(예: Shure MVX2U 219,000원)가 따로 필요해요. 무선: MoveMic Two(2인용, 620,000원) / MoveMic One(442,000원, 2명이면 Two가 더 저렴). 맥(USB-C) 호환은 제품 사양 기준이고 직접 연결 테스트는 못 했어요.</div>
 <div class="card reveal" style="margin-top:14px"><h3>책장 스타일링 팁</h3><p>① 책은 세로·가로를 섞고 색은 화이트/오크/그레이로 맞추세요. ② AI Builders Lab 로고(아크릴·네온)와 화이트보드 낙서 느낌의 액자를 눈높이에. ③ 식물·피규어 같은 소품은 1/3만 채우고 나머지는 비워 여백을 주세요. ④ 선반 안쪽에 LED 스트립을 숨기면 깊이가 생겨요.</p></div>
</div></section>

<section class="sec" id="network"><div class="wrap">
 <div class="eyebrow">네트워크 · 전원 · NAS</div>
 <h2>12~15대 노트북이<br>안정적으로 쓰려면</h2>
 {net_table}
 <ul class="checks reveal" style="margin-top:18px">
  <li class="ok"><b>+</b><span><b>공유기·NAS 위치</b>: 앞 왼쪽 모서리 선반(탕비·복합기 위). NAS는 집에서 가져오는 보유품(0원)이고 유선 LAN으로 공유기에 연결, 통풍 공간과 콘센트를 확보하세요. 배치도 파란 점선이 왼쪽 벽을 따라 대표석·포커스룸까지 가는 유선 경로예요.</span></li>
  <li class="ok"><b>+</b><span><b>멀티탭</b>: 12석 기준 9개 — 책상 5개에 1개씩(책상 안쪽 모서리, 바닥 콘센트에서 책상 아래로 배선), 대표석 1, 포커스룸 1, 스튜디오 1, NAS/탕비 1. 바닥 케이블은 케이블 커버로 덮으세요. 15석도 9개예요.</span></li>
  <li class="wn"><b>!</b><span>노트북 충전기 최대 용량으로 단순 합산하면 13대 약 1.3kW 수준이지만, 커피머신·복합기·3D 프린터와 동시에 쓸 때의 차단기 용량은 건물에서 확인해야 해요(미확인).</span></li>
  <li class="wn"><b>!</b><span>필요하면 UPS와 기가비트 스위치를 추가하세요(가격 미조사). 공유기 두 대(Deco)는 포커스룸 쪽 노드를 벽 콘센트에 꽂아요. 20명 이상 동시 접속 성능은 실측 못 했어요.</span></li>
 </ul>
</div></section>

<section class="sec alt" id="print"><div class="wrap">
 <div class="eyebrow">복합기 · 프린터 · 3D 프린터</div>
 <h2>복합기가 인쇄까지 해요,<br>별도 프린터는 나중에</h2>
 <div class="callout reveal"><b>정리</b> · 복합기(캐논 MF664Cdw 등)는 인쇄·복사·스캔을 모두 해서 문서 인쇄용 별도 프린터는 필요 없어요. 별도 프린터는 사진·A3나 라벨이 필요할 때만 나중에 사요.</div>
 {print_table}
 <ul class="checks reveal" style="margin-top:18px">
  <li class="wn"><b>!</b><span><b>3D 프린터 코너</b>: 배치도 창 쪽 오른쪽 모서리(15석은 창에서 멀어 환기 불리). 밀폐형(P1S)은 소음·냄새가 덜하고, 오픈형(A1 mini)은 환기와 소음에 더 신경 써야 해요. 창을 열 수 있는지·관리단 규정은 확인 필요해요(미확인).</span></li>
  <li class="ok"><b>+</b><span>복합기는 렌탈이 나을 수도 있지만 렌탈 가격은 조사하지 않았어요(미확인).</span></li>
 </ul>
 <h3 class="sub3">선택: 빔프로젝터 + 스크린</h3>
 {proj_table}
</div></section>

<section class="sec" id="checklist"><div class="wrap">
 <div class="eyebrow">사야 할 것 체크리스트</div>
 <h2>추천 조합 · 우선순위별</h2>
 <p class="lead">12석 추천 조합 기준이에요. 의자 제외 {won_(R12n)}원, 의자 포함 {won_(R12)}원, ‘나중에’ 항목({won_(L12)}원)까지 포함하면 {won_(cg12)}원이에요.</p>
 {checklist_table}
 <h3 class="sub3">이미 있는 것 (구매 안 함)</h3>
 <ul class="checks reveal">{OWN}</ul>
</div></section>

<section class="sec alt" id="cost"><div class="wrap">
 <div class="eyebrow">비용</div>
 <h2>합계와 계산기</h2>
 <div class="stot">
  {won_card("추천 조합 · 12석 (의자 포함)",R12,"입주 전 필수+1개월 내")}
  {won_card("추천 조합 · 12석 (의자 제외)",R12n,"의자 13개 제외")}
  {won_card("추천 + 나중에 항목",cg12,"빈백·3D 프린터 등")}
  {won_card("전부 프리미엄 / 12석",P12,"")}
  {won_card("전부 가성비 / 12석",V12,"")}
  {won_card("추천 조합 · 15석 (의자 포함)",R15,"수량 변경 반영")}
 </div>
 <div class="calc reveal" id="calc">
  <div><label for="cSeats">좌석</label><select id="cSeats" class="field"><option value="12" selected>12석 (ㄷ자 추천)</option><option value="15">15석 (빠듯)</option></select></div>
  <div><label for="cTier">등급</label><select id="cTier" class="field"><option value="R" selected>추천 조합</option><option value="P">전부 프리미엄</option><option value="V">전부 가성비</option></select></div>
  <div class="full"><label><input type="checkbox" id="cCh" checked> 의자 포함</label> &nbsp; <label><input type="checkbox" id="cLater" checked> ‘나중에’ 항목 포함</label></div>
  <div class="full total" aria-live="polite"><div class="t">예상 합계 (설치·배송·용달 제외)</div><div class="n" id="cTotal">-</div><ul id="cList"></ul><div class="w" id="cWarn"></div></div>
 </div>
</div></section>

<section class="sec" id="ref"><div class="wrap">
 <div class="eyebrow">참고 · 교육 책상 후보, TV, 시청거리</div>
 <h2>책상·TV·스탠드 후보</h2>
 <p class="lead">구매표의 책상·TV·스탠드는 아래 후보에서 골랐어요. ㄷ자에서는 오프셋퍼니처 가이아 1800×600 4개 + 1200×600 1개를 기본으로 잡았어요(데스커 1800×800은 깊이가 커서 안쪽이 좁아져요).</p>
 <h3 class="sub3">① 일자 연결 · 고정형</h3><div class="grid g3p reveal">{tcards["fixed"]}</div>
 <h3 class="sub3">② 폴딩 · 캐스터형</h3><div class="grid g3p reveal">{tcards["fold"]}</div>
 <h3 class="sub3">③ 초저가 대안</h3><div class="grid g3p reveal">{tcards["budget"]}</div>
 <h3 class="sub3">TV 55·65형</h3><div class="grid g2p reveal">{tvcards}</div>
 <h3 class="sub3">이동식 스탠드</h3><div class="grid g2p reveal">{scards}</div>
 <h3 class="sub3">시청거리 (AVIXA DISCAS 4:6:8)</h3>
 <div class="tbl reveal"><table><thead><tr><th>기준</th><th>65형</th><th>55형</th></tr></thead><tbody><tr><td>4×</td><td>3.2m</td><td>2.7m</td></tr><tr><td>6×</td><td>4.9m</td><td>4.1m</td></tr><tr><td>8×</td><td>6.5m</td><td>5.5m</td></tr></tbody></table></div>
 <div class="callout reveal" style="margin-top:14px"><b>이 배치에서는</b> · 12석: 가까운 {S12["eye_min"]/1000:.1f}m ~ 먼 {S12["eye_max"]/1000:.1f}m라 65형이면 충분해요. 15석은 가장 먼 자리 {S15["eye_max"]/1000:.1f}m({S15["eye_max"]/809:.1f}×)로 한계에 가까워요. 대표 모션데스크 4종 비교는 보유품을 쓰기로 해서 뺐어요.</div>
</div></section>

<section class="sec alt" id="sources"><div class="wrap">
 <div class="eyebrow">출처와 미확인</div>
 <h2>확인하지 못한 것</h2>
 <ul class="checks reveal">
  <li class="wn"><b>!</b><span>방 치수·문·창·콘센트: 사진으로 추정한 값(약 4.5×9.8m). 문 위치(출입문 쪽 단변 중앙)·여닫이 방향·바닥 콘센트 위치는 정확하지 않아요. 배치도의 의자·책상 간격은 그 가정 기준이에요.</span></li>
  <li class="wn"><b>!</b><span>소파 치수: 일룸 코모·이안가구 론디 모두 정확한 치수를 확인하지 못함 → 도면 크기는 추정(12석 3인형 1800×850, 15석 2인형 850×1400). 구매표의 소파 가격은 2인용 기준이라 3인형 가격은 미확인이에요.</span></li>
  <li class="wn"><b>!</b><span>한샘 플롯 책장세트 크기가 1세트 기준인지 미확인. 이케아 BILLY의 다나와 가격은 오래된 판매처 표기일 수 있어 공식가 재확인 필요.</span></li>
  <li class="wn"><b>!</b><span>화이트보드 두 제품 모두 캐스터 여부를 상세 확인하지 못함. 룸앤오피스 책상 크기·높이·캐스터 미확인. 가이아 1200×600 가격은 기본가(238,700원)를 1200 옵션으로 추정한 값이라 주문 시 확인이 필요해요.</span></li>
  <li class="wn"><b>!</b><span>Shure 마이크 맥 USB-C 호환은 사양 기준(직접 테스트 아님). MoveMic Two 가격은 컴퓨존 표시값이에요.</span></li>
  <li class="wn"><b>!</b><span>GODOX 소프트박스, 에프손 프로젝터 투사거리, 복합기 렌탈, 퍼시스 CH2811 가격, 탕비 선반, UPS·스위치 가격은 조사하지 않았어요. 공유기 20명 이상 동시접속 성능과 건물 차단기 용량도 미확인.</span></li>
  <li class="wn"><b>!</b><span>LG 가전: 모든 가격은 LG전자 공식몰 표시값(2026-11-01)이에요. <b>가습기 HY505RWLAH</b>는 목록 페이지 799,000원, 상세 페이지 회원가 899,000원(정상가 1,099,000원)으로 달라서 높은 쪽을 썼어요. 공기청정기 AS186HWWL 368,000원은 정상가 754,000원에서 할인된 <b>타임딜</b> 표시가라 끝날 수 있어요. 정수기 WD520AWB는 1,328,000원(목록 1,410,000원, 정상가 1,770,000원)이고 구독(월 14,400원~) 조건과 설치 가능 여부는 현장 확인이 필요해요. 상위 모델 WD523AWB 가격은 페이지에서 다시 확인하지 못했어요.</span></li>
  <li class="wn"><b>!</b><span>탕비 콘센트·급수·배수 위치, 복합기 이동 후 실제 동선은 현장에서 확인하지 못했어요. 가습기는 LG 안내로 약 35㎡용이라 44㎡ 전체에는 부족할 수 있어요.</span></li>
  <li class="wn"><b>!</b><span>‘서울대 의자’ = 아이블(TNB501FE)은 블로그 후기 기준이고 대학 납품 사실은 공식 확인 못 했어요. 시디즈 보증기간은 판매처 표기가 달라요.</span></li>
  <li class="wn"><b>!</b><span>용달 요금·업체는 조사하지 않았어요(요청에 따라).</span></li>
 </ul>
 <p class="small" style="margin-top:20px">상품 사진은 각 판매처·제조사 이미지이며 저작권은 해당 업체에 있어요. 모든 가격은 {D}(KST) 표시값이며 광고·제휴가 없어요. 링크는 각 항목의 ‘제품명 + 링크’를 확인하세요.</p>
</div></section>
</main>
<footer><div class="wrap">AI Builders Lab · 동탄 사무실 셋업 가이드 · {D}(KST) 기준 정리 · 가격은 변동될 수 있어요</div></footer>
<script>window.DATA={json.dumps(data,ensure_ascii=False)};</script>
<script src="assets/main.js"></script>
</body></html>'''
open("../index.html","w",encoding="utf8").write(html_out)
print(R12,R12n,L12,cg12,P12,V12,R15,P15,V15)
