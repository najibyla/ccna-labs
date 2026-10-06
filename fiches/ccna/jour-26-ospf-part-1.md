# CCNA Day 26 : OSPF Part 1 / OSPF partie 1

> Source : Jeremy's IT Lab, « Free CCNA | OSPF Part 1 | Day 26 » (cours, 40 min, vidéo n°53 de la playlist, sujet d'examen 3.4 « Configure and verify single area OSPFv2 » : neighbor adjacencies, point-to-point, broadcast, router ID) et « Configuring OSPF (1) | Day 26 Lab » (lab, 22 min, vidéo n°54). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Les bases d'OSPF

- **OSPF (Open Shortest Path First)** : protocole **link state**. Utilise l'algorithme **Shortest Path First**, créé par le chercheur néerlandais **Edsger Dijkstra**, dit **algorithme de Dijkstra** (question d'examen possible).
- Trois versions : **OSPFv1** (1989, plus utilisée), **OSPFv2** (1998, **IPv4**, la version de l'examen et de ces vidéos), **OSPFv3** (développée pour **IPv6**, utilisable aussi en IPv4 mais v2 reste la plus courante).
- Les routeurs stockent les informations sur le réseau dans des **LSA (Link State Advertisements)**, organisées dans la **LSDB (Link State Database)**. Les routeurs **inondent (flood)** les LSA (envoi à tous leurs voisins OSPF) jusqu'à ce que tous les routeurs de l'**aire (area)** aient la **même LSDB**, la même carte du réseau.
- Exemple : OSPF activé sur G1/0 de R4 → R4 crée une LSA contenant son **router ID** (RID, ici 4.4.4.4 : loopback ou configuration manuelle), le réseau 192.168.4.0/24 et son **coût** (1 pour une interface GigabitEthernet, détaillé au Day 27) ; la LSA est inondée à tout le réseau et ajoutée à la LSDB de chaque routeur ; chaque routeur exécute l'algorithme SPF pour calculer sa meilleure route. Chaque LSA a un **timer de vieillissement de 30 minutes** par défaut, après quoi elle est inondée à nouveau.
- **Trois étapes** : 1) devenir **voisins** (neighbors) avec les routeurs du même segment ; 2) **échanger les LSA** ; 3) **calculer** indépendamment les meilleures routes et les insérer dans la table de routage.

### 2. Les aires OSPF

- Un petit réseau (4 routeurs) fonctionne très bien en **aire unique (single-area)**. Dans un grand réseau (500 routeurs, 1000 sous-réseaux), une aire unique pose problème : calcul SPF plus long et **exponentiellement** plus coûteux en CPU, LSDB énorme en mémoire, et chaque petit changement (une interface activée) inonde tous les routeurs et relance le calcul SPF partout. On divise donc le réseau en plusieurs aires. L'examen ne demande que l'aire unique, mais il faut connaître les termes et règles :
  - **Aire (area)** : ensemble de routeurs et de liens qui **partagent la même LSDB** ; chaque aire a sa LSDB.
  - **Aire backbone = area 0** : aire spéciale à laquelle **toutes les autres aires doivent se connecter**.
  - **Internal router** : toutes ses interfaces dans la même aire.
  - **ABR (Area Border Router)** : interfaces dans **plusieurs aires** ; maintient une LSDB **par aire** ; recommandé : **2 aires maximum** par ABR (3 ou plus surcharge le routeur).
  - **Backbone router** : routeur avec au moins une interface dans l'aire 0 (y compris les ABR).
  - **Intra-area route** : destination dans la même aire ; **interarea route** : destination dans une autre aire.
- **Trois règles** : 1) les aires doivent être **contiguës** (une aire coupée en deux morceaux est interdite : faire du second morceau une autre aire) ; 2) chaque aire doit avoir **au moins un ABR connecté à l'aire 0** (une aire 1 reliée seulement à l'aire 2 est interdite) ; 3) **les interfaces OSPF d'un même sous-réseau doivent être dans la même aire**, sinon elles ne deviennent pas voisines.

### 3. Configuration de base

