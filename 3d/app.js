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

const groups={common:new THREE.Group(),g10:new THREE.Group(),g12:new THREE.Group(),g15:new THREE.Group()};
scene.add(groups.common,groups.g10,groups.g12,groups.g15);
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

// ===== 편집 가능한 가구 묶음 =====
const editables=[];
function item(id,name,parent,fn){ const g=new THREE.Group(); g.userData.editId=id; g.userData.name=name; fn(g); parent.add(g);
  const b=new THREE.Box3(); g.updateMatrixWorld(true); g.traverse(o=>{if(o.isMesh){o.geometry.computeBoundingBox(); b.union(o.geometry.boundingBox.clone().applyMatrix4(o.matrixWorld));}});
  const c=b.getCenter(new THREE.Vector3()); c.y=0; g.children.forEach(o=>o.position.sub(c)); g.position.copy(c); editables.push(g); return g; }
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
// 창문(전면 유리벽) y=9800 — 왼쪽 끝(x 0.1~1.0)은 외부 펜트리로 나가는 여닫이문(폭 0.9m·스윙 안쪽, 가정)
{const gm=new THREE.MeshStandardMaterial({color:'#9AD3FF',transparent:true,opacity:.22,roughness:.05,side:THREE.DoubleSide,depthWrite:false});
 for(const [x0,x1] of [[0,0.1],[1.0,W]]){const gl=new THREE.Mesh(new THREE.PlaneGeometry(x1-x0,CEIL),gm); gl.position.set((x0+x1)/2,CEIL/2,L-.01); C.add(gl);}
 for(const x of [0,1.0,2.5,4.5]){const v=new THREE.Mesh(new THREE.BoxGeometry(.05,CEIL,.06),BLACK); v.position.set(x,CEIL/2,L-.01); C.add(v);}
 for(const [x0,x1] of [[0,0.1],[1.0,W]]){const r1=new THREE.Mesh(new THREE.BoxGeometry(x1-x0,.05,.06),BLACK); r1.position.set((x0+x1)/2,.025,L-.01); C.add(r1); const r2=r1.clone(); r2.position.y=CEIL-.025; C.add(r2);}
 // 문틀 + 열린 문짝(경첩 x=0.1, 안쪽 -z 방향으로 90° 열림)
 box(C,100,L*1000-30,40,60,0,DH,BLACK); box(C,1000,L*1000-30,40,60,0,DH,BLACK); box(C,100,L*1000-30,940,60,DH,.05,BLACK);
 const lf=new THREE.Mesh(new THREE.BoxGeometry(.045,DH-.03,.9),M('#CDB48A',{r:.6})); lf.position.set(0.1+.03,(DH-.03)/2,L-.45); lf.castShadow=true; C.add(lf);
 const hd=new THREE.Mesh(new THREE.BoxGeometry(.03,.03,.14),BLACK); hd.position.set(0.1+.07,1.0,L-.85); C.add(hd);
 // 스윙 반경 0.9m 비움 (경첩 기준 안쪽 부채꼴)
 const f=new THREE.Mesh(new THREE.CircleGeometry(.9,40,-Math.PI/2,Math.PI/2),new THREE.MeshBasicMaterial({color:'#FFD43B',transparent:true,opacity:.45,side:THREE.DoubleSide,depthWrite:false})); f.rotation.x=Math.PI/2; f.position.set(0.1,.008,L); f.renderOrder=2; swingG.add(f);
 const ring=new THREE.Mesh(new THREE.RingGeometry(.895,.9,48,1,-Math.PI/2,Math.PI/2),new THREE.MeshBasicMaterial({color:'#B8860B',side:THREE.DoubleSide})); ring.rotation.x=Math.PI/2; ring.position.set(0.1,.01,L); swingG.add(ring);}
label(C,'창 쪽 왼쪽 출입문 (가정 0.9m)',550,2.55,9300,'k');
// 외부 펜트리 (실외, 가정 4.5m×1.3m, 사무실 폭과 같음) — 3D프린터는 문 반대편 오른쪽 끝
{const ef=new THREE.Mesh(new THREE.PlaneGeometry(4.5,1.3),M('#CFD5DB',{r:.95})); ef.rotation.x=-Math.PI/2; ef.position.set(2.25,.003,L+.65+.04); C.add(ef);
 const wm=M('#B8C0C8',{a:.45,ds:true}); box(C,0,L*1000+40,30,1300,0,1.1,wm,false); box(C,4470,L*1000+40,30,1300,0,1.1,wm,false); box(C,0,L*1000+1310,4500,30,0,1.1,wm,false);}
