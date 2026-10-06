# Contexte du projet pour Claude Code

Ce fichier est lu automatiquement par Claude Code à chaque session, sur n'importe quel PC. Il remplace la mémoire locale de la machine d'origine. Mettre à jour quand un fait change.

## Objectif

Montée en compétences infrastructure et code, base Linux, sur 12 mois (octobre 2026 à septembre 2027). Utilisateur francophone au Maroc, débutant motivé, répond en français. Point d'entrée : `README.md`. Carte complète : `curriculum.md`.

## Faits établis (ne pas re-supposer)

- **Cours CCNA suivi : Jeremy's IT Lab**, gratuit (playlist YouTube v1.1, 126 vidéos, listing exact dans `outils/data/jeremy-playlist.txt`). L'utilisateur **n'a pas accès** à NetworkChuck Academy (inscriptions closes) ; le PDF NetworkChuck ne sert que de structure en 26 Skills pour `ressources-ccna-13-semaines.md`.
- **Calendriers** (`agenda/*.ics`, importés dans Google Agenda le 2 octobre 2026, sept agendas) : CCNA 63 séances du 1er octobre au 30 décembre 2026, lundi à vendredi 21h ; Linux Upskill Challenge 22 séances, week-ends 10h-12h ; Practical Networking week-ends d'octobre 15h ; révision janvier 2027 ; examen CCNA cible le 2 février 2027 ; Ansible 101 en juin-juillet 2027.
- **Fuseau : UTC** (le Maroc a supprimé l'heure additionnelle en septembre 2026). Les `.ics` utilisent des horodatages `Z`, jamais de TZID. Google Agenda ignore les VALARM : les notifications sont réglées par agenda (voir `agenda/README.md`).
- **Lab** : Windows 11 Pro, VMware Workstation Pro 26H1u1, VM Ubuntu Server 22.04 `ubnu` (utilisateur `naj`, NAT DHCP, alias SSH `ubnu`, snapshot « 30Sept »), WSL2 Ubuntu 24.04 / Arch / Debian. Ne pas proposer Hyper-V comme hyperviseur. Dépôt de notes quotidiennes : `najibyla/lab-notes` (sur la VM).
- **Anki** : synchronisé AnkiWeb, type de note `md2anki Basic` avec CSS mode nuit. Decks : `bash-historique` (32 cartes, actif), `automate-workbook` (1127 cartes, nouvelles cartes à 0 jusqu'au bloc 3), decks officiels Jeremy importés un par jour après chaque séance.
- **Fichiers du cours Jeremy** (téléchargés le 6 octobre 2026, hors dépôt) : `ressources/jeremy-it-lab/anki/` (71 decks) et `ressources/jeremy-it-lab/labs/` (48 `.pkt` + Mega Lab). Les labs réalisés vont dans `labs/dayNN/` (versionné, convention dans `labs/README.md`).
- **Abonnements** : Boot.dev (complément 20-30 min/jour, pas à la place des labs). Pas de LabEx Pro, pas de GoMyCode, Linux Foundation seulement pour les certifications (LFCS bloc 5).
- **Programme ALX** (vault local `C:\utils\alx-se\vault`, hors dépôt) : banque d'exercices, correspondance par bloc dans `curriculum.md` section 6.

## Structure

| Dossier | Rôle |
| :--- | :--- |
| `agenda/` | Calendriers `.ics` générés + `README.md` (import, notifications) |
| `outils/` | `plan_to_ics.py` (CCNA, Linux, révision, jalons), `playlist_to_ics.py` (playlists), `scrape_atbs.py` + `localize_assets.py` (livres Sweigart hors ligne), `anki/md2anki.py` (Markdown/CSV/TSOFA vers `.apkg`), `data/` (listings yt-dlp) |
| `fiches/`, `cartes/` | Fiches de synthèse et cartes Anki au format md2anki, même nom de fichier par sujet |
| `labs/` | Labs Packet Tracer réalisés (copies de travail, configs exportées en texte, notes), projet `network-lab` |
| `ressources/` | **Hors dépôt** sauf son `README.md` : copies locales (Linux Upskill Challenge cloné, TLCL PDF, Automate the Boring Stuff localisé, decks `.apkg`). Régénérer avec les scripts. |

## Conventions

- Environnement Python : `.venv` à la racine (`python -m venv .venv ; .venv\Scripts\pip install -r outils\requirements.txt`). Hors dépôt.
- Les `.ics` sont écrits en binaire avec CRLF et repliement à 75 octets (`.gitattributes` : `*.ics -text`). Après tout changement d'horaire, regénérer avec `plan_to_ics.py` puis, dans Google Agenda, supprimer et recréer l'agenda concerné (un réimport ne met pas à jour).
- Les documents de référence sont en français. Vérifier la cohérence croisée (dates, nombres de séances, noms d'agendas) entre `README.md`, `curriculum.md`, `ressources-ccna-13-semaines.md`, `agenda/README.md`, `ressources/README.md` après chaque modification.
- Ne pas publier de solutions ALX ni de contenu NetworkChuck en public : le dépôt reste privé.
