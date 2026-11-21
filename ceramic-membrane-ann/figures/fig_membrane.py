import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fig_common import *
import numpy as np
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch
rng=np.random.default_rng(7)

def packed_layer(ax, x0, x1, y0, y1, r, color, jitter=0.10, edge='white'):
    clip=Rectangle((x0,y0),x1-x0,y1-y0,facecolor='none',edgecolor='none')
    ax.add_patch(clip)
    dx=2*r*1.03; dy=np.sqrt(3)*r*1.03
    row=0; y=y0+r*0.9
    while y < y1+r:
        off = 0 if row%2==0 else dx/2
        x=x0+off-r
        while x < x1+r:
            c=Circle((x+rng.normal(0,jitter*r), y+rng.normal(0,jitter*r)), r*rng.uniform(0.86,0.98),
                     facecolor=color, edgecolor=edge, linewidth=0.3)
            ax.add_patch(c); c.set_clip_path(clip)
            x+=dx
        y+=dy; row+=1
    ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,fill=False,edgecolor=INK,linewidth=0.7))

fig=plt.figure(figsize=(6.5,3.4))
# ---------- (a) asymmetric porous membrane ----------
ax=fig.add_axes([0.0,0.0,0.46,0.94]); ax.set_xlim(0,10); ax.set_ylim(-0.8,10.6); ax.axis('off')
ax.text(0.0,10.5,'(a) Porous asymmetric ceramic membrane',fontsize=8.5,va='top')
X0,X1=0.2,5.0
packed_layer(ax,X0,X1,0.3,5.6,0.50,'#8c8c8c')
packed_layer(ax,X0,X1,5.6,7.3,0.19,'#b5b5b5')
packed_layer(ax,X0,X1,7.3,7.9,0.065,'#d4d4d4',jitter=0.04,edge='#f4f4f4')
for xx in np.linspace(X0+0.4,X1-0.4,7):
    ax.add_patch(Circle((xx,8.2),0.2,facecolor=ACCENT2,edgecolor='none'))
ax.add_patch(FancyArrowPatch((2.6,10.0),(2.6,8.6),arrowstyle='-|>',mutation_scale=9,lw=1.0,color=INK))
ax.text(2.8,9.45,'feed',fontsize=7.5)
ax.text(X1+0.25,8.25,'retained particles',fontsize=7.2,color=ACCENT2,va='center')
ax.add_patch(FancyArrowPatch((2.6,0.2),(2.6,-0.75),arrowstyle='-|>',mutation_scale=9,lw=1.0,color=INK))
ax.text(2.8,-0.45,'permeate',fontsize=7.5)
def bracket(y0,y1,txt,sub):
    xb=X1+0.15
    ax.plot([xb,xb+0.15,xb+0.15,xb],[y0,y0,y1,y1],color=INK,lw=0.6)
    ax.text(xb+0.4,(y0+y1)/2+0.28,txt,fontsize=7.5,va='center')
    ax.text(xb+0.4,(y0+y1)/2-0.30,sub,fontsize=6.8,va='center',color='#444444')
bracket(7.3,7.9,'separating layer','pores below 0.1 µm')
bracket(5.6,7.3,'intermediate layer','pores 0.1–1 µm')
bracket(0.3,5.6,'macroporous support','pores of several µm')

# ---------- (b) quantities describing the pore structure ----------
bx=fig.add_axes([0.49,0.44,0.51,0.50]); bx.set_xlim(0,10); bx.set_ylim(0,6.3); bx.axis('off')
bx.text(0.0,6.25,'(b) Quantities that describe the pore structure',fontsize=8.5,va='top')
B0,B1,BY0,BY1=0.9,6.3,0.5,5.1
bx.add_patch(Rectangle((B0,BY0),B1-B0,BY1-BY0,facecolor='#bdbdbd',edgecolor=INK,lw=0.7))
t=np.linspace(0,1,300)
xs=2.0+1.0*np.sin(2.4*np.pi*t)+1.2*t
ys=BY1-(BY1-BY0)*t
bx.plot(xs,ys,color='white',lw=8,solid_capstyle='butt')
i0,i1=140,160                     # pore throat (constriction)
bx.plot(xs[i0:i1],ys[i0:i1],color='#bdbdbd',lw=8,solid_capstyle='butt')
bx.plot(xs[i0:i1],ys[i0:i1],color='white',lw=2.6,solid_capstyle='butt')
j=80                              # interconnected branch from the main pore
bx.plot([xs[j],4.9,5.5],[ys[j],2.3,BY0],color='white',lw=6,solid_capstyle='butt')
bx.plot([5.7,5.0],[BY1+0.02,4.55],color='white',lw=6,solid_capstyle='round')   # dead-end pore open to the feed side
bx.add_patch(Circle((1.55,1.25),0.28,facecolor='white',edgecolor='none'))   # closed pore
bx.plot(xs,ys,color=ACCENT,lw=0.9,ls=(0,(3,1.5)))
bx.plot([0.55,0.55],[BY0,BY1],color=INK,lw=0.7)
bx.plot([0.45,0.65],[BY0,BY0],color=INK,lw=0.7); bx.plot([0.45,0.65],[BY1,BY1],color=INK,lw=0.7)
bx.text(0.38,(BY0+BY1)/2,'$L$',fontsize=8,ha='right',va='center')
def lab(x,y,tx,ty,txt):
    bx.annotate(txt,xy=(x,y),xytext=(tx,ty),fontsize=7,va='center',
                arrowprops=dict(arrowstyle='-',lw=0.5,color='#333333',shrinkA=1,shrinkB=1))
lab(5.05,4.62,6.75,5.15,'dead-end pore')
lab(xs[40],ys[40],6.75,4.2,'tortuous path:\n$\\tau$ = path length / $L$')
lab(xs[150],ys[150],6.75,3.0,'pore throat: the narrowest\nsection, which sets $D_p$')
lab(5.1,1.9,6.75,1.75,'interconnected pores')
lab(1.55,1.25,6.75,0.7,'closed pore (not part of\nthe open porosity $\\varepsilon$)')

# ---------- (c) dense membrane ----------
cx=fig.add_axes([0.49,0.0,0.51,0.37]); cx.set_xlim(0,10); cx.set_ylim(0,4.2); cx.axis('off')
cx.text(0.0,4.15,'(c) Dense membrane, for comparison',fontsize=8.5,va='top')
cx.add_patch(Rectangle((0.9,0.9),5.4,1.6,facecolor='#9e9e9e',edgecolor=INK,lw=0.7))
for xx in [1.7,3.0,4.3,5.6]:
    cx.add_patch(Circle((xx,2.95),0.14,facecolor=ACCENT,edgecolor='none'))
    cx.add_patch(FancyArrowPatch((xx,2.75),(xx+0.3,0.72),arrowstyle='-|>',mutation_scale=6,lw=0.7,color=ACCENT,
                                 connectionstyle='arc3,rad=0.25'))
cx.text(6.75,2.6,'no continuous pores: species\ndissolve in the solid, diffuse\nacross it and leave on the\npermeate side',fontsize=7,va='top')
fig.savefig(os.path.join(HERE, 'fig_membrane_structure.png'),bbox_inches='tight',pad_inches=0.03)
print('ok')