- `router ospf <process ID>` : le **process ID est localement significatif** (un routeur peut exécuter plusieurs processus OSPF ; des routeurs avec des process ID différents **deviennent voisins**, contrairement à l'AS EIGRP) ; sans rapport avec le numéro d'aire. Généralement 1.
- `network <adresse> <wildcard> area <n>` : sans `area`, « Incomplete command ». **Wildcard mask** comme en EIGRP (Day 25). Même fonction qu'en RIP/EIGRP : chercher les interfaces dont l'IP est dans la plage, **activer OSPF dessus dans l'aire indiquée**, former des voisinages, annoncer le préfixe de l'interface. Ne dit pas « annonce ce réseau ». En aire unique, n'importe quel numéro d'aire est possible, mais **area 0 est la bonne pratique**.
- `passive-interface g2/0` : plus de **messages Hello** envoyés par l'interface (les Hello servent à se présenter aux voisins, Day 27), mais le sous-réseau de l'interface est **toujours annoncé** dans les LSA. À utiliser sur toute interface sans voisin OSPF.
- `default-information originate` : annonce la route par défaut (ex. vers l'ISP 203.0.113.2) en créant une nouvelle LSA inondée à tous ; R2, R3, R4 ajoutent la route par défaut via R1. Le routeur devient un **ASBR (Autonomous System Boundary Router)** : il relie le domaine OSPF à un réseau externe (Internet).
- **Router ID** : même ordre qu'EIGRP : **1) configuration manuelle, 2) IP la plus haute d'une loopback, 3) IP la plus haute d'une interface physique**. Commande `router-id 1.1.1.1` (pas `eigrp router-id`) ; message « Reload or use "clear ip ospf process" command, for this to take effect ». `clear ip ospf process` (mode privilégié, répondre `yes` ; le `[no]` entre crochets est le choix par défaut) réinitialise OSPF : mauvaise idée en production (perte temporaire des routes OSPF), sans problème en lab.
- `show ip protocols` : « Routing protocol is ospf 1 », router ID, « It is an autonomous system boundary router » (après default-information originate), « Number of areas in this router is 1. 1 normal 0 stub 0 nssa » (types d'aires hors programme), **Maximum path 4** (OSPF ne fait **pas** d'unequal-cost load balancing, seulement ECMP, `maximum-paths` pour changer), Routing for Networks (les commandes network), passive interfaces, Routing Information Sources (router ID des voisins, ici les loopbacks 2.2.2.2 etc.), **Distance 110** (`distance 85` pour préférer OSPF à EIGRP).

### 4. Pièges d'examen

- L'aire unique **n'est pas obligée** d'utiliser l'aire 0 (bonne pratique seulement) ; le process ID **n'a pas** à correspondre au numéro d'aire ni entre routeurs.
- Toute aire non-backbone doit avoir un ABR vers l'aire 0 ; un ASBR relie le domaine OSPF à l'extérieur (ce n'est pas un ABR).
- La commande `network` exige `area`. `network 0.0.0.0 255.255.255.255 area 0` active OSPF sur toutes les interfaces.
- `default-information originate` = ASBR ; sur Boson, « advertise the gateway of last resort » + « becomes the ASBR ».
- `router-id` demande un `clear ip ospf process` ou un reload. Configurer une loopback n'est pas une configuration manuelle du router ID.
- Dijkstra = SPF ; LSA dans la LSDB ; LSA réinondée toutes les 30 minutes.

### 5. Commandes IOS

```
Router(config)# router ospf 1                              ! process ID localement significatif
Router(config-router)# network 10.0.12.0 0.0.0.15 area 0   ! active OSPF sur les interfaces dans la plage, aire 0
Router(config-router)# network 0.0.0.0 255.255.255.255 area 0 ! toutes les interfaces (lab seulement)
Router(config-router)# passive-interface g2/0              ! plus de Hello, sous-réseau toujours annoncé
Router(config-router)# default-information originate       ! annonce la route par défaut (devient ASBR)
Router(config-router)# router-id 1.1.1.1                   ! router ID manuel (puis clear ip ospf process)
Router(config-router)# maximum-paths 8                     ! chemins ECMP (défaut 4)
Router(config-router)# distance 85                         ! AD d'OSPF (défaut 110)
Router# clear ip ospf process                              ! réinitialise OSPF (répondre yes)
Router(config)# ip route 0.0.0.0 0.0.0.0 203.0.113.2       ! route par défaut à annoncer
Router# show ip protocols                                  ! process, router ID, ASBR, aires, max paths, réseaux, passives, voisins, AD
Router# show ip ospf database                              ! la LSDB : Router, Net, Type-5 AS External link states
Router# show ip ospf neighbor                              ! voisins OSPF
Router# show ip ospf interface [g0/0]                      ! paramètres OSPF de l'interface (timers...)
Router# show interface l0                                  ! affiche le masque (/32), absent de show ip interface brief
```

### 6. Le lab (vidéo 054, Configuring OSPF 1)

Objectif : même réseau que le lab EIGRP (R1-R2 Gigabit, autres liens FastEthernet, LAN sur R4, lien Internet R1-ISPR1), loopbacks, OSPF aire unique, route par défaut.

1. Hostnames et IP (préconfigurés dans la vidéo).
2. **Loopbacks** : `interface l0`, `ip address 4.4.4.4 255.255.255.255` ; `show ip interface brief` n'affiche pas le masque, `show interface l0` montre « Internet address is 4.4.4.4/32 ».
3. **OSPF** avec un process ID différent par routeur pour prouver qu'il est local (R4 : 4, R3 : 3, R2 : 2, R1 : 1) et quatre façons d'activer OSPF : R4 `network 0.0.0.0 255.255.255.255 area 0` (toutes les interfaces) ; R3 `network 10.0.13.2 0.0.0.0 area 0`, `network 10.0.34.1 0.0.0.0 area 0`, `network 3.3.3.3 0.0.0.0 area 0` (adresse exacte /32) ; R2 `network 10.0.0.0 0.0.255.255 area 0` (les deux interfaces physiques d'un coup) + `network 2.2.2.2 0.0.0.0 area 0` ; R1 `network 10.0.12.0 0.0.0.3 area 0`, `network 10.0.13.0 0.0.0.3 area 0`, `network 1.1.1.1 0.0.0.0 area 0` (adresse réseau de chaque interface). **Pas d'OSPF sur le lien Internet** (G3/0) : les autres routeurs n'ont pas besoin de connaître 203.0.113.0/30, ils recevront la route par défaut. Interfaces passives : R4 G0/0 (LAN) et **Loopback0 sur chaque routeur** (sinon des Hello partent par la loopback).
4. **Route par défaut** : sur R1, `default-information originate` puis `ip route 0.0.0.0 0.0.0.0 203.0.113.2`. `show ip protocols` : router ID 1.1.1.1 (loopback), « It is an autonomous system boundary router ». Aperçu des commandes `show ip ospf database` (Router, Net, Type-5 AS External link states), `show ip ospf neighbor` (R2, R3), `show ip ospf interface`.
5. **Tables de routage** : R2 défaut via 10.0.12.1, R3 via 10.0.13.1 ; **R4 installe les deux routes** (via R2 et via R3) malgré le lien Gigabit vers R2 : explication dans les vidéos suivantes (coût par défaut identique pour FastEthernet et Gigabit, Day 27).

Aperçu Boson NetSim (« Planning and Configuring Single-Area OSPF ») : liens série en **Frame Relay** (encapsulation de couche 2 pour liaisons série, comme PPP et HDLC, hors programme), vérification `show ip interface brief` et pings, aire backbone = 0, commandes `network` **précises** (pas le raccourci 0.0.0.0) : `network 10.0.0.0 0.0.0.255 area 0` etc. ; la suite (DR) est pour les Days 27-28.

### 7. Le quiz (vidéo 053 : 5 questions, plus une question Boson ExSim)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Q1. Affirmations **fausses** sur OSPF ? (2) | **B** (l'aire unique doit utiliser l'aire 0) et **F** (le process ID doit égaler le numéro d'aire) | N'importe quelle aire fonctionne en aire unique (0 = bonne pratique) ; en multi-aires un seul processus gère plusieurs aires. A (ABR vers l'aire 0), C (process ID différents = voisins possibles), D (`area` obligatoire dans `network`), E (ASBR) sont vraies. |
| Q2. Activer OSPF sur G0/1 (10.0.12.1/28) et G0/2 (10.0.13.1/26) avec une seule commande ? | **C, `network 10.0.12.0 0.0.1.255 area 0`** | Seule plage qui contient les deux adresses. |
| Q3. Topologie multi-aires : combien de backbone routers, d'ABR, d'ASBR ? | **4 backbone routers** (au moins une interface dans l'aire 0), **3 ABR** (interfaces dans deux aires), **1 ASBR** (relié à Internet, annonce probablement une route par défaut) | Définitions des rôles. |
| Q4. Quelle configuration fait de R1 un ASBR ? | **B** : `ip route 0.0.0.0 0.0.0.0 ...` puis `default-information originate` | A : deux `network` ; C : `network 0.0.0.0 255.255.255.255` active OSPF partout ; D : commande inexistante. |
| Q5. Commande pour configurer manuellement le router ID OSPF ? | **A, `router-id 1.1.1.1`** en mode OSPF | EIGRP : `eigrp router-id` ; une IP sur une loopback (C) peut devenir router ID mais n'est pas une configuration manuelle. |
| Boson ExSim. `default-information originate` sur RouterA : deux affirmations vraies ? | **A** OSPF annonce la gateway of last resort de RouterA, **D** RouterA devient l'ASBR | Un ABR a des interfaces dans deux aires ; la commande ne résume ni ne redistribue les routes connectées. |

---

## 🇬🇧 English version

### 1. OSPF basics

- **OSPF (Open Shortest Path First)**: a **link state** protocol. Uses the **Shortest Path First** algorithm created by Dutch computer scientist **Edsger Dijkstra**, also called **Dijkstra's algorithm** (possible exam question).
- Three versions: **OSPFv1** (1989, no longer used), **OSPFv2** (1998, **IPv4**, the exam's version and the one in these videos), **OSPFv3** (developed for **IPv6**, can also be used for IPv4 but v2 is more common).
- Routers store information about the network in **LSAs (Link State Advertisements)**, organized in the **LSDB (Link State Database)**. Routers **flood** LSAs (send them to all OSPF neighbors) until all routers in the **area** have the **same LSDB**, the same map of the network.
- Example: OSPF enabled on R4's G1/0 → R4 creates an LSA with its **router ID** (RID, here 4.4.4.4: a loopback or manual configuration), the network 192.168.4.0/24 and its **cost** (1 for a GigabitEthernet interface, detailed in Day 27); the LSA is flooded throughout the network and added to every router's LSDB; each router runs the SPF algorithm to calculate its best route. Each LSA has an **aging timer of 30 minutes** by default, after which it is flooded again.
- **Three steps**: 1) become **neighbors** with routers on the same segment; 2) **exchange LSAs**; 3) independently **calculate** the best routes and insert them in the routing table.

### 2. OSPF areas

- A small network (4 routers) works fine as **single-area**. In a large network (500 routers, 1000 subnets) a single area causes problems: SPF takes longer and needs **exponentially** more processing power, a huge LSDB uses more memory, and every small change (an interface activated) floods LSAs to all routers and triggers SPF everywhere. So the network is divided into areas. The exam only requires single-area, but know the terms and rules:
  - **Area**: a set of routers and links **sharing the same LSDB**; each area has its own LSDB.
  - **Backbone area = area 0**: a special area that **all other areas must connect to**.
  - **Internal router**: all interfaces in the same area.
  - **ABR (Area Border Router)**: interfaces in **multiple areas**; maintains one LSDB **per area**; recommended **maximum 2 areas** per ABR (3 or more can overburden the router).
  - **Backbone router**: a router with at least one interface in area 0 (including ABRs).
  - **Intra-area route**: destination in the same area; **interarea route**: destination in another area.
- **Three rules**: 1) areas must be **contiguous** (an area split in two pieces is not allowed: make the second piece a separate area); 2) every area must have **at least one ABR connected to area 0** (an area 1 connected only to area 2 is not allowed); 3) **OSPF interfaces in the same subnet must be in the same area**, or they will not become neighbors.

