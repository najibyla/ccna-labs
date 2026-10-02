# Par où commencer

**Au quotidien, une seule chose à suivre : l'agenda Google.** Chaque événement contient tout ce qu'il faut pour la séance (vidéos à regarder par numéro, lab, deck Anki, durée). Vous n'avez pas besoin d'ouvrir un autre document pour travailler.

## Le rôle de chaque pièce

| Pièce | C'est quoi | Quand l'ouvrir |
| :--- | :--- | :--- |
| **Agenda Google** (fichiers dans `agenda/`) | Le planning opérationnel : quoi faire ce soir, avec le détail dans la description | Tous les jours. C'est la seule chose à suivre. |
| `curriculum.md` | La carte des 12 mois : 6 blocs, projets livrables, checklists de validation, charge horaire, certifications | Une fois en entier au début, puis à chaque changement de bloc (fin décembre, février, avril...) pour savoir ce qui vient. Et quand une checklist de fin de bloc est à cocher. |
| `ressources-ccna-13-semaines.md` | Un annuaire de secours pour le CCNA, classé par chapitre (les 26 Skills) : vidéos alternatives, cours payants, exercices | Seulement quand une vidéo de Jeremy n'a pas suffi sur une notion. Jamais en lecture continue. |
| `ressources/` | Les copies locales (livres, cours Linux, flashcards) et leur inventaire `README.md` | Quand l'agenda renvoie à un fichier local (leçon LUC, chapitre TLCL), ou pour retrouver un livre hors ligne. |
| `fiches/` | Fiches de synthèse (raccourcis Bash, méthode Anki) | Pour réviser un sujet précis. |
| `cartes/` et `outils/anki/` | Vos cartes Anki au format texte et l'outil qui les convertit | Le dimanche, pour ajouter les cartes de la semaine. |
| `outils/` | Les scripts qui ont produit tout cela | Jamais, sauf pour regénérer un calendrier après un changement d'horaire. |

## Une journée type

1. **Le rappel de l'agenda** arrive. Ouvrez l'événement : la description est votre feuille de route.
2. **Faites les cases** dans l'ordre. Pour le CCNA : vidéo de Jeremy avec notes, quiz, lab regardé puis refait seul, deck Anki importé.
3. **Si une notion reste floue**, et seulement alors : `ressources-ccna-13-semaines.md`, chapitre correspondant (l'événement indique le Skill).
4. **Après la séance** : 10 min d'Anki, une ligne dans `lab-notes` sur la VM, commit.

## Une semaine type (octobre à décembre 2026)

| Jour | Matin | Après-midi | Soir 21h |
| :--- | :--- | :--- | :--- |
| Lundi à vendredi | | | CCNA, Jeremy's IT Lab, 1h30 à 2h30 |
| Samedi et dimanche | 10h Linux Upskill Challenge, 2h | 15h Practical Networking en octobre, 1h à 2h | libre |

Plus Anki 10 min chaque jour, et à partir du 19 octobre 10 calculs de subnetting par jour.

## Ce qui est déjà fait

- VM Ubuntu Server prête, SSH depuis Windows, dépôt `lab-notes` sur GitHub.
- Anki installé et synchronisé, decks Bash et Python importés.
- Sept agendas Google importés (CCNA FALL, Linux, CCNA révision, CCNA JALONS, pn-fundamentals, pn-subnetting, ansible-101), notifications réglées par agenda selon `agenda/README.md`.

## Le programme ALX (vault local, `C:\utils\alx-se\vault`)

Banque d'exercices, pas un cours à suivre. Le tableau de correspondance avec les blocs est dans `curriculum.md`, section 6. On n'y pioche qu'un projet à la fois, quand le bloc concerné le prévoit.
