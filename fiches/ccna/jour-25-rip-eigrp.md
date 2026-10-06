# CCNA Day 25 : RIP & EIGRP

> Source : Jeremy's IT Lab, « Free CCNA | RIP & EIGRP | Day 25 » (cours, 44 min, vidéo n°51 de la playlist) et « Configuring EIGRP | Day 25 Lab » (lab mi-lab mi-cours, 26 min, vidéo n°52 : métrique EIGRP, successor, feasible successor, unequal-cost load balancing). Ni RIP ni EIGRP ne sont dans la liste des sujets d'examen, mais « other related topics may also appear » ; les configurations servent surtout à préparer OSPF. Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. RIP (Routing Information Protocol)

- Standard (pas propriétaire Cisco), IGP **distance vector** (routing by rumor). Métrique : **hop count**, chaque routeur = 1 saut, bande passante ignorée. **Maximum 15 sauts** : au-delà, destination injoignable, route non installée → inutilisable dans les grands réseaux. Quasi jamais utilisé en production, mais simple pour les petits réseaux et les labs.
- Trois versions : **RIPv1** et **RIPv2** (IPv4), **RIPng** (RIP Next Generation, IPv6, non couvert).
- Deux types de messages : **Request** (demande aux voisins RIP d'envoyer leur table de routage) et **Response** (envoie sa table aux voisins). Par défaut, un routeur RIP partage sa table **toutes les 30 secondes**, ce qui peut encombrer un réseau avec beaucoup de routeurs.
- **RIPv1** : très ancien ; n'annonce que des **adresses classful** (A, B, C), pas de VLSM ni CIDR, **n'inclut pas le masque** dans ses annonces (classe A → /8, B → /16, C → /24 : 10.1.1.0/24 devient 10.0.0.0, 172.16.192.0/18 devient 172.16.0.0, 192.168.1.4/30 devient 192.168.1.0). Messages en **broadcast 255.255.255.255**.
- **RIPv2** : supporte **VLSM et CIDR**, inclut le masque dans les annonces (un /30 est annoncé en /30). Messages en **multicast 224.0.0.9** (classe D). Broadcast = tous les équipements du réseau local ; multicast = seulement ceux qui ont rejoint le groupe (détails au niveau CCIE).

### 2. Configuration de RIP (introduction aux mécanismes d'OSPF)

- `router rip` : invite `(config-router)#`. **Toujours** `version 2` et `no auto-summary` (auto-summary est actif par défaut et convertit les réseaux annoncés en réseaux classful : 172.16.1.0/28 serait annoncé 172.16.0.0/16).
- **`network`** : la commande est **classful** (`network 10.0.12.0` devient 10.0.0.0, pas de masque à saisir). Elle **ne dit pas quel réseau annoncer** : elle demande au routeur de chercher les interfaces dont l'adresse IP est dans la plage indiquée, d'**activer RIP sur ces interfaces**, de former des adjacences avec les voisins RIP connectés, et d'**annoncer le préfixe réel de l'interface** (10.0.12.0/30 et 10.0.13.0/30, pas 10.0.0.0/8 ; 172.16.1.0/28, pas 172.16.0.0/16). Même logique pour EIGRP et OSPF, avec quelques différences.
- **`passive-interface g2/0`** (depuis le mode RIP, pas sur l'interface) : arrête l'envoi des annonces RIP par cette interface (sans voisin RIP, c'est du trafic inutile), mais le préfixe de l'interface **reste annoncé** aux voisins. Recommandé sur toute interface sans voisin. Même commande en EIGRP et OSPF.
- **`default-information originate`** : annonce la route par défaut du routeur (ici vers Internet, « Gateway of last resort is 203.0.113.2 to network 0.0.0.0 ») à ses voisins RIP, qui la relaient. Sur R4, deux routes par défaut (via R3 FastEthernet et via R2 Gigabit) avec le même hop count : load balancing malgré la différence de vitesse. Même commande en OSPF.
- **`show ip protocols`** (RIP, EIGRP, OSPF) : protocole, timers (détaillés pour OSPF), version 2, « Automatic network summarization is not in effect », **Maximum paths 4** (ECMP sur 4 chemins par défaut ; `maximum-paths <1-32>`, même commande pour EIGRP/OSPF), les réseaux des commandes `network`, les interfaces passives, les **Routing Information Sources** (voisins 10.0.12.2 et 10.0.13.2), **Distance 120** (`distance <1-255>` pour changer l'AD, ex. 85 pour préférer RIP à EIGRP ; même commande pour EIGRP/OSPF).

### 3. EIGRP (Enhanced Interior Gateway Routing Protocol)

- Version améliorée d'IGRP. Était propriétaire Cisco ; Cisco l'a publié en partie, mais peu de constructeurs l'implémentent : en pratique **Cisco seulement**. Distance vector « **avancé** » ou « **hybride** ». Bien plus rapide que RIP, **pas de limite de 15 sauts** (grands réseaux). Multicast **224.0.0.10**.
- **Seul IGP capable d'unequal-cost load balancing** ; par défaut ECMP sur 4 chemins comme RIP, configurable pour répartir le trafic **proportionnellement** à la bande passante (plus sur les chemins à métrique basse).
- Moins utilisé qu'OSPF à cause de la limite Cisco, d'où le choix d'OSPF pour le CCNA.
- **Configuration** : `router eigrp <AS>` ; le **numéro d'AS doit correspondre** entre routeurs, sinon pas d'adjacence. `no auto-summary` (activé ou non par défaut selon la version d'IOS ; le désactiver). `passive-interface`. `network 10.0.0.0` : classful si pas de masque (10.0.0.0/8) ; avec masque : **wildcard mask**, ex. `network 172.16.1.0 0.0.0.15`.
- **Wildcard mask** = masque de sous-réseau **inversé** (les 1 deviennent 0 et inversement) : 255.255.255.0 → 0.0.0.255 (/24) ; 255.255.0.0 → 0.0.255.255 (/16) ; 255.0.0.0 → 0.255.255.255 (/8) ; 255.255.255.240 → **0.0.0.15** (/28) ; /25 → 0.0.0.127 ; /14 → 0.3.255.255 ; /19 → 0.0.31.255 ; /21 → 0.0.7.255 ; **/32 → 0.0.0.0**. Raccourci : **255 moins chaque octet** du masque. Un bit **0** du wildcard = le bit **doit correspondre** entre l'IP de l'interface et la commande ; un bit **1** = indifférent. Exemples avec l'interface 172.16.1.14 : `network 172.16.1.0 0.0.0.15` (28 bits) → match ; `network 172.16.1.0 0.0.0.7` (29 bits) → **pas de match** ; `network 172.16.1.8 0.0.0.7` → match ; `network 168.0.0.0 7.255.255.255` (5 bits, 10101) → match. En pratique on utilise le préfixe de l'interface, ou /32 (0.0.0.0) avec l'adresse exacte. Le raccourci de lab `network 0.0.0.0 255.255.255.255` active EIGRP sur **toutes** les interfaces (déconseillé en production). OSPF utilise aussi les wildcard masks.
- `show ip protocols` avec EIGRP : « Routing protocol is EIGRP 1 » (AS) ; **valeurs K** : **K1 = 1 (bande passante), K3 = 1 (délai)**, **K2, K4, K5 = 0** par défaut ; **router ID** ; auto-summary ; maximum paths 4 ; réseaux ; interfaces passives ; voisins ; **Distance : internal 90, external 170** (routes externes = injectées dans EIGRP depuis l'extérieur, niveau CCNP).
- **Router ID** (EIGRP et OSPF) : identifie le routeur dans l'AS. Ordre de priorité : **1) configuration manuelle** (`eigrp router-id 1.1.1.1`), **2) adresse IP la plus haute d'une interface loopback**, **3) adresse IP la plus haute d'une interface physique** (ici 172.16.1.14 de G2/0). Ce n'est pas une adresse IP, juste un **nombre de 32 bits** écrit en décimal pointé.
- Table de routage : routes EIGRP indiquées par **D** (pas E) ; métriques très grandes (3072, 3328, 28416, 156 416...), plus difficiles à lire qu'en OSPF.

### 4. Métrique EIGRP, successor, feasible successor, variance (lab 052)

- Formule avec K1 à K5 (pas à mémoriser) ; retenir **métrique = bande passante du lien le plus lent du chemin + délais de tous les liens** ; le délai n'est pas mesuré par des pings, c'est une valeur par défaut selon la bande passante de l'interface.
- **Feasible distance (FD)** : métrique de **ce routeur** vers la destination. **Reported distance (RD)**, aussi **advertised distance** : métrique du **voisin** vers la destination. Sans rapport avec l'administrative distance. Dans `show ip eigrp topology`, pour chaque route : `(FD/RD)`, gauche = FD, droite = RD.
- **Successor** : la route avec la **métrique la plus basse** (la meilleure) ; plusieurs successors possibles si FD égales (ECMP).
- **Feasible successor** : route alternative qui respecte la **condition de faisabilité** : **sa reported distance est inférieure à la feasible distance du successor**. Exemple R1 → 192.168.4.0/24 : via R2 FD 28 672 (successor) ; via R3 RD 28 416 < 28 672 → feasible successor. Mécanisme de **prévention des boucles** : une route faisable est garantie sans boucle.
- **Unequal-cost load balancing** : `show ip protocols` affiche « EIGRP maximum metric variance 1 » par défaut (ECMP seulement). `variance 2` (mode EIGRP) = multiplicateur : les feasible successors dont la **FD ≤ 2 × FD du successor** entrent dans la table. 28 672 × 2 = 57 344 ; FD via R3 = 30 976 < 57 344 → les deux routes sont installées, avec un peu plus de trafic via R2 (métrique plus basse). **Seuls les feasible successors** peuvent être utilisés, quelle que soit la variance.

### 5. Pièges d'examen

- RIPv1 broadcast 255.255.255.255 ; RIPv2 multicast **224.0.0.9** ; EIGRP multicast **224.0.0.10**.
- RIP : 15 sauts max, mise à jour toutes les 30 s ; AD 120. EIGRP : AD **90 interne, 170 externe** ; code **D** dans la table.
- La commande `network` **active le protocole sur des interfaces**, elle n'annonce pas le réseau saisi.
- `default-information originate` se fait sur le routeur **qui possède** la route par défaut, en mode config-router.
- Router ID : **manuel > loopback la plus haute > interface physique la plus haute**.
- Wildcard : seuls les bits à 0 doivent correspondre ; `network 128.0.0.0 127.255.255.255` ne vérifie que le premier bit.
- Feasibility condition : **RD du candidat < FD du successor**. FD/RD sont des métriques, pas des AD.
- EIGRP est le seul IGP à faire de l'unequal-cost load balancing (variance), et uniquement sur des feasible successors.
- L'AD sert quand plusieurs routes vers la **même** destination viennent de protocoles **différents** ; même protocole → métrique ; destinations différentes → toutes installées (question Boson).

### 6. Commandes IOS

```
Router(config)# router rip                               ! mode config-router
Router(config-router)# version 2                         ! toujours RIPv2
Router(config-router)# no auto-summary                   ! annoncer les vrais préfixes, pas les réseaux classful
Router(config-router)# network 10.0.0.0                  ! classful : active RIP sur les interfaces en 10.x.x.x
Router(config-router)# passive-interface g2/0            ! plus d'annonces envoyées par G2/0, préfixe toujours annoncé
Router(config-router)# default-information originate     ! partager la route par défaut avec les voisins
Router(config-router)# maximum-paths 8                   ! chemins ECMP (1 à 32, défaut 4)
Router(config-router)# distance 85                       ! changer l'AD du protocole (1 à 255)
Router(config)# router eigrp 100                         ! AS 100, doit correspondre entre voisins
Router(config-router)# network 10.0.13.0 0.0.0.3         ! wildcard mask /30
Router(config-router)# network 3.3.3.3 0.0.0.0           ! wildcard /32 : l'adresse exacte (loopback)
Router(config-router)# network 0.0.0.0 255.255.255.255   ! toutes les interfaces (lab seulement)
Router(config-router)# eigrp router-id 1.1.1.1           ! router ID manuel
Router(config-router)# variance 2                        ! unequal-cost load balancing (FD jusqu'à 2 x successor)
Router(config)# interface loopback 0                     ! (ou interface l0) interface virtuelle, toujours up
Router(config-if)# ip address 1.1.1.1 255.255.255.255    ! masque /32 courant pour une loopback
Router# show ip protocols                                ! version, K values, router ID, auto-summary, max paths, réseaux, passives, voisins, AD, variance
Router# show ip eigrp neighbors                          ! voisins EIGRP (équivalent en OSPF)
Router# show ip eigrp topology                           ! toutes les routes apprises, (FD/RD), successors et feasible successors
Router# show ip route eigrp                              ! routes EIGRP seulement (aussi : connected, static)
```

### 7. Le lab (vidéo 052, Configuring EIGRP)

Objectif : quatre routeurs en **AS 100**, R1-R2 en Gigabit, les autres liens en FastEthernet, LAN 192.168.4.0/24 sur R4 ; loopbacks, EIGRP, puis étude de la métrique.

1. Hostnames, adresses IP, interfaces activées (préconfigurés dans la vidéo, à faire soi-même dans le fichier).
2. **Loopbacks** : `interface loopback 0` (ou `interface l0`), message « interface came up » immédiat ; `ip address 1.1.1.1 255.255.255.255` (/32 habituel) ; `show ip interface brief` : Loopback0 up/up, toujours up sauf `shutdown`. 2.2.2.2 sur R2, 3.3.3.3 sur R3, 4.4.4.4 sur R4.
3. **EIGRP** : R4 (depuis le mode interface, `router eigrp 100` fonctionne directement) : `network 0.0.0.0 255.255.255.255` (raccourci), `show ip protocols` → « Automatic network summarization is in effect » → `no auto-summary` ; `passive-interface g0/0` (LAN sans voisin) et `passive-interface l0` (le routeur enverrait sinon des messages EIGRP par la loopback : gaspillage). R3 : `network 10.0.13.0 0.0.0.3`, `network 10.0.34.0 0.0.0.3`, `network 3.3.3.3 0.0.0.0`, `no auto-summary`, `passive-interface l0`. R2 et R1 : idem avec leurs préfixes (adjacences formées quasi instantanément). Vérifications sur R1 : `show ip protocols` (voisins listés), `show ip eigrp neighbors`, `show ip route eigrp` (code D : loopbacks 2.2.2.2, 3.3.3.3, 4.4.4.4, 10.0.24.0, 10.0.34.0, 192.168.4.0/24 ; métrique 156 416 vers 4.4.4.4), `show ip eigrp topology` (deux routes vers 192.168.4.0/24, une seule dans la table : via R2, lien Gigabit).
4. **Métrique et variance** (partie cours, section 4 ci-dessus) : `variance 2` sur R1 → `show ip route` montre les deux routes vers 192.168.4.0/24 avec des métriques différentes.

Question Boson ExSim (à la place de NetSim) : glisser-déposer des quatre termes : **successor** = « the best path to a destination network » ; **feasible successor** = « a backup path that is guaranteed to be loop free » ; **advertised distance** = « the metric that the next hop router has calculated » ; **feasible distance** = « the best metric along a path ».

### 8. Le quiz (vidéo 051 : 3 questions, plus une question Boson ExSim)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Q1. R1 et R2 en RIP ; R1 a une route par défaut vers Internet à annoncer à R2 : quelle commande ? | **A, sur R1 en config-router : `default-information originate`** | `network 203.0.113.0` active RIP sur une interface ; `ip route 0.0.0.0 0.0.0.0 10.0.12.1` sur R2 crée une route locale mais ne fait rien annoncer par R1 ; la commande sur R2 (D) annoncerait dans le mauvais sens. |
| Q2. G1/0 = 172.20.20.17, G2/0 = 172.26.20.12 : quelle commande `network` active EIGRP sur les deux ? | **A, `network 128.0.0.0 127.255.255.255`** | Seul le premier bit du wildcard est 0 : seul le premier bit doit correspondre, et il vaut 1 dans la commande et dans les deux adresses. |
| Q3. Ordre de priorité du router ID EIGRP ? | **D, configuration manuelle, puis loopback la plus haute, puis interface physique la plus haute** | Les autres ordres inversent la priorité. |
| Boson ExSim. Dans quelle situation le routeur utilise-t-il l'AD pour choisir une route ? | **D, plusieurs routes vers la même destination reçues de protocoles différents** | A et C : destinations différentes → toutes installées ; B : même protocole → même AD, c'est la métrique qui tranche. |

---

## 🇬🇧 English version

### 1. RIP (Routing Information Protocol)

- Industry standard (not Cisco proprietary), **distance vector** IGP (routing by rumor). Metric: **hop count**, each router = one hop, bandwidth irrelevant. **Maximum 15 hops**: beyond that the destination is unreachable and the route is not installed → unusable in large networks. Almost never used in production, but simple for small networks and labs.
- Three versions: **RIPv1** and **RIPv2** (IPv4), **RIPng** (RIP Next Generation, IPv6, not covered).
- Two message types: **Request** (asks RIP neighbors to send their routing table) and **Response** (sends the local routing table to neighbors). By default a RIP router shares its table **every 30 seconds**, which can clog a network with many routers.
- **RIPv1**: very old; only advertises **classful** addresses (A, B, C), no VLSM or CIDR, **does not include the subnet mask** in advertisements (class A → /8, B → /16, C → /24: 10.1.1.0/24 becomes 10.0.0.0, 172.16.192.0/18 becomes 172.16.0.0, 192.168.1.4/30 becomes 192.168.1.0). Messages **broadcast to 255.255.255.255**.
- **RIPv2**: supports **VLSM and CIDR**, includes the mask in advertisements (a /30 is advertised as /30). Messages **multicast to 224.0.0.9** (class D). Broadcast = all devices on the local network; multicast = only devices that joined the group (details at CCIE level).

### 2. RIP configuration (an introduction to OSPF mechanics)

- `router rip`: prompt `(config-router)#`. **Always** `version 2` and `no auto-summary` (auto-summary is on by default and converts advertised networks to classful ones: 172.16.1.0/28 would be advertised as 172.16.0.0/16).
- **`network`**: the command is **classful** (`network 10.0.12.0` becomes 10.0.0.0, no mask to enter). It **does not say which network to advertise**: it tells the router to look for interfaces whose IP address falls in the range, **activate RIP on those interfaces**, form adjacencies with connected RIP neighbors, and **advertise the interface's actual prefix** (10.0.12.0/30 and 10.0.13.0/30, not 10.0.0.0/8; 172.16.1.0/28, not 172.16.0.0/16). Same logic for EIGRP and OSPF, with a few differences.
- **`passive-interface g2/0`** (from RIP mode, not on the interface): stops sending RIP advertisements out of that interface (with no RIP neighbor it is wasted traffic), but the interface prefix is **still advertised** to neighbors. Recommended on every interface without a neighbor. Same command in EIGRP and OSPF.
- **`default-information originate`**: advertises the router's default route (here to the Internet, "Gateway of last resort is 203.0.113.2 to network 0.0.0.0") to its RIP neighbors, which pass it on. On R4, two default routes (via R3 FastEthernet and via R2 Gigabit) with the same hop count: load balancing despite the speed difference. Same command in OSPF.
- **`show ip protocols`** (RIP, EIGRP, OSPF): protocol, timers (detailed for OSPF), version 2, "Automatic network summarization is not in effect", **Maximum paths 4** (ECMP over 4 paths by default; `maximum-paths <1-32>`, same for EIGRP/OSPF), the networks from the `network` commands, passive interfaces, **Routing Information Sources** (neighbors 10.0.12.2 and 10.0.13.2), **Distance 120** (`distance <1-255>` to change the AD, e.g. 85 to prefer RIP over EIGRP; same for EIGRP/OSPF).

### 3. EIGRP (Enhanced Interior Gateway Routing Protocol)

- Improved version of IGRP. Was Cisco proprietary; Cisco partly published it, but few vendors implement it: practically **Cisco only**. "**Advanced**" or "**hybrid**" distance vector. Much faster than RIP, **no 15-hop limit** (large networks). Multicast **224.0.0.10**.
- **The only IGP that can do unequal-cost load balancing**; by default ECMP over 4 paths like RIP, configurable to split traffic **in proportion** to bandwidth (more over lower-metric paths).
- Less used than OSPF because of the Cisco limitation, hence OSPF as the CCNA focus.
- **Configuration**: `router eigrp <AS>`; the **AS number must match** between routers or no adjacency forms. `no auto-summary` (enabled or not by default depending on IOS version; disable it). `passive-interface`. `network 10.0.0.0`: classful if no mask (10.0.0.0/8); with a mask: **wildcard mask**, e.g. `network 172.16.1.0 0.0.0.15`.
- **Wildcard mask** = **inverted** subnet mask (1s become 0s and vice versa): 255.255.255.0 → 0.0.0.255 (/24); 255.255.0.0 → 0.0.255.255 (/16); 255.0.0.0 → 0.255.255.255 (/8); 255.255.255.240 → **0.0.0.15** (/28); /25 → 0.0.0.127; /14 → 0.3.255.255; /19 → 0.0.31.255; /21 → 0.0.7.255; **/32 → 0.0.0.0**. Shortcut: **255 minus each octet** of the mask. A **0** bit in the wildcard = the bit **must match** between the interface IP and the command; a **1** bit = does not matter. Examples with interface 172.16.1.14: `network 172.16.1.0 0.0.0.15` (28 bits) → match; `network 172.16.1.0 0.0.0.7` (29 bits) → **no match**; `network 172.16.1.8 0.0.0.7` → match; `network 168.0.0.0 7.255.255.255` (5 bits, 10101) → match. In practice use the interface's prefix, or /32 (0.0.0.0) with the exact address. The lab shortcut `network 0.0.0.0 255.255.255.255` activates EIGRP on **all** interfaces (not recommended in production). OSPF also uses wildcard masks.
- `show ip protocols` with EIGRP: "Routing protocol is EIGRP 1" (AS); **K values**: **K1 = 1 (bandwidth), K3 = 1 (delay)**, **K2, K4, K5 = 0** by default; **router ID**; auto-summary; maximum paths 4; networks; passive interfaces; neighbors; **Distance: internal 90, external 170** (external routes = injected into EIGRP from outside, CCNP level).
- **Router ID** (EIGRP and OSPF): identifies the router within the AS. Priority order: **1) manual configuration** (`eigrp router-id 1.1.1.1`), **2) highest IP address on a loopback interface**, **3) highest IP address on a physical interface** (here 172.16.1.14 on G2/0). It is not an IP address, just a **32-bit number** written in dotted decimal.
- Routing table: EIGRP routes marked **D** (not E); very large metrics (3072, 3328, 28416, 156,416...), harder to read than OSPF.

### 4. EIGRP metric, successor, feasible successor, variance (lab 052)

- Formula with K1 to K5 (no need to memorise); remember **metric = bandwidth of the slowest link in the path + delay of all links**; delay is not measured with pings, it is a default value based on interface bandwidth.
- **Feasible distance (FD)**: **this router's** metric to the destination. **Reported distance (RD)**, also **advertised distance**: the **neighbor's** metric to the destination. Unrelated to administrative distance. In `show ip eigrp topology`, each route shows `(FD/RD)`, left = FD, right = RD.
- **Successor**: the route with the **lowest metric** (the best); several successors possible with equal FDs (ECMP).
- **Feasible successor**: an alternate route meeting the **feasibility condition**: **its reported distance is lower than the successor's feasible distance**. Example R1 → 192.168.4.0/24: via R2 FD 28,672 (successor); via R3 RD 28,416 < 28,672 → feasible successor. A **loop-prevention** mechanism: a feasible route is guaranteed loop-free.
- **Unequal-cost load balancing**: `show ip protocols` shows "EIGRP maximum metric variance 1" by default (ECMP only). `variance 2` (EIGRP mode) = multiplier: feasible successors whose **FD ≤ 2 × the successor's FD** enter the table. 28,672 × 2 = 57,344; FD via R3 = 30,976 < 57,344 → both routes installed, with slightly more traffic via R2 (lower metric). **Only feasible successors** can be used, whatever the variance.

### 5. Exam traps

- RIPv1 broadcast 255.255.255.255; RIPv2 multicast **224.0.0.9**; EIGRP multicast **224.0.0.10**.
- RIP: 15 hops max, updates every 30 s; AD 120. EIGRP: AD **90 internal, 170 external**; code **D** in the table.
- The `network` command **activates the protocol on interfaces**, it does not advertise the network typed.
- `default-information originate` goes on the router **that has** the default route, in config-router mode.
- Router ID: **manual > highest loopback > highest physical interface**.
- Wildcard: only the 0 bits must match; `network 128.0.0.0 127.255.255.255` checks only the first bit.
- Feasibility condition: **candidate's RD < successor's FD**. FD/RD are metrics, not ADs.
- EIGRP is the only IGP doing unequal-cost load balancing (variance), and only over feasible successors.
- AD is used when several routes to the **same** destination come from **different** protocols; same protocol → metric; different destinations → all installed (Boson question).

### 6. IOS commands

```
Router(config)# router rip                               ! config-router mode
Router(config-router)# version 2                         ! always RIPv2
Router(config-router)# no auto-summary                   ! advertise real prefixes, not classful networks
Router(config-router)# network 10.0.0.0                  ! classful: activates RIP on interfaces in 10.x.x.x
Router(config-router)# passive-interface g2/0            ! no more advertisements out G2/0, prefix still advertised
Router(config-router)# default-information originate     ! share the default route with neighbors
Router(config-router)# maximum-paths 8                   ! ECMP paths (1 to 32, default 4)
Router(config-router)# distance 85                       ! change the protocol's AD (1 to 255)
Router(config)# router eigrp 100                         ! AS 100, must match between neighbors
Router(config-router)# network 10.0.13.0 0.0.0.3         ! /30 wildcard mask
Router(config-router)# network 3.3.3.3 0.0.0.0           ! /32 wildcard: the exact address (loopback)
Router(config-router)# network 0.0.0.0 255.255.255.255   ! all interfaces (labs only)
Router(config-router)# eigrp router-id 1.1.1.1           ! manual router ID
Router(config-router)# variance 2                        ! unequal-cost load balancing (FD up to 2 x successor)
Router(config)# interface loopback 0                     ! (or interface l0) virtual interface, always up
Router(config-if)# ip address 1.1.1.1 255.255.255.255    ! /32 mask common for a loopback
Router# show ip protocols                                ! version, K values, router ID, auto-summary, max paths, networks, passives, neighbors, AD, variance
Router# show ip eigrp neighbors                          ! EIGRP neighbors (OSPF has an equivalent)
Router# show ip eigrp topology                           ! all learned routes, (FD/RD), successors and feasible successors
Router# show ip route eigrp                              ! EIGRP routes only (also: connected, static)
```

### 7. The lab (video 052, Configuring EIGRP)

Goal: four routers in **AS 100**, R1-R2 Gigabit, other links FastEthernet, LAN 192.168.4.0/24 on R4; loopbacks, EIGRP, then a study of the metric.

1. Hostnames, IP addresses, interfaces enabled (pre-configured in the video, to do yourself in the file).
2. **Loopbacks**: `interface loopback 0` (or `interface l0`), immediate "interface came up" message; `ip address 1.1.1.1 255.255.255.255` (/32 is usual); `show ip interface brief`: Loopback0 up/up, always up unless `shutdown`. 2.2.2.2 on R2, 3.3.3.3 on R3, 4.4.4.4 on R4.
3. **EIGRP**: R4 (`router eigrp 100` works directly from interface mode): `network 0.0.0.0 255.255.255.255` (shortcut), `show ip protocols` → "Automatic network summarization is in effect" → `no auto-summary`; `passive-interface g0/0` (LAN with no neighbor) and `passive-interface l0` (otherwise the router would send EIGRP messages out of the loopback: wasted resources). R3: `network 10.0.13.0 0.0.0.3`, `network 10.0.34.0 0.0.0.3`, `network 3.3.3.3 0.0.0.0`, `no auto-summary`, `passive-interface l0`. R2 and R1: same with their prefixes (adjacencies form almost instantly). Checks on R1: `show ip protocols` (neighbors listed), `show ip eigrp neighbors`, `show ip route eigrp` (code D: loopbacks 2.2.2.2, 3.3.3.3, 4.4.4.4, 10.0.24.0, 10.0.34.0, 192.168.4.0/24; metric 156,416 to 4.4.4.4), `show ip eigrp topology` (two routes to 192.168.4.0/24, only one in the table: via R2, Gigabit link).
4. **Metric and variance** (lecture part, section 4 above): `variance 2` on R1 → `show ip route` shows both routes to 192.168.4.0/24 with different metrics.

Boson ExSim question (instead of NetSim): drag and drop the four terms: **successor** = "the best path to a destination network"; **feasible successor** = "a backup path that is guaranteed to be loop free"; **advertised distance** = "the metric that the next hop router has calculated"; **feasible distance** = "the best metric along a path".

### 8. The quiz (video 051: 3 questions, plus one Boson ExSim question)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Q1. R1 and R2 use RIP; R1 has a default route to the Internet to advertise to R2: which command? | **A, on R1 in config-router mode: `default-information originate`** | `network 203.0.113.0` activates RIP on an interface; `ip route 0.0.0.0 0.0.0.0 10.0.12.1` on R2 creates a local route but makes R1 advertise nothing; the command on R2 (D) would advertise in the wrong direction. |
| Q2. G1/0 = 172.20.20.17, G2/0 = 172.26.20.12: which `network` command activates EIGRP on both? | **A, `network 128.0.0.0 127.255.255.255`** | Only the first wildcard bit is 0: only the first bit must match, and it is 1 in the command and in both addresses. |
| Q3. Priority order for the EIGRP router ID? | **D, manual configuration, then highest loopback, then highest physical interface** | The other orders reverse the priority. |
| Boson ExSim. In which situation does a router use AD values for route selection? | **D, multiple routes to the same destination received from different routing protocols** | A and C: different destinations → all installed; B: same protocol → same AD, the metric decides. |
