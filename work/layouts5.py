import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle, Circle, Polygon, Arc, Wedge
fp="/usr/share/fonts/truetype/sand-box/google/Nanum Gothic/NanumGothic-Bold.ttf"
fm.fontManager.addfont(fp); plt.rcParams["font.family"]=fm.FontProperties(fname=fp).get_name()
INK="#191F28"; GRAY="#6B7684"; BLUE="#3182F6"; WOOD="#EBD3AB"; EC="#9A7B4F"; RED="#F04452"; GRN="#0F9D7A"
W,H=4500,9800
OUT="/workspace/office-desk-guide/assets/img/"
def R(ax,x,y,w,h,fc,ec="none",lw=1,z=3,ls="-",alpha=1): ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=z,ls=ls,alpha=alpha))
def T(ax,x,y,s,fs=6.5,c=INK,ha="center",va="center",z=9,**k): ax.text(x,y,s,fontsize=fs,color=c,ha=ha,va=va,zorder=z,**k)
def Z(ax,x,y,w,h,fc,label,c=INK,lx=60,ly=90,fs=7.5):
    R(ax,x,y,w,h,fc,z=1,alpha=.55)
    if label: T(ax,x+lx,y+ly,label,fs=fs,c=c,ha="left",z=2,fontweight="bold")
def chair(ax,cx,cy,col=BLUE,r=230): ax.add_patch(Circle((cx,cy),r,fc=col,ec="white",lw=.8,zorder=5))
def dim(ax,x1,y1,x2,y2,txt,dx=0,dy=0,c=GRN):
    ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="<->",color=c,lw=1),zorder=8)
    if txt: T(ax,(x1+x2)/2+dx,(y1+y2)/2+dy,txt,fs=6.3,c=c,bbox=dict(fc="white",ec="none",pad=.6,alpha=.92))
def plug(ax,x,y,w=300,h=70): R(ax,x,y,w,h,"#FF9F1C","#B86E00",.8,z=7)
def outlet(ax,x,y): ax.plot([x],[y],marker="s",ms=4,color="#FF9F1C",mec="#B86E00",zorder=8)


import math
def chair2(ax,cx,cy,fx,fy,col=BLUE,r=205):
    ax.add_patch(Circle((cx,cy),r,fc=col,ec="white",lw=.8,zorder=5))
    k=r-14; kc="#143E8C"
    if fx: ax.plot([cx-fx*k]*2,[cy-130,cy+130],color=kc,lw=1.8,solid_capstyle="round",zorder=6)
    else: ax.plot([cx-130,cx+130],[cy-fy*k]*2,color=kc,lw=1.8,solid_capstyle="round",zorder=6)
def sofa(ax,x,y,w,d,back="down",label="소파 3인"):
    FC,EC2,BK="#E7D5BC","#8A6A3A","#C2A27A"
    R(ax,x,y,w,d,FC,EC2,1.6,z=5)
    if back=="down":
        R(ax,x,y+d-170,w,170,BK,EC2,1.2,z=6)
        R(ax,x,y,130,d-170,BK,EC2,1.2,z=6); R(ax,x+w-130,y,130,d-170,BK,EC2,1.2,z=6)
        n=3 if w>1500 else 2; cw=(w-260)/n
        for i in range(1,n): ax.plot([x+130+cw*i]*2,[y+20,y+d-175],color=EC2,lw=.9,zorder=7)
        T(ax,x+w/2,y+(d-170)/2,label,fs=6.0,c="#5A3E1B",fontweight="bold",z=8,bbox=dict(fc=FC,ec="none",pad=1.5))
        T(ax,x+w/2,y+d-85,"등받이",fs=4.2,c="#5A3E1B",z=8)
    elif back=="left":
        R(ax,x,y,170,d,BK,EC2,1.2,z=6)
        R(ax,x+170,y,w-170,130,BK,EC2,1.2,z=6); R(ax,x+170,y+d-130,w-170,130,BK,EC2,1.2,z=6)
        n=3 if d>1500 else 2; cw=(d-260)/n
        for i in range(1,n): ax.plot([x+175,x+w-20],[y+130+cw*i]*2,color=EC2,lw=.9,zorder=7)
        T(ax,x+170+(w-170)/2,y+d/2,label,fs=6.0,c="#5A3E1B",fontweight="bold",rotation=90,z=8,bbox=dict(fc=FC,ec="none",pad=1.5))
    else:
        R(ax,x+w-170,y,170,d,BK,EC2,1.2,z=6)
        R(ax,x,y,w-170,130,BK,EC2,1.2,z=6); R(ax,x,y+d-130,w-170,130,BK,EC2,1.2,z=6)
        n=3 if d>1500 else 2; cw=(d-260)/n
        for i in range(1,n): ax.plot([x+20,x+w-175],[y+130+cw*i]*2,color=EC2,lw=.9,zorder=7)
        T(ax,x+(w-170)/2,y+d/2,label,fs=6.0,c="#5A3E1B",fontweight="bold",rotation=90,z=8,bbox=dict(fc=FC,ec="none",pad=1.5))
