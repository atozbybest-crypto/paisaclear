const fs=require("fs");
const root="C:/Users/Gowtham_Sravya/Documents/deepseek-harness/default-workspace/paisaclear";
const html=fs.readFileSync(root+"/site/check.html","utf8");
const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
const nodes={};
const n=id=>{nodes[id]={id,value:"",innerHTML:"",handlers:{},addEventListener(t,f){this.handlers[t]=f;}};return nodes[id];};
const form=n("scam-form"); n("scam-input"); n("scam-results"); n("scam-reset");
global.document={getElementById:id=>nodes[id]||null}; global.window={setTimeout:f=>f()};
new Function(scripts[scripts.length-1])();
const samples={
 "package":"USPS: Your package could not be delivered due to an incomplete address. Update your info here to reschedule: suspicious-link.com",
 "toll":"ExpressToll Service: Our records show an unpaid balance of $4.50. Pay immediately to avoid a $50 late fee: fake-toll-site.com",
 "bank phish":"SECURITY ALERT: We detected a suspicious $500.00 charge on your debit card. If this wasn't you, reply STOP or verify your account here: fake-bank-login.com",
 "casual opener":"Hey, are we still meeting for lunch tomorrow?",
 "job offer":"Hello, I found your resume online. Our company is hiring remote workers for flexible hours making $300/day. Message us on WhatsApp to start: 555-0199",
 "normal":"Your order #1234 has been shipped and will arrive on 30 October."
};
for(const [k,v] of Object.entries(samples)){
  nodes["scam-input"].value=v; form.handlers.input();
  const txt=nodes["scam-results"].innerHTML.replace(/<[^>]+>/g," ").replace(/\s+/g," ").trim();
  console.log(k.padEnd(14),"|",txt.slice(0,95));
}