label(C,'외부 펜트리 (실외 · 폭 4.5m 가정)',2800,.5,10900,'k');
label(C,'창문 · 바닥~천장 전면 유리 (뒤쪽)',1700,2.95,9800,'k');

// ===== zones (바닥 색) =====
zone(C,100,2200,3460,3685,'#DCEBFF',.6); zone(C,1100,930,1500,1270,'#DCEBFF',.6);

// ===== 탕비 (입구 왼쪽 앞 벽 한 줄): 냉장고 → 정수기 → 커피머신 → 컵·선반 =====
const tangbi=[];
item('tangbi','탕비 (냉장고·커피·선반)',C,C=>{box(C,50,50,555,637,0,1.45,GRAY); box(C,595,70,10,6,.95,.0,GRAY); box(C,598,100,8,10,1.1,.4,DGRAY); box(C,598,100,8,10,.2,.4,DGRAY);
label(C,'냉장고',330,1.65,370);
box(C,620,50,880,600,0,.88,WHITE); box(C,620,50,880,600,.88,.04,WOOD);
box(C,900,110,420,300,.92,.36,BLACK); box(C,930,160,360,200,1.05,.12,DGRAY);   // 커피머신
box(C,620,50,880,250,1.55,.03,WOOD_D); box(C,640,60,12,230,1.4,.15,BLACK); box(C,1470,60,12,230,1.4,.15,BLACK);  // 선반
label(C,'커피머신(집에서 가져옴) + 선반',1110,1.75,200);});

zone(C,50,690,1130,800,'#FFF3BF',.45);

// ===== LG 퓨리케어 기기 (공기청정기·가습기·정수기) =====
const LGWH=M('#F7F8F8',{r:.45}), LGGRY=M('#3b4048',{r:.6}), LGBLU=M('#6fc3e6',{r:.2,a:.75,ds:true}), LGTEAL=M('#14a3ad',{r:.4,e:'#14a3ad',ei:.6});
function airPurifier(g,cx,cy){ // 315x315x511 (AS186HWWL)
  const x=cx-157,y=cy-157;
  box(g,x,y,315,315,0,.511,LGWH);
  box(g,x-3,y-3,321,321,.10,.30,LGGRY);            // 360˚ 흡입 그릴
  box(g,x+60,y+60,195,195,.511,.012,LGGRY);          // 상단 토출부
  box(g,x+100,y-4,115,6,.43,.03,LGTEAL,false);       // 청정 표시등
  label(g,'공기청정기',cx,.75,cy,'k');
}
function humidifier(g,cx,cy){ // 270x270x750 (HY505RWLAH)
  cyl(g,m(cx),m(cy),.135,0,.19,LGWH,32);
  cyl(g,m(cx),m(cy),.13,.19,.40,LGBLU,32);           // 투명 물통
  cyl(g,m(cx),m(cy),.135,.59,.16,LGWH,32);
  cyl(g,m(cx),m(cy),.09,.75,.012,LGGRY,24);          // 가습 토출구
  cyl(g,m(cx),m(cy),.03,.762,.12,M('#dff3fb',{a:.35}),12);
  label(g,'가습기',cx,.3,cy,'k');
}
function waterPurifier(g,x,y){ // 168(폭,x방향) x 400(깊이,y방향) x 398(높이), 카운터 위 y0=.92, 출수구는 +y(앞)
  box(g,x,y,168,400,.92,.398,LGWH);
  box(g,x+20,y+395,128,10,1.24,.10,LGGRY,false);     // 조작부 + 출수구
  box(g,x+66,y+395,36,18,1.02,.05,LGTEAL,false);
  label(g,'정수기',x+84,1.5,y+200,'k');
}
item('slipper','슬리퍼 랙',C,C=>{box(C,3500,0,900,300,0,.55,M('#F6EBD7',{r:.8})); label(C,'슬리퍼 랙(후보)',3950,.75,150,'s');}); item('air','공기청정기',C,C=>airPurifier(C,4190,1200)); item('water','정수기',C,C=>waterPurifier(C,660,100));

