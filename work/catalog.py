# 카테고리별 프리미엄/가성비 2안. 모든 가격은 2026.11.01 KST 판매 페이지 표시값(단가, 원).
DN="https://prod.danawa.com/info/?pcode="
def dn(c): return DN+str(c)
# tier: n=제품명, u=링크, img, p=단가, q=(12석,15석), why, src, w=미확인/주의
I=[]
def add(id,grp,name,pri,P,V,rec,note=""):
    I.append(dict(id=id,grp=grp,name=name,pri=pri,P=P,V=V,rec=rec,note=note))
def t(n,u,img,p,q,why,src,w=""): return dict(n=n,u=u,img=img,p=p,q=q,why=why,src=src,w=w)
# ---------------- 교육존
add("table","교육존","교육 책상 (3석/개)","입주 전 필수",
 t("데스커 멀티테이블 1800×800","https://www.desker.co.kr/product/detail/694","p-desker-multitable.jpg",261000,(4,5),"깊이 800이라 노트북+노트 여유","데스커 공식몰"),
 t("룸앤오피스 YWD6029","https://price.enuri.com/catalog/106739798","p-roomnoffice.jpg",62690,(4,5),"4개에 25만원대로 가장 저렴","에누리","높이·캐스터 사양은 판매 페이지에서 미확인"),"P")
add("chair_l","교육존","학습자 의자","입주 전 필수",
 t("시디즈 T20 2세대","https://kr.sidiz.com/products/t20","p3-ch-t20.jpg",239000,(12,15),"틸팅 강도 4단 조절, 3시간 이상 수업에 안전","시디즈 공식몰"),
 t("시디즈 IBLE (‘서울대 의자’)","https://kr.sidiz.com/products/ible","p3-ch-ible.jpg",189000,(12,15),"메시 등판·틸팅 없음(공식). 189,000원은 글라이드형(바퀴형 199,000원). 12개에 약 60만원 절감","시디즈 공식몰","틸팅 없음 → 4시간 이상 수업엔 불편 가능"),"V")
add("tv","교육존","TV 65형 (맨 앞)","입주 전 필수",
 t("삼성 65형 벽걸이 모델","https://prod.danawa.com/info/?pcode=122641155","p-samsung65w.jpg",1074120,(1,1),"삼성 65형 벽걸이형(VESA 200×200·14.1kg), 이동식 스탠드에 달기 쉬움","다나와 최저가"),
 t("LG 65UA7500ENA","https://prod.danawa.com/info/?pcode=92376488","p-lg65.jpg",845830,(1,1),"65형을 약 23만원 싸게","다나와 최저가"),"V")
add("stand","교육존","TV 이동식 스탠드","입주 전 필수",
 t("엔산마운트 FS-64B","https://www.nsan.co.kr/goods/goods_view.php?goodsNo=1000001322","p-nsan-fs64b.jpg",188000,(1,1),"40~70형·40kg, 바퀴로 이동","엔산 공식몰"),
 t("아이존 TFC-8060","https://eyezoneind.com/category/tv%EA%B1%B0%EC%B9%98%EB%8C%80/167/","",157500,(1,1),"50~100형·100kg 이동형, 약 3만원 저렴","아이존 목록","사진·상세 사양 미확인"),"P")
add("wb","교육존","이동식 화이트보드 180×90 (양면·스탠드)","입주 전 필수",
 t("두문 이동식 화이트보드 1800×900","https://prod.danawa.com/info/?pcode=79448198","p3-wb-dm.jpg",154930,(1,1),"양면 스탠드형, 유리 칠판 대신 이동 가능","다나와 최저가","캐스터 여부 상세 미확인"),
 t("오피스팁 이동식화이트보드 1800×900","https://opstip.com/pm/m/product/product_view.html?pid=432758","p3-wb-ops.jpg",155400,(1,1),"양면·스탠드 포함. 152,400원+배송 3,000원","오피스팁","가격 차 거의 없음 · 캐스터 미확인"),"P")
