/* Headless check: does compare.js render a table from the fetched catalogue? */

const fs = require("fs");
const path = require("path");
const root = path.resolve(__dirname, "..");

const products = JSON.parse(fs.readFileSync(path.join(root, "content/products.json"), "utf8"));
const catalog = products.slice(0, 3).map((p) => ({
  slug: p.slug, name: p.name, provider: p.provider, providerShort: p.providerShort,
  category: p.category, returnType: p.returnType, riskLevel: p.riskLevel,
  minInvestment: p.minInvestment, tenure: p.tenure, payout: p.payout,
  lockIn: p.lockIn || "None", liquidity: p.liquidity, eligibility: p.eligibility,
  tax: p.tax, protection: p.protection,
}));

const nodes = {};
function node(id, props = {}) {
  nodes[id] = Object.assign(
    { id, value: "", hidden: false, innerHTML: "", handlers: {},
      addEventListener(t, f) { this.handlers[t] = f; }, setAttribute() {}, removeAttribute() {}, classList: { toggle() {}, add() {}, remove() {} },
      querySelector() { return { hidden: false, addEventListener() {}, setAttribute() {}, classList: { toggle() {}, add() {}, remove() {} } }; },
      querySelectorAll() { return []; } },
    props
  );
  return nodes[id];
}

const slots = catalog.map((p, i) =>
  node("slot-" + i, { value: p.name + " — " + p.providerShort, dataset: { slot: String(i) } })
);
node("compare-wrap");
node("compare-head");

global.document = {
  getElementById: (id) => nodes[id] || null,
  querySelectorAll: (sel) => (sel === ".slot-select" ? slots : sel === ".slot" ? slots : []),
  querySelector: () => null,
};
global.window = { location: { search: "" }, history: { replaceState() {} }, console: console };
global.URLSearchParams = class { get() { return null; } };
global.fetch = () => Promise.resolve({ ok: true, json: () => Promise.resolve(catalog) });

require(path.join(root, "site/assets/js/compare.js"));

setTimeout(() => {
  const out = (nodes["compare-wrap"].innerHTML || "").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
  console.log("rendered length:", out.length);
  console.log("preview:", out.slice(0, 300) || "(empty)");
}, 60);
