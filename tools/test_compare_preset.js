/* Reproduces: opening /compare?p=<slug> should pre-select that product in slot 1. */

const fs = require("fs");
const path = require("path");
const root = path.resolve(__dirname, "..");

const products = JSON.parse(fs.readFileSync(path.join(root, "content/products.json"), "utf8"));
const picked = products[0];
const catalog = products.slice(0, 3).map((p) => ({
  slug: p.slug, name: p.name, provider: p.provider, providerShort: p.providerShort,
  category: p.category, returnType: p.returnType, riskLevel: p.riskLevel,
  minInvestment: p.minInvestment, tenure: p.tenure, payout: p.payout,
  lockIn: p.lockIn || "None", liquidity: p.liquidity, eligibility: p.eligibility,
  tax: p.tax, protection: p.protection,
}));

function makeNode(id) {
  return {
    id, value: "", hidden: false, innerHTML: "", textContent: "", disabled: false,
    dataset: {}, handlers: {},
    addEventListener(t, f) { this.handlers[t] = f; },
    setAttribute() {}, removeAttribute() {},
    classList: { toggle() {}, add() {}, remove() {} },
    querySelector() {
      return { hidden: false, addEventListener() {}, setAttribute() {},
               classList: { toggle() {}, add() {}, remove() {} } };
    },
    querySelectorAll() { return []; },
  };
}

const slots = [0, 1, 2].map((i) => makeNode("slot-" + i));
const nodes = {
  "compare-wrap": makeNode("compare-wrap"),
  "compare-head": makeNode("compare-head"),
};
const hint = makeNode("hint");

global.document = {
  getElementById: (id) => nodes[id] || null,
  querySelector: () => hint,
  querySelectorAll: (sel) =>
    sel === ".slot-select" ? slots : sel === ".slot" ? slots : [],
};
global.window = { location: { search: "?p=" + picked.slug }, history: { replaceState() {} }, console };
global.fetch = () => Promise.resolve({ ok: true, json: () => Promise.resolve(catalog) });

require(path.join(root, "site/assets/js/compare.js"));

setTimeout(() => {
  const expected = picked.name + " — " + picked.providerShort;
  const actual = slots[0].value;
  console.log("expected slot 1:", expected);
  console.log("actual slot 1  :", actual || "(empty)");
  console.log(actual === expected ? "PASS" : "FAIL");
  const table = (nodes["compare-head"].innerHTML || "").replace(/<[^>]+>/g, " ").trim();
  console.log("table rendered :", table ? "yes" : "no", table.slice(0, 80));
}, 80);
