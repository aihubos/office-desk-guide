import json, html, math
D="2026.11.01"
def won(n): return f"{n:,}"
E=html.escape

# ---------- DATA ----------
tables=[
 dict(id="gaia",cat="fixed",brand="오프셋퍼니처",name="TFS/가이아 일자 연결식 테이블",model="W1800×D600×H720 (1200/1400/1600/1800 선택)",
  price=269500,pl="269,500원 (계산값)",pn=f"퍼스트사무용가구 기본 238,700원 + W1800 옵션 +30,800원. 배송비 별도(착불 0원 표기). 동서가구 판매가 275,000원(쿠폰가 247,500원)도 확인. 확인일 {D}",
  seats=3,img="p-offset-gaia.jpg",spec=[("크기","1800×600×720mm"),("좌석","3인(좌석당 600mm)"),("연결","일자 연결식(기둥 사이 연결)"),("A/S","1년(동서가구 표기)")],
  flags=[("warn","1800 옵션가는 퍼스트 페이지 기준 계산값"),("","바퀴 없음·고정형")],
  links=[("퍼스트사무용가구 ↗","https://www.1gagu.com/goods/goods_view.php?goodsNo=186800931"),("동서가구 ↗","https://www.dongsuhfurniture.co.kr/goods/goods_view.php?goodsNo=37603")],
  credit="사진: 동서가구 상품 이미지"),
 dict(id="desker",cat="fixed",brand="데스커",name="멀티테이블 W1800×D800",model="DSTDA1808 · 1800×800×720",
  price=261000,pl="261,000원 (공식몰 정가)",pn=f"기업회원가 182,700~206,190원 표기. 다나와 최저 222,720원. 확인일 {D}",
  seats=3,img="p-desker-multitable.jpg",spec=[("크기","1800×800×720mm"),("좌석","3인(깊이 800 · 넉넉)"),("옵션","미니서랍 14,000 / 가방걸이 8,500 / 수직배선커버 11,000 / 멀티탭&클램프 55,000원"),("비고","일룸 OEM")],
  flags=[("ok","공식 브랜드 A/S"),("","바퀴 없음·고정형")],
  links=[("데스커 공식 ↗","https://www.desker.co.kr/product/detail/694"),("다나와 ↗","https://prod.danawa.com/info/?pcode=93912152")],
  credit="사진: 데스커 공식몰"),
 dict(id="clecs",cat="fold",brand="현대리바트",name="CLECS 폴딩테이블 3인",model="2000×540×745",
  price=791000,pl="791,000원~",pn=f"공식몰 '~' 표기(옵션에 따라 상이). 확인일 {D}",
  seats=3,img="p-livart-clecs.jpg",spec=[("크기","2000×540×745mm"),("좌석","3인(좌석당 약 667mm)"),("이동","캐스터(앞 이동 / 뒤 잠금)"),("구조","폴딩")],
  flags=[("ok","캐스터+폴딩 확인"),("warn","가격은 '최저 표시가'")],
  links=[("리바트 공식 ↗","https://www.hyundailivart.co.kr/p/P200203264")],credit="사진: 현대리바트 공식몰"),
 dict(id="hanssem",cat="fold",brand="한샘오피스",name="LT-소프트 교육용 테이블",model="3인용 1800×550×740 / 2인용 1400×550×740",
  price=None,pl="가격 비공개 (견적)",pn="공식 페이지에 가격 없음 → 견적 문의 필요. 계산기에서는 제외됩니다.",
  seats=3,img="p-hanssem-ltsoft.jpg",spec=[("크기","3인용 1800×550×740mm"),("좌석","3인 / 2인 모델"),("이동","캐스터 + 브레이크"),("구조","폴딩 · 적재")],
  flags=[("warn","가격 미확인"),("ok","캐스터+폴딩+적재")],
  links=[("한샘오피스 ↗","https://office.hanssem.com/products/meetingspaces/training/lt-soft")],credit="사진: 한샘오피스 공식 페이지"),
 dict(id="koas",cat="fold",brand="코아스",name="FOCUS 2인 테이블 KAFT1501",model="W1500×D550×H720",
  price=513700,pl="513,700원 (정가 650,000원)",pn=f"ggif.kr 표기. 검색 요약에 458,700원도 보여 가격이 변동될 수 있음. 확인일 {D}",
  seats=2,img=None,spec=[("크기","1500×550×720mm"),("좌석","2인(15명이면 8개 필요)"),("A/S","1년"),("선반","별매")],
  flags=[("warn","접이식·바퀴는 제조사 설명 기준, 판매 페이지에서 직접 확인 못함"),("warn","2인용이라 15석 = 8개")],
  links=[("판매 페이지 ↗","https://www.ggif.kr/goods/goods_view.php?goodsNo=1000002235")],credit=""),
 dict(id="roomn",cat="budget",brand="룸앤오피스",name="접이식 테이블 YWD6029",model="1800×600 (높이 정보 없음)",
  price=62690,pl="62,690원 (에누리 최저)",pn=f"에누리 '가격 갱신 {D}' 표기, 배송비 별도 가능. 재질 MDF·스틸.",
  seats=3,img="p-roomnoffice.jpg",spec=[("크기","1800×600mm"),("좌석","3인"),("재질","MDF · 스틸"),("구조","접이식")],
  flags=[("warn","높이·바퀴 정보 확인 못함"),("warn","내구성은 가장 낮을 수 있음")],
  links=[("에누리 ↗","https://price.enuri.com/catalog/106739798")],credit="사진: 에누리 상품 이미지"),
]
desks=[
 dict(id="d_prem",brand="데스커",name="모션데스크 프리미엄 W1600×D800",model="DSDDM1608",price=945000,pl="945,000원",
  motor="듀얼",img="p-desker-premium1600.jpg",spec=[("크기","1600×800mm"),("모터","LINAK 듀얼 · 3단"),("높이","630~1280mm"),("하중","적정 100kg / 최대 130kg")],
  flags=[("ok","듀얼 모터")],links=[("데스커 공식 ↗","https://www.desker.co.kr/product/detail/279")],credit="사진: 데스커 공식몰",pn=f"공식몰 표기가, 확인일 {D}"),
 dict(id="d_plus",brand="데스커",name="모션데스크 플러스 W1600×D700",model="DSDCM1607",price=692000,pl="692,000원",
  motor="싱글",img="p-desker-plus1600.jpg",spec=[("크기","1600×700mm"),("모터","싱글 모터(BEAM)"),("높이","페이지 표에서 확인 못함"),("하중","적정 50kg / 최대 70kg")],
  flags=[("warn","싱글 모터 · 하중 낮음")],links=[("데스커 공식 ↗","https://www.desker.co.kr/product/detail/247")],credit="사진: 데스커 공식몰",pn=f"공식몰 표기가, 확인일 {D}"),
 dict(id="d_newt",brand="일룸",name="뉴트 모션데스크 1400",model="IDM0012A",price=1059000,pl="1,059,000원",
  motor="듀얼",img="p-iloom-newt1400.jpg",spec=[("크기","1424×789mm"),("모터","LINAK 듀얼"),("높이","809~1349mm"),("하중","적정 100kg")],
  flags=[("ok","듀얼 모터"),("warn","상판 1400이라 가장 좁음")],links=[("일룸 공식 ↗","https://www.iloom.com/product/detail.do?productCd=IDM0012A")],credit="사진: 일룸 공식몰",pn=f"공식몰 표기가, 확인일 {D}"),
 dict(id="d_camel",brand="카멜마운트",name="핏쳐 E2 모션데스크 1600",model="1600×750",price=305100,pl="305,100원 (다나와 최저)",
  motor="듀얼",img="p-camel-fitcher-e2.jpg",spec=[("크기","1600×750mm"),("모터","듀얼"),("높이","670~1070mm"),("하중","최대 100kg")],
  flags=[("ok","듀얼 모터 중 최저가"),("warn","높이 범위가 좁음(최대 1070)")],links=[("다나와 ↗","https://prod.danawa.com/info/?pcode=73695098")],credit="사진: 다나와 상품 이미지",pn=f"다나와 최저가 표기, 확인일 {D}"),
]
tvs=[
 dict(id="tv55",brand="삼성전자",name="Crystal UHD KU55UH8000FXKR (벽걸이형) 55형",price=871170,pl="871,170원",img="p-samsung55.jpg",
  spec=[("크기","1225×708×77mm"),("2026년형","4K UHD")],flags=[("warn","VESA는 페이지에서 미확인")],link=("다나와 ↗","https://prod.danawa.com/info/?pcode=122641079"),pn=f"다나와 최저가 표기, {D}"),
 dict(id="tv65w",brand="삼성전자",name="Crystal UHD KU65UH8000FXKR (벽걸이형) 65형",price=1074120,pl="1,074,120원",img="p-samsung65w.jpg",
  spec=[("크기","1444×831×77mm (스탠드 포함 882×222)"),("VESA","200×200mm"),("무게","14.1kg")],flags=[("ok","다리 없는 벽걸이형 → 이동식 스탠드와 궁합")],link=("다나와 ↗","https://prod.danawa.com/info/?pcode=122641155"),pn=f"다나와 최저가 표기, {D}"),
 dict(id="tv65s",brand="삼성전자",name="Crystal UHD KU65UH8000FXKR (스탠드형) 65형",price=1009230,pl="1,009,230원",img="p-samsung65.jpg",
  spec=[("크기","1444×831(882)×77(222)mm"),("VESA","200×200mm"),("무게","14.1kg")],flags=[("warn","다리 분리 후 스탠드 장착 가능 여부는 제조사 확인")],link=("다나와 ↗","https://prod.danawa.com/info/?pcode=122641150"),pn=f"다나와 최저가 표기, {D}"),
 dict(id="tv65lg",brand="LG전자",name="65UA7500ENA 65형",price=845830,pl="845,830원",img="p-lg65.jpg",
  spec=[("크기","1455×841(904)mm"),("연식","2025년형")],flags=[("warn","다나와 359,990원 최저가 표기는 이상값으로 보고 제외")],link=("다나와 ↗","https://prod.danawa.com/info/?pcode=92376488"),pn=f"다른 판매처 845,830~939,000원 중 최저 사용, {D}"),
]
stands=[
 dict(id="s_none",name="스탠드 없음(벽걸이 설치)",price=0,note="벽 구조·설치비는 별도, 가격 미반영"),
 dict(id="s_wall",name="벽걸이 브라켓 (아이존 MTV-64)",price=11030,note="아이존 카테고리 표기가. 사양(고정/틸트)·적합 크기 미확인"),
 dict(id="s_fs64",name="엔산마운트 FS-64B 이동식 스탠드",price=188000,note="공식몰 188,000원"),
 dict(id="s_tfc",name="아이존 TFC-8060 이동형 거치대",price=157500,note="공식몰 157,500원"),
]
stand_cards=[
 dict(name="엔산마운트 FS-64B",pl="188,000원",img="p-nsan-fs64b.jpg",spec=[("적용","40~70형 · TV 40kg"),("VESA","최대 600×400"),("높이","VESA 중심 1200~1500mm"),("기능","바퀴·선반·높이조절")],
  flags=[("ok","65형 가능")],links=[("엔산 공식몰 ↗","https://www.nsan.co.kr/goods/goods_view.php?goodsNo=1000001322")],credit="사진: 엔산마운트 공식몰",pn=f"공식몰 표기가, 무료배송(VIP 제외) · {D}"),
 dict(name="아이존 TFC-8060 이동형 거치대",pl="157,500원",img=None,spec=[("적용","50~100형"),("하중","100kg")],
  flags=[("warn","사진·상세 사양은 카테고리 목록에서 확인 못함")],links=[("아이존 TV거치대 목록 ↗","https://eyezoneind.com/category/tv%EA%B1%B0%EC%B9%98%EB%8C%80/167/")],credit="",pn=f"제조사 몰 목록 표기가 · {D}"),
]