def bean(ax,x,y):
    ax.add_patch(Circle((x,y),270,fc="#8FB3E8",ec="white",zorder=5)); T(ax,x,y,"빈백",fs=5.6)
def build(mode):
    seats=12 if mode==12 else 15
    fig,ax=plt.subplots(figsize=(4.8,4.8*(H+1500)/(W+700)),dpi=260)
    R(ax,0,0,W,H,"#FBFCFD",z=0)
    # ---------- window (bottom short wall) / door (top short wall)
    R(ax,0,H-40,W,80,"#9AD3FF","#2C7FB8",1,z=6); T(ax,W/2,H+170,"창문 (바닥~천장 전면 유리) · 카메라는 창을 향하지 않음 · 암막/롤 블라인드 권장",fs=6.2,c="#2C7FB8")
    DX0,DX1=1800,2700   # 문: 짧은 벽(앞) 정중앙 (W/2=2250 기준 폭 900)
    R(ax,DX0,-35,DX1-DX0,70,"#FFFFFF","#555",1.2,z=7)
    ax.add_patch(Arc((DX0,0),1800,1800,theta1=0,theta2=90,color="#888",lw=1,ls="--",zorder=7))
    ax.plot([DX0,DX0+900],[0,0],color="#555",lw=1.2,zorder=7)
    ax.add_patch(Wedge((DX0,0),900,0,90,fc="#FFF3BF",alpha=.6,ec="none",zorder=2))
    T(ax,1150,-130,"출입문(복도) · 단변 정중앙\n문 스윙 0.9m 비움",fs=5.8,c="#555")
    # ---------- front wall: 전자칠판 75" (문 오른쪽, 스탠드 고정형)  제노스미디어 CO750LT4K 패널 1707x1034
    BX0=2760; BW=1707
    R(ax,BX0+120,100,BW-240,520,"#EEF1F6","#8B95A1",.9,z=4,ls="--",alpha=.7)      # 스탠드 발판(크기 가정)
    R(ax,BX0,100,BW,110,INK,z=6)
    T(ax,BX0+BW/2,420,"전자칠판 75\" 제노스미디어 CO750LT4K\n당근 중고 · 패널 1707×1034 · 고정 스탠드",fs=4.6)
    ax.plot([2715,4485],[18,18],color="#7B61FF",lw=3.2,zorder=8)
    T(ax,3650,-150,"전동 스크린(선택)",fs=5.8,c="#5B3FD1")
    # ---------- 탕비: 입구(문) 왼쪽 앞 벽에 한 줄 (냉장고 -> 정수기 -> 커피머신 -> 컵·선반)
    R(ax,50,50,555,637,"#E5E8EB","#8B95A1",1.2,z=5); T(ax,330,370,"냉장고\nRT20FARL3S9",fs=4.2)
    R(ax,620,50,880,600,"#FFFFFF","#8B95A1",1.2,z=5); T(ax,1060,590,"카운터 + 선반",fs=4.4)
    R(ax,660,100,168,400,"#BFEFF2","#0E7C86",1.4,z=7); T(ax,744,300,"정수기",fs=4.8,c="#0E6B73",rotation=90,fontweight="bold")
    R(ax,900,110,420,300,"#D9DDE2","#555",1,z=6); T(ax,1110,260,"커피머신",fs=5.0)
    R(ax,50,690,1450,800,"#FFF3BF","none",0,z=1,alpha=.35)
    T(ax,1100,950,"탕비 이용·대기 공간\n(문 열림과 안 겹침)",fs=4.6,c="#8A6D00")
    # 복합기 + NAS 선반 (왼쪽 벽, 탕비와 분리)
    R(ax,50,1750,380,460,"#FFFFFF","#2D6A4F",1.6,z=5); T(ax,240,1980,"복합기",fs=4.6); T(ax,470,1830,"위 선반: NAS +\n공유기 ASUS\nRT-BE92U",fs=4.4,c="#5B3FD6",ha="left")
    # 스타일러 후보(선택, 점선) 600x620, 문 열면 깊이 1190
    R(ax,50,1050,620,600,"none","#7A5BD8",1.3,z=6,ls="--"); T(ax,360,1350,"스타일러\n(선택·후보)\n600×620\n열면 1.19m",fs=4.2,c="#5B3FD1")
    # 공기청정기 (U 입구 오른쪽 앞) LG AS186HWWL 315x315, 주변 30cm 비움
    R(ax,3443,1343,614,614,"none","#0E7C86",.8,z=6,ls="--")
    ax.add_patch(Circle((3750,1650),157,fc="#E6F7F8",ec="#0E7C86",lw=1.4,zorder=7)); ax.add_patch(Circle((3750,1650),75,fc="none",ec="#0E7C86",lw=.8,zorder=8))
    T(ax,3750,1270,"공기청정기 (LG 퓨리케어 360°)",fs=4.6,c="#0E6B73",fontweight="bold")
    T(ax,3000,1950,"입구 쪽 회의 영역 (전자칠판 앞 · U 입구)",fs=5.0,c="#1F5FBF",fontweight="bold")
    # CCTV 2대 (실내, 천장/벽 설치) — 포커스석·스튜디오·서진이 구역은 시야 밖
    def cam(x,y,c,fov,rad,n):
        ax.add_patch(Wedge((x,y),rad,c-fov/2,c+fov/2,fc="#FF6B6B",alpha=.10,ec="#E03131",lw=.7,ls="--",zorder=2))
        ax.add_patch(Circle((x,y),95,fc="#E03131",ec="white",lw=1,zorder=9)); T(ax,x,y,"▣",fs=4.2,c="white",z=10)
        return n
    cam(2750,70,135,90,2550,"1"); T(ax,2480,330,"CCTV 1 입구·탕비",fs=4.6,c="#C92A2A",fontweight="bold",ha="center")
    cam(4430,4000,180,70,3800,"2"); T(ax,4150,3820,"CCTV 2 책상·U",fs=4.8,c="#C92A2A",fontweight="bold",ha="right")
    # 이동식 화이트보드 (선택, 점선)
    R(ax,4350,750,100,1500,"#FFFFFF","#444",1.2,z=5,ls="--"); T(ax,4290,1500,"이동식 화이트보드(선택)",fs=5.0,rotation=90)
    # ---------- projector (ceiling)
    px,py=2500,3500
    ax.add_patch(Rectangle((px-150,py-90),300,180,fc="#7B61FF",ec="white",zorder=8,alpha=.9)); T(ax,px,py-200,"빔프로젝터(천장, 선택)",fs=5.8,c="#5B3FD1")
    ax.add_patch(Polygon([[px,py-90],[2715,18],[4485,18]],fc="#7B61FF",alpha=.08,ec="#7B61FF",lw=.6,ls="--",zorder=2))
    # ---------- ceiling AC + floor outlet (from photos)
    ax.add_patch(Circle((2250,4950),260,fc="none",ec="#9AA5B1",lw=1,ls="--",zorder=4)); T(ax,2250,4950,"천장형\n에어컨",fs=5.2,c="#9AA5B1")
    FX,FY=900,4950
    ax.plot([FX],[FY],marker="o",ms=7,color="#FF9F1C",mec="#B86E00",zorder=9); 
    T(ax,60,FY-330 if mode==15 else FY-420,"바닥 콘센트\n(대략)",fs=4.4,c="#B86E00",ha="left",multialignment="left")
    # ---------- learners: 연결된 ㄷ자 (다리 1800+1800 x2, 바닥 1200) / 의자는 바깥, 안쪽을 향함
    UP=[(1050,2250),(1650,2250),(1650,5250),(2850,5250),(2850,2250),(3450,2250),(3450,5850),(1050,5850)]
    if mode==12:
        ch=[(790,2610+720*i,1,0) for i in range(5)]+[(3710,2610+720*i,-1,0) for i in range(5)]+[(1850,6110,0,-1),(2650,6110,0,-1)]
    else:
        ch=[(790,2550+600*i,1,0) for i in range(6)]+[(3710,2550+600*i,-1,0) for i in range(6)]+[(1450,6110,0,-1),(2250,6110,0,-1),(3050,6110,0,-1)]
    Z(ax,580,2250,3340,4070,"#DCEBFF","")
    ax.add_patch(Polygon(UP,closed=True,fc=WOOD,ec=EC,lw=2.2,zorder=4,joinstyle="round"))
    for (x1,y1,x2,y2) in [(1050,4050,1650,4050),(2850,4050,3450,4050),(1650,5250,1650,5850),(2850,5250,2850,5850)]:
        ax.plot([x1,x2],[y1,y2],color=EC,lw=.9,zorder=5)
    for (tx,ty) in [(1350,3150),(1350,4950),(3150,3150),(3150,4950)]: T(ax,tx,ty,"1800×600",fs=5.0,c="#6B5530",rotation=90)
    T(ax,2250,5550,"1200×600\n(추가)",fs=5.0,c="#6B5530")
    for (cx,cy,fx,fy) in ch: chair2(ax,cx,cy,fx,fy)
    T(ax,2250,3900,f"U 안쪽 발표·토론 공간\n(폭 1.2m · 앞 문·TV 쪽 열림)\n교육존 {seats}석",fs=6.2,c="#1F5FBF",fontweight="bold")
    ax.annotate("",xy=(2250,2380),xytext=(2250,3150),arrowprops=dict(arrowstyle="-|>",color="#1F5FBF",lw=1.4),zorder=8)
    for (x,y,o) in [(1580,2850,"v"),(1580,4800,"v"),(2850,2850,"v"),(2850,4800,"v"),(2100,5250,"h")]:
        if o=="v": R(ax,x,y,70,300,"#FF9F1C","#B86E00",.8,z=7)
        else: R(ax,x,y,300,70,"#FF9F1C","#B86E00",.8,z=7)
    ax.plot([FX,1580],[FY,FY],color="#FF9F1C",lw=.9,ls=":",zorder=7)
    ax.plot([1350,1350,1580],[FY,3000,3000],color="#FF9F1C",lw=.9,ls=":",zorder=7)
    ax.plot([1350,1350,2100,2100],[FY,5550,5550,5320],color="#FF9F1C",lw=.9,ls=":",zorder=7)
    ax.plot([2100,3150,3150,2920],[5550,5550,4950,4950],color="#FF9F1C",lw=.9,ls=":",zorder=7)
    ax.plot([3150,3150,2920],[4950,3000,3000],color="#FF9F1C",lw=.9,ls=":",zorder=7)
    for (ox,oy) in [(W-40,3500),(W-40,5300),(40,7000),(W-40,7600),(W-40,2300)]: outlet(ax,ox,oy)
    # ---------- rear zone (12·15석 공통): ㄱ자 = 창가 줄(대표석·서진이·포커스) + 오른쪽 벽 줄(YouTube 스튜디오)
    R(ax,4455,6400,45,800,"#8B95A1",z=6); T(ax,4380,6800,"흡음재(선택)",fs=5.0,c=GRAY,rotation=90)
    Z(ax,2150,7250,2350,1650,"#FFD9DE","")
    T(ax,2200,7215,"ㄱ자 조용한 구역 · YouTube 스튜디오 (책장 배경 1.5m)",fs=5.2,ha="left",c="#B1202C",fontweight="bold")
    ax.add_patch(Polygon([(2900,7260),(4495,7260),(4495,9795),(700,9795),(700,9000),(2900,9000)],closed=True,fc="none",ec="#7B61FF",lw=1.0,ls=":",zorder=3))
    R(ax,4054,7300,446,1500,"#D9B88A","#8A6A3A",1.5,z=5); T(ax,4280,8050,"책장 2대(배경)",fs=5.2,rotation=90)
    ax.plot([4054,4054],[7300,8800],color="#FFD60A",lw=3,zorder=6)
    R(ax,3000,7450,500,1100,"#FFFFFF","#F04452",1.6,z=5); T(ax,3180,8000,"촬영 책상",fs=4.8,rotation=90)
    for my in (7750,8250): ax.add_patch(Circle((3300,my),50,fc="#444",ec="white",zorder=7))
    T(ax,3300,7620,"Shure",fs=4.2)
    chair(ax,3800,7700,RED,r=200); chair(ax,3800,8350,"#F5A3AB",r=200); T(ax,3800,7700,"제레미",fs=4.8,c="white"); T(ax,3800,8350,"유하님",fs=4.6,c="white")
    cx,cy=1800,8050
    ax.add_patch(Polygon([[cx-130,cy-130],[cx-130,cy+130],[cx+120,cy]],fc="#222",zorder=8))
    ax.add_patch(Polygon([[cx+120,cy],[4054,7300],[4054,8800]],fc="#FFD60A",alpha=.12,ec="none",zorder=2))
    dim(ax,cx+140,cy,3640,cy,"",c="#8A6D00"); T(ax,2950,cy-230,"촬영거리 약 2.0m",fs=5.0,c="#8A6D00",ha="right")
    T(ax,1700,8300,"카메라/삼각대\n(→ 책장)",fs=4.6,ha="left")
    ax.add_patch(Circle((2300,7500),110,fc="#FFD60A",ec="#B58B00",zorder=8)); T(ax,2440,7500,"키 라이트",fs=4.6,ha="left")
    ax.add_patch(Circle((2200,8650),90,fc="#FFE066",ec="#B58B00",zorder=8)); T(ax,2080,8650,"보조 조명",fs=4.4,ha="right")
    R(ax,0,7700,35,1000,"#8B95A1",z=6)
    # 대표석 (창가, ㄱ자의 가로 끝) — 모션데스크 + Mac Studio
    R(ax,3000,9050,1500,700,"#FFFFFF","#F04452",2,z=5); T(ax,3750,9560,"대표 모션데스크(보유)",fs=5.0,c="#B1202C")
    R(ax,3150,9110,200,200,"#C9CED6","#555",1,z=6); T(ax,3250,9210,"Mac\nStudio",fs=4.2)
    R(ax,3800,9130,330,180,"#F2F3F5","#555",.8,z=6)
    chair(ax,3750,8800,RED,r=200); T(ax,3750,8800,"대표",fs=4.8,c="white")
    # 포커스석 1석 (책장 칸막이) — 서진이 구역을 접으면 한 자리 더 (2석)
    Z(ax,700,8640,1100,1160,"#D3F1F2","")
    R(ax,950,8650,700,150,"#8A6A3A","#5A3E1B",1,z=5); T(ax,1300,8560,"책장 칸막이",fs=4.6,c="#0B5C63")
    R(ax,900,9200,800,600,"#FFFFFF","#0F7E86",1.4,z=5); R(ax,900,9200,800,40,"#0F7E86",z=6)
    ax.add_patch(Circle((1300,8980),180,fc="#4DB6BD",ec="white",zorder=5)); T(ax,1300,9500,"포커스 1석",fs=5.0,c="#0B5C63",fontweight="bold")
    # 서진이 아지트 (선택, 점선) — 대표석 바로 옆
    R(ax,1800,8700,1350,1100,"#E6F9EA","#2F9E44",1.4,z=2,ls="--",alpha=.9)
    R(ax,1850,9200,1000,600,"#FFFFFF","#2F9E44",1.4,z=5,ls="--"); T(ax,2350,9500,"서진이 책상 1000×600\n(선택)",fs=4.4,c="#1F7A33")
    ax.add_patch(Circle((2350,8980),170,fc="#8CE99A",ec="#2F9E44",lw=1,ls="--",zorder=5))
    ax.add_patch(Circle((2850,8800),200,fc="#B2F2BB",ec="#2F9E44",lw=1,ls="--",zorder=5)); T(ax,2850,8800,"빈백",fs=4.4)
    # 34" 울트라와이드 모니터 (이동식 스탠드·기존 물품) — 대표석 옆, 필요하면 U 책상으로
    R(ax,3170,8700,300,200,"none","#555",1,z=6,ls="--"); R(ax,3290,8590,60,415,"#2B2F36","#111",1,z=7)
    T(ax,3040,8590,"34\" 모니터\n(이동식·기존)",fs=4.0,c="#333")
    # 로봇청소기 도크 (후방 통로 왼쪽 끝, 바닥 콘센트 옆, 기존 물품)
    R(ax,50,6900,400,350,"#EDEFF2","#555",1.2,z=5); T(ax,250,7075,"로봇청소기\n도크(기존)",fs=4.2)
    # 라운지 (왼쪽 벽): 소파 + 티테이블 + 가습기
    if mode==12: sofa(ax,50,7350,850,1800,"left","소파 3인")
    else: sofa(ax,50,7350,850,1400,"left","소파 2인")
    ax.add_patch(Circle((1300,8350),175,fc="#FFFFFF",ec="#9A7B4F",lw=1.3,zorder=5)); T(ax,1300,8350,"티\n테이블",fs=4.4)
    R(ax,1030,7380,540,540,"none","#2C7FB8",.8,z=6,ls="--")
    ax.add_patch(Circle((1300,7650),135,fc="#D6ECFA",ec="#2C7FB8",lw=1.4,zorder=7)); ax.add_patch(Circle((1300,7650),60,fc="none",ec="#2C7FB8",lw=.8,zorder=8))
    T(ax,1300,7330,"가습기 (LG 퓨리케어)",fs=4.6,c="#1F5E8F",fontweight="bold")
    # 3D 프린터 (창 쪽 왼쪽 모서리, 환기)
    R(ax,50,9200,560,540,"#FFE0B8","#E67E22",1.6,z=5); T(ax,330,9470,"3D프린터\n(창 쪽 환기)",fs=4.6,c="#8A4B00")
    # LAN: 복합기 옆 NAS/공유기 -> 왼쪽 벽 -> 대표석
    ax.plot([240,40,40],[1980,1980,6900],color=BLUE,lw=1.1,ls="--",zorder=7)
    ax.plot([40,2950,2950,3000],[6900,6900,9400,9400],color=BLUE,lw=1.1,ls="--",zorder=7)
    # aisles
    dim(ax,3100,6330,3100,7250,"뒤 통로 약 0.9~1.0m",dx=-420)
    dim(ax,3930,4300,4500,4300,"0.6m",dy=-110)
    dim(ax,0,4300,580,4300,"0.6m",dy=-110)
    dim(ax,1650,2900,2850,2900,"안쪽 1.2m",dy=-120)
    # ---------- scale, title
    R(ax,300,H+420,1000,70,INK,z=8); R(ax,1300,H+420,1000,70,"white",INK,1,z=8)
    T(ax,300,H+620,"0",fs=6.0); T(ax,1300,H+620,"1m",fs=6.0); T(ax,2300,H+620,"2m",fs=6.0)
    T(ax,2500,H+470,"축척 막대 · 치수 mm · 방 치수·문 위치는 가정(문=단변 중앙)",fs=5.8,c=GRAY,ha="left")
    ax.add_patch(Rectangle((0,0),W,H,fc="none",ec=INK,lw=3,zorder=10))
    ax.set_xlim(-250,W+250); ax.set_ylim(H+900,-350); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(f"ㄷ자(U형) 토론 배치 · {seats}석 · 가정한 방 4.5m × 9.8m = 44.1 m² (전용 44.205 m²)",fontsize=9,color=INK,loc="left",fontweight="bold")
    fig.savefig(OUT+f"layout-{mode}.png",bbox_inches="tight",facecolor="white"); plt.close(fig)
    d=[math.hypot(c[0]-3613,c[1]-350) for c in ch]
    stats[mode]=dict(seats=seats,tables=5,eye_min=round(min(d)),eye_max=round(max(d)))
stats={}
build(12); build(15)
json.dump(stats,open("/workspace/office-desk-guide/work/layout3_stats.json","w")); print(stats)
