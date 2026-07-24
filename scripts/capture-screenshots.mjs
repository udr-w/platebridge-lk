import playwright from '../frontend/node_modules/@playwright/test/index.js';
import {mkdir} from 'node:fs/promises';
import path from 'node:path';
const base=process.env.PLATEBRIDGE_URL||'http://localhost:5173';
const out=path.resolve('../docs/screenshots');await mkdir(out,{recursive:true});
const browser=await playwright.chromium.launch({channel:process.env.CI?undefined:'chrome'});
async function login(page,email){await page.goto(`${base}/login`);await page.getByText(email).click();await page.waitForURL('**/dashboard')}
async function shot(page,name){await page.screenshot({path:path.join(out,name),fullPage:true})}
let page=await browser.newPage({viewport:{width:1440,height:1000}});await page.goto(base);await shot(page,'01-landing.png');
await login(page,'donor.home@platebridge.demo');await shot(page,'02-donor-dashboard.png');await page.goto(`${base}/donate`);await shot(page,'03-create-listing.png');
await page.getByPlaceholder(/Rice and curry/i).fill('Screenshot rice and curry');for(let i=0;i<4;i++)await page.getByRole('button',{name:/Next step/i}).click();await page.getByRole('button',{name:/Run safety check/i}).click();await page.waitForSelector('.safety');await shot(page,'04-safety-result.png');
await page.evaluate(()=>{localStorage.removeItem('platebridge-token')});await login(page,'recipient@platebridge.demo');await page.goto(`${base}/food`);await shot(page,'05-nearby-food.png');await page.getByRole('link',{name:/View details/i}).first().click();await shot(page,'06-listing-detail.png');await page.getByRole('button',{name:/Claim food/i}).click();await page.waitForURL('**/rescues/**');await shot(page,'07-rescue-detail.png');
await page.evaluate(()=>localStorage.removeItem('platebridge-token'));await login(page,'volunteer@platebridge.demo');await page.goto(`${base}/tasks`);await shot(page,'08-volunteer-dashboard.png');
await page.evaluate(()=>localStorage.removeItem('platebridge-token'));await login(page,'coordinator@platebridge.demo');await page.goto(`${base}/reviews`);await shot(page,'09-coordinator-review.png');
await page.evaluate(()=>localStorage.removeItem('platebridge-token'));await login(page,'admin@platebridge.demo');await page.goto(`${base}/admin`);await shot(page,'10-admin-dashboard.png');
await page.goto(`${base}/dashboard`);await page.selectOption('.language select','si');await shot(page,'11-sinhala.png');await page.selectOption('.language select','ta');await shot(page,'12-tamil.png');
await page.close();page=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1});await page.goto(base);await shot(page,'13-mobile.png');await browser.close();
console.log(`Captured 13 real application screenshots in ${out}`);
