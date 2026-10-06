# CCNA Day 42 : SSH / Secure Shell (et Telnet, ligne console, IP de gestion)

> Source : Jeremy's IT Lab, « Free CCNA | SSH | Day 42 » (31 min, vidéo n°85 de la playlist, cours) et « Free CCNA | SSH | Day 42 Lab » (16 min, vidéo n°86, lab Packet Tracer). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Vue d'ensemble

- Sujet d'examen **4.8** : configurer les équipements réseau pour l'**accès distant via SSH**. Contrairement à Syslog et SNMP, **la configuration de SSH est au programme** : à pratiquer en lab.
- SSH permet de se connecter au CLI d'un équipement **à distance**, sans être branché au port console. La vidéo couvre aussi : la sécurité du port console, l'adresse IP de gestion des switches de couche 2, et Telnet.

### 2. Sécurité de la ligne console

- Par défaut, **aucun mot de passe** n'est demandé pour accéder au CLI par le port console : quiconque a un accès physique peut configurer l'équipement.
- `line console 0` : **une seule ligne console**, donc toujours **0** ; une seule connexion console à la fois.
- Méthode 1, mot de passe de ligne : `password ccna` puis **`login`** (sans `login`, le mot de passe n'est pas demandé). Le mot de passe ne s'affiche pas pendant la saisie.
- Méthode 2, comptes locaux : `username jeremy secret ccnp` en config globale, puis dans la ligne **`login local`** : nom d'utilisateur et mot de passe exigés. Le `password` de ligne reste dans la config mais n'est plus utilisé.
- `exec-timeout 3 30` : déconnexion après 3 min 30 s d'inactivité ; bonne pratique si l'on quitte son bureau sans se déconnecter.

### 3. Adresse IP de gestion d'un switch de couche 2

- Routeurs et switches de couche 3 ont des adresses IP pour la gestion à distance. Un **switch de couche 2** ne route pas et n'a pas de table de routage, mais on peut donner une adresse à une **SVI** (*switch virtual interface*) pour y accéder en Telnet ou SSH.
- `interface vlan 1`, `ip address ...`, `no shutdown` si l'interface est désactivée par défaut.
- **`ip default-gateway <ip>`** : indispensable pour communiquer **hors du LAN local** (l'admin PC2 est dans un autre réseau) ; équivalent d'une route par défaut, mais le switch L2 n'ayant pas de table de routage, on utilise cette commande.

### 4. Telnet

- **Telnet** (*Teletype Network*), **1969** : accès distant au CLI. Presque entièrement remplacé par **SSH** (**1995**), plus sûr.
- **Aucun chiffrement** : capture Wireshark, l'invite « password » puis le mot de passe `ccnp` lisibles **en clair**, ainsi que tout le trafic suivant.
- **Le serveur Telnet (l'équipement auquel on se connecte) écoute sur TCP port 23** ; le client est l'équipement qui se connecte.
- Configuration (sur SW1) :
  1. **`enable secret`** obligatoire : sans lui, impossible d'entrer en mode privilégié via Telnet ou SSH.
  2. `username ... secret ...` pour `login local`.
  3. Optionnel : ACL standard limitant les connexions (`access-list 1 permit host <ip-PC2>`).
  4. **`line vty 0 15`** : **16 lignes VTY** (*Virtual TeleType*), donc 16 utilisateurs simultanés ; configurer toutes les lignes à la fois pour une configuration identique.
  5. `login local`, `exec-timeout 5 0` (défaut selon l'équipement, 10 min ici).
  6. **`transport input telnet`** : connexions autorisées sur les VTY : `telnet`, `ssh`, `telnet ssh`, **`all`** (autres protocoles aussi), **`none`** (aucune). Défaut : `none` sur l'équipement de la démo, `all` sur beaucoup d'autres.
  7. **`access-class 1 in`** : applique l'ACL **aux lignes VTY** (ne bloque pas les pings ni le reste du trafic). Ne pas confondre : `access-class` (lignes VTY), `ip access-group` (interface), `access-list` / `ip access-list` (création).
- Vérification : depuis R2, ping OK mais `telnet` → « connection refused by remote host » (ACL) ; depuis PC2, Telnet fonctionne.
- Dans la running-config, les VTY apparaissent en deux blocs (**0 4** et **5 15**) : héritage des anciens IOS à 5 lignes ; sans effet.

### 5. SSH

- **SSH** (*Secure Shell*), **1995**, remplace Telnet. Un *shell* = programme qui expose les services du système d'exploitation à l'utilisateur ; tout CLI est un shell.
- **SSHv2** (2006), révision majeure, plus sûr : à utiliser dès que possible. Un équipement qui supporte v1 et v2 affiche **version 1.99** (ce n'est pas une vraie version, juste « v1 et v2 supportées »).
- **Chiffrement et authentification** des données : dans Wireshark, un paquet SSH n'est qu'une suite de caractères illisibles ; seuls client et serveur ont les clés.
- **SSH utilise TCP port 22** (Telnet TCP 23).
- Prérequis : `show version` → le nom de l'image IOS doit contenir **K9** (support cryptographique). Les images **NPE** (*No Payload Encryption*, exportées vers les pays restreignant le chiffrement) **ne supportent pas SSH**. `show ip ssh` indique si SSH est supporté, s'il est activé (« SSH Disabled - version 1.99 ») et rappelle « Please create RSA keys to enable SSH ».
- **Génération des clés RSA** (chiffrement/déchiffrement, authentification) : `ip domain name jeremysitlab.com` puis **`crypto key generate rsa`** ; les clés sont nommées d'après le **FQDN** (*Fully Qualified Domain Name* = hostname + nom de domaine, ex. SW1.jeremysitlab.com). Taille du **modulus** demandée (2048 bits), ou directement `crypto key generate rsa modulus 2048`. **Au moins 768 bits pour SSHv2** ; plus long = plus sûr mais plus lent. Un message Syslog confirme « SSH has been enabled ».
- La commande est **refusée** si le hostname est celui par défaut (« Please define a hostname other than Router ») ou s'il n'y a **pas de nom de domaine** (« Please define a domain-name first »).
- Configuration SSH complète (démo sur SW1, config Telnet retirée) : `enable secret`, `username`, ACL, **`ip ssh version 2`** (optionnel, recommandé), `line vty 0 15`, **`login local` obligatoire** (`login` seul ne marche pas avec SSH : un nom d'utilisateur est requis ; l'authentification par serveur sera vue plus tard), `exec-timeout`, **`transport input ssh`** (bonne pratique : SSH seul, Telnet désactivé), `access-class 1 in`.
- **Résumé des étapes** : 1) hostname non par défaut ; 2) `ip domain name` ; 3) `crypto key generate rsa` ; 4) enable secret + username/password (ordre indifférent) ; 5) `ip ssh version 2` ; 6) lignes VTY avec `transport input ssh` (+ timeout, ACL...).
- Depuis un PC : **`ssh -l <user> <ip>`** ou `ssh <user>@<ip>`.

