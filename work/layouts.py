import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json, math
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle, Circle, Arc
fp="/usr/share/fonts/truetype/sand-box/google/Nanum Gothic/NanumGothic-Bold.ttf"
fm.fontManager.addfont(fp); plt.rcParams["font.family"]=fm.FontProperties(fname=fp).get_name()
WOOD="#EBD3AB"; EC="#9A7B4F"; BLUE="#3182F6"; INK="#191F28"; GRAY="#6B7684"; MOT="#F04452"
TVW=1440; TVFACE=600  # 65" width, stand front plane (assumed 600mm from front wall)
H65=809
stats={}
def base(W,H,name,seats,tables,tdesc):
    fig,ax=plt.subplots(figsize=(6.4,6.4*(H+900)/(W+600)),dpi=170)
    ax.add_patch(Rectangle((0,0),W,H,fc="#F9FAFB",ec=INK,lw=3,zorder=1))
    # viewing rings (65")
    room=Rectangle((0,0),W,H,fc="none",ec="none")
    ax.add_patch(room)
    for m,c,lab in [(4,"#00B493","4× 3.2m"),(6,"#F59E0B","6× 4.9m"),(8,"#F04452","8× 6.5m")]:
        r=m*H65
        arc=Arc((W/2,TVFACE),2*r,2*r,theta1=0,theta2=180,fc="none",ec=c,lw=1.1,ls=(0,(4,4)),zorder=2)
        ax.add_patch(arc); arc.set_clip_path(room)
        dx=W/2-170
        if r>dx:
            yy=TVFACE+math.sqrt(r*r-dx*dx)
            if yy<H-100: ax.text(190,yy,lab,fontsize=5.5,color=c,ha="left",va="center",zorder=6,bbox=dict(fc="white",ec="none",pad=0.8,alpha=.85))
    # TV
    ax.add_patch(Rectangle((W/2-TVW/2,150),TVW,70,fc=INK,ec=INK,zorder=5))
    ax.add_patch(Rectangle((W/2-300,220),600,TVFACE-220,fc="#B0B8C1",ec="none",zorder=4,alpha=.7))
    ax.text(W/2,TVFACE+160,"TV 65\" (전면) · 이동식 스탠드",ha="center",va="top",fontsize=7,color=INK,zorder=6)
    ax.set_xlim(-250,W+250); ax.set_ylim(H+300,-300); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(f"{name}",fontsize=12,color=INK,pad=6,loc="left",fontweight="bold")
    return fig,ax
def table(ax,x,y,w,h,label=None):
    ax.add_patch(Rectangle((x,y),w,h,fc=WOOD,ec=EC,lw=1.4,zorder=3))
    if label: ax.text(x+w/2,y+h/2,label,ha="center",va="center",fontsize=6,color="#5a4020",zorder=4)
def chair(ax,cx,cy,face="N"):
    ax.add_patch(Circle((cx,cy),215,fc=BLUE,ec="white",lw=1,zorder=4))
def ceo(ax,x,y):
    # motion desk 1600x800 + chair behind (toward wall)
    ax.add_patch(Rectangle((x,y),1600,800,fc="#FFE4E6",ec=MOT,lw=2,zorder=3))
    ax.text(x+800,y+400,"대표 모션데스크\n1600×800",ha="center",va="center",fontsize=6.5,color=MOT,zorder=4)
    ax.add_patch(Circle((x+800,y-380),215,fc=MOT,ec="white",lw=1,zorder=4))
def dim(ax,x1,y1,x2,y2,txt,off=0,vert=False):
    ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="<->",color=GRAY,lw=.8),zorder=7)
    if vert: ax.text(x1-60,(y1+y2)/2,txt,rotation=90,ha="right",va="center",fontsize=7,color=GRAY)
    else: ax.text((x1+x2)/2,y1+off,txt,ha="center",va="top",fontsize=7,color=GRAY)
