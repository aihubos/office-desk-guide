import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json, math
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle, Circle, Polygon, FancyArrowPatch
fp="/usr/share/fonts/truetype/sand-box/google/Nanum Gothic/NanumGothic-Bold.ttf"
fm.fontManager.addfont(fp); plt.rcParams["font.family"]=fm.FontProperties(fname=fp).get_name()
INK="#191F28"; GRAY="#6B7684"; BLUE="#3182F6"; WOOD="#EBD3AB"; EC="#9A7B4F"; RED="#F04452"
W,H=5600,7900   # 44.24 m2 (assumed rectangle). y=0 front(TV wall), y=H window wall
stats={}
def R(ax,x,y,w,h,fc,ec="none",lw=1,z=3,ls="-",alpha=1):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=z,ls=ls,alpha=alpha))
def T(ax,x,y,s,fs=6.5,c=INK,ha="center",va="center",z=9,**k):
    ax.text(x,y,s,fontsize=fs,color=c,ha=ha,va=va,zorder=z,**k)
def zone(ax,x,y,w,h,fc,label,lx=None,ly=None,c=INK):
    R(ax,x,y,w,h,fc,ec="none",z=1,alpha=.55)
    T(ax,x+(lx if lx is not None else 60),y+(ly if ly is not None else 90),label,fs=7.5,c=c,ha="left",z=2,fontweight="bold")
def chair(ax,cx,cy,col=BLUE,r=230): ax.add_patch(Circle((cx,cy),r,fc=col,ec="white",lw=.8,zorder=5))
def dim(ax,x1,y1,x2,y2,txt,dx=0,dy=0,c="#0F9D7A"):
    ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="<->",color=c,lw=1),zorder=8)
    T(ax,(x1+x2)/2+dx,(y1+y2)/2+dy,txt,fs=6.5,c=c,bbox=dict(fc="white",ec="none",pad=.6,alpha=.9))
def plug(ax,x,y,w=300,h=90): R(ax,x,y,w,h,"#FF9F1C","#B86E00",.8,z=7); 
def outlet(ax,x,y): ax.plot([x],[y],marker="s",ms=4,color="#FF9F1C",mec="#B86E00",zorder=8)

