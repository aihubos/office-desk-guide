import * as THREE from 'three';
import {OrbitControls} from './vendor/OrbitControls.js';
import {CSS2DRenderer, CSS2DObject} from './vendor/CSS2DRenderer.js';

// ===== 좌표: layouts5.py 와 동일 (mm). x=가로(0~4500), y=세로(0 문/TV 벽 ~ 9800 창문 벽) → three: X=x, Z=y, Y=위 =====
const W=4.5, L=9.8, CEIL=2.6;   // 천장 2.6m는 가정
const m=v=>v/1000;
const stage=document.getElementById('stage');
let renderer;
try{ renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true}); }
catch(e){ document.getElementById('err').hidden=false; throw e; }
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled=true; renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.outputColorSpace=THREE.SRGBColorSpace;
stage.appendChild(renderer.domElement);
const lr=new CSS2DRenderer(); lr.domElement.style.cssText='position:absolute;inset:0;pointer-events:none';
stage.appendChild(lr.domElement);

const scene=new THREE.Scene(); scene.background=new THREE.Color('#F4F1EA');
const camera=new THREE.PerspectiveCamera(40,1,.05,100);
const controls=new OrbitControls(camera,renderer.domElement);
controls.enableDamping=true; controls.dampingFactor=.08; controls.maxPolarAngle=Math.PI*0.499; controls.minDistance=1; controls.maxDistance=30;
controls.screenSpacePanning=true;

// lights
scene.add(new THREE.HemisphereLight('#ffffff','#d9cdb8',1.15));
const sun=new THREE.DirectionalLight('#fff4e0',1.5); sun.position.set(-3,12,3); sun.target.position.set(2.25,0,5);
sun.castShadow=true; sun.shadow.mapSize.set(2048,2048); const sc=sun.shadow.camera; sc.left=-8;sc.right=8;sc.top=8;sc.bottom=-8;sc.near=1;sc.far=30; sun.shadow.bias=-.0005;
scene.add(sun,sun.target);

// materials
const _m={};
const M=(c,o={})=>{const k=c+JSON.stringify(o); return _m[k]||(_m[k]=new THREE.MeshStandardMaterial({color:c,roughness:o.r??.7,metalness:o.m??0,transparent:o.a!=null,opacity:o.a??1,emissive:o.e||0x000000,emissiveIntensity:o.ei||1,side:o.ds?THREE.DoubleSide:THREE.FrontSide,depthWrite:o.a==null}));};
const WOOD=M('#E3C79A',{r:.6}), WOOD_D=M('#B98F5B',{r:.65}), BLACK=M('#1d1f23',{r:.5,m:.3}), WHITE=M('#F5F5F2'), GRAY=M('#C9CED6'), DGRAY=M('#6b7480');
const wallM=M('#F3EFE8',{r:.95});

const groups={common:new THREE.Group(),g12:new THREE.Group(),g15:new THREE.Group()};
scene.add(groups.common,groups.g12,groups.g15);
const swingG=new THREE.Group(); groups.common.add(swingG);
const labels=[];
function box(g,x,y,w,d,y0,h,mat,cast=true){ // plan rect(mm) + 높이(m)
  const me=new THREE.Mesh(new THREE.BoxGeometry(m(w),h,m(d)),mat);
  me.position.set(m(x+w/2),y0+h/2,m(y+d/2)); me.castShadow=cast; me.receiveShadow=true; g.add(me); return me;
}
function cyl(g,x,z,r,y0,h,mat,seg=24){const me=new THREE.Mesh(new THREE.CylinderGeometry(r,r,h,seg),mat); me.position.set(x,y0+h/2,z); me.castShadow=true; me.receiveShadow=true; g.add(me); return me;}
function label(g,text,x,y,z,cls=''){ // x,z in mm, y in m
  const d=document.createElement('div'); d.className='lb '+cls; d.textContent=text;
  const o=new CSS2DObject(d); o.position.set(m(x),y,m(z)); o.userData.g=g; g.add(o); labels.push(o); return o;
}
function zone(g,x,y,w,d,color,a=.55){const me=new THREE.Mesh(new THREE.PlaneGeometry(m(w),m(d)),new THREE.MeshBasicMaterial({color,transparent:true,opacity:a,depthWrite:false})); me.rotation.x=-Math.PI/2; me.position.set(m(x+w/2),.004,m(y+d/2)); me.renderOrder=1; g.add(me);}

