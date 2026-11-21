import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fig_common import *
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

fig=plt.figure(figsize=(6.5,3.3))
# ---------------- (a) process route ----------------
ax=fig.add_axes([0,0.47,1,0.53]); ax.set_xlim(0,100); ax.set_ylim(4,40); ax.axis('off')
ax.text(0,39.5,'(a) Fabrication route of a sintered ceramic membrane',fontsize=8.5,va='top')
steps=[('Powder and\nadditives','binder, pore\nformer, water'),
       ('Mixing and\nmilling','slurry or\nmoist mass'),
       ('Forming','dry pressing,\nextrusion, slip or\ntape casting'),
       ('Drying','water removed\nslowly'),
       ('Sintering','heating, dwell\nand cooling'),
       ('Characteri-\nsation','pore size,\nporosity')]
w,h,gap=13.2,11,3.1
x=0.5; centers=[]
for i,(title,sub) in enumerate(steps):
    hl = i in (0,2,4)
    ax.add_patch(FancyBboxPatch((x,21),w,h,boxstyle='round,pad=0.25,rounding_size=1.2',
                 facecolor='#e8eef6' if hl else '#f2f2f2',edgecolor=ACCENT if hl else '#666666',lw=0.8))
    ax.text(x+w/2,21+h-2.6,title,ha='center',va='center',fontsize=7.6,fontweight='bold')
    ax.text(x+w/2,24.6,sub,ha='center',va='center',fontsize=6.4,color='#333333')
    centers.append(x+w/2)
    if i < len(steps)-1:
        ax.add_patch(FancyArrowPatch((x+w+0.4,26.5),(x+w+gap-0.4,26.5),arrowstyle='-|>',mutation_scale=8,lw=0.9,color=INK))
    x+=w+gap
# model inputs under the relevant steps
inp={0:'input: particle size $d$',2:'input: bulk (green) density $\\rho$',4:'inputs: heating rate $r$,\nsintering temperature $T_s$,\ndwell time $t_{dwell}$',5:'output: pore size $D_p$'}
for i,txt in inp.items():
    c=centers[i]
    ax.annotate('',xy=(c,20.2),xytext=(c,15.8),arrowprops=dict(arrowstyle='-',lw=0.6,color=ACCENT if i<5 else ACCENT2))
    ax.text(c,15.2,txt,ha='center',va='top',fontsize=7,color=ACCENT if i<5 else ACCENT2)

# ---------------- (b) firing schedule ----------------
bx=fig.add_axes([0.09,0.05,0.60,0.33])
t=[0,4.2,7.2,12.5]; T=[25,1250,1250,60]
bx.plot(t[:3],T[:3],color=INK,lw=1.4)
tt=np.linspace(7.2,12.5,60); TT=60+(1250-60)*np.exp(-(tt-7.2)/1.9)
bx.plot(tt,TT,color=INK,lw=1.2,ls=(0,(4,2)))
bx.set_xlim(0,12.8); bx.set_ylim(0,1500)
bx.set_xticks([]); bx.set_yticks([25,1250]); bx.set_yticklabels(['room\ntemperature','$T_s$'])
bx.set_xlabel('Time'); bx.set_ylabel('Furnace temperature')
for s in ('top','right'): bx.spines[s].set_visible(False)
bx.annotate('heating rate $r$\n(°C/min)',xy=(2.3,700),xytext=(3.0,330),fontsize=7,
            arrowprops=dict(arrowstyle='-',lw=0.5))
bx.annotate('',xy=(4.2,1365),xytext=(7.2,1365),arrowprops=dict(arrowstyle='<->',lw=0.7))
bx.text(5.7,1400,'dwell time $t_{dwell}$',ha='center',fontsize=7)
bx.text(9.3,820,'cooling',fontsize=7,color='#444444')
fig.text(0.0,0.455,'(b) Firing schedule',fontsize=8.5,va='top')
# side note
fig.text(0.72,0.22,'The model sees the firing only\nthrough $r$, $T_s$ and $t_{dwell}$. The\nsteps before firing enter only\nthrough particle size and, where\nreported, bulk density.',fontsize=7,va='center',color='#333333')
fig.savefig(os.path.join(HERE, 'fig_fabrication_route.png'),bbox_inches='tight',pad_inches=0.03)
print('ok')