# ---------------- 대표석
add("desk_ceo","대표석","대표 모션데스크 (집에 있는 것 이전)","입주 전 필수",
 t("보유 모션데스크 (집→사무실 용달 운반)","","",0,(1,1),"구매 아님 — 용달 운반 목록에 포함","보유"),
 t("보유 모션데스크 (집→사무실 용달 운반)","","",0,(1,1),"구매 아님 — 용달 운반 목록에 포함","보유"),"P","own")
add("chair_c","대표석","대표석 의자","입주 전 필수",
 t("시디즈 T50 2세대 T51HLDA0KK","https://kr.sidiz.com/products/t50-2","p3-ch-t50-2.jpg",419000,(1,1),"시디즈 상위 모델, 장시간 착석용 대표석","시디즈 공식몰"),
 t("시디즈 T20 2세대","https://kr.sidiz.com/products/t20","p3-ch-t20.jpg",239000,(1,1),"학습자와 같은 모델로 통일, 18만원 절감","시디즈 공식몰"),"P")
# ---------------- 포커스룸
add("f_desk","포커스룸","포커스 데스크 (칸막이형)","1개월 내",
 t("벨리카가구 오즈 1200×600×1329","https://prod.danawa.com/info/?pcode=99891800","p3-focus-oz.jpg",296080,(3,2),"높은 칸막이로 시선 차단, 폭 1200","다나와 최저가"),
 t("소담갤러리 파이 800×600×1190","https://prod.danawa.com/info/?pcode=30251057","p3-focus-pi.jpg",94730,(3,2),"3개에 28만원, 좁은 방에 폭 800","다나와 최저가"),"V")
add("f_mon","포커스룸","포커스 모니터 27형","1개월 내",
 t("LG 27UP850K (4K, USB-C)","https://prod.danawa.com/info/?pcode=73883519","p3-mon-lg.jpg",399000,(3,2),"맥북 USB-C 한 줄 연결·4K","다나와 최저가"),
 t("크로스오버 27QD166CM","https://prod.danawa.com/info/?pcode=90890663","p3-mon-cross.jpg",168980,(3,2),"QHD, 3대에 약 69만원 절감","다나와 최저가","USB-C 입력 여부는 판매 페이지에서 재확인"),"V")
add("f_arm","포커스룸","모니터암","1개월 내",
 t("NorthBayou NB F80","https://prod.danawa.com/info/?pcode=30126518","p3-arm-nb.jpg",29000,(3,2),"가스스프링, 널리 쓰는 검증 모델","다나와 최저가"),
 t("마루느루 MV12-T01","https://prod.danawa.com/info/?pcode=75600713","p3-arm-mv.jpg",28400,(3,2),"가격 거의 같은 대안","다나와 최저가"),"P")
# ---------------- 라운지·탕비
add("shelf","라운지·탕비","책장 (촬영 배경 겸용)","1개월 내",
 t("한샘 플롯 오픈 5단 책장세트 1200 (책장 2개)","https://prod.danawa.com/info/?pcode=65366576","p3-shelf-hs.jpg",617100,(1,1),"오픈 5단, 2개가 한 세트","다나와 최저가","세트 크기 124.5×44.6×187.7cm가 1세트 기준인지 개별 기준인지 미확인"),
 t("이케아 BILLY 6단 800×28×202","https://prod.danawa.com/info/?pcode=1503803","p3-shelf-billy.jpg",126900,(2,2),"2개에 25만원, 얇은 28cm 깊이","다나와 표시","다나와 목록이 오래된 판매처 가격일 수 있음 · 이케아 공식가 재확인"),"V")
