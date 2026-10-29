const fs=require("fs");
const t=fs.readFileSync("C:/Users/Gowtham_Sravya/Documents/deepseek-harness/default-workspace/paisaclear/builder/checker.py","utf8");
const line=t.split("\n").find(l=>l.includes("Electricity, gas or water disconnection"));
console.log("rule:", line.trim().slice(0,200));
const text="Dear Consumer, your electricity power connection will be disconnected tonight at 9:30 PM because your previous month's bill was not updated. Contact our officer immediately at 98765xxxxx";
const m=line.match(/re: \/(.*)\/i \}/);
if(m){ const re=new RegExp(m[1],"i"); console.log("matches electricity:", re.test(text)); }
