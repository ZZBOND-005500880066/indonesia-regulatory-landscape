const fs = require("fs/promises");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const DATA_DIR = path.join(ROOT, "data");
const PUBLIC_DIR = path.join(ROOT, "public");
const DATA_SNAPSHOT = path.join(DATA_DIR, "regulatory-updates.json");
const PUBLIC_SNAPSHOT = path.join(PUBLIC_DIR, "regulatory-updates.json");

const OFFICIAL_SOURCES = [
  {
    id: "ojk-regulasi",
    name: "OJK Regulasi",
    regulator: "OJK",
    url: "https://www.ojk.go.id/id/regulasi/Default.aspx",
  },
  {
    id: "bi-peraturan-default",
    name: "BI Publikasi Peraturan",
    regulator: "BI",
    url: "https://www.bi.go.id/id/publikasi/peraturan/Default.aspx",
  },
  {
    id: "bi-peraturan-pages",
    name: "BI Publikasi Peraturan",
    regulator: "BI",
    url: "https://www.bi.go.id/id/publikasi/peraturan/Pages/default.aspx",
  },
  {
    id: "jdih-bi",
    name: "JDIH Bank Indonesia",
    regulator: "BI",
    url: "https://jdih.bi.go.id/",
  },
];

const LICENSE_KEYWORDS = [
  {
    id: "commercial-bank",
    label: "商业银行",
    keywords: ["bank umum", "bank bhi", "commercial bank", "perbankan", "rasio pendanaan luar negeri bank"],
    impact: "商业银行准入、治理、资本、消费者保护或报送口径可能需要同步更新。",
  },
  {
    id: "multi-finance",
    label: "Multi-Finance",
    keywords: ["perusahaan pembiayaan", "lembaga pembiayaan", "multifinance", "perusahaan modal ventura", "modal ventura"],
    impact: "Multi-Finance 的牌照合规、月报、产品边界、NPF/gearing 或消费者保护要求可能变化。",
  },
  {
    id: "p2p",
    label: "P2P",
    keywords: ["lpbbti", "layanan pendanaan", "pendanaan bersama", "pinjaman online", "pindar", "fintech lending"],
    impact: "P2P/LPBBTI 的融资限额、费用、催收、数据报送或平台治理要求可能需要复核。",
  },
  {
    id: "pjp",
    label: "PJP",
    keywords: ["penyedia jasa pembayaran", "pjp", "qris", "sistem pembayaran", "payment system", "pembayaran"],
    impact: "PJP/QRIS 的业务范围、资金来源、交易处理、风控或技术合规要求可能变化。",
  },
  {
    id: "bpr",
    label: "BPR",
    keywords: ["bank perekonomian rakyat", "bpr", "bprs", "bank perkreditan rakyat"],
    impact: "BPR 收购、补资、核心资本、业务范围或数字化改造路径可能需要重新测算。",
  },
  {
    id: "ics",
    label: "ICS / PKA",
    keywords: ["pemeringkat kredit alternatif", "pka", "credit scoring", "inovasi teknologi sektor keuangan", "itsk"],
    impact: "ICS/PKA 的治理、数据来源、模型解释、信息系统和持续监管要求可能变化。",
  },
  {
    id: "loan-aggregator",
    label: "Loan Aggregator",
    keywords: ["agregasi jasa keuangan", "pajk", "aggregator", "financing agent", "funding agent"],
    impact: "Loan Aggregator/PAJK 的准入、合作金融机构、导流、数据授权或信息安全要求可能变化。",
  },
];

const GENERAL_KEYWORDS = [
  "pojk",
  "seojk",
  "padk",
  "pbi",
  "padg",
  "peraturan bank indonesia",
  "peraturan otoritas jasa keuangan",
  "surat edaran",
  "perlindungan konsumen",
  "pengaduan",
  "anti pencucian uang",
  "manajemen risiko",
  "tata kelola",
  "laporan",
  "perizinan",
  "modal minimum",
  "teknologi informasi",
];

