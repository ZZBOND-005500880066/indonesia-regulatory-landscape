from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "indonesia_financial_regulatory_landscape.html"
STATIC_OUT = ROOT / "outputs" / "indonesia_financial_regulatory_landscape_static.html"
SITE_OUT = ROOT / "public" / "index.html"
DEVLOG_PUBLIC = ROOT / "public" / "developer-log.json"
DEVLOG_DATA = ROOT / "data" / "developer-log.json"
REGULATORY_PUBLIC = ROOT / "public" / "regulatory-updates.json"
REGULATORY_DATA = ROOT / "data" / "regulatory-updates.json"
REGULATORY_HISTORY_PUBLIC = ROOT / "public" / "regulatory-history.json"
REGULATORY_HISTORY_DATA = ROOT / "data" / "regulatory-history.json"


licenses = [
    {
        "id": "commercial-bank",
        "name": "商业银行",
        "subtitle": "Bank Umum / Bank BHI",
        "regulator": "OJK 银行业监管",
        "category": "银行",
        "tone": "core",
        "oneLiner": "印尼金融体系最核心的资金中介，可吸收公众存款、发放贷款并提供支付流通服务。",
        "type": "商业银行牌照，含传统商业银行、伊斯兰商业银行、数字银行化 Bank BHI，以及外国银行分行 KCBLN 等形态。",
        "businessScope": [
            "吸收公众存款，包括活期、储蓄、定期存款和类似存款工具。",
            "发放企业贷款、中小企业贷款、消费贷、车贷、房贷、信用卡及伊斯兰融资。",
            "提供转账汇款、清算结算、借记卡或信用卡、数字银行、商户收单和工资代发等支付结算服务。",
            "开展同业业务、证券交易及投资、外汇、贸易金融、保理、托管和保管箱等业务。",
        ],
        "minCapital": "新设印尼法人商业银行 Bank BHI 原则上最低实缴资本为 Rp10 trillion；原则批准阶段至少提交 40% 实缴资本存款证明。",
        "foreignOwnership": "Bank BHI 可由印尼主体与外国公民或外国法人 partnership 设立；材料口径下外国公民或外国法人持股最高为 99%。外国银行分行 KCBLN 仅适用于符合规模条件的外国银行。",
        "playerCount": "材料口径显示商业银行约 105 家；其中 Bank Umum Persero 国有大行 4 家，Bank Umum Swasta Nasional 67 家，另有外资或区域金融集团背景银行和数字银行。",
        "market": [
            "银行信贷余额 Rp8,755 trillion，第三方存款 DPK Rp10,077 trillion。",
            "贷存比约 84%-85%，CAR 23.97%，Gross NPL 2.17%，ROA 2.46%。",
            "伊斯兰银行资产规模约 Rp1,067.73 trillion。",
        ],
        "restrictions": [
            "不能长期投资普通非金融公司或做产业控股，只能投资法律允许的金融服务机构或因坏账处置临时持股。",
            "不能直接经营保险业务，但可通过 bancassurance 等合规合作代销或协同。",
            "单一借款人或相关借款集团授信上限不得超过银行资本的 30%；特定关联方上限不得超过银行资本的 10%。",
            "须满足 KPMM/CAR、LCR、NSFR、资产质量、RGEC 健康评级、IT、治理、消费者保护和 AML/CFT/CPF 要求。",
        ],
        "competitorLens": [
            {
                "label": "第一层",
                "title": "KBMI 4 大行决定行业上限",
                "note": "BRI、Mandiri、BCA 体量远高于新进入者，核心看低成本资金、网点/企业关系和交易频次。",
            },
            {
                "label": "第二层",
                "title": "区域/外资银行代表入场路径",
                "note": "CIMB、OCBC、UOB、Danamon 更能反映外资通过收购、合并或业务组合进入印尼银行业的打法。",
            },
            {
                "label": "第三层",
                "title": "数字银行更接近产品对标",
                "note": "Jago、Superbank、Saqu 的看点不是绝对资产规模，而是生态获客、存款成本和亏损周期。",
            },
        ],
        "competitors": [
            {
                "name": "BRI",
                "tier": "国有 KBMI 4 大行",
                "scale": "2025 资产 Rp2,135tn；核心资本 Rp302tn",
                "position": "MSME、小微、农村金融和普惠金融",
                "edge": "基层网点、代理网络、政府普惠金融定位和小微信贷数据沉淀。",
                "implication": "不适合正面抢存贷款规模；更适合作为农村金融、普惠金融和小微风控的标杆。",
            },
            {
                "name": "Bank Mandiri",
                "tier": "国有 KBMI 4 大行",
                "scale": "2025 资产 Rp2,830tn；核心资本 Rp304tn",
                "position": "企业银行、批发金融、综合金融",
                "edge": "企业客户、工资代发、集团金融和跨产品综合服务能力强。",
                "implication": "商业银行牌照若走企业端，需要重点比较资金成本、企业关系和综合金融协同。",
            },
            {
                "name": "BCA",
                "tier": "本地财团 KBMI 4 大行",
                "scale": "2025 资产 Rp1,587tn；核心资本 Rp258tn",
                "position": "零售银行、交易银行和低成本存款",
                "edge": "CASA、交易频次、支付体验和高质量零售客户构成核心护城河。",
                "implication": "最值得研究的是低成本存款和交易入口，而不是单纯贷款扩张。",
            },
            {
                "name": "CIMB Niaga / OCBC / UOB / Danamon",
                "tier": "外资或区域集团银行",
                "scale": "中大型银行群；材料未逐一拆分资产口径",
                "position": "区域金融集团在印尼的综合银行平台",
                "edge": "常通过并购、合并和业务组合收购扩张，具备区域客户、资金和管理体系。",
                "implication": "更接近外资入场参考样本；应重点看收购审批、整合成本和存量业务质量。",
            },
            {
                "name": "Bank Jago / Superbank / Bank Saqu",
                "tier": "数字银行及生态型银行",
                "scale": "资产体量低于 KBMI 4；竞争重点在用户、存款和生态转化",
                "position": "App 获客、生态嵌入式金融和数字化存款",
                "edge": "依托股东生态、App 触点和线上产品快速获客，但需控制存款补贴和亏损周期。",
                "implication": "产品与获客最可对标；判断重点是生态流量质量、留存、存款成本和资本消耗。",
            },
        ],
        "latestRules": [
            {"name": "POJK No.12/POJK.03/2021", "note": "商业银行准入、机构形态、资本、股东和经营许可基础规则。"},
            {"name": "POJK No.17/2023", "note": "商业银行公司治理，强化董事会、监事会、委员会、合规和反欺诈。"},
            {"name": "POJK No.11/POJK.03/2022", "note": "商业银行 IT 实施、网络安全、业务连续性、外包和数据保护。"},
            {"name": "POJK No.8/2023", "note": "金融服务领域 AML/CFT/CPF 义务。"},
        ],
        "legalIndex": [
            "Law No.21/2008 on Sharia Banking",
            "POJK No.12/POJK.03/2021 on Commercial Banks",
            "POJK No.40/POJK.03/2019 on Commercial Bank Asset Quality",
            "POJK No.18/POJK.03/2016 on Risk Management",
            "POJK No.4/POJK.03/2016 on Bank Soundness Level",
            "POJK No.17/2023 on Commercial Bank Governance",
            "POJK No.50/POJK.03/2017 on NSFR",
            "POJK No.37/POJK.03/2019 on Transparency and Disclosure",
            "POJK No.11/POJK.03/2022 on IT Implementation",
            "POJK No.22/2023 on Consumer and Public Protection",
            "POJK No.8/2023 on AML/CFT/CPF",
            "Banking Act No.7/1992 and amendments",
        ],
        "sourceDoc": "印尼商业银行研究_202607.pdf",
    },
    {
        "id": "multi-finance",
        "name": "Multi-Finance",
        "subtitle": "Perusahaan Pembiayaan",
        "regulator": "OJK IKNB/PVML",
        "category": "非银融资",
        "tone": "asset",
        "oneLiner": "消费场景、资产场景和小微经营场景中的融资提供者，核心能力在渠道、风控、催收和资产处置。",
        "type": "融资公司或多元融资公司牌照，可为普通融资公司或伊斯兰融资公司。",
        "businessScope": [
            "投资融资，用于企业投资、修复、现代化、扩张或经营地点迁移。",
            "工作资本融资，满足企业一个经营周期内会消耗的支出。",
            "多用途融资，面向个人消费或使用需求提供商品或服务融资。",
            "OJK 批准的其他融资，包括供应链融资、平台场景融资、绿色融资、数字消费金融、BNPL 等。",
            "伊斯兰融资，包括买卖融资、投资融资和服务融资。",
        ],
        "minCapital": "新设融资公司最低实缴资本 Rp250 billion，须现金全额缴入并存放在印尼银行定期存款中。",
        "foreignOwnership": "外资直接或间接持有融资公司比例一般不得超过实缴资本的 85%；上市公司流通股不适用该 85% 限制。临时超限需按 OJK 批准计划最长 3 年内调整。",
        "playerCount": "截至 2026 年 3 月底，融资公司约 144 家，其中 141 家 conventional financing companies，3 家 full-fledged Sharia financing companies；融资机构、风投和基础设施融资公司合计 193 家。",
        "market": [
            "截至 2026 年 5 月，融资公司应收融资余额 Rp513.19 trillion，同比增长 1.71%。",
            "NPL/NPF 压力边际上升：NPF gross 3.06%，NPF net 0.85%。",
            "行业 gearing ratio 为 2.14x，低于监管上限 10x。",
            "2026 年 5 月 BNPL 融资余额同比增长 53.78% 至 Rp13.18 trillion。",
        ],
        "restrictions": [
            "必须取得 OJK 营业许可后经营，OJK 审查股东、PSP、组织架构、业务计划、管理层、风控、合规、IT 和消费者保护。",
            "现金贷和 BNPL 等数字业务需要满足额外条件；材料显示 BNPL 只能由商业银行和融资公司开展，融资公司开展 BNPL 需先获 OJK 批准。",
            "控股股东原则上需已运营至少 2 年，出资不能超过其自身 equity，且资金来源不得来自贷款或金融犯罪。",
            "外籍员工仅限董事、监事、专家或顾问等特定职位；外籍董事或监事存在时，至少 50% 董事和 50% 监事应为印尼公民。",
        ],
        "competitors": [
            {"name": "FIFGROUP", "position": "Astra 体系摩托车和消费金融强势玩家", "signal": "FIFASTRA、SPEKTRA、DANASTRA、FINATRA、AMITRA 覆盖多类融资"},
            {"name": "Adira Finance", "position": "综合型车辆和非车辆融资公司", "signal": "摩托车、汽车、非汽车、多用途、重型设备和伊斯兰融资"},
            {"name": "Astra Credit Companies", "position": "Astra 体系汽车金融平台", "signal": "新车、二手车、fleet、重型设备和多用途融资"},
            {"name": "BFI Finance", "position": "独立综合型融资公司", "signal": "工作资本、投资和多用途融资组合较灵活"},
            {"name": "Home Credit Indonesia", "position": "线下 POS 分期和 App 化消费金融", "signal": "18,842 个 POS，18m+ 注册用户"},
            {"name": "Kredivo Finance Indonesia", "position": "App-based BNPL 和消费分期", "signal": "merchant network、Kredivo App 和两轮电动车融资"},
            {"name": "PT Commerce Finance / SPayLater", "position": "Shopee 生态 paylater", "signal": "覆盖 Shopee 购物、账单票务、QRIS、Limit Xtra 和摩托车分期"},
        ],
        "latestRules": [
            {"name": "POJK No.35/POJK.05/2018", "note": "融资公司业务经营基础规则。"},
            {"name": "POJK No.47/POJK.05/2020", "note": "融资公司牌照和机构设立规则，包含最低资本、外资持股和组织架构。"},
            {"name": "POJK No.46/2024", "note": "融资公司、基础设施融资公司和风险投资公司的发展与强化规则。"},
            {"name": "POJK No.35/2025", "note": "修订 POJK 46/2024，涉及股权变更、证券发行推荐、机动车首付和资本比例调整。"},
        ],
        "legalIndex": [
            "Law No.4/2023 on Financial Sector Development and Strengthening",
            "POJK No.35/POJK.05/2018 on Financing Company Business Activities",
            "POJK No.47/POJK.05/2020 on Financing Company Licensing and Institution",
            "POJK No.46/2024 on Development and Strengthening of Financing Companies, Infrastructure Financing Companies and Venture Capital Companies",
            "POJK No.35/2025 amending POJK No.46/2024",
        ],
        "sourceDoc": "印尼Multi-Finance研究_202607.pdf",
    },
    {
        "id": "p2p",
        "name": "P2P",
        "subtitle": "LPBBTI / Pindar",
        "regulator": "OJK 金融科技融资监管",
        "category": "金融科技融资",
        "tone": "digital",
        "oneLiner": "通过互联网和电子系统撮合资金提供方与资金接收方，可做生产性融资和消费性融资。",
        "type": "Layanan Pendanaan Bersama Berbasis Teknologi Informasi，基于信息技术的共同融资服务。",
        "businessScope": [
            "提供、管理和运营 LPBBTI 撮合系统。",
            "撮合生产性融资，面向企业、个体经营者和 UMKM，覆盖经营周转、供应链融资、发票融资等。",
            "撮合消费性融资，面向个人消费、现金周转和其他非生产性用途。",
            "可采用传统模式，也可采用伊斯兰金融模式。",
        ],
        "minCapital": "新设平台最低实缴资本 Rp25 billion；持续经营期间净资产不得低于 Rp12.5 billion，净资产与实缴资本之比不得低于 50%。",
        "foreignOwnership": "外资直接及间接持股原则上不超过 85%；平台须采用 PT 或合作社形式，并至少指定一名控股股东或实际控制人。",
        "playerCount": "持牌平台数量持续收缩：2023 年 10 月 101 家，2024 年 97 家，2025 年 10 月 96 家，2026 年为 94 家。",
        "market": [
            "截至 2026 年 5 月，行业融资余额 Rp103.73 trillion，同比增长 25.60%。",
            "2021-2025 年融资余额扩大超过三倍，CAGR 约 34.1%。",
            "行业从新增平台数量驱动，转向单平台规模、复借、机构资金和生产性融资驱动。",
        ],
        "restrictions": [
            "单一借款人融资余额通常不超过 Rp2 billion，符合条件的生产性融资可提高至 Rp5 billion。",
            "单一资金方占比原则上不超过 25%。",
            "个人借款人须年满 18 岁或已婚，月均收入不低于 Rp3 million。",
            "综合融资成本按融资类型和期限设定上限，约 0.1%-0.3% 每日。",
            "资金需通过 escrow 和监管认可流程隔离，平台需满足信用评估、数据保护、催收、消费者保护和监管数据接入要求。",
        ],
        "competitors": [
            {"name": "Lentera Dana Nusantara / SPinjam", "position": "Shopee 生态型平台", "signal": "嵌入 Shopee、ShopeePay，覆盖消费者、卖家和商户"},
            {"name": "Easycash", "position": "独立消费现金贷平台", "signal": "累计放款 Rp98.27tn，2026 累计放款 Rp10.28tn"},
            {"name": "AdaKami", "position": "FinVolution 背景个人无抵押现金贷款", "signal": "累计放款约 Rp73.86tn，最近单月放款约 Rp1.60tn"},
            {"name": "Kredit Pintar", "position": "面向未充分服务人群的数字现金贷", "signal": "累计借款人 930 万，活跃借款人约 65 万"},
            {"name": "Amartha", "position": "农村及基层女性微型企业融资", "signal": "累计服务超过 370 万 UMKM，覆盖逾 5 万个村庄"},
            {"name": "Modalku", "position": "SME 营运资金、发票和订单融资", "signal": "累计放款约 Rp9.04tn，TKB90 99.20%"},
            {"name": "JULO", "position": "数字循环额度和虚拟信用卡", "signal": "累计融资额超过 Rp27tn，覆盖约 328 万用户"},
        ],
        "latestRules": [
            {"name": "Law No.4/2023", "note": "LPBBTI 上位法律基础，明确业务范围、法人形式、所有权、资本来源和许可。"},
            {"name": "POJK No.40/2024", "note": "核心监管文件，覆盖股权、最低资本、净资产、融资限额、数据、催收和退出。"},
            {"name": "SEOJK No.19/2025", "note": "借款人与资金方准入、信用评分、费用上限、合同、风险提示和资金流转。"},
            {"name": "PADK No.38/2025", "note": "机构健康度监管，要求至少维持综合评级 3 级。"},
            {"name": "POJK No.8/2026", "note": "融资交易日度数据报送及借款人信息查询机制。"},
        ],
        "legalIndex": [
            "Law No.4/2023 on Financial Sector Development and Strengthening",
            "POJK No.40/2024 on LPBBTI",
            "SEOJK No.19/2025 implementing provisions for LPBBTI",
            "PADK No.38/2025 on LPBBTI health assessment",
            "POJK No.8/2026 on transaction data reporting and borrower information mechanisms",
        ],
        "sourceDoc": "印尼P2P研究.pdf",
    },
    {
        "id": "pjp",
        "name": "PJP",
        "subtitle": "Payment Services Provider / QRIS",
        "regulator": "Bank Indonesia",
        "category": "支付",
        "tone": "payment",
        "oneLiner": "印尼核心电子支付牌照体系，PJP1 可覆盖电子钱包、账户信息、支付发起与收单、汇款，并可叠加 QRIS。",
        "type": "Bank Indonesia 支付服务提供商许可，分 PJP 1、PJP 2、PJP 3；QRIS 是叠加在 PJP/PIP 上的国家二维码支付处理资质。",
        "businessScope": [
            "PJP 1：资金来源管理，包括电子货币和钱包；资金信息提供；支付发起与收单；汇款。",
            "PJP 2：资金信息提供服务，以及支付发起与收单。",
            "PJP 3：汇款服务。",
            "QRIS：在印尼国家二维码支付标准下作为发行方或收单方处理二维码支付交易。",
        ],
        "minCapital": "PJP 1 最低资本金 Rp15 billion，约 USD 900k；PJP 2 为 Rp5 billion；PJP 3 为 Rp0.5-1 billion。非银行 PJP 还需按风险加权交易额计提持续资本，基础比例 10%。",
        "foreignOwnership": "非银 PJP 至少 15% 股份由印尼公民或印尼法人持有；具表决权股份中至少 51% 必须由本土方持有，且单一最大表决权也应为本土方。BI 按最终表决权穿透评估。",
        "playerCount": "材料口径：PJP1 存量 195 家，其中纯非银约 73 家；PJP2 约 35 家；PJP3 约 324 家。QRIS 服务提供商约 143 家，包括 82 家商业银行、47 家非银一级 PJP、5 家二级非银 PJP、4 家 PIP 和 3 家 BPR。",
        "market": [
            "2021 年 PJP 新规后，非银 PJP1 新批数量有限，2024 年以来材料口径仅 8 家获批。",
            "新申请 PJP1 周期可能约 2 年；收购壳公司材料口径公允价格约 USD 5-7m，周期 4-6 个月。",
            "PJP1 获批后叠加 QRIS 功能通常还需约 4-6 个月；既有案例显示 PJP1 上线 QRIS 约 8-15 个月。",
        ],
        "restrictions": [
            "同一主体不得对同一类别的多家非银 PJP 形成控股或控制，也不得同时在超过一家非银行机构上形成 PJP+PIP 双重控制。",
            "BI 按 PSPS/PSPK/PSPU 分类施加差异化风险管理和信息安全要求，包括外部 IT 审计、渗透测试、FRM、数据中心和灾备。",
            "境内交易的发起、授权、清算、结算原则上须在印尼境内处理；主数据中心和灾备应设在印尼，除非 BI 特批。",
            "2025 年 QRIS/PJP 更新后，信贷支持成为合法资金来源，但产品重大功能变更仍需提交产品和技术方案并获批。",
        ],
        "competitors": [
            {"name": "GoPay / OVO / DANA / ShopeePay", "position": "头部钱包和生态支付玩家", "signal": "PJP1 及 QRIS 生态核心参与者"},
            {"name": "Xendit / DOKU", "position": "支付网关和商户收单", "signal": "服务线上商户和企业收单需求"},
            {"name": "Payfazz", "position": "SME 支付和信贷公司", "signal": "材料显示 2025 年 1 月获 QRIS 功能"},
            {"name": "Finture / YUP", "position": "收购 PJP1 PT Indo Sukses Mandiri", "signal": "约 1 年内获批 QRIS"},
            {"name": "Airwallex", "position": "收购 PJP1 PT Skye Sab Indonesia", "signal": "材料显示尚不支持 QRIS"},
            {"name": "潜在收购标的", "position": "PT Hensel Davest Indonesia、PT Reformasi Uang Pembayaran Indonesia、PT Anadana Kode Nontunai 等", "signal": "低活跃或无公开产品痕迹的非银 PJP1"},
        ],
        "latestRules": [
            {"name": "BI 支付系统总则", "note": "PJP、PIP、Peserta、数据本地化、系统安全和支付基础设施参与规则。"},
            {"name": "2025 年 PJP/QRIS 更新", "note": "信贷支持 fasilitas kredit 被纳入 QRIS 资金来源之一，使银行授信额度和 BNPL 获得法理支持。"},
            {"name": "BI QRIS 标准", "note": "所有使用 QR Code Pembayaran 的 PJP 均须实施 QRIS。"},
        ],
        "legalIndex": [
            "Bank Indonesia payment system regulations on PJP/PIP/Peserta",
            "BI QRIS regulations and implementation standards",
            "BI licensed institution dataset for PJP, PIP, QRIS and payment infrastructure participants",
            "PBI on payment system operation and local processing requirements",
        ],
        "sourceDoc": "印尼支付牌照与QRIS情况梳理_20260420_副本.pdf",
    },
    {
        "id": "bpr",
        "name": "BPR",
        "subtitle": "Bank Perekonomian Rakyat",
        "regulator": "OJK 银行业监管",
        "category": "银行",
        "tone": "rural",
        "oneLiner": "印尼村镇银行，可吸储和放贷，但不得提供往来账户和支付结算，是传统牌照中较适合数字化改造的区域银行形态。",
        "type": "BPR / BPR Sharia 村镇银行牌照，受 OJK 银行业监管。",
        "businessScope": [
            "储蓄业务：吸纳定期存款和储蓄账户，资金来源可来自个人、企业和金融机构。",
            "信贷业务：面向个人和 SME 发放贷款。",
            "电子终端银行设备和卡片产品：可发行支持取款或存款、类似存折的储蓄卡，但不具支付功能。",
            "通过与商业银行或支付持牌机构合作，可在产品体验中形成存代付闭环。",
        ],
        "minCapital": "材料显示收购 BPR 通常需补充资本金至 IDR 6 billion；新设 BPR 按区域分级：Zone 1 约 IDR 10 billion，Zone 2 为 IDR 5 billion，Zone 3 为 IDR 2.5 billion。BPR Sharia 对应更高，Zone 1 约 IDR 75 billion。",
        "foreignOwnership": "POJK 7/2024 删除此前穿透后股东必须全部为印尼公民或政府的表述，BPR 股东只需为印尼公民或印尼法律实体，为引入外资股东打开空间；实操仍需 OJK case by case 审查。",
        "playerCount": "截至 2025 年中，印尼市场约 1300 余家 BPR；总规模约 Rp305.7 trillion，其中贷款余额约 IDR 155.9 trillion，存款余额约 Rp149.8 trillion。",
        "market": [
            "BPR 相对 P2P 没有同样的监管利率上限，但市场主流仍偏抵押和企业贷款。",
            "数字化渠道下有全国吸储实践，但跨省直营信贷的监管态度仍需个案确认。",
            "BPR + P2P channeling 已有 Komunal、Alami 等实践。",
        ],
        "restrictions": [
            "不得提供 Direct Giro 往来账户。",
            "禁止开展支付业务，不允许直接接入 BI 管理的全额结算、国家清算等支付系统。",
            "不得开展外汇兑换之外的外币业务。",
            "不得进行银行间资金交易，不得持有政府债券之外的证券。",
            "关联方贷款不得超过资本金 10%，非关联方单一主体不得超过 20%，集团授信不得超过 30%。",
            "线下网点原则上须与总部在同一省内，大雅加达地区视作一个省份。",
        ],
        "competitors": [
            {"name": "Komunal / DepositoBPR", "position": "本土 Fintech，拥有 BPR 与 P2P 牌照", "signal": "定期存款 marketplace，BPR 存款引流，P2P 项目 channeling"},
            {"name": "Alami / Bank Hijra", "position": "数字化伊斯兰 BPR", "signal": "收购 BPRS Cempaka Al-Amin 后形成 Bank Hijra"},
            {"name": "Bank Eka", "position": "传统头部 BPR 数字化", "signal": "Eka Mobile 和 Eka Pay，支付体验通过第三方持牌方合作"},
            {"name": "BPR Lestari", "position": "本土 BPR", "signal": "存贷款手机服务，消费、经营、房产和车贷"},
            {"name": "BPR BK Jateng", "position": "区域整合 BPR", "signal": "K-eris 支付体验由第三方 Spedcash 支持"},
            {"name": "BPR Karyajatnika Sadaya", "position": "数字化 BPR", "signal": "材料显示 2025 年 1 月获 QRIS 支付功能"},
        ],
        "latestRules": [
            {"name": "POJK 7/2024", "note": "规范 BPR 与 BPR Sharia，放宽股东定义，为外资通过印尼法律实体进入留下空间。"},
            {"name": "POJK 23/2022", "note": "BPR/BPRS 信贷限额相关规则，材料附录包含 BMPK/BMPD 条文。"},
            {"name": "Law No.4/2023", "note": "P2SK Law 中包含 BPR 可从事资金转化和同业存放等基础内容。"},
        ],
        "legalIndex": [
            "POJK 7 Tahun 2024 Bank Perekonomian Rakyat dan Bank Perekonomian Rakyat Syariah",
            "Peraturan OJK No.62 Tahun 2020, old BPR/BPRS rule",
            "POJK 23 Tahun 2022 on BMPK BPR and BMPD BPRS",
            "Law No.4/2023 on Financial Sector Development and Strengthening",
        ],
        "sourceDoc": "印尼BPR（村镇银行）收购_202602_副本.pdf",
    },
    {
        "id": "ics",
        "name": "ICS / PKA",
        "subtitle": "Alternative Credit Scoring",
        "regulator": "OJK 金融科技创新与数字资产监管",
        "category": "征信/数据",
        "tone": "data",
        "oneLiner": "从 2018 年监管沙盒演进出的另类征信牌照，强调使用非金融另类数据生成信用评分。",
        "type": "Pemeringkat Kredit Alternatif，PKA；英语口径仍常称 Innovative Credit Scoring, ICS。",
        "businessScope": [
            "核心产品为 Credit Score，可用符号、字母、颜色或数字呈现，并附解释说明。",
            "附加产品包括基于 Alternative Data 的欺诈警报、eKYC、收入或就业验证、黑名单、多头申请等增值服务。",
            "服务客户包括金融服务业参与者 PUJK、信用信息管理机构 LPIP、个人消费者及依法履职的公共机构等。",
        ],
        "minCapital": "本土公司申请 PKA 最低实缴资本 Rp5 billion；外资控股 PKA 仍需遵守外商投资公司最低注册资本和实缴资本 Rp10 billion。",
        "foreignOwnership": "外国个人或实体直接及间接所有权上限 85%。外籍员工限于直接向董事汇报层级或特殊专家/顾问位置，每次任期不超过 3 年，并需 1:1 印尼陪同工及技能转移。",
        "playerCount": "截至材料披露，8 家原沙盒参与厂商完成 PKA 注册流程并可持续展业，尚无新 PKA 公司走完整流程正式获批；OJK 5 月披露另有 3 家非老沙盒玩家处于申请中。",
        "market": [
            "Advance AI 是市场领先者，材料估算 ICS 年收入约 USD 2m，合并 CBI 征信约 USD 3.5m。",
            "二梯队如 iziDATA、TrustDecision 年收入估计约 USD 500k-600k。",
            "单次调用均价大致 USD 0.02-0.04，盈利关键在调用量、数据成本和多产品交叉销售。",
        ],
        "restrictions": [
            "仅可使用非金融机构 Alternative Data，如电商交易、通信运营商、公用事业缴费、社交媒体行为等。",
            "不得直接或间接使用 Credit or Financing Data，包括不得通过 OJK SLIK 接入债务和融资状况数据。",
            "PKA 营业执照后需在 30 日内提交 ESO/PSE 注册申请并在 60 日内获得，未满足前不得开展业务。",
            "数据中心和灾备中心必须设在印尼境内的独立地点。",
            "至少 2 名董事、1 名监事；至少 1 名董事具备信用评级、IT 或金融服务经验。",
        ],
        "competitors": [
            {"name": "Advance AI / BPS", "position": "市场领先者，拥有 ICS 与 CBI 征信协同", "signal": "信用评分、多头、欺诈、eKYC，数据含电商、支付网关、电信等"},
            {"name": "TrustDecision", "position": "同盾科技印尼主体", "signal": "FINScore、eKYC、欺诈检测和全球风险画像"},
            {"name": "iziDATA", "position": "中国数据公司印信科技投资", "signal": "信用评分、社交媒体号码检测、eKYC"},
            {"name": "Prime Analytics", "position": "CTOS Digital 印尼业务", "signal": "电信评分、地址核验、位置评分、收入评分"},
            {"name": "AIForesee", "position": "原 Investree 信用平台，后由韩国 PFC Technologies 收购", "signal": "eKYC、收入就业、税务、社保、法律风险和多头查询"},
            {"name": "Cloudun AI", "position": "中国和新加坡背景", "signal": "Credit insights、Digital lending 咨询和 AI 反欺诈"},
        ],
        "latestRules": [
            {"name": "POJK 3/2024", "note": "ITSK 金融科技创新统领性规则。"},
            {"name": "POJK 29/2024", "note": "正式定义 PKA/ICS 牌照，明确资本、外资、数据来源、治理和系统要求。"},
            {"name": "POJK 5/2022", "note": "Credit Bureau / LPIP 对照规则，区别于 PKA 的 SLIK 金融信用数据通道。"},
        ],
        "legalIndex": [
            "POJK 3 Tahun 2024 on Financial Sector Technology Innovation",
            "POJK 29 Tahun 2024 on Pemeringkat Kredit Alternatif",
            "POJK 5 Tahun 2022 on Credit Bureau / LPIP",
        ],
        "sourceDoc": "印尼ICS+(另类征信)监管规定与投入路径讨论决策_202605_副本.pdf",
    },
    {
        "id": "loan-aggregator",
        "name": "Loan Aggregator",
        "subtitle": "PAJK",
        "regulator": "OJK 金融科技创新与数字资产监管",
        "category": "聚合/导流",
        "tone": "market",
        "oneLiner": "贷款产品分销和获客渠道，聚合银行、Multi-Finance 和 P2P 贷款产品，帮助用户比较、筛选和申请。",
        "type": "并非独立牌照，通常纳入 PAJK，即 Penyelenggara Agregasi Jasa Keuangan 金融服务聚合商。",
        "businessScope": [
            "展示不同金融机构的贷款产品和服务信息。",
            "将潜在消费者信息转交给合作金融机构，进行 lead 转介。",
            "协助金融机构向消费者分销产品，管理金融产品申请文件。",
            "可通过 CPS/CPA/Revenue share/Lead 佣金/广告展示等方式收费，但须与合作金融机构书面约定佣金安排。",
        ],
        "minCapital": "申请 PAJK 牌照的主体必须为印尼 PT，最低实缴资本 Rp500 million，现金足额存入印尼银行账户，资金不得来源于贷款或违法活动。",
        "foreignOwnership": "外资直接及间接持股合计不得超过 85%，且不得代持；至少配置 2 名董事和 1 名监事，其中至少 1 名董事需具备金融服务聚合、IT 或金融机构相关经验。",
        "playerCount": "截至 2026 年 6 月，OJK 记录有 17 家正式注册 PAJK；26 项 PAJK 经营许可申请处于评估中，其中 17 家存量注册机构和 9 家新申请机构。",
        "market": [
            "OJK 以整个 PAJK 行业统计，未单独披露 Loan Aggregator 市场规模。",
            "2025 年 PAJK 获合作金融机构批准的交易金额 Rp26.76 trillion，累计用户 1,164.48 万。",
            "2026 年 1-5 月累计成交额 Rp10.30 trillion，月均约 Rp2.06 trillion。",
            "2026 年 5 月用户数增至 1,829 万，竞争重点从流量转向匹配准确度、申请完成率和放款转化率。",
        ],
        "restrictions": [
            "不能自行从互联网抓取贷款产品并直接销售，必须与合作贷款机构建立正式合作。",
            "合作金融机构需为持牌机构，且没有处于 OJK 业务限制或处罚状态。",
            "需要处理身份证明、手机号、收入、职业、银行账户和贷款需求等敏感数据，数据授权、共享和审计轨迹是监管重点。",
            "原则上需在获得经营许可后三年内取得符合要求的信息安全管理国际标准认证。",
            "严重违规可能导致书面警告、暂停业务、最高 Rp1 billion 行政罚款、主要责任人不适格名单或撤销许可。",
        ],
        "competitors": [
            {"name": "Cermati", "position": "综合消费金融聚合平台", "signal": "信用卡、个人贷款、保险、投资、黄金和信用评分"},
            {"name": "CashCerdas", "position": "纯线上贷款比较平台", "signal": "KTA、P2P、BPR 贷款和短期现金贷"},
            {"name": "Pilih Kredit", "position": "贷款比较及申请导流", "signal": "消费贷、现金贷、教育贷和经营贷"},
            {"name": "Ringkas", "position": "数字按揭基础设施", "signal": "连接 25 家以上银行，2025 年完成 USD 5.1m Pre-Series A"},
            {"name": "IDEAL", "position": "一站式 KPR 平台", "signal": "新房、二手房、转按揭和多用途抵押贷款"},
            {"name": "Yup", "position": "信用支付及消费金融生态", "signal": "信用额度、PayLater、Visa 信用卡和 QRIS 支付"},
            {"name": "Komunal / DepositoBPR", "position": "BPR 存款聚合平台", "signal": "累计连接存款超过 Rp21 trillion，覆盖 350 家以上 BPR"},
        ],
        "latestRules": [
            {"name": "POJK 4/2025", "note": "PAJK 从旧注册和沙盒模式转向正式经营许可制度。"},
            {"name": "过渡期要求", "note": "原已注册 Aggregator、Financing Agent、Funding Agent 和 Wealthtech 最迟于 2026-02-26 提交经营许可申请。"},
            {"name": "PSE/ESO 登记", "note": "取得 PAJK 后仍需完成电子系统运营者登记，才能正式开展服务。"},
        ],
        "legalIndex": [
            "POJK 4/2025 on Penyelenggara Agregasi Jasa Keuangan",
            "PAJK cooperation agreement requirements",
            "Personal data protection and electronic system operator registration requirements",
            "OJK SPRINT licensing process",
        ],
        "sourceDoc": "印尼Loan Aggregator研究_202607.pdf",
    },
]


