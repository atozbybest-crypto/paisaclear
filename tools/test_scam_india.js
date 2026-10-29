const fs=require("fs");
const root="C:/Users/Gowtham_Sravya/Documents/deepseek-harness/default-workspace/paisaclear";
const html=fs.readFileSync(root+"/site/check.html","utf8");
const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
const nodes={}; const n=id=>{nodes[id]={id,value:"",innerHTML:"",handlers:{},addEventListener(t,f){this.handlers[t]=f;}};return nodes[id];};
const form=n("scam-form"); n("scam-input"); n("scam-results"); n("scam-reset");
global.document={getElementById:id=>nodes[id]||null}; global.window={setTimeout:f=>f()};
new Function(scripts[scripts.length-1])();
const s={
 "1 KYC block":"Dear Customer, your HDFC account/PAN/KYC has expired. Your account will be blocked tonight. Update your KYC immediately using this link: suspicious-link.com",
 "2 task job":"Work from home part-time job! Like YouTube videos or rate hotels on Google and earn ₹3,000 to ₹5,000 per day. Message us on Telegram: @scam_handle",
 "3 family":"Hi Papa/Mummy, this is my new number. I lost my phone and wallet. I'm in an emergency, please transfer ₹15,000 immediately to this UPI ID: scam@upi",
 "4 electricity":"Dear Consumer, your electricity power connection will be disconnected tonight at 9:30 PM because your previous month's bill was not updated. Contact our officer immediately at 98765xxxxx",
 "5 wrong UPI":"Dear user, I have mistakenly sent ₹5,000 to your UPI instead of my friend. Please return the amount back to this number immediately.",
 "6 courier":"Your parcel could not be delivered / is held at customs due to illegal items. Update your address or pay clearance fees now at malicious-link.com or face police action."
};
for(const [k,v] of Object.entries(s)){
  nodes["scam-input"].value=v; form.handlers.input();
  const txt=nodes["scam-results"].innerHTML.replace(/<[^>]+>/g," ").replace(/\s+/g," ").trim();
  console.log(k.padEnd(14),"|",txt.slice(0,88));
}
