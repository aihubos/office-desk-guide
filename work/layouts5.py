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
    BY=8400   # 전자칠판 패널 앞면 y (창 쪽, 화면은 입구를 향함)
    BX0=1046; BW=1707; BCX=BX0+BW/2
    fig,ax=plt.subplots(figsize=(4.8,4.8*(H+2850)/(W+700)),dpi=260)
    R(ax,0,0,W,H,"#FBFCFD",z=0)
    # ---------- window (bottom short wall) with 외부 펜트리 출입문 (왼쪽 끝) / door (top short wall)
    R(ax,0,H-40,100,80,"#9AD3FF","#2C7FB8",1,z=6); R(ax,1000,H-40,W-1000,80,"#9AD3FF","#2C7FB8",1,z=6)
    T(ax,2480,H+230,"창문 (바닥~천장 전면 유리)\n카메라는 창을 향하지 않음 · 블라인드 권장",fs=4.8,c="#2C7FB8",ha="left")
    R(ax,100,H-35,900,70,"#FFFFFF","#555",1.2,z=7)
    ax.add_patch(Wedge((100,H),900,270,360,fc="#FFF3BF",alpha=.6,ec="none",zorder=2))
    ax.add_patch(Arc((100,H),1800,1800,theta1=270,theta2=360,color="#888",lw=1,ls="--",zorder=7))
    ax.plot([100,100],[H,H-900],color="#555",lw=1.2,zorder=7)
    T(ax,470,H-430,"출입문\n(가정 0.9m)",fs=4.4,c="#555")
    # 외부 펜트리 (벽 밖, 실외) + 3D 프린터 우측 끝
    EX1,EY1=2400,H+1300
    R(ax,0,H+40,EX1,EY1-H-40,"#EEF1F4","#555",1.3,z=2,ls="--")
    T(ax,40,H+190,"외부 펜트리(실외 · 가정: 폭 2.4m×깊이 1.3m)",fs=4.8,c="#555",ha="left")
    R(ax,1750,H+330,560,540,"#FFE0B8","#E67E22",1.6,z=5); T(ax,2030,H+600,"3D프린터",fs=4.8,c="#8A4B00",fontweight="bold")
    T(ax,1000,H+700,"← 펜트리 우측 끝\n   (환기 걱정 없음)",fs=4.4,c="#8A4B00",ha="center")
    ax.plot([2030],[H-30],alpha=0)
    # ---------- front door
    DX0,DX1=1800,2700
    R(ax,DX0,-35,DX1-DX0,70,"#FFFFFF","#555",1.2,z=7)
    ax.add_patch(Arc((DX0,0),1800,1800,theta1=0,theta2=90,color="#888",lw=1,ls="--",zorder=7))
    ax.plot([DX0,DX0+900],[0,0],color="#555",lw=1.2,zorder=7)
    ax.add_patch(Wedge((DX0,0),900,0,90,fc="#FFF3BF",alpha=.6,ec="none",zorder=2))
    T(ax,1150,-130,"출입문(복도) · 단변 정중앙\n문 스윙 0.9m 비움",fs=5.8,c="#555")
    # ---------- 전자칠판 75" (뒤쪽 창 쪽, 화면이 입구·U 열린 쪽을 향함) 제노스미디어 CO750LT4K 패널 1707x1034
    R(ax,BX0+120,BY,BW-240,520,"#EEF1F6","#8B95A1",.9,z=4,ls="--",alpha=.7)      # 스탠드 발판(크기 가정)
    R(ax,BX0,BY,BW,110,INK,z=6)
    T(ax,BCX,BY+330,"전자칠판 75\" 제노스미디어 CO750LT4K\n(화면 ↑ 입구 쪽) 고정 스탠드",fs=4.4)
    T(ax,BCX,BY+700,"보드 뒤 약 1.0m: 전원·AV·도크 (통행 X)",fs=4.2,c=GRAY)
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
    ax.plot([1700],[H-40],marker="s",ms=4,color=OR,mec="#B86E00",zorder=8); T(ax,2100,H-120,"보드·도크 콘센트(가정)",fs=3.8,c="#B86E00",ha="left")
    # ---------- 소파 (오른쪽 벽, 칠판을 비스듬히 봄)
    SXc,SYc=3650,5780
    if mode==12: pass
    sofa(ax,SXc,SYc,850,1400,"right","소파 2인")
    ax.add_patch(Circle((3250,6500),175,fc="#FFFFFF",ec="#9A7B4F",lw=1.3,zorder=5)); T(ax,3250,6500,"티\n테이블",fs=4.4)
    R(ax,3030,5730,540,540,"none","#2C7FB8",.8,z=6,ls="--")
    ax.add_patch(Circle((3300,6000),135,fc="#D6ECFA",ec="#2C7FB8",lw=1.4,zorder=7)); ax.add_patch(Circle((3300,6000),60,fc="none",ec="#2C7FB8",lw=.8,zorder=8))
    T(ax,3260,5700,"가습기",fs=4.2,c="#1F5E8F",fontweight="bold")
    R(ax,4455,6000,45,1100,"#8B95A1",z=7)
    sx,sy=3990,6480
    ax.plot([sx,BCX],[sy,BY+55],color="#7B61FF",lw=1.1,ls="--",zorder=8)
    dsof=math.hypot(sx-BCX,sy-(BY+55))
    T(ax,2700,6850,f"소파→칠판 약 {dsof/1000:.1f}m",fs=4.8,c="#5B3FD1",fontweight="bold",bbox=dict(fc="white",ec="none",pad=.8,alpha=.9))
    # ---------- 스튜디오 (오른쪽 벽, 그대로) + 대표석 (창 쪽 오른쪽 모서리, 그대로)
    Z(ax,2150,7250,2350,1150,"#FFD9DE","")
    Z(ax,2850,8400,1650,1400,"#FFD9DE","")
    T(ax,2200,7215,"ㄱ자 조용한 구역 (스튜디오 + 대표석)",fs=4.8,ha="left",c="#B1202C",fontweight="bold")
    ax.add_patch(Polygon([(2150,7250),(4495,7250),(4495,9795),(2850,9795),(2850,8400),(2150,8400)],closed=True,fc="none",ec="#7B61FF",lw=1.0,ls=":",zorder=3))
    R(ax,4054,7300,446,1500,"#D9B88A","#8A6A3A",1.5,z=5); T(ax,4280,8050,"책장 2대(배경)",fs=5.2,rotation=90)
    ax.plot([4054,4054],[7300,8800],color="#FFD60A",lw=3,zorder=6)
    R(ax,3000,7450,500,1100,"#FFFFFF","#F04452",1.6,z=5); T(ax,3180,8000,"촬영 책상",fs=4.8,rotation=90)
    for my in (7750,8250): ax.add_patch(Circle((3300,my),50,fc="#444",ec="white",zorder=7))
    T(ax,3300,7620,"Shure",fs=4.2)
    chair(ax,3800,7700,RED,r=200); chair(ax,3800,8350,"#F5A3AB",r=200); T(ax,3800,7700,"제레미",fs=4.8,c="white"); T(ax,3800,8350,"유하님",fs=4.6,c="white")
    cx,cy=1800,8050
    ax.add_patch(Polygon([[cx-130,cy-130],[cx-130,cy+130],[cx+120,cy]],fc="#222",zorder=8))
    ax.add_patch(Polygon([[cx+120,cy],[4054,7300],[4054,8800]],fc="#FFD60A",alpha=.12,ec="none",zorder=2))
    dim(ax,cx+140,cy,3640,cy,"",c="#8A6D00"); T(ax,2950,cy-330,"촬영거리 약 2.0m",fs=5.0,c="#8A6D00",ha="right")
    T(ax,1700,7830,"카메라/삼각대 (→ 책장)\n(촬영 때만 세움)",fs=4.4,ha="left")
    ax.add_patch(Circle((2300,7500),110,fc="#FFD60A",ec="#B58B00",zorder=8)); T(ax,2440,7500,"키 라이트",fs=4.6,ha="left")
    ax.add_patch(Circle((2350,8230),90,fc="#FFE066",ec="#B58B00",zorder=8)); T(ax,2470,8230,"보조 조명",fs=4.4,ha="left")
    R(ax,0,7780,35,1000,"#8B95A1",z=6)
    R(ax,3000,9050,1500,700,"#FFFFFF","#F04452",2,z=5); T(ax,3750,9560,"대표 모션데스크(보유)",fs=5.0,c="#B1202C")
    R(ax,3150,9110,200,200,"#C9CED6","#555",1,z=6); T(ax,3250,9210,"Mac\nStudio",fs=4.2)
    R(ax,3800,9130,330,180,"#F2F3F5","#555",.8,z=6)
    chair(ax,3750,8800,RED,r=200); T(ax,3750,8800,"대표",fs=4.8,c="white")
    R(ax,3170,8700,300,200,"none","#555",1,z=6,ls="--"); R(ax,3290,8590,60,415,"#2B2F36","#111",1,z=7)
    T(ax,3040,8590,"34\" 모니터\n(이동식·기존)",fs=4.0,c="#333")
    # ---------- 포커스석 + 서진이 아지트: 왼쪽 벽 줄 (U 뒤끝 ~ 창 쪽 출입문 사이)
    Z(ax,35,5740,1180,880,"#D3F1F2","")
    R(ax,50,5780,600,800,"#FFFFFF","#0F7E86",1.4,z=5); R(ax,610,5780,40,800,"#0F7E86",z=6)
    chair2(ax,835,6180,-1,0,col="#4DB6BD",r=180)
    R(ax,1030,5780,150,800,"#8A6A3A","#5A3E1B",1,z=5); T(ax,1105,6180,"책장 칸막이",fs=4.4,c="#0B5C63",rotation=90,z=9)
    T(ax,350,5690,"포커스 1석",fs=4.8,c="#0B5C63",fontweight="bold")
    R(ax,40,6620,1160,1160,"#E6F9EA","#2F9E44",1.4,z=2,ls="--",alpha=.9)
    R(ax,50,6650,600,1000,"#FFFFFF","#2F9E44",1.4,z=5,ls="--"); T(ax,350,7150,"서진이 책상\n1000×600\n(선택)",fs=4.2,c="#1F7A33",rotation=90)
    ax.add_patch(Circle((835,7150),170,fc="#8CE99A",ec="#2F9E44",lw=1,ls="--",zorder=5))
    ax.add_patch(Circle((900,7560),200,fc="#B2F2BB",ec="#2F9E44",lw=1,ls="--",zorder=5)); T(ax,900,7560,"빈백",fs=4.4)
    # 로봇청소기 도크 (보드 뒤 데드존, 기존)
    R(ax,1500,9250,400,350,"#EDEFF2","#555",1.2,z=5); T(ax,1700,9425,"로봇청소기\n도크(기존)",fs=4.0)
    # LAN: 복합기 옆 NAS/공유기 -> 왼쪽 벽 -> 포커스·서진이, 앞 벽 위 -> 대표석(천장 쪽 경로 가정)
    ax.plot([240,40,40],[1980,1980,7000],color=BLUE,lw=1.1,ls="--",zorder=7)
    ax.plot([430,640,640],[1900,1900,4950],color=BLUE,lw=.01,alpha=0)
    ax.plot([40,40,1200,2800,2950,3000],[7000,8000,8000,9100,9400,9400],color=BLUE,lw=1.1,ls="--",zorder=7,alpha=.0)
    ax.plot([40,40],[7000,8250],color=BLUE,lw=1.1,ls="--",zorder=7)
    ax.plot([40,1000,1000,2950,2950,3000],[8250,8250,9150,9150,9400,9400],color=BLUE,lw=1.1,ls="--",zorder=7)
    # aisles
    dim(ax,3565,3300,4500,3300,"통로 0.93m",dy=-110)
    dim(ax,0,3540,235,3540,"0.24m")
    dim(ax,1250,3900,2550,3900,"",c=GRN)
    dim(ax,40,8200,1046,8200,"문 통로 1.0m",dy=-110)
    dim(ax,1300,2950,2500,2950,"안쪽 1.2m",dy=-120)
    # ---------- scale, title
    SY=H+1750
    R(ax,300,SY,1000,70,INK,z=8); R(ax,1300,SY,1000,70,"white",INK,1,z=8)
    T(ax,300,SY+200,"0",fs=6.0); T(ax,1300,SY+200,"1m",fs=6.0); T(ax,2300,SY+200,"2m",fs=6.0)
    T(ax,2500,SY+50,"축척 막대 · 치수 mm · 방 치수·문·펜트리는 가정",fs=5.6,c=GRAY,ha="left")
    ax.add_patch(Rectangle((0,0),W,H,fc="none",ec=INK,lw=3,zorder=10))
    ax.set_xlim(-250,W+250); ax.set_ylim(SY+450,-350); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(f"ㄷ자(U형) 토론 배치(상석이 입구 쪽) · {seats}석 · 가정한 방 4.5m × 9.8m = 44.1 m² (전용 44.205 m²)",fontsize=8.6,color=INK,loc="left",fontweight="bold")
    fig.savefig(OUT+f"layout-{mode}.png",bbox_inches="tight",facecolor="white"); plt.close(fig)
    bc=(BCX,BY+55)
    d=[math.hypot(c[0]-bc[0],c[1]-bc[1]) for c in ch]
    def turn(c):
        fx,fy=(c[2],c[3]) ; vx,vy=bc[0]-c[0],bc[1]-c[1]
        return math.degrees(math.acos((fx*vx+fy*vy)/math.hypot(vx,vy)))
    leg=[turn(c) for c in ch if c[2]!=0]; head=[turn(c) for c in ch if c[3]!=0]
    stats[mode]=dict(seats=seats,tables=5,eye_min=round(min(d)),eye_max=round(max(d)),
        leg_turn_min=round(min(leg)),leg_turn_max=round(max(leg)),head_turn=round(max(head)),
        sofa_dist=round(dsof),
        sofa_off_axis=round(math.degrees(math.acos((BY+55-sy)*-1/-dsof))) if False else round(math.degrees(math.acos(abs(BY+55-sy)/dsof))))
stats={}
build(12); build(15)
json.dump(stats,open("/workspace/office-desk-guide/work/layout3_stats.json","w")); print(stats)
