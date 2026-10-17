/* Headless smoke test for the single-file build.
 *
 * There is no browser available in this environment, so this stubs the small
 * slice of the DOM the renderer touches, renders every route, and writes the
 * HTML out for structural checking.
 *
 *   node tools/test_spa.js
 */

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const bundle = fs.readFileSync(path.join(root, "PaisaClear.html"), "utf8");

const marker = "window.PAISA_DATA = ";
const start = bundle.indexOf(marker);
const end = bundle.indexOf(";</script>", start);
if (start === -1 || end === -1) {
  console.error("FAIL: could not find embedded data in PaisaClear.html");
  process.exit(1);
}
const data = JSON.parse(bundle.slice(start + marker.length, end));

global.window = {
  location: { hash: "#/" },
  addEventListener() {},
  scrollTo() {},
  history: { replaceState() {} }
};
global.document = {
  getElementById() { return null; },
  querySelectorAll() { return []; },
  addEventListener() {},
  title: ""
};

require(path.join(root, "spa", "app.js"));
window.PAISA_DATA = data;

if (!window.PaisaApp || typeof window.PaisaApp.render !== "function") {
  console.error("FAIL: renderer did not expose PaisaApp.render");
  process.exit(1);
}

const first = data.products[0];
const routes = [
  ["home", "#/"],
  ["browse", "#/browse"],
  ["browse-query", "#/browse?q=monthly"],
  ["category", "#/category/government-schemes"],
  ["category-guide", "#/category/bank-deposits"],
  ["product", "#/product/" + first.slug],
  ["compare", "#/compare?p=" + data.products.slice(0, 2).map((p) => p.slug).join(",")],
  ["method", "#/method"],
  ["missing", "#/nope"]
];

const outDir = path.join(root, ".spa-test");
fs.mkdirSync(outDir, { recursive: true });

let failures = 0;
for (const [name, hash] of routes) {
  window.location.hash = hash;
  let html = "";
  try {
    html = window.PaisaApp.render();
  } catch (error) {
    console.error(`FAIL ${name} (${hash}): ${error.message}`);
    failures += 1;
    continue;
  }

  if (typeof html !== "string" || html.length < 200) {
    console.error(`FAIL ${name}: rendered ${html ? html.length : 0} characters`);
    failures += 1;
    continue;
  }
  if (html.includes("undefined") || html.includes("NaN")) {
    console.error(`WARN ${name}: output contains undefined/NaN`);
    failures += 1;
  }

  fs.writeFileSync(path.join(outDir, name + ".html"), html, "utf8");
  console.log(`ok   ${name.padEnd(14)} ${String(html.length).padStart(6)} chars  ${hash}`);
}

console.log(failures ? `\n${failures} route(s) failed` : "\nall routes rendered");
window.PaisaApp = undefined;
process.exit(failures ? 1 : 0);