regulator_map = [
    {
        "name": "OJK",
        "full": "Otoritas Jasa Keuangan",
        "role": "统一监管金融服务业，覆盖银行、非银、金融科技创新、消费者保护、AML/CFT/CPF 和问题机构处置。",
        "focus": "牌照准入和持续监管的主责机构。",
        "licenses": ["商业银行", "BPR", "Multi-Finance", "P2P", "ICS/PKA", "Loan Aggregator"],
        "signals": ["准入许可", "资本和股东", "治理和风险", "消费者保护", "数据和 IT"],
        "importance": "商业银行、BPR、Multi-Finance、P2P、ICS/PKA 与 Loan Aggregator 的准入、股东、资本、治理和持续报送，基本都要回到 OJK 框架下判断。",
        "watch": ["新设或收购审批", "最低资本与核心资本", "外资持股与控制人", "董事会和风险管理", "消费者保护与投诉处理", "AML/CFT/CPF"],
        "decides": ["谁能成为控股股东或实际控制人", "机构能否取得或维持经营许可", "董事、监事和关键管理层是否适格", "业务扩张是否触发额外批准或报备", "监管报送、检查、整改和处罚口径"],
        "notInScope": ["不直接管理支付系统基础设施和 QRIS 标准", "不负责电子系统运营者 PSE/ESO 登记本身", "不负责存款保险赔付和问题银行处置资金安排"],
        "triggers": ["收购存量金融机构", "新增外资股东或控制权变化", "线上金融产品改变风控或消费者触点", "监管报表、投诉、催收、外包出现历史缺口", "同一集团在多个金融牌照之间做业务协同"],
    },
    {
        "name": "BI",
        "full": "Bank Indonesia",
        "role": "中央银行，负责货币、宏观审慎和支付系统；PJP、PIP、QRIS、BI-FAST、RTGS 等由 BI 管理。",
        "focus": "支付系统和支付基础设施的主责机构。",
        "licenses": ["PJP", "PIP", "QRIS", "Peserta BI-FAST/RTGS/SKNBI"],
        "signals": ["支付许可", "支付基础设施", "本地化处理", "支付数据安全", "持续资本"],
        "importance": "PJP、QRIS、支付清算、本地交易处理、支付数据安全和支付产品变更，都要按 BI 的支付系统规则判断；涉及外汇、跨境支付或银行支付合作时也要同步关注 BI 口径。",
        "watch": ["PJP 许可分类", "QRIS 接入和产品变更", "本地处理与数据安全", "支付基础设施参与资格", "持续资本和风险分类", "外汇和跨境支付规则"],
        "decides": ["支付服务提供商 PJP 的许可类别和业务范围", "QRIS、收单、汇款、账户信息和支付发起等功能是否可上线", "支付交易处理、清算、结算和数据本地化要求", "支付系统参与者接入 BI-FAST、RTGS、SKNBI 等基础设施的条件", "支付产品重大变更是否需要批准或报备"],
        "notInScope": ["不审批 P2P、Multi-Finance、ICS/PKA 或 PAJK 这类金融服务牌照", "不决定存款保险覆盖范围", "不替代 Komdigi 对电子系统登记和网络系统的要求"],
        "triggers": ["计划申请或收购 PJP/PIP/QRIS 能力", "钱包、收单、汇款、信贷支付或 QRIS 产品设计变化", "跨境收付款、外汇入账或银行通道安排", "支付数据、主数据中心、灾备或交易处理链路变化", "接入银行清算或实时支付基础设施"],
    },
    {
        "name": "LPS",
        "full": "Lembaga Penjamin Simpanan",
        "role": "存款保险和银行处置体系，对商业银行和 BPR 的存款保障、问题银行处置具有关键影响。",
        "focus": "银行存款保障和问题银行处置。",
        "licenses": ["商业银行", "BPR"],
        "signals": ["存款保险", "问题银行处置", "金融稳定"],
        "importance": "LPS 不决定大多数牌照准入，但会影响商业银行和 BPR 的存款吸收可信度、问题银行处置预期，以及收购存量银行时对负债端稳定性的判断。",
        "watch": ["存款保险范围", "保障利率和存款条件", "问题银行处置", "银行关停或救助安排", "公众信任和负债端稳定性"],
        "decides": ["哪些银行存款在制度上可被保障", "存款保险条件、保障利率和赔付边界", "问题银行进入处置时的路径和角色分工", "银行退出、清算或救助时存款人保护安排", "市场对存款端安全性的预期"],
        "notInScope": ["不审批商业银行或 BPR 的设立、收购和股东变更", "不管理支付系统或 QRIS 接入", "不负责线上电子系统登记、数据中心或网络安全登记"],
        "triggers": ["收购商业银行或 BPR，尤其是负债端依赖存款的标的", "设计高息存款、渠道吸储或存款聚合方案", "标的银行存在经营压力、监管评级压力或潜在处置情景", "需要向合作方解释存款安全性和公众信任基础"],
    },
    {
        "name": "Komdigi",
        "full": "通信和数字事务主管部门",
        "role": "电子系统运营者登记和数字系统要求，对 P2P、ICS、PAJK 等线上业务上线前置影响较大。",
        "focus": "电子系统登记、线上服务和数字基础设施要求。",
        "licenses": ["P2P", "ICS/PKA", "Loan Aggregator"],
        "signals": ["PSE/ESO 登记", "数据中心", "网络安全", "电子系统合规"],
        "importance": "Komdigi 通常不是金融牌照审批主责方，但对线上产品能否正式上线很关键。P2P、ICS/PKA、PAJK/Loan Aggregator 等数字业务，拿到金融许可后仍需关注 PSE/ESO、系统位置、网络安全和数据处理要求。",
        "watch": ["PSE/ESO 登记", "数据中心和灾备位置", "网络安全事件管理", "电子系统合规", "个人数据和系统访问控制"],
        "decides": ["线上平台是否完成电子系统运营者登记", "电子系统、域名、应用和服务描述是否与实际业务一致", "数据中心、灾备、系统访问和网络安全安排是否满足上线要求", "发生安全事件或系统事故时的报告和处置要求", "线上服务下架、阻断或整改的行政风险"],
        "notInScope": ["不判断金融机构是否具备金融牌照", "不审批 PJP/QRIS 支付系统资格", "不决定银行存款保障和问题银行处置"],
        "triggers": ["产品以 App、网站、API 或后台系统对外提供服务", "申牌后准备正式上线电子系统", "更换数据中心、云服务、灾备、域名或关键外包商", "涉及个人数据、设备数据、替代数据或风控模型调用", "发生系统事故、数据泄露或监管要求整改"],
    },
]


