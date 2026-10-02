# Ressources locales

Copies locales des supports gratuits du curriculum, récupérées le 30 septembre 2026. Usage personnel d'étude uniquement : chaque source a sa propre licence (indiquée ci-dessous).

| Dossier | Contenu | Source | Licence |
| :--- | :--- | :--- | :--- |
| `linuxupskillchallenge/` | Le cours complet Linux Upskill Challenge : `docs/00.md` (montage du serveur) à `docs/21.md`, plus `how-this-works.md`. Clone git du dépôt officiel, `git pull` pour mettre à jour. | [github.com/livialima/linuxupskillchallenge](https://github.com/livialima/linuxupskillchallenge) | CC BY-SA 4.0 (voir `LICENSE`) |
| `tlcl/TLCL-25.12A.pdf` | *The Linux Command Line*, William Shotts, Septième Édition Internet (v25.12A, juillet 2026), 596 pages. | [linuxcommand.org/tlcl.php](https://linuxcommand.org/tlcl.php) | CC BY-NC-ND 3.0 |
| `automate-the-boring-stuff/book-3e/` | *Automate the Boring Stuff with Python*, 3e édition, Al Sweigart. 27 pages (intro, 24 chapitres, 2 annexes) en HTML et Markdown. Voir `INDEX.md`. **Copie autonome** : images, feuille de style et fichiers d'exercices dans `assets/`, bannières publicitaires retirées, tous les liens web remplacés par leur texte. | automatetheboringstuff.com/3e | CC BY-NC-SA 3.0 |
| `automate-the-boring-stuff/workbook/` | *Automate the Boring Stuff Workbook* : exercices, questions et réponses par chapitre. 27 pages HTML et Markdown. Voir `INDEX.md`. Copie autonome, même traitement (images, polices, fichiers d'exercices, emails décodés). | inventwithpython.com/automate3workbook | CC BY-NC-SA 3.0 |
| `automate-the-boring-stuff/*/assets/files/` | Fichiers d'exercices de l'auteur (scripts Python, sons, pages HTML à scraper des chapitres 13 et 19 à 24). Un seul niveau : les pages à scraper gardent leurs propres liens internes, c'est leur contenu d'exercice. | autbor.com | idem |
| `automate-the-boring-stuff/flashcards-tsofa/` | Les 24 jeux de flashcards du workbook au format TSOFA. Chaque fichier HTML s'ouvre dans un navigateur, hors ligne. Pieds de page publicitaires et liens retirés. | idem | idem |
| `anki/automate-workbook.apkg` | Les mêmes 1127 cartes converties pour Anki, un sous-deck par chapitre. Généré par `outils/anki/fetch_workbook_flashcards.py`. | idem | idem |
| `anki/exemple.apkg` | Deck de démonstration de l'outil `md2anki`. | local | - |
| `anki/bash-historique.apkg` | 32 cartes : historique Bash, édition de ligne, sudo, motif conf.d. Source : `cartes/bash-historique.md`, fiche : `fiches/bash-historique-raccourcis.md`. | local | - |

## Fiches et cartes du projet (hors de ce dossier)

| Dossier | Contenu |
| :--- | :--- |
| `../fiches/` | Fiches de synthèse en Markdown, une par sujet : `bash-historique-raccourcis.md`, `methode-anki.md`. |
| `../cartes/` | Fichiers de cartes au format `md2anki`, un par sujet, même nom que la fiche. Générer avec `C:\utils\ccna\.venv\Scripts\python outils\anki\md2anki.py cartes\<sujet>.md -o ressources\anki\<sujet>.apkg -d "Linux"`. |

## Playlists YouTube (pas de copie locale)

Les listings exacts (numéro, durée, titre de chaque vidéo) sont dans `outils/data/*-playlist.txt`, relevés le 1er octobre 2026 avec yt-dlp. Ils alimentent les calendriers du dossier `agenda/`.

| Playlist | Auteur | Vidéos | Durée | Listing | Usage dans le curriculum |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [CCNA 200-301 Complete Course v1.1](https://www.youtube.com/playlist?list=PLxbwE86jKRgMpuZuLBivzlM8s2Dk5lXBQ) | Jeremy's IT Lab | 126 (63 jours, cours et labs entrelacés, Mega Lab final) | 56 h | `jeremy-playlist.txt` | Bloc 2, colonne vertébrale : `agenda/ccna-fall-2026.ics`. Decks Anki et labs Packet Tracer de chaque jour gratuits sur [jeremysitlab.com](https://www.jeremysitlab.com/). |
| [Networking Fundamentals](https://www.youtube.com/playlist?list=PLIFyRwBY_4bRLmKfP1KnZA6rZbRHtxmXi) | Practical Networking | 15 | 3 h 25 | `pn-networking-fundamentals-playlist.txt` | Bloc 2, le « pourquoi » des J.1 à J.12 : `agenda/pn-fundamentals-2026.ics`. |
| [Subnetting Mastery](https://www.youtube.com/playlist?list=PLIFyRwBY_4bQUE4IB5c4VPRyDoLgOdExE) | Practical Networking | 14 | 3 h 22 | `pn-subnetting-mastery-playlist.txt` | Bloc 2, avant J.13 à J.15 : `agenda/pn-subnetting-2026.ics`. |
| [Ansible 101](https://www.youtube.com/playlist?list=PL2_OBreMn7FqZkvMYt6ATmgC0KAGGJNAN) | Jeff Geerling | 15 épisodes d'1 h | 15 h 39 | `ansible-101-playlist.txt` | Bloc 5 : `agenda/ansible-101-2027.ics`. Code des exemples libre sur [github.com/geerlingguy/ansible-for-devops](https://github.com/geerlingguy/ansible-for-devops). |

Pour une copie hors ligne des vidéos : `yt-dlp` (`pip install yt-dlp`, puis `yt-dlp -f "bv*[height<=720]+ba" <url playlist>`). Non fait ici, à votre discrétion.

## Regénérer

```powershell
# Livres Sweigart : téléchargement (HTML + Markdown), puis localisation des ressources
python outils\scrape_atbs.py
python outils\localize_assets.py
# Flashcards -> Anki
python outils\anki\fetch_workbook_flashcards.py
# Mise à jour du cours Linux
git -C ressources\linuxupskillchallenge pull
```
