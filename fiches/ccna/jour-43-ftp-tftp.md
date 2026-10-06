# CCNA Day 43 : FTP & TFTP / File Transfer Protocol et Trivial File Transfer Protocol

> Source : Jeremy's IT Lab, « Free CCNA | FTP & TFTP | Day 43 » (31 min, vidéo n°87 de la playlist, cours) et « Free CCNA | FTP & TFTP | Day 43 Lab » (16 min, vidéo n°88, lab Packet Tracer). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Rôle de FTP et TFTP

- Sujet d'examen **4.9** : décrire les **capacités et la fonction de TFTP et FTP** dans le réseau. Comprendre leur objectif et **leurs différences**.
- **FTP** (*File Transfer Protocol*) et **TFTP** (*Trivial File Transfer Protocol*) : protocoles standard pour **transférer des fichiers** sur un réseau, modèle **client-serveur** : le client copie des fichiers **depuis** ou **vers** un serveur.
- Usage le plus courant pour un ingénieur réseau : **mise à jour de l'IOS** d'un équipement. L'admin télécharge la nouvelle image depuis software.cisco.com, la place sur un serveur joignable par R1, puis depuis le CLI de R1 la copie dans la **flash**, et redémarre R1 avec la nouvelle image.

### 2. TFTP

- Standardisé en **1981** (après FTP, mais plus simple). « Trivial » : fonctions basiques, **copie d'un fichier vers ou depuis un serveur, rien d'autre**. Ce n'est pas un remplaçant de FTP, mais un outil léger.
- **Aucune authentification** (pas de nom d'utilisateur ni de mot de passe : le serveur répond à toutes les requêtes), **aucun chiffrement** (texte clair). À utiliser dans un **environnement contrôlé** pour de petits fichiers, pas sur Internet pour des fichiers importants.
- **Les serveurs TFTP écoutent sur UDP port 69.**
- UDP est sans connexion et sans fiabilité, mais **TFTP intègre ses propres mécanismes** :
  - **Fiabilité** : **chaque message de données est acquitté** (Ack) ; des timers déclenchent la **retransmission** du dernier message si la réponse attendue n'arrive pas. Exemple : le client envoie un *read request*, le serveur envoie un bloc de données, le client envoie un Ack qui se perd ; le client retransmet l'Ack, le serveur envoie le bloc suivant. Communication **« lock-step »** : chacun envoie un message puis attend la réponse ; le serveur n'envoie jamais deux blocs de suite (sauf retransmission). Moins efficace que l'acquittement anticipé et la fenêtre glissante de TCP.
  - **Connexion** en **trois phases** : *connection phase* (requête du client, réponse du serveur = premier bloc de données), *data transfer* (données et Ack), *termination* (Ack final du dernier bloc).
- Détail hors programme : le port source aléatoire du client est un **TID** (*Transfer Identifier*) ; le serveur répond lui aussi depuis un **port aléatoire**, pas 69, et le client utilise ensuite ce port comme destination. **Le port 69 ne sert que pour le tout premier message.**

### 3. FTP

- Standardisé en **1971**, avant TCP et IP (mis à jour depuis). **TCP ports 20 et 21.**
- **Authentification par nom d'utilisateur et mot de passe**, mais **aucun chiffrement** (identifiants en clair). Pour plus de sécurité : **FTPS** (*FTP over SSL/TLS*, *FTP Secure*) = évolution de FTP ; **SFTP** (*SSH File Transfer Protocol*) = **protocole différent** au nom similaire.
- Plus complexe que TFTP : transfert de fichiers mais aussi **navigation dans les répertoires, création et suppression de répertoires, listage des fichiers**, via des **commandes FTP** envoyées par le client. TFTP ne peut même pas demander « quels fichiers as-tu ? ».
- Deux types de connexions :
  - **Connexion de contrôle vers TCP 21** : établie (SYN, SYN-ACK, ACK) pour envoyer les commandes FTP et recevoir les réponses du serveur. **Maintenue pendant tout l'échange.**
  - **Connexions de données vers TCP 20** : établies et terminées **à la demande** pour transférer les fichiers.
- Modes d'établissement de la connexion de données :
  - **Mode actif** (défaut, « normal ») : **le serveur initie** la connexion TCP de données (premier SYN du serveur vers le client).
  - **Mode passif** : **le client initie** la connexion de données. Nécessaire quand le client est **derrière un pare-feu**, qui bloquerait une connexion initiée de l'extérieur (les pare-feu n'autorisent généralement pas les équipements extérieurs à initier des connexions) mais laisse passer les réponses du serveur.