const RULE_SIGNAL = /(pojk|seojk|padk|pbi|padg|peraturan|surat edaran|nomor|tahun|kewajiban|penerapan|ketentuan|laporan|publikasi)/i;

const SEED_BRIEFINGS = [
  {
    date: "2026",
    publishedDate: "2026-01-06",
    title: "BPR 最低资本与核心资本要求更新",
    regulator: "OJK",
    licenses: ["BPR"],
    licenseIds: ["bpr"],
    level: "高",
    summary: "OJK 发布 POJK Nomor 7 Tahun 2026，主题为 Bank Perekonomian Rakyat 的最低资本充足和最低核心资本满足要求。",
    impact: "BPR 收购或数字化改造不能只看历史实缴资本和壳价，还要重新核算资本充足、核心资本缺口和后续补资压力。",
    action: "BPR 标的池增加核心资本缺口、资本充足率、历史利润留存、股东补资能力和 OJK 资本整改要求字段。",
    keywords: "POJK Nomor 7 Tahun 2026 Kewajiban Penyediaan Modal Minimum Pemenuhan Modal Inti Minimum Bank Perekonomian Rakyat",
    sourceLabel: "OJK 官方法规页",
    sourceUrl: "https://www.ojk.go.id/id/regulasi/Pages/POJK-Nomor-7-Tahun-2026-Kewajiban-Penyediaan-Modal-Minimum-dan-Pemenuhan-Modal-Inti-Minimum-Bank-Perekonomian-Rakyat.aspx",
    sourceAltLabel: "备用：OJK 站内检索",
    sourceAltUrl: "https://www.ojk.go.id/id/regulasi/_layouts/15/osssearchresults.aspx?u=https%3A%2F%2Fwww.ojk.go.id%2Fid%2Fregulasi&k=Kewajiban%20Penyediaan%20Modal%20Minimum%20Bank%20Perekonomian%20Rakyat",
  },
  {
    date: "2026",
    publishedDate: "2025-12-26",
    title: "ITSK 经营者治理和风险管理规则落地",
    regulator: "OJK",
    licenses: ["ICS / PKA", "Loan Aggregator"],
    licenseIds: ["ics", "loan-aggregator"],
    level: "高",
    summary: "OJK 发布 POJK Nomor 30 Tahun 2025，主题为金融科技创新部门经营者的治理与风险管理。",
    impact: "ICS/PKA、PAJK/Loan Aggregator 等 ITSK 相关主体的准入后监管会更关注董事会责任、风险管理、内控、数据/系统治理和持续合规。",
    action: "申牌或收购时增加治理框架、风险管理制度、信息安全职责、第三方外包管理和董事会监督材料的尽调要求。",
    keywords: "POJK Nomor 30 Tahun 2025 Tata Kelola Manajemen Risiko Penyelenggara Inovasi Teknologi Sektor Keuangan",
    sourceLabel: "OJK 官方法规页",
    sourceUrl: "https://www.ojk.go.id/id/regulasi/Pages/POJK-Nomor-30-Tahun-2025-Penerapan-Tata-Kelola-dan-Manajemen-Risiko-Bagi-Penyelenggara-Inovasi-Teknologi-Sektor-Keuangan.aspx",
    sourceAltLabel: "备用：OJK 站内检索",
    sourceAltUrl: "https://www.ojk.go.id/id/regulasi/_layouts/15/osssearchresults.aspx?u=https%3A%2F%2Fwww.ojk.go.id%2Fid%2Fregulasi&k=Penerapan%20Tata%20Kelola%20Manajemen%20Risiko%20Penyelenggara%20Inovasi%20Teknologi%20Sektor%20Keuangan",
  },
  {
    date: "2025",
    publishedDate: "2025-11-24",
    title: "融资公司月度报告规则更新",
    regulator: "OJK",
    licenses: ["Multi-Finance"],
    licenseIds: ["multi-finance"],
    level: "中",
    summary: "OJK 发布 PADK 45/PADK.06/2025，主题为普通融资公司和伊斯兰融资公司的月度报告。",
    impact: "Multi-Finance 的监管报送频率、字段完整性和口径一致性会成为合规重点，收购存量公司时需要核验历史月报质量和整改记录。",
    action: "尽调要求目标公司提供近 24 个月月报、OJK 回执、补正记录、NPF/gearing 报送口径和核心业务分项数据。",
    keywords: "45/PADK.06/2025 Laporan Bulanan Perusahaan Pembiayaan Perusahaan Pembiayaan Syariah",
    sourceLabel: "OJK 官方法规页",
    sourceUrl: "https://www.ojk.go.id/id/regulasi/Pages/PADK-45-PADK06-2025-Laporan-Bulanan-Perusahaan-Pembiayaan-dan-Perusahaan-Pembiayaan-Syariah.aspx",
  },
  {
    date: "2025",
    publishedDate: "2025-10-23",
    title: "投诉处理公开与投诉服务报告规则更新",
    regulator: "OJK",
    licenses: ["商业银行", "BPR", "Multi-Finance", "P2P", "ICS / PKA", "Loan Aggregator"],
    licenseIds: ["commercial-bank", "bpr", "multi-finance", "p2p", "ics", "loan-aggregator"],
    level: "中",
    summary: "OJK 发布 SEOJK 20/SEOJK.08/2025，主题为投诉处理公开和投诉服务报告。",
    impact: "面向消费者的银行、BPR、融资公司、P2P、金融科技聚合/评分服务都需要关注投诉披露、服务报告和消费者保护留痕。",
    action: "为各牌照子页面增加消费者投诉合规核查项：投诉 SLA、公开披露、定期报告、工单留痕、催收投诉和外包投诉管理。",
    keywords: "20/SEOJK.08/2025 Publikasi Penanganan Pengaduan Laporan Layanan Pengaduan",
    sourceLabel: "OJK 官方法规页",
    sourceUrl: "https://www.ojk.go.id/id/regulasi/Pages/SEOJK-20-SEOJK08-2025-Publikasi-Penanganan-Pengaduan-dan-Laporan-Layanan-Pengaduan.aspx",
  },
];

