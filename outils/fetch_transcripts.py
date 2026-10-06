#!/usr/bin/env python3
"""Récupère les transcriptions (sous-titres automatiques anglais) des vidéos d'une playlist YouTube,
sans télécharger les vidéos, et les enregistre en texte brut.

Par défaut : la playlist CCNA de Jeremy's IT Lab -> ressources/jeremy-it-lab/transcripts/
(hors dépôt). Un fichier par vidéo : "NNN - <titre court>.txt". Les fichiers existants sont ignorés,
le script peut donc être relancé après une interruption.

Usage : python fetch_transcripts.py [--url PLAYLIST] [--out DOSSIER] [--only 1,3,8-12]
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
YTDLP = ROOT / ".venv" / "Scripts" / "yt-dlp.exe"
DEFAULT_URL = "https://www.youtube.com/playlist?list=PLxbwE86jKRgMpuZuLBivzlM8s2Dk5lXBQ"
DEFAULT_OUT = ROOT / "ressources" / "jeremy-it-lab" / "transcripts"


def playlist_entries(url: str) -> list[tuple[int, str, str, int]]:
    """(index, id, titre, durée en secondes) pour chaque vidéo."""
    out = subprocess.run([str(YTDLP), "--flat-playlist", "--print", "%(playlist_index)s|%(id)s|%(duration)s|%(title)s", url],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    entries = []
    for line in out.stdout.splitlines():
        if line.count("|") < 3:
            continue
        idx, vid, dur, title = line.split("|", 3)
        entries.append((int(idx), vid, title.strip(), int(dur or 0)))
    return entries


def short_title(title: str) -> str:
    t = re.sub(r"\s*\|\s*CCNA 200-301 Complete Course\s*$", "", title)
    t = re.sub(r"^Free CCNA \| ", "", t)
    t = re.sub(r"[\\/:*?\"<>|]", "-", t)
    return t.strip()[:90]


def vtt_to_text(vtt: str) -> str:
    lines = []
    for l in vtt.splitlines():
        if "-->" in l or l.startswith(("WEBVTT", "Kind:", "Language:")) or not l.strip():
            continue
        l = re.sub(r"<[^>]+>", "", l).strip()
        if l and (not lines or l != lines[-1]):
            lines.append(l)
    text: list[str] = []
    for l in lines:  # les sous-titres automatiques répètent chaque ligne en la faisant défiler
        if text and (l in text[-1] or text[-1] in l):
            if len(l) > len(text[-1]):
                text[-1] = l
            continue
        text.append(l)
    return " ".join(text)


def fetch_one(vid: str, dest_txt: Path, tmp_dir: Path) -> bool:
    base = tmp_dir / vid
    subprocess.run([str(YTDLP), "--skip-download", "--write-auto-sub", "--write-sub", "--sub-lang", "en",
                    "--sub-format", "vtt", "-o", f"{base}.%(ext)s", f"https://www.youtube.com/watch?v={vid}"],
                   capture_output=True, text=True)
    vtts = sorted(tmp_dir.glob(f"{vid}*.vtt"))
    if not vtts:
        return False
    text = vtt_to_text(vtts[0].read_text(encoding="utf-8", errors="replace"))
    dest_txt.write_text(text, encoding="utf-8")
    for v in vtts:
        v.unlink(missing_ok=True)
    return bool(text.strip())


def parse_only(spec: str | None) -> set[int] | None:
    if not spec:
        return None
    out: set[int] = set()
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            out.update(range(int(a), int(b) + 1))
        else:
            out.add(int(part))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--only", help="indices de playlist, ex. 1,3,8-12")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    tmp = args.out / "_tmp"
    tmp.mkdir(exist_ok=True)
    only = parse_only(args.only)

    entries = playlist_entries(args.url)
    print(f"{len(entries)} vidéos dans la playlist", flush=True)
    index_lines = ["index|id|secondes|titre|fichier"]
    ok = skipped = failed = 0
    for idx, vid, title, dur in entries:
        name = f"{idx:03d} - {short_title(title)}.txt"
        dest = args.out / name
        index_lines.append(f"{idx}|{vid}|{dur}|{title}|{name}")
        if only and idx not in only:
            continue
        if dest.exists() and dest.stat().st_size > 0:
            skipped += 1
            continue
        print(f"[{idx:03d}] {short_title(title)} ... ", end="", flush=True)
        if fetch_one(vid, dest, tmp):
            ok += 1
            print(f"{dest.stat().st_size // 1024} Ko", flush=True)
        else:
            failed += 1
            print("PAS DE SOUS-TITRES", flush=True)
        time.sleep(1.5)
    (args.out / "INDEX.txt").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"\nterminé : {ok} récupérées, {skipped} déjà présentes, {failed} sans sous-titres -> {args.out}")


if __name__ == "__main__":
    sys.exit(main())