// ===== 전자칠판 75" (제노스미디어 CO750LT4K, 당근 중고) — ㄷ자 열린 쪽 끝에 붙여 화면이 입구 쪽(ㄷ자 상석)을 정면으로 보고, 바로 뒤가 책장 가벽 =====
{const gb=new THREE.Group(); gb.position.set(1.85,0,6.2); gb.rotation.y=Math.PI; // 로컬 +z = 화면 앞 → 월드 -z(입구 쪽)
 const bx=(x,z,w,d,y0,h,mat)=>{const b=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat); b.position.set(x,y0+h/2,z); b.castShadow=true; b.receiveShadow=true; gb.add(b); return b;};
 bx(0,-.055,1.707,.11,.80,1.034,BLACK);                                  // 패널 1707x1034
 bx(0,.003,1.627,.004,.84,.95,M('#1c2733',{r:.2,m:.4}));                // 화면면
 bx(0,-.16,.12,.08,.1,.7,BLACK);                                         // 기둥
 bx(0,-.16,1.1,.07,0,.1,BLACK); bx(-.5,-.31,.06,.42,0,.05,BLACK); bx(.5,-.31,.06,.42,0,.05,BLACK); // 발(크기 가정)
 item('board','전자칠판 75"',C,C=>{C.add(gb); label(C,'전자칠판 75" (ㄷ자 끝에 0.4m · 뒤는 책장 가벽)',1850,2.05,6200,'k');});}
// ===== 28인치 울트라와이드 + 이동식 스탠드(집에서 가져옴): 전자칠판 왼쪽 바로 옆(x 117~932), 같은 면(입구 쪽)을 봄 =====
{const gm=new THREE.Group(); gm.position.set(.525,0,6.21); gm.rotation.y=Math.PI; // 로컬 +z = 화면 앞 → 월드 -z(입구 쪽)
 const bx=(x,z,w,d,y0,h,mat)=>{const b=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat); b.position.set(x,y0+h/2,z); b.castShadow=true; b.receiveShadow=true; gm.add(b); return b;};
 bx(0,-.025,.815,.05,1.05,.36,BLACK);                                    // 패널 815x360x50 (가정)
 bx(0,.001,.78,.004,1.07,.32,M('#1c2733',{r:.2,m:.4}));                  // 화면면
 bx(0,-.09,.06,.06,.1,.95,BLACK);                                        // 기둥
 bx(0,-.18,.60,.34,.05,.05,BLACK);                                       // 바닥판 600x340
 for(const sx of [-.27,.27]) for(const sz of [-.04,-.32]) bx(sx,sz,.05,.05,0,.05,DGRAY); // 바퀴
 item('monitor28','28인치 모니터 + 스탠드',C,C=>{C.add(gm); label(C,'28인치 와이드 모니터 + 스탠드 (집에서 · 칠판 바로 옆)',525,1.65,6210,'k');});}
{const pts=[new THREE.Vector3(1.85,1.0,6.15),new THREE.Vector3(1.85,1.0,5.8)]; const ln=new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts),new THREE.LineDashedMaterial({color:'#7B61FF',dashSize:.12,gapSize:.08})); ln.computeLineDistances(); C.add(ln);
 label(C,'U 끝↔칠판 약 0.40m',2900,1.2,6000,'s');}

