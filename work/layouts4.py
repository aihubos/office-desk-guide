import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle, Circle, Polygon, Arc
fp="/usr/share/fonts/truetype/sand-box/google/Nanum Gothic/NanumGothic-Bold.ttf"
fm.fontManager.addfont(fp); plt.rcParams["font.family"]=fm.FontProperties(fname=fp).get_name()
INK="#191F28"; GRAY="#6B7684"; BLUE="#3182F6"; WOOD="#EBD3AB"; EC="#9A7B4F"; RED="#F04452"; GRN="#0F9D7A"
W,H=5600,7900
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

def build(mode):
    seats=12 if mode==12 else 15
    fig,ax=plt.subplots(figsize=(7.6,7.6*(H+1500)/(W+700)),dpi=200)
    R(ax,0,0,W,H,"#FBFCFD",z=0)
    # ---- zones
    Z(ax,0,0,2080,740,"#CDEFD9","",)
    T(ax,60,-120,"탕비 · 복합기/프린터 코너",fs=7.3,ha="left",fontweight="bold",c="#1B5E3A")
    Z(ax,0,740,440,620,"#E3D7FA","")
    Z(ax,3700,560,1900,1780,"#FFD9DE","대표석 + 스튜디오 코너 (책장 배경)",c="#B1202C",fs=7)
    # ---- window / door
    R(ax,350,H-40,W-700,80,"#9AD3FF","#2C7FB8",1,z=6); T(ax,W/2,H+170,"창문(가정) · 창 쪽 빛이 카메라 정면에 오지 않도록",fs=6.6,c="#2C7FB8")
    R(ax,W-45,5600,90,900,"#FFFFFF","#555",1.2,z=6); T(ax,W-70,6050,"출입문\n(가정)",fs=6.3,ha="right",c="#555")
    # ---- front wall: TV, screen
    R(ax,2080,130,1440,70,INK,z=6)
    R(ax,2500,200,600,400,"#B0B8C1","#8B95A1",1,z=5); T(ax,2800,400,"TV 65\"\n이동식 스탠드",fs=6.2)
    ax.plot([1690,3910],[18,18],color="#7B61FF",lw=3.2,zorder=8)
    T(ax,2800,-120,"전동 스크린 100\"(선택·천장에서 내림)",fs=6.4,c="#5B3FD1")
    # projector ceiling
    px,py=2800,3250 if mode==12 else 3300
    ax.add_patch(Rectangle((px-150,py-90),300,180,fc="#7B61FF",ec="white",zorder=8,alpha=.9)); T(ax,px,py+260,"빔프로젝터(천장, 선택)",fs=6.2,c="#5B3FD1")
    ax.add_patch(Polygon([[px,py-90],[1690,18],[3910,18]],fc="#7B61FF",alpha=.08,ec="#7B61FF",lw=.6,ls="--",zorder=2))
    # service wall
    R(ax,50,50,555,637,"#E5E8EB","#8B95A1",1.2,z=5); T(ax,330,370,"냉장고",fs=6.3)
    R(ax,650,50,900,450,"#FFFFFF","#8B95A1",1.2,z=5); T(ax,1100,275,"커피머신+선반",fs=6.1)
    R(ax,1580,50,460,420,"#FFFFFF","#2D6A4F",1.6,z=5); T(ax,1810,260,"복합기",fs=6.3)
    R(ax,1580,520,460,200,"#FFFFFF","#2D6A4F",1,z=5,ls="--"); T(ax,1810,625,"프린터(나중)",fs=5.6,c="#2D6A4F")
    R(ax,0,800,330,500,"#C9B5F2","#6F42C1",1.5,z=5); T(ax,165,1050,"NAS\n공유기",fs=5.8,c="#3D1E8F")
    # whiteboard parked
    R(ax,820,1500,1800,110,"#FFFFFF","#444",1.5,z=5); T(ax,1720,1740,"이동식 화이트보드(양면·캐스터)\n수업 때 TV 옆으로",fs=5.9)
    # ---- CEO + studio
    R(ax,3800,800,800,1600,"#FFFFFF","#F04452",2,z=5)
    R(ax,4130,980,200,200,"#C9CED6","#555",1,z=6); T(ax,4230,1080,"Mac\nStudio",fs=4.8)
    R(ax,4330,1350,200,330,"#F2F3F5","#555",.8,z=6); T(ax,4430,1520,"키보드",fs=4.6,rotation=90)
    ax.add_patch(Circle((4430,1850),55,fc="#F2F3F5",ec="#555",zorder=6))
    T(ax,3900,1600,"대표 모션데스크(보유) 1600×800",fs=5.6,c="#B1202C",rotation=90)
    R(ax,5154,700,446,1600,"#D9B88A","#8A6A3A",1.5,z=5); T(ax,5380,1500,"책장 2대(배경)",fs=6,rotation=90)
    chair(ax,4900,1250,RED); chair(ax,4900,1950,"#F5A3AB"); T(ax,4900,1250,"제레미",fs=5.2,c="white"); T(ax,4900,1950,"유하님",fs=5.2,c="white")
    ax.plot([5154,5154],[700,2300],color="#FFD60A",lw=3,zorder=6)
    cx,cy=2900,1500
    ax.add_patch(Polygon([[cx-130,cy-130],[cx-130,cy+130],[cx+120,cy]],fc="#222",zorder=8))
    ax.add_patch(Polygon([[cx+120,cy],[4800,650],[4800,2250]],fc="#FFD60A",alpha=.12,ec="none",zorder=2))
    dim(ax,cx+140,cy,4730,cy,"",c="#8A6D00"); T(ax,3350,cy-130,"촬영거리 약 2.0m",fs=6.3,c="#8A6D00")
    T(ax,cx+20,cy-330,"카메라/삼각대",fs=5.8)
    ax.add_patch(Circle((3300,500),120,fc="#FFD60A",ec="#B58B00",zorder=8)); T(ax,3300,740,"키 라이트",fs=5.8)
    ax.add_patch(Rectangle((3250,2310),220,60,fc="#FFD60A",ec="#B58B00",zorder=8)); T(ax,3060,2200,"LED 패널",fs=5.8)
    T(ax,4700,150,"흡음재(선택)",fs=5.6,c=GRAY); R(ax,3950,20,1500,40,"#8B95A1",z=6)
    plug(ax,4650,2330,250,60)
    # ---- learners: U layout
    tables=[]; chairs=[]
    if mode==12:
        ltab=[(100,2300)]; rtab=[(4700,2300)]; btab=[(900,4900),(2700,4900)]
        ch=[(1150,2600),(1150,3200),(1150,3800),(4450,2600),(4450,3200),(4450,3800)]+[(1200+600*i,4620) for i in range(6)]
        for (x,y) in ltab+rtab: R(ax,x,y,800,1800,WOOD,EC,1.4,z=4)
        for (x,y) in btab: R(ax,x,y,1800,800,WOOD,EC,1.4,z=4)
        tables=ltab+rtab+btab
    else:
        ltab=[(100,2300),(100,4100)]; rtab=[(4700,2300),(4700,4100)]; btab=[(2000,6200)]
        ch=[(1150,2600+600*i) for i in range(6)]+[(4450,2600+600*i) for i in range(6)]+[(2300+600*i,5920) for i in range(3)]
        for (x,y) in ltab+rtab: R(ax,x,y,800,1800,WOOD,EC,1.4,z=4)
        for (x,y) in btab: R(ax,x,y,1800,800,WOOD,EC,1.4,z=4)
        tables=ltab+rtab+btab
    for c in ch: chair(ax,*c)
    Z(ax,0,2230 if mode==12 else 2230,5600,3700 if mode==12 else 4900,"#DCEBFF","",)
    T(ax,2800,2420,f"ㄷ자 토론석 {seats}석 (의자는 U 안쪽)",fs=7.6,c="#1F5FBF",fontweight="bold") if False else None
    T(ax,2800,3300 if mode==12 else 3900,f"ㄷ자 토론석 {seats}석\n발표·토론 공간 ≈2.8m",fs=7,c="#1F5FBF",fontweight="bold") if False else None
    T(ax,2800,3850,f"U 안쪽 발표·토론 공간\n(폭 약 2.8m)\n교육존 {seats}석",fs=7.2,c="#1F5FBF",fontweight="bold")
    # table power strips
    if mode==12: pl=[(100,3000,"v"),(5500-70,3000,"v"),(1500,5700,"h"),(3300,5700,"h")]
    else: pl=[(100,3000,"v"),(100,4800,"v"),(5430,3000,"v"),(5430,4800,"v"),(2800,6950,"h")]
    for (x,y,o) in pl:
        if o=="v": R(ax,x-5,y,70,300,"#FF9F1C","#B86E00",.8,z=7)
        else: plug(ax,x,y-70,300,70)
    # ---- back zone
    if mode==12:
        R(ax,100,7050,1400,850,"#F1E3D3","#9A7B4F",1.4,z=5); T(ax,800,7500,"소파 2인\n(치수 추정)",fs=6)
        ax.add_patch(Circle((700,6850),185,fc="#FFFFFF",ec="#9A7B4F",lw=1.3,zorder=5)); T(ax,1250,6830,"티테이블",fs=5.8)
        for (x,y) in [(1950,7050),(1950,7600)]:
            ax.add_patch(Circle((x,y),270,fc="#8FB3E8",ec="white",zorder=5)); T(ax,x,y,"빈백",fs=5.8)
        Z(ax,0,6560,2250,1340,"#FBEBD6","라운지",ly=70)
        fx0=2350; n=3; fw=870
    else:
        for (x,y) in [(4300,7050),(4300,7600)]:
            ax.add_patch(Circle((x,y),270,fc="#8FB3E8",ec="white",zorder=5)); T(ax,x,y,"빈백",fs=5.8)
        T(ax,3000,7550,"소파·티테이블 제외",fs=6.2,c="#B1202C") if False else None
        Z(ax,3900,6500,1000,1400,"#FBEBD6","라운지(축소)",ly=70,fs=6)
        fx0=100; n=2; fw=1000
    for i in range(n):
        x=fx0+i*fw
        R(ax,x,7300,fw,600,"#FFFFFF","#0F7E86",1.5,z=5); R(ax,x,7230,fw,70,"#0F7E86",z=6)
        ax.add_patch(Circle((x+fw/2,6950),200,fc="#4DB6BD",ec="white",zorder=5))
        R(ax,x+fw/2-250,7340,500,60,"#222",z=6)
    zy=6600 if mode==12 else 6700
    Z(ax,fx0-60,zy,n*fw+120,7900-zy,"#D3F1F2",f"포커스룸 (드롭인 {n}석)",c="#0B5C63",ly=70,fs=6.8)
    plug(ax,fx0+fw/2-150,7220)
    # maker corner
    R(ax,5000,6700,560,540,"#FFE0B8","#E67E22",1.6,z=5); T(ax,5280,6970,"3D프린터\n(밀폐·환기)",fs=5.6,c="#8A4B00")
    Z(ax,4950,6520,650,800,"#FFE9CC","",); T(ax,5275,6600,"maker corner",fs=5.6,c="#8A4B00")
    plug(ax,5050,7280,300,60)
    # outlets
    for (ox,oy) in [(2000,40),(40,400),(40,3000),(40,4800),(W-40,3000),(W-40,4800),(W-40,7000),(2400,H-40),(4300,H-40),(40,7000)]: outlet(ax,ox,oy)
    # power dotted
    for (x,y,o) in pl:
        tx=40 if x<2800 else W-40
        ax.plot([x+30,tx],[y+150 if o=="v" else y,y+150 if o=="v" else y+250],color="#FF9F1C",lw=.8,ls=":",zorder=7)
    # LAN
    ax.plot([330,40,40],[1250,1250,2300],color=BLUE,lw=1.1,ls="--",zorder=7)
    ax.plot([200,200,3780],[800,22,22],color=BLUE,lw=1.1,ls="--",zorder=7)
    ax.plot([40,40,fx0+fw/2],[2300,6500,6500],color=BLUE,lw=1.1,ls="--",zorder=7)
    ax.plot([fx0+fw/2,fx0+fw/2],[6500,7220],color=BLUE,lw=1.1,ls="--",zorder=7)
    # aisles
    if mode==12:
        dim(ax,1380,4300,4220,4300,"2.8m",dy=0)
        dim(ax,900,4100,900,4900,"통로 0.8m 이상",dx=330) if False else None
        dim(ax,2800,5700,2800,6560,"뒤 통로 ≈0.9m",dx=0)
        dim(ax,4500,5300,5600,5300,"출입 통로 1.1m",dy=-130)
        dim(ax,200,4100,200,4900,"U 입구 0.8m",dx=330) if False else None
    else:
        dim(ax,3800,6600,3900,6600,"") if False else None
        T(ax,2850,5330,"※ 15석: 뒤 통로·U 입구 여유가 거의 없음",fs=6.2,c="#B1202C")
    # scale
    R(ax,300,H+420,1000,70,INK,z=8); R(ax,1300,H+420,1000,70,"white",INK,1,z=8)
    T(ax,300,H+620,"0",fs=6.3); T(ax,1300,H+620,"1m",fs=6.3); T(ax,2300,H+620,"2m",fs=6.3)
    T(ax,2900,H+470,"축척 막대 · 치수 mm · 문/창/콘센트는 가정",fs=6,c=GRAY,ha="left")
    ax.add_patch(Rectangle((0,0),W,H,fc="none",ec=INK,lw=3,zorder=10))
    ax.set_xlim(-250,W+250); ax.set_ylim(H+900,-350); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(f"ㄷ자(U형) 토론 배치 · {seats}석 · 가정한 방 5.6m × 7.9m = 44.2 m² (전용 44.205 m²)",fontsize=10,color=INK,loc="left",fontweight="bold")
    fig.savefig(OUT+f"layout-{mode}.png",bbox_inches="tight",facecolor="white"); plt.close(fig)
    import math
    d=[math.hypot(c[0]-2800,c[1]-400) for c in ch]
    stats[mode]=dict(seats=seats,tables=len(tables),eye_min=round(min(d)),eye_max=round(max(d)))
stats={}
build(12); build(15)
json.dump(stats,open("/workspace/office-desk-guide/work/layout3_stats.json","w")); print(stats)
