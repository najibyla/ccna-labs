# Fiche : méthode Anki

> Transverse à tous les blocs du curriculum. Anki représente chaque carte juste avant que vous ne l'oubliiez (répétition espacée). Votre seul travail : répondre honnêtement et revenir tous les jours.

## 1. La séance quotidienne (10 à 15 min)

1. Ouvrir le deck du moment (ex. **Linux**), puis **Étudier maintenant**.
2. Lire la question et **répondre dans sa tête** avant de retourner la carte. C'est l'effort de rappel qui fait mémoriser, pas la lecture de la réponse.
3. **Espace** ou **Entrée** retourne la carte.
4. Se noter avec les quatre boutons (touches 1 à 4) :

| Bouton | Touche | Quand | Effet |
| :--- | :--- | :--- | :--- |
| À revoir | 1 | Je ne savais pas, ou faux | Repasse dans quelques minutes |
| Difficile | 2 | Trouvé, mais lentement ou avec doute | Intervalle un peu plus court |
| Bon | 3 | Trouvé normalement | Intervalle qui s'allonge (1 j, 3 j, 7 j, 15 j...) |
| Facile | 4 | Réponse immédiate, évidente | Intervalle beaucoup plus long |

Dans le doute : **Bon**. Réflexe à combattre : cliquer Facile pour aller plus vite, la carte reviendra trop tard.

5. Quand Anki affiche « Félicitations », la séance est finie. Ne pas réétudier le deck en boucle.

## 2. Lire la liste des paquets

| Colonne | Couleur | Sens |
| :--- | :--- | :--- |
| Nouvelles | bleu | Cartes jamais vues, servies aujourd'hui (limite par deck) |
| En cours | rouge | Cartes en apprentissage, encore à revoir aujourd'hui |
| À réviser | vert | Cartes connues dont la révision est due |

La séance consiste à ramener les trois à zéro.

## 3. Règles qui font la différence

- **Tous les jours.** Dix minutes chaque jour valent mieux qu'une heure le dimanche. Trois jours sautés = révisions accumulées et pénibles. Le téléphone (AnkiDroid / AnkiMobile) sert à cela.
- **Une carte qui revient sans cesse** est mal écrite ou ambiguë. La corriger (touche **E** pendant la révision, ou dans le fichier `cartes/*.md` puis regénérer et réimporter).
- **Ne pas suspendre** les cartes difficiles pour s'en débarrasser : ce sont celles qui ont le plus besoin de passer.
- **Ne pas tricher** sur les boutons. Les statistiques ne servent qu'à soi.
- **Synchroniser** en fin de séance sur chaque appareil (bouton Synchronisation ou touche Y). Anki le fait aussi à l'ouverture et à la fermeture si l'option est cochée.

## 4. Écrire une bonne carte

| Bonne carte | Mauvaise carte |
| :--- | :--- |
| Un seul fait, une seule réponse possible | Une liste de huit éléments à réciter |
| « Que fait `ss -tulpn` ? » | « Résumer les commandes réseau » |
| Formulée comme on se poserait la question devant un terminal | Copiée mot pour mot d'un cours |
| Réponse courte, code en `backticks` | Réponse d'un paragraphe |

Une notion complexe = plusieurs cartes simples. Pour une liste, une carte par élément ou une carte « combien » plus une carte par élément.

## 5. Ajouter des cartes

- **Sur le vif**, pendant un lab : **Ajouter** > type Basique > deck > question, réponse > Ctrl+Entrée.
- **En fin de semaine** (méthode du curriculum) : noter les faits dans `cartes/<sujet>.md` au format md2anki, générer, importer. Les cartes sont ainsi versionnées avec les notes, et un réimport met à jour le contenu sans perdre la progression.

```powershell
C:\utils\ccna\.venv\Scripts\python outils\anki\md2anki.py cartes\<sujet>.md -o ressources\anki\<sujet>.apkg -d "Linux"
```

À l'import, laisser les options par défaut (« Mettre à jour les notes : si plus récent »).

## 6. Réglages à connaître, rien d'autre à toucher

| Réglage | Où | Valeur conseillée |
| :--- | :--- | :--- |
| Nouvelles cartes par jour | Roue dentée du deck > Options > onglet **Ce paquet** (pas Préréglage, partagé par tous les decks) > « Sauvegarder pour tous les sous-paquets » | 20 pour le deck en cours ; 10 si les révisions dépassent 15 min ; **0** pour un deck en attente (ex. workbook Python jusqu'au bloc 3) |
| Prochain jour commence à | Outils > Préférences > Révision | 4h du matin, pour qu'une séance à 23h compte pour le jour même |
| Synchronisation automatique | Outils > Préférences > Synchronisation | Activée |

## 7. Suivre sa progression

**Statistiques**, une fois par semaine : taux de réussite des révisions.

| Taux | Lecture |
| :--- | :--- |
| 80 à 90 % | Normal, la difficulté est bien dosée |
| > 95 % | Cartes trop faciles ou abus du bouton Facile |
| < 75 % | Trop de nouvelles cartes par jour, ou cartes mal écrites |

## 8. Pièges à la première utilisation

- **Premier sync d'un nouvel appareil** : Anki demande quel côté fait référence. Sur le PC initial avec AnkiWeb vide : **envoyer**. Sur un appareil neuf : **télécharger**, sinon la progression est écrasée par une collection vide.
- **Mettre 0 dans l'onglet Préréglage** coupe les nouvelles cartes de tous les decks qui partagent ce préréglage. Utiliser l'onglet « Ce paquet ».
- **Importer deux fois le même .apkg** ne duplique pas les cartes si elles ont un identifiant stable (c'est le cas avec md2anki) : les notes sont mises à jour.
