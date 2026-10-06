# CCNA Day 9 : Switch Interfaces / Interfaces de switch

> Source : Jeremy's IT Lab, « Free CCNA | Switch Interfaces | Day 9 » (32 min), vidéo n°16 de la playlist (cours), et « Configuring Interfaces | Day 9 Lab » (12 min), vidéo n°17 (lab Packet Tracer). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Programme et rappel sur les switches

- Au programme : **vitesse** (*speed*, débit en bits par seconde : 10, 100 ou 1000 Mbps) et **duplex** (capacité à envoyer **et** recevoir en même temps), l'**autonégociation** (*autonegotiation*) de ces deux réglages, l'**état des interfaces** (*interface status*) et les **compteurs d'erreurs** (*interface counters and errors*).
- Rappel du Day 1 en photo : un routeur Cisco ASR 1000-X a 8 interfaces SFP (fibre) et quelques RJ45 (console…) ; un switch Catalyst 9200 a 4 SFP et **48 RJ45** : le switch sert à connecter les hôtes finaux (48 PC), puis il remonte vers un routeur par la fibre.
- Topologie du cours : un seul LAN 192.168.1.0/24, R1, SW1, SW2, PC1 à PC4. On configure **SW1** : F0/1 à F0/4 connectées, le reste non connecté.

### 2. `show ip interface brief` sur un switch

- Les quatre interfaces connectées sont **up/up** (Status = couche 1, Protocol = couche 2) **sans aucune configuration** : contrairement aux routeurs, les interfaces de switch **n'ont pas `shutdown` par défaut**.
- *IP-Address* reste *unassigned* : ce sont des **ports de couche 2** (*Layer 2 switchports*), ils n'ont pas besoin d'adresse IP (le *multilayer switching* viendra plus tard). Ignorer aussi l'interface virtuelle *VLAN1*.
- Les interfaces non connectées sont **down/down**, ce qui est **différent de administratively down/down** : down/down signifie « pas connecté à un autre équipement », pas « désactivé ».
- Résumé : routeur → administratively down/down par défaut ; switch → up/up si connecté, down/down sinon.

### 3. `show interfaces status` (switch seulement)

| Colonne | Contenu |
| :--- | :--- |
| Port | l'interface |
| Name | la **description** de l'interface (nom trompeur) |
| Status | **connected**, **notconnect**, puis **disabled** après `shutdown` (= administratively down dans `show ip interface brief`, même chose) ; d'autres états viendront |
| Vlan | **1 par défaut** ; F0/2 vers SW2 affiche **trunk** (expliqué dans la vidéo VLAN) |
| Duplex | **auto** par défaut ; **a-full** = full négocié automatiquement (le *a* = auto) |
| Speed | **auto** par défaut ; **a-100** = 100 Mbps négociés. FastEthernet = 10 ou 100 Mbps |
| Type | **10/100BASE-TX** : RJ45 cuivre UTP ; un module SFP apparaîtrait ici |

### 4. Configurer vitesse, duplex, description, et désactiver les ports inutilisés

- Sur F0/1 (vers R1, interface FastEthernet elle aussi) : `speed ?` propose **10, 100, auto** → `speed 100` ; `duplex ?` propose **auto, full, half** → `duplex full` ; puis une `description`. Dans `show interfaces status`, duplex et speed passent à **full** et **100** (sans le *a*) : ils ne sont plus négociés.
- En général on **laisse l'autonégociation** ; il faut savoir configurer à la main en cas de problème.
- Des ports actifs par défaut sont pratiques mais posent un **problème de sécurité** : il faut **désactiver les interfaces inutilisées**.
- **`interface range f0/5 - 12`** : mode `(config-if-range)#`, une description puis `shutdown` pour toutes à la fois (messages *administratively down*). Plages non consécutives : `interface range f0/5 - 6, f0/9 - 12` ; un `no shutdown` n'y réactive que ces six ports, F0/7 et F0/8 restent down. Ensuite `show interfaces status` montre **disabled**.

### 5. Half duplex, full duplex, hub et CSMA/CD