// 에어컨 (천장) — 프로젝터·전동 스크린·이동식 화이트보드는 칠판이 뒤쪽으로 가서 도면에서 뺌
{const ac=new THREE.Mesh(new THREE.CylinderGeometry(.26,.26,.12,32),M('#e8ebee')); ac.position.set(2.25,CEIL-.06,4.95); C.add(ac); label(C,'천장형 에어컨',2250,2.45,4950,'s');}


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
function utable(g){ // 데스커 멀티데스크 1800x800 x5 (진짜 크기): 양팔 2개씩 + 입구 쪽 상석 1개(양팔 끝을 잇는 다리). 안쪽 통로 0.7m, 상석은 양팔 중심(x=1850)에 대칭
  for(const [x,y,w,d] of [[700,2200,800,1800],[700,4000,800,1800],[2200,2200,800,1800],[2200,4000,800,1800],[950,1400,1800,800]]) table(g,x,y,w,d);
  const sm=M('#8a6a3a'); // 이음매
  for(const [x,y,w,d] of [[700,3997,800,6],[2200,3997,800,6]]) box(g,x,y,w,d,.72,.003,sm,false);
}
function uchairs(g,n,pitchN,bx){ // n: 팔당 의자 수, bx: 상석 의자 x들
  for(let i=0;i<n;i++){const y=2200+3600*(i+.5)/n; chair(g,440,y,1,0); chair(g,3260,y,-1,0);}
  for(const x of bx) chair(g,x,1140,0,1);
}
function sofa(g,cx,cy,len,dep,back='down',n=3,name){ // cx,cy 평면 중심(mm), len 길이, dep 깊이, back: down(+y 창쪽)/up(-y 가벽쪽)/right(+x 벽쪽)
  const s=new THREE.Group(); s.position.set(m(cx),0,m(cy)); s.rotation.y=(back==='right')?Math.PI/2:(back==='left'?-Math.PI/2:(back==='up'?Math.PI:0));
  const L=m(len),D=m(dep),arm=.15,bk=.22;
  const body=M('#B8966A',{r:.9}), cus=M('#E7D5BC',{r:.95}), pil=M('#6B8FD6',{r:.9});
  const add=(w,h,d,x,y,z,mat)=>{const b=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat); b.position.set(x,y,z); b.castShadow=true; b.receiveShadow=true; s.add(b); return b;};
  add(L,.22,D,0,.19,0,body);                                  // 하부 프레임
  for(const sx of [-1,1]) for(const sz of [-1,1]) add(.05,.08,.05,sx*(L/2-.08),.04,sz*(D/2-.08),BLACK);
  add(L,.55,bk,0,.58,D/2-bk/2,body);                          // 등받이 프레임
  add(arm,.30,D,-(L/2-arm/2),.45,0,body); add(arm,.30,D,(L/2-arm/2),.45,0,body); // 팔걸이
  const iw=(L-2*arm)/n, sd=D-bk-.02;
  for(let i=0;i<n;i++){ const x=-(L/2-arm)+iw*(i+.5);
    add(iw-.025,.15,sd,x,.375,-bk/2,cus);                      // 좌석 쿠션
    const bc=add(iw-.04,.38,.13,x,.68,D/2-bk-.05,cus); bc.rotation.x=-.12; }  // 등 쿠션
  add(.4,.38,.12,-(L/2-arm-.28),.62,D/2-bk-.18,pil).rotation.z=.2; // 쿠션 하나
  g.add(s); return s;
}
function bean(g,x,y,col='#8FB3E8'){const b=new THREE.Mesh(new THREE.SphereGeometry(1,24,16),M(col,{r:.95})); b.scale.set(.27,.21,.27); b.position.set(m(x),.2,m(y)); b.castShadow=true; g.add(b);}
function shelf(g,x,y,w,d,col=WOOD_D,h=2.0,withBooks=true){ // 책장: 앞면이 -x 방향
  box(g,x+d-18,y,18,w,0,h,M('#8a6a3a')); // 뒷판
  for(const yy of [0,.4,.8,1.2,1.6,h-.03]) box(g,x,y,d,w,yy,.03,col);
  box(g,x,y,d,22,0,h,col); box(g,x,y+w-22,d,22,0,h,col); box(g,x,y+w/2-11,d,22,0,h,col);
  if(withBooks){const cols=['#c0563b','#3b6fc0','#e0b84a','#4a8f6b','#eee','#7a5aa8']; let k=0;
    for(const yy of [.03,.43,.83,1.23]) for(let z=y+40;z<y+w-60;z+=70+((k*37)%40)){ const hh=.2+((k*53)%15)/100; box(g,x+60,z,d-110,36+(k%3)*8,yy,hh,M(cols[k%6],{r:.8}),false); k++; }}
}
// ===== 10석 (기본) =====
const T10=groups.g10;
item('u10','ㄷ자 책상 세트 (10석)',T10,g=>{utable(g); uchairs(g,4,0,[1400,2300]); });
label(T10,'멀티데스크 1800×800 ×5 (상석 쪽이 입구)',1850,.95,1800,'k');
label(T10,'의자 · 교육 10석 (바깥에서 안쪽을 봄)',440,1.05,4000,'k');
label(T10,'U 안쪽 발표·토론 공간 (폭 0.7m)',1850,.3,4300,'s');
// ===== 12석 =====
const A=groups.g12;
item('u12','ㄷ자 책상 세트 (12석)',A,g=>{utable(g); uchairs(g,5,0,[1400,2300]); });
label(A,'멀티데스크 1800×800 ×5 (상석 쪽이 입구)',1850,.95,1800,'k'); 
label(A,'의자 · 교육 12석 (바깥에서 안쪽을 봄)',440,1.05,4000,'k');
label(A,'U 안쪽 발표·토론 공간 (폭 0.7m)',1850,.3,4300,'s');
// ===== 뒤쪽 공통 (12·15석): 칠판 바로 뒤 낮은 책장 가벽 + 그 뒤 라운지(소파) + 대표실(대표 · 서진이) =====
zone(C,0,7100,4500,2700,'#FFE8EC',.5);
// 낮은 책장 가벽: 이케아 BILLY 80x28x106 x3 (x 0~2400, y 6820~7100, 왼쪽 벽에 붙이고 오른쪽 2.1m 트임). 뒷판이 칠판 쪽(-y), 열린 앞면이 소파·대표실(+y)
function billy(g,x,y){ const w=800,d=280,h=1.06, wd=M('#F2F0EA',{r:.6});
  box(g,x,y,w,12,0,h,wd);                                     // 뒷판 (칠판 쪽)
  box(g,x,y,22,d,0,h,wd); box(g,x+w-22,y,22,d,0,h,wd);        // 옆판
  for(const yy of [0,.34,.68,h-.03]) box(g,x,y,w,d,yy,.03,wd); // 바닥·선반·상판
  const cols=['#c0563b','#3b6fc0','#e0b84a','#4a8f6b','#eee','#7a5aa8']; let k=0;
  for(const yy of [.03,.37]) for(let z=x+40;z<x+w-80;z+=64+((k*37)%30)){ box(g,z,y+60,34+(k%3)*8,d-110,yy,.2+((k*53)%12)/100,M(cols[k%6],{r:.8}),false); k++; }
}
item('billy','책장 가벽 (빌리 ×3)',C,C=>{for(const x0 of [0,800,1600]) billy(C,x0,6820);
// 마샬 스피커(액톤 III 260x170x150) — 가벽 위 왼쪽 끝
box(C,200,6875,260,170,1.06,.15,M('#1d1d1d',{r:.6})); box(C,215,6872,230,4,1.09,.07,M('#c9a24a',{r:.4}),false);
label(C,'마샬 스피커',330,1.3,6960,'s');
label(C,'낮은 책장 가벽 (빌리 ×3 · 칠판 바로 뒤)',1200,1.3,6960,'k');});
label(C,'가벽 뒤: 대표실 · 서진이',1900,.4,7500,'s');
// 창 쪽: 서진이 책상(창가). 모션데스크 #2·복합기·대표는 입구 쪽 한 줄(y 7650~8350, 창쪽 왼쪽 문 앞을 비움). 대표 시선은 출입문 정면
const MD=M('#F1E6D3');
function motion(C,x,y){ box(C,x,y,1500,700,.7,.04,MD); for(const [lx,ly] of [[x+30,y+30],[x+1420,y+30],[x+30,y+620],[x+1420,y+620]]) box(C,lx,ly,50,50,0,.7,BLACK); }
item('desk2','모션데스크 #2',C,C=>{motion(C,50,7650); box(C,300,7720,800,60,.95,.35,M('#2B2F36')); chair(C,800,8550,0,-1,'#6B7684',1);                    // 문 앞을 비우려고 대표 책상과 같은 줄(입구 쪽)로 옮김
label(C,'모션데스크 #2 (신규 · 대표와 동일 1500×700)',800,1.3,8000,'k');});
// 복합기 + NAS·공유기 선반 (두 책상 사이, 대표 책상 바로 옆)
item('copier','복합기 + NAS 선반',C,C=>{box(C,1550,7650,380,460,0,.95,WHITE); box(C,1550,7650,380,460,.95,.04,DGRAY); box(C,1570,7690,340,250,.99,.04,BLACK);
label(C,'복합기 (집에서 이전)',1740,1.15,7880,'k');
box(C,1550,7650,300,460,1.3,.03,WOOD_D); box(C,1560,7660,30,440,1.0,.3,BLACK); box(C,1820,7660,30,440,1.0,.3,BLACK);
box(C,1590,7730,220,320,1.33,.22,M('#7B61FF',{r:.5})); label(C,'NAS·공유기 (ASUS RT-BE92U)',1740,1.75,7880,'s');});
// 대표: 책상 입구 쪽(북), 의자 창 쪽(남). 34" 화면 남쪽 향함 → 입구에선 모니터 뒷면
item('ceo','대표 책상',C,C=>{motion(C,1930,7650); box(C,3130,7860,200,200,.74,.095,M('#c9ced6',{m:.7,r:.3}));                      // Mac Studio
chair(C,2680,8550,0,-1,'#F04452',1);
label(C,'대표석 (출입문 정면)',2680,1.3,8000,'k');});
// 서진이 책상: 창문 벽에 붙임 (가로 1000x600, x 2180~3180, y 9200~9800), 의자는 창 쪽(남)을 봄
item('seojin','서진이 책상',C,C=>{table(C,2180,9200,1000,600,MD,.72);
box(C,2530,9700,300,25,.75,.30,M('#2B2F36'));
chair(C,2680,9000,0,1,'#4DB6BD',.9);
label(C,'서진이 책상 1000×600 (창가)',2680,1.0,9500,'k');});
// 로봇청소기 도크 + 가습기 (창 쪽, 두 의자 사이)
item('robot','로봇청소기 도크',C,C=>{box(C,3300,9420,400,350,0,.12,M('#EDEFF2')); cyl(C,3.50,9.595,.17,.0,.03,DGRAY,28);
label(C,'로봇청소기 도크 (기존)',3500,.5,9595,'s');});
item('humid','가습기',C,C=>humidifier(C,1950,9580));
// 소파 2인: 칠판 오른쪽 · 오른쪽 벽 (가벽 뒤에서 이전)
item('sofa','소파 2인',C,C=>{sofa(C,4075,7170,1200,850,'right',2); label(C,'소파 2인 (오른쪽 벽)',4075,1.1,7170,'k');});
// 티테이블: 소파 앞(서쪽) 0.35m · 원형 지름 370 × 높이 580 (플라팜 라운드 기준), 가벽 y범위 밖
item('teatable','티테이블',C,C=>{const tx=3115,ty=7350, TTW=M('#C9A877',{r:.5}), TTL=M('#9A7B4F',{r:.6});
 cyl(C,m(tx),m(ty),.185,.55,.03,TTW,32); cyl(C,m(tx),m(ty),.02,.04,.51,TTL,12); cyl(C,m(tx),m(ty),.14,0,.04,TTL,28);
 label(C,'티테이블 Ø370 (소파 앞 0.35m)',tx,.8,ty,'s');});

