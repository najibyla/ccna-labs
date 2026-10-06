# CCNA Day 24 : Dynamic Routing / Routage dynamique

> Source : Jeremy's IT Lab, « Free CCNA | Dynamic Routing | Day 24 » (cours, 45 min, vidéo n°49 de la playlist, début de la section 3.0 IP Connectivity, 25 % de l'examen) et « Floating Static Routes | Day 24 Lab » (lab, 23 min, vidéo n°50). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Routage statique et routage dynamique

- **Routage statique** (Day 11) : routes configurées à la main avec `ip route`. Si un lien tombe, R1 ne le sait pas et continue d'envoyer le trafic vers un cul-de-sac. Impraticable dans un grand réseau (des milliers de routes).
- **Routage dynamique** : un protocole de routage est activé sur les routeurs, qui **annoncent** (*advertise*) leurs réseaux à leurs voisins (« tu peux joindre 192.168.4.0/24 via moi »), ajoutent les routes apprises à leur table, les relaient à leurs autres voisins, **retirent** automatiquement les routes invalides en cas de panne, et basculent sur le **prochain meilleur chemin** s'il existe (R1 : « via 10.0.12.2 » remplacé par « via 10.0.13.2 »).
- Vocabulaire de la liste d'examen : **route réseau (network route)** = route vers un réseau/sous-réseau, masque plus court que /32 (10.0.12.0/30, 192.168.4.0/24). **Route hôte (host route)** = route vers une adresse unique, masque **/32** (les routes locales 10.0.12.1/32 ajoutées automatiquement) ; route statique vers un hôte : `ip route <adresse> 255.255.255.255 ...`.
- Les routeurs forment des **adjacences** (*adjacencies*, *neighbor relationships*, *neighborships*) avec leurs voisins directement connectés pour échanger ces informations. Si plusieurs routes vers une destination sont apprises, la route avec la **métrique la plus basse** est ajoutée à la table (comme le root cost de STP).

### 2. Types de protocoles de routage dynamique

- **IGP (Interior Gateway Protocol)** : partage des routes **au sein d'un système autonome (AS, autonomous system)**, c'est-à-dire une organisation (une entreprise). **EGP (Exterior Gateway Protocol)** : partage des routes **entre AS** (Company A, Company B, ISP A, ISP B).
- Classement par **type d'algorithme** (processus de partage des routes et de choix de la meilleure) :

| Catégorie | Algorithme | Protocoles |
| :--- | :--- | :--- |
| IGP | **Distance vector** | **RIP** (Routing Information Protocol), **EIGRP** (Enhanced Interior Gateway Routing Protocol) |
| IGP | **Link state** | **OSPF** (Open Shortest Path First), **IS-IS** (Intermediate System to Intermediate System) |
| EGP | **Path vector** | **BGP** (Border Gateway Protocol), le seul EGP utilisé aujourd'hui |

- OSPF est le seul protocole de routage dynamique cité dans la liste d'examen (3.4), mais il faut savoir comparer les autres avec lui. BGP et IS-IS ne sont pas détaillés (IS-IS : voir CCNP Service Provider).

### 3. Distance vector vs link state

- **Distance vector** (inventés au début des années 1980 : RIP, IGRP de Cisco devenu EIGRP) : chaque routeur envoie à ses **voisins directement connectés** ses réseaux de destination connus et sa **métrique** pour les atteindre. Dit **« routing by rumor »** : le routeur ne connaît du réseau que ce que ses voisins lui disent. Il n'apprend que la **distance** (la métrique) et le **vecteur** (la direction : le next hop). Exemple : R4 dit à R2 « 192.168.4.0/24 via moi, métrique 1 » ; R2 dit à R1 « via moi, métrique 2 » ; R1 ne sait rien de plus.
- **Link state** : chaque routeur annonce des informations sur **ses interfaces et réseaux connectés**, qui sont relayées à tous ; chaque routeur construit la **même carte de connectivité** du réseau et calcule **indépendamment** les meilleures routes. Plus de ressources (CPU, mémoire) car plus d'informations partagées, mais réaction **plus rapide** aux changements. Protocoles : OSPF, IS-IS.

