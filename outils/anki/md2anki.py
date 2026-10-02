#!/usr/bin/env python3
"""md2anki : génère un paquet Anki (.apkg) à partir de fichiers texte.

Formats d'entrée acceptés (détectés par extension) :

  .md / .txt  Format Markdown "Q/A" :
                # Titre du sous-deck          (optionnel, crée un sous-deck)
                Q: Quelle commande affiche les processus ?
                A: `ps aux` ou `top`
                                              (ligne vide = fin de carte)
              Variante en une ligne :  question ;; réponse
              Les tags : une ligne "tags: linux, bash" en tête de fichier.

  .csv        Deux colonnes : question, réponse (en-tête optionnel).

  .html       Fichier TSOFA (The Simple Offline Flashcard App, Al Sweigart) :
              le tableau JS `let FLASHCARDS = [[q, a], ...]` est extrait.

Usage :
  python md2anki.py fichier1.md fichier2.html ... -o mon_deck.apkg --deck "Nom du deck"

Chaque fichier devient un sous-deck "Nom du deck::<nom du fichier>" sauf si --flat.
Les cartes ont un identifiant stable (hash de la question) : réimporter le
paquet dans Anki met à jour les cartes existantes sans perdre la progression.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import re
import sys
import warnings
from pathlib import Path

import genanki

# genanki avertit dès qu'un champ contient "<" hors balise (ex. : `i < 10` dans du code).
# Ces champs sont déjà du HTML valide dans nos sources ; on ignore ce faux positif.
warnings.filterwarnings("ignore", message="Field contained the following invalid HTML tags")

# Modèle "Basic" fixe : l'ID ne doit jamais changer pour que les réimports fonctionnent.
MODEL_ID = 1607392319

# Couleurs explicites en mode jour ET en mode nuit (Anki desktop : .card.nightMode,
# AnkiDroid : body.night_mode). Sans cela, le fond clair du code reste affiché en mode
# nuit alors que le texte passe en blanc : illisible.
CSS = """
.card { font-family: -apple-system, "Segoe UI", Roboto, sans-serif; font-size: 20px;
        line-height: 1.45; text-align: left; color: #1f1f1f; background: #ffffff; padding: 14px; }
code, pre { font-family: Consolas, Menlo, "DejaVu Sans Mono", monospace; font-size: 18px;
            color: #0b3d91; background: #eef2f7; border: 1px solid #c9d3e0;
            border-radius: 5px; padding: 2px 6px; font-weight: 600; }
pre { display: block; padding: 10px 12px; white-space: pre-wrap; margin: 8px 0; }
hr#answer { border: 0; border-top: 2px solid #c9d3e0; margin: 14px 0; }
b { color: #8a2d00; }

.card.nightMode, .night_mode .card, .nightMode .card {
    color: #ececec; background: #1e1e1e; }
.card.nightMode code, .card.nightMode pre, .night_mode code, .night_mode pre,
.nightMode code, .nightMode pre {
    color: #ffd866; background: #2d2d2d; border-color: #555; }
.card.nightMode hr#answer, .night_mode hr#answer, .nightMode hr#answer { border-top-color: #555; }
.card.nightMode b, .night_mode b, .nightMode b { color: #ff9e64; }
"""
MODEL = genanki.Model(
    MODEL_ID,
    "md2anki Basic",
    fields=[{"name": "Question"}, {"name": "Réponse"}, {"name": "Source"}],
    templates=[
        {
            "name": "Carte",
            "qfmt": "{{Question}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Réponse}}<br><br><small style="color:#888">{{Source}}</small>',
        }
    ],
    css=CSS,
)


def stable_id(text: str) -> int:
    """ID numérique stable (31 bits) dérivé d'un texte."""
    return int(hashlib.sha1(text.encode("utf-8")).hexdigest()[:8], 16) & 0x7FFFFFFF


class Note(genanki.Note):
    @property
    def guid(self):  # identité de la note = sa question (+ source)
        return genanki.guid_for(self.fields[0], self.fields[2])


# ---------- Parsers ----------

_INLINE_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*(.+?)\*\*")


def md_inline_to_html(text: str) -> str:
    """Conversion minimale Markdown -> HTML pour le contenu d'une carte."""
    text = html.escape(text, quote=False)
    text = _INLINE_CODE.sub(r"<code>\1</code>", text)
    text = _BOLD.sub(r"<b>\1</b>", text)
    return text.replace("\n", "<br>")


def parse_markdown(path: Path) -> list[tuple[str, str, str, list[str]]]:
    """Retourne [(question, réponse, sous-deck, tags)]."""
    cards: list[tuple[str, str, str, list[str]]] = []
    tags: list[str] = []
    section = ""
    q_lines: list[str] = []
    a_lines: list[str] = []
    mode = None  # "q" | "a" | None

    def flush():
        nonlocal q_lines, a_lines, mode
        if q_lines and a_lines:
            cards.append((md_inline_to_html("\n".join(q_lines).strip()),
                          md_inline_to_html("\n".join(a_lines).strip()), section, list(tags)))
        q_lines, a_lines, mode = [], [], None

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        low = line.lower()
        if low.startswith("tags:") and not cards and not q_lines:
            tags = [t.strip().replace(" ", "_") for t in line[5:].split(",") if t.strip()]
            continue
        if line.startswith("#"):
            flush()
            section = line.lstrip("#").strip()
            continue
        if not line.strip():
            flush()
            continue
        if " ;; " in line and mode is None:
            q, a = line.split(" ;; ", 1)
            cards.append((md_inline_to_html(q.strip()), md_inline_to_html(a.strip()), section, list(tags)))
            continue
        if low.startswith("q:"):
            flush()
            mode = "q"
            q_lines.append(line[2:].strip())
        elif low.startswith("a:"):
            mode = "a"
            a_lines.append(line[2:].strip())
        elif mode == "q":
            q_lines.append(line)
        elif mode == "a":
            a_lines.append(line)
        else:
            print(f"  ligne ignorée ({path.name}) : {line[:60]}", file=sys.stderr)
    flush()
    return cards


def parse_csv(path: Path) -> list[tuple[str, str, str, list[str]]]:
    cards = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for i, row in enumerate(csv.reader(f)):
            if len(row) < 2:
                continue
            q, a = row[0].strip(), row[1].strip()
            if i == 0 and q.lower() in {"question", "q", "front", "recto"}:
                continue
            cards.append((md_inline_to_html(q), md_inline_to_html(a), "", []))
    return cards


_PROMO = re.compile(r"<br>\s*<br>\s*<small>.*?</small>\s*$", re.S)


_ESCAPES = {"n": "\n", "t": "\t", "r": "", "\\": "\\", '"': '"', "'": "'", "`": "`"}


def _js_strings(src: str) -> list[str]:
    """Extrait toutes les chaînes JS délimitées par `, " ou ' (avec gestion des \\ échappés).

    Le contenu hors chaînes (crochets, virgules, commentaires //) est ignoré.
    """
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c == "/" and src.startswith("//", i):  # commentaire de ligne
            i = src.find("\n", i)
            if i == -1:
                break
            continue
        if c in "`\"'":
            quote, j, buf = c, i + 1, []
            while j < n and src[j] != quote:
                if src[j] == "\\" and j + 1 < n:
                    buf.append(_ESCAPES.get(src[j + 1], src[j + 1]))
                    j += 2
                else:
                    buf.append(src[j])
                    j += 1
            out.append("".join(buf))
            i = j + 1
        else:
            i += 1
    return out


def parse_tsofa(path: Path) -> list[tuple[str, str, str, list[str]]]:
    src = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"FLASHCARDS\s*=\s*\[(.*?)\n\];", src, re.S)
    if not m:
        m = re.search(r"FLASHCARDS\s*=\s*\[(.*)\]\s*;", src, re.S)
    if not m:
        print(f"  {path.name} : tableau FLASHCARDS introuvable", file=sys.stderr)
        return []
    strings = _js_strings(m.group(1))
    if len(strings) % 2:
        print(f"  {path.name} : nombre impair de chaînes ({len(strings)}), dernière ignorée", file=sys.stderr)
    cards = []
    for q, a in zip(strings[0::2], strings[1::2]):
        a = _PROMO.sub("", a.strip())
        q = q.replace("&#8203;", "").strip()
        a = a.replace("&#8203;", "").strip()
        cards.append((q, a, "", []))
    return cards


PARSERS = {".md": parse_markdown, ".txt": parse_markdown, ".csv": parse_csv, ".html": parse_tsofa, ".htm": parse_tsofa}


# ---------- Build ----------

def build(inputs: list[Path], out: Path, deck_name: str, flat: bool, extra_tags: list[str]) -> int:
    decks: dict[str, genanki.Deck] = {}
    total = 0
    for path in inputs:
        parser = PARSERS.get(path.suffix.lower())
        if not parser:
            print(f"  format non géré : {path}", file=sys.stderr)
            continue
        cards = parser(path)
        if not cards:
            print(f"  {path.name} : aucune carte", file=sys.stderr)
            continue
        for q, a, section, tags in cards:
            name = deck_name
            if not flat:
                name += f"::{path.stem}"
                if section:
                    name += f"::{section}"
            deck = decks.setdefault(name, genanki.Deck(stable_id(name), name))
            deck.add_note(Note(model=MODEL, fields=[q, a, path.name], tags=tags + extra_tags))
            total += 1
        print(f"  {path.name} : {len(cards)} cartes")
    if not decks:
        print("aucune carte générée", file=sys.stderr)
        return 0
    out.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(list(decks.values())).write_to_file(str(out))
    print(f"\n{total} cartes dans {len(decks)} deck(s) -> {out}")
    return total


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", type=Path, help="fichiers .md, .txt, .csv ou .html (TSOFA)")
    ap.add_argument("-o", "--output", type=Path, default=Path("deck.apkg"))
    ap.add_argument("-d", "--deck", default="md2anki", help="nom du deck racine")
    ap.add_argument("--flat", action="store_true", help="tout dans un seul deck (pas de sous-decks)")
    ap.add_argument("-t", "--tag", action="append", default=[], help="tag ajouté à toutes les cartes")
    args = ap.parse_args(argv)
    files: list[Path] = []
    for p in args.inputs:
        files.extend(sorted(p.glob("*")) if p.is_dir() else [p])
    n = build(files, args.output, args.deck, args.flat, args.tag)
    return 0 if n else 1


if __name__ == "__main__":
    sys.exit(main())
