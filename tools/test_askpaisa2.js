const fs=require("fs");
const root="C:/Users/Gowtham_Sravya/Documents/deepseek-harness/default-workspace/paisaclear";
const index=JSON.parse(fs.readFileSync(root+"/site/assets/data/askpaisa.json","utf8"));
const STOP=["open","show","me","about","the","a","an","of","for","what","is","tell","please","can","you","give","details","info","information","page","link","go","to","and","how","does","work","works","in","on"];
const SHORT=["us","usa","fd","sip","elss","nsc","kvp","scss","sbi"];
const toks=q=>q.toLowerCase().replace(/[^a-z0-9\s]/g," ").split(/\s+/).filter(t=>STOP.indexOf(t)===-1&&(t.length>2||SHORT.indexOf(t)!==-1));
const wantsUS=q=>/\b(us|usa|america|american|s&p|sp500|nasdaq|dow)\b/i.test(q);
function search(q){const ts=toks(q),ql=q.toLowerCase().trim(),us=wantsUS(q);
 return index.map(e=>{const title=e.t.toLowerCase(),w=(e.w||"").toLowerCase(),s=(e.s||"").toLowerCase();let v=0;
  if(title.includes(ql))v+=40; ts.forEach(t=>{if(title.includes(t))v+=8;if(w.includes(t))v+=4;if(s.includes(t))v+=1;});
  const hit=ts.filter(t=>title.includes(t)||w.includes(t)||s.includes(t)).length; if(ts.length&&hit===ts.length)v+=6;
  const isUS=e.u.indexOf("us-")===0; v+= us?(isUS?30:-10):(isUS?-6:0); return {e,s:v};})
  .filter(r=>r.s>0).sort((a,b)=>b.s-a.s||a.e.t.length-b.e.t.length).slice(0,3);}
for(const q of ["us index funds","tell me about sukanya yojana","is this message a scam","ppf vs fd","open mutual funds aditya birla","us treasury yields","senior citizen scheme"]){
  const r=search(q); console.log(q.padEnd(34),"->",r.length?r[0].e.t+" ["+r[0].e.k+"]": "no match");
}