### 4. Métriques

- La **métrique** mesure la « distance » vers la destination ; **la plus basse est la meilleure**. Chaque protocole a la sienne :

| Protocole | Métrique |
| :--- | :--- |
| **RIP** | **Hop count** (nombre de routeurs traversés) ; tous les liens comptent 1, quelle que soit la vitesse (10 Mbps = 10 Gbps = 1 saut) : primitif. |
| **EIGRP** | Calcul basé sur la **bande passante et le délai** (par défaut ; d'autres facteurs configurables). Bande passante du lien **le plus lent** du chemin + **somme des délais** de tous les liens ; le « délai » est une valeur par défaut assignée à l'interface selon sa bande passante. La plus compliquée des IGP. |
| **OSPF** | **Cost**, calculé d'après la **bande passante** de chaque lien ; la métrique de la route est la somme des coûts. |
| **IS-IS** | **Cost** aussi, mais pas calculé automatiquement : **10 par défaut** sur tous les liens, donc équivalent à un hop count sans configuration. |

- Exemple : R1 vers 192.168.4.0/24 via R2 (Gigabit) ou via R3 (lien R3-R4 FastEthernet). En **RIP**, 2 sauts dans les deux cas : les deux routes entrent dans la table, load balancing même sur le chemin lent. En **OSPF**, le lien FastEthernet coûte plus : seule la route via R2 est retenue.
- **ECMP (Equal Cost MultiPath)** : si un routeur apprend par le **même protocole** plusieurs routes vers **exactement la même destination** (même adresse réseau et même longueur de préfixe) avec la **même métrique**, toutes sont ajoutées et le trafic est réparti. Dans `show ip route`, les crochets `[110/3]` : **gauche = AD, droite = métrique**. Fonctionne aussi avec des **routes statiques** (deux `ip route` vers la même destination : métrique **0**, AD **1**).

### 5. Administrative Distance (AD)

- La métrique compare des routes du **même protocole** ; des protocoles différents ont des métriques incomparables (OSPF 30 contre EIGRP 33280). L'**AD** détermine quel protocole est **préféré** : **la plus basse gagne**, elle indique une source plus « fiable » (trustworthy). Valeurs Cisco (d'autres constructeurs peuvent différer) :

| Source | AD |
| :--- | :--- |
| Connected | **0** |
| Static | **1** |
| eBGP (external BGP) | **20** |
| EIGRP | **90** |
| IGRP | **100** |
| OSPF | **110** |
| IS-IS | **115** |
| RIP | **120** |
| EIGRP external | **170** |
| iBGP (internal BGP) | **200** |
| Inutilisable | **255** (« the router does not believe the source of that route and does not install the route ») |

- Ordre de décision : d'abord l'**AD**, puis la métrique. Exemple : trois routes vers 10.1.1.0/24, RIP métrique 5, RIP métrique 3, OSPF métrique 10 → la route **OSPF** (AD 110 < 120) entre dans la table.
- Dans `show ip route`, les routes statiques affichent `[1/0]` ; connected et local ont AD 0 mais elle n'est pas affichée ; OSPF `[110/...]`.
- L'AD d'un protocole peut être modifiée (démontré pour OSPF plus tard), celle d'une route statique aussi : `ip route <réseau> <masque> <next-hop> <AD>` ; le `?` affiche « distance metric », mais c'est bien l'**AD**, pas la métrique.
- **Floating static route** : route statique dont l'AD est **supérieure** à celle du protocole dynamique vers la même destination (ex. 111 > 110 pour OSPF). Elle reste **inactive** (absente de la table) tant que la route dynamique existe et prend le relais si celle-ci disparaît (voisin qui cesse d'annoncer, panne d'interface, adjacence perdue). Si l'AD de la statique reste inférieure, elle serait préférée, ce qui n'est pas voulu. Sujet de la liste d'examen.

