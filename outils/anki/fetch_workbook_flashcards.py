#!/usr/bin/env python3
"""Télécharge les 24 jeux de flashcards TSOFA du "Automate the Boring Stuff Workbook"
(Al Sweigart, inventwithpython.com) puis les convertit en un paquet Anki.

Les fichiers HTML sont conservés : chacun est une appli de flashcards autonome
utilisable hors ligne dans un navigateur.

Usage :
  python fetch_workbook_flashcards.py [--dest DOSSIER] [--out FICHIER.apkg]
"""
import argparse
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent))
from md2anki import build  # noqa: E402

BASE = "https://inventwithpython.com/automate3workbook/flashcards-automateworkbook{n}.html"
DEFAULT_DEST = Path(__file__).resolve().parents[2] / "ressources" / "automate-the-boring-stuff" / "flashcards-tsofa"
DEFAULT_OUT = Path(__file__).resolve().parents[2] / "ressources" / "anki" / "automate-workbook.apkg"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", type=Path, default=DEFAULT_DEST)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    args.dest.mkdir(parents=True, exist_ok=True)
    files = []
    for n in range(1, 25):
        target = args.dest / f"chapitre-{n:02d}.html"
        if not target.exists():
            url = BASE.format(n=n)
            print(f"GET {url}")
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (personal study archive)"}, timeout=30)
            if r.status_code != 200:
                print(f"  HTTP {r.status_code}, ignoré", file=sys.stderr)
                continue
            target.write_text(r.text, encoding="utf-8")
            time.sleep(1)
        files.append(target)
    build(files, args.out, "Automate the Boring Stuff - Workbook", flat=False, extra_tags=["python", "atbs"])


if __name__ == "__main__":
    main()