// ===== room =====
const C=groups.common;
const floor=new THREE.Mesh(new THREE.PlaneGeometry(W,L),M('#EDE6D8',{r:.9})); floor.rotation.x=-Math.PI/2; floor.position.set(W/2,0,L/2); floor.receiveShadow=true; C.add(floor);
const ground=new THREE.Mesh(new THREE.PlaneGeometry(60,60),M('#E4DED2',{r:1})); ground.rotation.x=-Math.PI/2; ground.position.set(W/2,-.02,L/2); C.add(ground);
function wallPlane(w,h,x,y,z,ry){const p=new THREE.Mesh(new THREE.PlaneGeometry(w,h),wallM); p.position.set(x,y,z); p.rotation.y=ry; p.receiveShadow=true; C.add(p);}
// 단변(앞) 벽: 문 틈 x 1.8~2.7
const D0=1.8,D1=2.7,DH=2.1;
wallPlane(D0,CEIL,D0/2,CEIL/2,0,0); wallPlane(W-D1,CEIL,(D1+W)/2,CEIL/2,0,0); wallPlane(D1-D0,CEIL-DH,(D0+D1)/2,(CEIL+DH)/2,0,0);
wallPlane(L,CEIL,0,CEIL/2,L/2,Math.PI/2);       // 왼쪽 긴 벽 (법선 +x)
wallPlane(L,CEIL,W,CEIL/2,L/2,-Math.PI/2);      // 오른쪽 긴 벽 (법선 -x)
// 벽 윗단(윤곽)
const cap=(x,z,w,d)=>{const c=new THREE.Mesh(new THREE.BoxGeometry(w,.03,d),M('#8B95A1')); c.position.set(x,CEIL+.015,z); C.add(c);};
cap(0,L/2,.06,L); cap(W,L/2,.06,L); cap(D0/2,0,D0,.06); cap((D1+W)/2,0,W-D1,.06); cap(W/2,L,W,.06);
// 문틀 + 문(열린 상태)
box(C,1750,-30,50,60,0,DH,BLACK); box(C,2700,-30,50,60,0,DH,BLACK); box(C,1750,-30,1000,60,DH,.05,BLACK);
const door=new THREE.Mesh(new THREE.BoxGeometry(.045,DH-.03,.9),M('#CDB48A',{r:.6})); door.position.set(D0+.03,(DH-.03)/2,.45); door.castShadow=true; C.add(door);
const hdl=new THREE.Mesh(new THREE.BoxGeometry(.03,.03,.14),BLACK); hdl.position.set(D0+.07,1.0,.8); C.add(hdl);
// 문 스윙 반경(0.9m 비움)
{const f=new THREE.Mesh(new THREE.CircleGeometry(.9,40,0,Math.PI/2),new THREE.MeshBasicMaterial({color:'#FFD43B',transparent:true,opacity:.45,side:THREE.DoubleSide,depthWrite:false})); f.rotation.x=Math.PI/2; f.position.set(D0,.008,0); f.renderOrder=2; swingG.add(f);
 const ring=new THREE.Mesh(new THREE.RingGeometry(.895,.9,48,1,0,Math.PI/2),new THREE.MeshBasicMaterial({color:'#B8860B',side:THREE.DoubleSide})); ring.rotation.x=Math.PI/2; ring.position.set(D0,.01,0); swingG.add(ring);}
