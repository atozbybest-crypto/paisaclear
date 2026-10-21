/* Headless check of the EMI maths. */

const fs = require("fs");
const path = require("path");
const root = path.resolve(__dirname, "..");

const nodes = {};
function node(id, props = {}) {
  nodes[id] = Object.assign(
    { id, value: "", hidden: false, innerHTML: "", handlers: {},
      addEventListener(t, f) { this.handlers[t] = f; }, setAttribute() {} },
    props
  );
  return nodes[id];
}

const form = node("loan-form");
node("loan-output");
const values = { "l-amount": 2000000, "l-rate": 8.5, "l-years": 20, "l-extra": 0 };
Object.keys(values).forEach((id) => node(id, { value: String(values[id]) }));

global.document = { getElementById: (id) => nodes[id] || null };

require(path.join(root, "site/assets/js/loan.js"));

const text = nodes["loan-output"].innerHTML.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
console.log(text.slice(0, 420));
console.log("\n--- expected: EMI ~17,356 · interest ~21.65 L · total ~41.65 L ---");
