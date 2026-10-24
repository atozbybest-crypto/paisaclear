/* Headless check of the scheme finder. */

const fs = require("fs");
const path = require("path");
const root = path.resolve(__dirname, "..");

const products = JSON.parse(fs.readFileSync(path.join(root, "content/products.json"), "utf8"));
const catalog = products.map((p) => ({
  s: p.slug, n: p.name, p: p.providerShort, c: p.category, r: p.returnType,
  l: p.riskLevel || "", m: typeof p.minInvestment === "number" ? p.minInvestment : null,
  k: Boolean(p.lockIn), y: (p.payoutFrequency || "").toLowerCase(), t: p.tenure || "",
  o: p.collections || [], b: p.bucket || "",
}));

const nodes = {};
function node(id, props = {}) {
  nodes[id] = Object.assign(
    { id, value: "", hidden: false, innerHTML: "", textContent: "", handlers: {},
      addEventListener(t, f) { this.handlers[t] = f; }, setAttribute() {} },
    props
  );
  return nodes[id];
}

const form = node("finder-form");
node("finder-results");
node("finder-reset");
node("finder-catalog", { textContent: JSON.stringify(catalog) });
["f-goal", "f-amount", "f-lock", "f-risk", "f-tax"].forEach((id) => node(id));

global.document = { getElementById: (id) => nodes[id] || null };
require(path.join(root, "site/assets/js/finder.js"));

function run(label, q) {
  nodes["f-goal"].value = q.goal;
  nodes["f-amount"].value = String(q.amount);
  nodes["f-lock"].value = q.lock;
  nodes["f-risk"].value = q.risk;
  nodes["f-tax"].value = q.tax;
  form.handlers.submit({ preventDefault() {} });
  const html = nodes["finder-results"].innerHTML;
  const count = (html.match(/<strong>(\d+)<\/strong>/) || [])[1];
  const names = [...html.matchAll(/class="finder-card-name"[^>]*>([^<]+)</g)].slice(0, 4).map((m) => m[1]);
  console.log(`${label}\n  matches: ${count}\n  first: ${names.join(" | ")}\n`);
}

run("Income, ₹1,00,000, reachable, no risk, no tax", { goal: "income", amount: 100000, lock: "none", risk: "none", tax: "no" });
run("Growth, ₹5,000, 5+ years, market swings", { goal: "grow", amount: 5000, lock: "long", risk: "any", tax: "no" });
run("Tax saving, ₹500, 5+ years, no risk", { goal: "tax", amount: 500, lock: "long", risk: "none", tax: "yes" });
run("Child, ₹1,000, 5+ years, no risk", { goal: "child", amount: 1000, lock: "long", risk: "none", tax: "no" });
run("Safe, ₹10,000, reachable, no risk", { goal: "safe", amount: 10000, lock: "none", risk: "none", tax: "no" });