label(C,'출입문 (단변 정중앙)',2250,2.3,0,'k');
// 창문(전면 유리벽) y=9800
{const gl=new THREE.Mesh(new THREE.PlaneGeometry(W,CEIL),new THREE.MeshStandardMaterial({color:'#9AD3FF',transparent:true,opacity:.22,roughness:.05,side:THREE.DoubleSide,depthWrite:false})); gl.position.set(W/2,CEIL/2,L-.01); C.add(gl);
 for(const x of [0,1.5,3.0,4.5]){const v=new THREE.Mesh(new THREE.BoxGeometry(.05,CEIL,.06),BLACK); v.position.set(x,CEIL/2,L-.01); C.add(v);}
 const r1=new THREE.Mesh(new THREE.BoxGeometry(W,.05,.06),BLACK); r1.position.set(W/2,.025,L-.01); C.add(r1); const r2=r1.clone(); r2.position.y=CEIL-.025; C.add(r2);}
label(C,'창문 · 바닥~천장 전면 유리 (뒤쪽)',2250,2.95,9800,'k');

// ===== zones (바닥 색) =====
zone(C,0,780,640,2100,'#CDEFD9'); zone(C,800,2850,2900,2700,'#DCEBFF',.6);

// ===== 앞쪽 서비스 벽 (왼쪽) =====
box(C,50,50,550,600,1.3,.03,WOOD_D); box(C,60,60,30,580,1.0,.3,BLACK); box(C,560,60,30,580,1.0,.3,BLACK); // NAS 선반
box(C,120,150,220,320,1.33,.22,M('#7B61FF',{r:.5})); box(C,380,200,160,260,1.33,.05,WHITE);
label(C,'NAS·공유기',325,1.75,350,'s');
box(C,50,820,555,640,0,1.75,GRAY); box(C,590,850,12,6,.95,.0,GRAY); box(C,585,900,10,500,1.1,.4,DGRAY); box(C,585,900,10,500,.2,.4,DGRAY);
label(C,'냉장고',330,1.95,1140);
box(C,50,1500,450,900,0,.88,WHITE); box(C,50,1500,450,900,.88,.04,WOOD);
box(C,100,1800,300,420,.92,.36,BLACK); box(C,130,1850,240,200,1.05,.12,DGRAY);   // 커피머신
box(C,50,1500,250,900,1.55,.03,WOOD_D); box(C,60,1530,12,840,1.4,.15,BLACK); box(C,280,1530,12,840,1.4,.15,BLACK);  // 선반
label(C,'커피머신 + 선반',300,1.75,1950);
box(C,50,2440,460,380,0,.95,WHITE); box(C,50,2440,460,380,.95,.04,DGRAY); box(C,60,2460,250,320,.99,.04,BLACK);
label(C,'복합기',280,1.25,2630);

// ===== 앞 벽: TV (문 오른쪽) + 전동 스크린 =====
box(C,2830,130,1440,70,.9,.81,BLACK);                       // 65" 패널
box(C,2850,203,1400,2,.92,.77,M('#1c2733',{r:.2,m:.4}),false);
box(C,3520,200,60,50,.15,.8,BLACK); box(C,3250,200,600,400,.0,.05,BLACK);   // 이동식 스탠드
label(C,'TV 65" (이동식 스탠드)',3950,1.75,200,'k');
{const t=new THREE.Mesh(new THREE.CylinderGeometry(.045,.045,1.77,16),M('#cfd3d9')); t.rotation.z=Math.PI/2; t.position.set(3.6,2.5,.07); C.add(t);}
label(C,'전동 스크린 80" (선택)',3600,2.7,70,'s');
// 이동식 화이트보드 (오른쪽 벽 세로 주차)
box(C,4350,750,100,1500,.55,1.15,WHITE); box(C,4345,745,110,1510,.55,.03,DGRAY); box(C,4345,745,110,1510,1.67,.03,DGRAY);
box(C,4350,750,100,40,0,.6,BLACK); box(C,4350,2210,100,40,0,.6,BLACK);
label(C,'이동식 화이트보드 (주차)',4400,1.95,1500);
// 에어컨 + 프로젝터(천장)
{const ac=new THREE.Mesh(new THREE.CylinderGeometry(.26,.26,.12,32),M('#e8ebee')); ac.position.set(2.25,CEIL-.06,4.95); C.add(ac); label(C,'천장형 에어컨',2250,2.45,4950,'s');}
{const pj=new THREE.Mesh(new THREE.BoxGeometry(.3,.12,.22),M('#e8ebee')); pj.position.set(2.95,2.3,3.5); pj.castShadow=true; C.add(pj); const rd=new THREE.Mesh(new THREE.CylinderGeometry(.015,.015,.3),BLACK); rd.position.set(2.95,2.45,3.5); C.add(rd);
  label(C,'빔프로젝터(선택)',2950,2.55,3500,'s');}

