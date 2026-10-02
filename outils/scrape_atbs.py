"""Download Automate the Boring Stuff (3e) and its Workbook as HTML + Markdown.

Both are published free under CC BY-NC-SA. Personal study copy only.
"""
import re
import sys
import time
from pathlib import Path

import html2text
import requests

OUT = Path(r"C:\utils\ccna\ressources\automate-the-boring-stuff")
HEADERS = {"User-Agent": "Mozilla/5.0 (personal study archive; contact: local)"}
DELAY = 1.0  # seconds between requests, be polite

BOOK_BASE = "https://automatetheboringstuff.com/3e/"
BOOK_PAGES = ["chapter0"] + [f"chapter{i}" for i in range(1, 25)] + ["appendixa", "appendixb"]

WB_BASE = "https://inventwithpython.com/automate3workbook/"
WB_PAGES = ["front", "introduction"] + [f"chapter{i}" for i in range(1, 25)] + ["answers"]

conv = html2text.HTML2Text()
conv.body_width = 0
conv.ignore_images = False
conv.protect_links = True
conv.mark_code = True


def title_of(html: str, fallback: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else fallback


def fetch(url: str) -> str | None:
    for attempt in range(3):
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 200:
                r.encoding = r.apparent_encoding or "utf-8"
                return r.text
            print(f"  HTTP {r.status_code} for {url}", file=sys.stderr)
            if r.status_code == 404:
                return None
        except requests.RequestException as e:
            print(f"  error {e} (attempt {attempt + 1})", file=sys.stderr)
        time.sleep(2 * (attempt + 1))
    return None


def grab(base: str, pages: list[str], subdir: str, index_title: str) -> list[tuple[str, str]]:
    html_dir = OUT / subdir / "html"
    md_dir = OUT / subdir / "markdown"
    html_dir.mkdir(parents=True, exist_ok=True)
    md_dir.mkdir(parents=True, exist_ok=True)
    got: list[tuple[str, str]] = []
    for i, page in enumerate(pages):
        url = f"{base}{page}.html"
        print(f"[{subdir}] {url}")
        html = fetch(url)
        if html is None:
            print("  skipped", file=sys.stderr)
            continue
        (html_dir / f"{page}.html").write_text(html, encoding="utf-8")
        md = conv.handle(html)
        # Make relative links point back to the site so they still work.
        md = md.replace("](/", f"]({base.rsplit('/', 2)[0]}/")
        name = f"{i:02d}-{page}.md"
        (md_dir / name).write_text(f"<!-- source: {url} -->\n\n{md}", encoding="utf-8")
        got.append((name, title_of(html, page)))
        time.sleep(DELAY)
    index = [f"# {index_title}", "", f"Source : {base}", "", "| Fichier | Titre |", "| :--- | :--- |"]
    index += [f"| [{n}](markdown/{n}) | {t} |" for n, t in got]
    (OUT / subdir / "INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    return got


if __name__ == "__main__":
    book = grab(BOOK_BASE, BOOK_PAGES, "book-3e", "Automate the Boring Stuff with Python, 3rd Edition (Al Sweigart)")
    wb = grab(WB_BASE, WB_PAGES, "workbook", "Automate the Boring Stuff Workbook (Al Sweigart)")
    print(f"\nbook: {len(book)}/{len(BOOK_PAGES)} pages, workbook: {len(wb)}/{len(WB_PAGES)} pages")
