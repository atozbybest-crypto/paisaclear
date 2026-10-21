/* Headless check of the emergency-fund and retirement arithmetic. */

const fs = require("fs");
const path = require("path");
const root = path.resolve(__dirname, "..");

const nodes = {};
function node(id, props = {}) {
  nodes[id] = Object.assign(
    { id, value: "", hidden: false, innerHTML: "", textContent: "", handlers: {},
      addEventListener(t, f) { this.handlers[t] = f; },
      setAttribute() {}, getAttribute() { return null; },
      classList: { toggle() {} }, querySelector() { return null; } },
    props
  );
  return nodes[id];
}

const form = node("plan-form");
node("plan-output");
node("plan-catalog", {
  textContent: JSON.stringify([
    { s: "x", n: "Test FD", p: "Bank", c: "bank-deposits", r: "guaranteed", m: 1000 },
    { s: "y", n: "Test Fund", p: "AMC", c: "mutual-funds", r: "market-linked", m: 500 },
  ]),
});

const values = {
  "e-expenses": 30000, "e-months": 6, "e-saved": 0, "e-monthly": 10000,
  "r-age": 30, "r-retire": 60, "r-expenses": 40000, "r-inflation": 5,
  "r-grow": 10, "r-post": 7, "r-years": 25, "r-saved": 0, "r-monthly": 15000,
};
Object.keys(values).forEach((id) => node(id, { value: String(values[id]) }));

const tabs = ["emergency", "retire"].map((m) => node("tab-" + m, { getAttribute: () => m }));

global.document = {
  getElementById: (id) => nodes[id] || null,
  querySelectorAll: (sel) => (sel === "[data-plan-tab]" ? tabs : []),
};

require(path.join(root, "site/assets/js/plan.js"));

function strip(html) { return html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim(); }

console.log("EMERGENCY:", strip(nodes["plan-output"].innerHTML).slice(0, 320));
tabs[1].handlers.click();
console.log("\nRETIREMENT:", strip(nodes["plan-output"].innerHTML).slice(0, 420));