sources = []

regulatory_briefings = [
    {
        "date": "2026",
        "publishedDate": "2026-01-06",
        "title": "BPR 最低资本与核心资本要求更新",
        "regulator": "OJK",
        "licenses": ["BPR"],
        "level": "高",
        "summary": "OJK 发布 POJK Nomor 7 Tahun 2026，主题为 Bank Perekonomian Rakyat 的最低资本充足和最低核心资本满足要求。",
        "impact": "BPR 收购或数字化改造不能只看历史实缴资本和壳价，还要重新核算资本充足、核心资本缺口和后续补资压力。",
        "action": "BPR 标的池增加核心资本缺口、资本充足率、历史利润留存、股东补资能力和 OJK 资本整改要求字段。",
        "keywords": "POJK Nomor 7 Tahun 2026 Kewajiban Penyediaan Modal Minimum Pemenuhan Modal Inti Minimum Bank Perekonomian Rakyat",
        "sourceLabel": "OJK 官方法规页",
        "sourceUrl": "https://www.ojk.go.id/id/regulasi/Pages/POJK-Nomor-7-Tahun-2026-Kewajiban-Penyediaan-Modal-Minimum-dan-Pemenuhan-Modal-Inti-Minimum-Bank-Perekonomian-Rakyat.aspx",
        "sourceAltLabel": "备用：OJK 站内检索",
        "sourceAltUrl": "https://www.ojk.go.id/id/regulasi/_layouts/15/osssearchresults.aspx?u=https%3A%2F%2Fwww.ojk.go.id%2Fid%2Fregulasi&k=Kewajiban%20Penyediaan%20Modal%20Minimum%20Bank%20Perekonomian%20Rakyat",
        "sourceStatus": "原文页与备用检索均已核验 200；若原文页打不开，请点备用检索。",
    },
    {
        "date": "2026",
        "publishedDate": "2025-12-26",
        "title": "ITSK 经营者治理和风险管理规则落地",
        "regulator": "OJK",
        "licenses": ["ICS / PKA", "Loan Aggregator"],
        "level": "高",
        "summary": "OJK 发布 POJK Nomor 30 Tahun 2025，主题为金融科技创新部门经营者的治理与风险管理。",
        "impact": "ICS/PKA、PAJK/Loan Aggregator 等 ITSK 相关主体的准入后监管会更关注董事会责任、风险管理、内控、数据/系统治理和持续合规。",
        "action": "申牌或收购时增加治理框架、风险管理制度、信息安全职责、第三方外包管理和董事会监督材料的尽调要求。",
        "keywords": "POJK Nomor 30 Tahun 2025 Tata Kelola Manajemen Risiko Penyelenggara Inovasi Teknologi Sektor Keuangan",
        "sourceLabel": "OJK 官方法规页",
        "sourceUrl": "https://www.ojk.go.id/id/regulasi/Pages/POJK-Nomor-30-Tahun-2025-Penerapan-Tata-Kelola-dan-Manajemen-Risiko-Bagi-Penyelenggara-Inovasi-Teknologi-Sektor-Keuangan.aspx",
        "sourceAltLabel": "备用：OJK 站内检索",
        "sourceAltUrl": "https://www.ojk.go.id/id/regulasi/_layouts/15/osssearchresults.aspx?u=https%3A%2F%2Fwww.ojk.go.id%2Fid%2Fregulasi&k=Penerapan%20Tata%20Kelola%20Manajemen%20Risiko%20Penyelenggara%20Inovasi%20Teknologi%20Sektor%20Keuangan",
        "sourceStatus": "原文页与备用检索均已核验 200；若原文页打不开，请点备用检索。",
    },
    {
        "date": "2025",
        "publishedDate": "2025-11-24",
        "title": "融资公司月度报告规则更新",
        "regulator": "OJK",
        "licenses": ["Multi-Finance"],
        "level": "中",
        "summary": "OJK 发布 PADK 45/PADK.06/2025，主题为普通融资公司和伊斯兰融资公司的月度报告。",
        "impact": "Multi-Finance 的监管报送频率、字段完整性和口径一致性会成为合规重点，收购存量公司时需要核验历史月报质量和整改记录。",
        "action": "尽调要求目标公司提供近 24 个月月报、OJK 回执、补正记录、NPF/gearing 报送口径和核心业务分项数据。",
        "keywords": "45/PADK.06/2025 Laporan Bulanan Perusahaan Pembiayaan Perusahaan Pembiayaan Syariah",
        "sourceLabel": "OJK 官方法规页",
        "sourceUrl": "https://www.ojk.go.id/id/regulasi/Pages/PADK-45-PADK06-2025-Laporan-Bulanan-Perusahaan-Pembiayaan-dan-Perusahaan-Pembiayaan-Syariah.aspx",
        "sourceStatus": "已核验 200",
    },
    {
        "date": "2025",
        "publishedDate": "2025-10-23",
        "title": "投诉处理公开与投诉服务报告规则更新",
        "regulator": "OJK",
        "licenses": ["商业银行", "BPR", "Multi-Finance", "P2P", "ICS / PKA", "Loan Aggregator"],
        "level": "中",
        "summary": "OJK 发布 SEOJK 20/SEOJK.08/2025，主题为投诉处理公开和投诉服务报告。",
        "impact": "面向消费者的银行、BPR、融资公司、P2P、金融科技聚合/评分服务都需要关注投诉披露、服务报告和消费者保护留痕。",
        "action": "为各牌照子页面增加消费者投诉合规核查项：投诉 SLA、公开披露、定期报告、工单留痕、催收投诉和外包投诉管理。",
        "keywords": "20/SEOJK.08/2025 Publikasi Penanganan Pengaduan Laporan Layanan Pengaduan",
        "sourceLabel": "OJK 官方法规页",
        "sourceUrl": "https://www.ojk.go.id/id/regulasi/Pages/SEOJK-20-SEOJK08-2025-Publikasi-Penanganan-Pengaduan-dan-Laporan-Layanan-Pengaduan.aspx",
        "sourceStatus": "已核验 200",
    },
]


