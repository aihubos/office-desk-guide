import json, html
from legacy import *          # D, won, E, tables, tvs, stand_cards, card, grp, tcards, tvcards, scards ...
import catalog
I=catalog.I
st=json.load(open("layout3_stats.json"))
def q(t,m):
    x=t["q"]
    if len(x)==3: return x[{10:0,12:1,15:2}[m]]
    return x[1 if m==15 else 0]   # 2-tuple (12,15): 10석은 12석과 같은 수량
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
R10=tot_rec(10); R10n=tot_rec(10,False); L10=tot_rec(10,True,True)
R12=tot_rec(12); R12n=tot_rec(12,False); L12=tot_rec(12,True,True)
R15=tot_rec(15); R15n=tot_rec(15,False); L15=tot_rec(15,True,True)
P10,V10=tot_tier("P",10),tot_tier("V",10)
P12,V12,P15,V15=tot_tier("P",12),tot_tier("V",12),tot_tier("P",15),tot_tier("V",15)
# ---- 다이어트: 새로 사는 것 = 책상·의자만. 나머지는 당근·중고 예정(새제품 참고가, 합계 제외)
MAIN=("table","chair_l","chair_c")
MAINI=[i for i in I if i["id"] in MAIN]
def mtot(m,k=None,chairs=True):
    return sum(sub(i[k or i["rec"]],m) for i in MAINI if chairs or i["id"] not in CH)
M10,M12,M15=mtot(10),mtot(12),mtot(15)
MP10,MV10,MP12,MV12,MP15,MV15=mtot(10,"P"),mtot(10,"V"),mtot(12,"P"),mtot(12,"V"),mtot(15,"P"),mtot(15,"V")
RENT=("water",)
NEWREC={"strip":"전기 안전·화재 위험이라 새제품","doorsign":"출입문 로고 인쇄물이라 새로 제작","nameplate":"이름·로고 새로 제작","switch":"네트워크 장비는 새제품이 안전","cctv_cam":"보안 장비는 새제품(펌웨어·보증)","cctv_rec":"저장장치(microSD/NVR)는 새제품"}
DEFI=[i for i in I if i["id"] not in MAIN and i["note"]!="own"]
def dtier(i): return i[i["rec"]] if i["rec"] else i["P"]
DEF_USED=[i for i in DEFI if i["id"] not in NEWREC and i["id"] not in RENT]
DEF_NEW=[i for i in DEFI if i["id"] in NEWREC]
DEF_RENT=[i for i in DEFI if i["id"] in RENT]
def dsum(L,m=10): return sum(sub(dtier(i),m) for i in L)
DU10,DN10=dsum(DEF_USED),dsum(DEF_NEW); DEF10=DU10+DN10
def won_(n): return f"{n:,}"
def link(t):
    if t["u"]: return f'<a href="{t["u"]}" target="_blank" rel="noopener">{E(t["n"])} ↗</a>'
    return f'<span style="font-weight:600">{E(t["n"])}</span>'
def thumb(t):
    return f'<img class="th" src="assets/img/{t["img"]}" alt="{E(t["n"])} 사진" loading="lazy">' if t["img"] else '<span class="th" style="display:flex;align-items:center;justify-content:center;font-size:10px;color:#8B95A1;text-align:center">사진<br>없음</span>'
def tier_rows(items,m=10,flag_rec=True):
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
            price=f'{won_(t["p"])}원<span class="wtxt" style="color:#6B7684">{E(t["src"])}</span>' if t["p"] else ('미정<span class="wtxt" style="color:#6B7684">가격 미확인</span>' if t["src"]=="미정" else '0원<span class="wtxt" style="color:#6B7684">보유</span>')
            out+=f'<tr class="{"recrow" if isrec and flag_rec else ""}"><td>{nm}</td><td><span class="tg {cl}">{lab}{recmark}</span></td><td><div class="pc">{thumb(t)}<div>{link(t)}</div></div></td><td class="num">{price}</td><td class="num">{q(t,m)}</td><td class="num"><b>{won_(sub(t,m))}원</b></td><td>{E(t["why"])}{w}</td></tr>'
        if i["note"] and i["note"]!="own": out+=f'<tr><td colspan="7" class="wtxt" style="background:#FFFAF0">{E(i["note"])}</td></tr>'
    return out
HEAD='<thead><tr><th>항목</th><th>등급</th><th>제품명 + 링크</th><th class="num">가격(단가)</th><th class="num">수량</th><th class="num">소계</th><th>한줄 이유</th></tr></thead>'
main_table=f'<div class="tbl reveal"><table class="big">{HEAD}<tbody>{tier_rows(MAINI,10)}</tbody>'+ \
 f'<tfoot><tr class="grpr"><td colspan="5">10석 · 책상+의자 추천 조합(⭐) 합계 — 새로 사는 것</td><td class="num">{won_(M10)}원</td><td></td></tr>'+ \
 f'<tr class="grpr"><td colspan="5">10석 · 책상+의자 전부 프리미엄 / 전부 가성비</td><td class="num">{won_(MP10)}원 / {won_(MV10)}원</td><td></td></tr></tfoot></table></div>'
def def_row(i,note=""):
    t=dtier(i)
    price=f'{won_(t["p"])}원' if t["p"] else '미정'
    w=f'<span class="wtxt">⚠ {E(t["w"])}</span>' if t["w"] else ""
    nt=f'<span class="wtxt" style="color:#6B7684">{E(note)}</span>' if note else ""
    return f'<tr><td>{E(i["grp"])}</td><td>{E(i["name"])}<span class="wtxt" style="color:#6B7684">{E(i["pri"])}</span></td><td><div class="pc">{thumb(t)}<div>{link(t)}</div></div></td><td class="num">{price}</td><td class="num">{q(t,10)}</td><td class="num"><b>{won_(sub(t,10))}원</b></td><td>{E(t["why"])}{w}{nt}</td></tr>'
DHEAD='<thead><tr><th>구분</th><th>항목</th><th>새제품 참고 제품 + 링크</th><th class="num">새제품 참고가</th><th class="num">수량</th><th class="num">참고 소계</th><th>메모</th></tr></thead>'
def def_sec(title,L,sm,notes=None):
    rows="".join(def_row(i,(notes or {}).get(i["id"],"")) for i in L)
    return f'<tr class="grpr"><td colspan="7">{title} · 새제품 참고 소계 {sm}</td></tr>{rows}'
def_table=f'<div class="tbl reveal"><table class="big">{DHEAD}<tbody>'+def_sec("당근·중고가구점 구매 예정",DEF_USED,won_(DU10)+"원",{"proj":"미니 빔프로젝터를 집에서 가져오므로 구매 불필요할 수 있어요","bean":"빈백은 집에서 가져옴 — 추가로 살 때만","screen":"프로젝터를 쓸 때만 필요"})+def_sec("새제품 권장 (중고 비권장)",DEF_NEW,won_(DN10)+"원",NEWREC)+def_sec("렌탈 예정 — 월 고정비 섹션 참고 (합계 제외)",DEF_RENT,"제외",{"water":"정수기는 렌탈 계약이라 아래 월 고정비 섹션에서 다뤄요. 구매가는 참고용"})+f'</tbody><tfoot><tr class="grpr"><td colspan="5">당근·중고 구매 예정 + 새제품 권장 합계 (새제품 참고가, 메인 합계에 미포함)</td><td class="num">{won_(DEF10)}원</td><td></td></tr></tfoot></table></div>'
studio_rows=tier_rows([i for i in I if i["grp"]=="스튜디오 코너"],10)
studio_table=f'<div class="tbl reveal"><table class="big">{HEAD}<tbody>{studio_rows}</tbody></table></div>'
net_table=f'<div class="tbl reveal"><table class="big">{HEAD}<tbody>{tier_rows([i for i in I if i["grp"]=="네트워크·전원"],10)}</tbody></table></div>'
print_table=f'<div class="tbl reveal"><table class="big">{HEAD}<tbody>{tier_rows([i for i in I if i["id"] in ("mfp","printer","p3d")],10,False)}</tbody></table></div>'
proj_table=f'<div class="tbl reveal"><table class="big">{HEAD}<tbody>{tier_rows([i for i in I if i["grp"]=="선택 장비"],10,False)}</tbody></table></div>'

# ---- checklist (recommended set)
PRI=["입주 전 필수","1개월 내","나중에"]
def checklist(m):
    out=""; grand=0
    for p in PRI:
        rows=[(i,i[i["rec"]]) for i in I if i["id"] in MAIN and i["rec"] and i["pri"]==p]
        if not rows: continue
        s=sum(sub(t,m) for i,t in rows); grand+=s
        out+=f'<tr class="grpr"><td colspan="7">{p} · 소계 {won_(s)}원</td></tr>'
        for i,t in rows:
            k=i["rec"]; lab="프리미엄" if k=="P" else "가성비"
            out+=f'<tr><td><span class="tg {"p" if k=="P" else "v"}">{p}</span></td><td>{E(i["name"])}</td><td><div class="pc">{thumb(t)}<div>{link(t)}<span class="wtxt" style="color:#6B7684">{lab} · {E(t["src"])}</span></div></div></td><td class="num">{q(t,m)}</td><td class="num">{won_(t["p"])}원</td><td class="num"><b>{won_(sub(t,m))}원</b></td><td>{"☐" }</td></tr>'
    return out,grand
cl10,cg10=checklist(10)
cl12,cg12=checklist(12)
own_rows="".join(f'<li><b>{E(i["name"])}</b> — 구매 목록 0원 (보유)</li>' for i in I if i["note"]=="own")+ '<li><b>iPhone</b> — 카메라 대용으로 이미 보유(0원)</li><li><b>Mac Studio</b> — 배치도 참고용(대표석 장비). 합계에 넣지 않음. 애플 코리아 구성 선택 화면에 ₩4,290,000부터 / ₩5,310,000부터 표시(2026.11.01 KST 확인).</li>'
checklist_table=f'<div class="tbl reveal"><table class="big"><thead><tr><th>우선순위</th><th>항목</th><th>제품 + 링크</th><th class="num">수량</th><th class="num">단가</th><th class="num">소계</th><th>구매</th></tr></thead><tbody>{cl10}</tbody><tfoot><tr class="grpr"><td colspan="5">총 합계 (10석 · 추천 조합 · 의자 포함 · 나중에 포함)</td><td class="num">{won_(cg10)}원</td><td></td></tr></tfoot></table></div>'

OWN="".join(f'<li class="ok"><b>✓</b><span>{x}</span></li>' for x in [
 "<b>모션데스크(대표 책상)</b> — 집에 있는 것을 가져옴(보유, 0원). 용달로 운반. 같은 모션데스크 1대를 대표 책상 옆에 더 놓을 거라 <b>구매표에 추가</b>했어요(모델·가격 확인 필요)",
 "<b>NAS</b> — 집에서 가져옴(보유, 0원). 용달로 운반",
 "<b>공유기 (집에 있는 것)</b> — 집에서 가져옴(ASUS RT-BE92U, 보유, 0원). 구매 안 함",
 "<b>iPhone</b> — 카메라 대용(보유, 0원)",
 "<b>로봇청소기</b> — 기존 사무실 것을 가져옴(기존 물품 가져감, 0원). 도크는 창 쪽 두 의자 사이(x 1.25~1.65m)",
 "<b>서진이 책상</b> — 집에서 가져옴(0원). 가벽 바로 뒤 왼쪽 벽에 세로로 세워요(1000×600은 가정)",
 "<b>접이식 책상</b> — 집에서 가져옴(0원). 서진이 책상과는 따로 적었어요(같은 물건이면 알려주세요). 쓸 자리·크기 미정이라 도면에는 없어요",
 "<b>빈백</b> — 집에서 가져옴(0원). 도면에는 자리가 없어요",
 "<b>미니 빔프로젝터</b> — 집에서 가져옴(0원). 가져오면 따로 프로젝터를 살 필요가 없어요",
 "<b>캠핑용품 (품목 확인 예정)</b> — 집에서 가져옴. 구체 품목은 아직 정하지 않았어요",
 "<b>이케아 전등</b> — 집에서 가져옴. 가격은 적지 않았어요",
 "<b>34형 울트라와이드 모니터 + 이동식 스탠드</b> — 기존 물품 가져감(0원). 대표 책상 위(화면 앞면은 창 쪽·남쪽, 뒷면이 출입문 쪽)",
 "<b>Mac Studio</b> — 배치도 참고용이라 합계에 넣지 않았어요. 애플 코리아 구성 선택 화면 표시: ₩4,290,000부터 / ₩5,310,000부터(2026.11.01 KST)"])
