const fs = require("fs");

const html = fs.readFileSync("public/index.html", "utf8");
const scripts = Array.from(html.matchAll(/<script>([\s\S]*?)<\/script>/g), (match) => match[1]).join("\n");
new Function(scripts);

const required = [
  'id="homeHub"',
  'data-module-page="regulators"',
  'data-module-page="licenses"',
  'data-module-page="compare"',
  'data-module-page="updates"',
  'data-module-page="developer-log"',
  '#module/licenses',
];

for (const text of required) {
  if (!html.includes(text)) {
    throw new Error(`Missing expected module marker: ${text}`);
  }
}

const removed = [
  'class="sidebar"',
  'id="sideLicenseNav"',
  'data-module-route="regulators"',
];

for (const text of removed) {
  if (html.includes(text)) {
    throw new Error(`Unexpected legacy sidebar marker remains: ${text}`);
  }
}

const devLog = JSON.parse(fs.readFileSync("public/developer-log.json", "utf8"));
if (!Array.isArray(devLog.entries) || !devLog.entries.some((entry) => entry.title.includes("信息模块"))) {
  throw new Error("Developer log does not include the modularization entry");
}

const regulatorFieldReferences = [
  "r.name",
  "r.full",
  "r.focus",
  "r.licenses",
  "r.role",
  "r.importance",
  "r.decides",
  "r.notInScope",
  "r.triggers",
  "r.watch",
  "r.signals",
];

for (const field of regulatorFieldReferences) {
  if (!html.includes(field)) {
    throw new Error(`Regulator render no longer references ${field}`);
  }
}

console.log("Modular dashboard check passed");