### 4. Comparaison

| | FTP | TFTP |
| :--- | :--- | :--- |
| Transport | **TCP**, orienté connexion ; **20** données, **21** contrôle | **UDP 69**, sans connexion (connexion basique interne au protocole) |
| Fonctions | Commandes variées : copier, lister, supprimer, répertoires... | **Copier un fichier vers ou depuis le serveur, seulement** |
| Authentification | **Nom d'utilisateur et mot de passe** | **Aucune** |
| Complexité | Plus complexe | Simple |

### 5. Systèmes de fichiers IOS

- `show file systems` affiche les systèmes de fichiers (sortie longue). Types :
  - **disk** : stockage comme la **flash**, où est en général stocké le fichier IOS ; au démarrage, l'IOS est copié de la flash vers la RAM.
  - **opaque** : fonctions internes spécifiques, systèmes logiques, pas des stockages séparés.
  - **nvram** : *non-volatile RAM*, conserve les données sans alimentation ; contient la **startup-config**.
  - **network** : systèmes de fichiers externes, serveurs **FTP ou TFTP**.
- Sujet retiré de la dernière version du CCNA : pas de questions attendues.

### 6. Utiliser TFTP et FTP dans IOS (mise à jour d'IOS, démo Packet Tracer)

- `show version` : nom de l'image (`C2900-UNIVERSALK9-M`, K9 = cryptographie), version **15.1(4)M4**. `show flash` : contenu de la flash, dont l'image IOS.
- **TFTP** : `copy tftp: flash:` ; le routeur demande l'**adresse du serveur**, le **nom du fichier source** (à connaître d'avance, TFTP ne liste pas), puis le **nom de destination** (Entrée = même nom). Le fichier arrive dans la flash (`show flash`).
- Démarrer sur la nouvelle image : **`boot system <chemin>`** en config globale ; sans cette commande, le routeur démarre sur **la première image trouvée dans la flash**. **Sauvegarder la configuration** avant `reload`, sinon `boot system` est sans effet. Après redémarrage, `show version` montre **15.5** au lieu de 15.1.
- Supprimer l'ancienne image : `delete <chemin>`, confirmation, `show flash`.
- **FTP** : configurer d'abord `ip ftp username cisco` et `ip ftp password cisco` (les mêmes identifiants que sur le serveur) ; puis `copy ftp: flash:`, adresse du serveur, nom source, nom destination. Suite identique (`boot system`, sauvegarde, `reload`).
- Rappel : `copy running-config startup-config` est la même commande `copy <source> <destination>`.

### 7. Pièges d'examen

- **FTP : TCP 21 contrôle, TCP 20 données. TFTP : UDP 69.**
- **Mode actif** : le serveur initie la connexion de données ; **mode passif** : le client l'initie, à utiliser **derrière un pare-feu**. Actif/passif ne concernent que la connexion de **données** : la connexion de contrôle est toujours initiée par le client.
- `copy tftp: flash:` = source puis destination.
- **Startup-config dans la NVRAM** ; IOS dans la **flash**.
- TFTP **ne peut pas** créer un répertoire ni lister le contenu du serveur.
- TFTP et SNMP utilisent **UDP** ; HTTP et SMTP utilisent **TCP** (bonus Boson).
- `boot system` + **sauvegarde** avant `reload`.

### 8. Commandes IOS

```text
R1# show version                       ! image IOS en cours (K9) et version
R1# show flash                         ! contenu de la flash
R1# show file systems                  ! systèmes de fichiers (disk, opaque, nvram, network)
R1# copy tftp: flash:                  ! copie depuis un serveur TFTP ; demande IP, fichier source, nom destination
R1(config)# ip ftp username jeremy     ! identifiants FTP du routeur (identiques au serveur)
R1(config)# ip ftp password ccna
R1# copy ftp: flash:                   ! copie depuis un serveur FTP
R1(config)# boot system flash:<fichier> ! image à utiliser au démarrage (sinon première image trouvée)
R1# write                              ! sauvegarder avant reload, sinon boot system ignoré
R1# reload                             ! redémarrer
R1# delete flash:<fichier>             ! supprimer l'ancienne image (confirmation)
R4# copy running-config tftp           ! sauvegarder la config sur un serveur TFTP (NetSim)
R4# copy tftp startup-config           ! restaurer la config dans la NVRAM (NetSim)
R4# copy startup-config running-config ! appliquer la startup-config (fusion dans la running-config)
```

### 9. Le lab (vidéo n°88)

