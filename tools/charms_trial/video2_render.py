import subprocess,numpy as np,json,sys,math
from PIL import Image,ImageDraw,ImageFont,ImageFilter
src,out,boxf=sys.argv[1:4]
W,H=928,1696; FPS=30; K=2
res=json.load(open(boxf)); n=len(res)
arr=np.array([r if r else [np.nan]*4 for r in res],float)
l,r,a,bb=arr.T
w=r-l; cx=(l+r)/2; ytop=a*cx+bb
def fix(v):
    i=np.arange(n);ok=~np.isnan(v);v=np.interp(i,i[ok],v[ok])
    m=np.array([np.median(v[max(0,k-4):k+5]) for k in range(n)])
    s=m.copy()
    for k in range(1,n): s[k]=s[k-1]*0.6+m[k]*0.4
    return s
w,cx,ytop,a=map(fix,(w,cx,ytop,a))
F=lambda p,s:ImageFont.truetype(p,s)
SB='/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'
GOLD=(196,152,58); CHOC=(70,40,24)
def card():
    cw,ch=1000,540
    im=Image.new('RGBA',(cw,ch),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,cw-1,ch-1],26,fill=(252,249,241,255))
    d.rounded_rectangle([14,14,cw-15,ch-15],18,outline=GOLD,width=5)
    c=cw/2
    d.text((c,120),"SET ASAS PERCUBAAN",font=F(SB,76),fill=CHOC,anchor='mm')
    d.text((c,222),"(TRIAL)",font=F(SB,64),fill=CHOC,anchor='mm')
    d.line([c-230,300,c-40,300],fill=GOLD,width=5); d.line([c+40,300,c+230,300],fill=GOLD,width=5)
    d.regular_polygon((c,300,14),4,fill=GOLD)
    d.text((c,400),"C H A R M S",font=F(SB,88),fill=GOLD,anchor='mm',stroke_width=2,stroke_fill=(150,110,40))
    return im
C=card()
def banner(scale=.85):
    l1="SET ASAS PERCUBAAN (TRIAL)"; l2="C H A R M S"
    f1=F(SB,50); f2=F(SB,64)
    d=ImageDraw.Draw(Image.new('RGBA',(10,10)))
    bw=int(max(d.textlength(l1,font=f1),d.textlength(l2,font=f2))+90); bh=184
    im=Image.new('RGBA',(bw+40,bh+40),(0,0,0,0))
    sh=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([20,26,20+bw,26+bh],28,fill=(0,0,0,120))
    im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(10))); d=ImageDraw.Draw(im)
    d.rounded_rectangle([20,20,20+bw,20+bh],28,fill=(58,34,22,240),outline=(214,176,84,255),width=5)
    d.rounded_rectangle([31,31,9+bw,9+bh],20,outline=(214,176,84,140),width=2)
    x=20+bw/2
    d.text((x,66),l1,font=f1,fill=(250,238,212),anchor='mm')
    d.line([x-150,112,x-40,112],fill=(214,176,84),width=3); d.line([x+40,112,x+150,112],fill=(214,176,84),width=3)
    d.regular_polygon((x,112,8),4,fill=(214,176,84))
    d.text((x,160),l2,font=f2,fill=(232,192,98),anchor='mm',stroke_width=1,stroke_fill=(150,110,40))
    return im.resize((int(im.width*scale),int(im.height*scale)),Image.LANCZOS)
B=banner()
def pill(scale=.85):
    f1=F(SB,52); f2=F(SB,64); l1="PAKEJ LENGKAP"; l2="RUTIN PAGI & MALAM"
    im=Image.new('RGBA',(900,200),(0,0,0,0))
    sh=Image.new('RGBA',im.size,(0,0,0,0)); ds=ImageDraw.Draw(sh)
    for (y,t,f) in ((60,l1,f1),(135,l2,f2)): ds.text((450,y+4),t,font=f,fill=(0,0,0,200),anchor='mm',stroke_width=8,stroke_fill=(0,0,0,200))
    im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(6))); d=ImageDraw.Draw(im)
    for (y,t,f) in ((60,l1,f1),(135,l2,f2)): d.text((450,y),t,font=f,fill=(255,214,40),anchor='mm',stroke_width=5,stroke_fill=(58,34,22))
    return im.resize((int(im.width*scale),int(im.height*scale)),Image.LANCZOS)
P=pill()
def ease(x): x=min(max(x,0),1); return 1-(1-x)**3
def popped(img,t):
    s=0.6+0.4*ease(t/10)
    if s>=1: return img
    o=img.resize((max(1,int(img.width*s)),max(1,int(img.height*s))),Image.LANCZOS)
    o.putalpha(o.getchannel('A').point(lambda v:int(v*min(1,t/6)))); return o
dec=subprocess.Popen(['ffmpeg','-v','error','-i',src,'-vf',f'scale={W}:{H}:flags=lanczos','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',out],stdin=subprocess.PIPE)
i=0
while True:
    b=dec.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    fr=Image.frombuffer('RGB',(W,H),b).convert('RGBA')
    if i<n:
        bw_=w[i]*K; cw=0.88*bw_; ch=cw*C.height/C.width
        im=C.resize((int(cw),int(ch)),Image.LANCZOS)
        ang=math.degrees(math.atan(a[i]))
        im=im.rotate(-ang,resample=Image.BICUBIC,expand=True)
        # soft shadow-less; position: card top a little below box top edge
        x0=cx[i]*K; y0=ytop[i]*K+0.025*bw_+ch/2
        im=popped(im,i)
        fr.alpha_composite(im,(int(x0-im.width/2),int(y0-im.height/2)))
    else:
        j=i-n; bi=popped(B,j)
        fr.alpha_composite(bi,(int(W/2-bi.width/2),int(50+B.height/2-bi.height/2)))
        if j>=8:
            pi=popped(P,j-8); fr.alpha_composite(pi,(int(W/2-pi.width/2),int(50+B.height+6+P.height/2-pi.height/2)))
    enc.stdin.write(fr.convert('RGB').tobytes()); i+=1
enc.stdin.close(); enc.wait(); print('frames',i)