add("bean","라운지·탕비","빈백","나중에",
 t("폴리몰리 607P","https://prod.danawa.com/info/?pcode=92232467","p3-bean-poly.jpg",214000,(2,2),"고급 소재, 오래 씀","다나와 최저가"),
 t("생활특권 쫀득 빈백","https://prod.danawa.com/info/?pcode=19548053","p3-bean-life.jpg",54980,(2,2),"2개에 11만원","다나와 최저가"),"V")
add("sofa","라운지·탕비","소파 2인","1개월 내",
 t("일룸 코모 2인 소파","https://www.iloom.com/product/detail.do?productCd=ISB0009A","p3-sofa-como.jpg",750000,(1,0),"클린터치 패브릭, 미니멀 톤","일룸 공식몰","치수가 판매 페이지에 ‘상세페이지 참조’로만 있어 도면 크기는 추정"),
 t("이안가구 론디 2인","https://prod.danawa.com/info/?pcode=76509122","p3-sofa-ian.jpg",79900,(1,0),"7만원대 가성비","다나와 최저가","치수 미확인(도면은 추정 크기)"),"P")
add("tea","라운지·탕비","티테이블","1개월 내",
 t("일룸 람다 소파테이블 120×59×33","https://prod.danawa.com/info/?pcode=31344101","p3-tt-lambda.jpg",185000,(1,0),"샌드오크/화이트","다나와 최저가"),
 t("플라팜 라운드 37×37×58","https://prod.danawa.com/info/?pcode=76402349","p3-tt-plapam.jpg",37900,(1,0),"작은 원형, 좁은 라운지에 부담 없음","다나와 최저가"),"V")
add("coffee","라운지·탕비","커피머신","1개월 내",
 t("필립스 3200 EP3243/53","https://prod.danawa.com/info/?pcode=20444393","p3-cof-phil.jpg",701030,(1,1),"전자동, 라떼·원두, 13명도 대응","다나와 최저가"),
 t("네스프레소 버츄오 팝 플러스","https://prod.danawa.com/info/?pcode=103482785","p3-cof-nes.jpg",77616,(1,1),"캡슐형 작은 크기","다나와 최저가","캡슐 소모비 별도"),"P")
add("fridge","라운지·탕비","냉장고","1개월 내",
 t("삼성 RT40H15V3SW 150L (화이트 494×1189×558)","https://prod.danawa.com/info/?pcode=124238410","p3-fr-40.jpg",435440,(1,1),"화이트·작은 크기","다나와 최저가"),
 t("삼성 RT20FARL3S9 203L (555×1445×637)","https://prod.danawa.com/info/?pcode=78786872","p3-fr-20.jpg",335790,(1,1),"더 크고 더 싼 203L","다나와 최저가"),"V")
add("mfp","라운지·탕비","복합기 (인쇄·복사·스캔)","입주 전 필수",
 t("캐논 MF664Cdw","https://prod.danawa.com/info/?pcode=124012067","p3-mfp-canon.jpg",489000,(1,1),"컬러 레이저 25ppm·양면·ADF, 맥 지원","다나와 최저가","렌탈 가격은 미조사"),
 t("삼성 SL-C563W","https://prod.danawa.com/info/?pcode=9847101","p3-mfp-sam.jpg",315000,(1,1),"복사·스캔·인쇄 되는 저가형","다나와 최저가","컬러 4ppm·흑백 18ppm로 느림 · 렌탈 미조사"),"P")
# ---------------- 네트워크·전원
add("router","네트워크·전원","공유기 (Wi-Fi 6/6E, 20+명)","입주 전 필수",
 t("TP-Link Deco XE75 Pro 2팩 (Wi-Fi 6E 메시)","https://prod.danawa.com/info/?pcode=17831153","p3-rt-deco.jpg",274230,(1,1),"2대 메시로 포커스룸까지 커버, 6E","다나와 최저가","동시접속 20+명 실측 성능은 미검증"),
 t("ipTIME BE7200M (Wi-Fi 7)","https://prod.danawa.com/info/?pcode=124481304","p3-rt-be.jpg",165400,(1,1),"1대로 저렴, Wi-Fi 7","다나와 최저가","1대라 구석 음영 가능 · 20+명 성능 미검증"),"P")