// ===== 가구 빌더 =====
function table(g,x,y,w,d,top=WOOD,h=.72){ // 책상
  box(g,x,y,w,d,h-.03,.03,top); const t=.045;
  for(const [lx,ly] of [[x+30,y+30],[x+w-30-t*1000,y+30],[x+30,y+d-30-t*1000],[x+w-30-t*1000,y+d-30-t*1000]]) box(g,lx,ly,t*1000,t*1000,0,h-.03,BLACK);
}
function chair(g,x,y,fx,fz,col='#3182F6',s=1){
  const c=new THREE.Group(); c.position.set(m(x),0,m(y)); c.rotation.y=Math.atan2(fx,fz); c.scale.setScalar(s);
  const mat=M(col,{r:.8});
  const seat=new THREE.Mesh(new THREE.CylinderGeometry(.21,.21,.07,20),mat); seat.position.y=.46; seat.castShadow=true; c.add(seat);
  const back=new THREE.Mesh(new THREE.BoxGeometry(.4,.4,.05),mat); back.position.set(0,.74,-.2); back.castShadow=true; c.add(back);
  const st=new THREE.Mesh(new THREE.CylinderGeometry(.025,.025,.3),BLACK); st.position.y=.27; c.add(st);
  for(let i=0;i<5;i++){const a=i*Math.PI*2/5; const b=new THREE.Mesh(new THREE.BoxGeometry(.04,.03,.24),BLACK); b.position.set(Math.sin(a)*.12,.06,Math.cos(a)*.12); b.rotation.y=a; c.add(b);}
  g.add(c); return c;
}
function bean(g,x,y,col='#8FB3E8'){const b=new THREE.Mesh(new THREE.SphereGeometry(1,24,16),M(col,{r:.95})); b.scale.set(.27,.21,.27); b.position.set(m(x),.2,m(y)); b.castShadow=true; g.add(b);}
function shelf(g,x,y,w,d,col=WOOD_D,h=2.0,withBooks=true){ // 책장: 앞면이 -x 방향
  box(g,x+d-18,y,18,w,0,h,M('#8a6a3a')); // 뒷판
  for(const yy of [0,.4,.8,1.2,1.6,h-.03]) box(g,x,y,d,w,yy,.03,col);
  box(g,x,y,d,22,0,h,col); box(g,x,y+w-22,d,22,0,h,col); box(g,x,y+w/2-11,d,22,0,h,col);
  if(withBooks){const cols=['#c0563b','#3b6fc0','#e0b84a','#4a8f6b','#eee','#7a5aa8']; let k=0;
    for(const yy of [.03,.43,.83,1.23]) for(let z=y+40;z<y+w-60;z+=70+((k*37)%40)){ const hh=.2+((k*53)%15)/100; box(g,x+60,z,d-110,36+(k%3)*8,yy,hh,M(cols[k%6],{r:.8}),false); k++; }}
}
// ===== 12석 =====
const A=groups.g12;
for(const [x,y,w,d] of [[0,2900,800,1800],[3700,2900,800,1800],[0,5600,1800,800],[1800,5600,1800,800]]) table(A,x,y,w,d);
for(let i=0;i<3;i++){ chair(A,1050,3200+600*i,-1,0); chair(A,3450,3200+600*i,1,0); }
for(let i=0;i<6;i++) chair(A,300+600*i,5320,0,1);
label(A,'U자 테이블',1800,.9,6000,'k'); 
label(A,'의자 · 교육 12석',1050,1.0,3800,'k');
label(A,'U 안쪽 발표·토론 공간',2250,.3,4200,'s');
box(A,640,2440,330,380,0,.5,M('#ffffff',{a:.55})); label(A,'프린터(나중)',805,.7,2630,'s');
// 대표석 + 스튜디오
zone(A,2650,7250,1850,1700,'#FFD9DE',.6);
box(A,2700,7300,800,1600,.7,.04,M('#F1E6D3')); for(const yy of [7380,8800]){box(A,3020,yy-0,60,120,0,.7,BLACK); box(A,2750,yy+30,700,60,0,.03,BLACK);}
box(A,2830,7440,200,200,.74,.095,M('#c9ced6',{m:.7,r:.3})); box(A,3050,7900,190,330,.74,.02,WHITE); box(A,3120,8380,50,70,.74,.03,WHITE);
chair(A,3800,7700,-1,0,'#F04452',1); chair(A,3800,8400,-1,0,'#F5A3AB',1);
label(A,'대표석 모션데스크 (보유)',3100,1.15,8100,'k');
shelf(A,4054,7300,1600,446);
box(A,4040,7300,14,1600,1.98,.03,M('#FFD60A',{e:'#FFD60A',ei:.8}),false);
label(A,'책장',4300,2.2,8400);
box(A,4455,6350,45,800,.9,1.1,M('#7b8794'));
// 카메라 + 조명
{const g=new THREE.Group(); g.position.set(1.8,0,8.05); for(let i=0;i<3;i++){const a=i*Math.PI*2/3+Math.PI/2; const l=new THREE.Mesh(new THREE.CylinderGeometry(.01,.012,1.4),BLACK); l.position.set(Math.cos(a)*.18,.7,Math.sin(a)*.18); l.rotation.set(Math.sin(a)*.2,0,-Math.cos(a)*.2); g.add(l);}
 const cb=new THREE.Mesh(new THREE.BoxGeometry(.2,.13,.12),BLACK); cb.position.y=1.5; cb.castShadow=true; g.add(cb); const ln=new THREE.Mesh(new THREE.CylinderGeometry(.04,.05,.1),DGRAY); ln.rotation.z=Math.PI/2; ln.position.set(.14,1.5,0); g.add(ln); A.add(g);}
