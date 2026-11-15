const fs = require("fs");
const root = "C:/Users/Gowtham_Sravya/Documents/deepseek-harness/default-workspace/paisaclear";
const code = fs.readFileSync(root + "/site/assets/js/market-game.js", "utf8");

const nodes = {};
function makeEl(id) {
  return {
    id, textContent: "", innerHTML: "", className: "", value: "10",
    listeners: {},
    addEventListener(t, f) { this.listeners[t] = f; },
    getAttribute() { return null; }
  };
}
["mg-cash","mg-worth","mg-pnl","mg-day","mg-market","mg-portfolio","mg-news","mg-badges","mg-log","mg-qty","mg-play","mg-reset"]
  .forEach(id => nodes[id] = makeEl(id));

global.document = {
  readyState: "complete",
  getElementById: id => nodes[id] || null,
  addEventListener() {},
  createElement: () => makeEl("x")
};
global.window = { setTimeout: (f) => f() };
const store = {};
global.localStorage = {
  getItem: k => (k in store ? store[k] : null),
  setItem: (k, v) => { store[k] = v; }
};
let intervals = [];
global.setInterval = (f, ms) => { intervals.push(f); return 1; };
global.clearInterval = () => {};

new Function(code)();
console.log("booted. cash:", nodes["mg-cash"].textContent);
console.log("market rows rendered:", (nodes["mg-market"].innerHTML.match(/data-buy/g) || []).length);

// tick the market 20 times
for (let i = 0; i < 20; i++) intervals[0]();
console.log("after 20 days:", nodes["mg-day"].textContent, "| worth:", nodes["mg-worth"].textContent);

// simulate a buy click on the first company
const handler = nodes["mg-market"].listeners["click"];
handler({ target: { getAttribute: (a) => a === "data-buy" ? "sunrise" : null } });
console.log("after buy:", "cash", nodes["mg-cash"].textContent, "| holdings rows:", (nodes["mg-portfolio"].innerHTML.match(/<tr>/g)||[]).length);
console.log("log:", nodes["mg-log"].innerHTML.replace(/<[^>]+>/g," ").trim().slice(0,90));

// simulate a sell
handler({ target: { getAttribute: (a) => a === "data-sell" ? "sunrise" : null } });
console.log("after sell:", "cash", nodes["mg-cash"].textContent);
console.log("saved state has holdings field:", "holdings" in JSON.parse(store["paisaclear-market-v1"]));
