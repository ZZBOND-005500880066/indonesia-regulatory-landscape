const fs = require("fs");
const fsp = require("fs/promises");
const http = require("http");
const path = require("path");
const { refreshRegulatoryData, paths } = require("./work/update_regulatory_data");

const ROOT = __dirname;
const PUBLIC_DIR = path.join(ROOT, "public");
const PORT = Number(process.env.PORT || 4173);
const UPDATE_HOUR = Number(process.env.UPDATE_HOUR || 8);
const UPDATE_MINUTE = Number(process.env.UPDATE_MINUTE || 30);

let refreshPromise = null;
let lastRefreshError = null;

function localDateStamp(date = new Date()) {
  const offset = date.getTimezoneOffset() * 60000;
  return new Date(date.getTime() - offset).toISOString().slice(0, 10);
}

function contentType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return {
    ".html": "text/html; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
  }[ext] || "application/octet-stream";
}

async function readSnapshotDate() {
  try {
    const raw = await fsp.readFile(paths.publicSnapshot, "utf8");
    const data = JSON.parse(raw);
    return data.generatedDate || String(data.generatedAt || "").slice(0, 10);
  } catch {
    return null;
  }
}

async function triggerRefresh(reason) {
  if (refreshPromise) return refreshPromise;
  refreshPromise = refreshRegulatoryData({ reason })
    .then((snapshot) => {
      lastRefreshError = null;
      return snapshot;
    })
    .catch((error) => {
      lastRefreshError = error && error.message ? error.message : String(error);
      throw error;
    })
    .finally(() => {
      refreshPromise = null;
    });
  return refreshPromise;
}

function msUntilNextRun() {
  const now = new Date();
  const next = new Date(now);
  next.setHours(UPDATE_HOUR, UPDATE_MINUTE, 0, 0);
  if (next <= now) next.setDate(next.getDate() + 1);
  return next.getTime() - now.getTime();
}

function scheduleDailyRefresh() {
  const delay = msUntilNextRun();
  setTimeout(async () => {
    try {
      await triggerRefresh("scheduled-daily");
      console.log(`[regulatory-monitor] daily refresh complete at ${new Date().toISOString()}`);
    } catch (error) {
      console.error("[regulatory-monitor] daily refresh failed", error);
    } finally {
      scheduleDailyRefresh();
    }
  }, delay);
}

async function ensureFreshSnapshot() {
  const snapshotDate = await readSnapshotDate();
  if (snapshotDate !== localDateStamp()) {
    await triggerRefresh("request-stale-cache");
  }
}

function send(res, status, body, type = "text/plain; charset=utf-8") {
  res.writeHead(status, {
    "content-type": type,
    "cache-control": "no-store",
  });
  res.end(body);
}

async function sendFile(res, filePath) {
  try {
    const body = await fsp.readFile(filePath);
    const name = path.basename(filePath);
    res.writeHead(200, {
      "content-type": contentType(filePath),
      "cache-control": name === "regulatory-updates.json" || name === "regulatory-history.json" ? "no-store" : "public, max-age=60",
    });
    res.end(body);
  } catch {
    send(res, 404, "Not found");
  }
}

async function handleUpdates(res) {
  try {
    await ensureFreshSnapshot();
  } catch (error) {
    if (!fs.existsSync(paths.publicSnapshot)) {
      send(res, 502, JSON.stringify({ error: "Unable to refresh regulatory data", detail: String(error) }), "application/json; charset=utf-8");
      return;
    }
  }
  await sendFile(res, paths.publicSnapshot);
}

async function handleHistory(res) {
  try {
    await ensureFreshSnapshot();
  } catch (error) {
    if (!fs.existsSync(paths.publicHistory)) {
      send(res, 502, JSON.stringify({ error: "Unable to refresh regulatory history", detail: String(error) }), "application/json; charset=utf-8");
      return;
    }
  }
  await sendFile(res, paths.publicHistory);
}

async function handleRefresh(res) {
  try {
    const snapshot = await triggerRefresh("manual-api");
    send(res, 200, JSON.stringify(snapshot, null, 2), "application/json; charset=utf-8");
  } catch (error) {
    send(res, 502, JSON.stringify({ error: "Refresh failed", detail: String(error), lastRefreshError }), "application/json; charset=utf-8");
  }
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host || "localhost"}`);
  if (url.pathname === "/regulatory-updates.json" || url.pathname === "/api/regulatory-updates") {
    await handleUpdates(res);
    return;
  }
  if (url.pathname === "/regulatory-history.json" || url.pathname === "/api/regulatory-history") {
    await handleHistory(res);
    return;
  }
  if (url.pathname === "/api/refresh-regulatory-updates") {
    await handleRefresh(res);
    return;
  }

  const safePath = url.pathname === "/" ? "/index.html" : decodeURIComponent(url.pathname);
  const filePath = path.normalize(path.join(PUBLIC_DIR, safePath));
  if (!filePath.startsWith(PUBLIC_DIR)) {
    send(res, 403, "Forbidden");
    return;
  }
  await sendFile(res, filePath);
});

server.listen(PORT, async () => {
  console.log(`Indonesia regulatory landscape site: http://localhost:${PORT}`);
  scheduleDailyRefresh();
  try {
    await triggerRefresh("startup");
    console.log("[regulatory-monitor] startup refresh complete");
  } catch (error) {
    console.error("[regulatory-monitor] startup refresh failed", error);
  }
});
