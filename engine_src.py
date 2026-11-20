import os,sys,json,urllib.request
H=os.environ.get("MAKEFUN_ENV_URL")
NB=int(os.environ.get("MAKEFUN_NODES_PER_MOVE","900"))
P,N,B,R,Q,K=1,2,3,4,5,6
V=[0,100,320,330,500,900,0]
MATE=30000
NEG=-MATE
MAXD=16
NB_CAP=NB
KN=(14,18,31,33,-14,-18,-31,-33)
KM=(1,-1,15,-15,16,-16,17,-17)
BS=(-17,-15,15,17)
RS=(-16,-1,1,16)
def s64(i):return (i>>4)*8+(i&7)
PW=tuple(r*7+(2 if f in (2,5) else 0) for r in range(8) for f in range(8))
PN=tuple(max(0,24-4*(abs(f-3.5)+abs(r-3.5))) for r in range(8) for f in range(8))
PB=tuple(10+4*min(r,7-r,f,7-f)-18*(abs(r-f)+abs(r+f-7)) for r in range(8) for f in range(8))
PR=tuple((8 if r in (0,7) else 0)+(5 if f in (0,7) else 0)+(20 if r==6 else 0) for r in range(8) for f in range(8))
PQ=tuple(4*min(r,7-r,f,7-f) for r in range(8) for f in range(8))
PKM=tuple((-30 if r<2 else (-50 if 3<=r<=4 and 3<=f<=4 else (-10 if 2<=r<=5 and 2<=f<=5 else 0)))+(20 if (r in (0,7) and f in (0,7)) else 0) for r in range(8) for f in range(8))
def pf(t):
 b=[0]*128;r=c=0
 for x in t.split()[0]:
  if x=="/":r+=1;c=0;continue
  if x>"9":b[(7-r)*16+c]=("PNBRQKpnbrqk".find(x)%6+1)|(8 if x>="a" else 0);c+=1;continue
  c+=int(x)
 s=0 if t.split()[1]=="w" else 8;cr=0
 for z in t.split()[2]:
  if z=="K":cr|=1
  elif z=="Q":cr|=2
  elif z=="k":cr|=4
  elif z=="q":cr|=8
 ep=-1
 if t.split()[3]!="-":ep="abcdefgh".index(t.split()[3][0])+(8-int(t.split()[3][1]))*16
 return [b,s,cr,ep,int(t.split()[4]),int(t.split()[5])]
def OB(i):return 0<=i<128 and (i&8)==0
def at(d,t,w):
 for i in range(128):
  z=d[i]
  if not z or (i&8)!=0 or (z&8)!=w:continue
  z&=7
  if z==P:
   if i+(-16 if w==8 else 16)+(-1 if t<i else 1)==t:return 1
  elif z==N:
   for x in KN:
    if i+x==t:return 1
  elif z in (B,R,Q):
   st=BS if z==B else(RS if z==R else BS+RS)
   for x in st:
    j=i+x
    while 0<=j<128 and OB(j):
     if j==t:return 1
     if d[j]:break
     j+=x
  else:
   for x in KM:
    if i+x==t:return 1
 return 0
def ks(d,s):
 for i in range(128):
  if OB(i) and d[i]==(K|s):return i
 return -1