- **Half duplex** : l'équipement **ne peut pas** envoyer et recevoir en même temps ; s'il reçoit une trame, il attend avant d'envoyer. **Full duplex** : il peut faire les deux à la fois. Dans les réseaux modernes à switches, **tout le monde est en full duplex** ; le half duplex ne s'emploie quasiment plus.
- Le **hub** (concentrateur), ancêtre du switch, est un simple **répéteur de couche 1** : toute trame reçue est répétée sur toutes les autres interfaces (comme un switch avec un broadcast ou un *unknown unicast*). Si PC1 et PC3 émettent en même temps, le hub répète les deux à la fois : **collision**, PC2 ne reçoit aucune trame intacte. Tous les équipements d'un hub forment un **domaine de collision** (*collision domain*).
- **CSMA/CD** (*Carrier Sense Multiple Access with Collision Detection*) : avant d'émettre, écouter le domaine jusqu'à ce que personne n'émette ; si une collision survient quand même, envoyer un **signal de brouillage** (*jamming signal*), puis chacun attend un **délai aléatoire** avant de réessayer.
- Un switch opère en couche 2 avec les MAC, n'envoie jamais deux trames à la fois au même hôte : avec trois PC, on passe d'un domaine de collision à **trois**. Les collisions deviennent rares et sont **signe d'un problème** (mauvaise configuration).
- Les équipements sur un hub doivent être en half duplex ; ceux sur un switch peuvent être en full duplex.

### 6. Autonégociation de la vitesse et du duplex (routeurs et switches)