// 3D 프린터 maker — 외부 펜트리(실외) 오른쪽 끝 · 문 반대편
{const dx=3790,dy=900;
zone(C,50+dx,9200+dy,560,540,'#FFE9CC',.8);
table(C,60+dx,9210+dy,540,520,WOOD_D,.74);
box(C,90+dx,9240+dy,480,460,.74,.42,M('#ffffff',{a:.5})); for(const [a,b] of [[100,9250],[520,9250],[100,9640],[520,9640]]) box(C,a+dx,b+dy,40,40,.74,.42,M('#E67E22'));
box(C,200+dx,9330+dy,260,260,.78,.3,M('#2c3138'));
label(C,'3D프린터 (외부 펜트리 오른쪽 끝 · 문 반대편)',330+dx,1.1,9470+dy,'k');}
// ===== CCTV 2대 (실내) =====
function cctv(x,y,ang,fov,rad,txt){ // ang/fov: 도, 평면 각도(+x→+y)
  const cam=new THREE.Group(); cam.position.set(m(x),2.25,m(y)); const body=new THREE.Mesh(new THREE.BoxGeometry(.12,.09,.1),M('#1d1f23')); cam.add(body);
  const dot=new THREE.Mesh(new THREE.SphereGeometry(.025,12,8),M('#E03131',{e:'#E03131',ei:1})); dot.position.set(0,0,.06); cam.add(dot); C.add(cam);
  const sec=new THREE.Mesh(new THREE.CircleGeometry(m(rad),40,(ang-fov/2)*Math.PI/180,fov*Math.PI/180),new THREE.MeshBasicMaterial({color:'#FF6B6B',transparent:true,opacity:.14,side:THREE.DoubleSide,depthWrite:false}));
  sec.rotation.x=Math.PI/2; sec.position.set(m(x),.03,m(y)); C.add(sec); cctvG.push(sec);
  label(C,txt,x+(x<3000?-500:0),(x<3000?3.3:2.9),y+(y<500?420:0),'k');
}
const cctvG=[];
cctv(2750,70,135,90,2550,'CCTV ① 입구·탕비'); cctv(4430,4000,180,70,3800,'CCTV ② 책상·U');