developer_log = [
    {
        "date": "2026-07-17",
        "type": "数据管道",
        "title": "监管动态改为长期历史库",
        "summary": "将监管动态从单日快照升级为可持续累积的历史库：首页只展示最新几条，历史页保留网站创建以来收录过的监管简报。",
        "changes": [
            "新增 regulatory-history.json，保存历史简报、首次收录日期、最近出现日期和出现次数。",
            "每日联网检索仍生成最新快照 regulatory-updates.json，但会同步合并进历史库。",
            "GitHub Actions 定时任务会把历史库写回仓库，避免下一次部署覆盖旧简报。",
        ],
    },
    {
        "date": "2026-07-17",
        "type": "模块优化",
        "title": "商业银行竞争对手改为横向对比",
        "summary": "商业银行详情页的竞争对手板块从普通卡片改为分层格局和横向对比表，突出玩家体量、主战场和对进入策略的启示。",
        "changes": [
            "新增 KBMI 4 大行、区域/外资银行、数字银行三层竞争格局提示。",
            "商业银行竞争对手表格新增行业体量、关键优势和策略启示字段。",
            "其他牌照的竞争对手卡片保持原样，避免尚未补充字段时被强行表格化。",
        ],
    },
    {
        "date": "2026-07-17",
        "type": "信息架构",
        "title": "首页新增监管动态滚动区",
        "summary": "将“监管更新”统一改名为“监管动态”，首页直接展示最新几条动态，完整历史仍保留在独立模块。",
        "changes": [
            "首页新增横向滚动的最新监管动态预览，并提供“查看历史”入口。",
            "监管动态卡片新增“发布日期”标签，优先展示官方列表或页面解析出的具体日期。",
            "牌照子页面的最新监管规定同步显示发布日期，便于判断法规新旧。",
        ],
    },
    {
        "date": "2026-07-17",
        "type": "\u90e8\u7f72\u81ea\u52a8\u5316",
        "title": "\u652f\u6301 GitHub Pages \u6bcf\u65e5\u81ea\u52a8\u90e8\u7f72",
        "summary": "\u65b0\u589e GitHub Actions \u5de5\u4f5c\u6d41\uff0c\u8ba9\u5176\u4ed6\u4eba\u53ef\u901a\u8fc7\u56fa\u5b9a\u7f51\u7ad9\u94fe\u63a5\u8bbf\u95ee\uff0c\u540c\u65f6\u4fdd\u7559\u6bcf\u65e5\u8054\u7f51\u66f4\u65b0\u80fd\u529b\u3002",
        "changes": [
            "\u65b0\u589e .github/workflows/deploy-pages.yml\uff0c\u652f\u6301\u5b9a\u65f6\u3001\u624b\u52a8\u548c push \u89e6\u53d1\u90e8\u7f72\u3002",
            "\u5c06\u751f\u6210\u5668\u4e2d\u7684\u672c\u673a\u7edd\u5bf9\u8def\u5f84\u6539\u4e3a\u9879\u76ee\u76f8\u5bf9\u8def\u5f84\uff0c\u9002\u914d GitHub Actions \u8fd0\u884c\u73af\u5883\u3002",
            "\u53d1\u5e03\u76ee\u5f55\u56fa\u5b9a\u4e3a public/\uff0c\u90e8\u7f72\u65f6\u81ea\u52a8\u5e26\u4e0a\u6700\u65b0\u76d1\u7ba1\u5feb\u7167\u548c\u5f00\u53d1\u8005\u65e5\u5fd7\u3002",
        ],
    },
    {
        "date": "2026-07-17",
        "type": "\u9759\u6001\u4ea4\u4ed8",
        "title": "\u751f\u6210\u53ef\u5355\u72ec\u5206\u53d1\u7684\u9759\u6001 HTML",
        "summary": "\u5c06\u76d1\u7ba1\u7b80\u62a5\u5feb\u7167\u548c\u5f00\u53d1\u8005\u65e5\u5fd7\u5185\u5d4c\u5230 HTML\uff0c\u4fbf\u4e8e\u79bb\u5f00\u672c\u673a\u670d\u52a1\u540e\u76f4\u63a5\u6253\u5f00\u9875\u9762\u3002",
        "changes": [
            "\u65b0\u589e outputs/indonesia_financial_regulatory_landscape_static.html \u4f5c\u4e3a\u9759\u6001\u4ea4\u4ed8\u6587\u4ef6\u3002",
            "\u9875\u9762\u5728 file:// \u6253\u5f00\u65f6\u8df3\u8fc7\u5916\u90e8 JSON \u8bf7\u6c42\uff0c\u76f4\u63a5\u4f7f\u7528\u5185\u7f6e\u5feb\u7167\u3002",
            "\u4fdd\u7559\u672c\u5730\u7f51\u7ad9\u6a21\u5f0f\uff1a\u901a\u8fc7 server.js \u8fd0\u884c\u65f6\u4ecd\u53ef\u8bfb\u53d6\u6bcf\u65e5\u66f4\u65b0 JSON\u3002",
        ],
    },
    {
        "date": "2026-07-17",
        "type": "\u89c6\u89c9\u8bd5\u9a8c",
        "title": "\u76d1\u7ba1\u7ed3\u6784\u4e09\u7ec4\u5224\u65ad\u6539\u4e3a Mindmap",
        "summary": "\u76d1\u7ba1\u7ed3\u6784\u4e2d\u4e09\u4e2a\u5224\u65ad\u533a\u5df2\u6539\u4e3a mindmap\u3002",
        "changes": [
            "\u4fdd\u7559\u539f\u6709\u76d1\u7ba1\u4fe1\u606f\u3002",
            "\u4e09\u6761\u5206\u652f\u5206\u522b\u5c55\u793a\u8fb9\u754c\u3001\u6392\u9664\u4e8b\u9879\u548c\u89e6\u53d1\u573a\u666f\u3002",
            "\u79fb\u52a8\u7aef\u6539\u4e3a\u7eb5\u5411\u5217\u8868\u3002",
        ],
    },
    {
        "date": "2026-07-16",
        "type": "模块精简",
        "title": "监管结构移除跨部门说明",
        "summary": "删除监管结构里信息密度偏低的跨部门说明段落，保留职责、边界、触发场景和监管抓手。",
        "changes": [
            "不再在监管结构卡片中展示跨部门说明。",
            "字段完整性检查同步移除该字段的必渲染要求。",
            "监管结构页面保留职责、研究意义、决定事项、不负责事项、触发场景和监管抓手。",
        ],
    },
    {
        "date": "2026-07-16",
        "type": "质量保护",
        "title": "监管结构排版增加信息完整性保护",
        "summary": "在调整监管结构版式后，补充字段合并和回归检查，确保排版优化不会导致原有监管信息被漏掉。",
        "changes": [
            "将“触发场景”和原有“关注事项”合并去重后展示。",
            "模块检查脚本新增监管结构字段引用检查。",
            "保留每个部门的职责、意义、边界、触发场景和监管抓手信息。",
        ],
    },
    {
        "date": "2026-07-16",
        "type": "视觉优化",
        "title": "监管结构模块排版整理",
        "summary": "将监管结构从密集信息块改为更清爽的部门档案版式，减少边框堆叠和表单感。",
        "changes": [
            "每个部门改为左侧身份区、右侧职责摘要和下方三栏信息区。",
            "列表从密集边框格子改成轻量 bullet，降低视觉噪音。",
            "监管抓手从重复区块中分离出来，阅读顺序更清晰。",
        ],
    },
    {
        "date": "2026-07-16",
        "type": "模块优化",
        "title": "监管结构补充边界和触发场景",
        "summary": "在每个监管部门下新增非重复信息，重点解释它具体决定什么、不负责什么，以及何时会影响项目。",
        "changes": [
            "OJK、BI、LPS、Komdigi 均新增“它具体决定什么”和“它不负责什么”。",
            "将原来的“阅读时重点关注”升级为更项目化的“什么时候需要重点看它”。",
            "新增监管边界说明，帮助判断每个部门负责与不负责的事项。",
        ],
    },
    {
        "date": "2026-07-16",
        "type": "模块优化",
        "title": "监管结构模块改为部门独立篇幅",
        "summary": "去掉监管结构中卡片和表格的重复展示，改为 OJK、BI、LPS、Komdigi 各自独立的阅读篇幅。",
        "changes": [
            "每个监管部门单独展示核心职责、覆盖牌照、监管抓手和对牌照策略的意义。",
            "新增“阅读时重点关注”清单，帮助快速判断尽调和申牌时要看什么。",
            "删除原有监管机构卡片 + 表格的重复结构。",
        ],
    },
    {
        "date": "2026-07-16",
        "type": "界面简化",
        "title": "移除左侧栏，减少与模块入口重复",
        "summary": "模块化首页已经承担主要导航功能，因此移除左侧固定侧栏，页面改为全宽展示，并保留顶部下拉作为轻量辅助导航。",
        "changes": [
            "删除左侧栏的品牌区、模块按钮和牌照按钮。",
            "页面主内容从左右分栏改为全宽布局。",
            "顶部下拉继续支持模块和牌照详情跳转，避免导航功能丢失。",
        ],
    },
    {
        "date": "2026-07-16",
        "type": "信息架构",
        "title": "首页拆分为可点击的信息模块",
        "summary": "把原来的长页面滚动结构改成模块入口式网站，用户通过点击进入监管结构、牌照库、横向对比、监管更新和开发者日志。",
        "changes": [
            "首页只保留主题说明和模块卡片，不再默认铺开所有长内容。",
            "新增 module 路由，支持 #module/regulators、#module/licenses、#module/compare、#module/updates、#module/developer-log。",
            "侧边栏和移动端选择器同步支持模块跳转，牌照详情页仍保持独立点击进入。",
        ],
    },
    {
        "date": "2026-07-16",
        "type": "文案优化",
        "title": "监管简报摘要本地化与去模板化",
        "summary": "把每日联网检索生成的简报摘要从机械抓取模板改成中文法规摘要，减少原始印尼语标题直接堆进正文的问题。",
        "changes": [
            "新增法规标题本地化规则，把 PADG、POJK、SEOJK、PADK 等标题转成中文阅读格式。",
            "摘要改为说明监管机构、法规编号和规则主题，不再使用“官方入口抓取到监管条目”的模板句。",
            "影响和建议动作按外汇、月报、治理风控、资本、投诉、AML 等主题分别生成更自然的表述。",
        ],
    },
    {
        "date": "2026-07-16",
        "type": "功能新增",
        "title": "新增开发者日志时间线",
        "summary": "把网站改动从页面正文说明中拆出来，形成独立的开发者日志模块，方便其他人看到网站本身做过哪些改动。",
        "changes": [
            "新增 public/developer-log.json 作为可持续维护的日志数据源。",
            "首页新增开发者日志时间线，按日期展示功能、数据和维护动作。",
            "页面会优先读取外部 developer-log.json，读取失败时使用内置日志快照。",
        ],
    },
    {
        "date": "2026-07-16",
        "type": "架构升级",
        "title": "从静态 HTML 升级为本地网站服务",
        "summary": "新增 Node 网站服务，让监管简报可以由服务端联网刷新，而不是只依赖静态页面内置快照。",
        "changes": [
            "新增 server.js，提供首页、监管更新 JSON、手动刷新 API。",
            "网站启动时会先刷新监管快照，运行期间每天 08:30 自动刷新。",
            "已创建 Codex 本地每日自动任务，每天约 08:45 运行更新器。",
        ],
    },
    {
        "date": "2026-07-16",
        "type": "数据管道",
        "title": "新增每日联网监管检索器",
        "summary": "新增 OJK、BI、JDIH BI 官方入口检索器，生成页面读取的 regulatory-updates.json。",
        "changes": [
            "只从官方入口抓取法规页，保留 sourcesChecked 诊断信息。",
            "收紧筛选规则，排除导航、目录、地址表和机构介绍页。",
            "如果某个来源超时或失败，只记录诊断，不生成不存在或不相关的简报。",
        ],
    },
    {
        "date": "2026-07-16",
        "type": "内容修正",
        "title": "修正监管简报链接与来源呈现",
        "summary": "把此前无法访问或与内容无关的链接替换为可核验的官方来源，并补充备用入口。",
        "changes": [
            "BPR 和 ITSK 简报增加 OJK 原文页与 OJK 站内检索备用链接。",
            "简报卡片显示来源状态，区分实时抓取和基准快照保留。",
            "未获取到稳定可核验来源的类别不硬生成监管变更。",
        ],
    },
]


