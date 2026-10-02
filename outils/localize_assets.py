#!/usr/bin/env python3
"""Rend les copies locales des livres d'Al Sweigart autonomes (aucun lien vers le web).

Pour chaque livre dans ressources/automate-the-boring-stuff/{book-3e,workbook} :
  1. supprime la bannière publicitaire en tête de chapitre ;
  2. télécharge la feuille de style, ses polices et toutes les images dans assets/ ;
  3. télécharge les fichiers d'exercices hébergés par l'auteur (autbor.com,
     inventwithpython.com/projects) dans assets/files/ ;
  4. remplace tout autre lien <a href="http..."> par son texte ;
  5. décode les adresses email protégées par Cloudflare ;
  6. régénère le Markdown depuis le HTML localisé.

Puis nettoie les fichiers de flashcards TSOFA (pied de page publicitaire, liens).

Les URL présentes dans les exemples de code du livre ne sont pas des liens : elles
sont conservées telles quelles.

Usage : python localize_assets.py  [--root DOSSIER]
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path, PurePosixPath
from urllib.parse import urljoin, urlparse

import html2text
import requests

ROOT = Path(__file__).resolve().parents[1] / "ressources" / "automate-the-boring-stuff"
BOOKS = {
    "book-3e": "https://automatetheboringstuff.com/3e/",
    "workbook": "https://inventwithpython.com/automate3workbook/",
}
# Hôtes dont on rapatrie les fichiers (exercices, exemples). Tout le reste devient du texte.
FILE_HOSTS = {"autbor.com", "inventwithpython.com", "automatetheboringstuff.com"}
HEADERS = {"User-Agent": "Mozilla/5.0 (personal study archive)"}
DELAY = 0.3

session = requests.Session()
session.headers.update(HEADERS)

conv = html2text.HTML2Text()
conv.body_width = 0
conv.ignore_images = False
conv.mark_code = True


# ---------- téléchargement ----------

def download(url: str, dest: Path, allow_redirect_host: str | None = None) -> bool:
    """Télécharge url vers dest. Refuse si la redirection finale quitte l'hôte attendu."""
    if dest.exists():
        return True
    try:
        r = session.get(url, timeout=30, allow_redirects=True)
    except requests.RequestException as e:
        print(f"    échec {url} : {e}", file=sys.stderr)
        return False
    time.sleep(DELAY)
    if r.status_code != 200:
        print(f"    HTTP {r.status_code} {url}", file=sys.stderr)
        return False
    if allow_redirect_host and urlparse(r.url).hostname not in FILE_HOSTS:
        print(f"    redirigé hors site, ignoré : {url} -> {r.url}", file=sys.stderr)
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(r.content)
    return True


def local_path_for(url: str, files_dir: Path) -> Path:
    """assets/files/<hôte>/<chemin>, les répertoires deviennent index.html."""
    u = urlparse(url)
    p = PurePosixPath(u.path or "/")
    if u.path.endswith("/") or not p.suffix:
        p = p / "index.html"
    return files_dir / u.hostname / Path(*p.parts[1:])


# ---------- réécriture HTML ----------

BANNER = re.compile(r'<div[^>]*id="closeable_ad_bar\d*">.*?</div>\s*', re.S)  # en tête et en pied de chapitre
# Sur inventwithpython.com, seuls les fichiers d'exemples et images sont des ressources ; le reste est du site web.
INVENT_ALLOWED_PREFIXES = ("/projects/", "/images/")
LOCAL_DENY = ("assets/files/inventwithpython.com/index.html", "assets/files/inventwithpython.com/blog/")
IMG = re.compile(r'<img\b([^>]*?)\bsrc="([^"]+)"([^>]*)>', re.S)
ANCHOR = re.compile(r'<a\b[^>]*?\bhref="([^"]*)"[^>]*>(.*?)</a>', re.S)
CF_EMAIL = re.compile(r"/cdn-cgi/l/email-protection#?([0-9a-fA-F]*)")


def decode_cf_email(hexstr: str) -> str:
    if len(hexstr) < 4:
        return "[email protégé]"
    key = int(hexstr[:2], 16)
    return "".join(chr(int(hexstr[i:i + 2], 16) ^ key) for i in range(2, len(hexstr), 2))