label(A,'카메라/삼각대',1800,1.75,8050,'s');
{const g=new THREE.Group(); g.position.set(2.2,0,7.45); const p=new THREE.Mesh(new THREE.CylinderGeometry(.015,.015,1.7),BLACK); p.position.y=.85; g.add(p); const sb=new THREE.Mesh(new THREE.BoxGeometry(.06,.45,.45),M('#FFF3B0',{e:'#FFE066',ei:.7})); sb.position.set(.03,1.75,0); g.add(sb); A.add(g);}
label(A,'스튜디오 조명',2200,2.15,7450,'s');
{const p=new THREE.Mesh(new THREE.BoxGeometry(.23,.02,.06),M('#FFF3B0',{e:'#FFE066',ei:.8})); p.position.set(2.265,1.3,8.85); A.add(p); const q=new THREE.Mesh(new THREE.CylinderGeometry(.012,.012,1.3),BLACK); q.position.set(2.265,.65,8.85); A.add(q);}
label(A,'스튜디오 (책장 배경)',3500,2.4,7300,'k');
// 포커스룸 (왼쪽 벽)
zone(A,0,7200,1250,2600,'#D3F1F2',.6);
for(let i=0;i<3;i++){const y=7300+i*800; table(A,0,y,600,800,WHITE); box(A,590,y,50,800,.74,.5,M('#0F7E86',{a:.85}),false); box(A,60,y+250,60,300,.74,.4,BLACK); chair(A,930,y+400,-1,0,'#4DB6BD',.9);}
label(A,'포커스룸 (드롭인 3석)',600,1.35,8500,'k');
// 라운지
box(A,1300,9250,1400,550,.0,.4,M('#D9C2A5',{r:.9})); box(A,1300,9600,1400,200,.0,.85,M('#D9C2A5',{r:.9})); box(A,1300,9250,110,550,.0,.6,M('#CDB38F',{r:.9})); box(A,2590,9250,110,550,.0,.6,M('#CDB38F',{r:.9}));
cyl(A,1.9,8.65,.175,.0,.45,M('#fff',{r:.4})); cyl(A,1.9,8.65,.18,.43,.03,WOOD);
bean(A,3000,9380); bean(A,3580,9380);
label(A,'라운지 · 소파 2인',2000,1.6,9450,'k'); label(A,'티테이블',1900,.7,8650,'s'); label(A,'빈백',3290,.65,9380,'s');
// 3D 프린터 maker
zone(A,3880,9000,620,800,'#FFE9CC',.8);
table(A,3900,9100,600,650,WOOD_D,.74);
box(A,3940,9150,520,520,.74,.42,M('#ffffff',{a:.5})); box(A,3950,9160,40,40,.74,.42,M('#E67E22')); box(A,4410,9160,40,40,.74,.42,M('#E67E22')); box(A,3950,9560,40,40,.74,.42,M('#E67E22')); box(A,4410,9560,40,40,.74,.42,M('#E67E22'));
box(A,4060,9260,300,300,.78,.3,M('#2c3138')); 
label(A,'3D프린터 maker corner (창 쪽 환기)',4150,1.45,9420,'k');

