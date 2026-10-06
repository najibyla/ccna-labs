# CCNA Day 52 : LAN Architectures / Architectures LAN

> Source : Jeremy's IT Lab, « Free CCNA | LAN Architectures | Day 52 » (28 min, vidéo n°105 de la playlist, cours) et « Free CCNA | STP & FHRP Synchronization | Day 52 Lab » (19 min, vidéo n°106, lab). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

Sujets d'examen 1.2.a, b, c et e : architectures **2 tiers, 3 tiers, spine-leaf, SOHO**. (1.2.d WAN et 1.2.f on-premises/cloud sont traités dans d'autres vidéos.) La conception réseau est un sujet profond ; la réponse à la plupart des questions générales est « ça dépend ». En début de carrière on ne conçoit pas les réseaux, mais il faut en comprendre les bases pour configurer et dépanner.

### 1. Terminologie des topologies

- **Étoile** (*star*) : plusieurs appareils connectés à **un appareil central** (des PC sur un switch), quelle que soit la façon de dessiner le schéma.
- **Maillage complet** (*full mesh*) : **chaque appareil connecté à chaque autre** (6 routeurs tous reliés entre eux).
- **Maillage partiel** (*partial mesh*) : certains appareils connectés entre eux, **pas tous** (4 switches : les deux du haut reliés à tous les autres, les deux du bas pas reliés directement).
- Les combinaisons sont parfois appelées **topologie hybride**.

### 2. Conception LAN à deux niveaux (*2-tier*)

LAN de campus = LAN d'un bâtiment ou de plusieurs bâtiments proches. Deux couches hiérarchiques : **accès** et **distribution**. Aussi appelée **collapsed core** : la couche cœur est omise, ou plus précisément fusionnée avec la distribution.