def localize_html(html: str, base: str, book_dir: Path, stats: dict) -> str:
    assets = book_dir / "assets"
    html = BANNER.sub("", html)
    html = html.replace('href="style.css"', 'href="../assets/style.css"')

    def img_repl(m: re.Match) -> str:
        before, src, after = m.groups()
        if src.startswith("../assets/"):
            return m.group(0)
        if src.startswith("/"):  # vignettes de la bannière, hors contenu
            stats["img_dropped"] += 1
            return ""
        url = urljoin(base, src)
        name = PurePosixPath(urlparse(url).path).name
        dest = assets / "images" / name
        if download(url, dest):
            stats["img"] += 1
            return f'<img{before}src="../assets/images/{name}"{after}>'
        stats["img_failed"] += 1
        return m.group(0)

    html = IMG.sub(img_repl, html)

    def a_repl(m: re.Match) -> str:
        href, inner = m.groups()
        if href.startswith("#"):
            return m.group(0)
        if href.startswith("../assets/"):
            if any(d in href for d in LOCAL_DENY):
                stats["links_stripped"] += 1
                return inner
            return m.group(0)
        cf = CF_EMAIL.search(href)
        if cf:
            stats["email"] += 1
            return decode_cf_email(cf.group(1))
        if "<img" in inner:  # lien-image résiduel de bannière
            return ""
        url = urljoin(base, href)
        parsed = urlparse(url)
        host = parsed.hostname or ""
        downloadable = host in FILE_HOSTS and not parsed.fragment
        if host == "inventwithpython.com" and not parsed.path.startswith(INVENT_ALLOWED_PREFIXES):
            downloadable = False
        if downloadable:
            dest = local_path_for(url, assets / "files")
            if download(url, dest, allow_redirect_host=host):
                stats["files"] += 1
                rel = Path("..") / dest.relative_to(book_dir)
                return f'<a href="{rel.as_posix()}">{inner}</a>'
        stats["links_stripped"] += 1
        return inner

    html = ANCHOR.sub(a_repl, html)
    return html


def localize_css(base: str, book_dir: Path) -> None:
    assets = book_dir / "assets"
    css_path = assets / "style.css"
    if not download(urljoin(base, "style.css"), css_path):
        return
    css = css_path.read_text(encoding="utf-8", errors="replace")
    for ref in sorted(set(re.findall(r"url\(([^)]+)\)", css))):
        ref = ref.strip("'\" ")
        if ref.startswith(("http", "data:")):
            continue
        download(urljoin(urljoin(base, "style.css"), ref), assets / ref)


def process_book(name: str, base: str, root: Path) -> None:
    book_dir = root / name
    html_dir, md_dir = book_dir / "html", book_dir / "markdown"
    print(f"\n== {name} ==")
    localize_css(base, book_dir)
    stats = {"img": 0, "img_dropped": 0, "img_failed": 0, "files": 0, "links_stripped": 0, "email": 0}
    index_rows = []
    for i, path in enumerate(sorted(html_dir.glob("*.html"), key=lambda p: (len(p.stem), p.stem))):
        html = localize_html(path.read_text(encoding="utf-8"), base, book_dir, stats)
        path.write_text(html, encoding="utf-8")
        title = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
        title = re.sub(r"\s+", " ", title.group(1)).strip() if title else path.stem
        md_name = next((p.name for p in md_dir.glob(f"*-{path.stem}.md")), f"{i:02d}-{path.stem}.md")
        md = conv.handle(html)
        header = (f"<!-- {title}. Copie locale pour usage personnel d'étude, licence CC BY-NC-SA 3.0 "
                  f"(Al Sweigart). Liens externes retirés, ressources dans ../assets/. -->\n\n")
        (md_dir / md_name).write_text(header + md, encoding="utf-8")
        index_rows.append((md_name, title))
    index = [f"# {name}", "", "Copie locale autonome : images, styles, polices et fichiers d'exercices dans `assets/`.",
             "", "| Fichier | Titre |", "| :--- | :--- |"]
    index += [f"| [{n}](markdown/{n}) | {t} |" for n, t in index_rows]
    (book_dir / "INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    print("  " + ", ".join(f"{k}={v}" for k, v in stats.items()))


# ---------- TSOFA ----------

PROMO = re.compile(r"<br><br><small>.*?</small>", re.S)
TSOFA_LINK = re.compile(r'<a\b[^>]*href="https?://[^"]*"[^>]*>(.*?)</a>', re.S)


def clean_tsofa(fc_dir: Path) -> None:
    print("\n== flashcards TSOFA ==")
    for path in sorted(fc_dir.glob("*.html")):
        src = path.read_text(encoding="utf-8")
        n_promo = len(PROMO.findall(src))
        src = PROMO.sub("", src)
        src = TSOFA_LINK.sub(r"\1", src)
        path.write_text(src, encoding="utf-8")
        print(f"  {path.name} : {n_promo} pieds de page retirés")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=ROOT)
    args = ap.parse_args()
    for name, base in BOOKS.items():
        process_book(name, base, args.root)
    clean_tsofa(args.root / "flashcards-tsofa")


if __name__ == "__main__":
    main()
