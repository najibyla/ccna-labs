# Fiche : historique et raccourcis de ligne de commande Bash

> Bloc 1 du curriculum. Correspond au jour 5 du Linux Upskill Challenge et au chapitre 8 de The Linux Command Line.
> Cartes Anki associées : `cartes/bash-historique.md` (à générer avec `outils/anki/md2anki.py`).

## 1. Rappel de l'historique (`!`)

| Raccourci | Effet | Exemple |
| :--- | :--- | :--- |
| `!!` | Dernière commande | `needrestart -b` puis `sudo !!` |
| `!$` | Dernier argument de la dernière commande | `cat /etc/needrestart/needrestart.conf` puis `vim !$` |
| `!^` | Premier argument de la dernière commande | `cp a.txt b.txt` puis `vim !^` ouvre `a.txt` |
| `!*` | Tous les arguments de la dernière commande | `ls a b c` puis `rm !*` |
| `!git` | Dernière commande commençant par `git` | `!git` relance `git push` |
| `!?push` | Dernière commande contenant `push` | |
| `!42` | Commande numéro 42 de `history` | |
| `!-2` | Avant-dernière commande | |
| `^conf.^conf` | Relance la dernière commande en remplaçant `conf.` par `conf` (première occurrence) | corrige une faute de frappe |
| `!!:s/a/b/` | Même chose, forme longue | `!!:gs/a/b/` pour toutes les occurrences |
| `!!:p` | Affiche la commande sans l'exécuter (`:p` = print) | vérifier avant un `!` risqué |

Bash affiche toujours la commande reconstituée avant de l'exécuter. Pour les commandes destructives (`rm`, `dd`), préférez `Ctrl+R` ou `:p` pour voir ce qui va partir.

## 2. Recherche et navigation dans l'historique

| Touche | Effet |
| :--- | :--- |
| `Ctrl+R` | Recherche incrémentale en arrière : taper un fragment, `Ctrl+R` encore pour l'occurrence précédente |
| `Ctrl+S` | Recherche en avant (si `stty -ixon` est actif, sinon la touche gèle le terminal : `Ctrl+Q` pour reprendre) |
| `Ctrl+G` ou `Échap` | Sortir de la recherche sans exécuter |
| `Entrée` | Exécuter la commande trouvée |
| `→` ou `Fin` | Reprendre la commande trouvée pour l'éditer |
| `↑` / `↓` | Commande précédente / suivante |
| `Alt+.` | Insère le dernier argument de la commande précédente (répéter pour remonter) |
| `history` | Liste numérotée ; `history 20` pour les 20 dernières ; `history \| grep ssh` |
| `history -d 42` | Supprime l'entrée 42 (mot de passe tapé par erreur) |
| `history -c` | Vide l'historique de la session |

## 3. Édition de la ligne (readline, mode Emacs par défaut)

| Touche | Effet |
| :--- | :--- |
| `Ctrl+A` / `Ctrl+E` | Début / fin de ligne |
| `Alt+B` / `Alt+F` | Mot précédent / suivant |
| `Ctrl+U` | Coupe du curseur au début de ligne |
| `Ctrl+K` | Coupe du curseur à la fin de ligne |
| `Ctrl+W` | Coupe le mot avant le curseur |
| `Alt+D` | Coupe le mot après le curseur |
| `Ctrl+Y` | Colle ce qui a été coupé (`yank`) |
| `Ctrl+L` | Efface l'écran (équivaut à `clear`) |
| `Ctrl+X Ctrl+E` | Ouvre la ligne dans `$EDITOR`, exécute à la fermeture (commandes longues) |
| `Ctrl+C` | Abandonne la ligne (ou interrompt la commande en cours) |
| `Ctrl+D` | Sur ligne vide : ferme le shell (`exit`). Sinon : supprime le caractère sous le curseur |
| `Ctrl+Z` | Suspend la commande en cours (`fg` pour la reprendre, `jobs` pour lister) |
| `Tab` / `Tab Tab` | Complétion / liste des complétions possibles |

Sous Windows Terminal, `Alt` fonctionne comme sur Linux. Sous certains terminaux macOS, activer "Use Option as Meta key".

## 4. Configuration utile (`~/.bashrc`)

```bash
# Ne pas enregistrer les doublons ni les commandes commençant par un espace
export HISTCONTROL=ignoreboth
# Historique plus long (défaut : 500 / 1000)
export HISTSIZE=10000
export HISTFILESIZE=20000
# Horodater chaque entrée
export HISTTIMEFORMAT='%F %T  '
# Ajouter au fichier au lieu d'écraser (plusieurs terminaux ouverts)
shopt -s histappend
# Vérifier la ligne reconstituée par ! avant exécution
shopt -s histverify
```

`histverify` est recommandé en apprentissage : `sudo !!` affiche la commande et attend une seconde validation.

## 5. Variantes avec sudo

| Commande | Usage |
| :--- | :--- |
| `sudo !!` | Relancer la dernière commande avec les privilèges |
| `sudo -i` | Ouvrir un shell root (environnement de root) ; `exit` pour revenir |
| `sudo -u postgres psql` | Exécuter en tant qu'un autre utilisateur |
| `sudoedit /etc/fichier` | Éditer un fichier système avec son éditeur habituel, sans lancer l'éditeur en root |
| `sudo -l` | Lister ce que sudo autorise pour l'utilisateur courant |

Beaucoup d'outils système renvoient un résultat vide ou partiel sans privilèges, **sans message d'erreur** (`needrestart -b` n'affiche que sa version). Quand une commande "ne dit rien", la première question est : ai-je les bons droits ?

## 6. Le motif `conf.d`

Rencontré avec needrestart : le fichier principal fourni par le paquet lit tout `*.conf` d'un dossier `conf.d/`. On y dépose ses surcharges au lieu de modifier le fichier principal, qui peut être écrasé à la prochaine mise à jour du paquet.

Même motif : `/etc/sudoers.d/`, `/etc/sysctl.d/`, `/etc/apt/apt.conf.d/`, `/etc/ssh/sshd_config.d/`, `/etc/systemd/system/<service>.d/override.conf` (drop-ins systemd, créés avec `systemctl edit <service>`).
