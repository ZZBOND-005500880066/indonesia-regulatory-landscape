const fs = require("fs");

const html = fs.readFileSync("public/index.html", "utf8");
const scripts = Array.from(html.matchAll(/<script>([\s\S]*?)<\/script>/g), (match) => match[1]).join("\n");
new Function(scripts);

const required = [
  'id="homeHub"',
  'data-module-page="regulators"',
  'data-module-page="licenses"',
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
  'data-module-page="compare"',
  '<a class="module-card" href="#module/compare"',
  'value="module:compare"',
  'id="licenseMatrix"',
];

for (const text of removed) {
  if (html.includes(text)) {
    throw new Error(`Unexpected legacy sidebar marker remains: ${text}`);
  }
}

const devLog = JSON.parse(fs.readFileSync("public/developer-log.json", "utf8"));
if (!Array.isArray(devLog.entries) || devLog.entries.length === 0) {
  throw new Error("Developer log is empty");
}

const invalidDevLogEntry = devLog.entries.find(
  (entry) => !entry.date || !entry.title || !entry.author || !entry.commit
);
if (invalidDevLogEntry) {
  throw new Error("Developer log entry is missing automatic commit metadata");
}

if (!devLog.entries.some((entry) => entry.commitUrl && entry.commitUrl.includes("/commit/"))) {
  throw new Error("Developer log does not include commit links");
}

const commercialBankMarkers = [
  '"bankDirectory"',
  "商业银行玩家库",
  'href="#license/${esc(item.id)}/${esc(bank.id)}"',
  'hash.match(/^license\\/commercial-bank\\/([^/]+)$/)',
  "function bankDetailPage",
  "Bank Nano Syariah",
  "牌照获批时间",
];

for (const text of commercialBankMarkers) {
  if (!html.includes(text)) {
    throw new Error(`Missing commercial bank directory marker: ${text}`);
  }
}

const licensesMatch = html.match(/const LICENSES = (\[.*?\]);/s);
if (!licensesMatch) {
  throw new Error("Cannot find generated license data");
}

const licenses = JSON.parse(licensesMatch[1]);
const commercialBank = licenses.find((item) => item.id === "commercial-bank");
const commercialBanks = (commercialBank.bankDirectory || []).flatMap((group) => group.banks || []);
if (commercialBanks.length < 40) {
  throw new Error("Commercial bank directory lost bank rows");
}

const banksWithoutSources = commercialBanks.filter(
  (bank) => !Array.isArray(bank.sources) || bank.sources.length === 0
);
if (banksWithoutSources.length > 0) {
  throw new Error(`Commercial bank rows missing sources: ${banksWithoutSources.map((bank) => bank.id).join(", ")}`);
}

const unresolvedCommercialBankRows = commercialBanks.filter((bank) =>
  ["assets", "coreCapital", "marketCap", "licenseApprovalTime"].some((field) =>
    String(bank[field] || "").includes("报告未列明")
  )
);
if (unresolvedCommercialBankRows.length > 0) {
  throw new Error(
    `Commercial bank rows still contain source-document placeholders: ${unresolvedCommercialBankRows
      .map((bank) => bank.id)
      .join(", ")}`
  );
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