### 6. Pièges d'examen

- **AD d'abord, métrique ensuite.** Jeremy : « je serais surpris que vous n'ayez pas une question du type : routes OSPF et EIGRP vers 10.0.0.0/24, laquelle entre dans la table ? » → **EIGRP (90 < 110)**. Mémoriser le tableau des AD (flashcards).
- Routing by rumor = **distance vector**. Path vector = EGP (BGP). IGP est une catégorie qui contient distance vector et link state.
- RIP et EIGRP = distance vector ; OSPF et IS-IS = link state ; BGP = path vector.
- ECMP demande la même destination, le même protocole et la même métrique. Avec RIP, deux routes de 5 sauts → les deux sont installées.
- Des routes vers des **préfixes différents** (10.20.0.0/22, /24, /26, /28) ne sont pas la même destination : toutes sont dans la table, et le choix se fait par la **correspondance la plus longue** (longest prefix match), sans regarder AD ni métrique (question Boson).
- `[AD/métrique]` dans `show ip route` ; le mot « metric » de `ip route ... ?` désigne l'AD.
- Codes : **O** = OSPF, **D** = EIGRP, **R** = RIP, **S** = static.

### 7. Commandes IOS

```
Router# show ip route                                       ! codes, [AD/métrique], gateway of last resort
Router(config)# ip route 192.168.4.0 255.255.255.0 10.0.12.2       ! route statique (AD 1, métrique 0)
Router(config)# ip route 10.1.1.1 255.255.255.255 10.0.12.2        ! route hôte (/32)
Router(config)# ip route 192.168.4.0 255.255.255.0 10.0.12.2 100   ! route statique avec AD 100
Router(config)# ip route 10.0.2.0 255.255.255.0 203.0.113.1 111    ! floating static route (111 > 110 OSPF)
Router(config)# interface loopback 0                        ! interface virtuelle (vue dans le lab, détaillée plus tard)
Router# traceroute 10.0.2.1                                 ! chaque saut de couche 3 répond (Windows : tracert)
```

### 8. Le lab (vidéo 050, Floating Static Routes)

Objectif : Enterprise A, deux LAN (10.0.1.0/24 sur R1, 10.0.2.0/24 sur R2), R1-R2 reliés en fibre, chacun relié à ISP A (SPR1, SPR2 : Service Provider Router) et à ISP B (ISPBR1, ISPBR2). OSPF entre R1 et R2. Configurer des floating static routes via ISP A en secours du lien direct.

