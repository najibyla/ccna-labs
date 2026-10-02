tags: linux, bloc1

# Fichiers et permissions

Q: Que signifie `chmod 750 script.sh` ?
A: Propriétaire : lecture, écriture, exécution (7).
Groupe : lecture, exécution (5).
Autres : rien (0).

Q: Quelle commande affiche les permissions d'un fichier avec le propriétaire et le groupe ?
A: `ls -l`

Quelle commande change le propriétaire d'un fichier ? ;; `chown utilisateur:groupe fichier`

# systemd

Q: Comment voir les logs du service `nginx` depuis le dernier démarrage ?
A: `journalctl -u nginx -b`

Q: Quelle commande active un service au démarrage **et** le lance tout de suite ?
A: `systemctl enable --now nginx`

# Réseau

Quelle commande liste les ports en écoute avec le processus associé ? ;; `ss -tulpn`
Quelle commande affiche les adresses IP des interfaces ? ;; `ip -br a`