// ===== 15석 =====
const B=groups.g15;
item('u15','ㄷ자 책상 세트 (15석)',B,g=>{utable(g); uchairs(g,6,0,[1250,1850,2450]); });
label(B,'멀티데스크 1800×800 ×5 (상석 쪽이 입구)',1850,.95,1800,'k'); label(B,'의자 · 교육 15석 (바깥에서 안쪽을 봄)',440,1.05,4000,'k'); label(B,'U 안쪽 발표·토론 공간 (폭 0.7m)',1850,.3,4300,'s');


// ===== UI / 카메라 =====
const tgt=new THREE.Vector3();
const views={
  entrance:()=>({pos:[2.25,1.62,.55],tgt:[2.25,1.0,6.8],fov:68}),
  top:()=>{const a=renderer.domElement.clientWidth/renderer.domElement.clientHeight; const f=40*Math.PI/180; const vh=(L+3.8)/2/Math.tan(f/2)*1.12, hh=(W+1.2)/2/Math.tan(f/2)/a; const d=Math.max(vh,hh); return {pos:[2.25,d,4.9+.4],tgt:[2.25,0,4.9],fov:40};},
  iso:()=>isoView(1), iso2:()=>isoView(-1),
  board:()=>({pos:[1.9,2.1,3.7],tgt:[1.4,.9,6.3],fov:55})   // 전자칠판·옆 모니터 근접(입구 쪽에서)
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
  groups.g10.visible=n==10; groups.g12.visible=n==12; groups.g15.visible=n==15; labels.forEach(o=>{let v=true; for(let p=o.userData.g;p;p=p.parent) if(p.visible===false) v=false; o.visible=v;});
  document.querySelectorAll('[data-seats]').forEach(b=>b.classList.toggle('on',b.dataset.seats==n));
  document.getElementById('sub').textContent='ㄷ자(U형) · '+n+'석';
  const q=new URLSearchParams(location.search); q.set('seats',n); history.replaceState(null,'','?'+q);
}
document.querySelectorAll('[data-seats]').forEach(b=>b.onclick=()=>setSeats(+b.dataset.seats));
const tl=document.getElementById('tgLabel'); tl.onclick=()=>{document.body.classList.toggle('nolabel'); tl.classList.toggle('on');};
const td=document.getElementById('tgDetail'); td.onclick=()=>{document.body.classList.toggle('detail'); td.classList.toggle('on');};
const ts=document.getElementById('tgSwing'); ts.onclick=()=>{swingG.visible=!swingG.visible; ts.classList.toggle('on');};

