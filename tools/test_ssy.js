const fs = require("fs"), path = require("path");
const root = "C:/Users/Gowtham_Sravya/Documents/deepseek-harness/default-workspace/paisaclear";
const nodes = {};
function node(id, props={}) {
  nodes[id] = Object.assign({ id, value:"", hidden:false, innerHTML:"", handlers:{},
    addEventListener(t,f){this.handlers[t]=f;}, setAttribute(){}, classList:{toggle(){},add(){},remove(){}} }, props);
  return nodes[id];
}
const form = node("ssy-form"); node("ssy-output"); node("ssy-reset");
node("ssy-rules", { textContent: JSON.stringify({rate:"8.20%", asOf:"2026-10-01"}) });
node("ssy-amount"); node("ssy-years"); node("ssy-rate");
global.document = { getElementById: id => nodes[id] || null };
require(path.join(root, "site/assets/js/ssy.js"));
nodes["ssy-amount"].value = "150000";
nodes["ssy-years"].value = "15";
nodes["ssy-rate"].value = "8.2";
form.handlers.input();
const text = nodes["ssy-output"].innerHTML.replace(/<[^>]+>/g," ").replace(/\s+/g," ").trim();
console.log(text.slice(0, 240));
