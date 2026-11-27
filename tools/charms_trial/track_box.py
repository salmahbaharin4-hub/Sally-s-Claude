import subprocess,numpy as np,sys,json
W,H=464,848
src=sys.argv[1]
p=subprocess.Popen(['ffmpeg','-v','error','-i',src,'-t','15','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
res=[]
while True:
    b=p.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    f=np.frombuffer(b,np.uint8).reshape(H,W,3).astype(int)
    mn=f.min(2);mx=f.max(2)
    m=(mn>170)&((mx-mn)<40)
    m[:int(.33*H)]=False
    frac=m[:,20:W-20].mean(1)
    top=None
    for y in range(int(.33*H),int(.75*H)):
        if frac[y:y+3].min()>.3: top=y;break
    if top is None: res.append(None);continue
    band=m[top+15:top+70]
    cf=band.mean(0)
    cols=np.where(cf>.6)[0]
    l,r=int(cols.min()),int(cols.max())
    # top edge per column
    xs=np.arange(l+int(.1*(r-l)),r-int(.1*(r-l)),4); ys=[]
    for x in xs:
        c=m[top-60:top+60,x]
        # first run of 4 white
        k=None
        for yy in range(len(c)-4):
            if c[yy:yy+4].all(): k=yy;break
        ys.append(np.nan if k is None else top-60+k)
    ys=np.array(ys,float); ok=~np.isnan(ys)
    if ok.sum()>5:
        a,bb=np.polyfit(xs[ok],ys[ok],1)
        # robust: refit on inliers
        e=np.abs(ys[ok]-(a*xs[ok]+bb)); inl=e<np.percentile(e,70)+2
        a,bb=np.polyfit(xs[ok][inl],ys[ok][inl],1)
    else: a,bb=0,top
    res.append([l,r,float(a),float(bb)])
json.dump(res,open(sys.argv[2],'w'))
for i in range(0,len(res),30): print(i,res[i])
