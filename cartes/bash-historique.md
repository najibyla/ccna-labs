tags: linux, bash, bloc1

# Historique

Que fait `!!` ? ;; Relance la dernière commande. Exemple : `sudo !!`
Que fait `!$` ? ;; Insère le dernier argument de la dernière commande. `cat fichier` puis `vim !$`
Que fait `!^` ? ;; Insère le premier argument de la dernière commande.
Que fait `!*` ? ;; Insère tous les arguments de la dernière commande.
Que fait `!git` ? ;; Relance la dernière commande commençant par `git`.
Que fait `!?push` ? ;; Relance la dernière commande contenant `push`.
Que fait `^conf.^conf` ? ;; Relance la dernière commande en remplaçant la première occurrence de `conf.` par `conf`.
Comment afficher une commande rappelée par `!` sans l'exécuter ? ;; Ajouter `:p`, par exemple `!!:p`
Quelle option `shopt` demande confirmation avant d'exécuter une ligne rappelée par `!` ? ;; `shopt -s histverify`
Que fait `Ctrl+R` ? ;; Recherche incrémentale en arrière dans l'historique. `Ctrl+R` à nouveau pour l'occurrence précédente, `Ctrl+G` pour annuler.
Que fait `Alt+.` ? ;; Insère le dernier argument de la commande précédente, répétable pour remonter.
Comment supprimer l'entrée 42 de l'historique ? ;; `history -d 42`
Quelle variable empêche d'enregistrer les doublons et les commandes commençant par un espace ? ;; `HISTCONTROL=ignoreboth`
Quelle option `shopt` ajoute à l'historique au lieu de l'écraser quand plusieurs shells sont ouverts ? ;; `shopt -s histappend`

# Édition de ligne

Que fait `Ctrl+A` / `Ctrl+E` ? ;; Début / fin de ligne.
Que fait `Ctrl+U` ? ;; Coupe du curseur jusqu'au début de la ligne.
Que fait `Ctrl+K` ? ;; Coupe du curseur jusqu'à la fin de la ligne.
Que fait `Ctrl+W` ? ;; Coupe le mot avant le curseur.
Que fait `Ctrl+Y` ? ;; Colle le dernier texte coupé (yank).
Que fait `Ctrl+L` ? ;; Efface l'écran, comme `clear`.
Que fait `Ctrl+X Ctrl+E` ? ;; Ouvre la ligne en cours dans `$EDITOR` et l'exécute à la fermeture.
Que fait `Ctrl+D` sur une ligne vide ? ;; Ferme le shell, comme `exit`.
Que fait `Ctrl+Z` ? ;; Suspend la commande en cours. `fg` pour la reprendre, `jobs` pour lister.
Que fait `Alt+B` / `Alt+F` ? ;; Recule / avance d'un mot.

# sudo

Que fait `sudo -i` ? ;; Ouvre un shell root avec l'environnement de root. `exit` pour revenir.
Que fait `sudoedit /etc/fichier` ? ;; Édite un fichier système avec l'éditeur de l'utilisateur, sans lancer l'éditeur en root.
Que fait `sudo -l` ? ;; Liste ce que sudo autorise pour l'utilisateur courant.
Pourquoi `needrestart -b` sans sudo n'affiche-t-il que sa version ? ;; Sans privilèges il ne peut pas lire les processus ni le noyau installé : beaucoup d'outils renvoient un résultat partiel sans message d'erreur.

# Motif conf.d

Pourquoi préférer un fichier dans `conf.d/` plutôt que modifier le fichier de configuration principal ? ;; Le fichier principal appartient au paquet et peut être écrasé à sa mise à jour. Les fichiers de `conf.d/` sont conservés.
Comment passer needrestart en mode automatique proprement ? ;; `echo "\$nrconf{restart} = 'a';" | sudo tee /etc/needrestart/conf.d/50-auto.conf`
Citez quatre dossiers `.d` de surcharge sous `/etc`. ;; `sudoers.d`, `sysctl.d`, `apt/apt.conf.d`, `ssh/sshd_config.d`
Comment créer un drop-in pour un service systemd ? ;; `systemctl edit <service>` crée `/etc/systemd/system/<service>.d/override.conf`
