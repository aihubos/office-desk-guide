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
    elif back=="up":
        R(ax,x,y,w,170,BK,EC2,1.2,z=6)
        R(ax,x,y+170,130,d-170,BK,EC2,1.2,z=6); R(ax,x+w-130,y+170,130,d-170,BK,EC2,1.2,z=6)
        n=3 if w>1500 else 2; cw=(w-260)/n
        for i in range(1,n): ax.plot([x+130+cw*i]*2,[y+175,y+d-20],color=EC2,lw=.9,zorder=7)
        T(ax,x+w/2,y+170+(d-170)/2,label,fs=6.0,c="#5A3E1B",fontweight="bold",z=8,bbox=dict(fc=FC,ec="none",pad=1.5))
        T(ax,x+w/2,y+85,"등받이",fs=4.2,c="#5A3E1B",z=8)
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
    seats={10:10,12:12,15:15}[mode]
    from shapely.geometry import Polygon as SP
    fig,ax=plt.subplots(figsize=(4.8,4.8*(H+2850)/(W+700)),dpi=260)
    R(ax,0,0,W,H,"#FBFCFD",z=0)
    # ---------- window (bottom short wall) with 외부 펜트리 출입문 (오른쪽 끝) / door (top short wall)
    R(ax,0,H-40,3500,80,"#9AD3FF","#2C7FB8",1,z=6); R(ax,4400,H-40,100,80,"#9AD3FF","#2C7FB8",1,z=6)
    T(ax,2900,H+900,"창문 (바닥~천장 전면 유리)\n카메라는 창을 향하지 않음 · 블라인드 권장",fs=4.8,c="#2C7FB8",ha="center")
    R(ax,3500,H-35,900,70,"#FFFFFF","#555",1.2,z=7)
    ax.add_patch(Wedge((4400,H),900,180,270,fc="#FFF3BF",alpha=.6,ec="none",zorder=2))
    ax.add_patch(Arc((4400,H),1800,1800,theta1=180,theta2=270,color="#888",lw=1,ls="--",zorder=7))
    ax.plot([4400,4400],[H,H-900],color="#555",lw=1.2,zorder=7)
    T(ax,4030,H-430,"펜트리 문\n(오른쪽 · 0.9m\n가정)",fs=4.4,c="#555")
    # 외부 펜트리 (벽 밖, 실외) + 3D 프린터 우측 끝
    EX1,EY1=W,H+1300
    R(ax,0,H+40,EX1,EY1-H-40,"#EEF1F4","#555",1.3,z=2,ls="--")
    T(ax,40,H+190,"외부 펜트리(실외 · 가정: 폭 4.5m=사무실 폭 · 깊이 1.3m 가정)",fs=4.8,c="#555",ha="left")
    R(ax,120,H+330,560,540,"#FFE0B8","#E67E22",1.6,z=5); T(ax,400,H+600,"3D프린터",fs=4.8,c="#8A4B00",fontweight="bold")
    T(ax,1500,H+470,"← 펜트리 왼쪽 끝\n(문 반대편 · 환기 걱정 없음)",fs=4.4,c="#8A4B00",ha="center")
    ax.plot([4100],[H-30],alpha=0)
    # ---------- front door
    DX0,DX1=1800,2700
    R(ax,DX0,-35,DX1-DX0,70,"#FFFFFF","#555",1.2,z=7)
    ax.add_patch(Arc((DX0,0),1800,1800,theta1=0,theta2=90,color="#888",lw=1,ls="--",zorder=7))
    ax.plot([DX0,DX0+900],[0,0],color="#555",lw=1.2,zorder=7)
    ax.add_patch(Wedge((DX0,0),900,0,90,fc="#FFF3BF",alpha=.6,ec="none",zorder=2))
    T(ax,1150,-130,"출입문(복도) · 단변 정중앙\n문 스윙 0.9m 비움",fs=5.8,c="#555")
    # ---------- 전자칠판 75": ㄷ자 열린 쪽 끝에 붙여 정면(입구 방향)을 향함, 바로 뒤가 책장 가벽 — 제노스미디어 CO750LT4K 패널 1707x1034
    BPHI=-90
    bn=(math.cos(math.radians(BPHI)),math.sin(math.radians(BPHI))); bt=(-bn[1],bn[0])
    BC=(1850,6700)
    BP=lambda u,v:(BC[0]+u*bt[0]+v*bn[0],BC[1]+u*bt[1]+v*bn[1])
    ax.add_patch(Polygon([BP(-733,-110),BP(733,-110),BP(733,-520),BP(-733,-520)],closed=True,fc="#EEF1F6",ec="#8B95A1",lw=.9,ls="--",zorder=4,alpha=.7))
    ax.add_patch(Polygon([BP(-853,0),BP(853,0),BP(853,-110),BP(-853,-110)],closed=True,fc=INK,ec=INK,zorder=6))
    sc=BP(0,-330); T(ax,sc[0],sc[1],"전자칠판 75\"\n제노스미디어 CO750LT4K\n(스탠드 크기·바퀴 가정)",fs=4.0,c=INK)
    ax.annotate("",xy=BP(0,420),xytext=BP(0,40),arrowprops=dict(arrowstyle="-|>",color="#7B61FF",lw=1.3),zorder=8)
    T(ax,1850,6250,"화면 방향 (ㄷ자 쪽)",fs=4.4,c="#5B3FD1",fontweight="bold",bbox=dict(fc="white",ec="none",pad=.6,alpha=.85))
    from shapely.geometry import Polygon as SP2, box as SBOX
    BOARD=SP2([BP(-853,0),BP(853,0),BP(853,-110),BP(-853,-110)]).union(SP2([BP(-733,-110),BP(733,-110),BP(733,-520),BP(-733,-520)]))
    # ---------- 탕비: 입구(문) 왼쪽 앞 벽에 한 줄
    R(ax,50,50,555,637,"#E5E8EB","#8B95A1",1.2,z=5); T(ax,330,370,"냉장고\nRT20FARL3S9",fs=4.2)
    R(ax,620,50,880,600,"#FFFFFF","#8B95A1",1.2,z=5); T(ax,1060,590,"카운터 + 선반",fs=4.4)
    R(ax,660,100,168,400,"#BFEFF2","#0E7C86",1.4,z=7); T(ax,744,300,"정수기",fs=4.8,c="#0E6B73",rotation=90,fontweight="bold")
    R(ax,900,110,420,300,"#D9DDE2","#555",1,z=6); T(ax,1110,260,"커피머신",fs=5.0)
    R(ax,50,690,1130,800,"#FFF3BF","none",0,z=1,alpha=.35)
    T(ax,620,950,"탕비 이용·대기 공간\n(문 열림과 안 겹침)",fs=4.6,c="#8A6D00")
    R(ax,50,1050,620,600,"none","#7A5BD8",1.3,z=6,ls="--"); T(ax,360,1350,"스타일러\n(선택·후보)\n600×620\n열면 1.19m",fs=4.2,c="#5B3FD1")
    R(ax,3500,0,900,300,"#F6EBD7","#9A7B4F",1.3,z=6,ls="--"); T(ax,3950,150,"슬리퍼 랙(후보) 900×300",fs=4.0,c="#5A3E1B")
    # 공기청정기 (문 오른쪽 앞 모서리) LG AS186HWWL
    PX,PY=4190,1200
    R(ax,PX-307,PY-307,614,614,"none","#0E7C86",.8,z=6,ls="--")
    ax.add_patch(Circle((PX,PY),157,fc="#E6F7F8",ec="#0E7C86",lw=1.4,zorder=7)); ax.add_patch(Circle((PX,PY),75,fc="none",ec="#0E7C86",lw=.8,zorder=8))
    T(ax,PX-60,PY-470,"공기청정기\n(LG 퓨리케어 360°)",fs=4.4,c="#0E6B73",fontweight="bold")
    T(ax,3350,520,"비워 둔 앞 벽 오른쪽\n(외투·택배 후보)",fs=4.6,c=GRAY)
    T(ax,2250,650,"▼ 문을 열면 상석 책상이 바로 보여요",fs=5.0,c="#1F5FBF",fontweight="bold")
    # CCTV
    def cam(x,y,c,fov,rad,n):
        ax.add_patch(Wedge((x,y),rad,c-fov/2,c+fov/2,fc="#FF6B6B",alpha=.10,ec="#E03131",lw=.7,ls="--",zorder=2))
        ax.add_patch(Circle((x,y),95,fc="#E03131",ec="white",lw=1,zorder=9)); T(ax,x,y,"▣",fs=4.2,c="white",z=10)
    cam(2750,70,135,90,2550,"1"); T(ax,2480,330,"CCTV 1 입구·탕비",fs=4.6,c="#C92A2A",fontweight="bold",ha="center")
    cam(4430,4000,180,70,3800,"2"); T(ax,4150,3840,"CCTV 2 책상·U",fs=4.8,c="#C92A2A",fontweight="bold",ha="right")
    # ---------- ceiling AC + floor outlet
    ax.add_patch(Circle((2250,4950),260,fc="none",ec="#9AA5B1",lw=1,ls="--",zorder=4)); T(ax,2250,4950,"천장형\n에어컨",fs=5.2,c="#9AA5B1")
    FX,FY=900,5450
    ax.plot([FX],[FY],marker="o",ms=7,color="#FF9F1C",mec="#B86E00",zorder=9)
    T(ax,1000,5650,"바닥 콘센트\n(대략)",fs=4.0,c="#B86E00",z=9)
    # ---------- learners: 데스커 멀티데스크 1800x800 x5 (진짜 크기). ㄷ자를 뒤집음 — 막힌 쪽(책상 1개, 상석)이 입구 쪽, 열린 쪽이 뒤(전자칠판)
    DW,DL=800,1800                      # 책상 깊이·길이
    AY0=2200                            # 양팔 시작 y (상석 책상 뒤)
    LX,RX=700,2200                      # 왼팔·오른팔 x 시작 (안쪽 통로 = 1500~2200 = 0.7m, 중심선 M=1850)
    M=1850
    BX0,BY0=M-900,1400                  # 상석 책상(1800x800): 양팔 중심선(M)에 좌우 대칭, x 950~2750, y 1400~2200
    DESKS=[(LX,AY0,DW,DL),(LX,AY0+DL,DW,DL),(RX,AY0,DW,DL),(RX,AY0+DL,DW,DL),(BX0,BY0,DL,DW)]
    na=seats and {10:4,12:5,15:6}[mode]
    ch=[(LX-260,AY0+3600*(i+.5)/na,1,0) for i in range(na)]+[(RX+DW+260,AY0+3600*(i+.5)/na,-1,0) for i in range(na)]
    bxs={10:[M-450,M+450],12:[M-450,M+450],15:[M-600,M,M+600]}[mode]
    ch+=[(x,BY0-260,0,1) for x in bxs]
    UPG=SBOX(*DESKS[0][:2],DESKS[0][0]+DW,DESKS[0][1]+DL)
    for (x,y,w,h) in DESKS: UPG=UPG.union(SBOX(x,y,x+w,y+h))
    ugap=BOARD.distance(UPG)
    R(ax,1100,930,1500,1270,"#DCEBFF",z=1,alpha=.55); R(ax,100,AY0,3460,3685,"#DCEBFF",z=1,alpha=.55)
    for (x,y,w,h) in DESKS: R(ax,x,y,w,h,WOOD,EC,2.0,z=4)
    for (x,y,w,h) in DESKS[:4]: T(ax,x+w/2,y+h/2,"멀티데스크 1800×800",fs=5.0,c="#6B5530",rotation=90)
    T(ax,BX0+DL/2,BY0+DW/2,"멀티데스크 1800×800 (입구 쪽 상석 · 양팔 가운데)",fs=5.0,c="#6B5530")
    for (cx,cy,fx,fy) in ch: chair2(ax,cx,cy,fx,fy)
    T(ax,1690,4000,f"U 안쪽 발표·토론 통로 · 교육존 {seats}석",fs=5.4,c="#1F5FBF",fontweight="bold",rotation=90)
    ax.annotate("",xy=(2080,5700),xytext=(2080,3100),arrowprops=dict(arrowstyle="-|>",color="#1F5FBF",lw=1.4),zorder=8)
    for (x,y,o) in [(LX+DW-70,2800,"v"),(LX+DW-70,4750,"v"),(RX,2800,"v"),(RX,4750,"v"),(M-150,BY0+DW-70,"h")]:
        if o=="v": R(ax,x,y,70,300,"#FF9F1C","#B86E00",.8,z=7)
        else: R(ax,x,y,300,70,"#FF9F1C","#B86E00",.8,z=7)
    OR="#FF9F1C"
    ax.plot([FX,LX+DW-35,LX+DW-35],[FY,FY,2800],color=OR,lw=.9,ls=":",zorder=7)
    ax.plot([LX+DW-35,LX+DW-35,RX+35,RX+35],[2800,2150,2150,2800],color=OR,lw=.9,ls=":",zorder=7)
    ax.plot([RX+35,RX+35],[2800,4900],color=OR,lw=.9,ls=":",zorder=7)
    for (ox,oy) in [(W-40,3500),(W-40,5300),(40,7000),(W-40,7600),(W-40,2300)]: outlet(ax,ox,oy)
    # ---------- 낮은 책장 가벽 (칠판 바로 뒤, 왼쪽 벽에 붙이고 오른쪽 2.1m는 통로로 트임): 이케아 BILLY 80x28x106 x4 (벽 고정 필요)
    PY0,PY1=7320,7600
    for k,x0 in enumerate((0,800,1600)):
        R(ax,x0,PY0,800,PY1-PY0,"#E9DCC3","#8A6A3A",1.3,z=6)
    T(ax,1600,(PY0+PY1)/2,"낮은 책장 가벽 · 빌리 80×28×106 ×3 (벽 고정)",fs=4.2,c="#5A3E1B",fontweight="bold",z=9,bbox=dict(fc="#E9DCC3",ec="none",pad=.6))
    T(ax,1850,7270,"배선 틈 0.10m",fs=3.6,c="#6B7684",z=9)
    # 마샬 스피커(액톤 III 260x170) — 책장 가벽 위 왼쪽 끝 (높이 1.06m), 왼쪽 벽 콘센트(40,7000)에서 약 0.4m
    R(ax,200,7375,260,170,"#2B2B2B","#000",1.0,z=9); T(ax,330,7460,"마샬",fs=3.8,c="#F2C94C",z=10,fontweight="bold")
    T(ax,330,7245,"마샬 스피커\n(가벽 위)",fs=3.6,c="#2B2B2B",z=9,fontweight="bold")
    # ---------- 가벽 뒤: 대표실(창 쪽 한 줄: 모션데스크 2 + 복합기 + 대표) + 서진이. 소파는 칠판 오른쪽 벽으로 이동
    Z(ax,0,PY1,W,H-PY1,"#FFE8EC","")
    T(ax,1000,7700,"가벽 뒤: 대표실 · 서진이",fs=4.8,ha="left",c="#B1202C",fontweight="bold")
    sofa(ax,3650,6100,850,1200,"right","소파 2인(소형)")
    T(ax,3300,6560,"소파 (칠판 오른쪽 · 이전: 가벽 뒤)",fs=3.6,c="#5A3E1B",ha="center",bbox=dict(fc="white",ec="none",pad=.3,alpha=.9),z=9)
    DY=8650                                   # 창 쪽 한 줄 책상 y 8650~9350 (의자는 창 쪽)
    # 모션데스크 #2(신규, 대표와 동일 1500x700) | 복합기(가운데, 두 자리 공용) | 대표 모션데스크(보유)
    R(ax,50,DY,1500,700,"#FFFFFF","#F04452",2,z=5); T(ax,800,DY+520,"모션데스크 #2 (신규)\n1500×700 (대표와 동일)",fs=3.9,c="#B1202C")
    R(ax,50+250,DY+70,800,60,"#2B2F36","#111",1,z=7)
    chair2(ax,800,DY+900,0,-1,col="#6B7684",r=200); T(ax,800,DY+900,"자리2",fs=4.2,c="white")
    ax.annotate("",xy=(800,DY+370),xytext=(800,DY+700),arrowprops=dict(arrowstyle="-|>",color="#6B7684",lw=1.1),zorder=8)
    R(ax,1550,DY,380,460,"#FFFFFF","#2D6A4F",1.6,z=5); T(ax,1740,DY+170,"복합기",fs=4.4)
    T(ax,1740,DY+620,"위 선반\nNAS+ASUS",fs=3.4,c="#5B3FD6")
    DX=1930
    R(ax,DX,DY,1500,700,"#FFFFFF","#F04452",2,z=5); T(ax,DX+430,DY+520,"대표 모션데스크(보유)\n1500×700",fs=3.9,c="#B1202C")
    R(ax,DX+350,DY+70,800,60,"#2B2F36","#111",1,z=7); T(ax,DX+580,DY+230,"34\" 모니터\n(뒷면=입구 쪽)",fs=3.4,c="#333")
    R(ax,DX+1200,DY+210,200,200,"#C9CED6","#555",1,z=6); T(ax,DX+1300,DY+310,"Mac\nStudio",fs=3.4)
    chair2(ax,DX+750,DY+900,0,-1,col=RED,r=200); T(ax,DX+750,DY+900,"대표",fs=4.8,c="white")
    ax.annotate("",xy=(DX+750,DY+370),xytext=(DX+750,DY+700),arrowprops=dict(arrowstyle="-|>",color=RED,lw=1.2),zorder=8)
    ax.annotate("",xy=(DX+1000,DY+270),xytext=(DX+1000,DY+150),arrowprops=dict(arrowstyle="-|>",color="#7B61FF",lw=1.1),zorder=8)
    ax.plot([DX+750,2250],[DY-10,120],color=RED,lw=.9,ls=":",alpha=.55,zorder=3)
    T(ax,3000,7860,"대표 시선: 출입문 정면\n(전자칠판이 중간에서 가려요)",fs=3.9,c="#B1202C",ha="center",bbox=dict(fc="#FFE8EC",ec="none",pad=.3,alpha=.9))
    # 서진이 책상: 왼쪽 벽, 가벽 바로 뒤(세로로 세움 600x1000), 의자는 동쪽에서 서쪽(벽)을 봄
    R(ax,50,7650,600,1000,"#FFFFFF","#2F9E44",1.8,z=5); T(ax,350,8150,"서진이 책상\n1000×600",fs=4.0,c="#1F7A33",rotation=90)
    R(ax,110,7900,60,300,"#2B2F36","#111",1,z=7)
    chair2(ax,900,8150,-1,0,col="#4DB6BD",r=190); T(ax,900,8150,"서진",fs=4.2,c="white")
    # 로봇청소기 도크 + 가습기 (창 쪽, 두 의자 사이)
    R(ax,1250,9420,400,350,"#EDEFF2","#555",1.2,z=5); T(ax,1450,9595,"로봇청소기\n도크(기존)",fs=3.8)
    ax.add_patch(Circle((1950,9580),135,fc="#D6ECFA",ec="#2C7FB8",lw=1.4,zorder=7)); ax.add_patch(Circle((1950,9580),60,fc="none",ec="#2C7FB8",lw=.8,zorder=8))
    T(ax,1950,9420,"가습기",fs=3.8,c="#1F5E8F",fontweight="bold",bbox=dict(fc="#FFE8EC",ec="none",pad=.4,alpha=.9))
    # LAN: 복합기 위 NAS/공유기 -> 양옆 책상 (짧게) / 서진이는 바닥 따라
    ax.plot([1550,1400],[DY+300,DY+300],color=BLUE,lw=1.1,ls="--",zorder=7); ax.plot([1930,2080],[DY+300,DY+300],color=BLUE,lw=1.1,ls="--",zorder=7)
    ax.plot([1740,1740,660],[DY,DY-120,DY-120],color=BLUE,lw=1.1,ls="--",zorder=7)
    # aisles
    dim(ax,3465,3300,4500,3300,"통로 1.03m",dy=-110)
    dim(ax,0,3000,235,3000,""); T(ax,250,3000,"0.24m",fs=4.4,c=GRN,ha="left",bbox=dict(fc="white",ec="none",pad=.4,alpha=.9),z=10)
    dim(ax,1500,2520,2200,2520,"안쪽 0.7m",dy=-110)
    dim(ax,2400,7460,4500,7460,"",c=GRN); T(ax,3450,7380,"가벽 트임 2.1m",fs=4.6,c=GRN,bbox=dict(fc="white",ec="none",pad=.5,alpha=.92))
    dim(ax,0,6700,997,6700,"왼쪽 통로 1.0m",dy=-110)
    dim(ax,2703,6900,3650,6900,"약 0.95m",dy=-110)
    dim(ax,3430,8800,4500,8800,"통로 1.07m",dy=-110)
    dim(ax,2400,5800,2400,6700,"",c=GRN)
    T(ax,3300,6250,f"U 끝↔칠판 약 {ugap/1000:.2f}m",fs=4.6,c=GRN,bbox=dict(fc="white",ec="none",pad=.6,alpha=.92))
    # ---------- scale, title
    SY=H+1750
    R(ax,300,SY,1000,70,INK,z=8); R(ax,1300,SY,1000,70,"white",INK,1,z=8)
    T(ax,300,SY+200,"0",fs=6.0); T(ax,1300,SY+200,"1m",fs=6.0); T(ax,2300,SY+200,"2m",fs=6.0)
    T(ax,2500,SY+50,"축척 막대 · 치수 mm · 방 치수·문·펜트리는 가정",fs=5.6,c=GRAY,ha="left")
    ax.add_patch(Rectangle((0,0),W,H,fc="none",ec=INK,lw=3,zorder=10))
    ax.set_xlim(-250,W+250); ax.set_ylim(SY+450,-350); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(f"ㄷ자(U형) · 데스커 멀티데스크 ×5 · 모션데스크 ×2 · {seats}석 · 가정한 방 4.5m × 9.8m = 44.1 m²",fontsize=8.6,color=INK,loc="left",fontweight="bold")
    fig.savefig(OUT+f"layout-{mode}.png",bbox_inches="tight",facecolor="white"); plt.close(fig)
    bc=BC
    d=[math.hypot(c[0]-bc[0],c[1]-bc[1]) for c in ch]
    def turn(c):
        fx,fy=(c[2],c[3]) ; vx,vy=bc[0]-c[0],bc[1]-c[1]
        return math.degrees(math.acos((fx*vx+fy*vy)/math.hypot(vx,vy)))
    def viewoff(c):
        vx,vy=c[0]-bc[0],c[1]-bc[1]
        return math.degrees(math.acos((vx*bn[0]+vy*bn[1])/math.hypot(vx,vy)))
    leg=[turn(c) for c in ch if c[2]!=0]; head=[turn(c) for c in ch if c[3]!=0]
    vleg=[viewoff(c) for c in ch if c[2]!=0]; vhead=[viewoff(c) for c in ch if c[3]!=0]
    stats[mode]=dict(seats=seats,tables=5,eye_min=round(min(d)),eye_max=round(max(d)),
        leg_turn_min=round(min(leg)),leg_turn_max=round(max(leg)),head_turn=round(max(head)),
        view_head_max=round(max(vhead)),view_leg_max=round(max(vleg)),view_leg_min=round(min(vleg)),
        u_gap=round(ugap))
import sys
stats={}
modes=[int(a) for a in sys.argv[1:]] or [12,15]
for m in modes: build(m)
old=json.load(open("/workspace/office-desk-guide/work/layout3_stats.json"))
old.update({str(k):v for k,v in stats.items()}); stats=old
json.dump(stats,open("/workspace/office-desk-guide/work/layout3_stats.json","w")); print(stats)
