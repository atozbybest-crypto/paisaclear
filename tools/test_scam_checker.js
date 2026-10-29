const fs=require("fs");
const root="C:/Users/Gowtham_Sravya/Documents/deepseek-harness/default-workspace/paisaclear";
const html=fs.readFileSync(root+"/site/check.html","utf8");
const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
const code=scripts[scripts.length-1];
const nodes={};
const n=(id)=>{nodes[id]={id,value:"",innerHTML:"",handlers:{},addEventListener(t,f){this.handlers[t]=f;}};return nodes[id];};
const form=n("scam-form"); n("scam-input"); n("scam-results"); n("scam-reset");
global.document={getElementById:id=>nodes[id]||null};
global.window={setTimeout:(f)=>f()};
new Function(code)();
const samples={
 "bank KYC scam":"Dear customer, your SBI account will be blocked in 24 hours. Complete KYC at http://sbi-kyc-verify.com and pay Rs 499",
 "lottery scam":"URGENT! You have won a lottery of Rs 25,00,000. Send your Aadhaar and PAN on WhatsApp 9876543210 to claim",
 "electricity scam":"Your electricity bill is overdue. Your power will be disconnected today. Pay now: https://bit.ly/xyz123",
 "loan scam":"Congratulations! Pre-approved loan of Rs 5,00,000. No CIBIL check. Pay processing fee Rs 2,999 for instant credit",
 "otp scam":"Your parcel is held at customs. Pay clearance fee and share the OTP to release it",
 "normal order":"Your order #1234 has been shipped and will arrive on 30 October. Track in the app.",
 "number only":"+91 98765 43210"
};
for (const [k,v] of Object.entries(samples)){
  nodes["scam-input"].value=v;
  form.handlers.input();
  const txt=nodes["scam-results"].innerHTML.replace(/<[^>]+>/g," ").replace(/\s+/g," ").trim();
  console.log(k.padEnd(18),"|",txt.slice(0,110));
}
