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

const pjpMarkers = [
  "PJP 玩家目录",
  "function renderPJPDirectory",
  "function pjpPlayerPage",
  'href="#license/${esc(item.id)}/${esc(pjpPlayerSlug(player))}"',
  'hash.match(/^license\\/pjp\\/([^/]+)$/)',
  "PJP 玩家二级信息",
  "资产/公开规模",
  "股权/牌照变更时间",
  "市值只按牌照主体本身是否上市判断",
  "生态钱包和高频支付入口",
  "支付网关和企业收单",
  "低活跃 PJP1 / 收购观察标的",
  "PT Hensel Davest Indonesia",
  "PT Reka Multi Aptika",
  "PT Yukk Kreasi Indonesia",
];

for (const text of pjpMarkers) {
  if (!html.includes(text)) {
    throw new Error(`Missing PJP player marker: ${text}`);
  }
}

const bprMarkers = [
  "BPR 玩家目录",
  "function renderBPRDirectory",
  "function bprPlayerPage",
  'href="#license/${esc(item.id)}/${esc(bprPlayerSlug(player))}"',
  'hash.match(/^license\\/bpr\\/([^/]+)$/)',
  "BPR 玩家二级信息",
  "资产/公开规模",
  "资本/核心资本",
  "股权/控股变更时间",
  "平台化与数字化 BPR/BPRS 路径",
  "规模型传统与区域 BPR",
  "支付合作、移动银行与合并样本",
  "Komunal / DepositoBPR",
  "Alami / Bank Hijra",
  "Bank Eka",
  "BPR Lestari",
  "BPR Modern Express",
  "BPR Hasamitra",
  "BPR BK Jateng",
  "BPR Karyajatnika Sadaya",
  "Universal BPR",
];

for (const text of bprMarkers) {
  if (!html.includes(text)) {
    throw new Error(`Missing BPR player marker: ${text}`);
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
const pjp = licenses.find((item) => item.id === "pjp");
const bpr = licenses.find((item) => item.id === "bpr");
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

const pjpCompetitors = pjp?.competitors || [];
if (pjpCompetitors.length < 19) {
  throw new Error("PJP player directory lost representative players");
}

for (const name of [
  "GoPay",
  "OVO",
  "DANA",
  "ShopeePay",
  "Xendit",
  "DOKU",
  "Payfazz",
  "Finture / YUP",
  "Airwallex",
  "PT Hensel Davest Indonesia",
  "PT Reformasi Uang Pembayaran Indonesia",
  "PT Anadana Kode Nontunai",
  "PT Reka Multi Aptika",
  "PT Fasa Centra Artajaya",
  "PT Ayopop Teknologi Indonesia",
  "PT Honest Financial Technologies",
  "PT Max Interactives Technologies",
  "PT Jatelindo Perkasa Abadi",
  "PT Yukk Kreasi Indonesia",
]) {
  if (!pjpCompetitors.some((player) => player.name === name)) {
    throw new Error(`PJP representative player missing: ${name}`);
  }
}

const pjpRowsMissingDetailFields = pjpCompetitors.filter((player) =>
  ["assets", "equityCapital", "marketCap", "controllingShareholder", "controlChangeTime"].some((field) => !player[field])
);
if (pjpRowsMissingDetailFields.length > 0) {
  throw new Error(
    `PJP players missing second-level detail fields: ${pjpRowsMissingDetailFields
      .map((player) => player.name)
      .join(", ")}`
  );
}

const pjpRowsWithoutSources = pjpCompetitors.filter(
  (player) => !Array.isArray(player.sources) || player.sources.length === 0
);
if (pjpRowsWithoutSources.length > 0) {
  throw new Error(
    `PJP players missing sources: ${pjpRowsWithoutSources
      .map((player) => player.name)
      .join(", ")}`
  );
}

const bprCompetitors = bpr?.competitors || [];
if (bprCompetitors.length < 9) {
  throw new Error("BPR player directory lost PDF-listed representative rows");
}

for (const name of [
  "Komunal / DepositoBPR",
  "Alami / Bank Hijra",
  "Bank Eka",
  "BPR Lestari",
  "BPR Modern Express",
  "BPR Hasamitra",
  "BPR BK Jateng",
  "BPR Karyajatnika Sadaya",
  "Universal BPR",
]) {
  if (!bprCompetitors.some((player) => player.name === name)) {
    throw new Error(`BPR representative player missing: ${name}`);
  }
}

const bprRowsMissingDetailFields = bprCompetitors.filter((player) =>
  ["assets", "marketCap", "controllingShareholder", "controlChangeTime"].some((field) => !player[field]) ||
  !(player.equityCapital || player.coreCapital)
);
if (bprRowsMissingDetailFields.length > 0) {
  throw new Error(
    `BPR players missing second-level detail fields: ${bprRowsMissingDetailFields
      .map((player) => player.name)
      .join(", ")}`
  );
}

const bprRowsWithoutSources = bprCompetitors.filter(
  (player) => !Array.isArray(player.sources) || player.sources.length === 0
);
if (bprRowsWithoutSources.length > 0) {
  throw new Error(
    `BPR players missing sources: ${bprRowsWithoutSources
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
