/* Headless check of the savings calculator arithmetic. */

const fs = require("fs");
const path = require("path");
const root = path.resolve(__dirname, "..");

const nodes = {};
function node(id, props = {}) {
  nodes[id] = Object.assign(
    { id, value: "", checked: false, hidden: false, innerHTML: "", handlers: {},
      addEventListener(t, f) { this.handlers[t] = f; },
      setAttribute() {}, getAttribute() { return null; }, classList: { toggle() {} },
      querySelector() { return null; } },
    props
  );
  return nodes[id];
}

const form = node("money-form");
const output = node("money-output");
["monthly", "stepup", "amount", "principal", "addmonthly", "years", "rate", "inflation"]
  .forEach((id) => node("m-" + id, {}));
node("m-compounding", { value: "quarterly" });

const tabs = ["sip", "lump", "deposit"].map((mode) =>
  node("tab-" + mode, { getAttribute: () => mode })
);

global.document = {
  getElementById: (id) => nodes[id] || null,
  querySelectorAll: (sel) => (sel === "[data-money-tab]" ? tabs : []),
};

require(path.join(root, "site/assets/js/money.js"));

function set(id, value) { node("m-" + id).value = String(value); }
function run(label) {
  form.handlers.input();
  const text = output.innerHTML.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
  console.log(`${label}: ${text.slice(0, 150)}`);
}

// SIP: 5,000/month, 10 years, 8%
set("monthly", 5000); set("stepup", 0); set("years", 10); set("rate", 8); set("inflation", 5);
run("SIP 5000 x 10y @8%");

// Lump sum: 1,00,000 for 10 years at 8% => 2,15,892
set("amount", 100000);
form.handlers.input();
console.log("lump expected ~215,892");

// Deposit: 1,00,000 quarterly @ 7% for 5 years
set("principal", 100000); set("years", 5); set("rate", 7); set("addmonthly", 0);
form.handlers.input();
console.log("deposit expected ~141,478");