- Les interfaces multi-vitesses (10/100 ou 10/100/1000) ont par défaut **speed auto** et **duplex auto** : elles annoncent leurs capacités et conviennent du meilleur réglage commun. Exemple : un PC Ethernet (10), un PC FastEthernet (10/100) et un PC Gigabit (10/100/1000) sur G0/1, G0/2, G0/3 négocient 10, 100 et 1000 Mbps, tous en full duplex.
- **Si l'autonégociation est désactivée en face** : le switch essaie de **détecter la vitesse** (*sense*) ; s'il échoue, il prend la **plus lente supportée** (10 Mbps sur un port 10/100/1000). Pour le duplex, il ne peut rien détecter : **half duplex si 10 ou 100 Mbps, full duplex si 1000 Mbps ou plus**.
- Exemple : PC à 10 Mbps → 10/half ; PC à 1000 → 1000/full ; PC à 100 full fixé à la main → le switch prend 100/**half** : **duplex mismatch**, collisions, mauvaises performances. Conclusion : utiliser l'autonégociation partout.

### 7. Compteurs d'erreurs dans `show interfaces` (switch ou routeur)

En bas de la sortie : total de **paquets et octets reçus**, puis :

- **runts** : trames plus petites que le minimum Ethernet de **64 octets** ;
- **giants** : trames plus grandes que le maximum de **1518 octets** ;
- **CRC** : trames ayant échoué au contrôle CRC (*cyclic redundancy check*, via le FCS du trailer Ethernet) ;
- **frame** : trames au format incorrect ou illégal ;
- **input errors** : total de plusieurs compteurs dont les quatre précédents ;
- **output errors** : trames que le switch a tenté d'envoyer sans y parvenir.

### Pièges d'examen

- **Routeur** : interfaces `shutdown` par défaut (administratively down/down). **Switch** : jamais `shutdown` par défaut (up/up ou down/down). Down/down ≠ administratively down.
- Dans `show interfaces status`, **disabled** et, dans `show ip interface brief`, **administratively down** désignent le même état.
- **Duplex mismatch** → collisions (et non un ajustement automatique) : sans autonégociation, le voisin ne peut pas deviner le duplex.
- Règle sans autonégociation en face : vitesse détectée (sinon la plus lente), **half si 10/100, full si 1000+**.
- **CSMA/CD** = half duplex et collisions ; CSMA/**CA** est autre chose (vu plus tard).
- Les compteurs d'erreurs sont dans **`show interfaces`** ; `show interfaces errors` n'existe pas ; les broadcasts ne sont pas des erreurs.
- Runt < 64 octets, giant > 1518 octets.

### Commandes IOS

```text
SW1# show ip interface brief                  ! Status/Protocol : up/up, down/down (switch) ou administratively down (routeur)
SW1# show interfaces status                   ! switch seulement : Port, Name, Status, Vlan, Duplex, Speed, Type
SW1# show interfaces f0/1                     ! détail d'une interface + compteurs (runts, giants, CRC, frame, input/output errors)
SW1(config)# interface f0/1                   ! mode interface
SW1(config-if)# speed 100                     ! 10 | 100 | auto (défaut auto) ; 1000 sur un port gigabit
SW1(config-if)# duplex full                   ! auto (défaut) | full | half
SW1(config-if)# description ## to R1 ##       ! apparaît dans la colonne Name de show interfaces status
SW1(config)# interface range f0/5 - 12        ! plusieurs interfaces à la fois, mode (config-if-range)#
SW1(config)# interface range f0/5 - 6, f0/9 - 12   ! plages non consécutives séparées par une virgule
SW1(config-if-range)# shutdown                ! désactive les ports inutilisés (sécurité) ; no shutdown réactive
R1(config-if)# do show running-config         ! vérifier speed, duplex, adresses, descriptions
R1# copy running-config startup-config        ! sauvegarder ; équivalents : write memory, write
R1# show startup-config                       ! vérifier la configuration sauvegardée
```

### Le lab (vidéo n°17)

**Objectif** : un seul LAN **172.16.0.0/16** relié à R1 G0/0 ; configurer R1, SW1, SW2 et quatre PC. Six étapes : hostnames, adresses IP, vitesse et duplex, descriptions, désactivation des interfaces inutilisées, sauvegarde. Jeremy procède équipement par équipement.

**R1** : `enable`, `configure terminal`, `hostname R1`. `interface g0/0`, puis `do show ip interface brief` (unassigned, unset, administratively down). `ip address 172.16.255.254 255.255.0.0` ; comme l'interface est reliée à un équipement réseau (SW1), vitesse et duplex à la main : `speed 1000` (interface gigabit), `duplex full` ; `description ## to SW1 ##` ; `no shutdown` (les interfaces de routeur étant shutdown par défaut, les ports inutilisés n'ont rien à faire, c'est l'inverse qu'il faut faire ici). Vérification : up/**down** dans Packet Tracer parce que le côté SW1 n'est pas encore configuré en manuel ; sur un vrai équipement ce serait up/up, c'est une limite du simulateur. `interface range g0/1 - 2`, `description ## not in use ##`. `do show run`, `end`, sauvegarde avec `copy running-config startup-config` (Entrée pour confirmer), contrôle avec `show startup-config`.

**PC1 à PC4** (*Config*, passerelle pré-configurée = R1) : *FastEthernet0*, adresses **172.16.0.1** à **172.16.0.4** ; la touche **Tab** remplit le masque 255.255.0.0.

**SW1** : `enable`, `conf t`, `hostname SW1`, `do show interfaces status` (commande qui marche sur switch, pas sur routeur ; tout par défaut, statuts connected ou notconnect, jamais disabled). `interface g0/1` : `speed 1000`, `duplex full`, `description ## to R1 ##`. `interface g0/2` : idem, `description ## to SW2 ##`. `interface range f0/1 - 2` (hôtes finaux : pas de vitesse/duplex selon les consignes) : `description ## to end hosts ##`. `interface range f0/3 - 24` (22 ports inutilisés) : `description ## not in use ##`, `shutdown`. `do show interfaces status` : ports disabled ; G0/2 encore down tant que SW2 n'est pas configuré. Autre limite de Packet Tracer : il affiche **a-1000 / a-full** alors qu'un vrai équipement afficherait **1000 / full** (réglages manuels). `end`, `write memory`, `show startup-config`.

**SW2** : `hostname SW2`, `interface g0/1` : `speed 1000`, `duplex full`, `description ## to SW1 ##` ; `interface range f0/1 - 2`, `description ## to end hosts ##` ; `interface range g0/2, f0/3 - 24`, `description ## not in use ##`, `shutdown`. `do show interfaces status`, `end`, sauvegarde avec `write`, `show startup-config`.

### Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| 1. Duplex mismatch entre SW1 F0/1 et SW2 F0/1, autonégociation désactivée : résultat ? A performances améliorées ; B collisions ; C SW1 détecte le duplex de SW2 et s'adapte | **B, collisions** | Le côté half ne peut pas émettre et recevoir en même temps, le côté full l'ignore et émet quand même. Les performances seront bien pires (A faux). Sans autonégociation, SW1 ne peut pas détecter le duplex (C faux). |
| 2. Mécanisme des interfaces half duplex pour détecter et éviter les collisions ? A CSMA/CD ; B CSMA/CA ; C autonégociation ; D duplex auto | **A, CSMA/CD** | Carrier sense multiple access with collision detection : écouter avant d'émettre, réagir aux collisions. CSMA/CA (collision avoidance) est un concept voisin vu plus tard ; C et D n'ont rien à voir. |
| 3. Commande qui affiche les compteurs d'erreurs d'une interface ? A show interfaces ; B show ip interface brief ; C show interfaces status ; D show interfaces errors | **A, show interfaces** | B ne montre aucun compteur (IP, shutdown…) ; C donne description, status, duplex, speed sans compteurs ; D n'existe pas (message d'erreur). Préciser l'interface (`show interfaces f0/1`), les compteurs sont en bas. |
| 4. Exemples d'erreurs sur une interface ? A runts, giants, broadcasts ; B shorts, longs, oversizes ; C packets, bytes, inputs, outputs ; D runts, giants, CRC | **D, runts, giants, CRC** | B et C ne sont pas de vraies erreurs. Dans A, runts et giants sont des erreurs mais les broadcasts font partie du fonctionnement normal. Runts = trop petites, giants = trop grandes, CRC = échec du contrôle FCS. |
| 5. SW1 autonégocie, SW2 a l'autonégociation désactivée avec 100 Mbps full : réglages de SW1 ? A 100/full ; B 100/half ; C 10/full ; D 10/half | **B, 100 Mbps, half** | SW1 détecte la vitesse (100) mais ne peut pas détecter le duplex : règle « 10 ou 100 → half, sinon full ». Résultat : duplex mismatch et collisions. |

---

## 🇬🇧 English version

### 1. Agenda and switch review

- Topics: **speed** (data rate in bits per second: 10, 100 or 1000 Mbps) and **duplex** (whether a device can send **and** receive at the same time), **autonegotiation** of both, **interface status**, and **interface counters and errors**.
- Day 1 reminder with photos: a Cisco ASR 1000-X router has 8 SFP (fiber) interfaces and a few RJ45 ports (console etc.); a Catalyst 9200 switch has 4 SFP plus **48 RJ45** ports: switches connect end hosts (48 PCs) and uplink to a router over fiber.
- Topology: one LAN 192.168.1.0/24, R1, SW1, SW2, PC1 to PC4. We configure **SW1**: F0/1 to F0/4 connected, the rest not connected.

### 2. `show ip interface brief` on a switch

- The four connected interfaces are **up/up** (Status = Layer 1, Protocol = Layer 2) **with no configuration at all**: unlike routers, switch interfaces **do not have `shutdown` applied by default**.
- *IP-Address* stays *unassigned*: these are **Layer 2 switchports**, they do not need an IP address (multilayer switching comes later). Ignore the *VLAN1* virtual interface too.
- Unconnected interfaces are **down/down**, which is **different from administratively down/down**: down/down means "not connected to another device", not "shut down".
- Summary: router → administratively down/down by default; switch → up/up if connected, down/down if not.

### 3. `show interfaces status` (switches only)

| Column | Content |
| :--- | :--- |
| Port | the interface |
| Name | the interface **description** (misleading name) |
| Status | **connected**, **notconnect**, then **disabled** after `shutdown` (= administratively down in `show ip interface brief`, same thing); other statuses come later |
| Vlan | **1 by default**; F0/2 to SW2 shows **trunk** (explained in the VLAN video) |
| Duplex | **auto** by default; **a-full** = full duplex autonegotiated (the *a* = auto) |
| Speed | **auto** by default; **a-100** = 100 Mbps autonegotiated. FastEthernet = 10 or 100 Mbps |
| Type | **10/100BASE-TX**: RJ45 copper UTP; an SFP module would show here instead |

### 4. Configuring speed, duplex, description, and disabling unused ports

- On F0/1 (to R1, also a FastEthernet interface): `speed ?` offers **10, 100, auto** → `speed 100`; `duplex ?` offers **auto, full, half** → `duplex full`; then a `description`. In `show interfaces status`, duplex and speed now read **full** and **100** (no *a*): no longer autonegotiated.
- Normally you **keep autonegotiation on**; you should know how to configure manually if it is not working.
- Ports enabled by default are convenient but a **security concern**: **disable unused interfaces**.
- **`interface range f0/5 - 12`**: `(config-if-range)#` mode, a description then `shutdown` for all of them at once (*administratively down* messages). Non-consecutive ranges: `interface range f0/5 - 6, f0/9 - 12`; a `no shutdown` there re-enables only those six, F0/7 and F0/8 stay down. `show interfaces status` then shows **disabled**.

### 5. Half duplex, full duplex, hubs and CSMA/CD

- **Half duplex**: the device **cannot** send and receive at the same time; if receiving a frame, it must wait before sending. **Full duplex**: it can do both at once. In modern switched networks **everything runs full duplex**; half duplex is used almost nowhere.
- The **hub**, which predates the switch, is a simple **Layer 1 repeater**: any frame received is repeated out of all other interfaces (like a switch flooding a broadcast or unknown unicast). If PC1 and PC3 send at the same time, the hub repeats both at once: **collision**, PC2 receives neither frame intact. All devices on a hub form one **collision domain**.
- **CSMA/CD** (*Carrier Sense Multiple Access with Collision Detection*): before sending, listen to the collision domain until no other device is sending; if a collision still occurs, send a **jamming signal**, then each device waits a **random period** before trying again.
- A switch works at Layer 2 with MAC addresses and never sends two frames to the same host at once: with three PCs, one collision domain becomes **three**. Collisions become rare and are **a sign of a problem** (misconfiguration).
- Devices attached to a hub must use half duplex; devices attached to a switch can use full duplex.

### 6. Speed and duplex autonegotiation (routers and switches)

- Multi-speed interfaces (10/100 or 10/100/1000) default to **speed auto** and **duplex auto**: they advertise their capabilities and agree on the best settings both support. Example: an Ethernet PC (10), a FastEthernet PC (10/100) and a Gigabit PC (10/100/1000) on G0/1, G0/2, G0/3 negotiate 10, 100 and 1000 Mbps, all full duplex.
- **If autonegotiation is disabled on the other device**: the switch tries to **sense the speed**; if it fails, it uses the **slowest supported speed** (10 Mbps on a 10/100/1000 port). It cannot sense the duplex: **half duplex if 10 or 100 Mbps, full duplex if 1000 Mbps or greater**.
- Example: PC at 10 Mbps → 10/half; PC at 1000 → 1000/full; PC fixed at 100 full → the switch uses 100/**half**: **duplex mismatch**, collisions, poor performance. Conclusion: use autonegotiation on all devices.

### 7. Error counters in `show interfaces` (switch or router)

At the bottom of the output: total **packets and bytes received**, then:

- **runts**: frames smaller than the Ethernet minimum of **64 bytes**;
- **giants**: frames larger than the maximum of **1518 bytes**;
- **CRC**: frames that failed the CRC check (*cyclic redundancy check*, done via the FCS in the Ethernet trailer);
- **frame**: frames with an incorrect or illegal format;
- **input errors**: a total of several counters including the four above;
- **output errors**: frames the switch tried to send but failed.

### Exam traps

- **Router**: interfaces `shutdown` by default (administratively down/down). **Switch**: never `shutdown` by default (up/up or down/down). Down/down is not administratively down.
- **disabled** in `show interfaces status` and **administratively down** in `show ip interface brief` mean the same thing.
- **Duplex mismatch** → collisions (not an automatic adjustment): without autonegotiation, the neighbor cannot guess the duplex.
- Rule when the neighbor has autonegotiation off: sense the speed (else slowest), **half if 10/100, full if 1000+**.
- **CSMA/CD** = half duplex and collisions; CSMA/**CA** is something else (covered later).
- Error counters live in **`show interfaces`**; `show interfaces errors` does not exist; broadcasts are not errors.
- Runt < 64 bytes, giant > 1518 bytes.

### IOS commands

```text
SW1# show ip interface brief                  ! Status/Protocol: up/up, down/down (switch) or administratively down (router)
SW1# show interfaces status                   ! switches only: Port, Name, Status, Vlan, Duplex, Speed, Type
SW1# show interfaces f0/1                     ! one interface's detail + counters (runts, giants, CRC, frame, input/output errors)
SW1(config)# interface f0/1                   ! interface mode
SW1(config-if)# speed 100                     ! 10 | 100 | auto (default auto); 1000 on a gigabit port
SW1(config-if)# duplex full                   ! auto (default) | full | half
SW1(config-if)# description ## to R1 ##       ! shows in the Name column of show interfaces status
SW1(config)# interface range f0/5 - 12        ! several interfaces at once, (config-if-range)# mode
SW1(config)# interface range f0/5 - 6, f0/9 - 12   ! non-consecutive ranges separated by a comma
SW1(config-if-range)# shutdown                ! disable unused ports (security); no shutdown re-enables
R1(config-if)# do show running-config         ! check speed, duplex, addresses, descriptions
R1# copy running-config startup-config        ! save; equivalents: write memory, write
R1# show startup-config                       ! check the saved configuration
```

### The lab (video #17)

**Goal**: one LAN **172.16.0.0/16** connected to R1 G0/0; configure R1, SW1, SW2 and four PCs. Six steps: hostnames, IP addresses, speed and duplex, descriptions, disabling unused interfaces, saving. Jeremy goes device by device.

**R1**: `enable`, `configure terminal`, `hostname R1`. `interface g0/0`, then `do show ip interface brief` (unassigned, unset, administratively down). `ip address 172.16.255.254 255.255.0.0`; because the interface connects to a network device (SW1), set speed and duplex manually: `speed 1000` (gigabit interface), `duplex full`; `description ## to SW1 ##`; `no shutdown` (router interfaces are shut down by default, so unused ports need nothing; the connected one needs the opposite). Check: up/**down** in Packet Tracer because SW1's side is not yet manually configured; a real device should show up/up, a limitation of the simulator. `interface range g0/1 - 2`, `description ## not in use ##`. `do show run`, `end`, save with `copy running-config startup-config` (Enter to confirm), check with `show startup-config`.

**PC1 to PC4** (*Config*, gateway pre-configured = R1): *FastEthernet0*, addresses **172.16.0.1** to **172.16.0.4**; the **Tab** key fills in the 255.255.0.0 mask.

**SW1**: `enable`, `conf t`, `hostname SW1`, `do show interfaces status` (works on switches, not routers; all defaults, statuses connected or notconnect, never disabled). `interface g0/1`: `speed 1000`, `duplex full`, `description ## to R1 ##`. `interface g0/2`: same, `description ## to SW2 ##`. `interface range f0/1 - 2` (end hosts: no speed/duplex per the lab instructions): `description ## to end hosts ##`. `interface range f0/3 - 24` (22 unused ports): `description ## not in use ##`, `shutdown`. `do show interfaces status`: ports disabled; G0/2 still down until SW2 is configured. Another Packet Tracer limitation: it shows **a-1000 / a-full** where a real device would show **1000 / full** (manual settings). `end`, `write memory`, `show startup-config`.

**SW2**: `hostname SW2`, `interface g0/1`: `speed 1000`, `duplex full`, `description ## to SW1 ##`; `interface range f0/1 - 2`, `description ## to end hosts ##`; `interface range g0/2, f0/3 - 24`, `description ## not in use ##`, `shutdown`. `do show interfaces status`, `end`, save with `write`, `show startup-config`.

### The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| 1. Duplex mismatch between SW1 F0/1 and SW2 F0/1, autonegotiation disabled: result? A improved performance; B collisions; C SW1 senses SW2's duplex and adjusts | **B, collisions** | The half-duplex side cannot send and receive at once; the full-duplex side is unaware and sends anyway. Performance will be much worse (A wrong). Without autonegotiation SW1 cannot sense the duplex (C wrong). |
| 2. What do half-duplex interfaces use to detect and avoid collisions? A CSMA/CD; B CSMA/CA; C autonegotiation; D duplex auto | **A, CSMA/CD** | Carrier sense multiple access with collision detection: listen before sending, react to collisions. CSMA/CA (collision avoidance) is a similar concept covered later; C and D are unrelated. |
| 3. Which command shows error counters on an interface? A show interfaces; B show ip interface brief; C show interfaces status; D show interfaces errors | **A, show interfaces** | B shows no counters (IP addresses, shutdown state); C shows description, status, duplex, speed but no counters; D is not a real command (error message). Specify the interface (`show interfaces f0/1`); counters are at the bottom. |
| 4. Examples of errors on a network interface? A runts, giants, broadcasts; B shorts, longs, oversizes; C packets, bytes, inputs, outputs; D runts, giants, CRC | **D, runts, giants, CRC** | B and C are not real errors. In A, runts and giants are errors but broadcasts are normal operation. Runts = too small, giants = too big, CRC = failed FCS check. |
| 5. SW1 autonegotiates, SW2 has autonegotiation disabled with 100 Mbps full: SW1's settings? A 100/full; B 100/half; C 10/full; D 10/half | **B, 100 Mbps, half** | SW1 senses the speed (100) but cannot sense the duplex: rule "10 or 100 → half, otherwise full". Result: duplex mismatch and collisions. |