def load_json_snapshot(*paths: Path, fallback: dict) -> dict:
    for path in paths:
        try:
            if path.exists():
                return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
    return fallback


KNOWN_PUBLISHED_DATES = {
    "SEOJK 23/SEOJK.06/2025": "2025-05-27",
    "POJK 30/2025": "2025-12-26",
    "POJK 7/2026": "2026-01-06",
    "PADK 45/PADK.06/2025": "2025-11-24",
    "SEOJK 20/SEOJK.08/2025": "2025-10-23",
    "PADG 19/2026": "2026-06-30",
}


def enrich_published_dates(snapshot: dict) -> dict:
    for item in snapshot.get("briefings", []) or []:
        if item.get("publishedDate"):
            continue
        text = " ".join(
            str(item.get(key, ""))
            for key in ("title", "sourceUrl", "sourceOriginalTitle", "keywords")
        )
        for marker, published_date in KNOWN_PUBLISHED_DATES.items():
            if marker in text:
                item["publishedDate"] = published_date
                break
    for updates in (snapshot.get("licenses") or {}).values():
        for item in updates:
            if item.get("publishedDate"):
                continue
            text = " ".join(str(item.get(key, "")) for key in ("name", "note", "sourceUrl"))
            for marker, published_date in KNOWN_PUBLISHED_DATES.items():
                if marker in text:
                    item["publishedDate"] = published_date
                    break
    return snapshot


embedded_update_snapshot = load_json_snapshot(
    REGULATORY_PUBLIC,
    REGULATORY_DATA,
    fallback={
        "generatedDate": "2026-07-16",
        "mode": "built-in-fallback",
        "briefings": regulatory_briefings,
        "licenses": {},
        "sourcesChecked": [],
    },
)
embedded_update_snapshot = enrich_published_dates(embedded_update_snapshot)

embedded_history_snapshot = load_json_snapshot(
    REGULATORY_HISTORY_PUBLIC,
    REGULATORY_HISTORY_DATA,
    fallback=embedded_update_snapshot,
)
embedded_history_snapshot = enrich_published_dates(embedded_history_snapshot)