const qp=new URLSearchParams(location.search);
resize(); setSeats(qp.get('seats')=='15'?15:qp.get('seats')=='12'?12:10);
if(qp.get('labels')=='0'){document.body.classList.add('nolabel'); tl.classList.remove('on');}
if(qp.get('detail')=='1'){document.body.classList.add('detail'); td.classList.add('on');}
go(views[qp.get('view')]?qp.get('view'):'iso',true);

function ease(t){return t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;}
let last=performance.now();
renderer.setAnimationLoop(now=>{
  const dt=Math.min((now-last)/1000,.05); last=now;
  if(anim){anim.t=Math.min(1,anim.t+dt/.9); const e=ease(anim.t);
    camera.position.lerpVectors(anim.p0,new THREE.Vector3(...anim.v.pos),e);
    controls.target.lerpVectors(anim.t0,new THREE.Vector3(...anim.v.tgt),e);
    camera.fov=anim.f0+(anim.v.fov-anim.f0)*e; camera.updateProjectionMatrix(); if(anim.t>=1) anim=null;}
  if(selHelper) selHelper.update(); controls.update(); renderer.render(scene,camera); lr.render(scene,camera);
});

// ===== 편집 모드: 선택 · 드래그 · 회전 · 저장(localStorage) · 내보내기/불러오기 =====
const LS_KEY='odg3d-layout-v2';
let editOn=false, sel=null, selHelper=null, drag=null, snap=true;
const defaults={}; const ray=new THREE.Raycaster(), ndc=new THREE.Vector2(), floorPl=new THREE.Plane(new THREE.Vector3(0,1,0),0);
function curLayout(){const it={}; editables.forEach(g=>{it[g.userData.editId]={x:+g.position.x.toFixed(3),z:+g.position.z.toFixed(3),r:+g.rotation.y.toFixed(4)};}); return {version:1,app:'office-desk-guide-3d',savedAt:new Date().toISOString(),items:it};}
function applyLayout(L){ if(!L||!L.items) return; editables.forEach(g=>{const v=L.items[g.userData.editId]; if(v&&isFinite(v.x)&&isFinite(v.z)){g.position.x=v.x; g.position.z=v.z; g.rotation.y=+v.r||0;}}); if(sel) select(sel); }
function clampIn(g){ g.updateMatrixWorld(true); const b=new THREE.Box3(); g.traverse(o=>{if(o.isMesh){b.union(o.geometry.boundingBox.clone().applyMatrix4(o.matrixWorld));}});
  let dx=0,dz=0; if(b.max.x-b.min.x<W){ if(b.min.x<0) dx=-b.min.x; else if(b.max.x>W) dx=W-b.max.x; } if(b.max.z-b.min.z<L){ if(b.min.z<0) dz=-b.min.z; else if(b.max.z>L) dz=L-b.max.z; }
  g.position.x+=dx; g.position.z+=dz; }
const tip=document.createElement('div'); tip.id='seltip'; tip.hidden=true; document.body.appendChild(tip);
function select(g){ sel=g; if(selHelper){scene.remove(selHelper); selHelper=null;}
  if(g){ selHelper=new THREE.BoxHelper(g,0x3182F6); selHelper.material.depthTest=false; selHelper.renderOrder=10; scene.add(selHelper); tip.textContent='선택: '+g.userData.name; tip.hidden=false; } else tip.hidden=true;
  document.getElementById('edRot').disabled=!g; }
