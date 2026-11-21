import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fig_common import *
import numpy as np
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch

W=4.0
def square_stage(ax, r_over_a, a=1.0):
    ax.set_xlim(0,W); ax.set_ylim(0,W); ax.set_aspect('equal'); ax.axis('off')
    r=r_over_a*a
    pts=[(i*a+a/2,j*a+a/2) for i in range(-1,int(W/a)+1) for j in range(-1,int(W/a)+1)]
    for (x,y) in pts:
        ax.add_patch(Circle((x,y),r,facecolor='#9d9d9d',edgecolor='none'))
    if r>a/2:
        h=np.sqrt(r*r-(a/2)**2)
        for (x,y) in pts:
            ax.plot([x+a/2,x+a/2],[y-h,y+h],color='#5a5a5a',lw=0.6)   # boundary with right neighbour
            ax.plot([x-h,x+h],[y+a/2,y+a/2],color='#5a5a5a',lw=0.6)   # boundary with upper neighbour
    ax.add_patch(Rectangle((0,0),W,W,fill=False,edgecolor=INK,lw=0.7))

def final_stage(ax):
    ax.set_xlim(0,W); ax.set_ylim(0,W); ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Rectangle((0,0),W,W,facecolor='#9d9d9d',edgecolor='none'))
    rng=np.random.default_rng(4)
    g=1.35
    # grain boundaries: a jittered grid of larger grains
    xs=np.arange(-g/2,W+g,g); ys=np.arange(-g/2,W+g,g)
    J={(i,j):(x+rng.normal(0,0.12),y+rng.normal(0,0.12)) for i,x in enumerate(xs) for j,y in enumerate(ys)}
    for (i,j),(x,y) in J.items():
        if (i+1,j) in J: ax.plot([x,J[(i+1,j)][0]],[y,J[(i+1,j)][1]],color='#5a5a5a',lw=0.6)
        if (i,j+1) in J: ax.plot([x,J[(i,j+1)][0]],[y,J[(i,j+1)][1]],color='#5a5a5a',lw=0.6)
        if rng.random()<0.55: ax.add_patch(Circle((x,y),0.075,facecolor='white',edgecolor='none'))
    ax.add_patch(Rectangle((0,0),W,W,fill=False,edgecolor=INK,lw=0.7))

fig=plt.figure(figsize=(6.5,3.05))
pw=0.205; ph=pw*6.5/3.05; y0=0.43; xs0=[0.01,0.265,0.52,0.775]
axs=[fig.add_axes([x,y0,pw,ph]) for x in xs0]
square_stage(axs[0],0.50); square_stage(axs[1],0.56); square_stage(axs[2],0.625); final_stage(axs[3])
titles=['(a) Green body','(b) Initial stage','(c) Intermediate stage','(d) Final stage']
subs=['particles in point contact;\nopen, connected pores','necks grow at the contacts;\npores stay open',
      'pores become narrow\nchannels between grains','pores close and become\nisolated; grains grow']
dens=['relative density ≈ 0.5–0.6','up to ≈ 0.65','≈ 0.65–0.9','above ≈ 0.9']
for x,ax,tt,ss,dd in zip(xs0,axs,titles,subs,dens):
    fig.text(x,y0+ph+0.025,tt,fontsize=8.2,va='bottom')
    fig.text(x,y0-0.025,ss,fontsize=6.9,va='top')
    fig.text(x,y0-0.135,dd,fontsize=6.9,va='top',color=ACCENT)
# usual range for porous membranes: stages (b) and early (c)
fig.patches.append(Rectangle((xs0[1],0.165),xs0[2]+pw*0.6-xs0[1],0.004,transform=fig.transFigure,facecolor=ACCENT2,edgecolor='none'))
fig.text(xs0[1],0.177,'usual firing range for porous membranes',fontsize=6.8,color=ACCENT2,va='bottom')
fig.patches.append(FancyArrowPatch((0.01,0.10),(0.98,0.10),transform=fig.transFigure,arrowstyle='-|>',mutation_scale=10,lw=1.0,color=INK))
fig.text(0.5,0.075,'higher sintering temperature or longer dwell: necks grow, pores shrink and close, density rises',ha='center',va='top',fontsize=7.2)
fig.savefig(os.path.join(HERE, 'fig_sintering_stages.png'),bbox_inches='tight',pad_inches=0.03)
print('ok')