Objectif : mettre à jour l'IOS de R1 par **TFTP** et de R2 par **FTP** depuis SRV1 (10.0.0.1), puis redémarrer et supprimer l'ancienne image. Adresses et route statique vers 10.0.0.0/24 sur R2 déjà configurées.

- **SRV1** : Services → TFTP : service **activé par défaut**, liste des fichiers OS ; FTP : activé par défaut, liste des **utilisateurs FTP** (défaut Packet Tracer : cisco / cisco ; Jeremy a créé jeremy / ccna).
- **R1 (TFTP)** : `show version` (15.1), `show flash` ; `copy tftp flash`, adresse 10.0.0.1, nom du fichier 15.5 (copié-collé), Entrée pour le nom par défaut ; transfert en quelques secondes ; `show flash`. `conf t`, `boot system flash <fichier>`, `exit`, **`write`** (obligatoire avant reload), `reload` (rapide dans Packet Tracer, plusieurs minutes en réel). `show version` → 15.5. `delete flash:<ancien fichier>`, confirmation, `show flash`.
- **R2 (FTP)** : `show version` (15.1) ; `ip ftp username jeremy`, `ip ftp password ccna` ; `copy ftp flash`, 10.0.0.1, nom du fichier, Entrée. **FTP est beaucoup plus lent que TFTP dans Packet Tracer** : patienter. `show flash`, `boot system flash <fichier>`, `write`, `reload`, `show version` → 15.5, `delete flash:<ancien>`, `show flash`.

Bonus Boson NetSim « TFTP » : autre usage, **sauvegarder la configuration**. `ipconfig /ip` et `/dg` sur PC1 et PC3 ; ping PC1 depuis Router4 (mot de passe Cisco) ; `copy running-config tftp`, adresse 192.168.1.2, nom r4config ; sur PC1 `show tftp-configs` (commande NetSim) ; `hostname MainRouter` ; `copy tftp startup-config` (fichier r4config) ; `show startup-config` montre hostname Router4 mais la running-config dit toujours MainRouter ; `copy startup-config running-config` → hostname redevient Router4. Pas besoin d'effacer la NVRAM avant d'y copier : la copie **remplace** totalement le fichier ; vers la running-config (DRAM), les fichiers **fusionnent**.

### 10. Le quiz (5 questions + 1 Boson)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Affirmations vraies sur FTP ? (deux) | **Connexions de contrôle sur TCP 21** (B) ; **connexions de données sur TCP 20** (D) | FTP utilise TCP ; port 21 pour les commandes et réponses, port 20 pour l'échange de données. |
| Quelle commande transfère un fichier d'un serveur TFTP externe vers la flash locale ? | **`copy tftp: flash:`** (A) | `copy` source destination : d'un serveur TFTP vers la flash. |
| R1 derrière un pare-feu veut joindre un serveur FTP externe : affirmation vraie ? | **R1 doit utiliser le mode passif pour la connexion de données** (C) | Actif/passif ne concernent que les connexions de données (la connexion de contrôle est toujours initiée par le client). Actif : le serveur initie ; passif : le client initie, requis derrière un pare-feu. |
| Quel système de fichiers stocke la startup-config ? | **NVRAM** (D) | RAM non volatile, conserve les données sans alimentation. |
| Fonctions impossibles avec TFTP ? (deux) | **Créer un répertoire sur le serveur** (B) ; **lister le contenu du serveur** (C) | TFTP ne fait que copier un fichier vers ou depuis un serveur. |
| Boson : quels protocoles applicatifs utilisent UDP pour un transfert sans connexion ? (deux) | **TFTP** et **SNMP** | TFTP utilise UDP (connexion basique interne, mais pas de TCP) ; SNMP aussi. HTTP et SMTP (*Simple Mail Transfer Protocol*) utilisent TCP. |

---

## 🇬🇧 English version

### 1. Purpose of FTP and TFTP

- Exam topic **4.9**: describe the **capabilities and function of TFTP and FTP** in the network. Understand their purpose and **differences**.
- **FTP** (File Transfer Protocol) and **TFTP** (Trivial File Transfer Protocol): industry-standard protocols to **transfer files** over a network, **client-server** model: clients copy files **from** or **to** a server.
- Most common use for a network engineer: **upgrading a device's IOS**. The admin downloads the new image from software.cisco.com, places it on a server reachable by R1, then from R1's CLI copies it into **flash**, and reboots R1 with the new image.

### 2. TFTP