add("strip","네트워크·전원","멀티탭 6구 16A 개별스위치 3m","입주 전 필수",
 t("대현써지오 모노케어","https://prod.danawa.com/info/?pcode=12551873","p3-ps-dh.jpg",16700,(8,9),"개별 스위치, 노트북 충전용","다나와 최저가"),
 t("현대일렉트릭 6구 3m","https://prod.danawa.com/info/?pcode=5199359","p3-ps-hd.jpg",12700,(8,9),"4천원 싸게","다나와 최저가","개별스위치·16A 세부는 판매 페이지 재확인"),"V")
add("nas","네트워크·전원","NAS (집에서 이전)","입주 전 필수",
 t("보유 NAS","","",0,(1,1),"구매 아님 — 이삿짐으로 운반","보유"),
 t("보유 NAS","","",0,(1,1),"구매 아님 — 이삿짐으로 운반","보유"),"P","own")
# ---------------- 스튜디오
add("light","스튜디오 코너","조명 (키 라이트 + 보조)","1개월 내",
 t("GODOX SL150II LED 150W","https://prod.danawa.com/info/?pcode=12957194","p3-lt-godox.jpg",350000,(1,1),"5600K·CRI96, 소프트박스와 쓰면 인물이 깨끗","다나와 최저가","소프트박스는 별도(미조사)"),
 t("울란지 W49 LED 패널","https://prod.danawa.com/info/?pcode=7999588","p3-lt-w49.jpg",8500,(2,2),"AA 건전지식 860lm, 2개로 보조광","다나와 최저가","건전지식이라 장시간 촬영엔 부족"),"P")
add("mic","스튜디오 코너","데스크 마이크 (Shure)","1개월 내",
 t("Shure MV7+ (USB-C/XLR)","https://prod.danawa.com/info/?pcode=57446294","p3-mic-mv7p.jpg",494990,(1,1),"USB-C로 맥에 바로 연결, XLR도 가능","다나와 최저가","맥 USB-C 호환은 슈어 제품 사양 기준(직접 연결 테스트 안 함)"),
 t("Shure MV6","https://prod.danawa.com/info/?pcode=76872590","p3-mic-mv6.jpg",265990,(1,1),"USB 게이밍/방송용, 가성비","다나와 최저가","맥 호환은 사양 기준"),"P",
 "참고: SM7B(870,000원, XLR 전용)·MV7X(318,000원, XLR 전용)는 오디오 인터페이스(예: Shure MVX2U 219,000원)가 따로 필요해 표에서 제외했어요.")
add("lav","스튜디오 코너","무선 라발리에 마이크 (Shure)","1개월 내",
 t("Shure MoveMic Two (2인용)","https://www.compuzone.co.kr/product/product_detail.htm?ProductNo=1149255","p3-mic-mm2.jpg",620000,(1,1),"제레미+유하님 2인 인터뷰 한 세트","컴퓨존","맥 USB-C 직결 여부는 수신기·앱 구성 확인 필요"),
 t("Shure MoveMic One (1인용)","https://www.compuzone.co.kr/product/product_detail.htm?ProductNo=1138599","p3-mic-mm1.jpg",442000,(1,1),"1명용 (유하님 쪽만)","컴퓨존","2명이면 Two(620,000원)가 더 저렴"),"P")
add("cam","스튜디오 코너","카메라 / 웹캠","나중에",
 t("Sony ZV-E10 II 렌즈킷","https://prod.danawa.com/info/?pcode=60063581","p3-cam-zv.jpg",1253720,(1,1),"유튜브 전용 APS-C","다나와 최저가"),
 t("보유 iPhone (삼각대 촬영)","","",0,(1,1),"이미 가진 폰이 가장 가성비","보유"),"V")
