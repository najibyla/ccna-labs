#!/usr/bin/env python3
"""Transforme une playlist YouTube (listing yt-dlp) en calendrier .ics de séances.

1. Relever la playlist (une fois, sans télécharger les vidéos) :
     yt-dlp --flat-playlist --print "%(playlist_index)s|%(duration)s|%(title)s" <url> > outils/data/<nom>-playlist.txt
2. Générer :
     python playlist_to_ics.py outils/data/<nom>-playlist.txt --name "Ansible 101" --start 2027-06-08 \
         --weekdays tue,thu --time 21:00 --max-video 70 --out agenda/ansible-101-2027.ics

Les vidéos sont regroupées dans l'ordre jusqu'à --max-video minutes de vidéo par séance. La durée réservée
est la vidéo × --factor (pauses, notes, manipulations) arrondie à la demi-heure, bornée par --min et --max.
Les séances prédéfinies du curriculum sont dans PRESETS ; `python playlist_to_ics.py --preset all` les génère toutes.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from plan_to_ics import ALARMS_SESSION, ALARMS_WEEKEND, calendar, event  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "outils" / "data"
WD = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}

# Séances prédéfinies : nom -> options
PRESETS = {
    "pn-fundamentals": dict(
        file="pn-networking-fundamentals-playlist.txt", name="Practical Networking · Fondamentaux",
        url="https://www.youtube.com/playlist?list=PLIFyRwBY_4bRLmKfP1KnZA6rZbRHtxmXi",
        start="2026-10-03", weekdays="sat,sun", time="15:00", max_video=60, factor=1.5, out="pn-fundamentals-2026.ics",
        intro="Série « How data moves through the Internet » d'Ed Harmoush : le POURQUOI derrière les jours J.1 à J.12 de Jeremy. "
              "À regarder en prenant un schéma par vidéo (hôte, switch, routeur, et ce que chacun fait du paquet).",
        skip=()),
    "pn-subnetting": dict(
        file="pn-subnetting-mastery-playlist.txt", name="Practical Networking · Subnetting Mastery",
        url="https://www.youtube.com/playlist?list=PLIFyRwBY_4bQUE4IB5c4VPRyDoLgOdExE",
        start="2026-10-17", weekdays="sat,sun", time="15:00", max_video=50, factor=2.0, out="pn-subnetting-2026.ics",
        intro="Méthode de la « cheat sheet » : résoudre n'importe quel problème de subnetting en moins de 60 s. "
              "Après chaque séance : 20 exercices sur subnetipv4.com, chronométrés. Objectif final : moins de 30 s par calcul. "
              "Programmé juste avant les jours J.13 à J.15 de Jeremy (19 au 21 octobre).",
        skip=()),
    "ansible-101": dict(
        file="ansible-101-playlist.txt", name="Ansible 101 (Jeff Geerling)",
        url="https://www.youtube.com/playlist?list=PL2_OBreMn7FqZkvMYt6ATmgC0KAGGJNAN",
        start="2027-06-08", weekdays="tue,thu", time="21:00", max_video=70, factor=1.5, out="ansible-101-2027.ics",
        intro="Bloc 5 du curriculum. Un épisode d'une heure par séance, suivi du même travail sur vos VM : "
              "reproduire chaque playbook de l'épisode dans le dépôt infra-as-code. Code des exemples : github.com/geerlingguy/ansible-for-devops.",
        skip=("#shorts",)),
}


def load(path: Path, skip: tuple[str, ...]) -> list[dict]:
    out = []
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        if raw.count("|") < 2:
            continue
        idx, secs, title = raw.split("|", 2)
        if any(s.lower() in title.lower() for s in skip):
            continue
        out.append({"idx": int(idx), "min": round(int(secs) / 60), "title": title.strip()})
    return out


def group(videos: list[dict], max_video: int) -> list[list[dict]]:
    sessions, cur, acc = [], [], 0
    for v in videos:
        if cur and acc + v["min"] > max_video:
            sessions.append(cur)
            cur, acc = [], 0
        cur.append(v)
        acc += v["min"]
    if cur:
        sessions.append(cur)
    return sessions


def slots(start: date, weekdays: set[int], n: int) -> list[date]:
    out, d = [], start
    while len(out) < n:
        if d.weekday() in weekdays:
            out.append(d)
        d += timedelta(days=1)
    return out


def build(file: str, name: str, url: str, start: str, weekdays: str, time: str, max_video: int, factor: float,
          out: str, intro: str = "", skip: tuple[str, ...] = (), vmin: int = 60, vmax: int = 150) -> tuple[Path, int, int]:
    videos = load(DATA / file, skip)
    sessions = group(videos, max_video)
    days = {WD[w.strip().lower()] for w in weekdays.split(",")}
    hh, mm = (int(x) for x in time.split(":"))
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    events = []
    for i, (day, vids) in enumerate(zip(slots(date.fromisoformat(start), days, len(sessions)), sessions)):
        video = sum(v["min"] for v in vids)
        minutes = max(vmin, min(vmax, ((round(video * factor) + 29) // 30) * 30))
        first, last = vids[0]["idx"], vids[-1]["idx"]
        rng = f"n°{first}" if first == last else f"n°{first} à {last}"
        summary = f"{name} · {i + 1}/{len(sessions)} · {rng}"
        lines = [f"{name}, séance {i + 1} sur {len(sessions)}.", f"Playlist : {url}", ""]
        if intro:
            lines += [intro, ""]
        lines += [f"Vidéo : {video} min. Bloc réservé : {minutes} min.", "", "Vidéos (n° = position dans la playlist) :"]
        lines += [f"  ☐ n°{v['idx']} {v['title']} ({v['min']} min)" for v in vids]
        lines += ["", "Noter dans lab-notes ce qui a été compris, créer 3 à 5 cartes Anki."]
        start_dt = datetime.combine(day, datetime.min.time()).replace(hour=hh, minute=mm)
        alarms = ALARMS_WEEKEND if day.weekday() >= 5 else ALARMS_SESSION
        events.append(event(f"{slug}-{i + 1:02d}@ccna-curriculum", start_dt, minutes, summary, "\n".join(lines), name, alarms))
    path = ROOT / "agenda" / out
    path.write_bytes(calendar(name, events).encode("utf-8"))
    return path, len(sessions), sum(v["min"] for v in videos)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", help="listing yt-dlp (dans outils/data ou chemin)")
    ap.add_argument("--preset", help="nom d'un preset, ou 'all'")
    ap.add_argument("--name"), ap.add_argument("--url", default="")
    ap.add_argument("--start"), ap.add_argument("--weekdays", default="mon,tue,wed,thu,fri"), ap.add_argument("--time", default="21:00")
    ap.add_argument("--max-video", type=int, default=60), ap.add_argument("--factor", type=float, default=1.5)
    ap.add_argument("--out"), ap.add_argument("--intro", default="")
    a = ap.parse_args()
    if a.preset:
        names = list(PRESETS) if a.preset == "all" else [a.preset]
        for n in names:
            path, ns, vid = build(**PRESETS[n])
            print(f"{n:16} {ns:2} séances, {vid:4} min de vidéo -> {path.name}")
        return
    if not (a.file and a.name and a.start and a.out):
        ap.error("file, --name, --start et --out sont requis sans --preset")
    path, ns, vid = build(a.file, a.name, a.url, a.start, a.weekdays, a.time, a.max_video, a.factor, a.out, a.intro)
    print(f"{ns} séances, {vid} min de vidéo -> {path}")


if __name__ == "__main__":
    main()
