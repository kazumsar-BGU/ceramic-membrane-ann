// Runs the thesis evaluation harness (Appendix A) headless in Node.
// Usage: node runner.js <variant: orig|nobd> <mathRandomSeed> <out.json>
'use strict';
const fs = require('fs');
const vm = require('vm');
const path = require('path');
const tf = require('@tensorflow/tfjs');

const variant = process.argv[2] || 'orig';
const mathSeed = parseInt(process.argv[3] || '1', 10);
const outPath = process.argv[4] || `result_${variant}_${mathSeed}.json`;

// Seed Math.random so that the mini-batch order inside tf.LayersModel.fit
// (which calls Math.random) is reproducible for this run.
function mulberry32(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
Math.random = mulberry32(mathSeed);

// ---- minimal DOM stubs -------------------------------------------------
function makeEl(id) {
  const el = {
    id, innerText: '', innerHTML: '', value: '', disabled: false, children: [],
    _handlers: {},
    classList: { add() {}, remove() {} },
    addEventListener(type, fn) { this._handlers[type] = fn; },
    appendChild(c) { this.children.push(c); },
    set onchange(fn) { this._onchange = fn; },
  };
  return el;
}
const elements = {};
const document = {
  getElementById(id) { if (!elements[id]) elements[id] = makeEl(id); return elements[id]; },
  createElement(tag) { return makeEl(tag); },
};
class Chart { constructor() {} destroy() {} }

const html = fs.readFileSync(path.join(__dirname, '..', 'app', 'index.html'), 'utf8');
const inline = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
let js = inline[inline.length - 1];

function mustReplace(src, a, b) {
  if (!src.includes(a)) throw new Error('patch target not found: ' + a.slice(0, 80));
  return src.split(a).join(b);
}

// expose results
js = mustReplace(js, 'highlightBest(ui.cvResultsBody, cvResults, false);',
  'globalThis.__cv = cvResults; globalThis.__annPooled = annCVPooled;');
js = mustReplace(js, 'highlightBest(ui.lopoResultsBody, lopoResults, true);',
  'globalThis.__lopo = lopoResults;');
js = mustReplace(js, 'renderProtocol(cvResults, finalCfgLabel);',
  'globalThis.__finalCfg = finalCfgLabel; globalThis.__imp = importanceByModel; renderProtocol(cvResults, finalCfgLabel);');

if (variant === 'nobd') {
  js = mustReplace(js,
    "const FEATURE_KEYS = ['sinteringTemp', 'dwellTime', 'particleSize', 'bulkDensity', 'heatingRate'];",
    "const FEATURE_KEYS = ['sinteringTemp', 'dwellTime', 'particleSize', 'heatingRate'];");
  js = mustReplace(js,
    "const featureNames = ['Sintering Temp', 'Dwell Time', 'Particle Size', 'Bulk Density', 'Heating Rate'];",
    "const featureNames = ['Sintering Temp', 'Dwell Time', 'Particle Size', 'Heating Rate'];");
  js = mustReplace(js,
    "return [f.sinteringTemp, Math.log1p(f.dwellTime), Math.log1p(f.particleSize), f.bulkDensity, Math.log1p(f.heatingRate)];",
    "return [f.sinteringTemp, Math.log1p(f.dwellTime), Math.log1p(f.particleSize), Math.log1p(f.heatingRate)];");
  js = mustReplace(js, '            t, lt, lp, ld, lr,\n', '            t, lt, lp, lr,\n');
  js = mustReplace(js,
    '? [[0, 5, 6, 8, 9], [1, 5, 7], [2, 6, 8], [3], [4, 7]]\n        : [[0], [1], [2], [3], [4]];',
    '? [[0, 4, 5, 7, 8], [1, 4, 6], [2, 5, 7], [3, 6]]\n        : [[0], [1], [2], [3]];');
}

if (process.env.SMOKE) {
  js = mustReplace(js, 'const BUDGET = { selEnsemble: 2, selEpochs: 150, refitEnsemble: 12, refitEpochs: 300 };',
    'const BUDGET = { selEnsemble: 1, selEpochs: 2, refitEnsemble: 1, refitEpochs: 2 };');
}
const t0 = Date.now();
const ctx = {
  console, setTimeout, clearTimeout, Promise, Math, JSON, Date,
  performance: { now: () => Date.now() },
  document, Chart, tf,
  alert: (m) => console.log('ALERT', m), confirm: () => true,
};
ctx.window = ctx; ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(js + '\n;highlightBest = function(){};', ctx, { filename: 'harness.js' });

(async () => {
  await ctx.window.onload();
  // progress log
  let last = '';
  const timer = setInterval(() => {
    const s = elements.status ? elements.status.innerText : '';
    if (s !== last) { last = s; console.log(`[${((Date.now() - t0) / 1000).toFixed(0)}s] ${s}`); }
  }, 2000);
  await elements.runEvalBtn._handlers.click();
  clearInterval(timer);
  const summarize = (r, pooled) => pooled
    ? { mae: r.mae, rmse: r.rmse, r2: r.r2, chosen: r.chosenLog }
    : { mae: r.mae, rmse: r.rmse, r2: r.r2, chosen: r.chosenLog };
  const out = { variant, mathSeed, seconds: (Date.now() - t0) / 1000, cv: {}, lopo: {}, importance: ctx.__imp, finalCfg: ctx.__finalCfg,
    annPooled: { preds: ctx.__annPooled.pooledPreds, actuals: ctx.__annPooled.pooledActuals, missing: ctx.__annPooled.pooledMissing } };
  for (const [k, v] of Object.entries(ctx.__cv)) out.cv[k] = summarize(v, false);
  for (const [k, v] of Object.entries(ctx.__lopo)) out.lopo[k] = summarize(v, true);
  fs.writeFileSync(outPath, JSON.stringify(out, null, 1));
  console.log('DONE', out.seconds, 's ->', outPath);
  for (const [k, v] of Object.entries(out.cv)) console.log('CV  ', k.padEnd(18), v.mae.mean.toFixed(3), '±', v.mae.std.toFixed(3), '|', v.rmse.mean.toFixed(3), '±', v.rmse.std.toFixed(3), '|', v.r2.mean.toFixed(3), '±', v.r2.std.toFixed(3));
  for (const [k, v] of Object.entries(out.lopo)) console.log('LOPO', k.padEnd(18), v.mae.toFixed(3), '|', v.rmse.toFixed(3), '|', v.r2.toFixed(3));
})().catch(e => { console.error('ERROR', e); process.exit(1); });
