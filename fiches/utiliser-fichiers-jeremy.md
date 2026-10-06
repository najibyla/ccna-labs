# Fiche : utiliser les decks Anki et les labs Packet Tracer de Jeremy's IT Lab

> Les fichiers officiels du cours ont été téléchargés depuis le Google Drive de Jeremy le 6 octobre 2026. Ils sont hors dépôt Git (dossier `ressources/`), usage personnel.

## 1. Où sont les fichiers

| Quoi | Emplacement | Dans Git ? |
| :--- | :--- | :--- |
| 71 decks Anki, un par jour ou par partie (ex. `Day 21-2 Flashcards - BPDU Guard & BPDU Filter.apkg`) | `ressources/jeremy-it-lab/anki/` | Non |
| 48 labs Packet Tracer d'origine, `.pkt` (jours 1 à 58) | `ressources/jeremy-it-lab/labs/` | Non. **Ne jamais les modifier.** |
| CCNA Mega Lab (`.pka` + tableau d'adressage `.xlsx`) | `ressources/jeremy-it-lab/labs/mega-lab/` | Non |
| Vos labs réalisés | `labs/dayNN/` à la racine du projet | **Oui** |

Jours sans deck : 12, 14 et 15 (leurs cartes sont dans le deck du jour 13, Subnetting). Jours sans lab : 5, 7, 10, 13, 14, 55 à 57, 59 à 63, comme dans la playlist.

Si le dossier `ressources/jeremy-it-lab/` manque (nouveau PC) : retélécharger les deux archives « CCNA 200-301 Course Files » et « CCNA Mega Lab » depuis le lien Drive en description de n'importe quelle vidéo du cours, et extraire comme ci-dessus.

## 2. Les decks Anki : un par jour, après la séance

**Pourquoi pas tout d'un coup.** Importer les 71 decks d'un coup mettrait une soixantaine de jours de cartes nouvelles dans la file, servies dans un ordre qui ne suit pas le cours : vous réviseriez OSPF avant d'avoir vu les VLANs. Le deck du jour s'importe **après la séance**, c'est la dernière case de chaque événement du calendrier.

**Importer un deck.**

1. Anki > Fichier > Importer > `ressources/jeremy-it-lab/anki/Day NN Flashcards - ….apkg`, options par défaut.
2. Les cartes arrivent dans un deck nommé par Jeremy. Au premier import, il crée son deck racine ; les suivants s'y ajoutent ou créent des decks voisins selon le nommage.
3. Synchroniser.

**Le conseil de Jeremy (vidéo Day 1) : un seul deck central.** Plutôt que des dizaines de decks séparés, gardez un deck « CCNA » unique et déplacez-y les cartes de chaque nouveau deck : dans Parcourir, sélectionner les cartes du deck fraîchement importé, clic droit > Changer de paquet > CCNA. Puis supprimer le deck vide. Avantage : une seule file de révision, les cartes de tous les jours se mélangent, ce qui est exactement ce que l'examen fait.

**Réglages du deck CCNA.** 20 nouvelles cartes par jour (onglet « Ce paquet », pas « Préréglage »), comme pour Linux. Si les révisions quotidiennes dépassent 15 minutes, baisser à 15.

**Rattrapage.** Au 6 octobre, les séances J.1 à J.3 sont faites : importer Day 01, Day 02 et Day 03 dès maintenant, puis Day 04 après la séance du soir.

**Et vos propres cartes ?** Les decks de Jeremy couvrent le cours. Vos cartes personnelles (une notion mal comprise, une commande qui vous a bloqué) vont dans `cartes/` au format md2anki et dans le même deck CCNA, pour ne pas multiplier les files. Voir `outils/anki/README.md`.

## 3. Les labs Packet Tracer : copie de travail, configs en texte

**Avant la séance.** Créer `labs/dayNN/` et y **copier** le `.pkt` du jour depuis `ressources/jeremy-it-lab/labs/`. L'original reste intact : vous pourrez refaire le lab en janvier.

**Pendant.** Regarder la vidéo du lab, puis fermer la vidéo et refaire le lab seul sur la copie. Si vous bloquez, revenir à la vidéo pour ce point seulement.

**Après.** Trois choses, dans le dossier du jour :

1. Enregistrer le `.pkt` travaillé.
2. Exporter la configuration de chaque équipement configuré : dans Packet Tracer, onglet CLI de l'équipement, `show running-config`, copier le texte dans `labs/dayNN/configs/<nom>.txt` (ex. `R1.txt`, `SW1.txt`). Les `.pkt` sont illisibles pour Git ; les configs texte se relisent, se comparent d'un jour à l'autre et se révisent la veille de l'examen.
3. `labs/dayNN/notes.md` : deux lignes, ce qui a bloqué et la commande qui a débloqué.

Puis `git add -A && git commit -m "Lab day NN" && git push`, et cocher la ligne dans le tableau d'état de `labs/README.md`.

**Version.** Packet Tracer 9.0.1 ouvre tous les `.pkt` de Jeremy, créés avec des versions antérieures. L'inverse n'est pas vrai : un fichier enregistré en 9.0.1 ne s'ouvre pas dans une version plus ancienne.

**Le Mega Lab.** C'est un `.pka`, une activité Packet Tracer avec correction intégrée et pourcentage de réussite. Il est prévu en deux samedis de janvier (9 et 16, calendrier de révision), à faire dans `labs/mega-lab/` avec le tableau d'adressage fourni. Ne pas l'ouvrir avant : c'est l'examen blanc pratique du cours.

## 4. En résumé, pour une séance CCNA avec lab

1. Vidéo du jour avec notes, quiz de fin de vidéo.
2. Copier le `.pkt` dans `labs/dayNN/`, regarder la vidéo du lab, refaire seul.
3. Exporter les configs en texte, deux lignes de notes, commit.
4. Importer le deck Anki du jour, déplacer ses cartes dans le deck CCNA, première passe.
5. 10 minutes d'Anki, toutes files confondues.
