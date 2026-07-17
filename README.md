# Indonesia Regulatory Landscape

这个项目用于展示“印尼核心金融牌照监管机构图景”，覆盖商业银行、Multi-Finance、P2P、PJP、BPR、ICS/PKA、Loan Aggregator，并提供每日监管简报快照。

## 在线部署方式

推荐部署到 GitHub Pages。仓库已经包含 `.github/workflows/deploy-pages.yml`：

- 每天 `00:30 UTC` 自动运行一次，相当于中国时间 `08:30`。
- 自动抓取 OJK / BI / JDIH BI 官方入口。
- 自动生成 `public/regulatory-updates.json`、`public/developer-log.json` 和 `public/index.html`。
- 自动把 `public/` 发布到 GitHub Pages。
- 支持手动触发：GitHub 仓库页面进入 `Actions`，选择 `Deploy Indonesia Regulatory Landscape`，点击 `Run workflow`。

GitHub Pages 需要在仓库设置里启用：

1. 进入 GitHub 仓库的 `Settings`。
2. 打开 `Pages`。
3. `Build and deployment` 选择 `GitHub Actions`。
4. 推送代码到 `main` 或 `master` 后，等待 Actions 完成部署。

部署完成后，GitHub 会给出一个固定链接，其他人可以直接访问。你的电脑不需要保持开机。

## 本地预览

```powershell
node server.js
```

默认地址：

```text
http://localhost:4173
```

常用模块：

```text
http://localhost:4173/#module/regulators
http://localhost:4173/#module/licenses
http://localhost:4173/#module/compare
http://localhost:4173/#module/updates
http://localhost:4173/#module/developer-log
```

## 本地手动更新

只刷新监管简报：

```powershell
node work/update_regulatory_data.js manual
```

刷新监管简报并重新生成页面：

```powershell
npm run build:site
```

只重新生成 HTML：

```powershell
npm run build:html
```

## 静态 HTML 备用文件

如果只想把一个文件发给别人，不依赖网站服务，可以使用：

```text
outputs/indonesia_financial_regulatory_landscape_static.html
```

这个文件已经内嵌监管简报快照和开发者日志，可以直接打开。但它不会自动联网更新；需要重新运行构建后再分发新文件。

## 主要文件

- `public/index.html`：线上站点入口。
- `public/regulatory-updates.json`：页面读取的每日监管简报快照。
- `public/developer-log.json`：开发者日志数据。
- `work/update_regulatory_data.js`：官方入口抓取与简报生成器。
- `work/build_indonesia_dashboard.py`：HTML 生成器。
- `server.js`：本地预览服务和本地每日刷新服务。
- `.github/workflows/deploy-pages.yml`：GitHub Pages 每日自动部署配置。

## 注意事项

GitHub Actions 的定时任务不是实时任务，可能会有延迟。某个官方入口如果当天无法访问，更新器会记录失败诊断，不会硬生成不存在或不相关的简报。