def build(mode):
    seats=12 if mode==12 else 15
    fig,ax=plt.subplots(figsize=(7.4,7.4*(H+1500)/(W+700)),dpi=170)
    R(ax,0,0,W,H,"#FBFCFD","none",z=0)
    # ---- zones
    zone(ax,0,0,2080,720,"#CDEFD9","",ly=-110); T(ax,60,-110,"탕비·복합기",fs=7.5,ha="left",fontweight="bold",c="#1B5E3A")
    zone(ax,0,720,420,720,"#E3D7FA","")
    zone(ax,3700,560,1900,2000,"#FFD9DE","대표석 + 스튜디오 코너",c="#B1202C")
    ty0=2300 if mode==15 else 2400
    zone(ax,880,ty0-120,4640,3300 if mode==12 else 4420,"#DCEBFF","교육존 ("+str(seats)+"석)",lx=70,ly=80)
    # ---- window (bottom) & door (right)
    R(ax,350,H-40,W-700,80,"#9AD3FF","#2C7FB8",1,z=6)
    T(ax,W/2,H+170,"창문(가정) — 빛은 들어오지만 카메라·TV 정면은 아님",fs=6.8,c="#2C7FB8")
    R(ax,W-45,5600,90,900,"#FFFFFF","#555",1.2,z=6)
    ax.add_patch(matplotlib.patches.Arc((W,5600),1800,1800,theta1=90,theta2=180,ec="#999",lw=.8,ls="--",zorder=6)) if False else None
    T(ax,W-60,6050,"출입문\n(가정)",fs=6.5,ha="right",c="#555")
    # ---- front wall: TV, stand, whiteboard
    R(ax,2080,130,1440,70,INK,z=6)
    R(ax,2500,200,600,400,"#B0B8C1","#8B95A1",1,z=5)
    T(ax,2800,420,"TV 65\"\n이동식 스탠드",fs=6.5,z=9)
    # service wall
    R(ax,50,50,555,637,"#E5E8EB","#8B95A1",1.2,z=5); T(ax,330,370,"냉장고",fs=6.5)
    R(ax,650,50,900,450,"#FFFFFF","#8B95A1",1.2,z=5); T(ax,1100,275,"커피머신+선반",fs=6.3)
    R(ax,1580,50,460,460,"#FFFFFF","#2D6A4F",1.5,z=5); T(ax,1810,280,"복합기",fs=6.5)
    R(ax,0,780,330,520,"#C9B5F2","#6F42C1",1.5,z=5); T(ax,170,1040,"NAS\n공유기",fs=6,c="#3D1E8F")
    # whiteboard parked
    R(ax,820,1500,1800,120,"#FFFFFF","#444",1.5,z=5); T(ax,1720,1740,"이동식 화이트보드(양면·캐스터) — 수업 때 TV 옆으로",fs=6.3,z=9)
    # ---- CEO + studio
    R(ax,3800,800,800,1600,"#FFFFFF","#F04452",2,z=5); T(ax,4200,1600,"대표 모션데스크\n1600×800",fs=6.3,c="#B1202C",rotation=90)
    R(ax,5154,700,446,1600,"#D9B88A","#8A6A3A",1.5,z=5); T(ax,5380,1500,"책장 2대(배경)",fs=6.3,rotation=90)
    chair(ax,4900,1250,RED); chair(ax,4900,1950,"#F5A3AB"); T(ax,4900,1250,"제레미",fs=5.2,c="white"); T(ax,4900,1950,"유하님",fs=5.2,c="white")
    ax.plot([5154,5154],[700,2300],color="#FFD60A",lw=3,zorder=6)  # LED strip
    # camera
    cx,cy=2900,1550
    ax.add_patch(Polygon([[cx-130,cy-130],[cx-130,cy+130],[cx+120,cy]],fc="#222",zorder=8))
    ax.add_patch(Polygon([[cx+120,cy],[4800,650],[4800,2250]],fc="#FFD60A",alpha=.12,ec="none",zorder=2))
    dim(ax,cx+140,1550,4730,1550,"",c="#8A6D00"); T(ax,3350,1420,"촬영거리 약 2.0m",fs=6.5,c="#8A6D00")
    T(ax,cx-50,cy+320,"카메라/삼각대",fs=6.3)
    ax.add_patch(Circle((3300,520),120,fc="#FFD60A",ec="#B58B00",zorder=8)); T(ax,3300,760,"키 라이트",fs=6)
    ax.add_patch(Rectangle((3250,2320),220,60,fc="#FFD60A",ec="#B58B00",zorder=8)); T(ax,3050,2230,"LED 패널",fs=6)
    R(ax,3950,20,1500,40,"#8B95A1",z=6); T(ax,4700,30-0,"",fs=6)
    T(ax,4700,150,"흡음재(선택)",fs=5.8,c=GRAY)
    plug(ax,4650,2300)  # CEO strip
    # ---- learners
    cols=[900,3700]
    tables=[]
    if mode==12:
        rows=[2400,4200]
        for ry in rows:
            for cxx in cols: tables.append((cxx,ry))
    else:
        rows=[2300,4000]
        for ry in rows:
            for cxx in cols: tables.append((cxx,ry))
        tables.append((900,5700))
    for (x,y) in tables:
        R(ax,x,y,1800,800,WOOD,EC,1.4,z=4)
        for i in range(3): chair(ax,x+300+i*600,y+800+230+60)
        plug(ax,x+750,y+710,300,70)
    T(ax,1800,tables[0][1]+400,"교육 책상 1800×800 (3석)",fs=6.3,c="#5a4020")
    # ---- back zone
    if mode==12:
        # lounge
        R(ax,100,7050,1500,850,"#F1E3D3","#9A7B4F",1.4,z=5); T(ax,850,7475,"소파 2인(치수 추정)",fs=6.2)
        R(ax,300,6450,1200,590,"#FFFFFF","#9A7B4F",1.2,z=5); T(ax,900,6745,"티테이블",fs=6.3)
        ax.add_patch(Circle((1850,7450),270,fc="#8FB3E8",ec="white",zorder=5)); T(ax,1850,7450,"빈백",fs=6)
        ax.add_patch(Circle((1850,6900),270,fc="#A6C7F0",ec="white",zorder=5)); T(ax,1850,6900,"빈백",fs=6)
        zone(ax,0,6230,2150,1670,"#FBEBD6","라운지",ly=60)
        fx0=2250; n=3; fw=900
    else:
        # lounge reduced
        ax.add_patch(Circle((450,7480),270,fc="#8FB3E8",ec="white",zorder=5)); T(ax,450,7480,"빈백",fs=6)
        ax.add_patch(Circle((1150,7550),270,fc="#A6C7F0",ec="white",zorder=5)); T(ax,1150,7550,"빈백",fs=6)
        T(ax,1900,7500,"소파·티테이블\n넣을 자리 없음 (제외)",fs=6.8,c="#B1202C")
        zone(ax,0,6900,2700,1000,"#FBEBD6","라운지(축소)",ly=90)
        fx0=2800; n=2; fw=1100
    # focus room
    for i in range(n):
        x=fx0+i*fw
        R(ax,x,7300,fw,600,"#FFFFFF","#0F7E86",1.5,z=5)
        R(ax,x,7230,fw,70,"#0F7E86",z=6)
        ax.add_patch(Circle((x+fw/2,6950),200,fc="#4DB6BD",ec="white",zorder=5))
        R(ax,x+fw/2-260,7340,520,60,"#222",z=6)
    zone(ax,fx0-80,6600,n*fw+160,1300,"#D3F1F2","포커스룸 (드롭인 "+str(n)+"석·모니터+칸막이)",ly=100,c="#0B5C63")
    plug(ax,fx0+fw/2-150,7220)
    # maker corner
    R(ax,5000,6700,600,550,"#FFE0B8","#E67E22",1.6,z=5); T(ax,5300,6975,"3D프린터\n(밀폐·환기)",fs=6,c="#8A4B00")
    zone(ax,4950,6520,650,800,"#FFE9CC","",)
    T(ax,5275,6600,"maker corner",fs=5.8,c="#8A4B00")
    plug(ax,5050,6560,300,70)
    # ---- outlets assumed
    for (ox,oy) in [(2000,40),(40,400),(40,2600),(40,4700),(40,6000),(W-40,2700),(W-40,4300),(W-40,7000),(2400,H-40),(4300,H-40)]: outlet(ax,ox,oy)
    # power trunk (orange dotted) from tables to wall outlets via center aisle
    for (x,y) in tables:
        sx=x+900; sy=y+745
        tx=W-40 if x>2700 else 40; ty=y+400
        ax.plot([sx,3200,tx] if False else [sx,(3200),tx],[sy,sy+60,ty],color="#FF9F1C",lw=.8,ls=":",zorder=7)
    # LAN: router -> CEO, -> focus (blue dashed)
    ax.plot([330,330,3800],[1200,30,30] if False else [1040,95,95][0:3],color=BLUE,lw=0)  # placeholder
    ax.plot([330,330,3780],[1040,22,22],color=BLUE,lw=1.2,ls="--",zorder=7)
    ax.plot([200,200,fx0+fw],[1300,6300,6300],color=BLUE,lw=1.2,ls="--",zorder=7)
    ax.plot([fx0+fw,fx0+fw],[6300,7220],color=BLUE,lw=1.2,ls="--",zorder=7)
        # ---- aisles
    dim(ax,2700,ty0+420,3700,ty0+420,"중앙통로 1.0m",dy=-130 if False else 0)
    cr0=(5600 if mode==12 else 6500)
    if mode==12: dim(ax,3000,5100+0,3000,6380,"교차통로 ≥1.2m",dx=0) 
    dim(ax,0,3500,900,3500,"측면 0.9m",dy=-120)
    # ---- scale bar & title
    R(ax,300,H+420,1000,70,INK,z=8); R(ax,1300,H+420,1000,70,"white",INK,1,z=8)
    T(ax,300,H+620,"0",fs=6.5); T(ax,1300,H+620,"1m",fs=6.5); T(ax,2300,H+620,"2m",fs=6.5)
    T(ax,3000,H+470,"축척 1m 막대 · 모든 치수는 mm 기준 가정",fs=6.2,c=GRAY,ha="left")
    ax.add_patch(Rectangle((0,0),W,H,fc="none",ec=INK,lw=3,zorder=10))
    ax.set_xlim(-250,W+250); ax.set_ylim(H+900,-350); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(f"{seats}석 안 · 가정한 방 5.6m × 7.9m = 44.2 m² (전용 44.205 m²)",fontsize=10.5,color=INK,loc="left",fontweight="bold")
    fig.savefig(f"/workspace/office-desk-guide/assets/img/layout-{mode}.png",bbox_inches="tight",facecolor="white")
    plt.close(fig)
    eye=[ (min(t[1] for t in tables)+800+300)-600, (max(t[1] for t in tables)+800+300)-600 ]
    stats[mode]=dict(seats=seats,tables=len(tables),eye_min=eye[0],eye_max=eye[1])
build(12); build(15)
json.dump(stats,open("/workspace/office-desk-guide/work/layout3_stats.json","w"))
print(stats)
