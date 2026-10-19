/* Headless check of the salary calculator: stubs the DOM, runs the real
   salary.js, and prints what it would render. */

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const rules = JSON.parse(fs.readFileSync(path.join(root, "content/tax-rules.json"), "utf8"));

const nodes = {};
function node(id, props = {}) {
  nodes[id] = Object.assign(
    { id, value: "", checked: false, hidden: false, innerHTML: "", textContent: "", handlers: {},
      addEventListener(type, fn) { this.handlers[type] = fn; },
      setAttribute() {}, querySelector() { return null; } },
    props
  );
  return nodes[id];
}

node("tax-rules", { textContent: JSON.stringify(rules) });
const form = node("salary-form");
node("calc-output");
node("calc-empty");
node("calc-reset");

function setValue(id, value) { node("calc-" + id, {}).value = String(value); }
["ctc", "basic", "hra", "rent", "sec80c", "sec80d", "home", "pt"].forEach((id) => node("calc-" + id, {}));
node("calc-metro", { checked: true });
node("calc-pf-in-ctc", { checked: true });

global.document = { getElementById: (id) => nodes[id] || null };

require(path.join(root, "site/assets/js/salary.js"));

function strip(html) {
  return html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
}

function run(label, values) {
  setValue("ctc", values.ctc);
  setValue("basic", values.basic ?? 40);
  setValue("hra", values.hra ?? 50);
  setValue("rent", values.rent ?? 0);
  setValue("sec80c", values.sec80c ?? 0);
  setValue("sec80d", values.sec80d ?? 0);
  setValue("home", values.home ?? 0);
  setValue("pt", values.pt ?? 2400);
  nodes["calc-metro"].checked = values.metro ?? true;

  const handler = form.handlers.submit;
  handler({ preventDefault() {} });

  const text = strip(nodes["calc-output"].innerHTML);
  console.log(`\n=== ${label} (CTC ${values.ctc}) ===`);
  console.log(text.slice(0, 700));
}

run("₹12L, no rent, no 80C", { ctc: 1200000 });
run("₹20L, rent 25k/mo, 80C 1.5L", { ctc: 2000000, rent: 25000, sec80c: 150000 });
run("₹35L, rent 40k, 80C 1.5L, 80D 25k, home loan 2L", {
  ctc: 3500000, rent: 40000, sec80c: 150000, sec80d: 25000, home: 200000,
});