function localDateStamp(date = new Date()) {
  const offset = date.getTimezoneOffset() * 60000;
  return new Date(date.getTime() - offset).toISOString().slice(0, 10);
}

function decodeEntities(value) {
  return String(value || "")
    .replace(/&#(\d+);/g, (_, code) => String.fromCharCode(Number(code)))
    .replace(/&#x([a-f0-9]+);/gi, (_, code) => String.fromCharCode(parseInt(code, 16)))
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/g, "'")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">");
}

function cleanText(value) {
  return decodeEntities(value)
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

const MONTHS = {
  januari: 1,
  january: 1,
  jan: 1,
  februari: 2,
  february: 2,
  feb: 2,
  maret: 3,
  march: 3,
  mar: 3,
  april: 4,
  apr: 4,
  mei: 5,
  may: 5,
  juni: 6,
  june: 6,
  jun: 6,
  juli: 7,
  july: 7,
  jul: 7,
  agustus: 8,
  august: 8,
  aug: 8,
  september: 9,
  sep: 9,
  oktober: 10,
  october: 10,
  oct: 10,
  november: 11,
  nov: 11,
  desember: 12,
  december: 12,
  dec: 12,
};

function pad2(value) {
  return String(value).padStart(2, "0");
}

function isoDate(year, month, day) {
  if (!year || !month || !day) return null;
  if (month < 1 || month > 12 || day < 1 || day > 31) return null;
  return `${year}-${pad2(month)}-${pad2(day)}`;
}

function extractPublishedDate(...parts) {
  const text = parts.filter(Boolean).join(" ");
  let match = text.match(/\b(20[2-4][0-9])[-/.](0?[1-9]|1[0-2])[-/.](0?[1-9]|[12][0-9]|3[01])\b/);
  if (match) return isoDate(Number(match[1]), Number(match[2]), Number(match[3]));

  match = text.match(/\b(0?[1-9]|[12][0-9]|3[01])\s+([A-Za-z]+|Januari|Februari|Maret|Mei|Juni|Juli|Agustus|Oktober|Desember)\s+(20[2-4][0-9])\b/i);
  if (match) {
    const month = MONTHS[match[2].toLowerCase()];
    if (month) return isoDate(Number(match[3]), month, Number(match[1]));
  }

  match = text.match(/\b([A-Za-z]+|Januari|Februari|Maret|Mei|Juni|Juli|Agustus|Oktober|Desember)\s+(0?[1-9]|[12][0-9]|3[01]),?\s+(20[2-4][0-9])\b/i);
  if (match) {
    const month = MONTHS[match[1].toLowerCase()];
    if (month) return isoDate(Number(match[3]), month, Number(match[2]));
  }

  match = text.match(/\b(0?[1-9]|1[0-2])[/-](0?[1-9]|[12][0-9]|3[01])[/-](20[2-4][0-9])\b/);
  if (match) return isoDate(Number(match[3]), Number(match[1]), Number(match[2]));

  match = text.match(/\b(0?[1-9]|[12][0-9]|3[01])[/-](0?[1-9]|1[0-2])[/-](20[2-4][0-9])\b/);
  if (match) return isoDate(Number(match[3]), Number(match[2]), Number(match[1]));

  return null;
}

function includesAny(text, keywords) {
  const lower = text.toLowerCase();
  return keywords.filter((keyword) => lower.includes(keyword.toLowerCase()));
}

function classify(text) {
  const matched = [];
  const ids = [];
  const impacts = [];
  for (const license of LICENSE_KEYWORDS) {
    const hits = includesAny(text, license.keywords);
    if (hits.length) {
      matched.push(license.label);
      ids.push(license.id);
      impacts.push(license.impact);
    }
  }
  return { labels: [...new Set(matched)], ids: [...new Set(ids)], impacts };
}

function extractAnchors(html, baseUrl) {
  const anchors = [];
  const re = /<a\b[^>]*href\s*=\s*(["'])(.*?)\1[^>]*>([\s\S]*?)<\/a>/gi;
  for (const match of html.matchAll(re)) {
    const href = decodeEntities(match[2]).trim();
    if (!href || href.startsWith("#") || /^javascript:/i.test(href) || /^mailto:/i.test(href)) continue;
    const title = cleanText(match[3]);
    if (!title || title.length < 8) continue;
    if (title.length > 240) continue;
    let url;
    try {
      url = new URL(href, baseUrl).href;
    } catch {
      continue;
    }
    const contextStart = Math.max(0, match.index - 500);
    const contextEnd = Math.min(html.length, match.index + match[0].length + 900);
    const context = cleanText(html.slice(contextStart, contextEnd));
    anchors.push({
      title,
      url,
      context,
      publishedDate: extractPublishedDate(title, url, context),
    });
  }
  return anchors;
}

function extractYear(text) {
  const years = [...String(text).matchAll(/\b(20[2-4][0-9])\b/g)].map((m) => Number(m[1]));
  return years.length ? String(Math.max(...years)) : localDateStamp();
}

function scoreCandidate(entry, source) {
  const combined = `${entry.title} ${entry.url}`;
  if (!isRegulatoryCandidate(entry, source)) {
    return { score: -100, generalHits: [], classified: { labels: [], ids: [], impacts: [] } };
  }
  const generalHits = includesAny(combined, GENERAL_KEYWORDS);
  const classified = classify(combined);
  const year = Number(extractYear(combined).slice(0, 4));
  let score = generalHits.length * 2 + classified.labels.length * 6;
  if (/\/regulasi\//i.test(entry.url) || /peraturan/i.test(entry.url)) score += 2;
  if (source.regulator === "BI" && /qris|pjp|pembayaran|sistem pembayaran|pbi|padg/i.test(combined)) score += 4;
  if (year >= 2026) score += 4;
  if (year === 2025) score += 2;
  if (/facebook|twitter|instagram|linkedin|youtube|whatsapp|rss|login|search/i.test(combined)) score -= 20;
  return { score, generalHits, classified };
}

function isRegulatoryCandidate(entry, source) {
  const combined = `${entry.title} ${entry.url}`;
  const url = entry.url.toLowerCase();
  if (/tentang-ojk|data-dan-statistik|daftar-alamat|visi-misi|karir|kontak|sosial-media|kanal\//i.test(url)) {
    return false;
  }
  if (source.id.startsWith("ojk-regulasi")) {
    return url.includes("/id/regulasi/pages/") && RULE_SIGNAL.test(combined);
  }
  if (source.id.startsWith("bi-peraturan")) {
    return url.includes("/id/publikasi/peraturan/") && RULE_SIGNAL.test(combined);
  }
  if (source.id === "jdih-bi") {
    return /jdih\.bi\.go\.id/i.test(url) && RULE_SIGNAL.test(combined);
  }
  if (source.id.startsWith("ojk-siaran")) {
    return /siaran-pers/i.test(url) && RULE_SIGNAL.test(combined);
  }
  return RULE_SIGNAL.test(combined);
}

function titleForBriefing(title) {
  return title.length > 72 ? `${title.slice(0, 69)}...` : title;
}

function regulationCode(title, url) {
  const text = `${title} ${url}`;
  let match = text.match(/PADG[_-]?(\d{1,2})(20\d{2})/i);
  if (match) return `PADG ${Number(match[1])}/${match[2]}`;
  match = text.match(/POJK(?:-Nomor)?[-\s]*(\d+)[-\s]*(?:Tahun[-\s]*)?(20\d{2})/i);
  if (match) return `POJK ${Number(match[1])}/${match[2]}`;
  match = text.match(/SEOJK[-\s]*(\d+)[-\s]*SEOJK(\d{2})[-\s]*(20\d{2})/i);
  if (match) return `SEOJK ${Number(match[1])}/SEOJK.${match[2]}/${match[3]}`;
  match = text.match(/PADK[-\s]*(\d+)[-\s]*PADK(\d{2})[-\s]*(20\d{2})/i);
  if (match) return `PADK ${Number(match[1])}/PADK.${match[2]}/${match[3]}`;
  match = text.match(/PADK[-\s]*(\d+)[-\s]*(?:Tahun[-\s]*)?(20\d{2})/i);
  if (match) return `PADK ${Number(match[1])}/${match[2]}`;
  match = title.match(/Nomor\s+(\d+)\s+Tahun\s+(20\d{2})/i);
  if (match) return `${Number(match[1])}/${match[2]}`;
  return null;
}

function amendmentText(title) {
  if (/Perubahan\s+Ketiga/i.test(title)) return "第三次修订";
  if (/Perubahan\s+Kedua/i.test(title)) return "第二次修订";
  if (/Perubahan\s+Pertama/i.test(title)) return "第一次修订";
  if (/Perubahan\s+Atas/i.test(title)) return "修订";
  return null;
}

function translatedTopic(title) {
  const rules = [
    [/Devisa Hasil Ekspor dan Devisa Pembayaran Impor/i, "出口收入外汇与进口付款外汇"],
    [/Peraturan Pelaksanaan Rasio Pendanaan Luar Negeri Bank/i, "银行境外融资比率实施规则"],
    [/Laporan Bulanan Perusahaan Modal Ventura dan Perusahaan Modal Ventura Syariah/i, "风险投资公司及伊斯兰风险投资公司月度报告"],
    [/Laporan Bulanan Perusahaan Pembiayaan dan Perusahaan Pembiayaan Syariah/i, "融资公司及伊斯兰融资公司月度报告"],
    [/Penerapan Tata Kelola dan Manajemen Risiko Bagi Penyelenggara Inovasi Teknologi Sektor Keuangan/i, "金融科技创新经营者治理和风险管理"],
    [/Kewajiban Penyediaan Modal Minimum dan Pemenuhan Modal Inti Minimum Bank Perekonomian Rakyat/i, "BPR 最低资本充足与最低核心资本"],
    [/Publikasi Penanganan Pengaduan dan Laporan Layanan Pengaduan/i, "投诉处理公开与投诉服务报告"],
    [/Pedoman Penerapan Program Anti Pencucian Uang/i, "反洗钱、反恐融资和防扩散融资实施指引"],
  ];
  for (const [pattern, label] of rules) {
    if (pattern.test(title)) return label;
  }
  return cleanText(title)
    .replace(/^Peraturan Anggota Dewan Gubernur\s+Nomor\s+\d+\s+Tahun\s+\d+\s+tentang\s+/i, "")
    .replace(/^Perubahan\s+(Ketiga|Kedua|Pertama)?\s*atas\s+/i, "")
    .replace(/^Penerapan\s+/i, "")
    .replace(/\s+/g, " ")
    .trim();
}

function localizedRegulation(entry, source) {
  const code = regulationCode(entry.title, entry.url);
  const topic = translatedTopic(entry.title);
  const amendment = amendmentText(entry.title);
  const title = [code, amendment ? `${topic}${amendment}` : topic].filter(Boolean).join("：");
  const agency = source.regulator === "BI" ? "BI" : "OJK";
  const verb = amendment ? `${amendment}了` : "发布了";

  return {
    code,
    topic,
    amendment,
    title: title || titleForBriefing(entry.title),
    summary: code
      ? `${agency} ${verb} ${code}，规则主题是${topic}。`
      : `${agency} 发布监管规则，主题是${topic}。`,
  };
}

function polishedImpact(entry, labels, fallbackImpact) {
  const title = entry.title;
  if (/Devisa Hasil Ekspor dan Devisa Pembayaran Impor/i.test(title)) {
    return "这项规则和出口商、进口商的外汇资金处理有关，也会影响银行及跨境支付链路中的外汇入账、结算和合规校验。";
  }
  if (/Rasio Pendanaan Luar Negeri Bank/i.test(title)) {
    return "这项规则影响银行境外融资比例的执行口径，做商业银行收购、外债融资安排或银行合作时需要复核资金来源和比例约束。";
  }
  if (/Laporan Bulanan Perusahaan Modal Ventura/i.test(title)) {
    return "这项规则聚焦风险投资公司月度报送，和 PVML 体系下的报表口径、数据完整性和历史补正风险有关。";
  }
  if (/Laporan Bulanan Perusahaan Pembiayaan/i.test(title)) {
    return "这项规则会影响融资公司月报的字段、频率和口径一致性，收购或申牌时要重点看历史报送质量。";
  }
  if (/Tata Kelola dan Manajemen Risiko/i.test(title)) {
    return "这项规则把 ITSK 经营者的治理、风险管理、内控和系统责任放到更明确的监管框架里，ICS/PAJK 等主体都需要纳入准入后合规清单。";
  }
  if (/Modal Minimum|Modal Inti Minimum/i.test(title)) {
    return "这项规则直接影响 BPR 资本缺口测算，收购估值不能只看壳价，还要把补资和核心资本压力算进去。";
  }
  if (/Penanganan Pengaduan|Layanan Pengaduan/i.test(title)) {
    return "这项规则强化投诉披露和服务报告，对面向消费者的银行、融资、P2P、聚合和数据类服务都有合规留痕要求。";
  }
  if (/Anti Pencucian Uang/i.test(title)) {
    return "这项规则补强 AML/CFT/CPF 执行口径，涉及客户识别、交易监测、可疑活动处理和合规报告。";
  }
  return fallbackImpact || `这项规则可能影响${labels.join("、")}的准入、报送、风控或持续合规。`;
}

function polishedAction(entry) {
  const title = entry.title;
  if (/Devisa Hasil Ekspor|Rasio Pendanaan Luar Negeri Bank/i.test(title)) {
    return "把原文加入 PJP/商业银行法规索引；涉及跨境收付款、外汇入账或银行资金安排的产品，先复核银行侧规则和合同分工。";
  }
  if (/Laporan Bulanan/i.test(title)) {
    return "尽调时要求目标公司提供近 24 个月报送文件、OJK/BI 回执、补正记录和内部报表口径说明。";
  }
  if (/Tata Kelola|Manajemen Risiko/i.test(title)) {
    return "申牌或收购材料中补齐董事会职责、风险管理制度、信息安全职责、外包管理和持续合规机制。";
  }
  if (/Modal Minimum|Modal Inti Minimum/i.test(title)) {
    return "更新 BPR 标的池字段，加入核心资本缺口、补资时间表、股东补资能力和监管整改记录。";
  }
  if (/Penanganan Pengaduan|Layanan Pengaduan/i.test(title)) {
    return "补充投诉 SLA、公开披露、定期报告、工单留痕、催收投诉和外包投诉管理检查项。";
  }
  return "把原文加入对应牌照法规索引，并在准入、收购、产品上线和持续合规清单中复核影响。";
}

function makeBriefing(candidate, nowIso) {
  const { entry, source, scoreInfo } = candidate;
  const labels = scoreInfo.classified.labels.length ? scoreInfo.classified.labels : ["跨牌照"];
  const ids = scoreInfo.classified.ids;
  const keywords = [...new Set([...scoreInfo.generalHits, ...labels])].join(", ");
  const fallbackImpact = scoreInfo.classified.impacts.length
    ? scoreInfo.classified.impacts.join(" ")
    : "该条目可能影响金融机构通用治理、报送、消费者保护、风控或许可流程。";
  const localized = localizedRegulation(entry, source);
  const impact = polishedImpact(entry, labels, fallbackImpact);
  const level = labels.length >= 2 || /modal|manajemen risiko|tata kelola|perlindungan konsumen|qris|pembayaran/i.test(entry.title)
    ? "高"
    : "中";

  return {
    date: extractYear(`${entry.title} ${entry.url}`),
    publishedDate: entry.publishedDate || extractPublishedDate(entry.title, entry.url, entry.context),
    title: titleForBriefing(localized.title),
    regulator: source.regulator,
    licenses: labels,
    licenseIds: ids,
    level,
    summary: localized.summary,
    impact,
    action: polishedAction(entry),
    keywords: keywords || entry.title,
    sourceLabel: source.name,
    sourceUrl: entry.url,
    sourceOriginalTitle: entry.title,
    sourceStatus: `每日更新器于 ${nowIso} 联网抓取；来源入口 HTTP 200。`,
  };
}

function mergeWithSeeds(briefings, nowIso) {
  const seen = new Set(briefings.map((item) => item.sourceUrl || item.title));
  const merged = [...briefings];
  for (const seed of SEED_BRIEFINGS) {
    if (seen.has(seed.sourceUrl)) continue;
    merged.push({
      ...seed,
      sourceStatus: `基准快照保留；每日更新器于 ${nowIso} 运行后未发现可替代的更新条目。`,
    });
    if (merged.length >= 8) break;
  }
  return merged;
}

function buildLicenseUpdates(briefings) {
  const updates = {};
  for (const item of briefings) {
    const ids = item.licenseIds || [];
    for (const id of ids) {
      if (!updates[id]) updates[id] = [];
      updates[id].push({
        name: item.title,
        publishedDate: item.publishedDate,
        note: `${item.summary} ${item.impact}`,
        sourceUrl: item.sourceUrl,
      });
    }
  }
  return updates;
}

async function fetchSource(source) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), Number(process.env.FETCH_TIMEOUT_MS || 18000));
  try {
    const res = await fetch(source.url, {
      signal: controller.signal,
      headers: {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "id-ID,id;q=0.9,en;q=0.8,zh-CN;q=0.6",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 regulatory-monitor/1.0",
      },
      redirect: "follow",
    });
    const text = await res.text();
    return { ok: res.ok, status: res.status, finalUrl: res.url, text };
  } finally {
    clearTimeout(timeout);
  }
}

async function buildSnapshot({ reason = "manual" } = {}) {
  const nowIso = new Date().toISOString();
  const candidates = [];

  const sourceResults = await Promise.all(OFFICIAL_SOURCES.map(async (source) => {
    try {
      const result = await fetchSource(source);
      const anchors = result.ok ? extractAnchors(result.text, result.finalUrl || source.url) : [];
      const matchedCandidates = [];
      for (const entry of anchors) {
        const scoreInfo = scoreCandidate(entry, source);
        if (scoreInfo.score < 7) continue;
        matchedCandidates.push({ entry, source, scoreInfo, score: scoreInfo.score });
      }
      return {
        candidates: matchedCandidates,
        checked: {
          id: source.id,
          name: source.name,
          regulator: source.regulator,
          url: source.url,
          ok: result.ok,
          status: result.status,
          itemsFound: anchors.length,
          matchedItems: matchedCandidates.length,
        },
      };
    } catch (error) {
      return {
        candidates: [],
        checked: {
        id: source.id,
        name: source.name,
        regulator: source.regulator,
        url: source.url,
        ok: false,
        status: "FETCH_ERROR",
        error: error && error.message ? error.message : String(error),
        },
      };
    }
  }));

  const sourcesChecked = sourceResults.map((result) => result.checked);
  for (const result of sourceResults) {
    candidates.push(...result.candidates);
  }

  const seen = new Set();
  const briefings = candidates
    .sort((a, b) => b.score - a.score)
    .filter((candidate) => {
      const key = candidate.entry.url || candidate.entry.title;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    })
    .slice(0, 6)
    .map((candidate) => makeBriefing(candidate, nowIso));

  const finalBriefings = mergeWithSeeds(briefings, nowIso);
  return {
    generatedAt: nowIso,
    generatedDate: localDateStamp(),
    mode: "daily-online-fetch",
    reason,
    sourcesChecked,
    briefings: finalBriefings,
    licenses: buildLicenseUpdates(finalBriefings),
    diagnostics: {
      candidates: candidates.length,
      generatedBriefings: briefings.length,
      fallbackBriefings: finalBriefings.length - briefings.length,
    },
  };
}

async function writeSnapshot(snapshot) {
  await fs.mkdir(DATA_DIR, { recursive: true });
  await fs.mkdir(PUBLIC_DIR, { recursive: true });
  const body = `${JSON.stringify(snapshot, null, 2)}\n`;
  await fs.writeFile(DATA_SNAPSHOT, body, "utf8");
  await fs.writeFile(PUBLIC_SNAPSHOT, body, "utf8");
}

async function refreshRegulatoryData(options = {}) {
  const snapshot = await buildSnapshot(options);
  await writeSnapshot(snapshot);
  return snapshot;
}

if (require.main === module) {
  refreshRegulatoryData({ reason: process.argv[2] || "manual" })
    .then((snapshot) => {
      const okCount = snapshot.sourcesChecked.filter((source) => source.ok).length;
      console.log(`Updated regulatory snapshot: ${snapshot.briefings.length} briefings, ${okCount}/${snapshot.sourcesChecked.length} sources ok`);
      console.log(PUBLIC_SNAPSHOT);
    })
    .catch((error) => {
      console.error(error);
      process.exit(1);
    });
}

module.exports = {
  refreshRegulatoryData,
  buildSnapshot,
  paths: {
    dataSnapshot: DATA_SNAPSHOT,
    publicSnapshot: PUBLIC_SNAPSHOT,
  },
};
