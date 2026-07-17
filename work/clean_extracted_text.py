from pathlib import Path
import re

IN_DIR = Path(r"C:\Users\zhuangzihao\Documents\Codex\2026-07-16\new-chat\work\extracted")
OUT_DIR = Path(r"C:\Users\zhuangzihao\Documents\Codex\2026-07-16\new-chat\work\cleaned")


def collapse_doubled_run(match: re.Match) -> str:
    text = match.group(0)
    if len(text) % 2:
        return text
    half = len(text) // 2
    if text[:half] == text[half:]:
        return text[:half]
    # Handle per-character overprint, e.g. 商商业业 or RRpp1100.
    chars = []
    i = 0
    changed = False
    while i < len(text):
        if i + 1 < len(text) and text[i] == text[i + 1]:
            chars.append(text[i])
            i += 2
            changed = True
        else:
            chars.append(text[i])
            i += 1
    return "".join(chars) if changed else text


def clean(text: str) -> str:
    # Collapse obvious PDF overprint runs without touching normal prose too broadly.
    text = re.sub(r"([\u4e00-\u9fffA-Za-z0-9%$.,_/()·+：:；;，、。！？《》“”\"'\-]){4,}", collapse_doubled_run, text)
    text = re.sub(r"([A-Za-z0-9%$.,_/()·+：:；;，、。！？《》“”\"'\-])\1{1,}", lambda m: m.group(1), text)
    text = re.sub(r"([\u4e00-\u9fff])\1", lambda m: m.group(1), text)
    return text


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for path in IN_DIR.glob("*.txt"):
        out = OUT_DIR / path.name
        out.write_text(clean(path.read_text(encoding="utf-8")), encoding="utf-8")
        print(out.name)


if __name__ == "__main__":
    main()
