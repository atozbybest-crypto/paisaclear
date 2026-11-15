const fs = require("fs");
const root = "C:/Users/Gowtham_Sravya/Documents/deepseek-harness/default-workspace/paisaclear";
const code = fs.readFileSync(root + "/site/assets/js/market-game.js", "utf8");
const nodes = {};
function mk(id){return {id,textContent:"",innerHTML:"",className:"",value:"10",listeners:{},
  addEventListener(t,f){this.listeners[t]=f;},getAttribute(){return null;}};}
["mg-cash","mg-worth","mg-pnl","mg-day","mg-market","mg-portfolio","mg-news","mg-badges","mg-log","mg-streak","mg-goal","mg-board","mg-qty","mg-play","mg-reset","mg-retire","mg-share"].forEach(i=>nodes[i]=mk(i));
global.document={readyState:"complete",getElementById:i=>nodes[i]||null,addEventListener(){},createElement:()=>mk("x")};
global.window={setTimeout:f=>f()};
const store={};
global.localStorage={getItem:k=>(k in store?store[k]:null),setItem:(k,v)=>{store[k]=v;}};
let ticks=[]; global.setInterval=(f)=>{ticks.push(f);return 1;};
new Function(code)();
console.log("boot cash:", nodes["mg-cash"].textContent, "| streak:", nodes["mg-streak"].textContent);
console.log("companies:", (nodes["mg-market"].innerHTML.match(/data-buy/g)||[]).length);
console.log("goal:", nodes["mg-goal"].innerHTML.replace(/<[^>]+>/g," ").replace(/\s+/g," ").trim());
for(let i=0;i<27;i++) ticks[0]();
console.log("after 27 days:", nodes["mg-day"].textContent, "| worth:", nodes["mg-worth"].textContent);
console.log("story/news sample:", nodes["mg-news"].innerHTML.replace(/<[^>]+>/g," ").replace(/\s+/g," ").trim().slice(0,140));
// buy then retire
nodes["mg-market"].listeners["click"]({target:{getAttribute:a=>a==="data-buy"?"nova":null}});
nodes["mg-retire"].listeners["click"]();
console.log("board rows:", (nodes["mg-board"].innerHTML.match(/<tr>/g)||[]).length);
console.log("log:", nodes["mg-log"].innerHTML.replace(/<[^>]+>/g," ").replace(/\s+/g," ").trim().slice(0,110));