// ===== 15석 =====
const B=groups.g15;
for(const [x,y,w,d] of [[0,2900,800,1800],[0,4700,800,1800],[3700,2900,800,1800],[3700,4700,800,1800],[1700,7400,1800,800]]) table(B,x,y,w,d);
for(let i=0;i<6;i++){chair(B,1050,3200+600*i,-1,0); chair(B,3450,3200+600*i,1,0);}
for(let i=0;i<3;i++) chair(B,2000+600*i,7120,0,1);
label(B,'U자 테이블',2250,.9,7800,'k'); label(B,'의자 · 교육 15석',1050,1.0,4500,'k');
zone(B,800,2850,2900,4400,'#DCEBFF',.0);
box(B,2850,9200,1600,600,.7,.04,M('#F1E6D3')); box(B,2900,9300,60,400,0,.7,BLACK); box(B,4300,9300,60,400,0,.7,BLACK);
box(B,3550,9350,200,200,.74,.095,M('#c9ced6',{m:.7})); chair(B,3650,8960,0,1,'#F04452');
label(B,'대표 모션데스크 (보유)',3650,1.2,9500,'k');
shelf(B,0,8300,1500,446,WOOD_D,2.0,true); label(B,'책장',230,2.2,9050);
zone(B,450,8700,1900,1100,'#D3F1F2',.6);
for(let i=0;i<2;i++){const x=500+i*950; table(B,x,9250,900,550,WHITE); box(B,x,9200,900,50,.74,.5,M('#0F7E86',{a:.85}),false); chair(B,x+450,8960,0,1,'#4DB6BD',.85);}
label(B,'포커스룸 (2석)',1400,1.3,9250,'k');
table(B,50,7300,560,540,WOOD_D,.74); box(B,100,7350,460,440,.74,.4,M('#ffffff',{a:.5})); box(B,160,7410,340,320,.78,.3,M('#2c3138'));
label(B,'3D프린터 (창에서 멀어 환기 곤란)',330,1.35,7570,'k');
bean(B,3750,1500); bean(B,3750,2100); label(B,'빈백',3750,.6,1800,'s');
label(B,'※ 15석: 스튜디오·소파 제외',2250,.3,6700,'s');