def finish(fig,ax,W,H,key,seats,n_tables,tsize,eyes,note):
    area=W*H/1e6
    ax.text(0,H+120,f"필요 공간 약 {W/1000:.1f}m × {H/1000:.1f}m = {area:.0f}m² ({area/3.3058:.1f}평, 벽 안쪽 최소)",fontsize=8,color=INK,va="top",fontweight="bold")
    ax.text(0,H+330,f"{seats}석 · 테이블 {n_tables}개({tsize}) · TV~가장 먼 눈높이 {max(eyes)/1000:.1f}m({max(eyes)/H65:.1f}×)",fontsize=7,color=GRAY,va="top")
    fig.savefig(f"/workspace/office-desk-guide/assets/img/layout-{key}.png",bbox_inches="tight",facecolor="white")
    plt.close(fig)
    stats[key]=dict(W=W,H=H,area=round(area,1),seats=seats,tables=n_tables,eye_min=min(eyes),eye_max=max(eyes),eye_max_x=round(max(eyes)/H65,1),eye_min_x=round(min(eyes)/H65,1))

# ---- A 교실형 (1800x600 x5)
W,H=6000,6900
fig,ax=base(W,H,"A. 교실형 (TV 정면 · 5개 연결 테이블)",15,5,"")
eyes=[]
for r in range(3):
    y=2400+r*1500
    for ci,x in enumerate([600,3600]):
        if r==2 and ci==1:
            ax.add_patch(Rectangle((x,y),1800,600,fc="#F2F4F6",ec=GRAY,lw=1,ls="--",zorder=2)); ax.text(x+900,y+300,"교재·음료·\n충전 코너(여유)",ha="center",va="center",fontsize=6,color=GRAY); continue
        table(ax,x,y,1800,600,"1800×600" if r==0 else None)
        for i in range(3):
            cx=x+300+600*i; cy=y+600+380; chair(ax,cx,cy); eyes.append(cy-TVFACE)
ceo(ax,3600,1100)
dim(ax,0,-120,W,-120,f"{W/1000:.1f}m",off=0) if False else None
ax.text(W/2,H-250,"통로 1,200mm (중앙)",ha="center",fontsize=6.5,color=GRAY,zorder=6) if False else None
finish(fig,ax,W,H,"A",15,5,"1800×600",eyes,"")
# ---- B ㄷ자형 (1800x600 x5)
W,H=5400,7500
fig,ax=base(W,H,"B. ㄷ자(U)형 토론 (5개 테이블)",15,5,"")
eyes=[]
for x,side in [(900,"L"),(3900,"R")]:
    for k in range(2):
        y=2400+k*1800
        table(ax,x,y,600,1800)
        for i in range(3):
            cy=y+300+600*i; cx=x-380 if side=="L" else x+600+380; chair(ax,cx,cy)
            # eye distance to TV center (euclid) from chair
            eyes.append(math.hypot(cx-W/2,cy-TVFACE))
table(ax,1800,6000,1800,600,"1800×600")
for i in range(3):
    cx=1800+300+600*i; cy=6600+380; chair(ax,cx,cy); eyes.append(cy-TVFACE)
ax.text(W/2,4300,"강사/대표 이동\n발표 공간\n(안쪽 2,400mm)",ha="center",va="center",fontsize=7,color=GRAY,zorder=6)
ceo(ax,3600,1100)
finish(fig,ax,W,H,"B",15,5,"1800×600",eyes,"")
# ---- C 모둠(아일랜드)형 (1800x800 x5)
W,H=6000,7500
fig,ax=base(W,H,"C. 모둠(아일랜드)형 (데스커 1800×800 5개)",15,5,"")
eyes=[]
for x in [600,3600]:
    table(ax,x,3300,1800,800,"1800×800"); table(ax,x,4100,1800,800)
    for i in range(3):
        cx=x+300+600*i
        chair(ax,cx,3300-380)             # N side: back to TV
        chair(ax,cx,4900+380); eyes.append(4900+380-TVFACE)  # S side faces TV
table(ax,2100,5800,1800,800,"1800×800")
for i in range(3):
    cx=2100+300+600*i; cy=6600+380; chair(ax,cx,cy); eyes.append(cy-TVFACE)
ax.text(W/2-0,2520,"▲ 이 줄 6석은 TV를 등지고 앉음(의자 돌려 시청)",ha="center",va="center",fontsize=6.5,color=MOT,zorder=6)
ceo(ax,3600,1100)
finish(fig,ax,W,H,"C",15,5,"1800×800",eyes,"")
json.dump(stats,open("/workspace/office-desk-guide/work/layout_stats.json","w"),indent=1)
print(json.dumps(stats,indent=1))