- Standardized in **1981** (after FTP, but simpler). "Trivial": basic features, **copy a file to or from a server, nothing else**. Not a replacement for FTP, just a lightweight tool.
- **No authentication** (no usernames or passwords: servers respond to all requests), **no encryption** (plain text). Best in a **controlled environment** for small files, not over the Internet for important files.
- **TFTP servers listen on UDP port 69.**
- UDP is connectionless and unreliable, but **TFTP builds its own mechanisms**:
  - **Reliability**: **every data message is acknowledged** (Ack); timers trigger **retransmission** of the previous message if the expected reply doesn't arrive. Example: the client sends a *read request*, the server sends a data block, the client's Ack is lost; the client retransmits the Ack, the server sends the next block. **"Lock-step"** communication: each side sends a message then waits for a reply; the server never sends two data messages in a row (except retransmission). Less efficient than TCP's forward acknowledgment and sliding window.
  - **Connection** in **three phases**: *connection phase* (client request, server reply = first data packet), *data transfer* (data and Acks), *termination* (final Ack for the last data packet).
- Beyond the CCNA: the client's random source port is a **TID** (Transfer Identifier); the server also replies from a **random port**, not 69, and the client then uses that port as destination. **Port 69 is only used in the very first message.**

### 3. FTP

- Standardized in **1971**, before TCP and IP (updated since). **TCP ports 20 and 21.**
- **Username and password authentication**, but **no encryption** (credentials in plain text). For more security: **FTPS** (FTP over SSL/TLS, FTP Secure) = an upgrade to FTP; **SFTP** (SSH File Transfer Protocol) = a **different protocol** with a similar name.
- More complex than TFTP: file transfers but also **navigating directories, adding and removing directories, listing files**, through **FTP commands** sent by the client. TFTP can't even ask "what files do you have?".
- Two connection types:
  - **Control connection to TCP 21**: established (SYN, SYN-ACK, ACK) to send FTP commands and receive server replies. **Maintained throughout.**
  - **Data connections to TCP 20**: established and terminated **as needed** to transfer files.
