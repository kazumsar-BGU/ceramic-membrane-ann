import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

# Liberation Sans is metrically identical to Arial, the heading/caption font of the thesis.
for f in font_manager.findSystemFonts():
    if 'Liberation' in f:
        font_manager.fontManager.addfont(f)
plt.rcParams.update({
    'font.family': 'Liberation Sans',
    'font.size': 8.5,
    'axes.titlesize': 9,
    'axes.labelsize': 8.5,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 7.5,
    'axes.linewidth': 0.7,
    'xtick.major.width': 0.7,
    'ytick.major.width': 0.7,
    'savefig.dpi': 300,
    'mathtext.fontset': 'custom',
    'mathtext.rm': 'Liberation Sans',
    'mathtext.it': 'Liberation Sans:italic',
    'mathtext.bf': 'Liberation Sans:bold',
})
INK = '#1a1a1a'
GREY = '#9a9a9a'
LIGHT = '#d9d9d9'
ACCENT = '#2b6cb0'
ACCENT2 = '#c05621'
