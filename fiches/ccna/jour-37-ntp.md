# CCNA Day 37 : NTP / Network Time Protocol

> Source : Jeremy's IT Lab, « Free CCNA | NTP | Day 37 » (42 min, vidéo n°75 de la playlist, cours) et « Free CCNA | NTP | Day 37 Lab » (19 min, vidéo n°76, lab Packet Tracer). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Pourquoi l'heure est importante

- Tout équipement (routeur, switch, PC, téléphone) a une horloge interne. Sujet d'examen **4.2** : configurer et vérifier NTP en mode client et serveur (première vidéo de la section 4.0, IP Services).
- `show clock` affiche l'heure ; le **fuseau par défaut est UTC** (*Coordinated Universal Time*).
- `show clock detail` montre la **source de temps** (*time source*). Par défaut : le **calendrier matériel** (*hardware calendar*), l'horloge interne intégrée. Un **astérisque** devant l'heure signifie qu'elle n'est **pas considérée comme fiable** (*not authoritative*) : l'horloge matérielle **dérive** (*drift*) avec le temps.
- Raison principale pour le CCNA : des **logs exacts pour le dépannage** (`show logging`). Exemple de Jeremy : R2 voit un voisin OSPF 10.0.0.6 passer FULL/DOWN entre 1h06 et 1h09 ; sur R3 les mêmes événements sont datés du 23 mai 2008 à 16h30 : impossible de corréler les logs. Syslog sera vu dans une vidéo ultérieure.

### 2. Configuration manuelle de l'heure

- **Horloge logicielle** (*clock*) : `clock set hh:mm:ss <jour> <mois> <année>` (jour et mois dans l'un ou l'autre ordre). Après, la source devient **« user configuration »**. Commande en **mode privilégié**, pas en configuration globale : ces réglages **ne font pas partie de la running-config**.
- **Horloge matérielle** (*calendar*) : `calendar set`, même syntaxe ; vérification avec `show calendar`. Horloge et calendrier sont **séparés** et configurables séparément.
- Synchroniser les deux :
  - `clock update-calendar` : le **calendrier** prend l'heure de l'horloge.
  - `clock read-calendar` : l'**horloge** prend l'heure du calendrier.
- **Fuseau horaire** : `clock timezone <nom> <décalage-heures> [minutes]` en **mode de configuration globale** (fait partie de la running-config). Le nom est un simple mot, non vérifié (exemple `clock timezone JST 9`, Japon = UTC+9). L'heure affichée saute immédiatement du décalage, car les réglages précédents étaient en UTC.
- **Heure d'été** (*daylight saving time*, *summer time*) : `clock summer-time <nom> recurring <début> <fin>` en configuration globale. Début et fin = **semaine, jour de semaine, mois, heure**. Exemple Canada : `clock summer-time EDT recurring 2 Sunday March 2:00 1 Sunday November 2:00`. Le mot-clé `date` fixe une date précise ; l'offset optionnel vaut **60 minutes** par défaut. Le signe `$` dans le terminal indique une ligne trop longue, tronquée à l'affichage.

### 3. Les bases de NTP

