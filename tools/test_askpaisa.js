const fs = require("fs");
const root = "C:/Users/Gowtham_Sravya/Documents/deepseek-harness/default-workspace/paisaclear";
const index = JSON.parse(fs.readFileSync(root + "/site/assets/data/askpaisa.json", "utf8"));
const STOP = ["open","show","me","about","the","a","an","of","for","what","is","tell","please","can","you","give","details","info","information","page","link","go","to","and","how","does","work","works","in","on"];
const toks = q => q.toLowerCase().replace(/[^a-z0-9\s]/g," ").split(/\s+/).filter(t=>t.length>2&&!STOP.includes(t));
function score(e,q,ts){const title=e.t.toLowerCase(),w=(e.w||"").toLowerCase(),s=(e.s||"").toLowerCase();let v=0;
  if(title.includes(q))v+=40; ts.forEach(t=>{if(title.includes(t))v+=8; if(w.includes(t))v+=4; if(s.includes(t))v+=1;});
  const hit=ts.filter(t=>title.includes(t)||w.includes(t)||s.includes(t)).length; if(ts.length&&hit===ts.length)v+=6; return v;}
function search(q){const ts=toks(q); if(!ts.length)return[]; const ql=q.toLowerCase().trim();
  return index.map(e=>({e,s:score(e,ql,ts)})).filter(r=>r.s>0).sort((a,b)=>b.s-a.s||a.e.t.length-b.e.t.length).slice(0,3);}
for (const q of ["open mutual funds aditya birla","tell me about sukanya yojana","is this message a scam","us index funds","ppf vs fd","best tax saving fund","senior citizen scheme","loan emi"]) {
  const r = search(q);
  console.log(q.padEnd(38), "->", r.length ? r[0].e.t + "  [" + r[0].e.k + "] " + r[0].s : "no match");
}