html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>印尼核心金融牌照监管机构图景</title>
  <style>
    :root {{
      --ink: #15212f;
      --muted: #657080;
      --line: #d9e0e7;
      --paper: #f7f8f6;
      --panel: #ffffff;
      --bank: #1c6f69;
      --pay: #2f68a3;
      --asset: #9a5a18;
      --digital: #b13f52;
      --data: #6a5c9f;
      --market: #54733b;
      --rural: #7a6145;
      --shadow: 0 18px 40px rgba(21, 33, 47, .08);
    }}

    * {{ box-sizing: border-box; }}

    html {{ scroll-behavior: smooth; }}

    body {{
      margin: 0;
      color: var(--ink);
      background: var(--paper);
      font-family: Inter, "Segoe UI", "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
      font-size: 15px;
      line-height: 1.55;
      letter-spacing: 0;
    }}

    button, input, select {{
      font: inherit;
      color: inherit;
    }}

    a {{ color: inherit; }}

    .app-shell {{
      min-height: 100vh;
      display: block;
    }}

    .mobile-bar {{
      position: sticky;
      top: 0;
      z-index: 20;
      background: rgba(251, 251, 248, .96);
      border-bottom: 1px solid var(--line);
      padding: 12px 14px;
      backdrop-filter: blur(10px);
    }}

    .mobile-bar select {{
      width: 100%;
      min-height: 42px;
      border-radius: 8px;
      border: 1px solid var(--line);
      background: #fff;
      padding: 0 12px;
    }}

    main {{
      min-width: 0;
    }}

    .page {{
      display: none;
      min-height: 100vh;
    }}

    .page.active {{
      display: block;
    }}

    .hero {{
      min-height: 86vh;
      padding: 44px clamp(18px, 4vw, 54px) 30px;
      display: grid;
      align-content: space-between;
      gap: 30px;
      background:
        linear-gradient(120deg, rgba(255,255,255,.88), rgba(255,255,255,.72)),
        radial-gradient(circle at 14% 20%, rgba(28,111,105,.13), transparent 30%),
        radial-gradient(circle at 85% 10%, rgba(177,63,82,.14), transparent 28%),
        #eef2ec;
      border-bottom: 1px solid var(--line);
    }}

    .hero-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1.05fr) minmax(380px, .95fr);
      gap: clamp(24px, 4vw, 54px);
      align-items: center;
    }}

    .eyebrow {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      width: fit-content;
      padding: 5px 9px;
      border: 1px solid #cbd8d5;
      border-radius: 999px;
      color: #2b5957;
      background: rgba(255,255,255,.76);
      font-size: 12px;
      font-weight: 700;
    }}

    .hero h2 {{
      margin: 18px 0 12px;
      max-width: 800px;
      font-size: clamp(34px, 6vw, 72px);
      line-height: 1.02;
      letter-spacing: 0;
    }}

    .hero-copy {{
      max-width: 760px;
      margin: 0;
      color: #42505e;
      font-size: clamp(16px, 2vw, 20px);
    }}

    .hero-actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 22px;
    }}

    .home-hub.hidden {{
      display: none;
    }}

    .module-hub {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      align-self: stretch;
    }}

    .module-card {{
      min-height: 138px;
      display: grid;
      align-content: space-between;
      gap: 16px;
      padding: 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255, 255, 255, .82);
      color: var(--ink);
      text-decoration: none;
      box-shadow: 0 10px 24px rgba(21, 33, 47, .05);
    }}

    .module-card:hover {{
      border-color: #9cb9b1;
      background: #fff;
      transform: translateY(-1px);
    }}

    .module-card strong {{
      display: block;
      margin-bottom: 6px;
      font-size: 18px;
      line-height: 1.25;
    }}

    .module-card p {{
      margin: 0;
      color: #536170;
      line-height: 1.55;
    }}

    .home-dynamics {{
      padding: 28px clamp(18px, 4vw, 54px) 34px;
      border-bottom: 1px solid var(--line);
      background: #fbfcfb;
    }}

    .home-dynamics.hidden {{
      display: none;
    }}

    .home-dynamics .section-header {{
      margin-bottom: 12px;
    }}

    .home-dynamic-strip {{
      display: grid;
      grid-auto-flow: column;
      grid-auto-columns: minmax(300px, 420px);
      gap: 12px;
      overflow-x: auto;
      padding: 2px 2px 12px;
      scroll-snap-type: x mandatory;
    }}

    .home-dynamic-card {{
      scroll-snap-align: start;
      min-height: 204px;
      padding: 15px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      display: grid;
      gap: 10px;
      align-content: start;
      box-shadow: 0 8px 20px rgba(21, 33, 47, .04);
    }}

    .home-dynamic-card h4 {{
      margin: 0;
      font-size: 17px;
      line-height: 1.3;
    }}

    .home-dynamic-card p {{
      margin: 0;
      color: #4c5968;
    }}

    .module-page {{
      display: none;
    }}

    .module-page.active {{
      display: block;
    }}

    .module-kicker {{
      padding: 0 0 18px;
    }}

    .module-kicker .btn {{
      width: fit-content;
    }}

    .btn {{
      min-height: 42px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 0 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      color: var(--ink);
      text-decoration: none;
      cursor: pointer;
    }}

    .btn.primary {{
      border-color: #173d3a;
      background: #173d3a;
      color: #fff;
    }}

    .reg-map {{
      background: rgba(255,255,255,.78);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      padding: 16px;
    }}

    .map-title {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 12px;
    }}

    .map-title h3 {{
      margin: 0;
      font-size: 16px;
    }}

    .map-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }}

    .map-node {{
      min-height: 152px;
      padding: 13px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      display: grid;
      gap: 9px;
      align-content: start;
    }}

    .map-node strong {{
      font-size: 18px;
    }}

    .map-node p {{
      margin: 0;
      color: #4c5968;
      font-size: 13px;
    }}

    .regulator-stack {{
      display: grid;
      gap: 16px;
    }}

    .regulator-section {{
      display: grid;
      grid-template-columns: minmax(230px, .5fr) minmax(0, 1fr);
      gap: 0;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      overflow: hidden;
      box-shadow: 0 10px 24px rgba(21, 33, 47, .04);
    }}

    .regulator-section + .regulator-section {{
      margin-top: 0;
    }}

    .regulator-identity {{
      display: grid;
      align-content: start;
      gap: 12px;
      padding: 22px;
      border-right: 1px solid var(--line);
      background: #f8faf8;
    }}

    .regulator-identity h4 {{
      margin: 0;
      font-size: clamp(32px, 4vw, 54px);
      line-height: 1;
      letter-spacing: 0;
    }}

    .regulator-full {{
      color: #405263;
      font-weight: 800;
    }}

    .regulator-focus {{
      margin: 0;
      color: #586675;
      font-size: 15px;
    }}

    .regulator-content {{
      display: grid;
      gap: 16px;
      padding: 22px;
    }}

    .regulator-block {{
      display: grid;
      gap: 8px;
    }}

    .regulator-block strong {{
      color: #516172;
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: .04em;
    }}

    .regulator-block p {{
      margin: 0;
      color: #455464;
    }}

    .regulator-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
    }}

    .regulator-watch {{
      display: grid;
      gap: 6px;
      margin: 0;
      padding: 0;
      list-style: none;
    }}

    .regulator-watch li {{
      position: relative;
      padding-left: 14px;
      color: #374656;
      line-height: 1.45;
    }}

    .regulator-watch li::before {{
      content: "";
      position: absolute;
      left: 0;
      top: .68em;
      width: 5px;
      height: 5px;
      border-radius: 50%;
      background: #1c6f69;
    }}

    .regulator-summary {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--line);
    }}

    .regulator-panel {{
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfcfb;
    }}


    .regulator-mindmap {{
      position: relative;
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
      align-items: stretch;
      padding-top: 56px;
    }}

    .regulator-mindmap::before {{
      content: "";
      position: absolute;
      top: 30px;
      left: 16.5%;
      right: 16.5%;
      height: 1px;
      background: #c9d8d4;
    }}

    .mindmap-center {{
      position: absolute;
      left: 50%;
      top: 0;
      transform: translateX(-50%);
      z-index: 1;
      display: grid;
      place-items: center;
      min-width: 148px;
      padding: 7px 14px;
      border: 1px solid #b8cbc6;
      border-radius: 999px;
      background: #eef6f2;
      box-shadow: 0 8px 18px rgba(20, 65, 60, .08);
      text-align: center;
    }}

    .mindmap-center span {{
      color: #526170;
      font-size: 12px;
      line-height: 1.2;
    }}

    .mindmap-center strong {{
      color: #173d3a;
      font-size: 14px;
      line-height: 1.2;
    }}

    .mindmap-branch {{
      position: relative;
      padding: 16px;
      border: 1px solid var(--line);
      border-top: 3px solid #1c6f69;
      border-radius: 8px;
      background: #fbfcfb;
      min-width: 0;
    }}

    .mindmap-branch::before {{
      content: "";
      position: absolute;
      top: -27px;
      left: 50%;
      height: 24px;
      border-left: 1px solid #c9d8d4;
    }}

    .mindmap-branch-title {{
      margin-bottom: 10px;
      color: var(--ink);
      font-size: 15px;
      font-weight: 900;
      line-height: 1.3;
    }}

    .mindmap-branch[data-tone="limits"] {{ border-top-color: #60717f; }}
    .mindmap-branch[data-tone="triggers"] {{ border-top-color: #7b6f42; }}
    .mindmap-branch[data-tone="limits"] .regulator-watch li::before {{ background: #60717f; }}
    .mindmap-branch[data-tone="triggers"] .regulator-watch li::before {{ background: #7b6f42; }}
    .regulator-footer {{
      padding-top: 2px;
    }}

    .mini-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
    }}

    .tag {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 2px 7px;
      border: 1px solid #dce4ea;
      border-radius: 999px;
      background: #f7f9fa;
      color: #4b5663;
      font-size: 12px;
      white-space: nowrap;
    }}

    .section {{
      padding: 34px clamp(18px, 4vw, 54px);
    }}

    .section + .section {{
      border-top: 1px solid var(--line);
    }}

    .section-header {{
      display: flex;
      align-items: end;
      justify-content: space-between;
      gap: 18px;
      margin-bottom: 18px;
    }}

    .section-header h3 {{
      margin: 0;
      font-size: clamp(22px, 3vw, 32px);
      letter-spacing: 0;
    }}

    .section-header p {{
      max-width: 680px;
      margin: 6px 0 0;
      color: var(--muted);
    }}

    .controls {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .seg {{
      min-height: 36px;
      padding: 0 12px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: #fff;
      cursor: pointer;
    }}

    .seg.active {{
      background: #173d3a;
      border-color: #173d3a;
      color: #fff;
    }}

    .license-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
    }}

    .license-card {{
      min-height: 254px;
      padding: 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      box-shadow: 0 10px 22px rgba(21, 33, 47, .04);
      display: grid;
      grid-template-rows: auto auto 1fr auto;
      gap: 10px;
      text-decoration: none;
      cursor: pointer;
    }}

    .license-card:hover {{
      transform: translateY(-2px);
      box-shadow: var(--shadow);
    }}

    .license-card h4 {{
      margin: 0;
      font-size: 22px;
    }}

    .license-card p {{
      margin: 0;
      color: #4e5a67;
    }}

    .card-top {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: start;
    }}

    .accent {{
      width: 38px;
      height: 6px;
      border-radius: 999px;
      background: var(--bank);
    }}

    [data-tone="payment"] .accent {{ background: var(--pay); }}
    [data-tone="asset"] .accent {{ background: var(--asset); }}
    [data-tone="digital"] .accent {{ background: var(--digital); }}
    [data-tone="data"] .accent {{ background: var(--data); }}
    [data-tone="market"] .accent {{ background: var(--market); }}
    [data-tone="rural"] .accent {{ background: var(--rural); }}

    .card-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}

    .matrix-wrap {{
      overflow-x: auto;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
    }}

    th, td {{
      padding: 13px 14px;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
      text-align: left;
      min-width: 150px;
    }}

    th {{
      background: #f2f5f4;
      color: #344150;
      font-size: 12px;
      text-transform: uppercase;
    }}

    tr:last-child td {{ border-bottom: 0; }}

    .detail-hero {{
      padding: 34px clamp(18px, 4vw, 54px) 22px;
      border-bottom: 1px solid var(--line);
      background: #fff;
    }}

    .detail-title {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 22px;
      align-items: start;
    }}

    .detail-title h2 {{
      margin: 10px 0 8px;
      font-size: clamp(34px, 5vw, 58px);
      line-height: 1.06;
      letter-spacing: 0;
    }}

    .detail-title p {{
      margin: 0;
      max-width: 860px;
      color: #4b5866;
      font-size: 18px;
    }}

    .quick-metrics {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-top: 22px;
    }}

    .metric {{
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #f9faf8;
      min-height: 116px;
    }}

    .metric span {{
      display: block;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      margin-bottom: 6px;
    }}

    .metric strong {{
      display: block;
      font-size: 14px;
      font-weight: 700;
    }}

    .detail-layout {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) 340px;
      gap: 24px;
      padding: 30px clamp(18px, 4vw, 54px);
    }}

    .detail-main {{
      display: grid;
      gap: 24px;
      min-width: 0;
    }}

    .info-band {{
      padding: 0;
    }}

    .info-band h3, .side-panel h3 {{
      margin: 0 0 12px;
      font-size: 20px;
    }}

    .list {{
      display: grid;
      gap: 9px;
      margin: 0;
      padding: 0;
      list-style: none;
    }}

    .list li {{
      position: relative;
      padding-left: 18px;
      color: #394655;
    }}

    .list li::before {{
      content: "";
      position: absolute;
      left: 0;
      top: .75em;
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #1c6f69;
    }}

    .two-col {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(300px, 360px);
      gap: 20px;
    }}

    .competitor-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }}

    .competitor {{
      min-height: 132px;
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
    }}

    .competitor strong {{
      display: block;
      margin-bottom: 5px;
      font-size: 16px;
    }}

    .competitor p {{
      margin: 0 0 8px;
      color: #4c5968;
    }}

    .competitor small {{
      color: var(--muted);
    }}

    .competitor-compare {{
      display: grid;
      gap: 14px;
    }}

    .competitor-lens {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
    }}

    .lens-card {{
      padding: 13px;
      border: 1px solid #d8e5e1;
      border-left: 4px solid #1c6f69;
      border-radius: 8px;
      background: #f8fbfa;
    }}

    .lens-card span {{
      display: inline-flex;
      margin-bottom: 6px;
      color: #1c6f69;
      font-size: 12px;
      font-weight: 800;
    }}

    .lens-card strong {{
      display: block;
      margin-bottom: 6px;
      color: var(--ink);
      font-size: 15px;
    }}

    .lens-card p {{
      margin: 0;
      color: #4d5b69;
      font-size: 13px;
      line-height: 1.55;
    }}

    .competitor-table-wrap {{
      overflow-x: auto;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
    }}

    .competitor-table {{
      min-width: 980px;
    }}

    .competitor-row {{
      display: grid;
      grid-template-columns: 1.1fr 1.05fr 1.1fr 1.25fr 1.35fr;
      border-top: 1px solid var(--line);
    }}

    .competitor-row:first-child {{
      border-top: 0;
    }}

    .competitor-row > div {{
      padding: 13px 14px;
      border-left: 1px solid var(--line);
      line-height: 1.55;
    }}

    .competitor-row > div:first-child {{
      border-left: 0;
    }}

    .competitor-head {{
      background: #eef6f3;
      color: #1d4f4c;
      font-size: 12px;
      font-weight: 900;
      letter-spacing: .04em;
      text-transform: uppercase;
    }}

    .competitor-name strong {{
      display: block;
      color: var(--ink);
      font-size: 16px;
    }}

    .competitor-name span {{
      display: inline-flex;
      margin-top: 7px;
      padding: 3px 8px;
      border: 1px solid #d7e4e0;
      border-radius: 999px;
      color: #526171;
      font-size: 12px;
      background: #f8fbfa;
    }}

    .competitor-scale {{
      color: #15202d;
      font-weight: 750;
    }}

    .competitor-cell-muted {{
      color: #485665;
    }}

    .side-panel {{
      position: sticky;
      top: 22px;
      align-self: start;
      display: grid;
      gap: 18px;
    }}

    .aside-box {{
      padding: 15px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
    }}

    .rule {{
      padding: 10px 0;
      border-bottom: 1px solid var(--line);
    }}

    .rule:last-child {{ border-bottom: 0; }}

    .rule strong {{
      display: block;
      margin-bottom: 4px;
    }}

    .rule .briefing-meta {{
      margin: 4px 0 6px;
    }}

    .rule p {{
      margin: 0;
      color: #566270;
      font-size: 13px;
    }}

    .source-list {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }}

    .source-section {{
      margin-top: 18px;
      padding-top: 16px;
      border-top: 1px solid var(--line);
    }}

    .source-section h4 {{
      margin: 0 0 10px;
      font-size: 18px;
    }}

    .briefing-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      margin-top: 14px;
    }}

    .briefing-card {{
      min-height: 214px;
      padding: 15px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      display: grid;
      gap: 10px;
      align-content: start;
      box-shadow: 0 8px 20px rgba(21, 33, 47, .04);
    }}

    .briefing-top {{
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: start;
    }}

    .briefing-card h4 {{
      margin: 0;
      font-size: 18px;
      line-height: 1.3;
    }}

    .briefing-card p {{
      margin: 0;
      color: #4c5968;
    }}

    .briefing-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}

    .briefing-action {{
      padding: 10px 11px;
      border-radius: 8px;
      background: #f5f7f3;
      color: #334353;
      font-size: 13px;
    }}

    .briefing-search {{
      padding-top: 2px;
      color: var(--muted);
      font-size: 12px;
      overflow-wrap: anywhere;
    }}

    .briefing-source {{
      width: fit-content;
      min-height: 32px;
      display: inline-flex;
      align-items: center;
      padding: 0 10px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfcfd;
      color: #173d3a;
      font-size: 13px;
      font-weight: 700;
      text-decoration: none;
    }}

    .briefing-source-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
    }}

    .briefing-source:hover {{
      border-color: #9cb9b1;
      background: #eef6f2;
    }}

    .briefing-status {{
      color: #697584;
      font-size: 12px;
    }}

    .source-link {{
      display: grid;
      gap: 6px;
      padding: 10px 11px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      text-decoration: none;
    }}

    .source-link.source-muted {{
      background: #f7f8f6;
      color: #5d6875;
    }}

    .source-head {{
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: center;
    }}

    .source-link p {{
      margin: 0;
      color: #566270;
      font-size: 13px;
    }}

    .source-link code {{
      padding: 2px 5px;
      border-radius: 6px;
      background: #f0f3f5;
      color: #334353;
      white-space: normal;
    }}

    .source-head span:last-child {{
      color: var(--muted);
      font-size: 12px;
      white-space: nowrap;
    }}

    .update-note {{
      border-left: 4px solid #1c6f69;
      padding: 12px 14px;
      background: #eef6f2;
      color: #394655;
      border-radius: 0 8px 8px 0;
      margin-bottom: 0;
    }}

    .devlog-shell {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      overflow: hidden;
    }}

    .devlog-entry {{
      display: grid;
      grid-template-columns: 142px 1fr;
      gap: 18px;
      padding: 18px;
      border-top: 1px solid var(--line);
    }}

    .devlog-entry:first-child {{
      border-top: 0;
    }}

    .devlog-date {{
      color: #435262;
      font-weight: 800;
      line-height: 1.5;
    }}

    .devlog-type {{
      display: inline-flex;
      width: fit-content;
      margin-top: 8px;
      padding: 3px 8px;
      border: 1px solid var(--line);
      border-radius: 999px;
      color: #627181;
      font-size: 12px;
      font-weight: 700;
      background: #f7f8f6;
    }}

    .devlog-body {{
      display: grid;
      gap: 9px;
    }}

    .devlog-title {{
      color: var(--ink);
      font-size: 18px;
      font-weight: 900;
      line-height: 1.35;
    }}

    .devlog-body p {{
      margin: 0;
      color: #526170;
    }}

    .devlog-list {{
      display: grid;
      gap: 7px;
      margin: 0;
      padding: 0;
      list-style: none;
    }}

    .devlog-list li {{
      position: relative;
      padding-left: 16px;
      color: #344454;
    }}

    .devlog-list li::before {{
      content: "";
      position: absolute;
      left: 0;
      top: .68em;
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #1c6f69;
    }}

    .footer {{
      padding: 24px clamp(18px, 4vw, 54px);
      border-top: 1px solid var(--line);
      color: var(--muted);
      font-size: 12px;
    }}

    @media (max-width: 1120px) {{
      .hero-grid {{ grid-template-columns: 1fr; }}
      .regulator-section {{ grid-template-columns: 1fr; }}
      .regulator-identity {{ border-right: 0; border-bottom: 1px solid var(--line); }}
      .regulator-grid {{ grid-template-columns: 1fr; }}
      .regulator-mindmap {{
        grid-template-columns: 1fr;
        padding-top: 0;
      }}
      .regulator-mindmap::before,
      .mindmap-branch::before {{ display: none; }}
      .mindmap-center {{
        position: static;
        transform: none;
        justify-self: start;
        margin-bottom: 2px;
      }}
      .quick-metrics {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .detail-layout {{ grid-template-columns: 1fr; }}
      .side-panel {{ position: static; }}
      .license-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .competitor-lens {{ grid-template-columns: 1fr; }}
    }}

    @media (max-width: 720px) {{
      body {{ font-size: 14px; }}
      .hero {{ min-height: auto; padding-top: 26px; }}
      .map-grid, .license-grid, .quick-metrics, .two-col, .competitor-grid, .briefing-grid, .source-list, .module-hub {{
        grid-template-columns: 1fr;
      }}
      .home-dynamic-strip {{ grid-auto-columns: minmax(260px, 86vw); }}
      .regulator-summary {{ grid-template-columns: 1fr; }}
      .regulator-watch {{ grid-template-columns: 1fr; }}
      .devlog-entry {{ grid-template-columns: 1fr; gap: 10px; }}
      .detail-title {{ grid-template-columns: 1fr; }}
      .section-header {{ display: block; }}
      .controls {{ margin-top: 12px; }}
      th, td {{ min-width: 220px; }}
    }}
  </style>
</head>
<body>
  <div class="mobile-bar">
    <select id="mobileNav" aria-label="页面导航"></select>
  </div>
  <div class="app-shell">
    <main>
      <section id="homePage" class="page active">
        <div class="hero home-hub" id="homeHub">
          <div class="hero-grid">
            <div>
              <span class="eyebrow">Indonesia Financial Licenses</span>
              <h2>印尼核心金融牌照监管机构图景</h2>
              <p class="hero-copy">以 OJK 与 Bank Indonesia 的监管分工为主轴，覆盖商业银行、Multi-Finance、P2P、PJP、BPR、ICS 和 Loan Aggregator 七类当前重点牌照。</p>
              <div class="hero-actions">
                <a class="btn primary" href="#module/licenses">牌照库</a>
                <a class="btn" href="#module/regulators">监管结构</a>
                <a class="btn" href="#module/updates">监管动态</a>
              </div>
            </div>
            <div class="module-hub" aria-label="模块入口">
              <a class="module-card" href="#module/regulators">
                <div><strong>监管结构</strong><p>查看 OJK、BI、LPS、Komdigi 的职责边界和监管抓手。</p></div>
                <span class="tag">OJK + BI</span>
              </a>
              <a class="module-card" href="#module/licenses">
                <div><strong>牌照库</strong><p>从七类核心牌照进入子页面，查看资本、外资、业务范围和限制。</p></div>
                <span class="tag">7 Licenses</span>
              </a>
              <a class="module-card" href="#module/compare">
                <div><strong>横向对比</strong><p>快速比较监管机构、最低资本、外资控制和玩家存量。</p></div>
                <span class="tag">Matrix</span>
              </a>
              <a class="module-card" href="#module/updates">
                <div><strong>监管动态历史</strong><p>回看每日联网检索生成的监管动态简报和来源链接。</p></div>
                <span class="tag">Daily</span>
              </a>
              <a class="module-card" href="#module/developer-log">
                <div><strong>开发者日志</strong><p>查看网站功能、数据管道和展示逻辑做过哪些调整。</p></div>
                <span class="tag">Changelog</span>
              </a>
            </div>
          </div>
          <div>
            <div class="mini-tags">
              <span class="tag">商业银行</span><span class="tag">Multi-Finance</span><span class="tag">P2P</span><span class="tag">PJP</span><span class="tag">BPR</span><span class="tag">ICS</span><span class="tag">Loan Aggregator</span>
            </div>
          </div>
        </div>

        <section id="homeDynamics" class="home-dynamics">
          <div class="section-header">
            <div>
              <span class="eyebrow">Regulatory Watch</span>
              <h3>监管动态</h3>
              <p>首页先展示最新几条监管动态；需要回看更早条目时，进入历史列表。</p>
            </div>
            <div class="controls">
              <a class="btn" href="#module/updates">查看历史</a>
            </div>
          </div>
          <div class="home-dynamic-strip" id="homeDynamicList" aria-label="最新监管动态"></div>
        </section>

        <section id="module-regulators" class="section module-page" data-module-page="regulators">
          <div class="module-kicker"><button class="btn" onclick="setRoute('home')">返回模块首页</button></div>
          <div class="section-header">
            <div>
              <h3>监管结构</h3>
              <p>按部门拆开阅读：每个机构独立说明职责、覆盖牌照、监管抓手，以及它对当前牌照路径的实际影响。</p>
            </div>
          </div>
          <div class="regulator-stack" id="regulatorSections"></div>
        </section>

        <section id="module-licenses" class="section module-page" data-module-page="licenses">
          <div class="module-kicker"><button class="btn" onclick="setRoute('home')">返回模块首页</button></div>
          <div class="section-header">
            <div>
              <h3>研究牌照</h3>
              <p>每张牌照进入后可阅读业务范围、资本门槛、外资控制、玩家存量、限制、竞品和法规索引。</p>
            </div>
            <div class="controls" id="categoryFilters"></div>
          </div>
          <div class="license-grid" id="licenseGrid"></div>
        </section>

        <section id="module-compare" class="section module-page" data-module-page="compare">
          <div class="module-kicker"><button class="btn" onclick="setRoute('home')">返回模块首页</button></div>
          <div class="section-header">
            <div>
              <h3>牌照横向对比</h3>
              <p>先从监管机构、资本、外资和存量数量判断进入路径，再进入各子页面看细项。</p>
            </div>
          </div>
          <div class="matrix-wrap">
            <table id="licenseMatrix"></table>
          </div>
        </section>

        <section id="module-updates" class="section module-page" data-module-page="updates">
          <div class="module-kicker"><button class="btn" onclick="setRoute('home')">返回模块首页</button></div>
          <div class="section-header">
            <div>
              <h3>监管动态历史</h3>
              <p>保留网站创建以来每日联网检索收录过的监管简报；首页只展示最新几条，完整记录在这里回看。</p>
            </div>
          </div>
          <div class="update-note" id="updateStatus">当前显示静态 HTML 内置监管动态历史；部署到网站后，页面会优先读取每日联网检索累积生成的 regulatory-history.json。</div>
          <div class="briefing-grid" id="briefingGrid"></div>
        </section>

        <section id="module-developer-log" class="section module-page" data-module-page="developer-log">
          <div class="module-kicker"><button class="btn" onclick="setRoute('home')">返回模块首页</button></div>
          <div class="section-header">
            <div>
              <h3>开发者日志</h3>
              <p>记录网站本身做过的功能、数据和维护动作，便于协作方理解页面为什么变成现在这样。</p>
            </div>
          </div>
          <div class="devlog-shell" id="developerLogList"></div>
        </section>

        <div class="footer">本页面为内部研究材料可视化，不构成法律意见。字段来自用户提供的 7 份 PDF，并按 2026-07-16 快照组织。</div>
      </section>

      <section id="detailPage" class="page"></section>
    </main>
  </div>

  <script>
    const LICENSES = {json.dumps(licenses, ensure_ascii=False)};
    const REGULATORS = {json.dumps(regulator_map, ensure_ascii=False)};
    const SOURCES = {json.dumps(sources, ensure_ascii=False)};
    const BUILT_IN_BRIEFINGS = {json.dumps(regulatory_briefings, ensure_ascii=False)};
    const BUILT_IN_DEV_LOG = {json.dumps(developer_log, ensure_ascii=False)};
    const BUILT_IN_UPDATE_SNAPSHOT = {json.dumps(embedded_update_snapshot, ensure_ascii=False)};
    const BUILT_IN_HISTORY_SNAPSHOT = {json.dumps(embedded_history_snapshot, ensure_ascii=False)};
    const KNOWN_PUBLISHED_DATES = {json.dumps(KNOWN_PUBLISHED_DATES, ensure_ascii=False)};
    const STATIC_HTML_MODE = window.location.protocol === "file:";
    let activeFilter = "全部";
    let externalUpdates = null;
    let activeBriefings = Array.isArray(BUILT_IN_HISTORY_SNAPSHOT.briefings) && BUILT_IN_HISTORY_SNAPSHOT.briefings.length
      ? BUILT_IN_HISTORY_SNAPSHOT.briefings
      : BUILT_IN_BRIEFINGS;
    let activeDeveloperLog = BUILT_IN_DEV_LOG;

    const qs = (sel, root = document) => root.querySelector(sel);
    const qsa = (sel, root = document) => [...root.querySelectorAll(sel)];
    const esc = (value) => String(value ?? "").replace(/[&<>"']/g, char => ({{ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }}[char]));
    const uniq = (items) => [...new Set((items || []).filter(Boolean))];

    function setRoute(route) {{
      if (route === "home") {{
        location.hash = "";
      }} else if (String(route).startsWith("module/")) {{
        location.hash = route;
      }} else {{
        location.hash = "license/" + route;
      }}
    }}

    function setModule(moduleId) {{
      location.hash = "module/" + moduleId;
    }}

    function currentRoute() {{
      const hash = decodeURIComponent(location.hash.replace(/^#/, ""));
      if (!hash || hash === "home") return {{ page: "home" }};
      const legacyModules = {{ regulators: "regulators", licenses: "licenses", sources: "updates", developerLog: "developer-log", compare: "compare" }};
      if (legacyModules[hash]) return {{ page: "module", id: legacyModules[hash] }};
      const moduleMatch = hash.match(/^module\\/(.+)$/);
      if (moduleMatch) return {{ page: "module", id: moduleMatch[1] }};
      const match = hash.match(/^license\\/(.+)$/);
      if (match) return {{ page: "license", id: match[1] }};
      return {{ page: "home" }};
    }}

    function renderNav() {{
      const moduleOptions = [
        ["regulators", "监管结构"],
        ["licenses", "牌照库"],
        ["compare", "横向对比"],
        ["updates", "监管动态"],
        ["developer-log", "开发者日志"],
      ];
      const mobile = qs("#mobileNav");
      mobile.innerHTML = `<option value="home">模块首页</option>`
        + moduleOptions.map(item => `<option value="module:${{esc(item[0])}}">${{esc(item[1])}}</option>`).join("")
        + LICENSES.map(item => `<option value="${{esc(item.id)}}">${{esc(item.name)}} - ${{esc(item.subtitle)}}</option>`).join("");
      mobile.addEventListener("change", e => {{
        const value = e.target.value;
        if (value.startsWith("module:")) setModule(value.slice(7));
        else setRoute(value);
      }});

      qsa("[data-route]").forEach(btn => btn.addEventListener("click", () => setRoute(btn.dataset.route)));
      qsa("[data-module-route]").forEach(btn => btn.addEventListener("click", () => setModule(btn.dataset.moduleRoute)));
    }}

    function mindmapBranch(label, items, tone) {{
      return `
        <section class="mindmap-branch" data-tone="${{esc(tone || "")}}">
          <div class="mindmap-branch-title">${{esc(label)}}</div>
          <ul class="regulator-watch">${{(items || []).map(x => `<li>${{esc(x)}}</li>`).join("")}}</ul>
        </section>
      `;
    }}

    function renderRegulators() {{
      qs("#regulatorSections").innerHTML = REGULATORS.map(r => `
        <article class="regulator-section">
          <div class="regulator-identity">
            <h4>${{esc(r.name)}}</h4>
            <div class="regulator-full">${{esc(r.full)}}</div>
            <p class="regulator-focus">${{esc(r.focus || "")}}</p>
            <div class="mini-tags">${{r.licenses.map(x => `<span class="tag">${{esc(x)}}</span>`).join("")}}</div>
          </div>
          <div class="regulator-content">
            <div class="regulator-summary">
              <div class="regulator-block">
                <strong>核心职责</strong>
                <p>${{esc(r.role)}}</p>
              </div>
              <div class="regulator-block">
                <strong>对当前牌照研究的意义</strong>
                <p>${{esc(r.importance || "")}}</p>
              </div>
            </div>
            <div class="regulator-mindmap" aria-label="${{esc(r.name)}} \u76d1\u7ba1\u8fb9\u754c mindmap">
              <div class="mindmap-center">
                <span>${{esc(r.name)}}</span>
                <strong>\u76d1\u7ba1\u8fb9\u754c</strong>
              </div>
              ${{mindmapBranch("\u5b83\u5177\u4f53\u51b3\u5b9a\u4ec0\u4e48", r.decides || [], "decides")}}
              ${{mindmapBranch("\u5b83\u4e0d\u8d1f\u8d23\u4ec0\u4e48", r.notInScope || [], "limits")}}
              ${{mindmapBranch("\u4ec0\u4e48\u65f6\u5019\u9700\u8981\u91cd\u70b9\u770b\u5b83", uniq([...(r.triggers || []), ...(r.watch || [])]), "triggers")}}
            </div>
            <div class="regulator-block regulator-footer">
              <strong>主要监管抓手</strong>
              <div class="mini-tags">${{r.signals.map(x => `<span class="tag">${{esc(x)}}</span>`).join("")}}</div>
            </div>
          </div>
        </article>
      `).join("");
    }}

    function categories() {{
      return ["全部", ...new Set(LICENSES.map(x => x.category))];
    }}

    function renderFilters() {{
      const el = qs("#categoryFilters");
      el.innerHTML = categories().map(c => `<button class="seg ${{c === activeFilter ? "active" : ""}}" data-filter="${{esc(c)}}">${{esc(c)}}</button>`).join("");
      qsa("[data-filter]", el).forEach(btn => btn.addEventListener("click", () => {{
        activeFilter = btn.dataset.filter;
        renderFilters();
        renderLicenseGrid();
      }}));
    }}

    function visibleLicenses() {{
      return activeFilter === "全部" ? LICENSES : LICENSES.filter(x => x.category === activeFilter);
    }}

    function renderLicenseGrid() {{
      qs("#licenseGrid").innerHTML = visibleLicenses().map(item => `
        <a class="license-card" data-tone="${{esc(item.tone)}}" href="#license/${{esc(item.id)}}">
          <div class="card-top">
            <div class="accent"></div>
            <span class="tag">${{esc(item.regulator)}}</span>
          </div>
          <div>
            <h4>${{esc(item.name)}}</h4>
            <div class="tag">${{esc(item.subtitle)}}</div>
          </div>
          <p>${{esc(item.oneLiner)}}</p>
          <div class="card-meta">
            <span class="tag">${{esc(item.category)}}</span>
            <span class="tag">${{esc(shortCapital(item.minCapital))}}</span>
          </div>
        </a>
      `).join("");
    }}

    function shortCapital(text) {{
      const match = String(text).match(/Rp[0-9.,\\s-]+(?:trillion|billion|million)?|IDR\\s?[0-9.,]+\\s?billion/i);
      return match ? match[0].replace(/\\s+/g, " ") : "资本见详情";
    }}

    function renderMatrix() {{
      qs("#licenseMatrix").innerHTML = `
        <thead><tr><th>牌照</th><th>监管机构</th><th>业务定位</th><th>最低资本</th><th>外资/控制</th><th>玩家存量</th></tr></thead>
        <tbody>${{LICENSES.map(x => `
          <tr>
            <td><a href="#license/${{esc(x.id)}}"><strong>${{esc(x.name)}}</strong></a><br><span class="tag">${{esc(x.subtitle)}}</span></td>
            <td>${{esc(x.regulator)}}</td>
            <td>${{esc(x.oneLiner)}}</td>
            <td>${{esc(x.minCapital)}}</td>
            <td>${{esc(x.foreignOwnership)}}</td>
            <td>${{esc(x.playerCount)}}</td>
          </tr>`).join("")}}</tbody>
      `;
    }}

    function renderSources() {{
      const target = qs("#sourceLinks");
      if (!target) return;
      target.innerHTML = SOURCES.map(s => `
        <${{String(s.status || "").startsWith("已核验") ? `a class="source-link" href="${{esc(s.url)}}" target="_blank" rel="noreferrer"` : `div class="source-link source-muted"`}}>
          <span class="source-head"><span>${{esc(s.label)}}</span><span>${{esc(s.owner)}}</span></span>
          <p>${{esc(s.note)}}</p>
          <p>核验状态：<code>${{esc(s.status || "未核验")}}</code></p>
          <p>检索关键词：<code>${{esc(s.keyword)}}</code></p>
        </${{String(s.status || "").startsWith("已核验") ? "a" : "div"}}>
      `).join("");
    }}

    function briefingDateLabel(item) {{
      const published = item.publishedDate || item.issueDate || item.releaseDate || "";
      if (published) return "发布：" + published;
      if (String(item.date || "").length > 4) return "发布：" + item.date;
      return "发布：未解析具体日";
    }}

    function briefingSortValue(item) {{
      const value = item.publishedDate || (String(item.date || "").length > 4 ? item.date : `${{item.date || "1900"}}-01-01`);
      const time = Date.parse(value);
      return Number.isFinite(time) ? time : 0;
    }}

    function sortedBriefings() {{
      return [...activeBriefings].sort((a, b) => briefingSortValue(b) - briefingSortValue(a));
    }}

    function renderHomeDynamics() {{
      const target = qs("#homeDynamicList");
      if (!target) return;
      const items = sortedBriefings().slice(0, 4);
      target.innerHTML = items.length ? items.map(item => `
        <article class="home-dynamic-card">
          <div class="briefing-meta">
            <span class="tag">${{esc(briefingDateLabel(item))}}</span>
            <span class="tag">${{esc(item.regulator)}}</span>
            <span class="tag">影响：${{esc(item.level)}}</span>
          </div>
          <h4>${{esc(item.title)}}</h4>
          <div class="briefing-meta">
            ${{(item.licenses || []).slice(0, 3).map(x => `<span class="tag">${{esc(x)}}</span>`).join("")}}
          </div>
          <p><strong>摘要：</strong>${{esc(item.summary)}}</p>
          <div class="briefing-source-row">
            ${{item.sourceUrl ? `<a class="briefing-source" href="${{esc(item.sourceUrl)}}" target="_blank" rel="noreferrer">${{esc(item.sourceLabel || "查看来源")}}</a>` : ""}}
          </div>
        </article>
      `).join("") : `<div class="update-note">暂无可展示的监管动态。</div>`;
    }}

    function renderBriefings() {{
      qs("#briefingGrid").innerHTML = sortedBriefings().map(item => `
        <article class="briefing-card">
          <div class="briefing-top">
            <div>
              <h4>${{esc(item.title)}}</h4>
              <div class="briefing-meta">
                <span class="tag">${{esc(briefingDateLabel(item))}}</span>
                ${{item.firstSeenDate ? `<span class="tag">首次收录：${{esc(item.firstSeenDate)}}</span>` : ""}}
                <span class="tag">${{esc(item.regulator)}}</span>
                <span class="tag">影响：${{esc(item.level)}}</span>
              </div>
            </div>
          </div>
          <div class="briefing-meta">
            ${{(item.licenses || []).map(x => `<span class="tag">${{esc(x)}}</span>`).join("")}}
          </div>
          <p><strong>摘要：</strong>${{esc(item.summary)}}</p>
          <p><strong>影响：</strong>${{esc(item.impact)}}</p>
          <div class="briefing-action"><strong>建议动作：</strong>${{esc(item.action)}}</div>
          <div class="briefing-search">法规关键词：${{esc(item.keywords)}}</div>
          <div class="briefing-source-row">
            ${{item.sourceUrl ? `<a class="briefing-source" href="${{esc(item.sourceUrl)}}" target="_blank" rel="noreferrer">${{esc(item.sourceLabel || "查看来源")}}</a>` : ""}}
            ${{item.sourceAltUrl ? `<a class="briefing-source" href="${{esc(item.sourceAltUrl)}}" target="_blank" rel="noreferrer">${{esc(item.sourceAltLabel || "备用链接")}}</a>` : ""}}
          </div>
          ${{item.sourceStatus ? `<div class="briefing-status">${{esc(item.sourceStatus)}}</div>` : ""}}
        </article>
      `).join("");
    }}

    function renderDeveloperLog() {{
      const target = qs("#developerLogList");
      if (!target) return;
      target.innerHTML = activeDeveloperLog.map(entry => `
        <article class="devlog-entry">
          <div>
            <div class="devlog-date">${{esc(entry.date)}}</div>
            <div class="devlog-type">${{esc(entry.type || "更新")}}</div>
          </div>
          <div class="devlog-body">
            <div class="devlog-title">${{esc(entry.title)}}</div>
            <p>${{esc(entry.summary || "")}}</p>
            <ul class="devlog-list">
              ${{(entry.changes || []).map(change => `<li>${{esc(change)}}</li>`).join("")}}
            </ul>
          </div>
        </article>
      `).join("");
    }}

    function arrayList(items) {{
      return `<ul class="list">${{items.map(item => `<li>${{esc(item)}}</li>`).join("")}}</ul>`;
    }}

    function renderCompetitors(item) {{
      const hasComparison = (item.competitorLens || []).length || item.competitors.some(c => c.scale || c.edge || c.implication);
      if (!hasComparison) {{
        return `
          <div class="competitor-grid">
            ${{item.competitors.map(c => `
              <article class="competitor">
                <strong>${{esc(c.name)}}</strong>
                <p>${{esc(c.position)}}</p>
                <small>${{esc(c.signal)}}</small>
              </article>
            `).join("")}}
          </div>
        `;
      }}

      return `
        <div class="competitor-compare">
          <div class="competitor-lens">
            ${{(item.competitorLens || []).map(lens => `
              <article class="lens-card">
                <span>${{esc(lens.label)}}</span>
                <strong>${{esc(lens.title)}}</strong>
                <p>${{esc(lens.note)}}</p>
              </article>
            `).join("")}}
          </div>
          <div class="competitor-table-wrap">
            <div class="competitor-table">
              <div class="competitor-row competitor-head">
                <div>玩家 / 类型</div>
                <div>行业体量</div>
                <div>主战场</div>
                <div>关键优势</div>
                <div>对我们意味着什么</div>
              </div>
              ${{item.competitors.map(c => `
                <div class="competitor-row">
                  <div class="competitor-name"><strong>${{esc(c.name)}}</strong><span>${{esc(c.tier || "")}}</span></div>
                  <div class="competitor-scale">${{esc(c.scale || c.signal || "")}}</div>
                  <div class="competitor-cell-muted">${{esc(c.position || "")}}</div>
                  <div class="competitor-cell-muted">${{esc(c.edge || c.signal || "")}}</div>
                  <div class="competitor-cell-muted">${{esc(c.implication || "")}}</div>
                </div>
              `).join("")}}
            </div>
          </div>
        </div>
      `;
    }}

    function detailPage(item) {{
      const rules = externalUpdates?.[item.id]?.length ? externalUpdates[item.id] : item.latestRules;
      return `
        <div class="detail-hero" data-tone="${{esc(item.tone)}}">
          <button class="btn" onclick="setRoute('home')">返回总览</button>
          <div class="detail-title">
            <div>
              <h2>${{esc(item.name)}}</h2>
              <p>${{esc(item.oneLiner)}}</p>
            </div>
            <div class="mini-tags">
              <span class="tag">${{esc(item.subtitle)}}</span>
              <span class="tag">${{esc(item.category)}}</span>
              <span class="tag">${{esc(item.regulator)}}</span>
            </div>
          </div>
          <div class="quick-metrics">
            <div class="metric"><span>牌照类型</span><strong>${{esc(item.type)}}</strong></div>
            <div class="metric"><span>最低资本金</span><strong>${{esc(item.minCapital)}}</strong></div>
            <div class="metric"><span>外资控股</span><strong>${{esc(item.foreignOwnership)}}</strong></div>
            <div class="metric"><span>玩家存量</span><strong>${{esc(item.playerCount)}}</strong></div>
          </div>
        </div>

        <div class="detail-layout">
          <div class="detail-main">
            <section class="info-band">
              <h3>允许开展的业务范围</h3>
              ${{arrayList(item.businessScope)}}
            </section>

            <section class="info-band">
              <h3>市场和经营信号</h3>
              ${{arrayList(item.market)}}
            </section>

            <section class="info-band">
              <h3>其他重要限制</h3>
              ${{arrayList(item.restrictions)}}
            </section>

            <section class="info-band">
              <h3>竞争对手板块</h3>
              ${{renderCompetitors(item)}}
            </section>
          </div>

          <aside class="side-panel">
            <div class="aside-box">
              <h3>最新监管规定</h3>
              ${{rules.map(r => `<div class="rule"><strong>${{r.sourceUrl ? `<a href="${{esc(r.sourceUrl)}}" target="_blank" rel="noreferrer">${{esc(r.name)}}</a>` : esc(r.name)}}</strong>${{r.publishedDate ? `<div class="briefing-meta"><span class="tag">发布：${{esc(r.publishedDate)}}</span></div>` : ""}}<p>${{esc(r.note || r.summary || "")}}</p></div>`).join("")}}
            </div>
            <div class="aside-box">
              <h3>法规索引</h3>
              ${{arrayList(item.legalIndex)}}
            </div>
            <div class="aside-box">
              <h3>来源文件</h3>
              <p>${{esc(item.sourceDoc)}}</p>
            </div>
          </aside>
        </div>
      `;
    }}

    function showModule(moduleId) {{
      qs("#homeHub")?.classList.toggle("hidden", Boolean(moduleId));
      qs("#homeDynamics")?.classList.toggle("hidden", Boolean(moduleId));
      qsa("[data-module-page]").forEach(section => {{
        section.classList.toggle("active", section.dataset.modulePage === moduleId);
      }});
    }}

    function renderRoute() {{
      const route = currentRoute();
      const home = qs("#homePage");
      const detail = qs("#detailPage");

      if (route.page === "license") {{
        const item = LICENSES.find(x => x.id === route.id) || LICENSES[0];
        home.classList.remove("active");
        detail.classList.add("active");
        showModule(null);
        detail.innerHTML = detailPage(item);
        qs("#mobileNav").value = item.id;
        window.scrollTo({{ top: 0, behavior: "instant" }});
      }} else if (route.page === "module") {{
        detail.classList.remove("active");
        home.classList.add("active");
        showModule(route.id);
        qs("#mobileNav").value = "module:" + route.id;
        window.scrollTo({{ top: 0, behavior: "instant" }});
      }} else {{
        detail.classList.remove("active");
        home.classList.add("active");
        showModule(null);
        qs("#mobileNav").value = "home";
        window.scrollTo({{ top: 0, behavior: "instant" }});
      }}
    }}

    function enrichBriefingDate(item) {{
      if (!item || item.publishedDate) return item;
      const text = [item.title, item.name, item.sourceUrl, item.sourceOriginalTitle, item.keywords, item.note]
        .filter(Boolean)
        .join(" ");
      for (const [marker, publishedDate] of Object.entries(KNOWN_PUBLISHED_DATES)) {{
        if (text.includes(marker)) {{
          item.publishedDate = publishedDate;
          break;
        }}
      }}
      return item;
    }}

    function normalizeUpdateSnapshot(data) {{
      if (!data || typeof data !== "object") return data;
      if (Array.isArray(data.briefings)) data.briefings.forEach(enrichBriefingDate);
      Object.values(data.licenses || {{}}).forEach(items => (items || []).forEach(enrichBriefingDate));
      return data;
    }}

    function applyUpdateSnapshot(data, mode) {{
      data = normalizeUpdateSnapshot(data);
      if (!data || typeof data !== "object") return false;
      externalUpdates = data.licenses || null;
      if (Array.isArray(data.briefings) && data.briefings.length) activeBriefings = data.briefings;
      const checked = Array.isArray(data.sourcesChecked) ? data.sourcesChecked.filter(s => s.ok).length : 0;
      const sourceText = checked ? "，本次成功检查 " + checked + " 个官方入口" : "";
      const generatedAt = data.generatedAt || data.generatedDate || "时间未记录";
      const total = Array.isArray(data.briefings) ? data.briefings.length : 0;
      const status = mode === "history"
        ? "已加载网站监管动态历史库：" + generatedAt + "，累计 " + total + " 条简报" + sourceText + "。首页展示最新几条，历史页保留全部收录记录。"
        : mode === "external"
          ? "未读取到历史库，已加载网站每日联网检索快照：" + generatedAt + sourceText + "。历史页暂时显示本次快照。"
          : "当前显示静态 HTML 内置监管动态历史：" + generatedAt + "，累计 " + total + " 条简报" + sourceText + "。部署后会优先读取 regulatory-history.json。";
      qs("#updateStatus").textContent = status;
      return true;
    }}

    async function loadExternalUpdates() {{
      const hasEmbeddedHistory = applyUpdateSnapshot(BUILT_IN_HISTORY_SNAPSHOT, "static-history");
      if (STATIC_HTML_MODE) return;
      try {{
        const res = await fetch("regulatory-history.json?d=" + new Date().toISOString().slice(0, 10), {{ cache: "no-store" }});
        if (!res.ok) return;
        const data = await res.json();
        applyUpdateSnapshot(data, "history");
        return;
      }} catch (err) {{
        // Fall back to the latest snapshot below.
      }}
      try {{
        const res = await fetch("regulatory-updates.json?d=" + new Date().toISOString().slice(0, 10), {{ cache: "no-store" }});
        if (!res.ok) return;
        const data = await res.json();
        applyUpdateSnapshot(data, "external");
      }} catch (err) {{
        if (!hasEmbeddedHistory) externalUpdates = null;
      }}
    }}

    async function loadDeveloperLog() {{
      if (STATIC_HTML_MODE) {{
        activeDeveloperLog = BUILT_IN_DEV_LOG;
        return;
      }}
      try {{
        const res = await fetch("developer-log.json?d=" + new Date().toISOString().slice(0, 10), {{ cache: "no-store" }});
        if (!res.ok) return;
        const data = await res.json();
        activeDeveloperLog = Array.isArray(data) ? data : (data.entries || activeDeveloperLog);
      }} catch (err) {{
        activeDeveloperLog = BUILT_IN_DEV_LOG;
      }}
    }}

    async function init() {{
      renderNav();
      renderRegulators();
      renderFilters();
      renderLicenseGrid();
      renderMatrix();
      renderSources();
      await loadExternalUpdates();
      await loadDeveloperLog();
      renderHomeDynamics();
      renderBriefings();
      renderDeveloperLog();
      renderRoute();
      window.addEventListener("hashchange", renderRoute);
    }}

    init();
  </script>
</body>
</html>
"""


def main() -> None:
    for out in (OUT, STATIC_OUT, SITE_OUT):
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(dedent(html), encoding="utf-8")
    log_body = json.dumps({"entries": developer_log}, ensure_ascii=False, indent=2) + "\n"
    for out in (DEVLOG_PUBLIC, DEVLOG_DATA):
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(log_body, encoding="utf-8")
    print(OUT)
    print(STATIC_OUT)
    print(SITE_OUT)
    print(DEVLOG_PUBLIC)


if __name__ == "__main__":
    main()