- La configuration manuelle n'est pas évolutive et les horloges dérivent. **NTP** synchronise automatiquement l'heure sur des **serveurs NTP** via le réseau (exemple : Windows se synchronise sur `time.windows.com`, résolu en adresse IP par **DNS**, aperçu avec `nslookup time.google.com` vers 8.8.8.8).
- Les **clients NTP** demandent l'heure aux **serveurs NTP** et s'y synchronisent. Un équipement peut être **serveur et client en même temps**.
- Précision approximative : **1 ms** dans le même LAN, **50 ms** via WAN ou Internet.
- **Stratum** : « distance » d'un serveur par rapport à l'horloge de référence (*reference clock*). Plus le stratum est élevé, moins le serveur est considéré précis.
- **NTP utilise UDP port 123.**
- Hiérarchie : **horloge de référence = stratum 0** (horloge atomique, horloge GPS, exemple de l'observatoire naval américain). Serveurs directement connectés à une horloge de référence = **stratum 1**. Stratum 2 prend son heure du stratum 1, etc. **Stratum 15 est le maximum** : au-delà, considéré non fiable, l'équipement ne se synchronise pas. Un équipement Cisco ne peut pas prendre l'heure directement d'une horloge stratum 0, mais peut utiliser un serveur stratum 1.
- **Peering NTP** : des équipements du même stratum se « peerent » pour une heure plus précise et comme secours s'ils perdent le serveur de stratum inférieur : mode **symmetric active**.
- Trois modes sur Cisco : **server mode, client mode, symmetric active mode**, cumulables simultanément. Un client peut se synchroniser à **plusieurs serveurs**.
- Terminologie : **serveurs primaires** (*primary servers*) = synchronisés directement sur une horloge de référence, stratum 1 ; **serveurs secondaires** (*secondary servers*) = prennent l'heure d'autres serveurs NTP, en mode serveur et client à la fois, stratum 2 et plus.

### 4. Configurer NTP (démonstration GNS3, R1 vers les serveurs Google)

- `ntp server <ip>` (configuration globale), répété pour les quatre adresses IPv4 de `time.google.com`. L'ordre n'importe pas : le routeur interroge tous les serveurs et choisit le meilleur ; le choix peut changer. Configurer plusieurs serveurs assure une source fiable. `ntp server <ip> prefer` force la préférence pour un serveur, les autres deviennent secours.
- `show ntp associations` : `*` = **sys.peer**, serveur auquel le routeur se synchronise actuellement ; `+` = candidat ; `~` = serveur configuré. **outlyer** ou **falseticker** = le routeur ne se synchronisera pas à ce serveur. Colonne **st** = stratum du serveur ; colonne **ref clock** = sa référence.
- `show ntp status` : première ligne **« Clock is synchronized »**, stratum du routeur lui-même (R1 = **stratum 2** car synchronisé sur des serveurs stratum 1 : il devient automatiquement serveur NTP un stratum plus haut), adresse de la référence.
- **NTP n'utilise que UTC** : configurer le fuseau sur chaque équipement.
- NTP ne met pas à jour le calendrier par défaut : `ntp update-calendar` configure le routeur à mettre à jour l'horloge matérielle avec l'heure NTP. Utile car au redémarrage, l'horloge matérielle initialise l'horloge logicielle.
- R2 utilise R1 comme serveur : Jeremy crée une **interface loopback** sur R1 (10.1.1.1, annoncée par OSPF) et `ntp source loopback0` pour que les messages NTP de R1 partent de 10.1.1.1. Avantage : l'adresse ne dépend pas de l'état d'une interface physique (si G0/0 de R2 tombe, R3 annonce encore la route vers 10.1.1.1). **Sans `ntp source`, R2 et R3 refusent de se synchroniser avec R1** (les réponses viendraient d'une autre adresse).
- R2 : `ntp server 10.1.1.1` ; `show ntp associations` montre la référence de R1 (un serveur Google) et son stratum 2 ; `show ntp status` : R2 = **stratum 3**.
- R3 avec deux serveurs (R1 10.1.1.1 et R2 10.2.2.2) : R3 préfère **R1**, car **un stratum plus bas est préféré** (plus proche de la source, plus précis).
- **Sans serveur NTP disponible** : `ntp master [stratum]` fait du routeur une horloge maîtresse NTP. `show ntp associations` montre alors une association vers **127.127.1.1**, une **adresse de loopback** (plage réservée 127.0.0.0/8 ; à ne pas confondre avec une interface loopback, qui est une interface virtuelle annonçable par OSPF, alors qu'une adresse loopback est purement interne) : le routeur se sert de lui-même comme référence. Stratum affiché 7, stratum réel du routeur (`show ntp status`) = **8 : stratum par défaut de `ntp master`**.
- **Symmetric active** : `ntp peer <ip>` entre R2 et R3 (tous deux stratum 9 puisque R1 est stratum 8).
- **Authentification NTP** (optionnelle, peut-être à l'examen) : le client vérifie que le serveur utilise le même mot de passe. Même configuration sur serveur et clients :
  1. `ntp authenticate` (activer) ;
  2. `ntp authentication-key 1 md5 <mot-de-passe>` (créer la clé) ;
  3. `ntp trusted-key 1` (déclarer la clé de confiance, **étape à ne pas oublier**) ;
  4. sur les clients seulement : `ntp server <ip> key 1`, et éventuellement `ntp peer <ip> key 1`.

### 5. Pièges d'examen

- Fuseau par défaut : **UTC**. NTP ne transmet que de l'heure UTC ; le fuseau se configure localement.
- `clock set` et `calendar set` : mode **privilégié**, hors running-config ; `clock timezone` et `clock summer-time` : **configuration globale**, dans la running-config.
- `clock read-calendar` : l'horloge logicielle **lit** le calendrier ; `clock update-calendar` : met **à jour** le calendrier depuis l'horloge.
- UDP **123**, stratum max **15**, horloge de référence **stratum 0**, `ntp master` par défaut **stratum 8** (association affichée 127.127.1.1 stratum 7). `ntp server 127.127.1.1` est **rejeté** par le routeur.
- `ntp server` = mode **client** ; `ntp master` = mode **serveur** ; `ntp peer` = **symmetric active** ; `ntp client` **n'existe pas**.
- Un client NTP devient automatiquement serveur, stratum +1. Stratum le plus bas = serveur préféré.
- Question Boson ExSim : `ntp server` active le mode **static client** (le mode *broadcast client* n'est pas au programme).

### 6. Commandes IOS

```text
Router# show clock                      ! heure, fuseau (UTC par défaut)
Router# show clock detail               ! + source de temps ; * = non fiable
Router# show calendar                   ! horloge matérielle (absente dans Packet Tracer)
Router# show logging                    ! logs de l'équipement (aperçu Syslog)
Router# clock set 12:00:00 30 Dec 2020  ! régler l'horloge logicielle
Router# calendar set 12:00:00 30 Dec 2020 ! régler l'horloge matérielle
Router# clock update-calendar           ! calendrier <- horloge
Router# clock read-calendar             ! horloge <- calendrier
Router(config)# clock timezone JST 9    ! nom libre + décalage par rapport à UTC
Router(config)# clock summer-time EDT recurring 2 Sunday March 2:00 1 Sunday November 2:00
Router(config)# ntp server 216.239.35.0 [prefer] ! mode client ; prefer = serveur préféré
Router(config)# ntp source loopback0    ! source des messages NTP (indispensable si on annonce une loopback)
Router(config)# ntp update-calendar     ! NTP met aussi à jour l'horloge matérielle
Router(config)# ntp master [stratum]    ! horloge maîtresse, stratum 8 par défaut
Router(config)# ntp peer 10.0.23.3      ! symmetric active mode
Router(config)# ntp authenticate        ! activer l'authentification
Router(config)# ntp authentication-key 1 md5 jeremysitlab ! créer la clé
Router(config)# ntp trusted-key 1       ! déclarer la clé de confiance
Router(config)# ntp server 10.0.12.1 key 1 ! client : clé à utiliser avec ce serveur
Router(config)# ntp peer 10.0.23.3 key 1   ! authentifier aussi le peer
Router# show ntp associations           ! * sys.peer, + candidat, ~ configuré, st = stratum
Router# show ntp status                 ! Clock is synchronized, stratum du routeur, référence
```

### 7. Le lab (vidéo n°76)

Objectif : R1 se synchronise sur SRV1 (1.1.1.1) via Internet, puis R2 et R3 se synchronisent sur R1 avec authentification. Dans Packet Tracer, `clock summer-time`, `ntp source`, `ntp peer` et `show calendar` **n'existent pas**.

1. **Heure manuelle** sur R1, R2, R3 : `clock set 12:00:00 Dec 30 2020` (en UTC, fuseau pas encore configuré) ; `show clock detail` : source « user configuration ». Régler l'heure proche de celle du serveur NTP **accélère** la synchronisation, qui peut être longue.
2. **Fuseau** : `clock timezone JST 9` sur les trois routeurs ; `do show clock detail` montre 9 h d'avance.
3. **R1 client de 1.1.1.1** : `ntp server 1.1.1.1`. `show ntp associations` : l'astérisque n'apparaît qu'après avoir fait **avancer la simulation** (flèches). SRV1 est stratum 1 ; `show ntp status` : R1 stratum 2 ; `show clock detail` : source **NTP**.
4. **R1 maître stratum 8** : `ntp master` (défaut = 8), secours pour R2 et R3 si R1 perd 1.1.1.1. Authentification sur R1 : `ntp authenticate`, `ntp authentication-key 1 md5 jeremysitlab`, `ntp trusted-key 1`. Sur R2 : les trois mêmes commandes puis `ntp server 192.168.12.1 key 1` ; sur R3 : idem puis `ntp server 192.168.13.1 key 1`. Faute de `ntp source`, on utilise l'adresse de l'interface physique de R1 (G0/1), pas une loopback. Vérifier après avance de simulation : `show ntp associations` (astérisque), `show clock detail` (source NTP).
5. **Calendrier** : `ntp update-calendar` sur R2, R3, R1 (sans effet visible dans Packet Tracer).

Bonus Boson NetSim « Configuring NTP 1 » : `clock set 9:00:00 25 JUL 2013`, `ntp master 3` sur Router1, `ntp server 10.0.12.1` sur Router2, `ntp server 10.0.23.2` sur Router3 ; `show ntp status` : Router1 stratum 3 (référence = adresse loopback), Router2 stratum 4, Router3 stratum 5 ; l'adresse de référence diffère sur chaque routeur car chacun se synchronise sur une horloge différente.

### 8. Le quiz (5 questions + 1 Boson)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quelle commande fait que le routeur ajuste son horloge logicielle sur l'horloge matérielle ? | **`clock read-calendar`** (C) | D, `clock update-calendar`, fait l'inverse (calendrier ← horloge). A et B ne sont pas des commandes valides. |
| Quelle commande configure le fuseau horaire de l'équipement ? | **`clock timezone <nom> <offset>`** en configuration globale (D) | Contrairement à d'autres commandes d'heure, celle-ci se fait en config globale, pas en mode privilégié. `clock set` ne configure pas le fuseau. |
| D'après la sortie (association 127.127.1.1, stratum 8), quelle commande a été configurée sur R1 ? | **`ntp master 9`** (A) | L'adresse loopback 127.127.1.1 indique `ntp master`. Avec le stratum par défaut (8, options C et D) l'association afficherait stratum 7 ; ici 8, donc `ntp master 9`. B, `ntp server 127.127.1.1`, est rejetée par le routeur. |
| Quelle commande met le routeur en mode client NTP ? | **`ntp server 216.239.35.0`** (C) | A, `ntp peer`, = symmetric active ; B, `ntp master`, = mode serveur ; D, `ntp client`, n'existe pas. |
| Quelles commandes faut-il sur un client NTP pour activer l'authentification ? (toutes celles qui s'appliquent) | **C `ntp authenticate`, D `ntp authentication-key`, F `ntp trusted-key`, G `ntp server ... key`** | C active l'authentification, D crée la clé, F la déclare de confiance, G indique la clé à utiliser avec le serveur. (À l'examen réel, la question précise toujours combien de réponses choisir.) |
| Boson : qu'active `ntp server` en configuration globale ? | **Static client mode** (A) | On indique au routeur le serveur auquel se synchroniser : il devient client. Pas symmetric active (B), pas broadcast client (C, hors programme), pas server mode (D), pas authentication (E). |

---

## 🇬🇧 English version

### 1. Why time matters

- Every device (router, switch, PC, phone) has an internal clock. Exam topic **4.2**: configure and verify NTP in client and server mode (first video of section 4.0, IP Services).
- `show clock` displays the time; the **default time zone is UTC** (Coordinated Universal Time).
- `show clock detail` shows the **time source**. Default: the **hardware calendar**, the built-in internal clock. An **asterisk** before the time means it is **not authoritative**: the hardware clock **drifts** over time.
- Main reason for the CCNA: **accurate logs for troubleshooting** (`show logging`). Jeremy's example: R2 sees OSPF neighbor 10.0.0.6 moving FULL/DOWN between 1:06 AM and 1:09 AM; on R3 the same events are stamped May 23rd 2008, 4:30 PM: logs cannot be correlated. Syslog comes in a later video.

### 2. Manual time configuration

- **Software clock**: `clock set hh:mm:ss <day> <month> <year>` (day and month in either order). The source then becomes **"user configuration"**. Done from **privileged exec mode**, not global config: these settings are **not part of the running-config**.
- **Hardware clock (calendar)**: `calendar set`, same syntax; check with `show calendar`. Clock and calendar are **separate** and configured separately.
- Syncing the two:
  - `clock update-calendar`: the **calendar** takes the clock's time.
  - `clock read-calendar`: the **clock** takes the calendar's time.
- **Time zone**: `clock timezone <name> <hours-offset> [minutes]` in **global config mode** (part of the running-config). The name is just a word, not checked (e.g. `clock timezone JST 9`, Japan = UTC+9). The displayed time immediately jumps by the offset because the earlier settings were in UTC.
- **Daylight saving time** (summer time): `clock summer-time <name> recurring <start> <end>` in global config. Start and end = **week, weekday, month, time**. Canada example: `clock summer-time EDT recurring 2 Sunday March 2:00 1 Sunday November 2:00`. The `date` keyword sets a specific date; the optional offset defaults to **60 minutes**. A `$` in the terminal means the line is too long and is cut off on screen.

### 3. NTP basics

- Manual configuration is not scalable and clocks drift. **NTP** automatically syncs time over the network to **NTP servers** (e.g. Windows syncs to `time.windows.com`, resolved to an IP address by **DNS**, previewed with `nslookup time.google.com` via 8.8.8.8).
- **NTP clients** request the time from **NTP servers** and sync to it. A device can be **server and client at the same time**.
- Rough accuracy: about **1 ms** within the same LAN, about **50 ms** over a WAN or the Internet.
- **Stratum**: the "distance" of a server from the original **reference clock**. The higher the stratum, the less accurate the server is considered.
- **NTP uses UDP port 123.**
- Hierarchy: **reference clock = stratum 0** (atomic clock, GPS clock, e.g. the US Naval Observatory clock). Servers directly connected to a reference clock = **stratum 1**. Stratum 2 gets its time from stratum 1, and so on. **Stratum 15 is the maximum**: anything above is unreliable and the device will not sync to it. Cisco devices cannot get time directly from a stratum 0 clock, but can use a stratum 1 server.
- **NTP peering**: devices at the same stratum peer to provide more accurate time and as a backup if they lose the lower-stratum server: **symmetric active** mode.
- Three modes on Cisco devices: **server mode, client mode, symmetric active mode**, all possible at the same time. A client can sync to **multiple servers**.
- Terminology: **primary servers** = sync directly to a reference clock, stratum 1; **secondary servers** = get time from other NTP servers, server and client mode at once, stratum 2 and above.

### 4. Configuring NTP (GNS3 demo, R1 to Google's servers)

- `ntp server <ip>` (global config), repeated for the four IPv4 addresses of `time.google.com`. Order does not matter: the router asks all of them and selects the best, quickest responses; the selection can change. Multiple servers keep a reliable time source. `ntp server <ip> prefer` makes one server preferred, the others backups.
- `show ntp associations`: `*` = **sys.peer**, the server currently synced to; `+` = candidate; `~` = configured. **outlyer** or **falseticker** = the router will not sync to that server. **st** column = the server's stratum; **ref clock** = its reference.
- `show ntp status`: top line **"Clock is synchronized"**, the router's own stratum (R1 = **stratum 2** because it syncs to stratum 1 servers: it automatically becomes an NTP server one stratum higher), reference address.
- **NTP uses only UTC**: configure the time zone on each device.
- NTP does not update the calendar by default: `ntp update-calendar` makes the router update the hardware clock with NTP time. Useful because on restart the hardware clock initializes the software clock.
- R2 uses R1 as its server: Jeremy creates a **loopback interface** on R1 (10.1.1.1, advertised by OSPF) and `ntp source loopback0` so R1's NTP messages come from 10.1.1.1. Benefit: the address does not depend on any physical interface's status (if R2's G0/0 fails, R3 still advertises a route to 10.1.1.1). **Without `ntp source`, R2 and R3 won't sync with R1** (replies would come from another address).
- R2: `ntp server 10.1.1.1`; `show ntp associations` shows R1's reference (a Google server) and its stratum 2; `show ntp status`: R2 = **stratum 3**.
- R3 with two servers (R1 10.1.1.1 and R2 10.2.2.2): R3 prefers **R1**, because **lower stratum is preferred** (closer to the source, more accurate).
- **No NTP server available**: `ntp master [stratum]` makes the device an NTP master clock. `show ntp associations` then shows an association with **127.127.1.1**, a **loopback address** (reserved 127.0.0.0/8 range; not to be confused with a loopback interface, a virtual interface advertisable by OSPF, whereas a loopback address is purely internal): the router uses itself as reference. Displayed stratum 7, the router's actual stratum (`show ntp status`) = **8: the default stratum of `ntp master`**.
- **Symmetric active**: `ntp peer <ip>` between R2 and R3 (both stratum 9 since R1 is stratum 8).
- **NTP authentication** (optional, possibly on the exam): the client checks that the server uses the same password. Same configuration on server and clients:
  1. `ntp authenticate` (enable);
  2. `ntp authentication-key 1 md5 <password>` (create the key);
  3. `ntp trusted-key 1` (declare the key trusted, **don't forget this step**);
  4. clients only: `ntp server <ip> key 1`, optionally `ntp peer <ip> key 1`.

### 5. Exam traps

- Default time zone: **UTC**. NTP only carries UTC; the time zone is configured locally.
- `clock set` and `calendar set`: **privileged exec**, outside the running-config; `clock timezone` and `clock summer-time`: **global config**, in the running-config.
- `clock read-calendar`: the software clock **reads** the calendar; `clock update-calendar`: **updates** the calendar from the clock.
- UDP **123**, max stratum **15**, reference clock **stratum 0**, `ntp master` default **stratum 8** (association shown as 127.127.1.1 stratum 7). `ntp server 127.127.1.1` is **rejected** by the router.
- `ntp server` = **client** mode; `ntp master` = **server** mode; `ntp peer` = **symmetric active**; `ntp client` **is not a valid command**.
- An NTP client automatically becomes a server, stratum +1. Lowest stratum = preferred server.
- Boson ExSim: `ntp server` enables **static client** mode (broadcast client mode is beyond the CCNA).

### 6. IOS commands

```text
Router# show clock                      ! time, time zone (UTC by default)
Router# show clock detail               ! + time source; * = not authoritative
Router# show calendar                   ! hardware clock (missing in Packet Tracer)
Router# show logging                    ! device logs (Syslog preview)
Router# clock set 12:00:00 30 Dec 2020  ! set the software clock
Router# calendar set 12:00:00 30 Dec 2020 ! set the hardware clock
Router# clock update-calendar           ! calendar <- clock
Router# clock read-calendar             ! clock <- calendar
Router(config)# clock timezone JST 9    ! free-form name + offset from UTC
Router(config)# clock summer-time EDT recurring 2 Sunday March 2:00 1 Sunday November 2:00
Router(config)# ntp server 216.239.35.0 [prefer] ! client mode; prefer = preferred server
Router(config)# ntp source loopback0    ! source of NTP messages (required when advertising a loopback)
Router(config)# ntp update-calendar     ! NTP also updates the hardware clock
Router(config)# ntp master [stratum]    ! master clock, stratum 8 by default
Router(config)# ntp peer 10.0.23.3      ! symmetric active mode
Router(config)# ntp authenticate        ! enable authentication
Router(config)# ntp authentication-key 1 md5 jeremysitlab ! create the key
Router(config)# ntp trusted-key 1       ! declare the key trusted
Router(config)# ntp server 10.0.12.1 key 1 ! client: key to use with this server
Router(config)# ntp peer 10.0.23.3 key 1   ! authenticate the peer too
Router# show ntp associations           ! * sys.peer, + candidate, ~ configured, st = stratum
Router# show ntp status                 ! Clock is synchronized, router's stratum, reference
```

### 7. The lab (video #76)

Goal: R1 syncs to SRV1 (1.1.1.1) over the Internet, then R2 and R3 sync to R1 with authentication. In Packet Tracer, `clock summer-time`, `ntp source`, `ntp peer` and `show calendar` **do not exist**.

1. **Manual time** on R1, R2, R3: `clock set 12:00:00 Dec 30 2020` (UTC, no time zone yet); `show clock detail`: source "user configuration". Setting the time close to the NTP server's time **speeds up** synchronization, which can take a long time.
2. **Time zone**: `clock timezone JST 9` on all three routers; `do show clock detail` shows 9 hours ahead.
3. **R1 as client of 1.1.1.1**: `ntp server 1.1.1.1`. `show ntp associations`: the asterisk only appears after **fast-forwarding the simulation** (arrows). SRV1 is stratum 1; `show ntp status`: R1 stratum 2; `show clock detail`: source **NTP**.
4. **R1 as stratum 8 master**: `ntp master` (default = 8), a backup clock for R2 and R3 if R1 loses 1.1.1.1. Authentication on R1: `ntp authenticate`, `ntp authentication-key 1 md5 jeremysitlab`, `ntp trusted-key 1`. On R2: the same three commands then `ntp server 192.168.12.1 key 1`; on R3: same then `ntp server 192.168.13.1 key 1`. Without `ntp source`, R1's physical interface address (G0/1) is used, not a loopback. Verify after fast-forwarding: `show ntp associations` (asterisk), `show clock detail` (source NTP).
5. **Calendar**: `ntp update-calendar` on R2, R3, R1 (no visible effect in Packet Tracer).

Boson NetSim bonus "Configuring NTP 1": `clock set 9:00:00 25 JUL 2013`, `ntp master 3` on Router1, `ntp server 10.0.12.1` on Router2, `ntp server 10.0.23.2` on Router3; `show ntp status`: Router1 stratum 3 (reference = loopback address), Router2 stratum 4, Router3 stratum 5; the reference address differs on each router because each syncs to a different clock.

### 8. The quiz (5 questions + 1 Boson)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which command causes the router to adjust its software clock to match the hardware clock? | **`clock read-calendar`** (C) | D, `clock update-calendar`, does the opposite (calendar ← clock). A and B are not valid commands. |
| Which command configures the device's time zone? | **`clock timezone <name> <offset>`** from global config (D) | Unlike some other time commands, this one is in global config, not privileged exec. `clock set` cannot set the time zone. |
| Given the output (association 127.127.1.1, stratum 8), which command was configured on R1? | **`ntp master 9`** (A) | The loopback address 127.127.1.1 means `ntp master`. With the default stratum (8, options C and D) the association would show stratum 7; here it is 8, so `ntp master 9`. B, `ntp server 127.127.1.1`, is rejected by the router. |
| Which command configures the router in NTP client mode? | **`ntp server 216.239.35.0`** (C) | A, `ntp peer`, = symmetric active; B, `ntp master`, = server mode; D, `ntp client`, is not valid. |
| Which commands must be configured on an NTP client to enable authentication? (select all that apply) | **C `ntp authenticate`, D `ntp authentication-key`, F `ntp trusted-key`, G `ntp server ... key`** | C enables authentication, D creates the key, F marks it trusted, G specifies the key to use with the server. (On the real exam, the question always says how many to select.) |
| Boson: what is enabled by `ntp server` in global config? | **Static client mode** (A) | You tell the router which server to sync to: it becomes a client. Not symmetric active (B), not broadcast client (C, beyond the CCNA), not server mode (D), not authentication (E). |
