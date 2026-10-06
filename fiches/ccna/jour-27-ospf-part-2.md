# CCNA Day 27 : OSPF Part 2 / OSPF partie 2

> Source : Jeremy's IT Lab, « Free CCNA | OSPF Part 2 | Day 27 » (cours, 37 min, vidéo n°55 de la playlist : métrique, états de voisinage, configurations) et « Configuring OSPF (2) | Day 27 Lab » (lab, 22 min, vidéo n°56). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. La métrique OSPF : le coût (cost)

- Calculé automatiquement d'après la **bande passante** de l'interface : **coût = reference bandwidth ÷ bande passante de l'interface**. **Reference bandwidth par défaut : 100 Mbps.** Ethernet 10 Mbps → 100/10 = **10** ; FastEthernet 100 Mbps → **1** ; GigabitEthernet → 100/1000 = 0,1 → **1** ; 10 Gig → 0,01 → **1** : **toute valeur inférieure à 1 est convertie en 1**, donc FastEthernet, Gigabit et 10 Gig ont le même coût par défaut. `show ip ospf interface f2/0` affiche le coût (à deux endroits).
- **Changer la reference bandwidth** (recommandé) : `auto-cost reference-bandwidth <Mbps>` en mode OSPF. Avec 100 000 (= 100 Gbps) : FastEthernet = 1000, Gigabit = 100. Choisir une valeur **supérieure aux liens les plus rapides** du réseau pour les futures mises à niveau. Message : « Please ensure reference bandwidth is consistent across all routers » : **même valeur sur tous les routeurs**.
- Le coût d'une route = **somme des coûts des interfaces de sortie** (comme STP). R1 → 192.168.4.0/24 via G0/0 de R1, G1/0 de R2, G1/0 de R4 : 100 + 100 + 100 = **300**. Une **loopback a un coût de 1** : R1 → 2.2.2.2 = 100 + 1 = **101**. Avant le changement, R1 avait deux routes vers 192.168.4.0 (FastEthernet R3-R4 au même coût 1) ; après, une seule, coût 300.
- `ip ospf cost <n>` sur l'interface : coût manuel, prioritaire sur le calcul (ex. 10 000 sur G0/0).
- `bandwidth <kbps>` sur l'interface : change la **valeur de bande passante** utilisée dans les calculs (OSPF, EIGRP...), **pas la vitesse réelle** (ça, c'est `speed`). Non recommandé car la valeur sert à d'autres calculs. Attention aux unités : reference-bandwidth en **Mbps**, bandwidth en **kbps** ; toujours vérifier avec `?`.
- Trois méthodes, résumé : reference bandwidth (OSPF), `ip ospf cost` (interface), `bandwidth` (interface, déconseillé). `show ip ospf interface brief` : vue rapide des coûts (absent de Packet Tracer).

### 2. Devenir voisins OSPF

- Tâche principale de la configuration et du dépannage d'OSPF : s'assurer que les routeurs deviennent voisins ; ensuite ils partagent les LSA et calculent seuls.
- Quand OSPF est activé sur une interface, le routeur envoie des **Hello** à intervalle régulier (**Hello timer, 10 secondes par défaut sur Ethernet**) en multicast **224.0.0.5** (tous les routeurs OSPF ; RIP : 224.0.0.9, EIGRP : 224.0.0.10). Les messages OSPF sont encapsulés dans IP avec le champ **Protocol = 89**.
- **États de voisinage**, dans l'ordre (R1 active OSPF alors que R2 l'a déjà) :
  1. **Down** : R1 ne connaît aucun voisin ; il envoie un Hello avec son RID et le champ neighbor RID à 0.0.0.0.
  2. **Init** : R2 reçoit le Hello et ajoute R1 à sa table de voisins ; Hello reçu mais **son propre RID n'y figure pas**.
  3. **2-way** : R2 envoie un Hello contenant les deux RID ; R1 ajoute R2 en 2-way, puis renvoie un Hello avec le RID de R2. **2-way = le routeur a reçu un Hello contenant son propre RID.** Toutes les conditions pour être voisins sont remplies ; sur certains types de réseau, l'**élection DR/BDR** a lieu ici (Day 28). Si ce stade n'est pas atteint, il faut dépanner.
  4. **Exstart** : choix du **Master** (RID le plus haut, ici R2) et du **Slave** (RID le plus bas) via des paquets **DBD (Database Description)** ; le Master lance l'échange. Rien à voir avec DR/BDR.
  5. **Exchange** : échange de **DBD** listant les LSA de chaque LSDB (sans le détail) ; chaque routeur compare avec sa LSDB pour savoir ce qui lui manque.
  6. **Loading** : **LSR (Link State Request)** pour demander les LSA manquantes, **LSU (Link State Update)** qui contiennent les LSA, **LSAck** pour accuser réception.
  7. **Full** : adjacence complète, LSDB identiques. Les Hello continuent toutes les 10 s ; le **Dead timer (40 secondes par défaut)** est remis à zéro à chaque Hello reçu ; s'il atteint 0, le voisin est supprimé.
