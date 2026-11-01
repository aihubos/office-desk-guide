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
    # ---------- front wall: TV, screen
    R(ax,2830,130,1440,70,INK,z=6)
    R(ax,3250,200,600,400,"#B0B8C1","#8B95A1",1,z=5); T(ax,3550,400,"TV 65\"\n이동식 스탠드",fs=6.0)
    ax.plot([2715,4485],[18,18],color="#7B61FF",lw=3.2,zorder=8)
    T(ax,3650,-150,"전동 스크린 80\"(선택·문 오른쪽)",fs=5.8,c="#5B3FD1")
    # ---------- service wall (left, front)
    R(ax,50,820,555,640,"#E5E8EB","#8B95A1",1.2,z=5); T(ax,330,1140,"냉장고",fs=6.0)
    R(ax,50,1500,450,900,"#FFFFFF","#8B95A1",1.2,z=5); T(ax,275,1950,"커피머신\n+선반",fs=5.8)
    R(ax,50,2440,460,380 ,"#FFFFFF","#2D6A4F",1.6,z=5); T(ax,280,2630,"복합기",fs=5.8)
    Z(ax,0,780,640,2100,"#CDEFD9","")
    T(ax,610,1650,"탕비·복합기",fs=5.6,c="#1B5E3A",fontweight="bold",rotation=90)
    R(ax,50,50,550,600,"#C9B5F2","#6F42C1",1.5,z=5); T(ax,325,350,"NAS\n공유기",fs=5.8,c="#3D1E8F")
    # whiteboard parked
    R(ax,4350,750,100,1500,"#FFFFFF","#444",1.5,z=5); T(ax,4290,1500,"이동식 화이트보드(주차)",fs=5.0,rotation=90)
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
    # ---------- rear zone
    LANp=[]
    if mode==12:
        # studio + CEO desk (right wall)
        Z(ax,2650,7250,1850,1700,"#FFD9DE","",)
        T(ax,2700,7210,"대표석 + 스튜디오 (책장 배경)",fs=6.0,ha="left",c="#B1202C",fontweight="bold")
        R(ax,2700,7300,800,1600,"#FFFFFF","#F04452",2,z=5)
        R(ax,2830,7440,200,200,"#C9CED6","#555",1,z=6); T(ax,2930,7540,"Mac\nStudio",fs=4.6)
        R(ax,3050,7900,190,330,"#F2F3F5","#555",.8,z=6); T(ax,3145,8065,"키보드",fs=4.4,rotation=90)
        ax.add_patch(Circle((3150,8400),55,fc="#F2F3F5",ec="#555",zorder=6))
        T(ax,2780,8300,"모션데스크(보유)",fs=5.0,c="#B1202C",rotation=90)
        R(ax,4054,7300,446,1600,"#D9B88A","#8A6A3A",1.5,z=5); T(ax,4280,8100,"책장 2대(배경)",fs=5.6,rotation=90)
        ax.plot([4054,4054],[7300,8900],color="#FFD60A",lw=3,zorder=6)
        chair(ax,3800,7700,RED,r=200); chair(ax,3800,8400,"#F5A3AB",r=200); T(ax,3800,7700,"제레미",fs=4.8,c="white"); T(ax,3800,8400,"유하님",fs=4.6,c="white")
        cx,cy=1800,8050
        ax.add_patch(Polygon([[cx-130,cy-130],[cx-130,cy+130],[cx+120,cy]],fc="#222",zorder=8))
        ax.add_patch(Polygon([[cx+120,cy],[4054,7300],[4054,8900]],fc="#FFD60A",alpha=.12,ec="none",zorder=2))
        dim(ax,cx+140,cy,3640,cy,"",c="#8A6D00"); T(ax,2670,cy+250,"촬영거리 약 2.0m",fs=5.6,c="#8A6D00",ha="right")
        T(ax,cx-60,cy-300,"카메라/삼각대(→ 책장)",fs=5.4,ha="center")
        ax.add_patch(Circle((2200,7450),110,fc="#FFD60A",ec="#B58B00",zorder=8)); T(ax,2200,7220,"키 라이트",fs=5.2)
        ax.add_patch(Rectangle((2150,8820),230,60,fc="#FFD60A",ec="#B58B00",zorder=8)); T(ax,2420,8850,"LED 패널",fs=5.0,ha="left")
        R(ax,4455,6350,45,800,"#8B95A1",z=6); T(ax,4380,6750,"흡음재(선택)",fs=5.0,c=GRAY,rotation=90)
        plug(ax,3560,7230,250,60)
        # focus room (left wall)
        Z(ax,0,7200,1250,2600,"#D3F1F2","",)
        T(ax,40,7160,"포커스룸 (드롭인 3석)",fs=6.0,ha="left",c="#0B5C63",fontweight="bold")
        for i in range(3):
            y=7300+i*800
            R(ax,0,y,600,800,"#FFFFFF","#0F7E86",1.4,z=5); R(ax,590,y,50,800,"#0F7E86",z=6)
            ax.add_patch(Circle((930,y+400),180,fc="#4DB6BD",ec="white",zorder=5))
            R(ax,60,y+250,60,300,"#222",z=6)
        plug(ax,10,9650,60,100)
        # lounge
        sofa(ax,1300,8950,1800,850,"down","소파 3인")
        ax.add_patch(Circle((1900,8650),175,fc="#FFFFFF",ec="#9A7B4F",lw=1.3,zorder=5)); T(ax,1900,8650,"티\n테이블",fs=4.6)
        bean(ax,3500,9380)
        T(ax,3500,9040,"라운지",fs=6.0,c="#8A5A1F",fontweight="bold")
        # maker
        R(ax,3920,9150,560,540,"#FFE0B8","#E67E22",1.6,z=5); T(ax,4200,9420,"3D프린터\n(창 쪽 환기)",fs=5.0,c="#8A4B00")
        Z(ax,3880,9000,620,800,"#FFE9CC","",); T(ax,4190,9010,"maker",fs=5.0,c="#8A4B00")
        # LAN lines
        ax.plot([325,325,40,40],[650,780,780,7300],color=BLUE,lw=1.1,ls="--",zorder=7)
        ax.plot([40,40,1500,1500,2700],[6900,6900,6900,7600,7600],color=BLUE,lw=1.1,ls="--",zorder=7)
        ax.plot([40,40],[6900,7300],color=BLUE,lw=1.1,ls="--",zorder=7)
        # aisles
        dim(ax,3100,6330,3100,7250,"뒤 통로 0.9m",dx=-330)
        dim(ax,3930,4300,4500,4300,"0.6m",dy=-110)
        dim(ax,0,4300,580,4300,"0.6m",dy=-110)
        dim(ax,1650,2900,2850,2900,"안쪽 1.2m",dy=-120)
    else:
        # 15: window strip
        R(ax,2850,9200,1600,600,"#FFFFFF","#F04452",2,z=5); T(ax,3650,9500,"대표 모션데스크(보유)·Mac Studio",fs=5.0,c="#B1202C")
        chair(ax,3650,8960,RED,r=200)
        R(ax,0,8300,446,1500,"#D9B88A","#8A6A3A",1.5,z=5); T(ax,230,9050,"책장",fs=5.6,rotation=90)
        Z(ax,450,8700,1900,1100,"#D3F1F2","",)
        T(ax,480,8660,"포커스룸 (2석)",fs=5.6,ha="left",c="#0B5C63",fontweight="bold")
        for i in range(2):
            x=500+i*950
            R(ax,x,9250,900,550,"#FFFFFF","#0F7E86",1.4,z=5); R(ax,x,9200,900,50,"#0F7E86",z=6)
            ax.add_patch(Circle((x+450,8870+0),0,fc="none"))
        for x in (950,1900): chair(ax,x,8960,"#4DB6BD",r=170)
        R(ax,50,7300,560,540,"#FFE0B8","#E67E22",1.6,z=5); T(ax,330,7570,"3D프린터\n(창에서 멀어\n환기 곤란)",fs=4.8,c="#8A4B00")
        bean(ax,3750,1300); bean(ax,3750,1880)
        sofa(ax,3650,7300,850,1400,"right","소파 2인")
        T(ax,3480,8000,"소파 850×1400(추정)\n오른쪽 벽 등받이",fs=4.6,c="#8A5A1F",ha="right")
        ax.plot([325,325,40,40],[650,780,780,7300],color=BLUE,lw=1.1,ls="--",zorder=7)
        T(ax,450,8420,"※ 15석: 스튜디오·티테이블 제외 (소파는 오른쪽 벽)",fs=5.2,c="#B1202C",ha="left")
        dim(ax,2250,6330,2250,7300,"뒤 통로 약 1.0m",dx=-300)
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
    d=[math.hypot(c[0]-3550,c[1]-400) for c in ch]
    stats[mode]=dict(seats=seats,tables=5,eye_min=round(min(d)),eye_max=round(max(d)))
stats={}
build(12); build(15)
json.dump(stats,open("/workspace/office-desk-guide/work/layout3_stats.json","w")); print(stats)
