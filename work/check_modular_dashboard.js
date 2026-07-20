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
  '.metric strong',
  'grid-template-columns: 1.1fr 1.35fr .9fr .9fr .8fr',
  'class="bank-row bank-head"',
];

for (const text of removed) {
  if (html.includes(text)) {
    throw new Error(`Unexpected removed marker remains: ${text}`);
  }
}

const formattingMarkers = [
  "IDR_USD_RATE = 17944",
  "Bank Indonesia JISDOR",
  "function moneyText",
  "function keyData",
  "keyDataPattern",
  'class="key-data"',
  'class="metric-value"',
  'class="usd-equiv"',
  'class="bank-shape-pill"',
  'class="bank-shape-pill player-shape-pill"',
  'class="bank-row-action"',
  'class="bank-detail-grid player-detail-grid"',
  "约 USD",
];

for (const text of formattingMarkers) {
  if (!html.includes(text)) {
    throw new Error(`Missing formatting marker: ${text}`);
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
  "股权变更时间",
];

for (const text of commercialBankMarkers) {
  if (!html.includes(text)) {
    throw new Error(`Missing commercial bank directory marker: ${text}`);
  }
}

const multiFinanceMarkers = [
  "Multi-Finance 玩家目录",
  "function renderMultiFinanceDirectory",
  "function multiFinancePlayerPage",
  'href="#license/${esc(item.id)}/${esc(multiFinancePlayerSlug(player))}"',
  'hash.match(/^license\\/multi-finance\\/([^/]+)$/)',
  "Multi-Finance 玩家二级信息",
  "权益/资本",
  "背后控股股东",
  "股权变更时间",
  "Mandiri Utama Finance",
  "WOM Finance",
  "Akulaku Finance Indonesia",
];

for (const text of multiFinanceMarkers) {
  if (!html.includes(text)) {
    throw new Error(`Missing multi-finance player marker: ${text}`);
  }
}

const p2pMarkers = [
  "P2P 竞争对手目录",
  "function renderP2PDirectory",
  "function p2pPlayerPage",
  'href="#license/${esc(item.id)}/${esc(p2pPlayerSlug(player))}"',
  'hash.match(/^license\\/p2p\\/([^/]+)$/)',
  "P2P 玩家二级信息",
  "查看二级信息",
  "资本/权益",
  "背后控股股东",
  "股权变更时间",
  "独立消费信贷平台",
  "互联网生态型平台",
  "生产性及 UMKM 融资平台",
  "Sharia 专业平台",
  "Rupiah Cepat",
  "Asetku",
  "Akseleran",
  "Alami",
];

for (const text of p2pMarkers) {
  if (!html.includes(text)) {
    throw new Error(`Missing P2P competitor marker: ${text}`);
  }
}

const licensesMatch = html.match(/const LICENSES = (\[.*?\]);/s);
if (!licensesMatch) {
  throw new Error("Cannot find generated license data");
}

const licenses = JSON.parse(licensesMatch[1]);
const commercialBank = licenses.find((item) => item.id === "commercial-bank");
const multiFinance = licenses.find((item) => item.id === "multi-finance");
const p2p = licenses.find((item) => item.id === "p2p");
const commercialBanks = (commercialBank.bankDirectory || []).flatMap((group) => group.banks || []);
if (commercialBanks.length < 40) {
  throw new Error("Commercial bank directory lost bank rows");
}

const multiFinanceCompetitors = multiFinance?.competitors || [];
if (multiFinanceCompetitors.length < 10) {
  throw new Error("Multi-Finance player directory lost competitor rows");
}

for (const name of ["Mandiri Utama Finance", "WOM Finance", "Akulaku Finance Indonesia"]) {
  if (!multiFinanceCompetitors.some((player) => player.name === name)) {
    throw new Error(`Multi-Finance player missing: ${name}`);
  }
}

const multiFinanceRowsMissingDetailFields = multiFinanceCompetitors.filter((player) =>
  ["assets", "equityCapital", "marketCap", "controllingShareholder", "controlChangeTime"].some((field) => !player[field])
);
if (multiFinanceRowsMissingDetailFields.length > 0) {
  throw new Error(
    `Multi-Finance players missing second-level detail fields: ${multiFinanceRowsMissingDetailFields
      .map((player) => player.name)
      .join(", ")}`
  );
}

const multiFinanceRowsWithoutSources = multiFinanceCompetitors.filter(
  (player) => !Array.isArray(player.sources) || player.sources.length === 0
);
if (multiFinanceRowsWithoutSources.length > 0) {
  throw new Error(
    `Multi-Finance players missing sources: ${multiFinanceRowsWithoutSources
      .map((player) => player.name)
      .join(", ")}`
  );
}

const p2pCompetitors = p2p?.competitors || [];
if (p2pCompetitors.length < 20) {
  throw new Error("P2P competitor directory lost representative players");
}

for (const name of ["Rupiah Cepat", "Asetku", "KrediFazz", "AwanTunai", "BATUMBU", "Akseleran", "Alami", "Ethis"]) {
  if (!p2pCompetitors.some((player) => player.name === name)) {
    throw new Error(`P2P representative player missing: ${name}`);
  }
}

const p2pRowsMissingDetailFields = p2pCompetitors.filter((player) =>
  ["assets", "equityCapital", "marketCap", "controllingShareholder", "controlChangeTime"].some((field) => !player[field])
);
if (p2pRowsMissingDetailFields.length > 0) {
  throw new Error(
    `P2P players missing second-level detail fields: ${p2pRowsMissingDetailFields
      .map((player) => player.name)
      .join(", ")}`
  );
}

const p2pRowsWithoutSources = p2pCompetitors.filter(
  (player) => !Array.isArray(player.sources) || player.sources.length === 0
);
if (p2pRowsWithoutSources.length > 0) {
  throw new Error(
    `P2P players missing sources: ${p2pRowsWithoutSources
      .map((player) => player.name)
      .join(", ")}`
  );
}

const banksWithoutSources = commercialBanks.filter(
  (bank) => !Array.isArray(bank.sources) || bank.sources.length === 0
);
if (banksWithoutSources.length > 0) {
  throw new Error(`Commercial bank rows missing sources: ${banksWithoutSources.map((bank) => bank.id).join(", ")}`);
}

const unresolvedCommercialBankRows = commercialBanks.filter((bank) =>
  ["assets", "coreCapital", "marketCap", "controlChangeTime"].some((field) =>
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

const banksWithoutControlChange = commercialBanks.filter((bank) => !bank.controlChangeTime);
if (banksWithoutControlChange.length > 0) {
  throw new Error(`Commercial bank rows missing control change time: ${banksWithoutControlChange.map((bank) => bank.id).join(", ")}`);
}

if (html.includes("牌照获批时间")) {
  throw new Error("Commercial bank detail still uses the old license approval label");
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