### 6. Pièges d'examen

- **TCP 22 = SSH, TCP 23 = Telnet.**
- `crypto key generate rsa` refusé : **hostname non configuré** (défaut « Router ») ou **nom de domaine absent** ; le FQDN nomme la paire de clés.
- **K9** = support SSH ; **NPE** = pas de cryptographie ; **768 bits minimum** pour SSHv2 ; **1.99** = v1 et v2 supportées, pas une version.
- Telnet et SSH : modèle client-serveur, l'équipement **auquel on se connecte est le serveur**, le PC qui se connecte est le client.
- Restreindre SSH à une adresse : ACL **sur les lignes VTY** avec **`access-class`** (pas `ip access-group`), port **TCP 22** si ACL étendue.
- Telnet et SSH ensemble : `transport input telnet ssh` ou `transport input all` ; `transport input none` = rien ; `transport input default` n'existe pas.
- `enable secret` requis pour passer en mode privilégié à distance ; `login local` requis pour SSH.

### 7. Commandes IOS

```text
SW1(config)# hostname SW1                         ! hostname non par défaut (requis pour les clés RSA)
SW1(config)# enable secret ccna                   ! requis pour le mode privilégié via Telnet/SSH
SW1(config)# username jeremy secret ccna          ! compte local (secret > password, mieux chiffré)
SW1(config)# interface vlan 1
SW1(config-if)# ip address 192.168.2.253 255.255.255.0 ! IP de gestion sur la SVI
SW1(config-if)# no shutdown
SW1(config)# ip default-gateway 192.168.2.254     ! passerelle du switch L2
SW1(config)# line console 0                       ! ligne console, toujours 0
SW1(config-line)# password ccna                   ! mot de passe de ligne...
SW1(config-line)# login                           ! ...exigé à la connexion
SW1(config-line)# login local                     ! ou : comptes locaux (username/secret)
SW1(config-line)# exec-timeout 5                  ! déconnexion après 5 min d'inactivité (secondes optionnelles)
SW1(config)# ip domain name jeremysitlab.com      ! nom de domaine (requis pour les clés RSA)
SW1(config)# crypto key generate rsa [modulus 2048] ! génère la paire de clés (>= 768 bits pour SSHv2), active SSH
SW1(config)# ip ssh version 2                     ! SSHv2 uniquement (recommandé)
SW1(config)# ip ssh time-out 90                   ! délai de négociation SSH (défaut 120 s, NetSim)
SW1(config)# access-list 1 permit host 192.168.1.1 ! ACL : seul PC1
SW1(config)# line vty 0 15                        ! les 16 lignes VTY
SW1(config-line)# login local                     ! obligatoire pour SSH
SW1(config-line)# exec-timeout 5
SW1(config-line)# transport input ssh             ! ssh | telnet | telnet ssh | all | none
SW1(config-line)# access-class 1 in               ! ACL appliquée aux VTY
SW1# show version                                 ! image IOS : K9 = SSH supporté
SW1# show ip ssh                                  ! SSH activé ?, version 1.99, time-out
SW1# show ssh                                     ! sessions SSH en cours : version, chiffrement, utilisateur
C:\> ssh -l jeremy 192.168.2.253                  ! depuis un PC (ou ssh jeremy@192.168.2.253)
C:\> telnet 192.168.1.1
```