- Modes for establishing the data connection:
  - **Active mode** (default, "normal"): **the server initiates** the data TCP connection (first SYN from server to client).
  - **Passive mode**: **the client initiates** the data connection. Needed when the client is **behind a firewall**, which would block a connection initiated from outside (firewalls usually don't permit outside devices to initiate connections) but permits the server's replies.

### 4. Comparison

| | FTP | TFTP |
| :--- | :--- | :--- |
| Transport | **TCP**, connection-based; **20** data, **21** control | **UDP 69**, connectionless (basic connection within the protocol) |
| Functions | Various commands: copy, list, delete, directories... | **Copy a file to or from the server, only** |
| Authentication | **Username and password** | **None** |
| Complexity | More complex | Simple |

### 5. IOS file systems

- `show file systems` lists the file systems (long output). Types:
  - **disk**: storage such as **flash**, where the IOS file is usually stored; at boot, IOS is copied from flash into RAM.
  - **opaque**: specific internal functions, logical systems, not separate storage devices.
  - **nvram**: non-volatile RAM, keeps data without power; holds the **startup-config**.
  - **network**: external file systems, **FTP or TFTP** servers.
- Removed from the latest CCNA: no questions expected.

### 6. Using TFTP and FTP in IOS (IOS upgrade, Packet Tracer demo)

- `show version`: image name (`C2900-UNIVERSALK9-M`, K9 = cryptography), version **15.1(4)M4**. `show flash`: flash contents, including the IOS image.
- **TFTP**: `copy tftp: flash:`; the router prompts for the **server address**, the **source filename** (must be known beforehand, TFTP can't list), then the **destination name** (Enter = same name). The file lands in flash (`show flash`).
- Boot with the new image: **`boot system <path>`** in global config; without it, the router boots the **first IOS file it finds in flash**. **Save the configuration** before `reload`, or `boot system` has no effect. After reboot, `show version` shows **15.5** instead of 15.1.
- Delete the old image: `delete <path>`, confirm, `show flash`.
- **FTP**: first configure `ip ftp username cisco` and `ip ftp password cisco` (same credentials as on the server); then `copy ftp: flash:`, server address, source name, destination name. Rest is identical (`boot system`, save, `reload`).
- Reminder: `copy running-config startup-config` is the same `copy <source> <destination>` command.

### 7. Exam traps

- **FTP: TCP 21 control, TCP 20 data. TFTP: UDP 69.**
- **Active mode**: the server initiates the data connection; **passive mode**: the client initiates it, used **behind a firewall**. Active/passive only apply to the **data** connection: the control connection is always initiated by the client.
- `copy tftp: flash:` = source then destination.
- **Startup-config in NVRAM**; IOS in **flash**.
- TFTP **cannot** create a directory or list the server's contents.
- TFTP and SNMP use **UDP**; HTTP and SMTP use **TCP** (Boson bonus).
- `boot system` + **save** before `reload`.

### 8. IOS commands

```text
R1# show version                       ! running IOS image (K9) and version
R1# show flash                         ! flash contents
R1# show file systems                  ! file systems (disk, opaque, nvram, network)
R1# copy tftp: flash:                  ! copy from a TFTP server; prompts for IP, source file, destination name
R1(config)# ip ftp username jeremy     ! router's FTP credentials (same as on the server)
R1(config)# ip ftp password ccna
R1# copy ftp: flash:                   ! copy from an FTP server
R1(config)# boot system flash:<file>   ! image to boot (otherwise first image found)
R1# write                              ! save before reload, or boot system is ignored
R1# reload                             ! restart
R1# delete flash:<file>                ! delete the old image (confirmation)
R4# copy running-config tftp           ! back up the config to a TFTP server (NetSim)
R4# copy tftp startup-config           ! restore the config into NVRAM (NetSim)
R4# copy startup-config running-config ! apply the startup-config (merged into running-config)
```

### 9. The lab (video #88)

Goal: upgrade R1's IOS via **TFTP** and R2's via **FTP** from SRV1 (10.0.0.1), then reboot and delete the old image. Addresses and a static route to 10.0.0.0/24 on R2 are pre-configured.

- **SRV1**: Services → TFTP: service **enabled by default**, list of OS files; FTP: enabled by default, list of **FTP users** (Packet Tracer default: cisco / cisco; Jeremy created jeremy / ccna).
- **R1 (TFTP)**: `show version` (15.1), `show flash`; `copy tftp flash`, address 10.0.0.1, 15.5 filename (pasted), Enter for the default name; transfer takes seconds; `show flash`. `conf t`, `boot system flash <file>`, `exit`, **`write`** (required before reload), `reload` (fast in Packet Tracer, several minutes on a real router). `show version` → 15.5. `delete flash:<old file>`, confirm, `show flash`.
- **R2 (FTP)**: `show version` (15.1); `ip ftp username jeremy`, `ip ftp password ccna`; `copy ftp flash`, 10.0.0.1, filename, Enter. **FTP is much slower than TFTP in Packet Tracer**: be patient. `show flash`, `boot system flash <file>`, `write`, `reload`, `show version` → 15.5, `delete flash:<old>`, `show flash`.

Boson NetSim bonus "TFTP": another use, **backing up the configuration**. `ipconfig /ip` and `/dg` on PC1 and PC3; ping PC1 from Router4 (password Cisco); `copy running-config tftp`, address 192.168.1.2, name r4config; on PC1 `show tftp-configs` (NetSim command); `hostname MainRouter`; `copy tftp startup-config` (file r4config); `show startup-config` shows hostname Router4 but the running-config still says MainRouter; `copy startup-config running-config` → hostname back to Router4. No need to clear NVRAM before copying into it: the copy **fully replaces** the file; into the running-config (DRAM), files **merge**.

### 10. The quiz (5 questions + 1 Boson)

| Question | Answer | Why |
| :--- | :--- | :--- |
| True statements about FTP? (select two) | **Control connections use TCP port 21** (B); **data connections use TCP port 20** (D) | FTP uses TCP; port 21 for commands and replies, port 20 for data exchange. |
| Which command transfers a file from an external TFTP server to local flash? | **`copy tftp: flash:`** (A) | `copy` source destination: from a TFTP server to flash. |
| R1 behind a firewall wants to reach an external FTP server: true statement? | **R1 should use FTP passive mode for the data connection** (C) | Active/passive only apply to data connections (the client always initiates the control connection). Active: server initiates; passive: client initiates, needed behind a firewall. |
| Which file system stores the startup-config? | **NVRAM** (D) | Non-volatile RAM, keeps data after power loss. |
| Functions NOT possible with TFTP? (select two) | **Create a new directory on a server** (B); **list the contents of a server** (C) | TFTP only copies a file to or from a server. |
| Boson: which Application layer protocols use UDP for unsynchronized, connectionless transfer? (two) | **TFTP** and **SNMP** | TFTP uses UDP (basic internal connection, but no TCP); so does SNMP. HTTP and SMTP (Simple Mail Transfer Protocol) use TCP. |