- **Couche d'accès** (*access layer*) : couche à laquelle se connectent les **hôtes finaux** (PC, imprimantes, caméras de sécurité). Switches avec **beaucoup de ports**. **Marquage QoS** fait ici (le plus tôt possible dans le réseau). **Services de sécurité** (port security, DAI, DHCP snooping) faits ici. Ports éventuellement **PoE** pour les points d'accès sans fil et téléphones IP.
- **Couche de distribution** (*distribution layer*) : **agrège** les connexions des switches d'accès, en général vers une **paire redondante** de switches de distribution. Typiquement la **frontière entre couche 2 et couche 3** : ces switches font tourner à la fois des protocoles de couche 3 (OSPF) et de couche 2 (spanning tree). En général les liens accès-distribution sont de couche 2 et les hôtes utilisent les **SVI** des switches de distribution comme passerelle par défaut. Connecte aux services : **Internet, WAN**, autres parties du LAN. Parfois appelée **couche d'agrégation** ; dans un collapsed core, **core-distribution layer**.
- Exemple : A1 et A2 (accès, chacun avec des hôtes et un point d'accès) connectés tous deux à D1 et D2 (distribution) pour la **redondance**. Liens accès-distribution de couche 2 : **boucles possibles**, STP désactive des liens. D1 et D2 sont des switches multicouches ; les hôtes utilisent leurs SVI avec un **FHRP** (HSRP ou VRRP) pour une IP virtuelle redondante. Deux connexions Internet redondantes vers deux ISP. Un autre bloc distribution/accès (serveurs) : chaque switch de distribution relié à chaque autre, liens de **couche 3**, pas de STP, routes partagées par OSPF.
- Lecture topologique : chaque switch d'accès avec ses hôtes = **étoile** ; accès-distribution = **maillage partiel** (les switches de distribution reliés entre eux et à chaque switch d'accès, les switches d'accès pas reliés entre eux) ; les quatre switches de distribution = **maillage complet**.

### 3. Conception à trois niveaux (*3-tier*) : la couche cœur

- Problème des grands LAN : avec de nombreuses couches de distribution (bâtiments d'un campus), le **nombre de connexions** entre switches de distribution croît rapidement ; difficile à faire évoluer (*scale*). **Cisco recommande une couche cœur au-delà de trois couches de distribution** sur un même site (l'exemple en a 6).
- **Couche cœur** (*core layer*) : relie les couches de distribution entre elles dans les grands LAN. Objectif : la **vitesse** (*fast transport*). **Éviter les opérations gourmandes en CPU** : sécurité, marquage et classification QoS. Connexions **toutes de couche 3**, **pas de spanning tree**. Doit maintenir la connectivité même en cas de panne : **redondance** des équipements et des liens essentielle (c'est le backbone du LAN). Paire de switches très puissants et rapides.
- Avec le cœur, les routeurs Internet se connectent aux switches cœur, ainsi que les blocs distribution/accès supplémentaires. Les petits LAN se contentent de deux niveaux ; les grands en ont trois. Peu de réponses universelles : d'innombrables variantes selon l'entreprise.

### 4. Architecture spine-leaf (centres de données)

- **Centre de données** (*data center*) : espace ou bâtiment dédié aux serveurs et équipements réseau, montés dans des **racks**. Conception traditionnelle : trois niveaux, adaptée au trafic **nord-sud** (de l'accès vers la distribution, le cœur, Internet, ou vers d'autres blocs). Le trafic **est-ouest** = trafic entre serveurs d'une même partie du réseau.
- Avec les **serveurs virtuels**, les applications sont déployées de façon distribuée sur plusieurs serveurs physiques : le trafic est-ouest augmente ; le modèle à trois niveaux crée des **goulots d'étranglement** de bande passante et une **latence variable** serveur à serveur selon le chemin.
- **Spine-leaf**, aussi appelée **architecture Clos** (du nom d'un de ses concepteurs) : deux niveaux, **switches spine** et **switches leaf**. Règles :
  1. **Chaque leaf est connecté à chaque spine** (et donc chaque spine à chaque leaf).
  2. **Les leaf ne se connectent pas entre eux ; les spine ne se connectent pas entre eux.**
  3. **Les hôtes finaux (serveurs) ne se connectent qu'aux leaf** (la « couche d'accès » du spine-leaf).
- Le chemin est **choisi aléatoirement** pour équilibrer la charge entre les spine. Chaque serveur est séparé des autres par le **même nombre de sauts** (sauf ceux sur le même leaf) : **latence constante** pour le trafic est-ouest (serveur à serveur : trois switches). **Facile à faire évoluer** : ajouter un leaf et le connecter aux spine existants.

### 5. Réseaux SOHO (*Small Office/Home Office*)

- Bureau d'une petite entreprise ou bureau à domicile avec peu d'appareils ; tout réseau domestique connecté à Internet est un SOHO.
- Besoins simples : toutes les fonctions fournies par **un seul appareil**, le **routeur domestique** ou **routeur sans fil** (*home router*, *wireless router*) : **routeur** (vers Internet), **switch** (quelques ports à l'arrière), **pare-feu** simple (bloque les connexions entrantes, autorise les sorties), **point d'accès sans fil** (WiFi), parfois **modem** câble (parfois séparé). Une entreprise aurait un appareil dédié par fonction. Les petites structures louent souvent ce routeur à l'ISP.

### 6. Pièges d'examen

- La **distribution** est la frontière couche 2 / couche 3 : liens accès-distribution de couche 2 avec STP, liens distribution-cœur de couche 3.
- **Pas de STP au cœur** (tout en couche 3) ; pas de sécurité ni de QoS au cœur.
- Les ports **PoE** sont à la couche d'**accès** (points d'accès, téléphones IP, caméras IP).
- Spine-leaf : un leaf ne se connecte **jamais à un autre leaf** ; un spine jamais à un autre spine ; les serveurs seulement aux leaf.
- Un routeur sans fil SOHO combine **routage, commutation, sécurité, accès sans fil**.
- Terminologie : étoile, maillage complet, maillage partiel ; distribution = agrégation.

### 7. Commandes IOS

```
DSW1(config)# spanning-tree vlan 10 root primary    ! DSW1 devient root bridge du VLAN 10
DSW1(config)# spanning-tree vlan 20 root secondary  ! root secondaire du VLAN 20
DSW1(config)# interface vlan 10
DSW1(config-if)# standby version 2                  ! HSRP version 2
DSW1(config-if)# standby 10 ip 10.0.10.254          ! IP virtuelle du groupe 10 (le numéro de groupe n'a pas à égaler le VLAN)
DSW1(config-if)# standby 10 priority 105            ! priorité supérieure au défaut 100
DSW1(config-if)# standby 10 preempt                 ! préemption
DSW1# show standby brief                            ! état HSRP : active/standby par groupe
DSW1# show spanning-tree vlan 10                    ! root bridge, root port, ports designated
```

### 8. Le lab : synchronisation STP et FHRP (HSRP)

- Principe : le **HSRP active doit être le root bridge STP**, le **HSRP standby le root secondaire**, pour que le trafic des hôtes suive le **chemin le plus direct vers la passerelle**. Sinon le trafic de PC1 vers DSW1 peut prendre un chemin plus long (pas une catastrophe, mais pas idéal). STP cherche le plus court chemin vers le root. Vaut pour tout FHRP.
- Objectif : DSW1 active HSRP et root STP pour le **VLAN 10** ; DSW2 pour le **VLAN 20**.
- **État initial** sur DSW1 : `show standby brief` vide ; `show spanning-tree vlan 10` : DSW1 a un root port G1/0/3 vers DSW2, donc DSW2 est root ; idem VLAN 20.
- **DSW1** :

```
DSW1(config)# spanning-tree vlan 10 root primary
DSW1(config)# spanning-tree vlan 20 root secondary
DSW1(config)# do show spanning-tree vlan 10     ! DSW1 root, tous les ports designated
DSW1(config)# do show spanning-tree vlan 20     ! DSW1 root aussi pour l'instant (DSW2 pas encore configuré)
DSW1(config)# interface vlan 10
DSW1(config-if)# standby version 2
DSW1(config-if)# standby 10 ip 10.0.10.254
DSW1(config-if)# standby 10 priority 105
DSW1(config-if)# standby 10 preempt
DSW1(config-if)# interface vlan 20
DSW1(config-if)# standby version 2
DSW1(config-if)# standby 20 ip 10.0.20.254
DSW1(config-if)# standby 20 priority 95
DSW1(config-if)# standby 20 preempt
```

- **DSW2** : `spanning-tree vlan 10 root secondary`, `spanning-tree vlan 20 root primary` ; `do show spanning-tree vlan 20` : DSW2 root ; `do show spanning-tree vlan 10` : root port G1/0/3 vers DSW1. Puis `interface vlan 10` : `standby version 2`, `standby 10 ip 10.0.10.254`, `standby 10 priority 95`, `standby 10 preempt` ; `interface vlan 20` : `standby version 2`, `standby 20 ip 10.0.20.254`, `standby 20 priority 105`, `standby 20 preempt`.
- **Vérification** : `show standby brief` sur DSW2 : VLAN 10 active 10.0.10.1 (DSW1), standby local ; VLAN 20 active local, standby 10.0.20.1 (DSW1). Sur DSW1 : l'inverse. Les hôtes du VLAN 10 ont un chemin direct vers DSW1, ceux du VLAN 20 vers DSW2. Bon principe de conception LAN, probablement pas demandé à l'examen.

### 9. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quelle couche sert de frontière entre couche 2 et couche 3 dans un LAN 2 ou 3 niveaux ? | **B** : distribution | Liens accès-distribution en couche 2 avec STP ; liens distribution-cœur en couche 3. |
| Que ne s'attend-on PAS à trouver à la couche cœur d'un LAN 3 niveaux ? | **B** : STP | Les connexions du cœur sont toutes de couche 3 ; pas de spanning tree. |
| À quelle couche trouve-t-on des ports PoE ? | **A** : accès | Points d'accès, téléphones IP, caméras IP se connectent à la couche d'accès. |
| En spine-leaf, qu'est-ce qui ne doit pas être connecté à un switch leaf ? | **B** : un switch leaf | Les serveurs se connectent aux leaf, chaque leaf à tous les spine, mais les leaf ne se connectent pas entre eux. |
| Quelles fonctions peut inclure un « routeur sans fil » ? | **F** (toutes) | Appareil multifonction d'un réseau SOHO : routage, commutation, accès sans fil, sécurité. |

---

## 🇬🇧 English version

Exam topics 1.2.a, b, c and e: **2-tier, 3-tier, spine-leaf, SOHO** architectures. (1.2.d WAN and 1.2.f on-premises/cloud are covered in other videos.) Network design is a deep topic; the answer to most general questions is "it depends". Early in your career you won't design networks, but you need the basics to configure and troubleshoot them.

### 1. Topology terminology

- **Star**: several devices connected to **one central device** (PCs on a switch), however the diagram is drawn.
- **Full mesh**: **each device connected to each other device** (6 routers all interconnected).
- **Partial mesh**: some devices connected to each other, **not all** (4 switches: the top two connected to every other switch, the bottom two not directly connected).
- Combinations are sometimes called a **hybrid topology**.

### 2. Two-tier LAN design

Campus LAN = LAN of a building or several nearby buildings. Two hierarchical layers: **access** and **distribution**. Also called **collapsed core**: the core layer is omitted, or more accurately combined with distribution.

- **Access layer**: the layer **end hosts** connect to (PCs, printers, security cameras). Switches with **lots of ports**. **QoS marking** done here (mark as early as possible). **Security services** (port security, DAI, DHCP snooping) done here. Ports may be **PoE** for wireless access points and IP phones.
- **Distribution layer**: **aggregates** connections from access switches, usually to a **redundant pair** of distribution switches. Typically the **border between Layer 2 and Layer 3**: these switches run both Layer 3 protocols (OSPF) and Layer 2 protocols (spanning tree). Usually access-to-distribution links are Layer 2 and hosts use the distribution switches' **SVIs** as default gateways. Connects to services: **Internet, WAN**, other parts of the LAN. Sometimes called the **aggregation layer**; in a collapsed core, the **core-distribution layer**.
- Example: A1 and A2 (access, each with hosts and an access point) both connected to D1 and D2 (distribution) for **redundancy**. Layer 2 access-distribution links: **loops possible**, STP disables some links. D1 and D2 are multilayer switches; hosts use their SVIs with an **FHRP** (HSRP or VRRP) for a redundant virtual IP. Two redundant Internet connections to two ISPs. Another distribution/access block (servers): each distribution switch connected to each other, **Layer 3** links, no STP, routes shared via OSPF.
- Topology reading: each access switch with its hosts = **star**; access-distribution = **partial mesh** (distribution switches connected to each other and to each access switch, access switches not connected to each other); the four distribution switches = **full mesh**.

### 3. Three-tier design: the core layer

- Problem in large LANs: with many distribution layers (campus buildings), the **number of connections** between distribution switches grows rapidly; hard to **scale**. **Cisco recommends a core layer with more than three distribution layers** in a single location (the example has 6).
- **Core layer**: connects separate distribution layers together in large LANs. Focus: **speed** (**fast transport**). **Avoid CPU-intensive operations**: security, QoS marking and classification. Connections **all Layer 3**, **no spanning tree**. Must maintain connectivity even if devices fail: **redundancy** of devices and connections is very important (the LAN backbone). A pair of very powerful, fast switches.
- With a core, the Internet routers connect to the core switches, as do additional distribution/access blocks. Smaller LANs use two tiers; larger ones three. Few universal answers: countless variations depending on the enterprise.

### 4. Spine-leaf architecture (data centers)

- **Data center**: dedicated space or building for servers and network devices, mounted in **racks**. Traditional design: three tiers, suited to **north-south** traffic (from access up to distribution, core, Internet, or to other blocks). **East-west** traffic = traffic between servers in the same part of the network.
- With **virtual servers**, applications are deployed in a distributed manner across multiple physical servers: east-west traffic increases; the three-tier model creates bandwidth **bottlenecks** and **variable** server-to-server latency depending on the path.
- **Spine-leaf**, also called **Clos architecture** (after one of its designers): two tiers, **spine switches** and **leaf switches**. Rules:
  1. **Every leaf connects to every spine** (so every spine connects to every leaf).
  2. **Leaves do not connect to other leaves; spines do not connect to other spines.**
  3. **End hosts (servers) connect only to leaf switches** (the "access layer" of spine-leaf).
- The path is **chosen randomly** to balance load among the spines. Each server is separated by the **same number of hops** (except those on the same leaf): **consistent latency** for east-west traffic (server to server: three switches). **Easy to scale**: add a leaf and connect it to the existing spines.

### 5. SOHO networks (Small Office/Home Office)

- Office of a small company or a small home office with few devices; any home network connected to the Internet is a SOHO.
- Simple needs: all functions provided by **a single device**, the **home router** or **wireless router**: **router** (to the Internet), **switch** (a few ports on the back), simple **firewall** (blocks inbound connections, allows outbound), **wireless access point** (WiFi), sometimes a cable **modem** (sometimes separate). An enterprise would have a dedicated device for each. Small businesses often rent this router from the ISP.

### 6. Exam traps

- The **distribution** layer is the Layer 2 / Layer 3 boundary: access-distribution links are Layer 2 with STP, distribution-core links are Layer 3.
- **No STP in the core** (all Layer 3); no security or QoS in the core.
- **PoE** ports are at the **access** layer (access points, IP phones, IP cameras).
- Spine-leaf: a leaf **never connects to another leaf**; a spine never to another spine; servers only to leaves.
- A SOHO wireless router combines **routing, switching, security, wireless access**.
- Terminology: star, full mesh, partial mesh; distribution = aggregation.

### 7. IOS commands

```
DSW1(config)# spanning-tree vlan 10 root primary    ! DSW1 becomes root bridge for VLAN 10
DSW1(config)# spanning-tree vlan 20 root secondary  ! secondary root for VLAN 20
DSW1(config)# interface vlan 10
DSW1(config-if)# standby version 2                  ! HSRP version 2
DSW1(config-if)# standby 10 ip 10.0.10.254          ! virtual IP for group 10 (group number need not match the VLAN)
DSW1(config-if)# standby 10 priority 105            ! priority above the default 100
DSW1(config-if)# standby 10 preempt                 ! preemption
DSW1# show standby brief                            ! HSRP state: active/standby per group
DSW1# show spanning-tree vlan 10                    ! root bridge, root port, designated ports
```

### 8. The lab: STP and FHRP (HSRP) synchronization

- Principle: the **HSRP active should be the STP root bridge**, the **HSRP standby the secondary root**, so host traffic follows the **most direct path to the default gateway**. Otherwise traffic from PC1 to DSW1 may take a longer path (not a disaster, but not ideal). STP finds the shortest path to the root. Applies to any FHRP.
- Goal: DSW1 HSRP active and STP root for **VLAN 10**; DSW2 for **VLAN 20**.
- **Initial state** on DSW1: `show standby brief` empty; `show spanning-tree vlan 10`: DSW1 has root port G1/0/3 to DSW2, so DSW2 is root; same for VLAN 20.
- **DSW1**:

```
DSW1(config)# spanning-tree vlan 10 root primary
DSW1(config)# spanning-tree vlan 20 root secondary
DSW1(config)# do show spanning-tree vlan 10     ! DSW1 root, all ports designated
DSW1(config)# do show spanning-tree vlan 20     ! DSW1 root for now too (DSW2 not configured yet)
DSW1(config)# interface vlan 10
DSW1(config-if)# standby version 2
DSW1(config-if)# standby 10 ip 10.0.10.254
DSW1(config-if)# standby 10 priority 105
DSW1(config-if)# standby 10 preempt
DSW1(config-if)# interface vlan 20
DSW1(config-if)# standby version 2
DSW1(config-if)# standby 20 ip 10.0.20.254
DSW1(config-if)# standby 20 priority 95
DSW1(config-if)# standby 20 preempt
```

- **DSW2**: `spanning-tree vlan 10 root secondary`, `spanning-tree vlan 20 root primary`; `do show spanning-tree vlan 20`: DSW2 root; `do show spanning-tree vlan 10`: root port G1/0/3 to DSW1. Then `interface vlan 10`: `standby version 2`, `standby 10 ip 10.0.10.254`, `standby 10 priority 95`, `standby 10 preempt`; `interface vlan 20`: `standby version 2`, `standby 20 ip 10.0.20.254`, `standby 20 priority 105`, `standby 20 preempt`.
- **Verification**: `show standby brief` on DSW2: VLAN 10 active 10.0.10.1 (DSW1), standby local; VLAN 20 active local, standby 10.0.20.1 (DSW1). On DSW1: the opposite. VLAN 10 hosts have a direct path to DSW1, VLAN 20 hosts to DSW2. Good LAN design principle, probably not asked on the exam.

### 9. The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which layer serves as the boundary between Layer 2 and Layer 3 in a 2-tier or 3-tier LAN? | **B**: distribution | Access-to-distribution links are Layer 2 running STP; distribution-to-core links are Layer 3. |
| Which would you NOT expect to find in the core layer of a 3-tier LAN? | **B**: STP | Core connections are all Layer 3; spanning tree should not run there. |
| At which layer would you expect PoE-enabled ports? | **A**: access | Access points, IP phones and IP cameras connect to the access layer. |
| In spine-leaf, what should not be connected to a leaf switch? | **B**: a leaf switch | Servers connect to leaves, each leaf to all spines, but leaves do not connect to each other. |
| Which functions might a "wireless router" include? | **F** (all of them) | Multipurpose SOHO device: routing, switching, wireless access, security. |