def chk(d,s):return at(d,ks(d,s),s^8)
def baX(s):return 0 if s==0 else 112
def gm(d,s,ca,ep):
 caP=[];qu=[];ba=0 if s==0 else 112
 for i in range(128):
  z=d[i]
  if not z or (i&8)!=0 or (z&8)!=s:continue
  z&=7;dd=16 if s==0 else-16
  if z==P:
   w=i+dd
   if OB(w) and not d[w]:
    if (w>>4)==(7 if s==0 else 0):caP+=tuple(((i<<14)|(w<<7)|y) for y in (N,B,R,Q))
    else:qu.append((i<<14)|(w<<7)|0)
   if (i>>4)==(1 if s==0 else 6) and not d[w+dd]:qu.append((i<<14)|((w+dd)<<7)|0)
   for dc in (-1,1):
    w=i+dd+dc
    if 0<=w<128 and OB(w):
     c=d[w]
     if c and (c&8)!=s:
      if (w>>4)==(7 if s==0 else 0):caP+=tuple(((i<<14)|(w<<7)|y) for y in (N,B,R,Q))
      else:caP.append((i<<14)|(w<<7)|0)
     elif w==ep:caP.append((i<<14)|(w<<7)|6)
  elif z==N:
   for x in KN:
    w=i+x
    if 0<=w<128 and OB(w):
     c=d[w]
     if c:
      if (c&8)!=s:caP.append((i<<14)|(w<<7)|0)
     else:qu.append((i<<14)|(w<<7)|0)
  elif z in (B,R,Q):
   st=BS if z==B else(RS if z==R else BS+RS)
   for x in st:
    w=i+x
    while 0<=w<128 and OB(w):
     c=d[w]
     if c:
      if (c&8)!=s:caP.append((i<<14)|(w<<7)|0)
      break
     qu.append((i<<14)|(w<<7)|0);w+=x
  else:
   for x in KM:
    w=i+x
    if 0<=w<128 and OB(w):
     c=d[w]
     if c:
      if (c&8)!=s:caP.append((i<<14)|(w<<7)|0)
     else:qu.append((i<<14)|(w<<7)|0)
 if d[baX(s)+4]==(K|s):
  if ca&(1 if s==0 else 4) and not d[baX(s)+5] and not d[baX(s)+6] and not chk(d,s) and not at(d,baX(s)+5,s^8) and not at(d,baX(s)+6,s^8):caP.append(((baX(s)+4)<<14)|((baX(s)+6)<<7)|7)
  if ca&(2 if s==0 else 8) and not d[baX(s)+1] and not d[baX(s)+2] and not d[baX(s)+3] and not chk(d,s) and not at(d,baX(s)+3,s^8) and not at(d,baX(s)+2,s^8):caP.append(((baX(s)+4)<<14)|((baX(s)+2)<<7)|8)
 return caP+qu
def mvpc(sp,s,pt):return (s|K) if sp in (7,8) else ((s|pt) if sp==0 else (s|sp))
def ap(d,mv,st):
 f=(mv>>14)&127;t=(mv>>7)&127;sp=mv&127;pc=d[f];pt=pc&7;s=pc&8
 ci=[d[f],d[t],st[1],st[2],st[3],st[4],st[5]]
 d[t]=mvpc(sp,s,pt);d[f]=0;nm=st[4]+1;ne=-1;ca=st[2]
 if pt==P:
  nm=0
  if sp==5:ne=f+(-16 if s==0 else 16)
  if sp==7:d[baX(s)+7]=0;d[baX(s)+6]=(s|K);d[baX(s)+5]=(s|R)
  elif sp==8:d[baX(s)+0]=0;d[baX(s)+2]=(s|K);d[baX(s)+3]=(s|R)
  ca=st[2]&~(1 if s==0 else 4)&~(2 if s==0 else 8)
 elif pt==R:ne=-1;ca=st[2]
 if f==baX(s):ca&=~(2 if s==0 else 8)
 elif f==baX(s)+7:ca&=~(1 if s==0 else 4)
 else:ne=-1;ca=st[2]
 ns=s^8;sflag=st[5]+(1 if s==8 else 0)
 if ci[1]:nm=0
 if sp==6:d[t+(-16 if s==0 else 16)]=0
 st[1]=ns;st[2]=ca;st[3]=ne;st[4]=nm;st[5]=sflag
 ci[6]=sflag
 return ci
def um(d,mv,ci,st):
 f=(mv>>14)&127;t=(mv>>7)&127;sp=mv&127;sd=ci[2]
 if sp==6:d[t]=0;d[f]=ci[0];d[t+(-16 if sd==0 else 16)]=ci[1]
 elif sp==7:d[baX(sd)+6]=0;d[baX(sd)+5]=0;d[baX(sd)+7]=(R|sd);d[f]=ci[0]
 elif sp==8:d[baX(sd)+3]=0;d[baX(sd)+0]=(R|sd);d[f]=ci[0]
 else:d[t]=ci[1];d[f]=ci[0]
 st[1]=ci[2];st[2]=ci[3];st[3]=ci[4];st[4]=ci[5];st[5]=ci[6]
