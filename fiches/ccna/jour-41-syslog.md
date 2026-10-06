# CCNA Day 41 : Syslog

> Source : Jeremy's IT Lab, « Free CCNA | Syslog | Day 41 » (28 min, vidéo n°83 de la playlist, cours) et « Free CCNA | Syslog | Day 41 Lab » (14 min, vidéo n°84, lab Packet Tracer). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Vue d'ensemble

- Sujet d'examen **4.5** : décrire l'utilisation des fonctions Syslog, notamment les **facilities** et les **levels**.
- **Syslog** est un protocole standard de l'industrie pour la **journalisation des messages** (*message logging*) : changements d'état d'interface, de voisinage OSPF (ou EIGRP, BGP), redémarrages système, etc.
- Les messages peuvent être **affichés en temps réel dans le CLI**, **enregistrés en RAM** sur l'équipement, ou **envoyés à un serveur Syslog externe**. Exemple : `no shutdown` sur une interface affiche deux messages Syslog (état passé à UP).
- Essentiels pour le dépannage et l'analyse des incidents. Syslog et SNMP sont **complémentaires** mais différents (comparaison en fin de fiche).

### 2. Format d'un message Syslog

Champs, dans l'ordre : **sequence number** (ordre des messages) ; **timestamp** (heure de génération, très important pour comparer les logs de plusieurs équipements, d'où NTP) ; **facility** (le **processus** qui a généré le message, ex. OSPF) ; **severity** (gravité, **8 niveaux**) ; **mnemonic** (code court indiquant ce qui s'est passé, ex. adjacence OSPF, interface up/down) ; **description** (détail de l'événement).

Le **numéro de séquence et le timestamp** peuvent être affichés ou non selon la configuration. Les numéros de séquence sont souvent inutilisés ; les timestamps sont fortement recommandés.

### 3. Les niveaux de gravité (à mémoriser tous)

| Niveau | Mot-clé | Description (RFC) |
| :--- | :--- | :--- |
| **0** | **Emergency** | Système inutilisable |
| **1** | **Alert** | Action à prendre immédiatement |
| **2** | **Critical** | Conditions critiques |
| **3** | **Error** | Conditions d'erreur |
| **4** | **Warning** | Conditions d'avertissement |
| **5** | **Notice** (RFC) / **Notification** (Cisco IOS) | Condition normale mais significative |
| **6** | **Informational** | Messages d'information |
| **7** | **Debugging** | Messages de débogage |

