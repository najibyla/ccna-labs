# Calendriers d'étude

| Fichier | Contenu | Créneau |
| :--- | :--- | :--- |
| `ccna-fall-2026.ics` | 63 séances, du 1er octobre au 30 décembre 2026 : le cours gratuit **Jeremy's IT Lab CCNA 200-301 v1.1** (126 vidéos), un jour (J.1 à J.63) par soir de semaine, fêtes du 6 et 18 novembre sautées, J.21 coupé en deux (STP puis STP Toolkit), J.62 et J.63 regroupés. Chaque événement donne la durée de la vidéo, le nombre de labs, le déroulé cochable (vidéo, quiz, lab refait seul, deck Anki), le Skill NetworkChuck équivalent et les ressources de secours. | Lundi à vendredi, 21h00, 1h30 à 2h30 selon la charge du jour |
| `linux-track-2026.ics` | 22 séances, du 3 octobre au 6 décembre 2026 : les jours 0 à 21 du Linux Upskill Challenge, avec le fichier local de la leçon et les chapitres de The Linux Command Line à lire. | Samedi et dimanche, 10h00-12h00 |
| `ccna-revision-2027.ics` | 21 séances, du 4 au 28 janvier 2027 : 2 semaines de révision par domaine d'examen avec Jeremy's IT Lab et deux labs de synthèse, puis 2 semaines d'examens blancs Boson (A, B, C) avec corrections et révisions ciblées. Chaque séance détaille le contenu et les critères. | Semaine 21h00 (2h, 2h30 pour un examen blanc), samedi 15h00 (2h30) |
| `ccna-jalons-2027.ics` | 4 jalons : préparation du 30 décembre (achat Boson, réservation Pearson VUE), décision du 27 janvier (confirmer ou reporter), veille d'examen du 29 janvier, et l'examen cible du mardi 2 février 2027 à 10h00. Calendrier séparé pour recevoir des rappels longs. | Voir chaque événement |
| `pn-fundamentals-2026.ics` | 4 séances, week-ends du 3 au 11 octobre 2026 : la série « Networking Fundamentals » de Practical Networking (15 vidéos, 3 h 25), le « pourquoi » derrière J.1 à J.12. | Samedi et dimanche, 15h00 |
| `pn-subnetting-2026.ics` | 5 séances, week-ends du 17 au 31 octobre 2026 : « Subnetting Mastery » de Practical Networking (14 vidéos, 3 h 22), calé juste avant J.13 à J.15. Chaque séance se termine par 20 exercices chronométrés. | Samedi et dimanche, 15h00 |
| `ansible-101-2027.ics` | 15 séances, du 8 juin au 27 juillet 2027 : un épisode d'« Ansible 101 » de Jeff Geerling par séance (15 h 39 au total), pour le bloc 5. | Mardi et jeudi, 21h00 |
| `ccna-plan.json` | Le plan extrait du PDF, tâche par tâche, avec le type et l'estimation. | - |

Les trois calendriers de playlists sont produits par `outils/playlist_to_ics.py` à partir des listings exacts de `outils/data/` (relevés avec yt-dlp, sans téléchargement). Chaque événement liste les vidéos par numéro dans la playlist, avec leur durée. Le même outil sert pour toute autre playlist : voir son en-tête.

## Rappels

Les fichiers contiennent des alarmes, respectées par Outlook, Apple Calendar et Thunderbird. **Google Agenda les ignore à l'import** (vérifié le 1er octobre 2026 : les rappels affichés sont ceux réglés sur l'agenda, pas ceux du fichier) et applique les notifications par défaut de chaque agenda. C'est pourquoi il y a un fichier par catégorie : importez chaque fichier dans son propre agenda Google, puis réglez une seule fois, dans Paramètres > l'agenda > **Notifications pour les événements** :

| Agenda Google | Fichier | Notifications à régler |
| :--- | :--- | :--- |
| CCNA | `ccna-fall-2026.ics` | 15 minutes avant, et 12 heures avant (réglé le 1er octobre 2026) |
| Linux | `linux-track-2026.ics` | 15 minutes avant, et 2 heures avant (réglé) |
| CCNA révision | `ccna-revision-2027.ics` | 15 minutes avant, et 2 heures avant (réglé) |
| CCNA jalons | `ccna-jalons-2027.ics` | 1 semaine avant, 1 jour avant, et 2 heures avant (réglé) |
| pn-fundamentals | `pn-fundamentals-2026.ics` | 15 minutes avant, et 2 heures avant |
| pn-subnetting | `pn-subnetting-2026.ics` | 15 minutes avant, et 2 heures avant |
| ansible-101 | `ansible-101-2027.ics` | 15 minutes avant, et 12 heures avant |

Ces notifications s'appliquent à tous les événements présents et futurs de l'agenda. Sur le téléphone, vérifiez que l'application Google Agenda a l'autorisation de notifier et que les sept agendas (CCNA FALL, Linux, CCNA révision, CCNA JALONS, pn-fundamentals, pn-subnetting, ansible-101, tous importés le 2 octobre 2026) sont cochés dans Paramètres > compte.

Fuseau : UTC, heure légale du Maroc depuis septembre 2026 (heure additionnelle supprimée). Les horaires sont écrits en UTC absolu (suffixe `Z`), pas avec un nom de fuseau : ils restent à 21h même si la base des fuseaux horaires de Google ou du téléphone n'est pas encore à jour de ce changement. Rappel 15 minutes avant chaque séance.

Si votre téléphone ou Google Agenda affichent encore un décalage d'une heure, c'est leur réglage de fuseau qui est resté sur l'ancienne règle (UTC+1) : mettez-le sur « UTC » ou « Temps universel coordonné » dans les paramètres.

## Importer dans Google Agenda

1. Sur ordinateur, ouvrez Google Agenda, puis la roue dentée > **Paramètres**.
2. Dans la colonne de gauche, **Ajouter un agenda > Créer un agenda**. Nommez-le « CCNA » (puis un second « Linux »). Un agenda dédié permet de tout supprimer d'un coup si vous changez de rythme.
3. Toujours dans les paramètres, **Importer et exporter > Importer**. Choisissez le fichier `.ics` et l'agenda de destination créé à l'étape 2.
4. Répétez pour le second fichier.

Les événements passés (avant aujourd'hui) sont importés aussi : ils servent de trace de ce qui a été fait.

## Changer les horaires ou le rythme

Modifiez les constantes en tête de `outils/plan_to_ics.py` (`SOURCE` : `"jeremy"` ou `"networkchuck"` si vous achetez ce cours un jour, `START_DATE` pour décaler tout le plan, `SKIP_DATES` pour les jours fériés, `CCNA_START`, `LINUX_START`, `LINUX_FIRST_DAY`...) puis relancez :

```powershell
C:\utils\ccna\.venv\Scripts\python outils\plan_to_ics.py
```

Les identifiants d'événements sont stables : réimporter un fichier regénéré dans le même agenda met les séances à jour au lieu de les dupliquer. Google Agenda ne supprime toutefois pas les événements disparus du fichier ; dans ce cas, supprimez l'agenda et réimportez.
