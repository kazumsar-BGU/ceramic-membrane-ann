"""Statistics of the dataset reported in Chapter 2 of the thesis (Table 2 and Section 2.1.5).

Usage:  python dataset_stats.py            (reads ../data/dataset.csv)
"""
import csv
import collections
import os
import numpy as np
from scipy.stats import skew

HERE = os.path.dirname(os.path.abspath(__file__))
COLS = ['sintering_temp_C', 'dwell_time_min', 'particle_size_um', 'bulk_density_g_cm3', 'heating_rate_C_min', 'pore_size_um']
LOG_SCALE = {'dwell_time_min', 'particle_size_um', 'heating_rate_C_min', 'pore_size_um'}   # log(1 + x) in the models


def load():
    with open(os.path.join(HERE, '..', 'data', 'dataset.csv'), encoding='utf8') as f:
        return [{k: (float(v) if v != '' else None) for k, v in r.items()} for r in csv.DictReader(f)]


def scaled_var(x):
    x = np.asarray(x, float)
    s = (x - x.min()) / (x.max() - x.min())
    return s.var(ddof=1)


rows = load()
print('Table 2: missing values, distinct values, skewness, scaled variance (model scale)')
for c in COLS:
    vals = np.array([r[c] for r in rows if r[c] is not None])
    f = np.log1p if c in LOG_SCALE else (lambda v: v)
    imputed = np.array([r[c] if r[c] is not None else vals.mean() for r in rows])
    print('%-20s reported %2d  missing %2d (%4.1f %%)  distinct %2d  skew %.2f / %.2f  scaled var %.3f / %.3f' % (
        c, len(vals), len(rows) - len(vals), 100 * (len(rows) - len(vals)) / len(rows), len(set(vals)),
        skew(vals, bias=False), skew(f(vals), bias=False), scaled_var(f(vals)), scaled_var(f(imputed))))

# error floor: best possible predictor of the five inputs = group mean of rows with identical inputs
key = lambda r: tuple(r[c] for c in COLS[:5])
groups = collections.defaultdict(list)
for r in rows:
    groups[key(r)].append(r['pore_size_um'])
y = np.array([r['pore_size_um'] for r in rows])
p = np.array([np.mean(groups[key(r)]) for r in rows])
print('\nDistinct input combinations:', len(groups))
print('Error floor over all rows: MAE %.2f  RMSE %.2f  R2 %.3f' % (
    np.abs(y - p).mean(), np.sqrt(((y - p) ** 2).mean()), 1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum()))
shared = [i for i, r in enumerate(rows) if len(groups[key(r)]) > 1]
print('Error floor over the %d rows that share inputs: MAE %.2f  RMSE %.2f' % (
    len(shared), np.abs(y[shared] - p[shared]).mean(), np.sqrt(((y[shared] - p[shared]) ** 2).mean())))

# reference point for out-of-sample R2 (Section 2.5.1): under leave-one-paper-out, predict for every held-out paper
# the mean pore size of the other 17 papers. Out of sample, R2 can be negative; this constant prediction scores below 0.
pid = np.array([r['paper_id_code'] for r in rows])
naive = np.array([y[pid != pid[i]].mean() for i in range(len(y))])
print('\nLOPO, constant prediction = mean of the other papers: R2 %.3f' % (
    1 - ((y - naive) ** 2).sum() / ((y - y.mean()) ** 2).sum()))