function pick(e){ const r=renderer.domElement.getBoundingClientRect(); ndc.set((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1); ray.setFromCamera(ndc,camera); }
function hit(){ const vis=editables.filter(g=>{for(let p=g;p;p=p.parent) if(!p.visible) return false; return true;});
  const hs=ray.intersectObjects(vis,true); for(const h of hs){ let o=h.object; while(o&&!o.userData.editId) o=o.parent; if(o) return o; } return null; }
function rotateSel(){ if(!sel) return; sel.rotation.y=Math.round((sel.rotation.y+Math.PI/2)/(Math.PI/2))*(Math.PI/2)%(Math.PI*2); clampIn(sel); dirty(true); }
function dirty(v){ document.getElementById('edSave').classList.toggle('pend',v); }
function initEditor(){
  // 기본값 기억 → 저장본 불러오기
  editables.forEach(g=>defaults[g.userData.editId]={x:g.position.x,z:g.position.z,r:g.rotation.y});
  try{ const s=localStorage.getItem(LS_KEY); if(s) applyLayout(JSON.parse(s)); }catch(e){}
  const $=id=>document.getElementById(id), cv=renderer.domElement;
  $('edToggle').onclick=()=>{ editOn=!editOn; document.body.classList.toggle('editing',editOn); $('edToggle').classList.toggle('on',editOn); $('edToggle').textContent=editOn?'편집 끝':'편집'; if(!editOn) select(null); };
  $('edRot').onclick=rotateSel;
  $('edSnap').onclick=()=>{snap=!snap; $('edSnap').classList.toggle('on',snap);};
  $('edSave').onclick=()=>{ localStorage.setItem(LS_KEY,JSON.stringify(curLayout())); dirty(false); toast('저장했어요 (이 기기 브라우저)'); };
  $('edReset').onclick=()=>{ if(!confirm('기본 배치로 되돌릴까요? 저장한 배치도 지워져요.')) return; localStorage.removeItem(LS_KEY); applyLayout({items:defaults}); dirty(false); toast('기본 배치로 되돌렸어요'); };
  $('edExport').onclick=()=>{ const txt=JSON.stringify(curLayout(),null,1); const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([txt],{type:'application/json'})); a.download='office-layout-'+new Date().toISOString().slice(0,10)+'.json'; document.body.appendChild(a); a.click(); a.remove();
    (navigator.clipboard?navigator.clipboard.writeText(txt):Promise.reject()).then(()=>toast('파일 저장 + 클립보드 복사 완료'),()=>toast('파일로 내보냈어요')); };
  $('edImport').onclick=()=>$('edFile').click();
  $('edFile').onchange=e=>{ const f=e.target.files[0]; if(!f) return; f.text().then(t=>{ applyLayout(JSON.parse(t)); dirty(true); toast('불러왔어요 · 저장을 눌러야 유지돼요'); }).catch(()=>toast('JSON 파일을 읽지 못했어요')); e.target.value=''; };
  addEventListener('keydown',e=>{ if(editOn&&(e.key==='r'||e.key==='R')&&!e.metaKey&&!e.ctrlKey) rotateSel(); if(editOn&&e.key==='Escape') select(null); });
  cv.addEventListener('pointerdown',e=>{ if(!editOn||!e.isPrimary) return; pick(e); const g=hit(); if(!g){ return; }
    select(g); const p=new THREE.Vector3(); if(!ray.ray.intersectPlane(floorPl,p)) return;
    drag={g,id:e.pointerId,off:new THREE.Vector3().subVectors(g.position,p),moved:false}; controls.enabled=false; cv.setPointerCapture(e.pointerId); e.preventDefault(); e.stopPropagation(); },{capture:true});
  cv.addEventListener('pointermove',e=>{ if(!drag||e.pointerId!==drag.id) return; pick(e); const p=new THREE.Vector3(); if(!ray.ray.intersectPlane(floorPl,p)) return;
    let x=p.x+drag.off.x, z=p.z+drag.off.z; if(snap){x=Math.round(x*10)/10; z=Math.round(z*10)/10;} drag.g.position.x=x; drag.g.position.z=z; clampIn(drag.g); drag.moved=true; },{capture:true});
  const end=e=>{ if(!drag||e.pointerId!==drag.id) return; if(drag.moved) dirty(true); drag=null; controls.enabled=true; };
  cv.addEventListener('pointerup',end,{capture:true}); cv.addEventListener('pointercancel',end,{capture:true});
  window.__editor={editables,curLayout,proj:(x,y,z)=>{const v=new THREE.Vector3(x,y,z).project(camera),r=cv.getBoundingClientRect(); return [r.left+(v.x+1)/2*r.width,r.top+(1-v.y)/2*r.height];}};
}
let toastT; function toast(t){ const el=document.getElementById('toast'); el.textContent=t; el.hidden=false; clearTimeout(toastT); toastT=setTimeout(()=>el.hidden=true,2200); }

initEditor();
window.__ready=true;