# ---- chairs
CHAIRS=[
 dict(n="시디즈 IBLE (아이블, 일명 서울대 의자)",p="189,000원",img="p3-ch-ible.jpg",u="https://kr.sidiz.com/products/ible",spec="S라인 메시 등판 · 틸팅 기능 없음(공식 설명) · 189,000원은 글라이드 프레임 기준, 높이조절형/바퀴 옵션은 199,000원(공식몰 표시)",who="가성비 · 학습자용",why="10개 약 189만원 (바퀴형이면 +10만원)",w="보증기간이 판매처마다 다르게 표시(SSG ‘무상 1년’) — 구매 전 확인"),
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

# ---- 프리미엄 책상·의자 후보 (데스커·일룸, 10석 기준) ----
DK="https://www.desker.co.kr/product/detail/"; IL="https://www.iloom.com/product/detail.do?productCd="
DESKS=[
 dict(brand="데스커",n="컴퓨터데스크 2.0",u=DK+"616",img="desker-616.webp",size="W1200~1800 × D590/700/800 (28mm 상판)",pick="1400×700",unit=207000,qty=10,qn="개인 책상 10대",color="화이트 · 메이플 · 모던아카시아 · 빈티지블랙",pro="최저가 · 배선트레이 · 모니터암 홀 · 28mm 상판",con="D600 규격 없음 · 모션(높이조절) 아님",rec=2,alt="1800×800은 259,000원"),
 dict(brand="데스커",n="모션데스크 플러스",u=DK+"239",img="desker-239.webp",size="W1400/1600 × D700",pick="1400×700",unit=670000,qty=10,qn="개인 책상 10대",color="화이트 · 메이플 · 모던아카시아 · 블랙",pro="LINAK 모터 5년 · 높이 메모리 저장",con="하중 50kg · 컴퓨터데스크의 약 3배 가격",rec=0,alt="1600×700은 685,000원"),
 dict(brand="데스커",n="모션데스크 프리미엄",u=DK+"295",img="desker-295.webp",size="W1400/1600/1800 × D700/800",pick="1800×800",unit=961000,qty=10,qn="개인 책상 10대",color="상세 페이지에서 확인",pro="듀얼모터 · 높이 630~1280mm · 하중 100kg",con="10석 총액 약 1천만원 · 차지하는 면적이 큼",rec=0,alt=""),
 dict(brand="데스커",n="멀티데스크",u=DK+"688",img="",size="1800×800 (22mm 상판)",pick="1800×800",unit=294000,qty=5,qn="2인 공유 5대",color="화이트 · 오크 · 쿨그레이",pro="협업용 · 배선 커버",con="상판 22mm · 높이조절 불가",rec=0,alt=""),
 dict(brand="데스커",n="멀티테이블",u=DK+"694",img="",size="1800×800",pick="1800×800",unit=253000,qty=5,qn="2인 공유 5대",color="화이트 · 오크 · 쿨그레이",pro="저렴 · 스터디용",con="배선트레이 없음",rec=0,alt=""),
 dict(brand="일룸",n="뉴트 홈오피스 모션데스크 1400",u=IL+"IDM0012A",img="iloom-IDM0012A.jpg",size="1424×789 · H809~1349",pick="1400",unit=1059000,qty=10,qn="개인 책상 10대",color="내추럴오크 · 화이트",pro="LINAK 듀얼모터 · 멀티탭 · 파티션",con="최고가 · 10석 약 1,400만원(의자 별도)",rec=0,alt=""),
 dict(brand="일룸",n="뉴트 홈오피스 책상 1400",u=IL+"IDL0007A",img="iloom-IDL0007A.jpg",size="1400 (상세 사이즈는 판매 페이지 확인)",pick="1400",unit=789000,qty=10,qn="개인 책상 10대",color="오크 · 화이트",pro="파티션 · 모니터암 2개 포함",con="높이조절 불가 · 가격 대비 비쌈",rec=0,alt=""),
 dict(brand="일룸",n="엘바 2인용 책상 1800",u=IL+"HSUD018",img="iloom-HSUD018.jpg",size="1800×600 · H725 (22T)",pick="1800×600",unit=349000,qty=5,qn="2인용 5대(=10석)",color="NCC · 애쉬원목 다리",pro="깊이 600이라 ㄷ자 안쪽이 넓음 · 저렴(도면은 데스커 1800×800 기준이라 배치 다시 확인)",con="배선트레이 없음 · 상판 22T",rec=1,alt=""),
 dict(brand="일룸",n="엘바패밀리 1800 (페닉스)",u=IL+"HSUD018F",img="iloom-HSUD018F.jpg",size="1800×800",pick="1800×800",unit=799000,qty=3,qn="3대(12석 기준)",color="노르딕그레이",pro="페닉스 상판(내오염)",con="개인 업무용으로는 부적합",rec=0,alt=""),
 dict(brand="일룸",n="케플러클래식 1500",u=IL+"HSVD015",img="iloom-HSVD015.jpg",size="1500×750",pick="1500×750",unit=599000,qty=10,qn="개인 책상 10대",color="WP",pro="서랍 · 고급스러움",con="가정 서재형 디자인",rec=0,alt=""),
]
CH2=[
 dict(brand="데스커",n="올라운드 HF",u="https://www.desker.co.kr/product/detail/305",img="desker-305.webp",unit=252000,color="화이트쉘 · 블랙쉘",rec=0,note="이전 선택. 시디즈 아이블(189,000원)로 바꿨어요"),
 dict(brand="일룸",n="알렉스",u=IL+"HVCH3900H",img="iloom-HVCH3900H.jpg",unit=219000,color="색상은 판매 페이지에서 확인",rec=1,note="추천 1과 짝"),
 dict(brand="일룸",n="아이핏",u=IL+"HVCH3501HLN",img="iloom-HVCH3501HLN.jpg",unit=379000,color="색상은 판매 페이지에서 확인",rec=0,note=""),
 dict(brand="시디즈",n="T50 2세대",u="https://kr.sidiz.com/products/t50-2",img="sidiz-t50.jpg",unit=439000,color="색상은 판매 페이지에서 확인",rec=0,note="구매표(대표석)에는 419,000원으로 적혀 있어요"),
 dict(brand="일룸",n="올리버 메쉬",u=IL+"HCH290S",img="iloom-HCH290S.jpg",unit=294000,color="색상은 판매 페이지에서 확인",rec=0,note=""),
]
def cand_card(c,kind):
    qty=c.get("qty",10); tot=c["unit"]*qty
    ph=f'<div class="ph"><img src="assets/desks/{c["img"]}" alt="{E(c["brand"]+" "+c["n"])} 공식 상품 이미지" loading="lazy"></div>' if c["img"] else f'<div class="ph none">상품 이미지를 가져오지 못했어요<br><small>판매 페이지에서 확인</small></div>'
    rec=f'<span class="tag blue">⭐ 추천 {c["rec"]}</span>' if c["rec"] else ''
    if kind=="desk":
        info=f'<div class="spec"><span>폭/사이즈</span><b>{E(c["size"])}</b><span>비교 기준</span><b>{E(c["pick"])}</b></div>'
        pn=f'단가 · 10석 기준 {E(c["qn"])} × {won_(c["unit"])}원'+(f' · {E(c["alt"])}' if c["alt"] else '')
        pc=f'<div class="pc2"><div class="ok2"><b>장점</b> {E(c["pro"])}</div><div class="no2"><b>단점</b> {E(c["con"])}</div></div>'
    else:
        info=''
        pn=f'단가 · 10개 × {won_(c["unit"])}원'+(f' · {E(c["note"])}' if c["note"] else '')
        pc=''
    return f'<article class="card prod reveal{" hl" if c["rec"] else ""}">{ph}<div class="bd"><div class="model">{E(c["brand"])} {rec}</div><h3><a href="{c["u"]}" target="_blank" rel="noopener">{E(c["n"])} ↗</a></h3><div class="price">{won_(c["unit"])}<small>원</small></div><div class="pnote">{pn}</div><div class="tot2">10석 합계 <b>{won_(tot)}원</b></div>{info}<p class="small" style="margin:6px 0"><b>색상</b> · {E(c["color"])}</p>{pc}</div></article>'
cand_desks="".join(cand_card(c,"desk") for c in DESKS)
cand_chairs="".join(cand_card(c,"chair") for c in CH2)
REC1=349000*5+219000*10; REC2=207000*10+189000*10
assert REC1==3935000 and REC2==3960000
# ---- 데스커 구성 3안 (2026-11-02 확인 가격)
CHAIR_L=189000; CFG_A=294000*5+CHAIR_L*10; CFG_B=207000*10+CHAIR_L*10; CFG_C=207000*7+670000*3+CHAIR_L*10
assert (CFG_A,CFG_B,CFG_C)==(3360000,3960000,5349000)
assert M10==CFG_A+419000, (M10,CFG_A)
cand_sec=f"""<section class="sec" id="premium"><div class="wrap">
 <div class="eyebrow">프리미엄 후보 · 책상+의자</div>
 <h2>프리미엄 책상·의자 후보<br>(데스커·일룸, 10석 기준)</h2>
 <p class="lead">데스커와 일룸의 정가 기준 후보예요. 책상은 데스커 구성으로 정했어요(위 구매표·합계 기준). 아래는 다른 브랜드·모델 후보예요. 추천 2가지는 책상 + 의자 10개를 묶은 금액이에요.</p>
 <div class="grid g2 reveal">
  <div class="card hl"><span class="tag blue">⭐ 추천 1 · 저렴한 대안</span><h3>일룸 엘바 2인용 1800×600 × 5 + 알렉스 × 10</h3><p>349,000원 × 5 + 219,000원 × 10 = <b>{won_(REC1)}원</b>. 깊이가 600이라 ㄷ자 안쪽이 넓어지는 대신, 지금 도면은 데스커 멀티데스크 1800×800 기준이라 이 책상으로 가면 도면을 다시 그려야 해요.</p></div>
  <div class="card hl"><span class="tag blue">⭐ 추천 2 · 가성비·개인 책상</span><h3>데스커 컴퓨터데스크 2.0 W1400×D700 × 10 + 시디즈 아이블 × 10</h3><p>207,000원 × 10 + 189,000원 × 10 = <b>{won_(REC2)}원</b>. 배선트레이·모니터암 홀이 있는 개인 책상이에요. 개인 책상 10대라 ㄷ자 연결 배치와는 달라서 배치를 새로 짜야 해요.</p></div>
 </div>
 <h3 class="sub3">책상 후보</h3>
 <div class="grid g3p reveal">{cand_desks}</div>
 <h3 class="sub3">의자 후보 (10개)</h3>
 <div class="grid g3p reveal">{cand_chairs}</div>
 <div class="callout reveal" style="margin-top:18px"><b>가격 출처</b> · 2026-11-02(KST) 기준 데스커·일룸·시디즈 공식몰 표시 정가(일부 대리점가 포함)이고 쿠폰·카드 할인, 배송·설치비는 빠져 있어요. 이미지는 각 공식몰 상품 이미지를 저장해 쓴 것이고, 이미지를 못 가져온 상품은 빈 카드로 두었어요. 색상·세부 사양은 구매 전 판매 페이지에서 한 번 더 확인해 주세요.</div>
</div></section>

"""

data=dict(items=[dict(id=i["id"],grp=i["grp"],name=i["name"],pri=i["pri"],rec=i["rec"],own=i["note"]=="own",main=i["id"] in MAIN,chair=i["id"] in CH,
  P=dict(p=i["P"]["p"],q={str(m):q(i["P"],m) for m in (10,12,15)},n=i["P"]["n"]),V=dict(p=i["V"]["p"],q={str(m):q(i["V"],m) for m in (10,12,15)},n=i["V"]["n"])) for i in I])

def won_card(l,n,sm=""): return f'<div class="card reveal"><div class="l">{l}</div><div class="n">{won_(n)}원</div><div class="l">{sm}</div></div>'
S10,S12,S15=st["10"],st["12"],st["15"]

old_html=f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#3182F6">
<title>동탄 사무실 셋업 가이드 · ㄷ자 교육장 + 책장 가벽 대표실 + 구매 체크리스트</title>
<meta name="description" content="동탄 사무실(44.2㎡) 교육장·대표실 셋업: ㄷ자 배치도, 프리미엄/가성비 구매표, 사야 할 것 체크리스트, 입주 준비 할 일.">
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
 <span class="pill">AI Builders Lab · 현대실리콘앨리 동탄 1529호 · 전용 44.2㎡ (약 13.4평) · {D} 기준</span>
 <h1>44.2㎡ 안에 교육장·대표실까지,<br><span class="blue">ㄷ자 배치와 구매 체크리스트</span></h1>
 <p class="sub">10석 ㄷ자(U형) 토론 배치를 기본으로(12·15석도 같은 책상 5개로 가능), 모든 품목을 프리미엄/가성비 2안으로 정리했어요. 입주 준비 할 일(용달 예약 포함)도 맨 위에 넣었어요.</p>
 <div class="stats">
  <div class="stat"><b>10석</b><span>ㄷ자 토론 배치(기본)<br>12·15석도 같은 책상 5개로 가능</span></div>
  <div class="stat"><b>{won_(M10)}원</b><span>책상+의자 합계(10석, 데스커 A + 대표 의자)<br>새로 사는 건 이것뿐</span></div>
  <div class="stat"><b>{won_(DEF10)}원</b><span>나머지 당근·중고 예정(새제품 참고가)<br>메인 합계 제외</span></div>
  <div class="stat"><b>11/5~7</b><span>용달 예약 권장<br>(입주 11/10 화)</span></div>
 </div>
 <a class="cta" href="#todo">입주 준비 할 일 보기</a>
</div></header>
<nav class="nav" aria-label="목차"><div class="navin">
 <a href="#summary">요약</a><a href="#todo">입주 할 일</a><a href="#layout">배치도</a><a href="#buy">구매표</a><a href="#premium">프리미엄 후보</a><a href="#chairs">의자</a><a href="#zone">라운지·대표실·CCTV</a><a href="#studio">촬영 코너(선택)</a><a href="#network">네트워크·전원</a><a href="#monthly">월 고정비·인터넷·정수기</a><a href="#print">복합기·3D</a><a href="#checklist">체크리스트</a><a href="#cost">비용</a><a href="#ref">책상·전자칠판·시청거리</a><a href="#sources">출처·미확인</a>
</div></nav>
<main>

<section class="sec" id="summary"><div class="wrap">
 <div class="eyebrow">한눈에</div>
 <h2>이 공간에 넣을 것들</h2>
 <p class="lead">전용 44.205㎡(약 13.4평) 지식산업센터 사무실에 교육 책상 10석(<b>ㄷ자 상석이 입구 쪽</b>, 12·15석 변형도 같은 책상), 입구 쪽 탕비, 그리고 ㄷ자 열린 쪽 끝에 <b>75형 전자칠판을 바로 붙이고</b>, 그 바로 뒤에 <b>낮은 책장 가벽</b>, 가벽 뒤에 <b>대표실</b>(창 쪽 한 줄: 모션데스크 #2 · 복합기 · 대표 모션데스크)과 서진이 책상을 둬요. 대표는 <b>창 쪽에서 출입문을 정면으로 마주 보게</b> 앉고, 소파는 <b>오른쪽 벽의 펜트리 문 쪽</b>에 붙였어요. 서진이 책상은 가벽 뒤 왼쪽 벽에 세로로 세웠어요. 복합기+NAS·공유기 선반은 대표 책상 바로 옆이고, CCTV 2대도 넣어요. <b>3D 프린터는 창 쪽 오른쪽 문 밖 외부 펜트리의 왼쪽 끝(문 반대편)</b>에 둬요. 로봇청소기와 34형 울트라와이드 모니터는 기존 사무실 것을 가져와요. YouTube 촬영 코너와 포커스석은 이번 배치에서 <b>고정 자리가 없어져 선택·이동식</b>이에요.</p>
 <div class="callout warn reveal"><b>가정한 것</b> · 보내주신 방 사진 3장으로 <b>폭 약 4.5m × 길이 약 9.8m = 44.1㎡의 길쭉한 직사각형</b>을 추정했어요(전용 44.205㎡ 기준, 실측 아님). 한쪽 짧은 벽은 <b>바닥~천장 전면 유리창</b>, 반대쪽 짧은 벽에 <b>출입문</b>(단변 정중앙, 폭 약 0.9m·안쪽 여닫이 가정)이 있어요. 알려주신 대로 <b>창문 쪽 오른쪽(도면 오른쪽 끝)에 열리는 문</b>이 있고 그 밖이 <b>외부 펜트리</b>라고 보고, 문 폭 0.9m·안쪽 여닫이·펜트리 폭 4.5m(사무실 폭과 같음, 확인받음)×깊이 1.3m는 <b>제가 가정한 값</b>이에요. ‘왼쪽·오른쪽’은 도면 이미지 기준이에요(실제 방향이 반대라면 알려주세요). 바닥 콘센트는 방 중간쯤 한쪽 벽 가까이 1개를 대략 표시했어요. 천장형 에어컨은 중앙. <b>실측치가 오면 배치도를 다시 그릴게요.</b></div>
 <div class="callout reveal" style="margin-top:12px"><b>스타일 가정</b> · 애플 사용자(Mac Studio·MacBook), 깔끔한 미니멀·모던, 유튜브 촬영(유하님과 함께), 화이트/오크/그레이 톤, USB-C·맥 호환 장비를 우선했어요.</div>
 <div class="grid g3p reveal" style="margin-top:20px">
  <div class="card"><h3>배치</h3><p>ㄷ자 10석이 기본(12석은 같은 책상에 의자만 늘린 변형). 문을 열면 ㄷ자 상석이 바로 보이고, 전자칠판은 ㄷ자 열린 쪽 끝에 붙여 상석 쪽을 정면으로 봐요. 칠판 바로 뒤가 낮은 책장 가벽(빌리 ×3, 왼쪽 벽에 붙임)이고 가벽 뒤 창 쪽에 대표실(모션데스크 2개 사이에 복합기, 대표석은 출입문 정면)과 서진이 책상이 있고, 소파는 오른쪽 벽(펜트리 문 쪽)에 있어요. 앞↔뒤 이동은 오른쪽 통로로 바로 이어져요. 15석은 통로가 더 빠듯해요.</p></div>
  <div class="card"><h3>보유 → 구매 아님</h3><p>대표 모션데스크, 서진이 책상, 접이식 책상, 빈백, 미니 빔프로젝터, 캠핑용품, 이케아 전등, NAS, iPhone, 로봇청소기, 34형 모니터는 있는 것을 가져와요(0원). 모션데스크·NAS는 용달로 옮겨요(두 번째 모션데스크와 가벽 책장은 새로 사요, 모션데스크 가격은 확인 필요).</p></div>
  <div class="card"><h3>가격</h3><p>모두 {D}(KST) 판매 페이지 표시값. 쿠폰·옵션·배송비에 따라 달라요.</p></div>
 </div>
</div></section>

<section class="sec alt" id="todo"><div class="wrap">
 <div class="eyebrow">입주 준비 할 일 (구매 아님)</div>
 <h2>입주 11/10(화) 전에<br>끝낼 일</h2>
 <div class="todo reveal">
  <div class="it hot"><div class="bx"></div><div><b>용달 부르기 — 11/5(목)~11/7(토) 예약 권장 <span class="tg p">TODO</span></b><p>집→사무실로 옮길 짐: <b>NAS</b>, <b>모션데스크</b>(집에 있는 것), <b>서진이 책상·접이식 책상</b>, <b>빈백</b>, <b>미니 빔프로젝터</b>, <b>캠핑용품</b>(품목 확인 예정), <b>이케아 전등</b>, 그 밖의 짐. 입주일(2026-11-10, 화) 기준으로 3~5일 전에 예약하는 걸 권장해요. 구매 항목이 아니며 업체·요금은 조사하지 않았어요.</p></div></div>
  <div class="it"><div class="bx"></div><div><b>관리단 업종 확인</b><p>지식산업센터는 입주 가능 업종·시설 사용 규정이 있을 수 있어요. 교육장 운영, 촬영 스튜디오, 3D 프린터(소음·냄새), 이삿짐 엘리베이터 사용 시간을 관리단/관리사무소에 확인하세요.</p></div></div>
  <div class="it"><div class="bx"></div><div><b>명패 만들기 <span class="tg p">TODO</span></b><p>출입문용 도어사인에 AI Builders Lab 로고를 넣어 주문하세요(추천: 마플 아크릴 도어사인 11,000원, 영업일 3~6일 출고). 로고 파일은 PNG·JPG 300dpi 이상이 필요해요. 11/10 입주 전에 받으려면 늦어도 11/5까지 주문하는 걸 권해요(제 추정). 대표 책상 명패는 선택이라 구매표에서 나중에로 두었어요. 문구(회사명·직함)와 크기는 <b>미정</b>이에요.</p></div></div>
  <div class="it"><div class="bx"></div><div><b>인터넷 개통 신청 <span class="tg p">TODO</span></b><p>추천은 <b>KT 오피스넷 프리미엄(2.5G) 월 55,000원</b>(3년·VAT 포함)이에요. 신청 전에 건물이 2.5G 인입을 지원하는지, 가능한 개통일을 통신사에 확인하세요. 자세한 비교는 <a href="#monthly">월 고정비</a> 섹션에 있어요. 공유기·NAS 위치(대표 책상 옆 복합기 위 선반)를 정해두면 첫날부터 쓸 수 있어요.</p></div></div>
  <div class="it"><div class="bx"></div><div><b>정수기 설치 신청 + 급수 위치 확인 <span class="tg p">TODO</span></b><p>탕비 카운터(문 왼쪽 앞 벽)에서 <b>수도 급수관·배수 위치·단독 콘센트</b>를 먼저 확인하고(관리사무소 포함), 렌탈이면 입주일(11/10) 전에 설치일을 잡으세요. 자세한 내용은 <a href="#monthly">월 고정비</a> 섹션에 있어요.</p></div></div>
  <div class="it"><div class="bx"></div><div><b>전자칠판 당근 거래 확인</b><p>제노스미디어 CO750LT4K 75형(당근 중고, 150만원). 상태·AS·스탠드 바닥 크기(도면은 가정)·무게 53.8kg 운반 방법을 거래 전에 확인하세요. 링크는 받지 못해 가격·사양은 사용자 제공 값이에요.</p></div></div>
  <div class="it"><div class="bx"></div><div><b>전입/사업자 주소</b><p>사업자 주소지·우편물 주소 이전 절차를 확인하세요(필요 서류는 세무서·관리사무소에서 확인).</p></div></div>
  <div class="it"><div class="bx"></div><div><b>NAS 백업 후 이동</b><p>운반 전 중요한 데이터는 별도로 백업해 두세요. NAS는 이삿짐으로 옮기고 사무실에서 공유기 옆(대표 책상 옆 복합기 위 선반)에 놓아요.</p></div></div>
  <div class="it"><div class="bx"></div><div><b>실측</b><p>방 가로·세로, 문·창문, 콘센트 위치를 재서 알려주시면 배치도를 확정해요.</p></div></div>
 </div>
</div></section>

<section class="sec" id="layout"><div class="wrap">
 <div class="eyebrow">배치도 · 메인</div>
 <h2>ㄷ자(U형) 토론 10석<br>44.2㎡ 배치도</h2>
 <p class="lead">책상 5개를 이어 붙여 <b>끊김 없는 ㄷ자</b>로 만들었어요(데스커 멀티데스크 1800×800 5개: 양쪽 다리 2개씩 + 입구 쪽 상석 1개가 두 다리 끝을 이어요). <b>상석 책상은 두 다리의 한가운데(x 0.95~2.75m, 중심 1.85m)</b>에 좌우 대칭으로 놓았고 <b>ㄷ자 안쪽은 0.7m로 좁혔어요</b>. 막힌 쪽(상석)이 <b>입구 쪽</b>이고 열린 쪽이 뒤쪽이에요. 문 <b>왼쪽에 탕비</b>가 있어요. 방 뒤쪽은 이번에 이렇게 바뀌었어요: <b>① 75형 전자칠판을 ㄷ자 열린 쪽 끝에 바짝 붙여(책상 끝과 약 0.40m) 상석 쪽을 정면으로 보게 했어요 ② 칠판 바로 뒤(약 0.10m)에 낮은 책장(IKEA 빌리 80×28×106cm ×3)을 <b>왼쪽 벽에 붙여</b> 가벽을 세워 교육존과 뒤쪽을 나눴어요(오른쪽은 트임: 약 1.25m까지 소파 쪽으로 열려 있어요) ③ <b>소파(2인 소형)는 오른쪽 벽 펜트리 문 쪽으로 붙였어요</b>(티테이블은 여전히 자리가 없어 뺐어요) ④ 창 쪽에 한 줄로 <b>모션데스크 #2(x 0.05~1.55m) · 복합기(x 1.55~1.93m) · 대표 모션데스크(x 1.93~3.43m)</b>를 놓고 <b>대표가 출입문을 정면으로 보게</b> 앉혔어요(모니터 뒷면이 입구 쪽이라 입구에서 화면이 안 보여요) ⑤ 서진이 책상을 가벽 바로 뒤 왼쪽 벽에 세로로 세웠어요 ⑥ 펜트리 문은 창 쪽 <b>오른쪽</b> 끝이에요.</b> 왼쪽·오른쪽은 모두 <b>도면 이미지 기준</b>(입구가 위, 창이 아래)이에요.</p>
 <div class="lay1 reveal"><figure><a href="assets/img/layout-10.png" target="_blank" rel="noopener"><img src="assets/img/layout-10.png" alt="ㄷ자 10석 배치도 (상석이 양팔 가운데, ㄷ자 끝에 전자칠판, 오른쪽 벽 소파, 창 쪽 대표실에 모션데스크 2개와 복합기)" loading="lazy"></a></figure></div>
 <div class="legend reveal"><span><i style="background:#3182F6;border-radius:50%"></i>학습자 의자</span><span><i style="background:#EBD3AB;border:2px solid #9A7B4F"></i>교육 책상</span><span><i style="background:#FFD9DE;border:2px solid #F04452"></i>가벽 뒤 라운지·대표실</span><span><i style="background:#D4F5DC;border:2px solid #2E9E58"></i>서진이 책상</span><span><i style="background:#FF9F1C"></i>멀티탭(주황 점선=케이블)</span><span><i style="background:#3182F6;opacity:.5"></i>파란 점선=유선 LAN</span><span><i style="background:#7B61FF"></i>빔프로젝터·스크린(선택)</span><span><i style="background:#FF6B6B;opacity:.6"></i>CCTV 시야</span><span><i style="background:#fff;border:2px dashed #7B61FF"></i>점선 = 선택·후보</span></div>
 <ul class="checks reveal" style="margin-top:20px">
 <li class="ok"><b>+</b><span><b>책상 5개</b>: 데스커 멀티데스크 1800×800(구매 예정 모델) 5개를 진짜 크기로 그렸어요. <b>양쪽 다리 2개씩(x 0.7~1.5m, 2.2~3.0m)</b> + <b>입구 쪽 상석 1개(x 0.95~2.75m, y 1.4~2.2m)</b>가 두 다리 끝을 이어요. 상석은 두 다리의 한가운데(중심 x 1.85m)에 좌우 대칭이에요(이전엔 오른쪽으로 치우쳐 있었어요). 안쪽 통로는 <b>0.7m</b>예요(이전 0.9m에서 더 좁혔어요). <b>10석(기본)은 다리마다 4석(간격 900mm) + 상석 2석</b>, 12석은 다리마다 5석(간격 720mm) + 상석 2석, 15석은 다리마다 6석 + 상석 3석(간격 600mm)이에요. 10·12·15석 모두 책상은 같은 5개예요. 멀티데스크는 2인용이라 상석 책상도 2명이 나란히 앉아요. 책상 모서리 이음은 다리 끝을 상석 책상에 붙이는 방식이라 실제 연결 부품은 없고, 배선 트레이가 있어 멀티탭은 책상 안쪽 면에 고정해요(도면 주황색).</span></li>
 <li class="ok"><b>+</b><span><b>전자칠판 75형</b>(제노스미디어 CO750LT4K, 당근 중고 150만원, 패널 1707×1034mm, 스탠드 포함 높이 1840mm, 53.8kg — 판매자 제시 값): <b>ㄷ자 열린 쪽 끝 바로 앞(약 0.40m), 중심 x 1.85m·화면 앞면 y 6.2m</b>에 놓고 화면이 입구 쪽(ㄷ자 상석 방향)을 <b>정면</b>으로 봐요. 스탠드 바닥(1467×520mm, <b>도면 가정값</b>·고정형이라 바퀴 없음으로 봄)까지 점유 영역은 x 1.12~2.58m(패널 x 1.0~2.7m), y 6.2~6.72m예요. <b>칠판 뒤 약 0.10m 틈</b>(y 6.72~6.82m)이 있고 그 뒤가 책장 가벽이라 전원·AV 선을 넣을 수는 있지만 사람이 드나들 폭은 아니에요. 칠판 왼쪽 통로는 벽까지 약 1.0m, 오른쪽은 소파까지 약 0.95m 통로예요. 전동 스크린·빔프로젝터·이동식 화이트보드는 자리가 없어 도면에서 뺐어요(구매표에는 선택 항목으로 남김).</span></li>
 <li class="ok"><b>+</b><span><b>ㄷ자 열린 쪽 끝(책상 끝)↔칠판 약 {S10["u_gap"]/1000:.2f}m</b>는 발표자가 서는 자리이면서 <b>뒤쪽으로 가는 통로</b>이기도 해요. 가장 먼 학습자(상석, 머리 위치)까지 약 {S10["eye_max"]/1000:.1f}m({S10["eye_max"]/1034:.1f}×), 가장 가까운 자리는 {S10["eye_min"]/1000:.1f}m({S10["eye_min"]/1034:.1f}×)예요(15석: {S15["eye_min"]/1000:.1f}~{S15["eye_max"]/1000:.1f}m). 칠판이 U 정면이라 상석·머리 쪽 자리는 거의 정면(최대 약 {S10["view_head_max"]}°, 15석 {S15["view_head_max"]}°)이고, U 다리 쪽 앞자리는 화면을 최대 약 {S10["view_leg_max"]}°(15석 {S15["view_leg_max"]}°) 비스듬히 봐요. <b>칠판에 가장 가까운 다리 쪽 의자는 화면 높이의 2배도 안 되는 거리</b>라 첫 줄 자리는 고개를 많이 돌리고 올려다봐야 해요. 바퀴 달린 스탠드면 수업 때 돌리기 쉬운데 실물은 미확인이에요.</span></li>
 <li class="wn"><b>!</b><span>의자는 U 안쪽을 향하니 칠판을 보려면 몸을 돌려야 해요. 다리 쪽 자리의 회전각은 약 {S10["leg_turn_min"]}~{S10["leg_turn_max"]}°(10석, 15석 {S15["leg_turn_min"]}~{S15["leg_turn_max"]}°), 상석 쪽은 약 {S10["head_turn"]}°예요. 칠판이 ㄷ자 열린 쪽 정면에 있어 <b>직전 판(소파 쪽으로 비스듬히)보다 정면 시청이 좋아졌어요</b> — 대신 소파는 칠판 옆 벽이라 정면 시청용은 아니에요.</span></li>
 <li class="wn"><b>!</b><span>통로 점검(수치, 도면 가정 기준): ① <b>입구 통로</b> 문 열린 폭 0.9m는 그대로 비어 있어요. ② <b>오른쪽 통로</b> 약 1.03m(U 의자 ~ 오른쪽 벽, 이전 0.93m에서 0.1m 넓어짐). ③ <b>U 끝↔칠판 약 0.40m</b>(이전 0.90m에서 0.5m 당겼어요, 발표자가 서는 자리라 사람이 옆으로만 지나가요). ④ <b>칠판 왼쪽 통로</b> 벽까지 약 1.0m, 칠판 오른쪽은 소파(오른쪽 벽)와 약 0.95m 통로. ⑤ <b>가벽 트임</b> 약 1.25m(가벽 오른쪽 끝 x 2.4m ~ 소파 x 3.65m, 이전 2.1m). ⑥ <b>가벽↔창 쪽 책상 줄 통로</b> 약 1.55m(y 7.1~8.65m, 가벽을 입구 쪽으로 0.5m 옮겨 넓어졌어요). ⑦ <b>대표 책상↔오른쪽 벽</b> 약 1.07m라 오른쪽 벽을 따라 <b>창 쪽 오른쪽 펜트리 문</b> 앞(0.9m 부채꼴)까지 갈 수 있어요(대표 책상과 문 반경은 약 0.07m 떨어짐). ⑧ <b>소파 앞</b>은 칠판 오른쪽 끝~소파 사이 약 0.95m 통로예요. <b>소파 모서리(x 3.65m, y 7.77m)↔대표 책상 모서리(x 3.43m, y 8.65m) 약 0.9m</b>가 펜트리 문으로 가는 가장 좁은 곳이라, 소파를 이보다 더 아래(문 쪽)로 내리면 문으로 가는 길이 0.9m 아래로 좁아져요. <b>앞↔뒤 이동</b>은 오른쪽 통로(1.03m)→칠판·소파 사이(0.95m)→가벽 트임(1.25m)→소파 앞 모서리(0.9m)→대표 책상 오른쪽(1.07m)→펜트리 문 앞으로 이어져요(도면 수치 기준, 격자 탐색은 이번에 다시 하지 않았어요). 10·12석 기준이고(10석은 의자 간격이 넓어 앉은 자리 여유가 더 커요) 15석은 의자를 빼 앉으면 오른쪽 통로가 더 줄어요. <b>빠듯한 곳</b>: ⓪ <b>U 안쪽 폭 0.7m</b>라 발표·토론 공간으로는 좁고(이전 0.9m), 왼쪽 의자는 벽에서 약 0.24m라 왼쪽 통로는 없어요. 상석 의자는 문 열림 반경(0.9m) 밖이에요(10·12석 0.14m 이상, 15석 가운데 의자는 약 0.04m 여유). ⓐ <b>대표·모션데스크 #2 의자 등받이가 유리창에 거의 닿아요</b>(약 0.05m), 의자는 옆으로 드나들어요, ⓑ 서진이 의자와 복합기 사이는 약 0.45m, ⓒ 모션데스크 #2 의자(자리2)↔도크 약 0.05m, 도크↔가습기 약 0.16m, ⓓ 창 쪽 책상 줄은 벽에 붙지 않아 전원은 바닥 콘센트·멀티탭 연결이 필요해요(콘센트 위치 미확인).</span></li>
 <li class="ok"><b>+</b><span><b>입구 쪽 상석·회의</b>: 문을 열면 ㄷ자 상석 2석(10·12석 기준)이 바로 보여요. 탕비가 바로 옆이라 커피·물을 가지고 바로 앉고, 냉장고·정수기·커피머신은 문 왼쪽 앞 벽에 한 줄로 붙였어요(복합기는 대표 책상 옆으로 옮겨서 앞쪽 왼쪽 벽은 비었어요). 줄 서는 공간(약 1.13×0.8m)은 문 여닫이 반경 밖이에요. 문에서 전자칠판 화면이 정면으로 보이고, 가벽 뒤 대표실은 칠판·가벽에 일부 가려져요(오른쪽 트임으로는 보여요).</span></li>
 <li><b>·</b><span>빔프로젝터·전동 스크린은 칠판이 U 끝에 있고 바로 뒤가 가벽이라 맞는 투사 방향·스크린 자리가 없어서 <b>도면에서 뺐어요</b>(구매표 ‘선택 장비’에는 남겨 둠). 전자칠판 하나로 가는 구성이에요.</span></li>
  <li><b>·</b><span>별도 프린터는 복합기가 대신해서 뺐고, 복합기+NAS·공유기 선반은 <b>대표 책상 바로 옆(두 모션데스크 사이)</b>으로 옮겼어요. <b>3D 프린터는 창 쪽 오른쪽 문 밖 외부 펜트리(창 벽 전체 폭)의 맨 왼쪽 끝</b>(도면 오렌지 상자, 문 반대편)에 둬요. 문을 오른쪽으로 옮기면서 예전 ‘우측 끝’ 자리는 문 앞을 막아 왼쪽 끝으로 바꿨어요. 외부라 환기·냄새 걱정이 줄지만 실내 전원 연결·겨울 온도·도난은 확인이 필요해요. 모션데스크는 보유품이고 Mac Studio·키보드·마우스를 올려둔 모습이에요. 바닥 콘센트 연결선은 오렌지 점선이에요.</span></li>
 <li><b>·</b><span><b>소파</b>: 창 쪽 책상 줄에 자리를 내려고 <b>오른쪽 벽의 펜트리 문 쪽</b>에 붙였어요(약 850(깊이)×1200, 치수 추정, 10·12·15석 같음, x 3.65~4.5m, y 6.57~7.77m, 등받이가 벽 쪽이고 방 안쪽(서쪽)을 향해요). 칠판 오른쪽 끝과 소파 사이 약 0.95m는 앞↔뒤 통로예요. 펜트리 문 문틀 반경(y 8.9m~)과는 약 1.1m 떨어져 있어 문 열림은 막지 않아요. <b>티테이블은 자리가 없어 도면에서 뺐어요</b>(구매표에는 선택 품목으로 남아 있어요). 소파는 칠판 옆에서 비스듬히 보는 위치예요.</span></li>
  <li class="ok"><b>+</b><span><b>공기청정기</b>(LG 퓨리케어 360° AS186HWWL, 315×511mm): 앞 벽 오른쪽 모서리 근처(중심 x 4.19m, y 1.2m)로 옮겼어요. 문 통로와 오른쪽 통로(1.03m)를 막지 않고, 사방 흡입이라 주변 0.3m를 비웠어요. 청정 62㎡라 44㎡ 전체를 덮어요. 가습기와는 약 8m 떨어져 있어요.</span></li>
 <li class="ok"><b>+</b><span><b>가습기</b>(하이드로에센셜 HY505RWLAH, 270×750mm): 창 쪽 두 의자 사이(중심 x 1.95m, y 9.58m)로 옮겼어요. 도크와 약 0.16m, 대표 의자와 약 0.3m예요. 가습 권장 면적이 약 35㎡라 뒤쪽 구역 한정이에요(콘센트 위치 미확인).</span></li>
 <li class="wn"><b>!</b><span><b>세라믹 식탁 4인(구매표 추가, 도면에는 못 그렸어요)</b>: 크기는 일룸 블릭 1200폭(1196×746mm) 또는 마루이 오클린 1400폭(1400×797mm) 기준이에요. 입구 쪽 탕비·미팅 자리로 보고 놓을 곳을 찾았지만, 통로 0.9m를 지키면서 4인 의자까지 둘 자리가 없었어요. 가장 가까운 후보인 앞 벽 오른쪽 모서리(x 3.0~4.4m, y 0.4~1.2m)는 공기청정기·슬리퍼 랙을 옮겨야 하고, 의자를 빼면 입구에서 오른쪽 통로로 가는 길이 약 0.5m로 막혀요(의자 없이 서서 쓰는 카운터용이면 가능). 탕비 대기 공간(약 1.13×0.8m)은 크기는 맞지만 냉장고·정수기 앞을 막아요. 그래서 <b>구매표에만 넣었고</b>(합계 포함) 후보 자리는 외부 펜트리 가운데(폭 4.5m·깊이 1.3m 가정, 실외라 세라믹 야외 사용 가능 여부는 미확인)예요. 의자 4개는 구매표에 없어요(미정).</span></li>
  <li class="ok"><b>+</b><span><b>마샬 스피커</b>: 책장 가벽 위 왼쪽 끝(도면 x 0.2~0.46m, 높이 1.06m)에 올렸어요. 액톤 III(260×170×150mm)는 책장 깊이 280mm 안에 들어가고, 가까운 왼쪽 벽 콘센트에서 전원을 받아요(콘센트는 미확인). 가성비안 엠버튼 II는 배터리형이라 콘센트가 필요 없어요.</span></li>
  <li class="ok"><b>+</b><span><b>정수기</b>(WD520AWB 데스크형 직수, 168×398×400mm): 문 왼쪽 탕비 카운터 위, 냉장고 바로 옆. 직수형이라 <b>급수 연결이 필요</b>하고 소비전력이 2,820W라 단독 콘센트가 필요해요(위치 미확인, 아래 점검 참고).</span></li>
 </ul>
 <div class="callout reveal" style="margin-top:14px"><b>이번 배치의 이유와 대가</b> · 요청대로 ① 전자칠판을 ㄷ자 끝에 붙이고, ② 칠판 바로 뒤에 낮은 책장 가벽을 <b>왼쪽 벽에 붙여</b> 세우고(조금 밀어 오른쪽을 트임으로), ③ <b>소파는 오른쪽 벽 펜트리 문 쪽</b>으로, ④ 펜트리 문은 오른쪽, ⑤ 대표 책상은 창 쪽에서 출입문 정면으로(옆에 모션데스크 #2와 복합기), ⑥ 서진이 책상은 가벽 뒤 왼쪽 벽에 세로로 배치했어요. 상석은 양팔 가운데에 대칭으로 놓고 ㄷ자 안쪽을 0.7m로 좁혔어요. <b>대가</b>: ⓐ 칠판에 가장 가까운 다리 쪽 의자는 약 {S10["eye_min"]/1000:.1f}m(화면 높이의 {S10["eye_min"]/1034:.1f}배)로 너무 가까워요(화면 최대 약 {S10["view_leg_max"]}° 비스듬), ⓑ 칠판 뒤는 약 0.10m 틈이라 배선 접근이 어렵고 로봇이 못 지나가요, ⓒ 소파는 칠판 바로 옆이라 수업 중엔 소란하면 부담이에요, ⓓ <b>소파가 1.2m 소형</b>이고 티테이블은 뺐어요, ⓔ <b>촬영 코너와 포커스석은 고정 자리가 없어</b> 선택·이동식이고, ⓕ 창 쪽 두 의자 등받이가 유리와 약 0.05m예요, ㄷ자 안쪽 0.7m는 좁아요, ⓖ <b>대표는 출입문을 정면으로 보지만 실제 시선은 전자칠판(높이 약 1.83m)과 U 책상에 가려져요</b>. 모니터 뒷면이 입구 쪽이라 <b>입구에서 화면은 보이지 않아요</b>(이전의 ‘78° 비스듬히 보임’은 이번 배치로 바뀌었어요), ⓗ 이동식 촬영 후보로 쓰던 칠판 오른쪽 빈 공간은 이제 통로와 소파가 차지해요. 칠판 스탠드 크기·펜트리 문·콘센트는 가정값이에요.</div>
 <p style="margin-top:12px"><a href="3d/" style="font-weight:700">🧊 3D 모델로 보기 (돌려보고 확대 · 10/12/15석 전환) →</a></p>
 <p class="small" style="margin-top:10px">스탠드얼론 이미지: <a href="assets/img/layout-12.png" target="_blank" rel="noopener">layout-12.png ↗</a></p>

<h3 class="sub3" style="margin-top:40px">탕비 공간 점검 (입구 왼쪽 앞 벽)</h3>
 <p class="lead">냉장고·정수기·커피머신을 문 왼쪽 앞 벽으로 옮겼어요. 좌표는 왼쪽 벽·앞 벽(문 쪽) 모서리에서 잰 값이에요(모두 도면 가정 기준).</p>
 <div class="tbl reveal"><table class="big"><thead><tr><th>구분</th><th>이전</th><th>이번 배치(도면에 반영)</th><th>이유</th></tr></thead><tbody>
 <tr><td><b>냉장고·정수기·커피</b></td><td>왼쪽 벽을 따라(y 0.8~2.3m)</td><td>앞 벽 문 왼쪽 한 줄: 냉장고(x 0.05~0.61m) → 카운터(x 0.62~1.5m, 깊이 0.6m) 위에 정수기(x 0.66~0.83m)·커피머신(x 0.9~1.32m)·선반</td><td>입구 바로 옆·회의 영역과 가깝고, 카운터 끝(x 1.5m)이 문 열린 폭(x 1.8m)과 0.3m 떨어져요.</td></tr>
 <tr><td><b>이용·대기 공간</b></td><td>왼쪽 벽 카운터 앞</td><td>카운터 앞 x 0.05~1.18m, y 0.69~1.49m(깊이 0.8m, 상석 의자 때문에 이전 1.45m에서 줄었어요)</td><td>문 여닫이 반경(x 1.8~2.7m, y 0.9m까지)과 안 겹쳐요. 2~3명이 줄 서도 입구 통로가 안 막혀요.</td></tr>
<tr><td><b>복합기·NAS 선반</b></td><td>대표 책상 바로 왼쪽(창 쪽, 두 모션데스크 사이)</td><td>x 1.55~1.93m, y 8.65~9.11m, 복합기 380×460 위에 NAS·공유기(ASUS RT-BE92U) 선반</td><td>대표와 모션데스크 #2 자리 둘 다 팔이 닿는 거리예요. 탕비 줄·소음과 분리돼요.</td></tr>
 <tr><td><b>공기청정기</b></td><td>앞 벽 오른쪽 모서리 근처</td><td>중심 x 4.19m, y 1.2m</td><td>문 통로와 오른쪽 통로 밖이고, 탕비 증기·커피 냄새 쪽을 피해요.</td></tr>
 <tr><td><b>비워진 옛 탕비 자리</b></td><td>왼쪽 벽 x 0.05~0.6m, y 0.8~2.3m</td><td>비움. 후보: ① 스타일러(선택, 점선) ② 외투 행거·우산꽂이 ③ 택배·소모품 보관 ④ (포커스석은 이번 배치에 고정 자리가 없어 선택·이동식)</td><td>가구는 추가하지 않았어요. 스타일러 후보와 모델은 아래 ‘스타일러’ 참고.</td></tr>
 </tbody></table></div>
 <ul class="checks reveal" style="margin-top:20px">
  <li class="ok"><b>+</b><span><b>문 여닫이</b>: 반경 0.9m 부채꼴(x 1.8~2.7m, y 0.9m까지)은 그대로 비어 있어요. 입구 통로(폭 0.9m)도 비어 있어요.</span></li>
  <li class="wn"><b>!</b><span><b>의자와 거리</b>: 탕비 대기 공간 끝(x 1.18m)과 상석 왼쪽 의자(x 1.2m~, y 0.94m~)가 거의 닿아(약 0.02m) 줄 서는 사람이 상석 의자 바로 옆에 서요. 줄이 길면 상석이 불편하니 커피 시간을 정하거나 상석을 한 칸 뒤로 옮길 수 있어요.</span></li>
  <li class="wn"><b>!</b><span><b>콘센트</b>: 탕비 쪽 콘센트 위치와 수량은 미확인이에요. 정수기(2,820W)와 커피머신은 카운터 높이의 단독 콘센트가 필요하고, LG도 냉온정수기는 다른 가전과 멀티탭을 같이 쓰지 말라고 안내해요. 건물 차단기 용량도 확인해야 해요.</span></li>
  <li class="wn"><b>!</b><span><b>정수기 물(새 자리에서도 그대로)</b>: WD520AWB는 <b>직수형이라 상수도 급수관과 배수 연결이 필요</b>하고, 수압이 낮으면 펌프(약 46,000원)가 필요해요. 도면에는 앞 벽 쪽 싱크대·급수관이 없고 건물에 탕비 급수가 있는지 미확인이에요. 없으면 <b>물통(생수통)형 정수기나 렌탈(케어십 구독)로 바꾸는 것</b>이 현실적이에요. 현장에서 급수·배수 위치 확인 후 설치 일정을 잡으세요.</span></li>
  <li><b>·</b><span>냉장고는 삼성 RT20FARL3S9(555×1445×637) 한 대만 쓰고, 구매표에는 탕비 항목(냉장고·정수기·커피머신)을 한 묶음으로 모았어요.</span></li>
 </ul>

 <h3 class="sub3" id="zone" style="margin-top:40px">뒤쪽 라운지 · 가벽 · 대표실 · CCTV · 스타일러</h3>
 <p class="lead">10·12·15석은 뒤쪽 구역 배치가 같아요(소파도 2인용으로 통일, 오른쪽 벽 펜트리 문 쪽). 도면은 입구가 위, 창이 아래예요. 방 왼쪽·오른쪽은 도면 이미지 기준이에요.</p>
 <ul class="checks reveal" style="margin-top:12px">
 <li class="ok"><b>+</b><span><b>책장 가벽</b>: IKEA 빌리 80×28×106cm 3개를 <b>칠판 바로 뒤</b> y 6.82~7.10m에 <b>왼쪽 벽에 붙여</b>(x 0~2.4m, 약 2.4m) 나란히 세워요(칠판 스탠드와 약 0.15m, 뒤쪽 서진이 책상과는 약 0.05m). 높이 약 1.06m라 앉은 사람 시선은 가리지 않고 <b>공간 구분용</b>이에요(소리 차단 없음). 오른쪽(x 2.4~3.65m) 약 1.25m는 <b>트임</b>으로 비워 오른쪽 통로에서 대표실·펜트리 문으로 가요. 이케아 안내상 <b>전복 위험이 있어 벽·바닥 고정이 필요</b>한데, 한쪽 끝은 왼쪽 벽에 붙지만 서로 연결·고정 방법은 현장에서 확인해야 해요(미확인). 책이 비치는 쪽은 대표실 쪽(열린 면)이고 뒷판이 칠판 쪽이에요.</span></li>
 <li class="ok"><b>+</b><span><b>대표석</b>(창 쪽 오른쪽 가운데, 책상 x 1.9~3.4m, y 8.5~9.2m, 1500×700 가정): <b>Jeremy는 북쪽(출입문)을 보고 앉아요</b>(의자 x 2.65m·y 9.4m, 출입문 정면 = 단변 중앙 x 2.25m). 34형 모니터는 책상 안쪽 줄(y 8.57m)에서 <b>화면이 남쪽(대표 쪽)</b>을 향하고 <b>뒷면이 입구 쪽</b>이라 입구에서는 화면이 안 보여요. 다만 정면 시선은 중간의 전자칠판·U 책상에 가려져 문 자체는 잘 안 보여요. 창이 대표 등 뒤(남쪽)라 화면 역광은 적지만 등받이와 유리가 약 0.2m라 블라인드·단열 확인이 필요하고, 책상이 벽에 붙지 않아 전원은 바닥 콘센트·멀티탭이 필요해요(미확인). ‘출입문’은 사무실 정문으로 읽었고, 창 쪽 문을 정면으로 보고 싶으면 의자 방향만 바꾸면 돼요.</span></li>
 <li class="ok"><b>+</b><span><b>서진이 책상</b>(가벽 바로 뒤 왼쪽 벽에 세로: x 0.05~0.65m, y 7.65~8.65m, 600×1000 가정, 집에서 가져오는 책상이라 구매 항목 아님): 서진이 의자는 x 0.9m·y 8.15m로 <b>왼쪽 벽을 보고 앉아요</b>. 책상 뒤 모서리가 모션데스크 #2와 거의 이어져요(y 8.65m). 구매표에서는 뺐어요(집에서 가져옴).</span></li>
 <li class="wn"><b>!</b><span><b>촬영 코너·포커스석(고정 자리 없음)</b>: 이전 판의 YouTube 촬영 코너(약 2.3×2.4m)와 포커스석은 칠판·가벽·소파·대표실·통로를 모두 지키면서 놓을 수 없어 <b>고정 자리를 없앴어요</b>. 촬영이 필요할 때만 가벽 뒤 빈 곳에 삼각대·조명을 임시 설치하는 선택이에요. 구매표의 촬영 장비·포커스 장비는 ‘나중에/선택’으로 내렸어요. 빈백·아지트 코너도 자리가 없어 도면에서 뺐어요.</span></li>
 <li class="ok"><b>+</b><span><b>로봇청소기 도크(기존)</b>: 창 쪽 두 의자 사이(x 1.25~1.65m, y 9.42~9.77m)에 둬요. 대표 의자와 약 0.8m, 펜트리 문 반경에서 약 1.8m 떨어져 있어요. 콘센트 위치는 추정이에요. 로봇이 앞쪽으로 나가려면 가벽 트임(1.25m)을 지나야 하고, 칠판 뒤 0.10m 틈은 못 지나가요.</span></li>
 <li class="ok"><b>+</b><span><b>34형 울트라와이드(기존, 이동식 스탠드)</b>: 대표 책상 위 안쪽 줄(x 2.25~3.05m)에 두고 <b>화면이 남쪽(대표 쪽), 뒷면이 출입문 쪽</b>이에요(도면 크기는 가정). 캐스터라 필요하면 U 책상 발표용으로 굴려갈 수 있어요.</span></li>
 <li class="ok"><b>+</b><span><b>CCTV 2대</b>: ‘CCTV 1’은 앞 벽 문 오른쪽 천장 부근(x 2.75m), 입구·탕비 쪽을 향해 시야 약 90°로 문 열린 곳을 봐요. ‘CCTV 2’는 오른쪽 벽 중간(y 4.0m), 책상 U 쪽을 향해 약 70°예요. 대표 책상·서진이 책상·소파 위치가 바뀌어도 시야는 그대로예요. 계산상 시야 부채꼴(도면 빨강)은 y 약 0.1~6.2m 안이라 <b>대표 책상·모션데스크 #2·서진이 책상·대표실·전자칠판·가습기·로봇 도크·34형 모니터는 시야 밖</b>이에요(대표 책상은 약 2.2m 밖). <b>소파는 시야에서 약 1.7m 밖</b>이에요. 다만 <b>전자칠판이 시야 가장자리에 거의 닿아요</b>(약 0.02m 밖, 이전 0.5m — 실제 시야각은 설치 후 확인). 촬영·포커스석은 고정 자리가 없어 해당 없음. 실제 시야각은 설치 후 확인.</span></li>
  <li class="wn"><b>!</b><span><b>개인정보 안내</b>: CCTV를 달면 <b>촬영 안내표지를 눈에 띄게 붙이고, 음성 녹음은 하지 않도록(카메라 앱에서 마이크 끄기)</b> 설정하세요. 직원·수강생이 찍히는 구조라 보관 기간·열람 권한도 정해두세요. 관련 법 조항·안내표지 규격과 가격은 확인하지 않았으니 시설관리사무소·전문가에게 확인하세요.</span></li>
  <li class="ok"><b>+</b><span><b>카메라별 전원·네트워크</b>: Tapo C225는 12V DC 어댑터(콘센트 1개), C110은 AC 어댑터(콘센트 1개)이고 둘 다 Wi-Fi예요. 천장·벽에 달면 콘센트까지 케이블 경로가 필요해요(공유기 커버리지·콘센트 위치는 미확인). 녹화는 카메라 microSD(별도 구매), 클라우드(Tapo Care, 구독), 또는 PoE NVR 구성(VIGI NVR1104H-4P 84,990원, HDD·VIGI 카메라 별도)이 있고, 보유 NAS 녹화는 호환 여부를 확인하지 못했어요.</span></li>
 </ul>
 <div class="callout warn reveal" style="margin-top:14px"><b>스타일러 (고민 중 · 확정 아님)</b> · 후보 위치는 <b>왼쪽 벽, 탕비 냉장고 바로 아래</b>(도면 보라색 점선, x 0.05~0.65m, y 1.05~1.65m)예요. 입구·코트 자리와 가깝지만 <b>전용 콘센트(1,500W급)</b>가 필요하고, 문을 열면 약 1.19m가 필요해서 탕비 대기 공간과 겹쳐요(열 때 줄이 막힘). <b>실제 크기는 추정했던 445×600×1850이 아니라 600(폭)×1965(높이)×620(깊이)mm</b>이에요. 확인한 모델: <b>SC5MBR42</b>(올 뉴 5벌, 83kg) 정상가 1,540,000원·회원가 1,150,000원·쿠폰가 1,120,000원 — <a href="https://www.lge.co.kr/lg-styler/sc5mbr42" target="_blank" rel="noopener">LG전자 페이지 ↗</a> / <b>SC5MBR61S</b>(2026 NEW 5벌+바지 1벌, 85kg, 1,500W, 문 경첩 방향 변경 가능) — 페이지 표시가 판매가 2,191,000원·할인결제가 2,070,000원으로 헷갈려 정확한 가격은 재확인이 필요해요 — <a href="https://www.lge.co.kr/lg-styler/sc5mbr61s" target="_blank" rel="noopener">LG전자 페이지 ↗</a>. 3벌 모델은 확인하지 못했어요. LG 안내에 <b>가정용 설치만 가능(상업용 설치 불가)</b>이라고 적혀 있어 사무실에 설치 가능한지 먼저 문의가 필요해요. 구매표에는 넣지 않았어요.</div>

<h3 class="sub3" style="margin-top:40px">12석 변형 (참고)</h3>
 <div class="lay1 reveal"><figure><a href="assets/img/layout-12.png" target="_blank" rel="noopener"><img src="assets/img/layout-12.png" alt="ㄷ자 12석 배치도" loading="lazy"></a></figure></div>
<div class="callout reveal" style="margin-top:16px"><b>참고</b> · 12석은 10석과 같은 책상 5개에 다리마다 의자 1개씩만 더 놓은 변형이에요(좌석 간격 720mm). 구매표는 의자·슬리퍼만 12개로 늘어요. 아래 계산기에서 10/12/15석을 바꿔 볼 수 있어요.</div>
<h3 class="sub3" style="margin-top:40px">15석 변형 (참고)</h3>
 <div class="lay1 reveal"><figure><a href="assets/img/layout-15.png" target="_blank" rel="noopener"><img src="assets/img/layout-15.png" alt="ㄷ자 15석 배치도" loading="lazy"></a></figure></div>
<div class="callout warn reveal" style="margin-top:16px"><b>솔직하게</b> · 15석도 <b>같은 책상 5개</b>(멀티데스크 1800×800)로 가능해요. 다리마다 6석, 상석 3석이라 좌석 간격이 600mm로 빠듯하고(팔걸이 없는 의자 권장), 소파는 12석과 같은 2인용이에요. 탕비·전자칠판·책장 가벽·소파·대표실·CCTV는 12석과 같아요. 상석 의자 간격은 600mm예요(가운데 의자는 문 열림 반경과 약 0.04m 여유). 오른쪽 통로는 12석과 같은 약 1.03m이며 가장 먼 자리는 전자칠판에서 {S15["eye_max"]/1000:.1f}m({S15["eye_max"]/1034:.1f}×)예요. 그래도 여유는 <b>10석(기본)</b>이 가장 커요.</div>
</div></section>

<section class="sec alt" id="buy"><div class="wrap">
 <div class="eyebrow">프리미엄 vs 가성비</div>
 <h2>구매표 — 새로 사는 건 책상·의자만 (10석 기준)</h2>
 <p class="lead">예산 다이어트로 <b>새로 사는 건 교육 책상·학습자 의자 10개·대표석 의자</b>뿐이에요. 나머지는 최대한 당근·중고가구점에서 구할 거라 아래 별도 표로 옮겼고 <b>메인 합계에 넣지 않았어요</b>. 가격은 {D}(KST) 판매 페이지 표시값(단가)이고 ⭐가 추천 조합이에요. 책상 모델을 아직 고르지 않아서 아래 프리미엄 후보 추천 2가지의 합계를 대안으로 같이 보여줘요.</p>
 <div class="stot">{won_card("데스커 구성 A ⭐ · 책상+의자 10석",CFG_A,"멀티데스크×5 + 아이블×10")}{won_card("데스커 구성 B",CFG_B,"컴퓨터데스크 2.0×10 + 아이블×10")}{won_card("데스커 구성 C",CFG_C,"컴퓨터데스크×7 + 모션데스크 플러스×3 + 아이블×10")}{won_card("새로 사는 합계 (A + 대표 의자)",M10,"구매표·계산기 기준 · 대표 의자 시디즈 T50 포함")}{won_card("대안 · 추천 1 (일룸 엘바+알렉스)",REC1,"프리미엄 후보 · 10석")}{won_card("10석 · 책상+의자 전부 프리미엄",MP10,"현재 구매표 기준")}{won_card("10석 · 책상+의자 전부 가성비",MV10,"현재 구매표 기준")}{won_card("12석 · 책상+의자 추천 조합",M12,"참고")}{won_card("15석 · 책상+의자 추천 조합",M15,"참고")}</div>
 {main_table}
 <h3 class="sub3">당근·중고가구점 구매 예정 (새제품 참고가 · 메인 합계 제외)</h3>
 <p class="small" style="margin-bottom:10px">아래 가격은 새제품 기준 <b>참고가</b>예요. 당근·중고로 구하면 대부분 더 싸고, 실제 금액은 그때그때 달라요. 멀티탭·도어사인·명패·네트워크 장비·CCTV처럼 중고가 안 맞는 항목은 <b>새제품 권장</b>으로 따로 표시했어요(이것도 메인 합계에는 넣지 않았어요). 이미 집에 있는 물건은 아래 ‘이미 있는 것’ 목록이에요.</p>
 {def_table}
 <p class="small">참고가 합계에는 전자칠판·프로젝터·스크린·화이트보드·3D 프린터·별도 프린터·카메라·흡음재·포커스석·티테이블 등 ‘나중에/선택’ 품목도 들어 있어요. 슬리퍼는 가격 미정이라 0원으로 들어갔고, Mac Studio는 참고용이라 제외했어요.</p>
</div></section>

{cand_sec}
<section class="sec" id="chairs"><div class="wrap">
 <div class="eyebrow">의자</div>
 <h2>‘서울대 의자’는 어떤 의자?</h2>
 <p class="lead">‘서울대 의자’는 공식 모델명이 아니라 별칭이에요. 블로그·후기들은 <b>시디즈 아이블(IBLE, TNB501FE)</b>을 가리키고, 이전 세대는 T501FE로 소개돼요(대학 납품 사실은 공식 확인을 못 했어요). 퍼시스 CH2811은 ‘연세대 의자’로 불려요.</p>
 <div class="grid g3p reveal">{chair_cards}</div>
 <div class="grid g2 reveal" style="margin-top:20px">
  <div class="card hl"><span class="tag blue">학습자 10석 추천</span><h3>시디즈 IBLE (서울대 의자)</h3><p>189,000원 × 10 = {won_(189000*10)}원. S라인 메시 등판과 글라이드(밀림 적음)라 집중하기 좋아요(바퀴형은 199,000원). 다만 <b>틸팅이 없어</b> 4시간 이상 수업이면 T20 2세대(239,000원, 10개 {won_(239000*10)}원)를 권해요.</p></div>
  <div class="card hl"><span class="tag blue">대표석 추천</span><h3>시디즈 T50 2세대 · 419,000원</h3><p>하루 종일 앉는 자리라 상위 모델을 권해요. 예산을 줄이려면 T20(239,000원)이에요.</p></div>
 </div>
</div></section>

<section class="sec alt" id="studio"><div class="wrap">
 <div class="eyebrow">YouTube 스튜디오 · 선택·이동식 촬영 코너</div>
 <h2>고정 자리는 없어요,<br>필요할 때만 이동 설치하는 촬영 코너</h2>
 <ul class="checks reveal" style="margin-top:20px">
 <li class="wn"><b>!</b><span><b>위치 변경(정직하게)</b>: 이번 배치에서는 라운지·책장 가벽·대표실·통로 0.9m를 모두 지키면 이전의 약 2.3×2.4m 촬영 코너가 들어가지 않아 <b>고정 자리를 없앴어요</b>. 필요할 때 가벽 뒤 빈 곳에 촬영 책상·삼각대·조명을 임시로 놓고, 끝나면 치우는 방식이에요. 아래 내용은 임시 설치 때의 요령이고 도면에는 표시하지 않았어요(기본 책장 배경은 가벽 책장이 대신할 수 있지만 책이 보이는 열린 면이 소파·대표실 쪽이라 가벽 뒤쪽 면을 배경으로 촬영해야 해요).</span></li>
 <li class="ok"><b>+</b><span><b>카메라</b>: 삼각대를 책상에서 약 1.2m 떨어뜨리고 책장 가벽(대표실 쪽 면)을 배경으로 향해 촬영해요(현장에서 확인 필요). 2인 인터뷰는 두 의자 나란히, 1인 토킹헤드는 한 의자예요.</span></li>
 <li class="ok"><b>+</b><span><b>조명</b>: 키 라이트는 카메라 쪽 위에서 비스듬히, 보조(필) 라이트는 반대편에서 약하게. 책장 가벽 위에 LED 스트립 간접조명을 붙일 수 있어요. 흡음 패널은 선택이에요.</span></li>
 <li class="ok"><b>+</b><span><b>방향</b>: 창이 렌즈 정면에 오지 않게 촬영 방향을 정하고 블라인드로 조절하세요. CCTV는 이 구역을 보지 않아요.</span></li>
 <li class="wn"><b>!</b><span><b>트레이드오프</b>: 촬영 중에는 수업을 같이 하기 어려워요(시간 분리). 임시 설치라 매번 세팅이 필요하고 방음은 안 돼요. 상시 촬영이 필요하면 빈 공간 위치를 다시 상의해야 해요.</span></li>
 </ul>
 <h3 class="sub3">장비 (모두 프리미엄/가성비)</h3>
 {studio_table}
 <div class="callout warn reveal" style="margin-top:14px"><b>마이크는 Shure만</b> · 데스크: MV7+(USB-C/XLR, 494,990원) / MV6(265,990원). XLR 전용인 SM7B(870,000원)·MV7X(318,000원)는 오디오 인터페이스(예: Shure MVX2U 219,000원)가 따로 필요해요. 무선: MoveMic Two(2인용, 620,000원) / MoveMic One(442,000원, 2명이면 Two가 더 저렴). 맥(USB-C) 호환은 제품 사양 기준이고 직접 연결 테스트는 못 했어요.</div>
 <div class="card reveal" style="margin-top:14px"><h3>책장 스타일링 팁</h3><p>① 책은 세로·가로를 섞고 색은 화이트/오크/그레이로 맞추세요. ② AI Builders Lab 로고(아크릴·네온)와 화이트보드 낙서 느낌의 액자를 눈높이에. ③ 식물·피규어 같은 소품은 1/3만 채우고 나머지는 비워 여백을 주세요. ④ 선반 안쪽에 LED 스트립을 숨기면 깊이가 생겨요.</p></div>
</div></section>

<section class="sec" id="network"><div class="wrap">
 <div class="eyebrow">네트워크 · 전원 · NAS</div>
 <h2>10~15대 노트북이<br>안정적으로 쓰려면</h2>
 {net_table}
 <ul class="checks reveal" style="margin-top:18px">
 <li class="ok"><b>+</b><span><b>공유기·NAS 위치</b>: 대표 책상 옆 복합기 위 선반(창 쪽, 두 모션데스크 사이)에 <b>집에서 가져오는 공유기(ASUS RT-BE92U)</b>. NAS는 집에서 가져오는 보유품(0원)이고 유선 LAN으로 공유기에 연결, 통풍 공간과 콘센트를 확보하세요. 배치도 파란 점선은 복합기 선반에서 양옆의 모션데스크 #2·대표석으로 짧게 가고, 서진이 책상까지는 바닥을 따라 약 1.1m 가는 경로예요(경로 가정). 공유기가 뒤쪽 끝으로 가서 앞쪽 책상까지는 약 8m라 Wi-Fi 커버리지는 현장 확인이 필요해요.</span></li>
  <li class="ok"><b>+</b><span><b>멀티탭</b>: 10·12석 기준 11개 — 책상 5개에 1개씩, 대표석 1, 모션데스크 #2 1, 서진이 1, 소파·칠판 1, NAS/복합기 1, 탕비 1(CCTV·로봇 도크·정수기 등은 별도 콘센트). 바닥 케이블은 케이블 커버로 덮으세요. 15석도 11개예요.</span></li>
  <li class="wn"><b>!</b><span>노트북 충전기 최대 용량으로 단순 합산하면 13대 약 1.3kW 수준이지만, 커피머신·복합기·3D 프린터(외부 펜트리, 전원 인입 방법 미확인)와 동시에 쓸 때의 차단기 용량은 건물에서 확인해야 해요(미확인).</span></li>
  <li class="wn"><b>!</b><span><b>집에서 가져오는 공유기 ASUS RT-BE92U는 LAN 포트가 2.5G × 3개뿐</b>이에요. NAS + 복합기 + 대표석 유선 장비만 해도 꽉 차므로 더 필요하면 <b>소형 스위칭 허브</b>(가격 TBD, 구매표에 미정으로 추가)를 쓰세요. 전자칠판(CO750LT4K)은 LAN이 없는 모델이라 Wi-Fi 전용이에요(Jeremy 확인값). UPS도 선택(가격 미조사). 단일 공유기라 뒤쪽 대표실·라운지(약 8~9m)까지 신호가 충분한지는 미검증이고, 메시 지원 표기가 있어 부족하면 추가 노드를 고려하세요. 20명 이상 동시 접속 성능도 실측 못 했어요.</span></li>
 </ul>
</div></section>

<section class="sec alt" id="monthly"><div class="wrap">
 <div class="eyebrow">월 고정비 · 설치 확인 (일회성 구매 합계에는 넣지 않았어요)</div>
 <h2>인터넷 회선과<br>정수기 설치</h2>
 <h3 class="sub3">① 사무실 인터넷 — 3년 약정 · 월 요금 · VAT 포함 (2026-11-02 KST 확인)</h3>
 <div class="tbl reveal"><table class="big"><thead><tr><th>통신사·상품</th><th>500M</th><th>1G</th><th>2.5G</th><th>5G / 10G</th><th>고정IP · Wi-Fi · 설치비</th></tr></thead><tbody>
 <tr><td><b>KT 오피스넷</b><br><a href="https://enterprise.kt.com/pd/P_PD_NW_GI_003.do" target="_blank" rel="noopener">KT 공식 요금표</a></td><td>44,000원<br>(베이직)</td><td>49,500원<br>(에센스)</td><td><b>55,000원</b><br>(프리미엄)</td><td>77,000원 / 110,000원</td><td>고정IP 1개당 추가: 500M 49,500 · 1G 55,000 · 2.5G 60,500 · 5G 82,500 · 10G 115,500원. 모뎀 임대 3년 약정 무료. 설치 출동비 36,000원(야간·주말 45,000원). 오피스넷 Wi-Fi는 별도 상품이라 요금 <b>미정</b>.</td></tr>
 <tr><td><b>SK브로드밴드 GigaBiz</b><br><a href="https://biz.skbroadband.com/page.do?menu_id=P05010000" target="_blank" rel="noopener">SKB 기업 공식 요금표</a></td><td>44,000원<br>(라이트)</td><td>49,500원</td><td>55,000원<br>(프리미엄: 이용 속도 최대 1G, 단말 WAN 포트 2.5G)</td><td>제공 안 함</td><td>고정IP 추가: 500M 49,500 · 1G 55,000 · 프리미엄 55,000원. GigaWiFi 공유기 임대 월 3,300원(설치비 11,000원은 인터넷 동시 가입 시 면제). 인터넷 설치비는 페이지에 없어 <b>미정</b>.</td></tr>
 <tr><td><b>LG U+ 소호 인터넷</b><br><a href="https://www.lguplus.com/internet-iptv/soho/internet-plan/1000003021" target="_blank" rel="noopener">U+ 공식 소호 요금</a></td><td>33,000원<br>(온라인 31,350)</td><td>38,500원<br>(온라인 36,300)</td><td>45,100원 (대리점 유비즈 표기, 공식 소호 페이지에서는 확인 못함)</td><td>소호 요금표에 없음</td><td>설치비 36,300원(첫 달 합산, 야간·주말 25% 할증). <b>일일 제공량 초과 시 100Mbps로 제한</b>(500M 150GB, 1G 300GB, 2.5G 400GB). 고정IP는 소호 페이지에 없어 <b>미정</b>.</td></tr>
 <tr><td><b>LG U+ 오피스넷</b><br><a href="https://www.lguplus.com/biz/all/telecom/internet-cctv/officenet/B000000005" target="_blank" rel="noopener">U+ 공식 오피스넷</a></td><td>44,000원</td><td>49,500원</td><td>55,000원</td><td>77,000원 / 110,000원</td><td>고정IP 표기(유동IP와 함께 필수): 500M 49,500 · 1G 60,500 · 2.5G 60,500 · 5G 77,000 · 10G 115,500원. 페이지의 ‘고정’ 요금이 추가분인지 합계인지 불명확해 상담 확인. 설치비 <b>미정</b>.</td></tr>
 </tbody></table></div>
 <ul class="checks reveal" style="margin-top:18px">
  <li class="ok"><b>+</b><span><b>추천: KT 오피스넷 프리미엄(2.5G), 월 55,000원 + 설치 출동비 36,000원(1회)</b>. 3개 통신사의 2.5G가 같은 월 55,000원 선이라, 최대속도를 2.5G로 표기하고, 3년 약정 시 모뎀 임대료가 없으며, 설치 출동비가 공개된 KT로 골랐어요(SK 프리미엄은 이용 속도 1G로 표기). 10~15명 노트북과 유튜브 업로드에는 1G(49,500원)로도 충분할 가능성이 크지만 월 5,500원 차이라 2.5G를 권해요. 공유기 ASUS RT-BE92U는 2.5G/10G 포트가 있어 그대로 받아요(10G 회선은 월 110,000원이라 지금은 과해요).</span></li>
  <li class="wn"><b>!</b><span>오피스넷 같은 기업 회선은 대역폭을 나눠 쓰는 공유형일 수 있어요(상품 약관 확인 필요). 업로드 속도는 요금표에 별도 표기가 없어 <b>미정</b>이고, 유튜브 업로드가 많은 날의 실제 속도는 개통 후 측정해야 해요. 건물 인입 설비가 2.5G를 지원하는지는 주소별 확인이 필요하고, 안 되면 KT 에센스(1G)로 내려가요.</span></li>
  <li class="wn"><b>!</b><span><b>고정IP는 필요할 때만</b>: NAS·CCTV를 밖에서 직접 접속할 때만 필요해요(KT 2.5G 기준 월 60,500원 추가). 없이 쓰려면 공유기 DDNS 같은 대안이 있지만 이 사무실에서의 동작은 확인하지 못했어요. Wi-Fi는 ASUS 공유기를 쓰므로 통신사 Wi-Fi 임대는 넣지 않았어요. 3D 프린터는 트래픽이 작아 회선 선택에 영향이 없어요(인터넷 요금제는 모든 사용자 합계로 봄).</span></li>
  <li class="ok"><b>+</b><span><b>월 고정비 추가분</b>: 인터넷 월 55,000원(추천안) · 정수기 렌탈을 고르면 아래 월 요금이 더해져요. 이 값은 위쪽 구매 합계·계산기에 들어가지 않아요. 개통까지 걸리는 기간은 확인하지 못해 <b>미정</b>이에요(통신사에 문의).</span></li>
 </ul>
 <h3 class="sub3" style="margin-top:40px">② 정수기 — 렌탈 vs 구매 (자리는 도면의 탕비 카운터 그대로: 폭 168mm 자리, 문 왼쪽 앞 벽)</h3>
 <div class="tbl reveal"><table class="big"><thead><tr><th>제품</th><th>렌탈 월 요금</th><th>구매가</th><th>설치·조건</th></tr></thead><tbody>
 <tr><td><b>코웨이 아이콘 정수기3</b> CHP-7220N (160×368×385mm, 카운터형 직수 냉온정)<br><a href="https://www.coway.com/product/detail?optno=2&amp;prdno=1384" target="_blank" rel="noopener">코웨이 공식 상품 페이지</a></td><td>5년 자가관리 32,900원 · <b>방문관리 35,900원</b><br>6년 30,900원 / 33,900원 · 3년 35,900원 / 38,900원</td><td>일시불 1,310,000원</td><td>등록·설치비 10만원 면제. 5년 렌탈 총액 방문관리 2,154,000원(일시불의 1.6배, 방문관리·AS 포함). 월 요금·일시불은 검색 요약에 나온 코웨이 렌탈샵 표기값이고 공식 페이지 본문에서 직접 확인하지 못해 계약 전 재확인이 필요해요. 코웨이닷컴 페이지에서 폭 16cm는 확인.</td></tr>
 <tr><td><b>SK매직 초소형 라이트 직수</b> WPU-JAC125S (카운터형)<br><a href="https://www.skmagic.com/goods/indexGoodsDetail?goodsId=G000069527" target="_blank" rel="noopener">SK매직몰</a></td><td>SK매직몰 3년 의무 34,900원(셀프관리) · 렌탈 대행몰 표기 26,400원(조건 상이)</td><td>다나와 1,228,990원 · 에누리 918,960원 · 3년 필터 포함 906,400원(오늘의집)</td><td>구매 가격이 몰마다 300,000원 넘게 달라 조건(필터 포함 여부)이 다른 것으로 보여요. 확정가 <b>미정</b>.</td></tr>
 <tr><td><b>LG 퓨리케어 슬림스탠드</b> WS511SH (260×1,158×467mm, 바닥 설치형)<br><a href="https://www.lge.co.kr/product/care-solutions/water-purifiers/ws511sh" target="_blank" rel="noopener">LG전자 공식</a></td><td>72개월 26,000원 · 60개월 28,700원 · 48개월 33,200원 (방문 6개월 · LG 공식판매점 표기)</td><td>공식 페이지에 구매가 없음 → <b>미정</b> (구독만 표시, 구매 시에도 케어십 필수)</td><td>바닥에 서는 모델이라 지금의 카운터 자리에는 안 맞아요(자리를 바꿀 때만 후보). 설치비 무료(싱크대 타공·펌프 등 추가 작업은 별도). 중도 해지 위약금은 잔여 요금의 30·20·10%(1년·2년 기준).</td></tr>
 <tr><td><b>구매표의 현재 안: LG WD520AWB</b> (168×398×400mm, 카운터형)</td><td>렌탈 요금 <b>미정</b>(조회 못함)</td><td>1,328,000원 (구매표에 이미 합산)</td><td>구매하면 LG 케어십(필터 교체) 가입이 필수라 월 비용이 생기지만 금액은 <b>미정</b>이에요.</td></tr>
 <tr><td><b>청호나이스 직수형 냉온정수기</b></td><td><b>미정</b>(직수형 요금 확인 못함. 참고로 업소용 탱크형은 19,900~25,900원 표기)</td><td><b>미정</b></td><td>직수형 모델·가격은 조사하지 못했어요.</td></tr>
 </tbody></table></div>
 <ul class="checks reveal" style="margin-top:18px">
  <li class="ok"><b>+</b><span><b>추천(렌탈을 택한다면): 코웨이 아이콘 정수기3 방문관리 5년, 월 35,900원</b>. 폭 160mm라 도면의 168mm 자리(문 왼쪽 앞 벽 카운터)에 그대로 들어가고, 10~15명이 쓰므로 필터·살균을 방문관리로 맡기는 쪽이 편해요. 렌탈로 가면 구매표의 LG WD520AWB(1,328,000원)를 빼야 해서, 합계는 그만큼 줄어요(이번에는 합계에서 빼지 않았어요). 5년 안에 쓰는 총액만 보면 구매가 싸지만(일시불 1,310,000원 vs 렌탈 5년 2,154,000원) 필터·AS 비용이 구매 쪽에 따로 들어서 어느 쪽이 싼지는 확정하지 못했어요.</span></li>
  <li class="wn"><b>!</b><span><b>직수형이라 급수관(상수도) 연결이 필수</b>예요. LG 안내 기준으로 상수도만 가능(지하수·조리수 불가), 냉온정수기는 <b>단독 콘센트</b>(커피머신·냉장고와 멀티탭 공유 금지), 싱크대·카운터 타공(전원·급수 호스), 얼음·고온살균 모델은 배수 연결이 필요하고, 수압이 낮으면 펌프가 필요해요. 타공·펌프·차단기는 추가 설치비가 생길 수 있어요.</span></li>
  <li class="wn"><b>!</b><span><b>탕비 쪽 급수 확인 (입주 전 현장 체크)</b>: ① 문 왼쪽 앞 벽 카운터(x 0.62~1.5m) 근처에 상수도 급수 밸브가 있는지 ② 배수구가 있는지 ③ 단독 콘센트 위치 ④ 수압 ⑤ 관리사무소의 공사·타공 허가. 지금까지 이 위치의 급수·배수·콘센트는 현장에서 확인하지 못했어요. 급수가 멀면 호스 연장 또는 공사비가 더 들 수 있어요.</span></li>
  <li class="wn"><b>!</b><span><b>설치 기간</b>: LG 구독 페이지는 전문기사 설치로 내일(11/3)부터 12/3까지 날짜 지정이 가능하다고 표시해요(오후 3시 이전 구독 시 다음 날 배송). 코웨이·SK매직은 대리점 글 기준으로 보통 접수 후 2~5영업일이지만 공식 확인은 못 했어요. 입주일 11/10 전에 쓰려면 늦어도 11/5(목)까지 신청하고, 현장 급수 위치를 같이 확인해 달라고 요청하세요(날짜는 제 추정).</span></li>
 </ul>
 <p class="small" style="margin-top:14px">월 요금은 모두 부가세 포함·프로모션에 따라 변동되는 표시값이고 계약 전 재확인이 필요해요. 통신사 공식 페이지 값은 검색 결과에 나온 표기를 따랐어요.</p>
</div></section>

<section class="sec alt" id="print"><div class="wrap">
 <div class="eyebrow">복합기 · 프린터 · 3D 프린터</div>
 <h2>복합기가 인쇄까지 해요,<br>별도 프린터는 나중에</h2>
 <div class="callout reveal"><b>정리</b> · 복합기(캐논 MF664Cdw 등)는 인쇄·복사·스캔을 모두 해서 문서 인쇄용 별도 프린터는 필요 없어요. 별도 프린터는 사진·A3나 라벨이 필요할 때만 나중에 사요.</div>
 {print_table}
 <ul class="checks reveal" style="margin-top:18px">
  <li class="wn"><b>!</b><span><b>3D 프린터 코너</b>: <b>창 쪽 오른쪽 문 밖 외부 펜트리(창 벽 전체 폭)의 맨 왼쪽 끝</b>(도면 오렌지 상자, 문 반대편이라 문 앞을 막지 않아요). 외부 공간이라 환기·냄새는 덜 걱정돼요. 밀폐형(P1S)은 소음·냄새가 더 적고, 오픈형(A1 mini)은 외부라도 비·먼지·온도(겨울 저온)에 신경 써야 해요. 펜트리 깊이(1.3m 가정; 폭 4.5m는 사무실 폭과 같다고 확인)·콘센트·관리단 규정·분실/도난은 확인 필요해요(미확인).</span></li>
  <li class="ok"><b>+</b><span>복합기는 렌탈이 나을 수도 있지만 렌탈 가격은 조사하지 않았어요(미확인).</span></li>
 </ul>
 <h3 class="sub3">선택: 빔프로젝터 + 스크린 (이번 도면에서는 제외)</h3>
 {proj_table}
</div></section>

<section class="sec" id="checklist"><div class="wrap">
 <div class="eyebrow">사야 할 것 체크리스트</div>
 <h2>새로 살 것 · 책상과 의자</h2>
 <p class="lead">예산 다이어트로 <b>새로 사는 건 책상과 의자뿐</b>이에요(10석 추천 조합 {won_(M10)}원). 나머지 품목은 당근·중고가구점에서 구할 예정이라 구매표 섹션의 별도 표(새제품 참고가 {won_(DEF10)}원, 합계 제외)로 옮겼어요. 12석이면 책상+의자가 {won_(M12)}원이에요.</p>
 {checklist_table}
 <h3 class="sub3">집에서 가져올 물건 · 이미 있는 것 (구매 안 함)</h3>
 <ul class="checks reveal">{OWN}</ul>
</div></section>

<section class="sec alt" id="cost"><div class="wrap">
 <div class="eyebrow">비용</div>
 <h2>합계와 계산기</h2>
 <div class="stot">
  {won_card("데스커 구성 A ⭐ · 10석",CFG_A,"멀티데스크×5 + 아이블×10")}{won_card("새로 사는 합계 · 10석 (A + 대표 의자)",M10,"구매표·계산기 기준")}
  {won_card("대안 · 추천 1 · 10석",REC1,"일룸 엘바 2인용×5 + 알렉스×10")}
  {won_card("데스커 구성 B · 10석",CFG_B,"컴퓨터데스크 2.0×10 + 아이블×10")}{won_card("데스커 구성 C · 10석",CFG_C,"컴퓨터데스크×7 + 모션데스크 플러스×3 + 아이블×10")}
  {won_card("당근·중고 예정 (새제품 참고가)",DEF10,"메인 합계 제외 · 중고면 더 낮아요")}
  {won_card("책상+의자 전부 프리미엄 / 10석",MP10,"")}
  {won_card("책상+의자 전부 가성비 / 10석",MV10,"")}
  {won_card("책상+의자 추천 · 12석",M12,"참고")}
  {won_card("책상+의자 추천 · 15석",M15,"참고")}
 </div>
 <div class="calc reveal" id="calc">
  <div><label for="cSeats">좌석</label><select id="cSeats" class="field"><option value="10" selected>10석 (ㄷ자 기본)</option><option value="12">12석</option><option value="15">15석 (빠듯)</option></select></div>
  <div><label for="cTier">등급</label><select id="cTier" class="field"><option value="R" selected>추천 조합</option><option value="P">전부 프리미엄</option><option value="V">전부 가성비</option></select></div>
  <div class="full"><label><input type="checkbox" id="cCh" checked> 의자 포함</label> &nbsp; <label><input type="checkbox" id="cLater"> 당근·중고 예정 항목(새제품 참고가)도 포함</label></div>
  <div class="full total" aria-live="polite"><div class="t">예상 합계 (설치·배송·용달 제외)</div><div class="n" id="cTotal">-</div><ul id="cList"></ul><div class="w" id="cWarn"></div></div>
 </div>
</div></section>

<section class="sec" id="ref"><div class="wrap">
<div class="eyebrow">참고 · 교육 책상 후보, 전자칠판, 시청거리</div>
<h2>책상·전자칠판 후보</h2>
<p class="lead">구매표의 책상은 아래 후보에서 골랐어요(TV·이동식 스탠드는 전자칠판으로 대체해 구매표에서 뺐어요. 전자칠판은 ㄷ자 끝에 정면으로). ㄷ자 도면은 데스커 멀티데스크 1800×800 5개 기준이에요(상석을 양팔 가운데에 놓고 ㄷ자 안쪽은 0.7m로 좁혔어요).</p>
 <h3 class="sub3">① 일자 연결 · 고정형</h3><div class="grid g3p reveal">{tcards["fixed"]}</div>
 <h3 class="sub3">② 폴딩 · 캐스터형</h3><div class="grid g3p reveal">{tcards["fold"]}</div>
 <h3 class="sub3">③ 초저가 대안</h3><div class="grid g3p reveal">{tcards["budget"]}</div>
   <h3 class="sub3">시청거리 (AVIXA DISCAS 4:6:8) · 75형 전자칠판</h3>
<div class="tbl reveal"><table><thead><tr><th>기준</th><th>75형(화면 높이 1034mm 기준)</th></tr></thead><tbody><tr><td>4×</td><td>4.1m</td></tr><tr><td>6×</td><td>6.2m</td></tr><tr><td>8×</td><td>8.3m</td></tr></tbody></table></div>
<div class="callout reveal" style="margin-top:14px"><b>이 배치에서는</b> · 10·12석(의자 양끝 위치가 같아 거리 같음): 가까운 {S12["eye_min"]/1000:.1f}m ~ 먼 {S12["eye_max"]/1000:.1f}m, 15석 가장 가까운 {S15["eye_min"]/1000:.1f}m ~ 먼 {S15["eye_max"]/1000:.1f}m예요. 칠판이 ㄷ자 열린 쪽 정면이라 상석 쪽이 가장 먼 자리(4×~6× 사이)이고, 다리 쪽 앞자리는 4×(4.1m)보다 훨씬 가까워요(칠판 정면은 아니고 최대 약 {S12["view_leg_max"]}° 비스듬). 전자칠판은 구매 전 확인할 수 없어 크기·무게는 판매자 제시 값이에요. 대표 모션데스크 4종 비교는 보유품을 쓰기로 해서 뺐어요.</div>
</div></section>

<section class="sec alt" id="sources"><div class="wrap">
 <div class="eyebrow">출처와 미확인</div>
 <h2>확인하지 못한 것</h2>
 <ul class="checks reveal">
  <li class="wn"><b>!</b><span>방 치수·문·창·콘센트: 사진으로 추정한 값(약 4.5×9.8m). 문 위치(출입문 쪽 단변 중앙)·여닫이 방향·바닥 콘센트 위치는 정확하지 않아요. 배치도의 의자·책상 간격은 그 가정 기준이에요.</span></li>
  <li class="wn"><b>!</b><span>소파 치수: 일룸 코모·이안가구 론디 모두 정확한 치수를 확인하지 못함 → 도면 크기는 추정(2인형 850×1200 도면 크기, 10·12·15석 같음). 구매표의 소파 가격은 2인용 기준이라 도면과 맞아요.</span></li>
 <li class="wn"><b>!</b><span><b>책장 가벽</b>: IKEA 빌리 80×28×106cm(705.220.44) 64,900원은 이케아 공식 페이지 표시값(2026-11-02)이에요. 3개를 쓰는 가벽의 실제 길이·벽 고정·서로 연결 고정 방법, 배송·조립 비용은 미확인이고 이케아는 전복 방지 고정을 요구해요. 쿠팡 판매가(74,400원)는 별도 판매자 가격이에요. 한샘 플롯 책장세트는 이번에 구매표에서 뺐어요.</span></li>
  <li class="wn"><b>!</b><span>화이트보드 두 제품 모두 캐스터 여부를 상세 확인하지 못함(이번 도면에서는 자리가 없어 뺐어요). 룸앤오피스 책상 크기·높이·캐스터 미확인. 가이아 1200×600 가격은 기본가(238,700원)를 1200 옵션으로 추정한 값이라 주문 시 확인이 필요해요.</span></li>
  <li class="wn"><b>!</b><span>Shure 마이크 맥 USB-C 호환은 사양 기준(직접 테스트 아님). MoveMic Two 가격은 컴퓨존 표시값이에요.</span></li>
  <li class="wn"><b>!</b><span>GODOX 소프트박스, 에프손 프로젝터 투사거리, 복합기 렌탈, 퍼시스 CH2811 가격, 탕비 선반, UPS·스위치 가격은 조사하지 않았어요. 공유기 20명 이상 동시접속 성능과 건물 차단기 용량도 미확인.</span></li>
  <li class="wn"><b>!</b><span>LG 가전: 모든 가격은 LG전자 공식몰 표시값(2026-11-01)이에요. <b>가습기 HY505RWLAH</b>는 목록 페이지 799,000원, 상세 페이지 회원가 899,000원(정상가 1,099,000원)으로 달라서 높은 쪽을 썼어요. 공기청정기 AS186HWWL 368,000원은 정상가 754,000원에서 할인된 <b>타임딜</b> 표시가라 끝날 수 있어요. 정수기 WD520AWB는 1,328,000원(목록 1,410,000원, 정상가 1,770,000원)이고 구독(월 14,400원~) 조건과 설치 가능 여부는 현장 확인이 필요해요. 상위 모델 WD523AWB 가격은 페이지에서 다시 확인하지 못했어요.</span></li>
  <li class="wn"><b>!</b><span>탕비 콘센트·급수·배수 위치와 새 탕비 자리의 실제 동선은 현장에서 확인하지 못했어요. 가습기는 LG 안내로 약 35㎡용이라 44㎡ 전체에는 부족할 수 있어요.</span></li>
  <li class="wn"><b>!</b><span>‘서울대 의자’ = 아이블(TNB501FE)은 블로그 후기 기준이고 대학 납품 사실은 공식 확인 못 했어요. 시디즈 보증기간은 판매처 표기가 달라요.</span></li>
  <li class="wn"><b>!</b><span><b>전자칠판</b>: 제노스미디어 CO750LT4K 75형 150만원은 사용자가 알려준 당근 중고 값이고 링크·실물 확인은 못 했어요. 스탠드 바닥 크기(도면 1467×520mm 가정)·AS는 미확인이에요. 칠판 뒤 약 0.2m 틈의 전원·AV 선 접근과 콘센트 위치도 미확인이고, 칠판 바로 뒤 책장 가벽(전복 방지 고정·한쪽 끝만 벽에 닿는 구조)의 실제 시공 방법도 미확인이에요.</span></li>
 <li class="wn"><b>!</b><span><b>배치·크기 가정</b>: 대표 책상 1500×700(모션데스크 #2도 같은 크기로 가정), 서진이 책상 1000×600(집에서 가져옴, 크기는 가정), 로봇 도크·34형 모니터·Mac Studio 크기, 칠판 스탠드 1467×520(바퀴 유무 포함)은 가정이에요. <b>창 쪽 오른쪽 출입문(폭 0.9m·안쪽 여닫이)과 외부 펜트리(폭 4.5m=사무실 폭은 확인, 깊이 1.3m는 가정)</b>이고 ‘왼쪽·오른쪽’은 <b>도면 이미지 기준</b>이에요(실제 방향이 반대라면 알려주세요). 소파 크기 850×1200(소형)도 가정이에요. 복합기 380×460도 가정이에요. 대표석은 출입문(정문)을 정면으로 보고 모니터 뒷면이 입구 쪽이지만, 칠판·U 책상에 시선이 가려지는 정도는 실측 전 추정이에요. 슬리퍼 랙(900×300)은 후보 위치예요. CCTV 시야각은 제품 사양 기준 대략값이고 콘센트·급수·배수·바닥 콘센트 위치와 방 치수는 미확인이에요.</span></li>
 <li class="wn"><b>!</b><span><b>CCTV 가격</b>: Tapo C225 76,310원·C110 38,280원·VIGI NVR1104H-4P 84,990원은 다나와 표시값(2026-11-02)이에요. microSD·스튜디오 책상·<b>두 번째 모션데스크는 가격 미정</b>이에요(합계 미포함). 서진이 책상은 집에서 가져와서 구매표에서 뺐어요. 개인정보 안내표지 규격·가격은 조사하지 않았어요.</span></li>
  <li class="wn"><b>!</b><span><b>스타일러</b>: SC5MBR61S 가격은 LG 페이지 표시가 혼재(2,191,000/2,070,000원)해 확정하지 못했고, 3벌 모델과 사무실(상업용) 설치 가능 여부는 확인하지 못했어요. 확정 구매 항목이 아니에요.</span></li>
  <li class="wn"><b>!</b><span>용달 요금·업체는 조사하지 않았어요(요청에 따라).</span></li>
 </ul>
 <p class="small" style="margin-top:20px">상품 사진은 각 판매처·제조사 이미지이며 저작권은 해당 업체에 있어요. 모든 가격은 {D}(KST) 표시값이며 광고·제휴가 없어요. 링크는 각 항목의 ‘제품명 + 링크’를 확인하세요.</p>
</div></section>
</main>
<footer><div class="wrap">AI Builders Lab · 동탄 사무실 셋업 가이드 · {D}(KST) 기준 정리 · 가격은 변동될 수 있어요</div></footer>
<script>window.DATA={json.dumps(data,ensure_ascii=False)};</script>
<script src="assets/main.js"></script>
</body></html>'''
exec(open("apple.py",encoding="utf8").read())
print("MAIN",M10,M12,M15,MP10,MV10,"DEF",DEF10,DU10,DN10);print("10:",R10,R10n,L10,cg10,P10,V10); print("12:",R12,R12n,L12,cg12,P12,V12); print("15:",R15,P15,V15)
