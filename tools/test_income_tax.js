/* Headless check of the income-tax calculator. */

const fs = require("fs");
const path = require("path");
const root = path.resolve(__dirname, "..");

const rules = JSON.parse(fs.readFileSync(path.join(root, "content/tax-rules.json"), "utf8"));

const nodes = {};
function node(id, props = {}) {
  nodes[id] = Object.assign(
    { id, value: "", hidden: false, innerHTML: "", handlers: {},
      addEventListener(t, f) { this.handlers[t] = f; }, setAttribute() {} },
    props
  );
  return nodes[id];
}

const form = node("it-form");
node("it-output");
node("it-rules", { textContent: JSON.stringify(rules) });
node("it-reset");
["it-year", "it-entity", "it-age", "it-status", "it-regime", "it-turnover", "it-income",
 "row-age", "row-status", "row-regime", "row-turnover"].forEach((id) => node(id));

global.document = { getElementById: (id) => nodes[id] || null };

require(path.join(root, "site/assets/js/income-tax.js"));

function run(label, cfg) {
  nodes["it-entity"].value = cfg.entity || "individual";
  nodes["it-age"].value = cfg.age || "below60";
  nodes["it-status"].value = cfg.status || "resident";
  nodes["it-regime"].value = cfg.regime || "new";
  nodes["it-turnover"].value = cfg.turnover || "small";
  nodes["it-income"].value = String(cfg.income);
  form.handlers.submit({ preventDefault() {} });
  const text = nodes["it-output"].innerHTML.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
  console.log(`\n${label}\n  ${text.slice(0, 260)}`);
}

run("Individual, new regime, ₹15,00,000", { income: 1500000 });
run("Individual, old regime, ₹15,00,000 (expect 2,62,500 + cess)", { income: 1500000, regime: "old" });
run("Individual, old regime, senior 60-80, ₹6,00,000", { income: 600000, regime: "old", age: "senior" });
run("Individual, old regime, super senior 80+, ₹12,00,000", { income: 1200000, regime: "old", age: "superSenior" });
run("Firm, ₹15,00,000 (expect 30% + cess)", { income: 1500000, entity: "firm" });
run("Company (small), ₹15,00,000 (expect 25% + cess)", { income: 1500000, entity: "company" });
run("Non-resident, new regime, ₹15,00,000 (no rebate)", { income: 1500000, status: "nonresident" });
run("Individual, new regime, ₹11,00,000 (rebate applies)", { income: 1100000 });