- Correspondance avec les trois étapes du Day 26 : Down/Init/2-way = devenir voisins ; Exstart/Exchange/Loading = échanger les LSA ; puis calcul des routes.
- **Cinq types de messages OSPF** : **1 Hello, 2 DBD, 3 LSR, 4 LSU, 5 LSAck**.
- `show ip ospf neighbor` : état FULL avec R2 et R3, tous deux **DR** (Day 28), **Dead Time** qui descend de 40 à 30 puis revient à 40 à chaque Hello. `show ip ospf interface g0/0` : « Hello 10, Dead 40 », « Hello due in 7 seconds », « Neighbor Count is 1, Adjacent neighbor count is 1 » (différence expliquée au Day 28), « Adjacent with neighbor 2.2.2.2 (Designated Router) ».

### 3. Configurations supplémentaires

- Activer OSPF **directement sur l'interface**, sans `network` : `ip ospf <process ID> area <n>` en mode interface. `show ip protocols` affiche alors « Routing on Interfaces Configured Explicitly » au lieu de « Routing for Networks » (pas dans Packet Tracer).
- Interfaces passives par défaut : `passive-interface default` puis `no passive-interface g0/0` pour les interfaces avec voisins. Même effet que la méthode classique, parfois plus rapide.

### 4. Pièges d'examen

