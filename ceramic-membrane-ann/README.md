# Fabrication–pore size trends in ceramic membranes: data and code

Data and code for the M.Sc. thesis *Fabrication-Pore Size Trends in Ceramic Membranes: An Artificial Neural Network
Feasibility Study* (Omer Kazum Sarid, Department of Mechanical Engineering, Ben-Gurion University of the Negev, 2026;
supervisor Prof. Vitaly Gitis). Table, figure and section numbers below refer to the revised thesis.

## Contents

| Path | Contents |
|---|---|
| `data/dataset.csv` | The 78 rows of Table 3: sintering temperature (°C), dwell time (min), initial particle size (µm), bulk density (g/cm³), heating rate (°C/min) and final pore size (µm). Empty cells are values not reported in the source paper (NR). `paper_id_code` is the paper id used inside the code; `ref_thesis` is the reference number in the revised thesis (`paper_id_code + 3`). |
| `data/references.csv` | The 18 source papers, with the number of rows each contributes. |
| `app/index.html` | The evaluation harness and prediction interface (Tables 5 and 7, Figures 9 and 10). |
| `analysis/run_headless.js` | Runs the harness of `app/index.html` in Node.js with `Math.random` seeded. Variant `orig` uses all five inputs; `nobd` leaves out bulk density (Table 8). |
| `analysis/results/` | Output and logs of the two seeded runs reported in Sections 4.1.1 and 4.3.3 (seed 1). |
| `analysis/dataset_stats.py` | The statistics of Table 2 and the error floor of Section 2.1.5. |
| `figures/` | Scripts and images for Figures 1, 2, 3, 7 and 11. |

## Reproducing the results

**In a browser.** Open `app/index.html` and press *Run Full Evaluation*. The page loads TensorFlow.js 4.10.0, Chart.js
and Tailwind from public CDNs, so it needs an internet connection. A full run takes between half an hour and an hour on
a laptop without a GPU.

**In Node.js** (version 18 or later):

```bash
cd analysis
npm install
npm run orig    # all five inputs   -> results/full_orig_s1.json
npm run nobd    # no bulk density   -> results/full_nobd_s1.json
```

Each run took about 38 minutes on one CPU core. `node run_headless.js <orig|nobd> <seed> <output.json>` runs other
seeds. Setting the environment variable `SMOKE=1` gives a run of under a minute with a tiny ANN budget, which is only
useful for checking that the script works.

**Python scripts** (numpy, scipy, matplotlib):

```bash
python analysis/dataset_stats.py
python figures/fig_hist.py          # and fig_membrane.py, fig_sinter.py, fig_process.py, fig_design.py
```

## Reproducibility notes

* The four comparison models (linear regression, ridge regression, random forest, gradient boosting) are deterministic.
  The run with all five inputs reproduces their entries in Table 7 exactly.
* The ANN depends on the order of the mini-batches, which TensorFlow.js draws from `Math.random`. The browser page does
  not seed it, so the ANN results change from one browser run to the next (Section 4.1.1). The Node.js runner replaces
  `Math.random` with a seeded generator (mulberry32), so a runner result can be repeated exactly.
* The runner uses the TensorFlow.js CPU backend, while a browser normally uses WebGL. Seeded browser runs would therefore
  still not match the runner to the last digit.
* The ANN values in Table 7 come from an earlier, unseeded browser run and cannot be reproduced exactly; the seeded
  re-run is given in Section 4.1.1.

## Licence

No licence has been chosen yet. Add one before the repository is made public (for example MIT for the code and
CC BY 4.0 for the data table). The data values are taken from the publications listed in `data/references.csv`.