### 8. Le lab (vidéo n°86)

Objectif : configurer SW2 (neuf) depuis Laptop1 par la console, puis l'accès SSH limité à PC1.

1. **Console** : câble console (bleu clair) entre le port RS232 de Laptop1 et le port console de SW2 ; Desktop → Terminal, réglages par défaut. `hostname SW2` ; `enable secret ccna` (sensible à la casse ; sans enable secret, pas de mode privilégié en Telnet/SSH, sauf niveau de privilège élevé sur l'utilisateur, vu plus tard) ; `username jeremy secret ccna` (`password` = stockage en clair, `service password-encryption` chiffre faiblement, `secret` est préférable) ; `interface vlan 1`, `ip address 192.168.2.253 255.255.255.0`, `no shutdown` (SVI désactivée par défaut sur ce modèle) ; `ip default-gateway 192.168.2.254`.
2. **Ligne console** : `line console 0`, `login local`, `exec-timeout 5` (pas besoin de préciser 0 seconde). Test : `end`, `exit`, Entrée → username/password demandés.
3. **SSH** : `crypto key generate rsa` échoue (pas de domaine) ; `ip domain name jeremysitlab.com` ; `crypto key generate rsa`, modulus 2048 : OK. `access-list 1 permit host 192.168.1.1` (inutile de préciser le port : `transport input ssh` suffit). `line vty 0 15`, `login local`, `exec-timeout 5`, `transport input ssh`, `access-class 1 in`.
4. **Vérification** : depuis R2, `ping 192.168.2.253` OK mais `ssh -l jeremy 192.168.2.253` refusé (ACL). Depuis PC1, ping OK (ARP lent, premiers pings peuvent échouer) puis `ssh -l jeremy 192.168.2.253`, mot de passe ccna : connecté.

Bonus Boson NetSim « Configuring SSH » : Telnet vers Router1 fonctionne (mot de passe boson), SSH refusé ; `show ip ssh` → disabled ; `ip ssh version 2` → « create RSA keys » ; `crypto key generate rsa` refusé sans domaine ; `ip domain name boson.com` ; clés 1024 bits ; **`ip ssh time-out 90`** (défaut et max **120 s**, visibles avec `show ip ssh`) ; `username admin privilege 15 password boson` ; `line vty 0 15`, `transport input ssh` ; SSH depuis PC1 OK ; `enable secret boson` ajouté pour pouvoir faire `enable` ; **`show ssh`** (différent de `show ip ssh`) : connexion 0, version 2, chiffrement, état, utilisateur admin ; Telnet maintenant refusé.

### 9. Le quiz (5 questions + 1 Boson)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| `crypto key generate rsa` est rejetée : causes possibles ? (deux) | **Hostname non configuré** (A) et **nom de domaine DNS non configuré** (E) | Le FQDN (hostname + domaine) nomme la paire de clés ; le hostname par défaut « Router » ne peut pas être utilisé. |
| Quelles commandes autorisent Telnet et SSH sur les VTY ? (deux, chacune complète) | **`transport input telnet ssh`** (C) et **`transport input all`** (D) | D autorise aussi d'autres protocoles. A, `transport input default`, n'existe pas ; B, `transport input none`, n'autorise rien. |
| N'autoriser que 192.168.1.1 à se connecter à R1 en SSH : quelle configuration ? | **B** | SSH = TCP 22 ; il faut configurer les lignes VTY et appliquer l'ACL avec `access-class` ; seule B remplit ces trois conditions. |
| Affirmations vraies sur SSH ? (deux) | **Les images IOS K9 supportent SSH** (B) ; **clés d'au moins 768 bits requises pour SSHv2** (F) | A faux : les clés RSA sont requises ; C faux : 1.99 n'est pas une version mais signifie v1 et v2 supportées ; D faux : SSH chiffre ; E faux : les images NPE ne supportent pas la cryptographie. |
| Un admin sur PC1 configure SW1 via SSH : rôle de SW1 ? | **Serveur SSH** (B) | Modèle client-serveur : l'équipement auquel on se connecte est le serveur, PC1 est le client. |
| Boson : Router1 (hostname Router1, image K9, sans domaine ni clés), `crypto key generate rsa` : quel message ? | **« Please define a domain-name first »** (B) | Le hostname est déjà non par défaut (pas D) ; le nom de clé nécessite le FQDN donc un domaine (pas A) ; C est le message de `show ip ssh` ; SSHv2 n'est pas requis pour générer les clés (pas E). |

---

## 🇬🇧 English version

### 1. Overview

- Exam topic **4.8**: configure network devices for **remote access using SSH**. Unlike Syslog and SNMP, **SSH configuration is an exam topic**: practice it in labs.
- SSH connects to a device's CLI **remotely**, without a console cable. The video also covers console port security, Layer 2 switch management IP, and Telnet.

### 2. Console line security

- By default **no password** is needed to access the CLI via the console port: anyone with physical access can configure the device.
- `line console 0`: there is **a single console line**, so always **0**; only one console connection at a time.
- Method 1, line password: `password ccna` then **`login`** (without `login`, the password is not required). The password is not displayed as you type.
- Method 2, local accounts: `username jeremy secret ccnp` in global config, then on the line **`login local`**: username and password required. The line `password` stays in the config but is no longer used.
- `exec-timeout 3 30`: logs the user out after 3 min 30 s of inactivity; good practice if you leave your desk without logging out.

### 3. Layer 2 switch management IP

- Routers and Layer 3 switches have IP addresses for remote management. A **Layer 2 switch** doesn't route and has no routing table, but an address can be assigned to an **SVI** (switch virtual interface) to allow Telnet or SSH connections.
- `interface vlan 1`, `ip address ...`, `no shutdown` if shut down by default.
- **`ip default-gateway <ip>`**: required to communicate **outside the local LAN** (admin PC2 is in another network); like a default route, but a Layer 2 switch has no routing table, so this command is used instead.

### 4. Telnet

- **Telnet** (Teletype Network), **1969**: remote CLI access. Almost entirely replaced by **SSH** (**1995**), more secure.
- **No encryption**: Wireshark capture shows the "password" prompt and then the password `ccnp` **in plain text**, as well as all later traffic.
- **The Telnet server (the device being connected to) listens on TCP port 23**; the client is the connecting device.
- Configuration (on SW1):
  1. **`enable secret`** required: without it, privileged exec mode is not accessible via Telnet or SSH.
  2. `username ... secret ...` for `login local`.
  3. Optional: standard ACL restricting connections (`access-list 1 permit host <PC2-ip>`).
  4. **`line vty 0 15`**: **16 VTY lines** (Virtual TeleType), so 16 simultaneous users; configure all lines at once so they share the same configuration.
  5. `login local`, `exec-timeout 5 0` (default depends on device, 10 min here).
  6. **`transport input telnet`**: allowed VTY connections: `telnet`, `ssh`, `telnet ssh`, **`all`** (other protocols too), **`none`** (nothing). Default: `none` on the demo device, `all` on many others.
  7. **`access-class 1 in`**: applies the ACL **to the VTY lines** (pings and other traffic still work). Don't confuse: `access-class` (VTY lines), `ip access-group` (interface), `access-list` / `ip access-list` (creation).
- Verification: from R2, ping OK but `telnet` → "connection refused by remote host" (ACL); from PC2, Telnet works.
- In the running-config, VTY lines show as two blocks (**0 4** and **5 15**): a leftover from old IOS with 5 lines; no effect.

### 5. SSH

- **SSH** (Secure Shell), **1995**, replaces Telnet. A *shell* = a program exposing the OS's services to a user; any CLI is a shell.
- **SSHv2** (2006), major revision, more secure: use it whenever possible. A device supporting both v1 and v2 shows **version 1.99** (not a real version, just "v1 and v2 supported").
- **Encryption and authentication** of data: in Wireshark an SSH packet is just a seemingly random string; only client and server have the keys.
- **SSH uses TCP port 22** (Telnet TCP 23).
- Prerequisite: `show version` → the IOS image name must contain **K9** (cryptographic support). **NPE** images (No Payload Encryption, exported to countries restricting encryption) **do not support SSH**. `show ip ssh` says whether SSH is supported, enabled ("SSH Disabled - version 1.99") and hints "Please create RSA keys to enable SSH".
- **RSA key generation** (encryption/decryption, authentication): `ip domain name jeremysitlab.com` then **`crypto key generate rsa`**; the keys are named after the **FQDN** (Fully Qualified Domain Name = hostname + domain name, e.g. SW1.jeremysitlab.com). The **modulus** size is prompted (2048 bits), or directly `crypto key generate rsa modulus 2048`. **At least 768 bits for SSHv2**; longer = more secure but slower. A Syslog message confirms "SSH has been enabled".
- The command is **rejected** if the hostname is the default ("Please define a hostname other than Router") or if there is **no domain name** ("Please define a domain-name first").
- Full SSH configuration (demo on SW1, Telnet config removed): `enable secret`, `username`, ACL, **`ip ssh version 2`** (optional, recommended), `line vty 0 15`, **`login local` required** (`login` alone doesn't work with SSH: a username is needed; authentication servers come later), `exec-timeout`, **`transport input ssh`** (best practice: SSH only, Telnet disabled), `access-class 1 in`.
- **Summary of steps**: 1) non-default hostname; 2) `ip domain name`; 3) `crypto key generate rsa`; 4) enable secret + username/password (order doesn't matter); 5) `ip ssh version 2`; 6) VTY lines with `transport input ssh` (+ timeout, ACL...).
- From a PC: **`ssh -l <user> <ip>`** or `ssh <user>@<ip>`.

### 6. Exam traps

- **TCP 22 = SSH, TCP 23 = Telnet.**
- `crypto key generate rsa` rejected: **hostname not configured** (default "Router") or **domain name missing**; the FQDN names the key pair.
- **K9** = SSH supported; **NPE** = no cryptography; **768 bits minimum** for SSHv2; **1.99** = v1 and v2 supported, not a version.
- Telnet and SSH: client-server model, the device **being connected to is the server**, the connecting PC is the client.
- Restrict SSH to one address: ACL **on the VTY lines** with **`access-class`** (not `ip access-group`), port **TCP 22** if extended ACL.
- Telnet and SSH together: `transport input telnet ssh` or `transport input all`; `transport input none` = nothing; `transport input default` doesn't exist.
- `enable secret` needed for privileged exec mode remotely; `login local` needed for SSH.

### 7. IOS commands

```text
SW1(config)# hostname SW1                         ! non-default hostname (required for RSA keys)
SW1(config)# enable secret ccna                   ! required for privileged exec via Telnet/SSH
SW1(config)# username jeremy secret ccna          ! local account (secret > password, stronger encryption)
SW1(config)# interface vlan 1
SW1(config-if)# ip address 192.168.2.253 255.255.255.0 ! management IP on the SVI
SW1(config-if)# no shutdown
SW1(config)# ip default-gateway 192.168.2.254     ! Layer 2 switch default gateway
SW1(config)# line console 0                       ! console line, always 0
SW1(config-line)# password ccna                   ! line password...
SW1(config-line)# login                           ! ...required at login
SW1(config-line)# login local                     ! or: local accounts (username/secret)
SW1(config-line)# exec-timeout 5                  ! logout after 5 min idle (seconds optional)
SW1(config)# ip domain name jeremysitlab.com      ! domain name (required for RSA keys)
SW1(config)# crypto key generate rsa [modulus 2048] ! generate the key pair (>= 768 bits for SSHv2), enables SSH
SW1(config)# ip ssh version 2                     ! SSHv2 only (recommended)
SW1(config)# ip ssh time-out 90                   ! SSH negotiation timeout (default 120 s, NetSim)
SW1(config)# access-list 1 permit host 192.168.1.1 ! ACL: PC1 only
SW1(config)# line vty 0 15                        ! all 16 VTY lines
SW1(config-line)# login local                     ! required for SSH
SW1(config-line)# exec-timeout 5
SW1(config-line)# transport input ssh             ! ssh | telnet | telnet ssh | all | none
SW1(config-line)# access-class 1 in               ! ACL applied to VTY lines
SW1# show version                                 ! IOS image: K9 = SSH supported
SW1# show ip ssh                                  ! SSH enabled?, version 1.99, time-out
SW1# show ssh                                     ! current SSH sessions: version, encryption, user
C:\> ssh -l jeremy 192.168.2.253                  ! from a PC (or ssh jeremy@192.168.2.253)
C:\> telnet 192.168.1.1
```

### 8. The lab (video #86)

Goal: configure SW2 (new) from Laptop1 via console, then SSH access limited to PC1.

1. **Console**: console cable (light blue) between Laptop1's RS232 port and SW2's console port; Desktop → Terminal, default settings. `hostname SW2`; `enable secret ccna` (case-sensitive; without an enable secret, no privileged exec over Telnet/SSH, unless a high privilege level is set on the user, covered later); `username jeremy secret ccna` (`password` = stored in plain text, `service password-encryption` is weak, `secret` is better); `interface vlan 1`, `ip address 192.168.2.253 255.255.255.0`, `no shutdown` (SVI shut down by default on this model); `ip default-gateway 192.168.2.254`.
2. **Console line**: `line console 0`, `login local`, `exec-timeout 5` (no need to specify 0 seconds). Test: `end`, `exit`, Enter → username/password requested.
3. **SSH**: `crypto key generate rsa` fails (no domain); `ip domain name jeremysitlab.com`; `crypto key generate rsa`, modulus 2048: OK. `access-list 1 permit host 192.168.1.1` (no need to specify the port: `transport input ssh` handles it). `line vty 0 15`, `login local`, `exec-timeout 5`, `transport input ssh`, `access-class 1 in`.
4. **Verification**: from R2, `ping 192.168.2.253` OK but `ssh -l jeremy 192.168.2.253` refused (ACL). From PC1, ping OK (slow ARP, first pings may fail) then `ssh -l jeremy 192.168.2.253`, password ccna: connected.

Boson NetSim bonus "Configuring SSH": Telnet to Router1 works (password boson), SSH refused; `show ip ssh` → disabled; `ip ssh version 2` → "create RSA keys"; `crypto key generate rsa` rejected without a domain; `ip domain name boson.com`; 1024-bit keys; **`ip ssh time-out 90`** (default and max **120 s**, shown by `show ip ssh`); `username admin privilege 15 password boson`; `line vty 0 15`, `transport input ssh`; SSH from PC1 OK; `enable secret boson` added to allow `enable`; **`show ssh`** (different from `show ip ssh`): connection 0, version 2, encryption, state, user admin; Telnet now refused.

### 9. The quiz (5 questions + 1 Boson)

| Question | Answer | Why |
| :--- | :--- | :--- |
| `crypto key generate rsa` is rejected: possible causes? (select two) | **Hostname not configured** (A) and **DNS domain name not configured** (E) | The FQDN (hostname + domain) names the key pair; the default hostname "Router" cannot be used. |
| Which commands allow both Telnet and SSH on the VTY lines? (two, each a complete solution) | **`transport input telnet ssh`** (C) and **`transport input all`** (D) | D also allows other protocols. A, `transport input default`, isn't real; B, `transport input none`, allows nothing. |
| Allow only 192.168.1.1 to connect to R1 via SSH: which configuration? | **B** | SSH = TCP 22; the VTY lines must be configured and the ACL applied with `access-class`; only B meets all three. |
| True statements about SSH? (select two) | **K9 IOS images support SSH** (B); **key length of at least 768 bits required for SSHv2** (F) | A wrong: RSA keys are required; C wrong: 1.99 isn't a version, it means v1 and v2 supported; D wrong: SSH encrypts; E wrong: NPE images don't support cryptography. |
| An admin on PC1 configures SW1 via SSH: SW1's role? | **SSH server** (B) | Client-server model: the device being connected to is the server, PC1 is the client. |
| Boson: Router1 (hostname Router1, K9 image, no domain or keys), `crypto key generate rsa`: which message? | **"Please define a domain-name first"** (B) | The hostname is already non-default (not D); the key name needs the FQDN, hence a domain (not A); C is the `show ip ssh` hint; SSHv2 isn't needed to generate keys (not E). |
