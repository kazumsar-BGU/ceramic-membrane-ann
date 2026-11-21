import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fig_common import *
import numpy as np
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
from mpl_toolkits.mplot3d import Axes3D  # noqa

fig=plt.figure(figsize=(6.5,2.9))
ax=fig.add_axes([0.0,0.02,0.48,0.92],projection='3d')
# cube edges
r=[-1,1]
for s in r:
    for t in r:
        ax.plot([-1,1],[s,s],[t,t],color='#b0b0b0',lw=0.6)
        ax.plot([s,s],[-1,1],[t,t],color='#b0b0b0',lw=0.6)
        ax.plot([s,s],[t,t],[-1,1],color='#b0b0b0',lw=0.6)
pts=[(-1,-1,0),(1,-1,0),(-1,1,0),(1,1,0),(-1,0,-1),(1,0,-1),(-1,0,1),(1,0,1),(0,-1,-1),(0,1,-1),(0,-1,1),(0,1,1)]
P=np.array(pts)
ax.scatter(P[:,0],P[:,1],P[:,2],s=26,color=ACCENT,depthshade=False,edgecolor='white',linewidth=0.5)
ax.scatter([0],[0],[0],s=60,color=ACCENT2,depthshade=False,edgecolor='white',linewidth=0.5)
ax.text(0.12,0.12,0.18,'centre ×3',fontsize=7,color=ACCENT2)
ax.set_xticks([-1,0,1]); ax.set_xticklabels(['1200','1350','1500'],fontsize=6.5)
ax.set_yticks([-1,0,1]); ax.set_yticklabels(['30','120','480'],fontsize=6.5)
ax.set_zticks([-1,0,1]); ax.set_zticklabels(['2.5','5','10'],fontsize=6.5)
ax.set_xlabel('$T_s$ (°C)',fontsize=7.5,labelpad=-4)
ax.set_ylabel('$t_{dwell}$ (min)',fontsize=7.5,labelpad=-4)
ax.set_zlabel('$r$ (°C/min)',fontsize=7.5,labelpad=-6)
ax.tick_params(pad=-3)
for a in (ax.xaxis,ax.yaxis,ax.zaxis):
    a.pane.set_facecolor('white'); a.pane.set_edgecolor('#dddddd')
ax.view_init(elev=18,azim=-58); ax.grid(False)
fig.text(0.01,0.95,'(a) 15 furnace firings (Box–Behnken)',fontsize=8.5,va='top')

bx=fig.add_axes([0.52,0.04,0.48,0.86]); bx.set_xlim(-0.6,10); bx.set_ylim(0,7.2); bx.set_aspect('equal'); bx.axis('off')
fig.text(0.53,0.95,'(b) Discs fired together in one firing',fontsize=8.5,va='top')
bx.add_patch(FancyBboxPatch((0.5,0.4),9.2,5.7,boxstyle='round,pad=0.1,rounding_size=0.3',facecolor='#f4f4f4',edgecolor='#666666',lw=0.8))
bx.text(4.9,5.75,'furnace setter (one firing = one whole plot)',ha='center',fontsize=7,color='#444444')
grades=[('fine','0.5 µm','#d9d9d9'),('medium','3 µm','#a6a6a6'),('coarse','10 µm','#6e6e6e')]
xs=[2.2,5.1,8.0]
for x,(g,d,c) in zip(xs,grades):
    for y,lab in [(4.2,'50 MPa'),(2.2,'150 MPa')]:
        bx.add_patch(Circle((x,y),0.75,facecolor=c,edgecolor=INK,lw=0.6))
    bx.text(x,0.95,'%s powder\n$d_{50}$ ≈ %s'%(g,d),ha='center',fontsize=6.6,va='center')
bx.text(-0.45,4.2,'50\nMPa',fontsize=6.3,va='center')
bx.text(-0.45,2.2,'150\nMPa',fontsize=6.3,va='center')
# random repeat
bx.add_patch(Circle((8.95,5.15),0.42,facecolor='white',edgecolor=ACCENT2,lw=1.0,ls=(0,(2,1))))
bx.text(8.95,5.15,'R',ha='center',va='center',fontsize=7,color=ACCENT2,fontweight='bold')
bx.text(9.5,6.55,'random repeat of\none combination',ha='right',fontsize=6.4,color=ACCENT2)
fig.savefig(os.path.join(HERE, 'fig_design.png'),bbox_inches='tight',pad_inches=0.04)
print('ok')
