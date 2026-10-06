# Par où commencer

**Au quotidien, une seule chose à suivre : l'agenda Google.** Chaque événement contient tout ce qu'il faut pour la séance (vidéos à regarder par numéro, lab, deck Anki, durée). Vous n'avez pas besoin d'ouvrir un autre document pour travailler.

## Le rôle de chaque pièce

| Pièce | C'est quoi | Quand l'ouvrir |
| :--- | :--- | :--- |
| **Agenda Google** (fichiers dans `agenda/`) | Le planning opérationnel : quoi faire ce soir, avec le détail dans la description | Tous les jours. C'est la seule chose à suivre. |
| `curriculum.md` | La carte des 12 mois : 6 blocs, projets livrables, checklists de validation, charge horaire, certifications | Une fois en entier au début, puis à chaque changement de bloc (fin décembre, février, avril...) pour savoir ce qui vient. Et quand une checklist de fin de bloc est à cocher. |
| `ressources-ccna-13-semaines.md` | Un annuaire de secours pour le CCNA, classé par chapitre (les 26 Skills) : vidéos alternatives, cours payants, exercices | Seulement quand une vidéo de Jeremy n'a pas suffi sur une notion. Jamais en lecture continue. |
| `ressources/` | Les copies locales (livres, cours Linux, flashcards) et leur inventaire `README.md` | Quand l'agenda renvoie à un fichier local (leçon LUC, chapitre TLCL), ou pour retrouver un livre hors ligne. |
| `fiches/` | Fiches de synthèse (raccourcis Bash, méthode Anki, utilisation des decks et labs de Jeremy) et, dans `fiches/ccna/`, une fiche bilingue par jour Jeremy (`jour-NN-<sujet>.md`), vérifiée contre la transcription de la vidéo | Pour réviser un sujet précis. Les fiches CCNA se relisent la veille de l'examen blanc. |
| `cartes/` et `outils/anki/` | Vos cartes Anki au format texte et l'outil qui les convertit | Le dimanche, pour ajouter les cartes de la semaine. |
| `labs/` | Vos labs Packet Tracer réalisés, un sous-dossier par jour (convention dans son README) | À chaque séance CCNA avec un lab. Les fichiers d'origine de Jeremy sont dans `ressources/jeremy-it-lab/`. |
| `outils/` | Les scripts qui ont produit tout cela | Jamais, sauf pour regénérer un calendrier après un changement d'horaire. |

## Une journée type

1. **Le rappel de l'agenda** arrive. Ouvrez l'événement : la description est votre feuille de route.
2. **Faites les cases** dans l'ordre. Pour le CCNA : vidéo de Jeremy avec notes, quiz, lab (copie du `.pkt` depuis `ressources/jeremy-it-lab/labs/` vers `labs/dayNN/`, regardé puis refait seul), deck Anki du jour importé depuis `ressources/jeremy-it-lab/anki/`.
3. **Si une notion reste floue**, et seulement alors : `ressources-ccna-13-semaines.md`, chapitre correspondant (l'événement indique le Skill).
4. **Après la séance** : 10 min d'Anki, une ligne dans `lab-notes` sur la VM, commit.

## Une semaine type (octobre à décembre 2026)

| Jour | Matin | Après-midi | Soir 21h |
| :--- | :--- | :--- | :--- |
| Lundi à vendredi | | | CCNA, Jeremy's IT Lab, 1h30 à 2h30 |
| Samedi et dimanche | 10h Linux Upskill Challenge, 2h | 15h Practical Networking en octobre, 1h à 2h | libre |

Plus Anki 10 min chaque jour, et à partir du 19 octobre 10 calculs de subnetting par jour.

## Dépôt

Ce dossier est versionné sur GitHub, dépôt privé `najibyla/ccna-labs`. Le dossier `ressources/` (copies locales de livres et cours) et `.venv/` n'y sont pas : ils se régénèrent avec les scripts de `outils/`. Après chaque modification des documents ou des cartes : `git add -A && git commit -m "..." && git push`.

### Reprendre le travail sur un autre PC

Les conversations Claude Code et sa mémoire automatique sont locales à chaque machine (`~/.claude/projects/`) et ne se transfèrent pas. Le contexte, lui, est dans `CLAUDE.md` à la racine : Claude Code le lit automatiquement à chaque session, sur n'importe quel PC. Une nouvelle session repart donc avec les bons faits (cours suivi, calendriers, lab, conventions), sans l'historique des échanges.

Sur le nouveau PC, en gardant le même chemin `C:\utils\ccna` (Claude Code dérive son dossier de session du chemin absolu) :

```powershell
git clone git@github.com:najibyla/ccna-labs.git C:\utils\ccna
cd C:\utils\ccna
python -m venv .venv
.venv\Scripts\pip install -r outils\requirements.txt
```

Puis ouvrir le dossier dans VS Code et lancer Claude Code. Pour retrouver les copies locales de `ressources/` : `git clone https://github.com/livialima/linuxupskillchallenge ressources\linuxupskillchallenge`, télécharger le PDF TLCL (lien dans `ressources\README.md`), puis `outils\scrape_atbs.py`, `outils\localize_assets.py` et `outils\anki\fetch_workbook_flashcards.py`.

Pour continuer **la même conversation** plutôt qu'en ouvrir une nouvelle : Remote Control (la session reste sur le PC d'origine, pilotée depuis claude.ai/code ou l'application mobile) ou Claude Code sur le web (claude.ai/code, session hébergée dans le cloud et liée à ce dépôt).

Mettre `CLAUDE.md` à jour quand un fait change (examen passé, nouvelle VM, changement d'horaire), puis pousser.

## Ce qui est déjà fait

- VM Ubuntu Server prête, SSH depuis Windows, dépôt `lab-notes` sur GitHub.
- Anki installé et synchronisé, decks Bash et Python importés.
- Sept agendas Google importés (CCNA FALL, Linux, CCNA révision, CCNA JALONS, pn-fundamentals, pn-subnetting, ansible-101), notifications réglées par agenda selon `agenda/README.md`.

## Le programme ALX (vault local, `C:\utils\alx-se\vault`)

Banque d'exercices, pas un cours à suivre. Le tableau de correspondance avec les blocs est dans `curriculum.md`, section 6. On n'y pioche qu'un projet à la fois, quand le bloc concerné le prévoit.