- **Reference bandwidth par défaut 100 Mbps** ; FastEthernet, Gigabit et 10 Gig ont **tous un coût de 1** par défaut (pas Ethernet 10 Mbps, coût 10).
- Pour qu'une FastEthernet coûte 100 : `auto-cost reference-bandwidth 10000` (10 000 / 100). Avec 1000 : Gigabit = 1, FastEthernet = 10 (question Boson : chemin A-B-E-C = 3).
- Ordre des états : **Down, Init, 2-way, Exstart, Exchange, Loading, Full**. Master/Slave décidés en **Exstart** (le Master commence l'échange de DBD en Exchange) ; DR/BDR en 2-way (certains réseaux).
- Timers par défaut sur Ethernet : **Hello 10 s, Dead 40 s** (30/120 sur d'autres types de connexion, Day 28).
- 224.0.0.5, protocole IP **89** (0x59 dans Packet Tracer), Hello = type 1, version 2, Area ID écrit 0.0.0.0.
- `bandwidth` ne change pas la vitesse ; `speed` oui.
- Une interface passive **ne peut pas** avoir de voisin : `passive-interface default` fait tomber immédiatement les voisins.

### 5. Commandes IOS

```
Router(config-router)# auto-cost reference-bandwidth 10000   ! en Mbps, même valeur sur tous les routeurs
Router(config-if)# ip ospf cost 10000                        ! coût manuel de l'interface
Router(config-if)# bandwidth 100000                          ! en kbps, valeur de calcul seulement (déconseillé)
Router(config-if)# speed 100                                 ! vitesse physique réelle (pas pour OSPF)
Router(config-if)# ip ospf 1 area 0                          ! activer OSPF directement sur l'interface
Router(config)# interface range g0/0, f1/0, l0               ! virgule pour des types d'interfaces différents
Router(config-router)# passive-interface default             ! tout passif...
Router(config-router)# no passive-interface f1/0             ! ...sauf les interfaces avec voisins
Router# show ip ospf interface [f2/0]                        ! coût, Hello/Dead, Hello due, neighbor count, adjacent count, DR
Router# show ip ospf interface brief                         ! coûts de toutes les interfaces OSPF (pas dans Packet Tracer)
Router# show ip ospf neighbor                                ! état (FULL), rôle DR/BDR, Dead Time
Router# show ip protocols                                    ! Routing on Interfaces Configured Explicitly
```

### 6. Le lab (vidéo 056, Configuring OSPF 2)

Objectif : même réseau que le Day 26, OSPF activé directement sur les interfaces, reference bandwidth, route par défaut, Hello en simulation.

1. Hostnames et IP préconfigurés.
2. **OSPF sur les interfaces** : R1 `interface range g0/0, f1/0, l0` (virgule entre types différents ; tiret pour une plage comme g0/0 - 3), `ip ospf 1 area 0` ; pas d'OSPF sur G3/0 (Internet). `router ospf 1`, `passive-interface l0`. R2 (g0/0, f1/0, l0), R3 (f1/0, f2/0, l0) idem. R4 (g0/0, f1/0, f2/0, l0) : `passive-interface default` → message « neighbor changed to DOWN » (pas de voisin via une interface passive) ; `no passive-interface f1/0`, `no passive-interface f2/0` ; `show ip protocols` : seules G0/0 et L0 passives. `show ip ospf neighbor` : R2 et R3, Dead Time qui descend jusqu'à 30 puis se remet à 40.
3. **Reference bandwidth** pour qu'une FastEthernet coûte 100 : `auto-cost reference-bandwidth 10000` (« what divided by 100 equals 100 ? ») sur les quatre routeurs ; `show ip ospf interface` : F1/0 coût **100**, G0/0 coût **10** ; 10 Gig et plus = 1.
4. **Route par défaut** sur R1 : `default-information originate` puis `ip route 0.0.0.0 0.0.0.0 203.0.113.2`. Sur R4, `show ip route` : seule la route via R2 est installée, avec un **coût de 1** et le code **E2 (OSPF external type 2)** : sujet CCNP, la métrique interne vers R1 est ignorée pour les routes externes de type 2 ; les deux routes (via R2 et via R3) devraient donc être installées, c'est une **erreur de Packet Tracer** (sur GNS3 ou un vrai routeur, les deux apparaissent). Preuve : `interface f1/0`, `shutdown` → la route via R3 (10.0.34.1) apparaît avec le même coût 1.
5. **Hello en mode simulation** : destination 224.0.0.5 ; PDU Details : version 2, **Type 1** (Hello), Router ID, **Area ID 0.0.0.0** (les aires sont des nombres de 32 bits, écrits en décimal pointé), masque, Hello 10 / Dead 40, DR et BDR, voisin ; champ protocole IP **0x59 = 89**.

Aperçu Boson NetSim (« OSPF 2 ») : mot de passe `cisco` ; `show ip route` sans routes OSPF ; `show running-config` → `network 200.120.45.0 0.0.0.0 area 0` (wildcard /32 qui ne correspond à aucune interface) ; `show run | section ospf` pour filtrer ; `no network 200.120.45.0 0.0.0.0 area 0` puis `network 200.120.45.0 0.0.0.255 area 0` ; voisinage avec Miami, routes reçues après quelques secondes.

### 7. Le quiz (vidéo 055 : 5 questions, plus une question Boson ExSim)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Q1. Mettre les états de voisinage OSPF dans l'ordre (1 à 7). | **Down, Init, 2-way, Exstart, Exchange, Loading, Full** | Voir section 2. |
| Q2. Affirmation correcte sur le coût OSPF par défaut ? | **C, FastEthernet, Gigabit et 10 Gig ont le même coût** | Reference bandwidth 100 Mbps : FastEthernet = 1, et tout ce qui est plus rapide est ramené à 1 ; Ethernet 10 Mbps = 10. |
| Q3. Dans quel état sont décidés Master et Slave ? | **A, Exstart** | Le Master démarre l'échange de DBD en Exchange (C) ; 2-way (B) élit DR/BDR dans certains cas ; Loading (D) échange LSR/LSU/LSAck. |
| Q4. Commande pour qu'une interface FastEthernet ait un coût OSPF de 100 ? | **C, `auto-cost reference-bandwidth 10000`** | 10 000 / 100 = 100. |
| Q5. Timers Hello/Dead OSPF par défaut sur Ethernet ? | **B, Hello 10 s, Dead 40 s** | 30/120 (C) vaut pour d'autres types de connexion (Day 28). |
| Boson ExSim. `auto-cost reference-bandwidth 1000` partout : coût de la route RouterA → RouterC ? | **B, 3** | Gigabit = 1000/1000 = 1, FastEthernet = 10 ; chemin sans FastEthernet A → B → E → C = 1 + 1 + 1. |

---

## 🇬🇧 English version

### 1. OSPF's metric: cost

- Calculated automatically from the interface **bandwidth**: **cost = reference bandwidth ÷ interface bandwidth**. **Default reference bandwidth: 100 Mbps.** Ethernet 10 Mbps → 100/10 = **10**; FastEthernet 100 Mbps → **1**; GigabitEthernet → 100/1000 = 0.1 → **1**; 10 Gig → 0.01 → **1**: **any value less than 1 is converted to 1**, so FastEthernet, Gigabit and 10 Gig have the same default cost. `show ip ospf interface f2/0` shows the cost (in two places).
- **Change the reference bandwidth** (recommended): `auto-cost reference-bandwidth <Mbps>` in OSPF mode. With 100,000 (= 100 Gbps): FastEthernet = 1000, Gigabit = 100. Choose a value **greater than the fastest links** in the network to allow for future upgrades. Message: "Please ensure reference bandwidth is consistent across all routers": **same value on every router**.
- A route's cost = **total cost of the outgoing (exit) interfaces** (like STP). R1 → 192.168.4.0/24 via R1 G0/0, R2 G1/0, R4 G1/0: 100 + 100 + 100 = **300**. A **loopback has a cost of 1**: R1 → 2.2.2.2 = 100 + 1 = **101**. Before the change R1 had two routes to 192.168.4.0 (FastEthernet R3-R4 at the same cost 1); after, only one, cost 300.
- `ip ospf cost <n>` on the interface: manual cost, takes priority over the calculation (e.g. 10,000 on G0/0).
- `bandwidth <kbps>` on the interface: changes the **bandwidth value** used in calculations (OSPF, EIGRP...), **not the actual speed** (that is `speed`). Not recommended because the value is used in other calculations. Mind the units: reference-bandwidth in **Mbps**, bandwidth in **kbps**; always check with `?`.
- Three methods, summary: reference bandwidth (OSPF), `ip ospf cost` (interface), `bandwidth` (interface, not recommended). `show ip ospf interface brief`: quick view of costs (not in Packet Tracer).

### 2. Becoming OSPF neighbors

- The main task in configuring and troubleshooting OSPF: make sure routers become neighbors; then they share LSAs and calculate routes on their own.
- When OSPF is activated on an interface, the router sends **Hello** messages at regular intervals (**Hello timer, 10 seconds by default on Ethernet**) multicast to **224.0.0.5** (all OSPF routers; RIP: 224.0.0.9, EIGRP: 224.0.0.10). OSPF messages are encapsulated in IP with **Protocol = 89**.
- **Neighbor states**, in order (R1 activates OSPF while R2 already has it):
  1. **Down**: R1 knows no neighbor; it sends a Hello with its RID and the neighbor RID field at 0.0.0.0.
  2. **Init**: R2 receives the Hello and adds R1 to its neighbor table; a Hello was received but **its own RID is not in it**.
  3. **2-way**: R2 sends a Hello with both RIDs; R1 adds R2 in 2-way, then sends a Hello with R2's RID. **2-way = the router received a Hello containing its own RID.** All conditions to be neighbors are met; on some network types the **DR/BDR election** happens here (Day 28). If this state is not reached, troubleshoot.
  4. **Exstart**: choose the **Master** (highest RID, here R2) and **Slave** (lowest RID) with **DBD (Database Description)** packets; the Master starts the exchange. Unrelated to DR/BDR.
  5. **Exchange**: exchange of **DBDs** listing the LSAs in each LSDB (no detail); each router compares with its LSDB to find what it is missing.
  6. **Loading**: **LSR (Link State Request)** to request missing LSAs, **LSU (Link State Update)** carrying the LSAs, **LSAck** to acknowledge.
  7. **Full**: full adjacency, identical LSDBs. Hellos continue every 10 s; the **Dead timer (40 seconds by default)** is reset on each Hello received; if it reaches 0, the neighbor is removed.
- Mapping to Day 26's three steps: Down/Init/2-way = becoming neighbors; Exstart/Exchange/Loading = exchanging LSAs; then route calculation.
- **Five OSPF message types**: **1 Hello, 2 DBD, 3 LSR, 4 LSU, 5 LSAck**.
- `show ip ospf neighbor`: FULL state with R2 and R3, both **DR** (Day 28), **Dead Time** counting down from 40 to 30 then back to 40 on each Hello. `show ip ospf interface g0/0`: "Hello 10, Dead 40", "Hello due in 7 seconds", "Neighbor Count is 1, Adjacent neighbor count is 1" (difference explained in Day 28), "Adjacent with neighbor 2.2.2.2 (Designated Router)".

### 3. Additional configurations

- Activate OSPF **directly on the interface**, without `network`: `ip ospf <process ID> area <n>` in interface mode. `show ip protocols` then shows "Routing on Interfaces Configured Explicitly" instead of "Routing for Networks" (not in Packet Tracer).
- Passive interfaces by default: `passive-interface default` then `no passive-interface g0/0` for interfaces with neighbors. Same effect as the usual method, sometimes faster.

### 4. Exam traps

- **Default reference bandwidth 100 Mbps**; FastEthernet, Gigabit and 10 Gig **all have cost 1** by default (not 10 Mbps Ethernet, cost 10).
- For a FastEthernet cost of 100: `auto-cost reference-bandwidth 10000` (10,000 / 100). With 1000: Gigabit = 1, FastEthernet = 10 (Boson question: path A-B-E-C = 3).
- State order: **Down, Init, 2-way, Exstart, Exchange, Loading, Full**. Master/Slave decided in **Exstart** (the Master starts the DBD exchange in Exchange); DR/BDR in 2-way (some networks).
- Default timers on Ethernet: **Hello 10 s, Dead 40 s** (30/120 on other connection types, Day 28).
- 224.0.0.5, IP protocol **89** (0x59 in Packet Tracer), Hello = type 1, version 2, Area ID written 0.0.0.0.
- `bandwidth` does not change the speed; `speed` does.
- A passive interface **cannot** have a neighbor: `passive-interface default` drops neighbors immediately.

### 5. IOS commands

```
Router(config-router)# auto-cost reference-bandwidth 10000   ! in Mbps, same value on all routers
Router(config-if)# ip ospf cost 10000                        ! manual interface cost
Router(config-if)# bandwidth 100000                          ! in kbps, calculation value only (not recommended)
Router(config-if)# speed 100                                 ! actual physical speed (not for OSPF)
Router(config-if)# ip ospf 1 area 0                          ! activate OSPF directly on the interface
Router(config)# interface range g0/0, f1/0, l0               ! comma for different interface types
Router(config-router)# passive-interface default             ! everything passive...
Router(config-router)# no passive-interface f1/0             ! ...except interfaces with neighbors
Router# show ip ospf interface [f2/0]                        ! cost, Hello/Dead, Hello due, neighbor count, adjacent count, DR
Router# show ip ospf interface brief                         ! costs of all OSPF interfaces (not in Packet Tracer)
Router# show ip ospf neighbor                                ! state (FULL), DR/BDR role, Dead Time
Router# show ip protocols                                    ! Routing on Interfaces Configured Explicitly
```

### 6. The lab (video 056, Configuring OSPF 2)

Goal: same network as Day 26, OSPF activated directly on interfaces, reference bandwidth, default route, a Hello in simulation mode.

1. Hostnames and IPs pre-configured.
2. **OSPF on interfaces**: R1 `interface range g0/0, f1/0, l0` (comma between different types; hyphen for a range like g0/0 - 3), `ip ospf 1 area 0`; no OSPF on G3/0 (Internet). `router ospf 1`, `passive-interface l0`. R2 (g0/0, f1/0, l0), R3 (f1/0, f2/0, l0) likewise. R4 (g0/0, f1/0, f2/0, l0): `passive-interface default` → message "neighbor changed to DOWN" (no neighbor through a passive interface); `no passive-interface f1/0`, `no passive-interface f2/0`; `show ip protocols`: only G0/0 and L0 passive. `show ip ospf neighbor`: R2 and R3, Dead Time counting down to 30 then resetting to 40.
3. **Reference bandwidth** so a FastEthernet costs 100: `auto-cost reference-bandwidth 10000` ("what divided by 100 equals 100?") on all four routers; `show ip ospf interface`: F1/0 cost **100**, G0/0 cost **10**; 10 Gig and faster = 1.
4. **Default route** on R1: `default-information originate` then `ip route 0.0.0.0 0.0.0.0 203.0.113.2`. On R4, `show ip route`: only the route via R2 is installed, with **cost 1** and code **E2 (OSPF external type 2)**: a CCNP topic, the internal metric to R1 is ignored for external type 2 routes; both routes (via R2 and via R3) should therefore be installed, this is a **Packet Tracer error** (in GNS3 or on real routers both appear). Proof: `interface f1/0`, `shutdown` → the route via R3 (10.0.34.1) appears with the same cost 1.
5. **Hello in simulation mode**: destination 224.0.0.5; PDU Details: version 2, **Type 1** (Hello), Router ID, **Area ID 0.0.0.0** (areas are 32-bit numbers, written in dotted decimal), mask, Hello 10 / Dead 40, DR and BDR, neighbor; IP protocol field **0x59 = 89**.

Boson NetSim preview ("OSPF 2"): password `cisco`; `show ip route` with no OSPF routes; `show running-config` → `network 200.120.45.0 0.0.0.0 area 0` (/32 wildcard matching no interface); `show run | section ospf` to filter; `no network 200.120.45.0 0.0.0.0 area 0` then `network 200.120.45.0 0.0.0.255 area 0`; neighborship with Miami, routes received after a few seconds.

### 7. The quiz (video 055: 5 questions, plus one Boson ExSim question)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Q1. Put the OSPF neighbor states in order (1 to 7). | **Down, Init, 2-way, Exstart, Exchange, Loading, Full** | See section 2. |
| Q2. Correct statement about OSPF's default cost? | **C, FastEthernet, Gigabit and 10 Gig have the same cost** | Reference bandwidth 100 Mbps: FastEthernet = 1, and anything faster is rounded up to 1; 10 Mbps Ethernet = 10. |
| Q3. In which state are Master and Slave decided? | **A, Exstart** | The Master starts the DBD exchange in Exchange (C); 2-way (B) elects DR/BDR in some cases; Loading (D) exchanges LSR/LSU/LSAck. |
| Q4. Command to give a FastEthernet interface an OSPF cost of 100? | **C, `auto-cost reference-bandwidth 10000`** | 10,000 / 100 = 100. |
| Q5. Default OSPF Hello/Dead timers on Ethernet? | **B, Hello 10 s, Dead 40 s** | 30/120 (C) applies to other connection types (Day 28). |
| Boson ExSim. `auto-cost reference-bandwidth 1000` on every router: cost of the route RouterA → RouterC? | **B, 3** | Gigabit = 1000/1000 = 1, FastEthernet = 10; the path with no FastEthernet A → B → E → C = 1 + 1 + 1. |