// ===== UI / 카메라 =====
const tgt=new THREE.Vector3();
const views={
  entrance:()=>({pos:[2.25,1.62,.55],tgt:[2.25,1.0,6.8],fov:68}),
  top:()=>{const a=renderer.domElement.clientWidth/renderer.domElement.clientHeight; const f=40*Math.PI/180; const vh=(L+3.8)/2/Math.tan(f/2)*1.12, hh=(W+1.2)/2/Math.tan(f/2)/a; const d=Math.max(vh,hh); return {pos:[2.25,d,4.9+.4],tgt:[2.25,0,4.9],fov:40};},
  iso:()=>isoView(1), iso2:()=>isoView(-1)
};
function isoView(sg){const a=renderer.domElement.clientWidth/renderer.domElement.clientHeight; const por=a<.8; const d=por?32:19; const dir=por?new THREE.Vector3(-.4,.8,.6*sg).normalize():new THREE.Vector3(-.62,.62,.62*sg).normalize(); const t=new THREE.Vector3(2.25,0,4.9); const p=t.clone().addScaledVector(dir,d); return {pos:p.toArray(),tgt:t.toArray(),fov:30};}
let anim=null, curView='iso';
function go(name,instant=false){
  curView=name; const v=views[name]();
  document.querySelectorAll('[data-view]').forEach(b=>b.classList.toggle('on',b.dataset.view===name));
  if(instant){camera.position.set(...v.pos);controls.target.set(...v.tgt);camera.fov=v.fov;camera.updateProjectionMatrix();controls.update();return;}
  anim={t:0,p0:camera.position.clone(),t0:controls.target.clone(),f0:camera.fov,v};
}
function resize(){const w=stage.clientWidth,h=stage.clientHeight; renderer.setSize(w,h); lr.setSize(w,h); camera.aspect=w/h; camera.updateProjectionMatrix();}
addEventListener('resize',()=>{resize(); if(!anim&&!userMoved) go(curView,true);});
let userMoved=false; controls.addEventListener('start',()=>{userMoved=true;anim=null;});
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>{userMoved=false;go(b.dataset.view);});
function setSeats(n){
  groups.g12.visible=n==12; groups.g15.visible=n==15; labels.forEach(o=>{o.visible=o.userData.g.visible!==false;});
  document.querySelectorAll('[data-seats]').forEach(b=>b.classList.toggle('on',b.dataset.seats==n));
  document.getElementById('sub').textContent='ㄷ자(U형) · '+n+'석';
  const q=new URLSearchParams(location.search); q.set('seats',n); history.replaceState(null,'','?'+q);
}
document.querySelectorAll('[data-seats]').forEach(b=>b.onclick=()=>setSeats(+b.dataset.seats));
const tl=document.getElementById('tgLabel'); tl.onclick=()=>{document.body.classList.toggle('nolabel'); tl.classList.toggle('on');};
const td=document.getElementById('tgDetail'); td.onclick=()=>{document.body.classList.toggle('detail'); td.classList.toggle('on');};
const ts=document.getElementById('tgSwing'); ts.onclick=()=>{swingG.visible=!swingG.visible; ts.classList.toggle('on');};

const qp=new URLSearchParams(location.search);
resize(); setSeats(qp.get('seats')=='15'?15:12);
if(qp.get('labels')=='0'){document.body.classList.add('nolabel'); tl.classList.remove('on');}
if(qp.get('detail')=='1'){document.body.classList.add('detail'); td.classList.add('on');}
go(views[qp.get('view')]?qp.get('view'):'iso',true);
window.__ready=true;
function ease(t){return t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;}
let last=performance.now();
renderer.setAnimationLoop(now=>{
  const dt=Math.min((now-last)/1000,.05); last=now;
  if(anim){anim.t=Math.min(1,anim.t+dt/.9); const e=ease(anim.t);
    camera.position.lerpVectors(anim.p0,new THREE.Vector3(...anim.v.pos),e);
    controls.target.lerpVectors(anim.t0,new THREE.Vector3(...anim.v.tgt),e);
    camera.fov=anim.f0+(anim.v.fov-anim.f0)*e; camera.updateProjectionMatrix(); if(anim.t>=1) anim=null;}
  controls.update(); renderer.render(scene,camera); lr.render(scene,camera);
});