### 3. Basic configuration

- `router ospf <process ID>`: the **process ID is locally significant** (a router can run several OSPF processes; routers with different process IDs **do become neighbors**, unlike the EIGRP AS); unrelated to the area number. Usually 1.
- `network <address> <wildcard> area <n>`: without `area`, "Incomplete command". **Wildcard mask** as in EIGRP (Day 25). Same function as in RIP/EIGRP: look for interfaces whose IP is in the range, **activate OSPF on them in the given area**, form neighborships, advertise the interface prefix. It does not say "advertise this network". In single-area any area number is possible, but **area 0 is best practice**.
- `passive-interface g2/0`: no more **Hello messages** sent out of the interface (Hellos introduce the router to neighbors, Day 27), but the interface's subnet is **still advertised** in LSAs. Use it on every interface with no OSPF neighbor.
- `default-information originate`: advertises the default route (e.g. to the ISP 203.0.113.2) by creating a new LSA flooded to all; R2, R3, R4 add the default route via R1. The router becomes an **ASBR (Autonomous System Boundary Router)**: it connects the OSPF domain to an external network (the Internet).
- **Router ID**: same order as EIGRP: **1) manual configuration, 2) highest loopback IP, 3) highest physical interface IP**. Command `router-id 1.1.1.1` (not `eigrp router-id`); message "Reload or use "clear ip ospf process" command, for this to take effect". `clear ip ospf process` (privileged exec, answer `yes`; the `[no]` in brackets is the default choice) resets OSPF: a bad idea in production (OSPF routes lost for a short time), fine in a lab.
- `show ip protocols`: "Routing protocol is ospf 1", router ID, "It is an autonomous system boundary router" (after default-information originate), "Number of areas in this router is 1. 1 normal 0 stub 0 nssa" (area types not a CCNA topic), **Maximum path 4** (OSPF does **not** do unequal-cost load balancing, only ECMP; `maximum-paths` to change), Routing for Networks (the network commands), passive interfaces, Routing Information Sources (neighbors' router IDs, here the loopbacks 2.2.2.2 etc.), **Distance 110** (`distance 85` to prefer OSPF over EIGRP).

### 4. Exam traps

- Single-area **does not have to** use area 0 (best practice only); the process ID **need not** match the area number or other routers.
- Every non-backbone area needs an ABR to area 0; an ASBR connects the OSPF domain to the outside (it is not an ABR).
- The `network` command requires `area`. `network 0.0.0.0 255.255.255.255 area 0` activates OSPF on all interfaces.
- `default-information originate` = ASBR; in Boson's words, "advertise the gateway of last resort" + "becomes the ASBR".
- `router-id` needs `clear ip ospf process` or a reload. Configuring a loopback is not a manual router ID configuration.
- Dijkstra = SPF; LSAs in the LSDB; LSA re-flooded every 30 minutes.

### 5. IOS commands

```
Router(config)# router ospf 1                              ! locally significant process ID
Router(config-router)# network 10.0.12.0 0.0.0.15 area 0   ! activates OSPF on interfaces in the range, area 0
Router(config-router)# network 0.0.0.0 255.255.255.255 area 0 ! all interfaces (labs only)
Router(config-router)# passive-interface g2/0              ! no Hellos, subnet still advertised
Router(config-router)# default-information originate       ! advertise the default route (becomes ASBR)
Router(config-router)# router-id 1.1.1.1                   ! manual router ID (then clear ip ospf process)
Router(config-router)# maximum-paths 8                     ! ECMP paths (default 4)
Router(config-router)# distance 85                         ! OSPF's AD (default 110)
Router# clear ip ospf process                              ! resets OSPF (answer yes)
Router(config)# ip route 0.0.0.0 0.0.0.0 203.0.113.2       ! default route to advertise
Router# show ip protocols                                  ! process, router ID, ASBR, areas, max paths, networks, passives, neighbors, AD
Router# show ip ospf database                              ! the LSDB: Router, Net, Type-5 AS External link states
Router# show ip ospf neighbor                              ! OSPF neighbors
Router# show ip ospf interface [g0/0]                      ! OSPF settings of the interface (timers...)
Router# show interface l0                                  ! shows the mask (/32), missing from show ip interface brief
```

### 6. The lab (video 054, Configuring OSPF 1)

Goal: same network as the EIGRP lab (R1-R2 Gigabit, other links FastEthernet, LAN on R4, Internet link R1-ISPR1), loopbacks, single-area OSPF, default route.

1. Hostnames and IPs (pre-configured in the video).
2. **Loopbacks**: `interface l0`, `ip address 4.4.4.4 255.255.255.255`; `show ip interface brief` does not show the mask, `show interface l0` shows "Internet address is 4.4.4.4/32".
3. **OSPF** with a different process ID per router to prove it is local (R4: 4, R3: 3, R2: 2, R1: 1) and four ways to activate OSPF: R4 `network 0.0.0.0 255.255.255.255 area 0` (all interfaces); R3 `network 10.0.13.2 0.0.0.0 area 0`, `network 10.0.34.1 0.0.0.0 area 0`, `network 3.3.3.3 0.0.0.0 area 0` (exact /32 address); R2 `network 10.0.0.0 0.0.255.255 area 0` (both physical interfaces at once) + `network 2.2.2.2 0.0.0.0 area 0`; R1 `network 10.0.12.0 0.0.0.3 area 0`, `network 10.0.13.0 0.0.0.3 area 0`, `network 1.1.1.1 0.0.0.0 area 0` (each interface's network address). **No OSPF on the Internet link** (G3/0): the other routers do not need to know 203.0.113.0/30, they will get the default route. Passive interfaces: R4 G0/0 (LAN) and **Loopback0 on every router** (otherwise Hellos go out of the loopback).
4. **Default route**: on R1, `default-information originate` then `ip route 0.0.0.0 0.0.0.0 203.0.113.2`. `show ip protocols`: router ID 1.1.1.1 (loopback), "It is an autonomous system boundary router". Preview of `show ip ospf database` (Router, Net, Type-5 AS External link states), `show ip ospf neighbor` (R2, R3), `show ip ospf interface`.
5. **Routing tables**: R2 default via 10.0.12.1, R3 via 10.0.13.1; **R4 installs both routes** (via R2 and via R3) despite the Gigabit link to R2: explained in the next videos (same default cost for FastEthernet and Gigabit, Day 27).

Boson NetSim preview ("Planning and Configuring Single-Area OSPF"): serial links with **Frame Relay** (a Layer 2 encapsulation for serial links, like PPP and HDLC, not a CCNA topic), `show ip interface brief` and ping checks, backbone area = 0, **specific** `network` commands (not the 0.0.0.0 shortcut): `network 10.0.0.0 0.0.0.255 area 0` etc.; the rest (DR) is for Days 27-28.

### 7. The quiz (video 053: 5 questions, plus one Boson ExSim question)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Q1. Statements that are **not true** about OSPF? (2) | **B** (single-area must use area 0) and **F** (process ID must match the area number) | Any area works for single-area (0 = best practice); in multi-area one process handles several areas. A (ABR to area 0), C (different process IDs can be neighbors), D (`area` required in `network`), E (ASBR) are true. |
| Q2. Activate OSPF on G0/1 (10.0.12.1/28) and G0/2 (10.0.13.1/26) with one command? | **C, `network 10.0.12.0 0.0.1.255 area 0`** | The only range containing both addresses. |
| Q3. Multi-area topology: how many backbone routers, ABRs, ASBRs? | **4 backbone routers** (at least one interface in area 0), **3 ABRs** (interfaces in two areas), **1 ASBR** (connected to the Internet, likely advertising a default route) | Role definitions. |
| Q4. Which configuration makes R1 an ASBR? | **B**: `ip route 0.0.0.0 0.0.0.0 ...` then `default-information originate` | A: two `network` commands; C: `network 0.0.0.0 255.255.255.255` activates OSPF everywhere; D: not a real command. |
| Q5. Command to manually configure the OSPF router ID? | **A, `router-id 1.1.1.1`** in OSPF mode | EIGRP: `eigrp router-id`; an IP on a loopback (C) may become the router ID but is not a manual configuration. |
| Boson ExSim. `default-information originate` on RouterA: two true statements? | **A** OSPF advertises RouterA's gateway of last resort, **D** RouterA becomes the ASBR | An ABR has interfaces in two areas; the command neither summarizes nor redistributes connected routes. |