add("tripod","스튜디오 코너","삼각대","1개월 내",
 t("맨프로토 엘리먼트 MII","https://prod.danawa.com/info/?pcode=12471671","p3-tri-man.jpg",159520,(1,1),"맨프로토 정품 삼각대","다나와 최저가"),
 t("LK-9892","https://prod.danawa.com/info/?pcode=18870608","p3-tri-lk.jpg",15700,(1,1),"1.5만원대","다나와 최저가","폰 거치대 포함 여부 미확인"),"V")
add("shelfled","스튜디오 코너","책장 간접조명 LED 스트립","1개월 내",
 t("필립스 휴 라이트스트립 플러스 20W 200cm","https://prod.danawa.com/info/?pcode=11918494","p3-strip-hue.jpg",97750,(1,1),"색·밝기 앱 제어","다나와 최저가"),
 t("TP-Link Tapo L900 5m","https://prod.danawa.com/info/?pcode=62175998","p3-strip-tapo.jpg",24390,(1,1),"5m에 2.4만원, 색 변경","다나와 최저가"),"V")
add("foam","스튜디오 코너","흡음재 (선택, 약 6장)","나중에",
 t("아트보드 9T 600×1200","https://prod.danawa.com/info/?pcode=52156100","p3-foam-art.jpg",6800,(6,6),"패널형 흡음재","다나와 최저가"),
 t("올폼 계란판 50T 500×1000","https://prod.danawa.com/info/?pcode=14151677","p3-foam-egg.jpg",6500,(6,6),"소리 흡수 효과 더 큼","다나와 최저가"),None)
# ---------------- 프로젝터(선택)
add("proj","선택 장비","빔프로젝터 (대체/보조 화면)","나중에",
 t("엡손 EB-L210SW 레이저 4000lm","https://prod.danawa.com/info/?pcode=20098214","p3-pj-epson.jpg",1265000,(1,1),"레이저 4000lm, 소형(325×90×337mm)","다나와 최저가","투사거리 사양 미확인"),
 t("뷰소닉 PA503W 3800안시","https://prod.danawa.com/info/?pcode=5788165","p3-pj-vs.jpg",530000,(1,1),"100인치를 3.3m에서","다나와 최저가"),None)
add("screen","선택 장비","프로젝터 스크린 100형 전동","나중에",
 t("성지 SJ-NC100W","https://prod.danawa.com/info/?pcode=16165202","p3-sc-sj.jpg",309000,(1,1),"전동 100형","다나와 최저가"),
 t("성지 SJ-BNC100W","https://prod.danawa.com/info/?pcode=99126140","p3-sc-bnc.jpg",158000,(1,1),"절반 가격","다나와 최저가"),None)
# ---------------- 프린터 / 3D
add("printer","프린터·메이커","별도 프린터 (복합기와 별개)","나중에",
 t("엡손 EcoTank Photo L18050 (A3 포토)","https://prod.danawa.com/info/?pcode=19603004","p3-pr-l18050.jpg",549000,(1,1),"사진·A3 무한잉크, 맥 지원","다나와 최저가"),
 t("브라더 PT-H110BW 라벨프린터","https://prod.danawa.com/info/?pcode=5344591","p3-pr-pth110.jpg",59000,(1,1),"라벨·명찰용 소형","다나와 최저가"),None)
add("p3d","프린터·메이커","3D 프린터","나중에",
 t("뱀부랩 P1S 콤보 (밀폐형)","https://prod.danawa.com/info/?pcode=76550822","p3-3d-p1s.jpg",749000,(1,1),"밀폐형이라 냄새·소음 덜함, 256³","다나와 최저가"),
 t("뱀부랩 A1 mini (오픈형)","https://prod.danawa.com/info/?pcode=75538655","p3-3d-a1m.jpg",279000,(1,1),"입문용 180³, 2.8만원대","다나와 최저가","오픈형 → 환기·소음 신경 필요"),"V")