1. **Tables de routage** : sur R1, `show ip route` : connected/local, route statique par défaut vers 203.0.113.9 (ISPBR1), et **10.0.2.0/24 apprise par OSPF (code O)**, l'IGP d'Enterprise A. PC1 → SRV1 (10.0.2.1) : correspondance la plus précise = route OSPF via R2. PC1 → 1.1.1.1 (serveur « Internet ») : seule la route par défaut correspond → ISP B. R2 : symétrique, défaut vers 203.0.113.13 (ISPBR2), OSPF vers 10.0.1.0 via 10.0.0.1 (R1). Pings en mode temps réel (pour l'ARP) puis en **mode simulation** : SRV1 via R1-R2, 1.1.1.1 via R1-ISPBR1. 1.1.1.1 est en fait une **interface loopback** (Loopback0) sur ISPBR1 : interface virtuelle, comme une SVI, pratique pour simuler une destination distante en lab (`show ip interface brief` sur ISPBR1).
2. **Floating static routes** : R1 : `ip route 10.0.2.0 255.255.255.0 203.0.113.1 111` (next hop G0/0/0 de SPR1 ; `?` affiche « distance metric » = AD ; OSPF = 110 donc 111). `do show ip route` : la route **n'apparaît pas**, la route OSPF (AD 110) est préférée. R2 : `ip route 10.0.1.0 255.255.255.0 203.0.113.5 111` (SPR2), nécessaire pour le trafic retour. Même constat.
3. **Test de bascule** : sur R2, `interface g0/2/0`, `shutdown` : la route OSPF devient invalide ; `do show ip route` : **10.0.1.0/24 via 203.0.113.5 [111/0]** apparaît ; idem sur R1. Ping PC1 → SRV1 en temps réel (ARP à refaire sur R1, SPR1, SPR2, R2 ; bouton « avance rapide 30 s » de Packet Tracer), puis en simulation : aller et retour via **ISP A**.
4. **traceroute** : sur un vrai réseau, pas de mode simulation ; `tracert 10.0.2.1` sur le PC Windows (IOS : `traceroute`) : chaque saut de couche 3 répond : 10.0.1.254 (R1 G0/1), 203.0.113.1 (SPR1), 192.168.1.2 (SPR2 G0/1/0), 203.0.113.6 (R2 G0/0/0), 10.0.2.1 (SRV1). À connaître pour l'examen.

Aperçu Boson NetSim (« Static Routes 2 ») : liaisons **série** (retirées de la liste d'examen) : côté **DCE** configure `clock rate 64000`, côté DTE non ; `hostname`, `ip address`, `no shutdown`, `ip route`, sur les PC NetSim `ipconfig /ip <adresse> <masque>` et `ipconfig /dg <passerelle>`, `ipconfig /all` ; ping HostA → HostB ; notation du lab (rouge = commande manquante, bleu = commande en trop).

### 9. Le quiz (vidéo 049 : une question en cours de vidéo, 3 questions, plus une question Boson ExSim)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| En cours de vidéo. Routes vers 10.1.1.0/24 : via 192.168.1.1 RIP métrique 5 ; via 192.168.2.1 RIP métrique 3 ; via 192.168.3.1 OSPF métrique 10. Laquelle entre dans la table ? | La route **OSPF** | L'AD est comparée avant la métrique : OSPF (110) bat RIP (120) quelle que soit la métrique. |
| Q1. R1 apprend quatre routes vers 192.168.1.0/24 par RIP, EIGRP, OSPF, IS-IS : lesquelles entrent dans la table ? | **B, EIGRP seulement** | AD la plus basse (90). Les options « les deux distance vector » ou « les deux link state » ou « toutes » ignorent l'AD. |
| Q2. Quel type de protocole est appelé « routing by rumor » ? | **C, distance vector** | Les routeurs ne connaissent que ce que leurs voisins annoncent (routes + métriques). Link state : carte complète ; path vector : un EGP, hors CCNA ; IGP : catégorie englobant les deux. |
| Q3. R1 apprend deux routes RIP vers 172.16.0.0/16, via 10.0.0.1 et 10.1.0.1, toutes deux à 5 sauts : lesquelles entrent ? | **A, les deux** | Même destination, même protocole, même métrique → ECMP. D serait vrai seulement si une route OSPF concurrente existait. |
| Boson ExSim. `show ip route` montre S 10.20.0.0/22, R /24, D /26, O /28 ; paquet pour 10.20.0.14 : quelle route ? | **B, la route OSPF, longest prefix match** | Destinations différentes (préfixes différents) : AD et métrique ne jouent pas, le routeur prend la correspondance la plus spécifique (/28), vers 192.168.10.1 par Serial0/1. |

---

## 🇬🇧 English version

### 1. Static vs dynamic routing

- **Static routing** (Day 11): routes configured manually with `ip route`. If a link fails, R1 does not know and keeps sending traffic to a dead end. Impractical in large networks (thousands of routes).
- **Dynamic routing**: a routing protocol is enabled on the routers, which **advertise** their networks to neighbors ("you can reach 192.168.4.0/24 via me"), add learned routes to their table, pass them on to other neighbors, automatically **remove** invalid routes on failure, and switch to the **next-best path** if one exists (R1: "via 10.0.12.2" replaced by "via 10.0.13.2").
- Exam topics vocabulary: **network route** = route to a network/subnet, mask shorter than /32 (10.0.12.0/30, 192.168.4.0/24). **Host route** = route to a single address, **/32** mask (the automatically added local routes 10.0.12.1/32); static host route: `ip route <address> 255.255.255.255 ...`.
- Routers form **adjacencies** (**neighbor relationships**, **neighborships**) with directly connected neighbors to exchange this information. If several routes to a destination are learned, the one with the **lowest metric** goes in the table (like STP root cost).

### 2. Types of dynamic routing protocols

- **IGP (Interior Gateway Protocol)**: shares routes **within a single autonomous system (AS)**, i.e. one organization (a company). **EGP (Exterior Gateway Protocol)**: shares routes **between ASes** (Company A, Company B, ISP A, ISP B).
- Classified by **algorithm type** (the processes used to share routes and pick the best):

| Category | Algorithm | Protocols |
| :--- | :--- | :--- |
| IGP | **Distance vector** | **RIP** (Routing Information Protocol), **EIGRP** (Enhanced Interior Gateway Routing Protocol) |
| IGP | **Link state** | **OSPF** (Open Shortest Path First), **IS-IS** (Intermediate System to Intermediate System) |
| EGP | **Path vector** | **BGP** (Border Gateway Protocol), the only EGP used today |

- OSPF is the only dynamic routing protocol in the exam topics list (3.4), but you must be able to compare the others with it. BGP and IS-IS are not detailed (IS-IS: see CCNP Service Provider).

### 3. Distance vector vs link state

- **Distance vector** (invented in the early 1980s: RIP, Cisco's IGRP later updated to EIGRP): each router sends its **directly connected neighbors** its known destination networks and its **metric** to reach them. Called **"routing by rumor"**: the router only knows what its neighbors tell it. It learns only the **distance** (metric) and the **vector** (direction: the next hop). Example: R4 tells R2 "192.168.4.0/24 via me, metric 1"; R2 tells R1 "via me, metric 2"; R1 knows nothing more.
- **Link state**: each router advertises information about **its interfaces and connected networks**, passed along to all; every router builds the **same connectivity map** and **independently** calculates the best routes. More resources (CPU, memory) since more information is shared, but **faster** reaction to changes. Protocols: OSPF, IS-IS.

### 4. Metrics

- The **metric** measures how "far" the destination is; **lower is better**. Each protocol has its own:

| Protocol | Metric |
| :--- | :--- |
| **RIP** | **Hop count** (number of routers in the path); every link counts 1 regardless of speed (10 Mbps = 10 Gbps = one hop): primitive. |
| **EIGRP** | Calculation based on **bandwidth and delay** (by default; other factors configurable). Bandwidth of the **slowest** link in the path + **sum of the delay** values of all links; "delay" is a default value assigned to the interface based on its bandwidth. The most complicated of the IGPs. |
| **OSPF** | **Cost**, calculated from each link's **bandwidth**; the route metric is the total of the links' costs. |
| **IS-IS** | **Cost** too, but not calculated automatically: **10 by default** on all links, so without configuration it works like a hop count. |

- Example: R1 to 192.168.4.0/24 via R2 (Gigabit) or via R3 (R3-R4 link FastEthernet). With **RIP**, 2 hops either way: both routes enter the table, load balancing even over the slow path. With **OSPF**, the FastEthernet link costs more: only the route via R2 is kept.
- **ECMP (Equal Cost MultiPath)**: if a router learns via the **same protocol** several routes to **exactly the same destination** (same network address and prefix length) with the **same metric**, all are added and traffic is load-balanced. In `show ip route`, the brackets `[110/3]`: **left = AD, right = metric**. Also works with **static routes** (two `ip route` to the same destination: metric **0**, AD **1**).

### 5. Administrative Distance (AD)

- Metric compares routes from the **same protocol**; different protocols have incomparable metrics (OSPF 30 vs EIGRP 33280). The **AD** decides which protocol is **preferred**: **lower wins**, meaning a more "trustworthy" source. Cisco values (other vendors may differ):

| Source | AD |
| :--- | :--- |
| Connected | **0** |
| Static | **1** |
| eBGP (external BGP) | **20** |
| EIGRP | **90** |
| IGRP | **100** |
| OSPF | **110** |
| IS-IS | **115** |
| RIP | **120** |
| EIGRP external | **170** |
| iBGP (internal BGP) | **200** |
| Unusable | **255** ("the router does not believe the source of that route and does not install the route") |

- Decision order: **AD** first, then metric. Example: three routes to 10.1.1.0/24, RIP metric 5, RIP metric 3, OSPF metric 10 → the **OSPF** route (AD 110 < 120) enters the table.
- In `show ip route`, static routes show `[1/0]`; connected and local have AD 0 but it is not displayed; OSPF `[110/...]`.
- A protocol's AD can be changed (shown for OSPF later), a static route's too: `ip route <network> <mask> <next-hop> <AD>`; `?` says "distance metric", but this is the **AD**, not the metric.
- **Floating static route**: a static route whose AD is **higher** than the dynamic protocol's for the same destination (e.g. 111 > 110 for OSPF). It stays **inactive** (not in the table) while the dynamic route exists and takes over if it disappears (neighbor stops advertising, interface failure, adjacency lost). If the static AD stayed lower, it would be preferred, which is not what you want. In the exam topics list.

### 6. Exam traps

- **AD first, metric second.** Jeremy: "I would be surprised if you don't get a question like: OSPF and EIGRP routes to 10.0.0.0/24, which enters the table?" → **EIGRP (90 < 110)**. Memorize the AD table (flashcards).
- Routing by rumor = **distance vector**. Path vector = EGP (BGP). IGP is a category containing both distance vector and link state.
- RIP and EIGRP = distance vector; OSPF and IS-IS = link state; BGP = path vector.
- ECMP requires same destination, same protocol, same metric. With RIP, two 5-hop routes → both installed.
- Routes to **different prefixes** (10.20.0.0/22, /24, /26, /28) are not the same destination: all are in the table, and selection uses the **longest prefix match**, ignoring AD and metric (Boson question).
- `[AD/metric]` in `show ip route`; the word "metric" in `ip route ... ?` means AD.
- Codes: **O** = OSPF, **D** = EIGRP, **R** = RIP, **S** = static.

### 7. IOS commands

```
Router# show ip route                                       ! codes, [AD/metric], gateway of last resort
Router(config)# ip route 192.168.4.0 255.255.255.0 10.0.12.2       ! static route (AD 1, metric 0)
Router(config)# ip route 10.1.1.1 255.255.255.255 10.0.12.2        ! host route (/32)
Router(config)# ip route 192.168.4.0 255.255.255.0 10.0.12.2 100   ! static route with AD 100
Router(config)# ip route 10.0.2.0 255.255.255.0 203.0.113.1 111    ! floating static route (111 > OSPF's 110)
Router(config)# interface loopback 0                        ! virtual interface (seen in the lab, detailed later)
Router# traceroute 10.0.2.1                                 ! every Layer 3 hop replies (Windows: tracert)
```

### 8. The lab (video 050, Floating Static Routes)

Goal: Enterprise A, two LANs (10.0.1.0/24 on R1, 10.0.2.0/24 on R2), R1-R2 connected by fiber, each connected to ISP A (SPR1, SPR2: Service Provider Router) and ISP B (ISPBR1, ISPBR2). OSPF between R1 and R2. Configure floating static routes via ISP A as backup for the direct link.

1. **Routing tables**: on R1, `show ip route`: connected/local, static default route to 203.0.113.9 (ISPBR1), and **10.0.2.0/24 learned via OSPF (code O)**, Enterprise A's IGP. PC1 → SRV1 (10.0.2.1): most specific match = OSPF route via R2. PC1 → 1.1.1.1 ("Internet" server): only the default route matches → ISP B. R2: symmetrical, default to 203.0.113.13 (ISPBR2), OSPF to 10.0.1.0 via 10.0.0.1 (R1). Pings in realtime mode (for ARP) then in **simulation mode**: SRV1 via R1-R2, 1.1.1.1 via R1-ISPBR1. 1.1.1.1 is actually a **loopback interface** (Loopback0) on ISPBR1: a virtual interface, like an SVI, handy to simulate a remote destination in a lab (`show ip interface brief` on ISPBR1).
2. **Floating static routes**: R1: `ip route 10.0.2.0 255.255.255.0 203.0.113.1 111` (next hop SPR1 G0/0/0; `?` shows "distance metric" = AD; OSPF = 110 so 111). `do show ip route`: the route **does not appear**, the OSPF route (AD 110) is preferred. R2: `ip route 10.0.1.0 255.255.255.0 203.0.113.5 111` (SPR2), needed for return traffic. Same result.
3. **Failover test**: on R2, `interface g0/2/0`, `shutdown`: the OSPF route becomes invalid; `do show ip route`: **10.0.1.0/24 via 203.0.113.5 [111/0]** appears; same on R1. Ping PC1 → SRV1 in realtime (ARP redone on R1, SPR1, SPR2, R2; Packet Tracer "fast forward 30 s" button), then in simulation: both directions via **ISP A**.
4. **traceroute**: on a real network there is no simulation mode; `tracert 10.0.2.1` on the Windows PC (IOS: `traceroute`): every Layer 3 hop replies: 10.0.1.254 (R1 G0/1), 203.0.113.1 (SPR1), 192.168.1.2 (SPR2 G0/1/0), 203.0.113.6 (R2 G0/0/0), 10.0.2.1 (SRV1). Know it for the exam.

Boson NetSim preview ("Static Routes 2"): **serial** links (removed from the exam topics): the **DCE** side configures `clock rate 64000`, the DTE side does not; `hostname`, `ip address`, `no shutdown`, `ip route`, on NetSim PCs `ipconfig /ip <address> <mask>` and `ipconfig /dg <gateway>`, `ipconfig /all`; ping HostA → HostB; lab grading (red = missing command, blue = extra command).

### 9. The quiz (video 049: one mid-video question, 3 questions, plus one Boson ExSim question)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Mid-video. Routes to 10.1.1.0/24: via 192.168.1.1 RIP metric 5; via 192.168.2.1 RIP metric 3; via 192.168.3.1 OSPF metric 10. Which enters the table? | The **OSPF** route | AD is compared before metric: OSPF (110) beats RIP (120) whatever the metric. |
| Q1. R1 learns four routes to 192.168.1.0/24 via RIP, EIGRP, OSPF, IS-IS: which enter the table? | **B, the EIGRP route only** | Lowest AD (90). "Both distance vector", "both link state" or "all" ignore AD. |
| Q2. Which type of routing protocol is known as "routing by rumor"? | **C, distance vector** | Routers only know what neighbors advertise (routes + metrics). Link state: full map; path vector: an EGP, not in the CCNA; IGP: category covering both. |
| Q3. R1 learns two RIP routes to 172.16.0.0/16, via 10.0.0.1 and 10.1.0.1, both 5 hops: which enter? | **A, both** | Same destination, same protocol, same metric → ECMP. D would be true only if a competing OSPF route existed. |
| Boson ExSim. `show ip route` shows S 10.20.0.0/22, R /24, D /26, O /28; packet for 10.20.0.14: which route? | **B, the OSPF route, longest prefix match** | Different destinations (different prefixes): AD and metric are irrelevant, the router uses the most specific match (/28), to 192.168.10.1 out Serial0/1. |
