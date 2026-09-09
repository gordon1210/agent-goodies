// Use an already installed Playwright package; this runner never installs anything.
import { createRequire } from 'node:module';
import { readFile } from 'node:fs/promises';
const require=createRequire(import.meta.url);
if(!process.argv[2])throw new Error('Usage: node run-browser.mjs /absolute/path/to/installed/playwright');
const {chromium}=require(process.argv[2]);
const browser=await chromium.launch({headless:true});
try {
  const page=await browser.newPage();
  const source=await readFile(new URL('./test-browser.js',import.meta.url),'utf8');
  // Only the maintained, repository-owned test expression is evaluated.
  const test=(0,eval)(`(${source})`);
  console.log(JSON.stringify(await test(page),null,2));
} finally {await browser.close();}