def ev(d,s):
 w=0;kw=-1;kwo=-1;wb=0;ob=0
 for i in range(128):
  z=d[i]
  if not z or (i&8)!=0:continue
  pt=z&7;c=z&8
  if pt==B:
   if c==0:wb+=1
   else:ob+=1
  ix=s64(i)
  if pt==P:m=V[P]+PW[ix if c==0 else 63-ix]
  elif pt==N:m=V[N]+PN[ix if c==0 else 63-ix]
  elif pt==B:m=V[B]+PB[ix if c==0 else 63-ix]
  elif pt==R:m=V[R]+PR[ix if c==0 else 63-ix]
  elif pt==Q:m=V[Q]+PQ[ix if c==0 else 63-ix]
  else:m=PKM[ix if c==0 else 63-ix]
  if c==0:w+=m;kw=i
  else:w-=m;kwo=i
 if wb>=2:w+=30
 if ob>=2:w-=30
 for sd in (0,8):
  for f in range(8):
   n=0
   for rr in range(8):
    if (rr*16+f&8)==0 and d[rr*16+f]==(P|sd):n+=1
   if n>1:w-=12*(n-1) if sd==0 else-12*(n-1)
 for i in range(128):
  z=d[i]
  if not z or (i&8)!=0 or (z&7)!=P:continue
  c=z&8;ix=s64(i);rr=ix//8;ff=ix%8;passed=1
  for df in (ff-1,ff,ff+1):
   if df<0 or df>7:continue
   for qr in (range(rr+1,8) if c==0 else range(rr)):
    j=qr*16+df
    if 0<=j<120 and OB(j) and d[j]==(P|8 if c==0 else P):passed=0;break
   if not passed:break
  if passed:w+=(0,0,0,0,0,8,18,32,50)[rr] if c==0 else-(0,0,0,0,0,8,18,32,50)[7-rr]
 for i in range(128):
  z=d[i]
  if not z or (i&8)!=0 or (z&7)!=R:continue
  c=z&8;ffo=s64(i)&7;op=1
  for rr in range(8):
   j=rr*16+ffo
   if 0<=j<120 and OB(j) and (d[j]&7)==P:op=0;break
  if op:w+=18 if c==0 else-18
 w+=16 if s==0 else-16
 sfc=24
 if kw>=0 and kwo>=0:
  co=0;pd=-16 if kwo==8 else 16
  for dc in (-1,1):
   j=kw+pd+dc
   if 0<=j<128 and OB(j) and d[j]==(P|kwo^8):co+=1
  for x in KN:
   j=kw+x
   if 0<=j<128 and OB(j) and d[j]==(N|kwo^8):co+=2
  for x in BS+RS:
   j=kw+x
   while 0<=j<128 and OB(j):
    z=d[j]
    if z:
     if (z&8)==kwo^8 and (z&7) in (B,R,Q):co+=2;break
     j+=x
  w-=22*co*sfc//32
  ce=0;pd=-16 if kw==8 else 16
  for dc in (-1,1):
   j=kwo+pd+dc
   if 0<=j<128 and OB(j) and d[j]==(P|kw^8):ce+=1
  for x in KN:
   j=kwo+x
   if 0<=j<128 and OB(j) and d[j]==(N|kw^8):ce+=2
  for x in BS+RS:
   j=kwo+x
   while 0<=j<128 and OB(j):
    z=d[j]
    if z:
     if (z&8)==kw^8 and (z&7) in (B,R,Q):ce+=2;break
     j+=x
  w+=22*ce*sfc//32
  if kw<112:
   j=kw+16
   if 0<=j<120 and OB(j) and not d[j]:w-=6*sfc//32
   if (j-1&8)==0 and not d[j-1] and kw&7:w-=2*sfc//32
   if (j+1&8)==0 and not d[j+1] and kw&7<7:w-=2*sfc//32
  else:
   j=kw-16
   if 0<=j<120 and OB(j) and not d[j]:w-=6*sfc//32
   if (j-1&8)==0 and not d[j-1] and kw&7:w-=2*sfc//32
   if (j+1&8)==0 and not d[j+1] and kw&7<7:w-=2*sfc//32
 return w if s==0 else-w
_HMASK=(1<<64)-1
_HX=0x9E3779B97F4A7C15
def hr():
 global _HX
 _HX=(_HX*6364136223846793005+1442695040888963407)&_HMASK
 return _HX
PSQH=[[[hr() for _ in range(64)] for _ in range(2)] for _ in range(7)]
ZSIDE=hr();ZCA=[hr() for _ in range(4)];ZEP=[hr()&63 for _ in range(8)]
def bh(st):
 d,side,ca,ep,hm,fm=st;h=0
 for i in range(128):
  z=d[i]
  if z and OB(i):h^=PSQH[z&7][1 if z&8 else 0][s64(i)]
 if side:h^=ZSIDE
 cb=ca;bb=0
 while cb:
  if cb&1:h^=ZCA[bb]
  cb>>=1;bb+=1
 if ep>=0:h^=ZEP[s64(ep)&7]
 return h