- **0 = le plus grave, 7 = le moins grave.** Connaître les deux noms du niveau 5 : **Notice** et **Notification**.
- La RFC ne définit pas précisément quels événements vont dans quel niveau : chaque constructeur interprète (RFC 5424 : « severities are very subjective » ; le Warning d'un Cisco n'est pas forcément celui d'un Juniper).
- Mnémonique : **Every Awesome Cisco Engineer Will Need Ice cream Daily.**

### 4. Exemples de messages

- `*Jan 1 00:00:00.000: %LINK-3-UPDOWN: Interface GigabitEthernet0/0, changed state to up` : timestamp (mois, jour, h, min, s, ms), pas de numéro de séquence ; facility **LINK**, severity **3** (error), mnemonic **UPDOWN**, puis la description. Savoir répondre « facility ? » → LINK, « severity ? » → 3 ou error.
- `%OSPF-5-ADJCHG` : facility OSPF, niveau 5 (notification), mnemonic ADJCHG (*adjacency change*), voisin passé FULL.
- `000123: ... %SYS-5-CONFIG_I: Configured from console by jeremy on console` : avec numéro de séquence ; facility SYS, niveau 5, affiché quand on quitte le mode de configuration globale.
- `%SYS-6-CLOCKUPDATE` : facility SYS, niveau 6 (informational), après un changement de fuseau horaire.

### 5. Destinations des messages

| Destination | Défaut | Commande |
| :--- | :--- | :--- |
| **Console line** (connexion par le port console ; dans Packet Tracer l'onglet CLI est une connexion console) | **Activée, tous les niveaux 0 à 7** | `logging console <niveau>` |
| **VTY lines** (connexion Telnet ou SSH) | **Désactivée** | `logging monitor <niveau>` + `terminal monitor` à chaque session |
| **Buffer** (RAM de l'équipement, lecture avec `show logging`) | **Activé, niveaux 0 à 7** | `logging buffered [taille-octets] <niveau>` |
| **Serveur Syslog externe** (gestion centralisée, comparaison des logs) | Désactivé | `logging <ip>` ou `logging host <ip>` + `logging trap <niveau>` |

- **Les serveurs Syslog écoutent sur UDP port 514.** À retenir.
- Dans toutes ces commandes, le niveau se donne **par numéro ou par mot-clé** (`6` ou `informational`), et il active les messages **de ce niveau et plus graves** : `logging console 6` = niveaux 6, 5, 4, 3, 2, 1, 0 (restreint légèrement par rapport au défaut qui inclut 7). `logging trap debugging` = tous les niveaux.
- Taille du buffer : optionnelle (défaut sinon) ; ne pas la mettre trop grande, cela prend de la mémoire aux autres opérations.
- **`terminal monitor`** (mode privilégié) : obligatoire pour voir les messages en Telnet/SSH même avec `logging monitor`, et **à refaire à chaque nouvelle session** (la commande cesse d'agir à la déconnexion).
- **`logging synchronous`** (sur la ligne, ex. `line console 0`) : si un message interrompt la saisie d'une commande, la commande est **réaffichée sur une nouvelle ligne** ; pratique, Jeremy l'utilise en lab. La configuration des lignes sera détaillée dans la vidéo Telnet/SSH.
- **`service timestamps log datetime`** (date et heure réelles, option préférée) ou **`uptime`** (durée de fonctionnement au moment de l'événement) ; **`service sequence-numbers`** active les numéros de séquence (Jeremy les laisse désactivés).

### 6. Syslog et SNMP

- **Syslog** : journalisation de messages ; les événements sont classés par **facility et severity** et enregistrés sur l'équipement et probablement sur un serveur externe ; gestion, analyse, dépannage. **Les messages vont des équipements vers le serveur ; le serveur ne peut pas interroger** (pas d'équivalent de Get) **ni modifier** (pas d'équivalent de Set).
- **SNMP** : récupère et organise des informations sur les équipements gérés (adresses IP, état des interfaces, température, CPU) sous forme de **variables dans la MIB** ; le serveur utilise **Get** pour interroger et **Set** pour modifier.
- Utilisés ensemble pour la gestion des équipements ; connaître les deux.

### 7. Pièges d'examen

- Les **8 niveaux** avec numéros et mots-clés (niveau 1 = Alert, 6 = Informational, 3 = Error, 5 = Notice/Notification...).
- Identifier chaque partie d'un message `%FACILITY-SEVERITY-MNEMONIC: description`.
- Par défaut : messages vers **console** et **buffer** ; **pas** vers les VTY (Telnet/SSH) ni vers un serveur externe.
- `logging buffered 6` = niveaux **0 à 6** (ce niveau et les plus graves, numériquement inférieurs).
- Champs facultatifs : **sequence** et **timestamp** (`service sequence-numbers`, `service timestamps`).
- **UDP 514** pour le serveur Syslog.
- Niveau « warning ou plus » = **plus grave**, donc **numéro plus bas**, pas plus haut (bonus NetSim).

### 8. Commandes IOS

```text
R1(config)# logging console 6                   ! console : niveau 6 et plus graves (défaut : tous)
R1(config)# logging monitor informational        ! VTY (Telnet/SSH) : niveau par numéro ou mot-clé
R1# terminal monitor                             ! afficher les logs dans la session Telnet/SSH courante
R1(config)# logging buffered 8192 6              ! buffer RAM, taille optionnelle en octets, niveau
R1(config)# logging 192.168.1.100                ! serveur Syslog externe (= logging host <ip>)
R1(config)# logging trap debugging               ! niveau des messages envoyés au serveur
R1(config)# line console 0
R1(config-line)# logging synchronous             ! réaffiche la commande interrompue par un log
R1(config)# service timestamps log datetime [msec] ! timestamps date/heure (ou uptime) ; msec obligatoire dans Packet Tracer
R1(config)# service sequence-numbers             ! numéros de séquence
R1# show logging                                 ! paramètres de logging + messages du buffer
```

### 9. Le lab (vidéo n°84)

Objectif : observer les logs via la console, les VTY, le buffer et un serveur Syslog externe (SRV1 192.168.1.100). Syslog est mieux supporté que SNMP dans Packet Tracer.

1. **Console depuis PC2** : Desktop → Terminal (réglages par défaut) ; login jeremy / ccna, `enable` (ccna). `interface g0/0`, `shutdown` : **deux** messages, car `show ip interface brief` a deux colonnes : **Status** (administratively down) et **Protocol** (down). `no shutdown`. Tous ces messages sont de niveau **5** (notice/notification). Sans timestamps : `service timestamps log datetime msec` (**`msec` obligatoire dans Packet Tracer**, optionnel en vrai IOS). En sortant de config, le message porte un timestamp (heure non réglée).
2. **Telnet depuis PC1** : `telnet 192.168.1.1` (Telnet pré-configuré sur R1, vu dans une vidéo ultérieure). `interface g0/1`, `no shutdown` : **aucun message** (VTY désactivé par défaut). `logging monitor` n'existe pas dans Packet Tracer ; `do terminal monitor` active l'affichage pour la session, puis `shutdown` affiche un message. En vrai IOS, il faut refaire `terminal monitor` à chaque session ; Packet Tracer ne simule pas ce point exactement.
3. **Buffer** : `do show logging` montre « buffer logging disabled » (désactivé par défaut sur ce routeur Packet Tracer) ; `logging buffered 8192` (pas d'option de niveau dans Packet Tracer) ; `do show logging` : niveau par défaut **debugging** ; « trap logging: level informational » = niveau par défaut envoyé à un serveur.
4. **Serveur Syslog** : `logging 192.168.1.100` (ou `logging host`), `logging trap debugging` (seule option dans Packet Tracer). Générer des messages (`interface g0/1`, `no shutdown`, `shutdown`, `end`), puis sur SRV1 : Services → **Syslog** : les messages reçus de R1.

Bonus Boson NetSim (lab ENCOR « System message logging ») : `ping 10.1.0.10`, `logging 10.1.0.10`, `show logging` (trap level informational = 0 à 6 ; **8 niveaux** disponibles ; niveau 7 configuré = beaucoup plus de messages que niveau 1, qui n'inclut que alerts et emergencies), `logging trap warnings`, vérification `show logging` « trap logging level warnings » ; idem sur Switch1 et Switch2 (adresse sur VLAN99) ; grade lab réussi.

### 10. Le quiz (5 questions + 1 Boson)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Niveau de gravité du message affiché (… -5- …) ? | **Notification** (C) | Le 5 entre facility et mnemonic ; appelé Notice dans la RFC, Notification dans Cisco IOS. |
| Niveau de gravité du message affiché (… -3- …) ? | **Error** (B) | Nom du niveau 3. Connaître tous les niveaux et leurs noms. |
| Vers quelles destinations les messages Syslog sont-ils envoyés par défaut ? (deux) | **Console line** (B) et **buffer** (C) | Pas de serveur externe sans configuration ; pas d'affichage sur les VTY (Telnet/SSH) par défaut. |
| `logging buffered 6` sur R1 : quels niveaux sont sauvés dans le buffer ? | **Gravité 0 à 6** (C) | Un niveau donné inclut ce niveau et les plus graves (numéros plus bas). |
| Quels champs peuvent ne pas être affichés selon la configuration ? (deux) | **Sequence** (A) et **timestamp** (D) | Contrôlés par `service timestamps` et `service sequence-numbers`. |
| Boson (glisser-déposer) : associer les mots-clés aux niveaux | **0 emergencies, 1 alerts, 2 critical, 3 errors, 4 warnings, 5 notifications, 6 informational, 7 debugging** | Mnémonique « Every Awesome Cisco Engineer Will Need Ice cream Daily ». |

---

## 🇬🇧 English version

### 1. Overview

- Exam topic **4.5**: describe the use of syslog features including **facilities** and **levels**.
- **Syslog** is an industry-standard protocol for **message logging**: interface status changes, OSPF (or EIGRP, BGP) neighbor changes, system restarts, etc.
- Messages can be **displayed in real time in the CLI**, **saved in the device's RAM**, or **sent to an external Syslog server**. Example: `no shutdown` on an interface displays two Syslog messages (state changed to UP).
- Essential for troubleshooting and incident analysis. Syslog and SNMP are **complementary** but different (comparison at the end).

### 2. Syslog message format

Fields, in order: **sequence number** (order of messages); **timestamp** (when generated; very important to compare logs across devices, hence NTP); **facility** (the **process** that generated the message, e.g. OSPF); **severity** (**8 levels**); **mnemonic** (short code for what happened, e.g. OSPF adjacency, interface up/down); **description** (details of the event).

The **sequence number and timestamp** may or may not be displayed, depending on configuration. Sequence numbers are often unused; timestamps are highly recommended.

### 3. Severity levels (memorize them all)

| Level | Keyword | Description (RFC) |
| :--- | :--- | :--- |
| **0** | **Emergency** | System is unusable |
| **1** | **Alert** | Action must be taken immediately |
| **2** | **Critical** | Critical conditions |
| **3** | **Error** | Error conditions |
| **4** | **Warning** | Warning conditions |
| **5** | **Notice** (RFC) / **Notification** (Cisco IOS) | Normal but significant condition |
| **6** | **Informational** | Informational messages |
| **7** | **Debugging** | Debug-level messages |

- **0 = most severe, 7 = least severe.** Know both names for level 5: **Notice** and **Notification**.
- The RFC doesn't define exactly which events fit each level: each vendor interprets them (RFC 5424: "severities are very subjective"; a Cisco Warning isn't necessarily a Juniper Warning).
- Mnemonic: **Every Awesome Cisco Engineer Will Need Ice cream Daily.**

### 4. Message examples

- `*Jan 1 00:00:00.000: %LINK-3-UPDOWN: Interface GigabitEthernet0/0, changed state to up`: timestamp (month, date, h, min, s, ms), no sequence number; facility **LINK**, severity **3** (error), mnemonic **UPDOWN**, then the description. Be able to answer "facility?" → LINK, "severity?" → 3 or error.
- `%OSPF-5-ADJCHG`: facility OSPF, level 5 (notification), mnemonic ADJCHG (adjacency change), neighbor moved to FULL.
- `000123: ... %SYS-5-CONFIG_I: Configured from console by jeremy on console`: with sequence number; facility SYS, level 5, displayed when leaving global config mode.
- `%SYS-6-CLOCKUPDATE`: facility SYS, level 6 (informational), after changing the time zone.

### 5. Message destinations

| Destination | Default | Command |
| :--- | :--- | :--- |
| **Console line** (console port connection; in Packet Tracer the CLI tab acts as a console connection) | **Enabled, all levels 0 to 7** | `logging console <level>` |
| **VTY lines** (Telnet or SSH connection) | **Disabled** | `logging monitor <level>` + `terminal monitor` every session |
| **Buffer** (device RAM, viewed with `show logging`) | **Enabled, levels 0 to 7** | `logging buffered [size-bytes] <level>` |
| **External Syslog server** (central management, easier log comparison) | Disabled | `logging <ip>` or `logging host <ip>` + `logging trap <level>` |

- **Syslog servers listen on UDP port 514.** Remember that.
- In all these commands the level can be given **as a number or keyword** (`6` or `informational`), and it enables messages **of that level and more severe**: `logging console 6` = levels 6, 5, 4, 3, 2, 1, 0 (slightly restricts the default, which includes 7). `logging trap debugging` = all levels.
- Buffer size: optional (default otherwise); don't set it too large, it takes memory from other operations.
- **`terminal monitor`** (privileged exec): required to see messages over Telnet/SSH even with `logging monitor`, and **must be repeated every new session** (it stops applying when you log out).
- **`logging synchronous`** (on the line, e.g. `line console 0`): if a message interrupts your typing, the command is **reprinted on a new line**; convenient, Jeremy uses it in labs. Line configuration is detailed in the Telnet/SSH video.
- **`service timestamps log datetime`** (actual date and time, preferred) or **`uptime`** (how long the device had been running); **`service sequence-numbers`** enables sequence numbers (Jeremy keeps them off).

### 6. Syslog vs SNMP

- **Syslog**: message logging; events are categorized by **facility and severity** and logged on the device and likely to an external server; system management, analysis, troubleshooting. **Messages go from devices to the server; the server cannot actively pull** (no Get equivalent) **nor modify** (no Set equivalent).
- **SNMP**: retrieves and organizes information about managed devices (IP addresses, interface status, temperature, CPU) as **variables in the MIB**; servers use **Get** to query and **Set** to modify.
- Used together for device management; know both.

### 7. Exam traps

- The **8 levels** with numbers and keywords (level 1 = Alert, 6 = Informational, 3 = Error, 5 = Notice/Notification...).
- Identify each part of `%FACILITY-SEVERITY-MNEMONIC: description`.
- Defaults: messages to **console** and **buffer**; **not** to VTY (Telnet/SSH) nor to an external server.
- `logging buffered 6` = levels **0 to 6** (that level and more severe, numerically lower).
- Optional fields: **sequence** and **timestamp** (`service sequence-numbers`, `service timestamps`).
- **UDP 514** for the Syslog server.
- "Warning or higher" = **more severe**, hence **lower number**, not higher (NetSim bonus).

### 8. IOS commands

```text
R1(config)# logging console 6                   ! console: level 6 and more severe (default: all)
R1(config)# logging monitor informational        ! VTY (Telnet/SSH): level by number or keyword
R1# terminal monitor                             ! show logs in the current Telnet/SSH session
R1(config)# logging buffered 8192 6              ! RAM buffer, optional size in bytes, level
R1(config)# logging 192.168.1.100                ! external Syslog server (= logging host <ip>)
R1(config)# logging trap debugging               ! level of messages sent to the server
R1(config)# line console 0
R1(config-line)# logging synchronous             ! reprint the command interrupted by a log
R1(config)# service timestamps log datetime [msec] ! date/time timestamps (or uptime); msec required in Packet Tracer
R1(config)# service sequence-numbers             ! sequence numbers
R1# show logging                                 ! logging settings + buffer messages
```

### 9. The lab (video #84)

Goal: observe logs via the console, VTY lines, buffer and an external Syslog server (SRV1 192.168.1.100). Syslog is better supported than SNMP in Packet Tracer.

1. **Console from PC2**: Desktop → Terminal (default settings); login jeremy / ccna, `enable` (ccna). `interface g0/0`, `shutdown`: **two** messages, because `show ip interface brief` has two columns: **Status** (administratively down) and **Protocol** (down). `no shutdown`. All these messages are level **5** (notice/notification). No timestamps: `service timestamps log datetime msec` (**`msec` is required in Packet Tracer**, optional in real IOS). On leaving config mode, the message carries a timestamp (time not set).
2. **Telnet from PC1**: `telnet 192.168.1.1` (Telnet pre-configured on R1, covered in a later video). `interface g0/1`, `no shutdown`: **no message** (VTY disabled by default). `logging monitor` doesn't exist in Packet Tracer; `do terminal monitor` enables display for the session, then `shutdown` shows a message. In real IOS, `terminal monitor` must be repeated each session; Packet Tracer doesn't simulate this exactly.
3. **Buffer**: `do show logging` shows "buffer logging disabled" (off by default on this Packet Tracer router); `logging buffered 8192` (no level option in Packet Tracer); `do show logging`: default level **debugging**; "trap logging: level informational" = default level sent to a server.
4. **Syslog server**: `logging 192.168.1.100` (or `logging host`), `logging trap debugging` (only option in Packet Tracer). Generate messages (`interface g0/1`, `no shutdown`, `shutdown`, `end`), then on SRV1: Services → **Syslog**: the messages received from R1.

Boson NetSim bonus (ENCOR lab "System message logging"): `ping 10.1.0.10`, `logging 10.1.0.10`, `show logging` (trap level informational = 0 to 6; **8 levels** available; level 7 configured = far more messages than level 1, which only includes alerts and emergencies), `logging trap warnings`, verify `show logging` "trap logging level warnings"; same on Switch1 and Switch2 (address on VLAN99); lab graded correct.

### 10. The quiz (5 questions + 1 Boson)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Severity level of the message shown (… -5- …)? | **Notification** (C) | The 5 between facility and mnemonic; called Notice in the RFC, Notification in Cisco IOS. |
| Severity level of the message shown (… -3- …)? | **Error** (B) | Name of level 3. Know all levels and their names. |
| Which locations receive Syslog messages by default, without configuration? (select two) | **Console line** (B) and **buffer** (C) | No external server without configuration; no display on VTY lines (Telnet/SSH) by default. |
| `logging buffered 6` on R1: which severity levels are saved to the buffer? | **Severity 0 to 6** (C) | A given level includes that level and more severe (lower numbers). |
| Which fields might not be displayed depending on configuration? (select two) | **Sequence** (A) and **timestamp** (D) | Controlled by `service timestamps` and `service sequence-numbers`. |
| Boson (drag and drop): match keywords to levels | **0 emergencies, 1 alerts, 2 critical, 3 errors, 4 warnings, 5 notifications, 6 informational, 7 debugging** | Mnemonic "Every Awesome Cisco Engineer Will Need Ice cream Daily". |
