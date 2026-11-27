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
def thumb():
    src=Image.open('gambar_produk.jpg').convert('RGB')
    tw=int(W*0.22); th=int(tw*src.height/src.width)
    src=src.resize((tw,th),Image.LANCZOS)
    pad=24; im=Image.new('RGBA',(tw+2*pad,th+2*pad),(0,0,0,0))
    sh=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([pad,pad+8,pad+tw,pad+th+8],26,fill=(0,0,0,150))
    im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(10)))
    m=Image.new('L',(tw,th),0); ImageDraw.Draw(m).rounded_rectangle([0,0,tw-1,th-1],24,fill=255)
    ph=src.convert('RGBA'); ph.putalpha(m); im.alpha_composite(ph,(pad,pad))
    ImageDraw.Draw(im).rounded_rectangle([pad,pad,pad+tw,pad+th],24,outline=(214,176,84),width=6)
    return im
TH=thumb()
def subline():
    im=Image.new('RGBA',(1000,130),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.text((500,65),"Set lengkap rutin pagi & malam",font=F(SB,72),fill=CHOC,anchor='mm',stroke_width=3,stroke_fill=(255,246,214))
    return im
SUB=subline()
SR='/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'
def items(f):
    # f = frames since panel start; items slide in from right one by one
    cw,ch=1000,300
    im=Image.new('RGBA',(cw,ch),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,cw-1,ch-1],24,fill=(255,243,190,245),outline=GOLD,width=4)
    d.text((cw/2,58),"Ada 4 item:",font=F(SR,62),fill=CHOC,anchor='mm')
    it=["1. Cleanser","2. Toner","3. Krim Siang","4. Krim Malam"]
    pos=[(60,145),(560,145),(60,235),(560,235)]
    for j in range(4):
        st=10+j*14; p=ease((f-st)/10)
        if p<=0: continue
        layer=Image.new('RGBA',(cw,ch),(0,0,0,0)); dl=ImageDraw.Draw(layer)
        x=pos[j][0]+(1-p)*420
        dl.text((x,pos[j][1]),it[j],font=F(SR,60),fill=CHOC+(int(255*min(1,p*1.5)),),anchor='lm')
        mask=Image.new('L',(cw,ch),0); ImageDraw.Draw(mask).rounded_rectangle([6,6,cw-7,ch-7],20,fill=255)
        layer.putalpha(Image.fromarray(np.minimum(np.array(layer.getchannel('A')),np.array(mask))))
        im=Image.alpha_composite(im,layer)
    return im
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
    f1=F(SB,46); f2=F(SB,58); l1="PAKEJ LENGKAP"; l2="RUTIN PAGI & MALAM"
    d=ImageDraw.Draw(Image.new('RGBA',(10,10)))
    pw=int(max(d.textlength(l1,font=f1),d.textlength(l2,font=f2))+80); ph=150
    im=Image.new('RGBA',(pw+40,ph+40),(0,0,0,0))
    sh=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([20,26,20+pw,26+ph],30,fill=(0,0,0,110))
    im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(10))); d=ImageDraw.Draw(im)
    d.rounded_rectangle([20,20,20+pw,20+ph],30,fill=(255,210,20,250),outline=(58,34,22,255),width=5)
    x=20+pw/2
    d.text((x,62),l1,font=f1,fill=(58,34,22),anchor='mm'); d.text((x,122),l2,font=f2,fill=(58,34,22),anchor='mm')
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
        sf=i-60
        if sf>=0:
            sw=0.62*bw_; shh=sw*SUB.height/SUB.width
            si=SUB.resize((int(sw),int(shh)),Image.LANCZOS)
            sp=ease(sf/12); si.putalpha(si.getchannel('A').point(lambda v:int(v*sp)))
            si=si.rotate(-ang,resample=Image.BICUBIC,expand=True)
            sy=ytop[i]*K+0.025*bw_+ch+0.065*bw_+(1-sp)*20+0.10*bw_*a[i]
            sx=x0+(sy-y0)*0  
            fr.alpha_composite(si,(int(x0+0.10*bw_*math.cos(math.atan(a[i]))-si.width/2),int(sy-si.height/2)))
        t0=30
        if i>=t0:
            f=i-t0
            def ftext(txt,cx_,cy_,size,col,p,fromx):
                if p<=0: return
                fnt=F(SR,size)
                lay=Image.new('RGBA',(W,200),(0,0,0,0))
                sh=Image.new('RGBA',(W,200),(0,0,0,0))
                xx=cx_+fromx*(1-p)
                ImageDraw.Draw(sh).text((xx,104),txt,font=fnt,fill=(0,0,0,190),anchor='mm',stroke_width=7,stroke_fill=(0,0,0,190))
                lay=Image.alpha_composite(lay,sh.filter(ImageFilter.GaussianBlur(5)))
                ImageDraw.Draw(lay).text((xx,100),txt,font=fnt,fill=col,anchor='mm',stroke_width=4,stroke_fill=(58,34,22))
                lay.putalpha(lay.getchannel('A').point(lambda v:int(v*min(1,p*1.5))))
                fr.alpha_composite(lay,(0,int(cy_-100)))
            ftext("Ada 4 item:",W/2,125,60,(255,214,40),ease(f/12),-500)
            it=["1. Cleanser","2. Toner","3. Krim Siang","4. Krim Malam"]
            pos=[(W*0.28,197),(W*0.72,197),(W*0.28,263),(W*0.72,263)]
            for j in range(4):
                ftext(it[j],pos[j][0],pos[j][1],52,(255,250,240),ease((f-10-j*14)/10),500)
    else:
        break
        j=i-n; bi=popped(B,j)
        fr.alpha_composite(bi,(int(W/2-bi.width/2),int(50+B.height/2-bi.height/2)))
        if j>=8:
            pi=popped(P,j-8); fr.alpha_composite(pi,(int(W/2-pi.width/2),int(50+B.height+6+P.height/2-pi.height/2)))
    if i<n:
        tf=i-45
        if tf>=0:
            ti=popped(TH,tf)
            bob=6*math.sin(i/30*2*math.pi/2.5)
            cxT=24+TH.width/2-6; cyT=int(H*0.955)-TH.height/2+bob
            fr.alpha_composite(ti,(int(cxT-ti.width/2),int(cyT-ti.height/2)))
    enc.stdin.write(fr.convert('RGB').tobytes()); i+=1
enc.stdin.close(); enc.wait(); print('frames',i)
