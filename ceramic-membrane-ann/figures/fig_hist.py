import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fig_common import *
import numpy as np
import csv
with open(os.path.join(HERE, '..', 'data', 'dataset.csv'), encoding='utf8') as fh:
    y=np.array([float(r['pore_size_um']) for r in csv.DictReader(fh)])
med=np.median(y)
fig,(a1,a2)=plt.subplots(1,2,figsize=(6.5,2.55),gridspec_kw={'wspace':0.28})
bins=np.arange(0,52,2)
a1.hist(y,bins=bins,color=ACCENT,edgecolor='white',linewidth=0.6)
a1.axvline(med,color=INK,ls='--',lw=0.9)
a1.text(med+1.2,a1.get_ylim()[1]*0.92 if False else 37,f'median {med:.2f} µm',fontsize=7.5,va='top')
a1.set_xlabel('Pore size (µm)')
a1.set_ylabel('Number of observations')
a1.set_xlim(0,50)
a1.set_title('(a) Linear scale',loc='left',fontsize=8.5)
lb=np.arange(-3,2.01,0.25)
a2.hist(np.log10(y),bins=lb,color=ACCENT,edgecolor='white',linewidth=0.6)
a2.axvline(np.log10(med),color=INK,ls='--',lw=0.9)
a2.set_xticks([-3,-2,-1,0,1,2])
a2.set_xticklabels(['0.001','0.01','0.1','1','10','100'])
a2.set_xlabel('Pore size (µm), logarithmic axis')
a2.set_ylabel('Number of observations')
a2.set_title('(b) Logarithmic scale',loc='left',fontsize=8.5)
for a in (a1,a2):
    a.spines['top'].set_visible(False); a.spines['right'].set_visible(False)
# fix y limits after drawing
a1.set_ylim(0,40); a1.texts[0].set_position((med+1.2,38))
fig.savefig(os.path.join(HERE, 'fig_target_histogram.png'),bbox_inches='tight',pad_inches=0.03)