TT={};KILL=[[0,0] for _ in range(18)];HIST={};J=0;DEADLINE=float("inf")
def qs(d,st,a,bt):
 global J
 if J>=NB:return ev(d,st[1])
 J+=1;st0=ev(d,st[1])
 if st0>=bt:return bt
 if st0>a:a=st0
 ms=[mv for mv in gm(d,st[1],st[2],st[3]) if d[(mv>>7)&127] or (mv&127) in (5,6)]
 ms.sort(key=lambda mv:-V[d[(mv>>7)&127]&7]*16+V[d[(mv>>14)&127]&7],reverse=True)
 for mv in ms:
  if J>=NB:break
  sqf=(mv>>14)&127;mover=d[sqf]&8
  ci=ap(d,mv,st)
  if chk(d,mover):um(d,mv,ci,st);continue
  x=-qs(d,st,-bt,-a);um(d,mv,ci,st)
  if x>=bt:return bt
  if x>a:a=x
 return a
def _order(ms,d,st,best,ttmv):
 def key(mv):
  score=0
  if mv==ttmv:score+=1000000
  elif mv==best:score+=900000
  f=(mv>>14)&127;t=(mv>>7)&127;cap=d[t]
  if cap:score+=(V[cap&7]*16-V[d[f]&7])*32
  if mv&127 in (5,6):score+=50000
  return score
 return sorted(ms,key=key,reverse=True)
def search(d,st,de):
 global J
 if J>=NB:return ev(d,st[1])
 J+=1
 if de<=0 or st[4]>=100:return qs(d,st,NEG,MATE)
 ms=gm(d,st[1],st[2],st[3]);b=NEG;best=0
 for mv in ms:
  if J>=NB:break
  ci=ap(d,mv,st)
  if chk(d,st[1]^8):um(d,mv,ci,st);continue
  x=-search(d,st,de-1);um(d,mv,ci,st)
  if x>b:b=x;best=mv
  if best==0 and b==NEG:return -MATE if chk(d,st[1]) else 0
 return b
def tk(st,legal):
 global J
 d,side,ca,ep,hm,fm=st
 ms=gm(d,side,ca,ep);lg=[];leg={x for x in legal}
 for mv in ms:
  ci=ap(d,mv,st)
  if chk(d,side):um(d,mv,ci,st);continue
  if _uc(mv) not in leg:um(d,mv,ci,st);continue
  lg.append(mv);um(d,mv,ci,st)
 if not lg:return None
 J=0;best=lg[0]
 for de in range(1,17):
  if J>=NB:break
  a,bt=NEG,MATE;cur=best
  for mv in _order(lg,d,st,best,0):
   if J>=NB:break
   ci=ap(d,mv,st)
   if chk(d,ci[2]):um(d,mv,ci,st);continue
   x=-search(d,st,de-1);um(d,mv,ci,st)
   if x>a:a=x;cur=mv
   if cur is not None:best=cur
 return best
def _uc(mv):
 if mv is None:return"none"
 f=(mv>>14)&127;t=(mv>>7)&127;sp=mv&127
 return "abcdefgh"[f&7]+"12345678"[f>>4]+"abcdefgh"[t&7]+"12345678"[t>>4]+("nbrq"[sp-1] if 1<=sp<=4 else "")
def po(path,body):
 req=urllib.request.Request(H+path,data=json.dumps(body).encode(),headers={"content-type":"application/json"})
 return json.loads(urllib.request.urlopen(req,timeout=8).read().decode())
def main():
 if H is None:sys.exit("MAKEFUN_ENV_URL is not set")
 st=None
 while 1:
  gg=po("/game",{})
  if gg.get("status")=="done":break
  st=pf(gg["fen"])
  while gg.get("status")=="your_move":
   mv=tk(st,set(gg.get("legal_moves") or []))
   if mv is None:
    po("/resign",{"game":gg["game"]});break
   z=_uc(mv);gg=po("/move",{"game":gg["game"],"move":z})
   if gg.get("status")!="over":st=pf(gg["fen"])
 print("done",gg.get("wins"),gg.get("draws"),gg.get("losses"),file=sys.stderr)
if __name__=="__main__":main()
