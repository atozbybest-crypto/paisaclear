const fs=require("fs");
const html=fs.readFileSync("C:/Users/Gowtham_Sravya/Documents/deepseek-harness/default-workspace/paisaclear/site/check.html","utf8");
const rules=[...html.matchAll(/\{ s: (\d), name: "([^"]+)", why: "([^"]*)", re: \/(.+?)\/i \}/g)];
console.log("parsed rules:", rules.length);
const text="Dear Consumer, your electricity power connection will be disconnected tonight at 9:30 PM because your previous month's bill was not updated. Contact our officer immediately at 98765xxxxx";
for(const r of rules){
  let re; try { re=new RegExp(r[4],"i"); } catch(e){ console.log("BAD REGEX:", r[2], e.message); continue; }
  if(re.test(text)) console.log("  match:", r[1], r[2]);
}
