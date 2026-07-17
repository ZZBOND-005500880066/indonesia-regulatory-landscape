from pathlib import Path
import json
import pdfplumber

BASE = Path(r"C:\Users\zhuangzihao\Desktop\印尼金融牌照")
OUT = Path(r"C:\Users\zhuangzihao\Documents\Codex\2026-07-16\new-chat\work\extracted")

FILES = [
    "印尼BPR（村镇银行）收购_202602_副本.pdf",
    "印尼ICS+(另类征信)监管规定与投入路径讨论决策_202605_副本.pdf",
    "印尼Loan Aggregator研究_202607.pdf",
    "印尼Multi-Finance研究_202607.pdf",
    "印尼P2P研究.pdf",
    "印尼商业银行研究_202607.pdf",
    "印尼支付牌照与QRIS情况梳理_20260420_副本.pdf",
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    summary = []
    for name in FILES:
        path = BASE / name
        pages = []
        with pdfplumber.open(path) as pdf:
            for idx, page in enumerate(pdf.pages, start=1):
                text = page.extract_text(x_tolerance=1.5, y_tolerance=3) or ""
                pages.append({"page": idx, "text": text})
        stem = path.stem
        text_path = OUT / f"{stem}.txt"
        json_path = OUT / f"{stem}.json"
        text_path.write_text(
            "\n\n".join(f"--- page {p['page']} ---\n{p['text']}" for p in pages),
            encoding="utf-8",
        )
        json_path.write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
        summary.append({"file": name, "pages": len(pages), "chars": sum(len(p["text"]) for p in pages)})
    (OUT / "_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    for item in summary:
        print(f"{item['file']}\t{item['pages']} pages\t{item['chars']} chars")


if __name__ == "__main__":
    main()
