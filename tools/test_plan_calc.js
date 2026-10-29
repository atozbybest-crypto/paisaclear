const fs=require("fs"),path=require("path");
const root="C:/Users/Gowtham_Sravya/Documents/deepseek-harness/default-workspace/paisaclear";
function run(type, periods, term, amount, rate, years){
  const nodes={};
  const n=(id,p={})=>nodes[id]=Object.assign({id,value:"",innerHTML:"",handlers:{},addEventListener(t,f){this.handlers[t]=f;},setAttribute(){},classList:{toggle(){}}},p);
  const form=n("plan-form"); n("plan-output"); n("plan-reset");
  n("plan-config",{textContent:JSON.stringify({type,periods,term})});
  n("plan-amount",{value:String(amount)}); n("plan-rate",{value:String(rate)}); n("plan-years",{value:String(years)});
  global.document={getElementById:id=>nodes[id]||null};
  delete require.cache[require.resolve(path.join(root,"site/assets/js/plan-calc.js"))];
  require(path.join(root,"site/assets/js/plan-calc.js"));
  form.handlers.input();
  const text=nodes["plan-output"].innerHTML.replace(/<[^>]+>/g," ").replace(/\s+/g," ").trim();
  console.log(type.padEnd(10), "|", text.slice(0,150));
}
run("recurring",null,15,150000,7.1,15);
run("lumpsum",null,5,100000,7.7,5);
run("payout",4,5,1000000,8.2,5);
