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
    from shapely.geometry import Polygon as SP
    import sys; sys.path.insert(0,"/workspace")
    from geom import UP as UPG, board as gboard
    _pn,_st,_n=gboard((2300,7050),-55); ugap=_pn.union(_st).distance(UPG)
    fig,ax=plt.subplots(figsize=(4.8,4.8*(H+2850)/(W+700)),dpi=260)
    R(ax,0,0,W,H,"#FBFCFD",z=0)
    # ---------- window (bottom short wall) with 외부 펜트리 출입문 (왼쪽 끝) / door (top short wall)
    R(ax,0,H-40,100,80,"#9AD3FF","#2C7FB8",1,z=6); R(ax,1000,H-40,W-1000,80,"#9AD3FF","#2C7FB8",1,z=6)
    T(ax,1900,H+650,"창문 (바닥~천장 전면 유리)\n카메라는 창을 향하지 않음 · 블라인드 권장",fs=4.8,c="#2C7FB8",ha="center")
    R(ax,100,H-35,900,70,"#FFFFFF","#555",1.2,z=7)
    ax.add_patch(Wedge((100,H),900,270,360,fc="#FFF3BF",alpha=.6,ec="none",zorder=2))
    ax.add_patch(Arc((100,H),1800,1800,theta1=270,theta2=360,color="#888",lw=1,ls="--",zorder=7))
    ax.plot([100,100],[H,H-900],color="#555",lw=1.2,zorder=7)
    T(ax,470,H-430,"출입문\n(가정 0.9m)",fs=4.4,c="#555")
    # 외부 펜트리 (벽 밖, 실외) + 3D 프린터 우측 끝
    EX1,EY1=W,H+1300
    R(ax,0,H+40,EX1,EY1-H-40,"#EEF1F4","#555",1.3,z=2,ls="--")
    T(ax,40,H+190,"외부 펜트리(실외 · 가정: 폭 4.5m=사무실 폭 · 깊이 1.3m 가정)",fs=4.8,c="#555",ha="left")
    R(ax,3820,H+330,560,540,"#FFE0B8","#E67E22",1.6,z=5); T(ax,4100,H+600,"3D프린터",fs=4.8,c="#8A4B00",fontweight="bold")
    T(ax,3350,H+620,"펜트리 우측 끝 →\n(환기 걱정 없음)",fs=4.4,c="#8A4B00",ha="center")
    ax.plot([4100],[H-30],alpha=0)
    # ---------- front door
    DX0,DX1=1800,2700
    R(ax,DX0,-35,DX1-DX0,70,"#FFFFFF","#555",1.2,z=7)
    ax.add_patch(Arc((DX0,0),1800,1800,theta1=0,theta2=90,color="#888",lw=1,ls="--",zorder=7))
    ax.plot([DX0,DX0+900],[0,0],color="#555",lw=1.2,zorder=7)
    ax.add_patch(Wedge((DX0,0),900,0,90,fc="#FFF3BF",alpha=.6,ec="none",zorder=2))
    T(ax,1150,-130,"출입문(복도) · 단변 정중앙\n문 스윙 0.9m 비움",fs=5.8,c="#555")
    # ---------- 전자칠판 75" : 소파 앞, 화면이 북동쪽(소파·U 열린 쪽)을 향함 (55도 비스듬히) — 제노스미디어 CO750LT4K 패널 1707x1034
    BPHI=-55
    bn=(math.cos(math.radians(BPHI)),math.sin(math.radians(BPHI))); bt=(-bn[1],bn[0])
    BC=(2300,7050)
    BP=lambda u,v:(BC[0]+u*bt[0]+v*bn[0],BC[1]+u*bt[1]+v*bn[1])
    ax.add_patch(Polygon([BP(-733,-110),BP(733,-110),BP(733,-520),BP(-733,-520)],closed=True,fc="#EEF1F6",ec="#8B95A1",lw=.9,ls="--",zorder=4,alpha=.7))
    ax.add_patch(Polygon([BP(-853,0),BP(853,0),BP(853,-110),BP(-853,-110)],closed=True,fc=INK,ec=INK,zorder=6))
    sc=BP(0,-330); T(ax,sc[0],sc[1],"전자칠판 75\"\n제노스미디어 CO750LT4K\n(스탠드 크기·바퀴 가정)",fs=4.0,rotation=-35,c=INK)
    ax.annotate("",xy=BP(0,520),xytext=BP(0,40),arrowprops=dict(arrowstyle="-|>",color="#7B61FF",lw=1.3),zorder=8)
    bp2=BP(0,640); T(ax,bp2[0]+150,bp2[1]-60,"화면 방향\n(소파 + U 열린 쪽)",fs=4.2,c="#5B3FD1",fontweight="bold")
    # ---------- 탕비: 입구(문) 왼쪽 앞 벽에 한 줄
    R(ax,50,50,555,637,"#E5E8EB","#8B95A1",1.2,z=5); T(ax,330,370,"냉장고\nRT20FARL3S9",fs=4.2)
    R(ax,620,50,880,600,"#FFFFFF","#8B95A1",1.2,z=5); T(ax,1060,590,"카운터 + 선반",fs=4.4)
    R(ax,660,100,168,400,"#BFEFF2","#0E7C86",1.4,z=7); T(ax,744,300,"정수기",fs=4.8,c="#0E6B73",rotation=90,fontweight="bold")
    R(ax,900,110,420,300,"#D9DDE2","#555",1,z=6); T(ax,1110,260,"커피머신",fs=5.0)
    R(ax,50,690,1450,800,"#FFF3BF","none",0,z=1,alpha=.35)
    T(ax,1000,950,"탕비 이용·대기 공간\n(문 열림과 안 겹침)",fs=4.6,c="#8A6D00")
    R(ax,50,1750,380,460,"#FFFFFF","#2D6A4F",1.6,z=5); T(ax,240,1980,"복합기",fs=4.6); T(ax,450,1990,"위 선반\nNAS + ASUS\nRT-BE92U",fs=4.0,c="#5B3FD6",ha="left")
    R(ax,50,1050,620,600,"none","#7A5BD8",1.3,z=6,ls="--"); T(ax,360,1350,"스타일러\n(선택·후보)\n600×620\n열면 1.19m",fs=4.2,c="#5B3FD1")
    # 공기청정기 (문 오른쪽 앞 모서리) LG AS186HWWL
    PX,PY=4190,1200
    R(ax,PX-307,PY-307,614,614,"none","#0E7C86",.8,z=6,ls="--")
    ax.add_patch(Circle((PX,PY),157,fc="#E6F7F8",ec="#0E7C86",lw=1.4,zorder=7)); ax.add_patch(Circle((PX,PY),75,fc="none",ec="#0E7C86",lw=.8,zorder=8))
    T(ax,PX-60,PY-470,"공기청정기\n(LG 퓨리케어 360°)",fs=4.4,c="#0E6B73",fontweight="bold")
    T(ax,3350,520,"비워 둔 앞 벽 오른쪽\n(외투·택배 후보)",fs=4.6,c=GRAY)
    T(ax,2250,1420,"▼ 문을 열면 ㄷ자 상석이 바로 보여요",fs=5.0,c="#1F5FBF",fontweight="bold")
    # CCTV
    def cam(x,y,c,fov,rad,n):
        ax.add_patch(Wedge((x,y),rad,c-fov/2,c+fov/2,fc="#FF6B6B",alpha=.10,ec="#E03131",lw=.7,ls="--",zorder=2))
        ax.add_patch(Circle((x,y),95,fc="#E03131",ec="white",lw=1,zorder=9)); T(ax,x,y,"▣",fs=4.2,c="white",z=10)
    cam(2750,70,135,90,2550,"1"); T(ax,2480,330,"CCTV 1 입구·탕비",fs=4.6,c="#C92A2A",fontweight="bold",ha="center")
    cam(4430,4000,180,70,3800,"2"); T(ax,4150,3840,"CCTV 2 책상·U",fs=4.8,c="#C92A2A",fontweight="bold",ha="right")
    # ---------- ceiling AC + floor outlet
    ax.add_patch(Circle((2250,4950),260,fc="none",ec="#9AA5B1",lw=1,ls="--",zorder=4)); T(ax,2250,4950,"천장형\n에어컨",fs=5.2,c="#9AA5B1")
    FX,FY=900,4950
    ax.plot([FX],[FY],marker="o",ms=7,color="#FF9F1C",mec="#B86E00",zorder=9)
    T(ax,1000,5200,"바닥 콘센트\n(대략)",fs=4.0,c="#B86E00",z=9)
    # ---------- learners: ㄷ자를 뒤집음 — 막힌 쪽(1200x600 상석)이 입구 쪽, 열린 쪽이 뒤(전자칠판)
    UP=[(700,2100),(3100,2100),(3100,5700),(2500,5700),(2500,2700),(1300,2700),(1300,5700),(700,5700)]
    if mode==12:
        ch=[(440,2460+720*i,1,0) for i in range(5)]+[(3360,2460+720*i,-1,0) for i in range(5)]+[(1500,1840,0,1),(2300,1840,0,1)]
    else:
        ch=[(440,2460+600*i,1,0) for i in range(6)]+[(3360,2460+600*i,-1,0) for i in range(6)]+[(1100,1840,0,1),(1900,1840,0,1),(2700,1840,0,1)]
    Z(ax,235,1635,3330,4250,"#DCEBFF","")
    ax.add_patch(Polygon(UP,closed=True,fc=WOOD,ec=EC,lw=2.2,zorder=4,joinstyle="round"))
    for (x1,y1,x2,y2) in [(700,3900,1300,3900),(2500,3900,3100,3900),(1300,2100,1300,2700),(2500,2100,2500,2700)]:
        ax.plot([x1,x2],[y1,y2],color=EC,lw=.9,zorder=5)
    for (tx,ty) in [(1000,3000),(1000,4800),(2800,3000),(2800,4800)]: T(ax,tx,ty,"1800×600",fs=5.0,c="#6B5530",rotation=90)
    T(ax,1900,2400,"1200×600 (상석 · 추가)",fs=4.8,c="#6B5530")
    for (cx,cy,fx,fy) in ch: chair2(ax,cx,cy,fx,fy)
    T(ax,1900,4300,f"U 안쪽 발표·토론 공간\n(폭 1.2m · 열린 쪽이 뒤 전자칠판)\n교육존 {seats}석",fs=5.8,c="#1F5FBF",fontweight="bold")
    ax.annotate("",xy=(1900,5450),xytext=(1900,3550),arrowprops=dict(arrowstyle="-|>",color="#1F5FBF",lw=1.4),zorder=8)
    for (x,y,o) in [(1230,2800,"v"),(1230,4750,"v"),(2500,2800,"v"),(2500,4750,"v"),(1600,2630,"h")]:
        if o=="v": R(ax,x,y,70,300,"#FF9F1C","#B86E00",.8,z=7)
        else: R(ax,x,y,300,70,"#FF9F1C","#B86E00",.8,z=7)
    OR="#FF9F1C"
    ax.plot([FX,1265,1265],[FY,FY,2800],color=OR,lw=.9,ls=":",zorder=7)
    ax.plot([1265,1265,1600],[2800,2665,2665],color=OR,lw=.9,ls=":",zorder=7)
    ax.plot([1900,2535,2535,2535],[2665,2665,2800,4900],color=OR,lw=.9,ls=":",zorder=7)
    for (ox,oy) in [(W-40,3500),(W-40,5300),(40,7000),(W-40,7600),(W-40,2300)]: outlet(ax,ox,oy)
    # ---------- 라운지: 소파는 오른쪽 벽, 전자칠판을 마주 봄 (소파 위 끝 y=6450: 오른쪽 통로가 막히지 않게)
    sofa(ax,3650,6450,850,1400,"right","소파 2인")
    ax.add_patch(Circle((3390,7050),150,fc="#FFFFFF",ec="#9A7B4F",lw=1.3,zorder=5)); T(ax,3390,7050,"티",fs=4.2)
    R(ax,3070,7430,540,540,"none","#2C7FB8",.8,z=6,ls="--")
    ax.add_patch(Circle((3340,7700),135,fc="#D6ECFA",ec="#2C7FB8",lw=1.4,zorder=7)); ax.add_patch(Circle((3340,7700),60,fc="none",ec="#2C7FB8",lw=.8,zorder=8))
    T(ax,3340,7490,"가습기",fs=4.2,c="#1F5E8F",fontweight="bold")
    R(ax,4455,6600,45,1100,"#8B95A1",z=7)
    sx,sy=3990,7150
    ax.plot([sx,BC[0]],[sy,BC[1]],color="#7B61FF",lw=1.1,ls="--",zorder=8)
    dsof=math.hypot(sx-BC[0],sy-BC[1])
    T(ax,3050,6700,f"소파→칠판 약 {dsof/1000:.1f}m",fs=4.8,c="#5B3FD1",fontweight="bold",bbox=dict(fc="white",ec="none",pad=.8,alpha=.9))
    T(ax,2900,6180,"라운지 (소파 + 전자칠판)",fs=5.0,c="#6B4FBF",fontweight="bold",z=9)
    # ---------- 낮은 책장 가벽 (회의·교육존 | 대표실): 이케아 BILLY 80x28x106 x4 (벽 고정 필요)
    PY0,PY1=8000,8280
    for k,x0 in enumerate((1300,2100,2900,3700)):
        R(ax,x0,PY0,800,PY1-PY0,"#E9DCC3","#8A6A3A",1.3,z=6)
    T(ax,2900,(PY0+PY1)/2,"낮은 책장 가벽 · 빌리 80×28×106 ×4 (벽 고정)",fs=4.5,c="#5A3E1B",fontweight="bold",z=9)
    # ---------- 대표실 (가벽 뒤, 창 쪽)
    Z(ax,1300,PY1,3200,H-PY1,"#FFE8EC","")
    T(ax,1360,PY1+110,"대표실 (가벽 뒤)",fs=4.8,ha="left",c="#B1202C",fontweight="bold")
    # 대표 모션데스크: 오른쪽 벽 끝(뒤 오른쪽 모서리), 제레미는 서쪽에서 동쪽(벽)을 보고 앉음 -> 화면은 서쪽 = 입구에선 옆면
    R(ax,3800,8300,700,1500,"#FFFFFF","#F04452",2,z=5); T(ax,4390,9150,"대표 데스크(보유) 1500×700",fs=4.0,c="#B1202C",rotation=90)
    R(ax,4250,8420,200,200,"#C9CED6","#555",1,z=6); T(ax,4350,8520,"Mac\nStudio",fs=3.8)
    R(ax,3950,8650,60,800,"#2B2F36","#111",1,z=7); T(ax,4090,9050,"34\" 모니터",fs=4.0,c="#333",rotation=90)
    chair(ax,3450,9050,RED,r=200); T(ax,3450,9050,"대표",fs=4.8,c="white")
    ax.annotate("",xy=(3820,9050),xytext=(3680,9050),arrowprops=dict(arrowstyle="-|>",color=RED,lw=1.2),zorder=8)
    ax.annotate("",xy=(3560,8600),xytext=(3900,8600),arrowprops=dict(arrowstyle="-|>",color="#7B61FF",lw=1.1),zorder=8)
    T(ax,3300,8450,"화면은 서쪽 향함\n(입구에선 옆·뒷면)",fs=4.0,c="#5B3FD1",ha="center")
    # 서진이 책상 (필수): 창 쪽 벽, 대표 책상 옆
    R(ax,2050,9200,1000,600,"#FFFFFF","#2F9E44",1.8,z=5); T(ax,2550,9500,"서진이 책상 1000×600",fs=4.4,c="#1F7A33")
    R(ax,2300,9250,300,60,"#2B2F36","#111",1,z=7)
    chair2(ax,2550,9050,0,1,col="#4DB6BD",r=190); T(ax,2550,9050,"서진",fs=4.2,c="white")
    # 로봇청소기 도크 (창 쪽 왼쪽 끝)
    R(ax,1350,9350,400,350,"#EDEFF2","#555",1.2,z=5); T(ax,1550,9525,"로봇청소기\n도크(기존)",fs=4.0)
    T(ax,1750,8800,"촬영 코너(선택): 고정 자리 없음\n필요할 때만 이동 설치",fs=4.0,c="#8A6D00",ha="center")
    # LAN: 복합기 옆 NAS/공유기 -> 왼쪽 벽 -> 가벽 뒤쪽 -> 서진이·대표석 (벽·천장 경로 가정)
    ax.plot([240,40,40],[1980,1980,8340],color=BLUE,lw=1.1,ls="--",zorder=7)
    ax.plot([40,3790,3790],[8340,8340,9300],color=BLUE,lw=1.1,ls="--",zorder=7)
    ax.plot([2300,2300],[8340,9190],color=BLUE,lw=1.1,ls="--",zorder=7)
    # aisles
    dim(ax,3565,3300,4500,3300,"통로 0.93m",dy=-110)
    dim(ax,0,3540,235,3540,"0.24m")
    dim(ax,1250,3900,2550,3900,"",c=GRN)
    dim(ax,0,8140,1300,8140,"창문 쪽 통로 1.3m",dy=-110)
    dim(ax,0,7056,1401,7056,"왼쪽 통로 1.4m",dy=-110)
    dim(ax,2500,5700,2500,6160,"",c=GRN)
    T(ax,2150,5930,f"U 끝↔칠판 약 {ugap/1000:.2f}m",fs=4.4,c=GRN,bbox=dict(fc="white",ec="none",pad=.6,alpha=.92))
    dim(ax,1300,2950,2500,2950,"안쪽 1.2m",dy=-120)
    # ---------- scale, title
    SY=H+1750
    R(ax,300,SY,1000,70,INK,z=8); R(ax,1300,SY,1000,70,"white",INK,1,z=8)
    T(ax,300,SY+200,"0",fs=6.0); T(ax,1300,SY+200,"1m",fs=6.0); T(ax,2300,SY+200,"2m",fs=6.0)
    T(ax,2500,SY+50,"축척 막대 · 치수 mm · 방 치수·문·펜트리는 가정",fs=5.6,c=GRAY,ha="left")
    ax.add_patch(Rectangle((0,0),W,H,fc="none",ec=INK,lw=3,zorder=10))
    ax.set_xlim(-250,W+250); ax.set_ylim(SY+450,-350); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(f"ㄷ자(U형) 토론 + 책장 가벽 · {seats}석 · 가정한 방 4.5m × 9.8m = 44.1 m²",fontsize=8.6,color=INK,loc="left",fontweight="bold")
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
    vsof=math.degrees(math.acos(((sx-bc[0])*bn[0]+(sy-bc[1])*bn[1])/dsof))
    stats[mode]=dict(seats=seats,tables=5,eye_min=round(min(d)),eye_max=round(max(d)),
        leg_turn_min=round(min(leg)),leg_turn_max=round(max(leg)),head_turn=round(max(head)),
        view_head_max=round(max(vhead)),view_leg_max=round(max(vleg)),view_leg_min=round(min(vleg)),
        sofa_dist=round(dsof),sofa_off_axis=round(vsof),u_gap=round(ugap))
stats={}
build(12); build(15)
json.dump(stats,open("/workspace/office-desk-guide/work/layout3_stats.json","w")); print(stats)