# ---------- HTML helpers ----------
def card(x,price_key="pl",extra_tag=None):
    ph=(f'<div class="ph"><img src="assets/img/{x["img"]}" alt="{E(x.get("brand","")+" "+x["name"])} 상품 사진" loading="lazy" width="720" height="540"></div>' if x.get("img") else '<div class="ph none">상품 사진을 확인하지 못했어요<br>(판매 페이지 링크 참고)</div>')
    pr=x["pl"]; na=' na' if x.get("price",1) is None else ''
    spec="".join(f"<dt>{E(a)}</dt><dd>{E(b)}</dd>" for a,b in x["spec"])
    fl="".join(f'<span class="tag {c}">{E(t)}</span>' for c,t in x.get("flags",[]))
    lk="".join(f'<a class="{"" if i==0 else "g"}" href="{u}" target="_blank" rel="noopener">{E(t)}</a>' for i,(t,u) in enumerate(x.get("links",[x["link"]] if x.get("link") else [])))
    cr=f'<div class="credit">{E(x["credit"])}</div>' if x.get("credit") else ""
    brand=E(x.get("brand","")); model=E(x.get("model",""))
    head=f'<div class="model">{brand}{" · "+model if model else ""}</div>'
    return f'''<article class="card prod reveal">{ph}<div class="bd">{head}<h3>{E(x["name"])}</h3><div class="price{na}">{E(pr)}</div><div class="pnote">{E(x["pn"])}</div><dl class="spec">{spec}</dl><div class="flags">{fl}</div><div class="links">{lk}</div>{cr}</div></article>'''
def grp(items): return "".join(card(i) for i in items)

tcards={k:grp([t for t in tables if t["cat"]==k]) for k in("fixed","fold","budget")}
dcards=grp(desks)
# tv cards need link list
for t in tvs: t["links"]=[t["link"]]
tvcards=grp(tvs)
for s in stand_cards: s["brand"]=""
scards="".join(card(s) for s in stand_cards)
