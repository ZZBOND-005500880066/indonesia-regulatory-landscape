const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");

const dashboard = path.resolve(__dirname, "../outputs/indonesia_financial_regulatory_landscape.html");
const screenshotDir = path.resolve(__dirname, "screenshots");
fs.mkdirSync(screenshotDir, { recursive: true });

async function main() {
  const { chromium } = require("playwright");
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  const errors = [];
  page.on("pageerror", err => errors.push(err.message));
  page.on("console", msg => {
    if (msg.type() === "error") errors.push(msg.text());
  });

  await page.goto(pathToFileURL(dashboard).href, { waitUntil: "networkidle" });
  await page.screenshot({ path: path.join(screenshotDir, "home.png"), fullPage: true });
  const cards = await page.locator(".license-card").count();
  const title = await page.locator("h2").first().innerText();

  await page.goto(pathToFileURL(dashboard).href + "#license/p2p", { waitUntil: "networkidle" });
  await page.screenshot({ path: path.join(screenshotDir, "p2p.png"), fullPage: true });
  const p2pTitle = await page.locator(".detail-title h2").innerText();
  const metrics = await page.locator(".metric").count();

  await browser.close();

  if (errors.length) {
    throw new Error(errors.join("\n"));
  }
  if (cards !== 7) {
    throw new Error(`Expected 7 license cards, found ${cards}`);
  }
  if (!title.includes("印尼核心金融牌照")) {
    throw new Error(`Unexpected home title: ${title}`);
  }
  if (p2pTitle.trim() !== "P2P" || metrics !== 4) {
    throw new Error(`Detail route failed: ${p2pTitle}, metrics ${metrics}`);
  }
  console.log("Dashboard check passed");
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
