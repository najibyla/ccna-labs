# CCNA Day 28 : OSPF Part 3 / OSPF partie 3

> Source : Jeremy's IT Lab, « Free CCNA | OSPF Part 3 | Day 28 » (cours, 48 min, vidéo n°57 de la playlist : types de réseau, DR/BDR, conditions de voisinage, types de LSA, liaisons série) et « Configuring OSPF (3) | Day 28 Lab » (lab de dépannage, 21 min, vidéo n°58). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Les interfaces loopback

Interface **virtuelle**, **toujours up/up** sauf `shutdown` manuel : son état ne dépend d'aucune interface physique (qui peut tomber sur panne matérielle). Elle fournit une **adresse IP stable pour joindre et identifier le routeur** : si R4 envoie un paquet à R1 sur 10.0.13.1 (G1/0) et que G1/0 tombe, le paquet n'arrive plus ; avec la loopback 1.1.1.1, R1 reste joignable par ses autres interfaces.

### 2. Les types de réseau OSPF (network types)

Le type de connexion entre voisins influence le comportement d'OSPF. Trois types principaux :

| Type | Par défaut sur | Découverte des voisins | DR/BDR | Timers Hello/Dead |
| :--- | :--- | :--- | :--- | :--- |
| **Broadcast** (sujet 3.4c) | **Ethernet**, FDDI | dynamique, Hello multicast 224.0.0.5 | **élus** sur chaque sous-réseau | **10 / 40 s** |
| **Point-to-point** (sujet 3.4b) | liaisons série **PPP** et **HDLC** | dynamique, 224.0.0.5 | **pas d'élection** (deux routeurs seulement, adjacence Full directe) | **10 / 40 s** |
| Non-broadcast (hors programme) | Frame Relay, X.25 | voisins à configurer **manuellement** | | 30 / 120 s |

#### 2.1 Broadcast : DR, BDR, DROther

- Un **DR (Designated Router)** et un **BDR (Backup Designated Router)** doivent être élus sur **chaque sous-réseau** ; sur une interface sans voisin (G1/0 de R1, R3, R4, R5), il y a un DR mais pas de BDR. Les autres routeurs du sous-réseau sont **DROther**.
- **Élection** : 1) **priorité d'interface OSPF la plus haute** (défaut **1** sur toutes les interfaces, donc égalité) ; 2) **router ID le plus haut**. Premier = DR, deuxième = BDR. `ip ospf priority <0-255>` sur l'interface ; **priorité 0 = ne peut jamais être DR/BDR**.
- L'élection est **non préemptive** : après `ip ospf priority 255` sur R2, R2 reste DROther ; DR et BDR gardent leur rôle jusqu'à une réinitialisation d'OSPF, une panne ou un shutdown d'interface (notion de préemption revue au Day 29 avec les FHRP). Après `clear ip ospf process` sur R5 (le DR) : **le BDR (R4) devient DR** immédiatement, puis une élection désigne le nouveau BDR (R2, priorité 255). R5 et R3 deviennent DROther.
- **Les DROther ne forment une adjacence Full qu'avec le DR et le BDR** ; entre DROther, l'état reste **2-way** (R3 reste stable en 2-way avec R5). Le DR et le BDR forment une adjacence Full avec **tous** les routeurs du sous-réseau. But : réduire l'inondation de LSA (6 routeurs qui s'échangent tous leurs LSA = beaucoup de trafic ; via DR/BDR, beaucoup moins) ; tous ont quand même la même LSDB. Les messages destinés au DR et au BDR utilisent le multicast **224.0.0.6** (224.0.0.5 = tous les routeurs OSPF).
- `show ip ospf interface brief` : colonne Nbrs **F/C** = adjacences **Full** / **Count** total de voisins (R3 : 2 Full, 3 voisins). `show ip ospf interface g0/0` : « Neighbor Count is 3, Adjacent neighbor count is 2 », liste des voisins adjacents (BDR, DR). `show ip ospf interface` affiche aussi State DR/BDR/DROTHER, Priority, Router ID et adresse du DR et du BDR.

#### 2.2 Point-to-point et liaisons série

- Sur une liaison série (PPP ou HDLC) entre deux routeurs, pas de DR/BDR : `show ip ospf neighbor` affiche **un tiret** à la place de DR/BDR/DROTHER.
- Liaisons série (retirées de l'examen sauf pour ce type de réseau) : un côté **DCE (Data Communications Equipment)**, l'autre **DTE (Data Terminal Equipment)**. Le **DCE fixe la vitesse** avec `clock rate <bits/s>` (ex. 64000 = 64 kbps) ; Ethernet utilise `speed`, série utilise `clock rate`. `show controllers s2/0` indique DCE ou DTE (côté DTE : « detected Tx and Rx clocks »). Encapsulation par défaut **HDLC** (en réalité cHDLC, Cisco HDLC, affiché « HDLC » ; trame sans champ MAC) ; `encapsulation ppp` pour PPP, **à configurer des deux côtés** sinon l'interface tombe (deux « langues » différentes). Config R1 : clock rate, encapsulation, IP (`serial restart-delay 0` présent par défaut) ; R2 : pas de clock rate (DTE).
- `ip ospf network {broadcast | point-to-point | non-broadcast | point-to-multipoint}` sur l'interface pour changer le type (point-to-multipoint = sous-type, hors programme). Deux routeurs reliés en Ethernet direct peuvent utiliser point-to-point (pas de DR/BDR inutile), sans obligation. Une liaison série **ne peut pas** utiliser broadcast (pas de trames broadcast de couche 2).

### 3. Conditions pour devenir voisins OSPF

1. **Même aire** (area 0 sur R1, area 1 sur R2 → aucun voisin ; corriger la commande network).
2. **Même sous-réseau** sur les interfaces.
3. **Processus OSPF non arrêté** : `shutdown` en mode OSPF désactive OSPF sans effacer la config (voisin FULL → DOWN) ; `no shutdown` le relance.
4. **Router ID uniques** : avec `router-id 192.168.1.1` dupliqué sur R2 puis `clear ip ospf process`, message « OSPF detected duplicate router-id 192.168.1.1 from 192.168.1.1 on interface GigabitEthernet0/0 », voisin reste down. `no router-id` (sans préciser la valeur) corrige ; ici sans clear car R2 n'avait pas d'autre voisin.
5. **Timers Hello et Dead identiques** : `ip ospf hello-interval 5`, `ip ospf dead-interval 20` sur l'interface → voisin down, même si un seul des deux change ; `no ip ospf hello-interval`, `no ip ospf dead-interval` rétablissent les défauts.
6. **Authentification identique** : `ip ospf authentication-key jeremy` configure le mot de passe sur l'interface, mais seul `ip ospf authentication` l'active ; sans mot de passe correspondant côté R1, voisin down.
7. **IP MTU identique** (cas particulier : les routeurs **deviennent voisins** mais OSPF ne fonctionne pas) : `ip mtu 1400` sur R2 (défaut 1500) ; après `clear ip ospf process`, voisin bloqué en **EXSTART**, messages répétés ; `no ip mtu` → FULL.
8. **Même type de réseau** (cas particulier aussi) : R2 G0/0 en point-to-point, R1 en broadcast → voisin **FULL** des deux côtés, mais la loopback de R2 **n'apparaît pas** dans la table de routage de R1. Piège de dépannage : tout semble fonctionner.

### 4. Types de LSA

11 types existent, 3 à connaître :

- **Type 1, Router LSA** : générée par **chaque routeur OSPF** ; identifie le routeur par son router ID et liste les réseaux de ses interfaces OSPF.
- **Type 2, Network LSA** : générée par le **DR de chaque réseau multi-accès** (ex. Ethernet en broadcast) ; liste les routeurs attachés à ce réseau. Pas générée quand le DR n'a aucun voisin sur l'interface (G1/0 de R1, R3, R5).
- **Type 5, AS-External LSA** : générée par un **ASBR** pour les destinations hors du domaine OSPF (ex. route par défaut de R4 après `default-information originate`).
- `show ip ospf database` : même résultat sur tous les routeurs de l'aire (même LSDB). Type 3 = Summary LSA, non détaillée.

### 5. Pièges d'examen

- Point-to-point vs broadcast : **pas d'élection DR/BDR** en point-to-point ; la découverte dynamique des voisins est commune aux deux.
- Le DR a une adjacence Full avec **tous** ses voisins (4 voisins sur un segment de 5 routeurs = 4 adjacences) ; un DROther n'a que 2 adjacences Full (DR et BDR), les autres voisins restent en 2-way : « Neighbor Count 5, Adjacent neighbor count 2 » (question Boson).
- Élection : priorité la plus haute puis router ID le plus haut ; **non préemptive** : monter la priorité ne change rien tant que le DR/BDR actuels restent ; si le DR tombe, le **BDR devient DR** et le routeur à la plus haute priorité devient BDR (Q5).
- Conditions de voisinage : timers Hello/Dead identiques et même aire **oui** ; process ID identiques **non**, router ID identiques **non** (ils doivent être différents).
- MTU et type de réseau ne bloquent pas forcément le voisinage mais cassent OSPF (Exstart bloqué ; routes manquantes avec état Full).
- Type 2 = DR d'un réseau multi-accès ; type 1 = tout routeur ; type 5 = ASBR.
- Série : `clock rate` côté DCE, HDLC par défaut, PPP des deux côtés, `show controllers`.
- Priorité 0 = jamais DR/BDR. 224.0.0.6 = DR/BDR.

### 6. Commandes IOS

```
Router(config-if)# ip ospf priority 255                     ! priorité d'interface (0-255, défaut 1 ; 0 = jamais DR/BDR)
Router(config-if)# ip ospf network point-to-point           ! changer le type de réseau (broadcast, non-broadcast, point-to-multipoint)
Router(config-if)# no ip ospf network point-to-point        ! revenir au type par défaut
Router(config-if)# ip ospf hello-interval 5                 ! Hello en secondes (défaut 10) ; no ... pour rétablir
Router(config-if)# ip ospf dead-interval 20                 ! Dead en secondes (défaut 40) ; no ... pour rétablir
Router(config-if)# ip ospf authentication-key jeremy        ! mot de passe OSPF
Router(config-if)# ip ospf authentication                   ! active l'authentification sur l'interface
Router(config-if)# ip mtu 1400                              ! IP MTU en octets (défaut 1500) ; no ip mtu pour rétablir
Router(config-router)# shutdown                             ! arrête le processus OSPF sans effacer la config
Router(config-router)# no router-id                         ! retire le router ID manuel
Router(config-if)# clock rate 64000                         ! vitesse en bits/s, côté DCE seulement
Router(config-if)# encapsulation ppp                        ! remplace HDLC (défaut), des deux côtés
Router# show controllers s0/0/0                             ! DCE ou DTE, clock rate
Router# show ip ospf interface [brief]                      ! type de réseau, état DR/BDR/DROTHER, priorité, timers, Nbrs F/C
Router# show ip ospf neighbor                               ! état, rôle DR/BDR/DROTHER ou tiret (point-to-point)
Router# show ip ospf database                               ! LSDB : Router (1), Net (2), Type-5 AS External (5)
Router# show running-config | section ospf                  ! filtrer la config OSPF
Router# clear ip ospf process                               ! réinitialise OSPF (relance l'élection DR/BDR)
```

### 7. Le lab (vidéo 058, Configuring OSPF 3 : configuration et dépannage)

Objectif : réseau préconfiguré avec quelques erreurs ; R1-R2 en série ; R3-R4 en Ethernet ; R2, R4, R5 sur 192.168.245.0/29 ; R5 vers Internet ; PC1 et PC2 (10.0.2.0/24). Jeremy conseille d'essayer avant de regarder.

1. **Liaison série R1-R2** : R1 `interface s0/0/0`, `ip address 192.168.12.1 255.255.255.252`, `show controllers s0/0/0` → DCE → `clock rate 128000`, `no shutdown`. R2 : IP 192.168.12.2, DTE confirmé, `no shutdown`. OSPF : R2 a déjà OSPF sur G0/0 (`show ip protocols`) → `ip ospf 1 area 0` sur S0/0/0 (en vrai réseau, rester cohérent : tout sur l'interface ou tout par `network`). R1 : `ip ospf 1 area 0` sur S0/0/0 et G0/0. `show ip ospf interface s0/0/0` : type **point-to-point** par défaut (série, HDLC), aucun DR/BDR, Hello 10 / Dead 40 ; G0/0 : **broadcast**, R1 est DR, pas de BDR (aucun voisin). `show ip route` sur R1 : deux routes OSPF (192.168.34.0/30 et 192.168.245.0/29), il en manque.
2. **Seul R3 a une route vers 10.0.2.0/24** : sur R4, `show ip ospf neighbor` : adjacence Full avec R3, mais pas de route. `show ip ospf interface g0/1` : R4 en **broadcast**, R3 en **point-to-point** → mismatch de type de réseau. Sur R3 : `interface g0/1`, `no ip ospf network point-to-point`. R4 apprend 10.0.2.0/24 ; ping PC1 → PC2 (10.0.2.1) réussi.
3. **R2 et R4 ne deviennent pas voisins de R5** : `show ip ospf interface g0/0` sur R2 et R4 : sous-réseau, aire 0, timers par défaut corrects. Sur R5 : **Hello 5, Dead 20** → `no ip ospf hello-interval`, `no ip ospf dead-interval` ; avance de 30 s ; `show ip ospf neighbor` : R2 et R4 voisins.
4. **PC1/PC2 ne pinguent pas 8.8.8.8** : sur R5, `show running-config | section ospf` : `default-information originate` présent, mais `show ip route` : **aucune route par défaut à annoncer** → `ip route 0.0.0.0 0.0.0.0 203.0.113.2`. R5 génère alors la LSA type 5 ; R1 reçoit la route par défaut ; ping PC1 → 8.8.8.8 réussi.
5. **LSDB** : `show ip ospf database` sur R1 (identique partout) : Router link states (type 1, un par routeur), Network link states (type 2, DR des réseaux multi-accès), un Type-5 AS External (route par défaut de R5).

Aperçu Boson NetSim (« OSPF Routes ») : hostnames, IP, `show controllers s0/0` (DCE cable) et `clock rate 64000` sur Router1, DTE sur Router2 ; `router ospf 1`, `network ... 0.0.0.255 area 0` pour chaque réseau ; observation des états **INIT → EXSTART → EXCHANGE → (LOADING) → FULL** dans `show ip ospf neighbor` ; routes apprises ; ping HostA → HostB ; notation du lab.

### 8. Le quiz (vidéo 057 : 5 questions, plus une question Boson ExSim)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Q1. Caractéristique du type point-to-point différente du type broadcast ? | **B, pas d'élection DR/BDR** | C (découverte dynamique des voisins) est vrai mais aussi pour broadcast. |
| Q2. Réseau broadcast de 5 routeurs, R1 est DR sur G0/0 : combien d'adjacences FULL sur l'interface ? | **C, 4, avec tous ses voisins** | Le DR est Full avec tous les voisins ; pas de relation avec lui-même (B, D faux) ; A ne compte que le BDR. |
| Q3. Conditions pour devenir voisins OSPF ? (2) | **A, timers Hello et Dead identiques ; D, interfaces dans la même aire** | Les process ID n'ont pas à correspondre ; les router ID doivent être **différents** ; même sous-réseau requis, pas différent. |
| Q4. Type de LSA généré seulement par le DR d'un réseau multi-accès ? | **B, type 2** (Network LSA) | Type 1 = Router LSA (chaque routeur) ; type 5 = AS-External (ASBR) ; type 3 = Summary, non traité. |
| Q5. R4 DR, R3 BDR, priorités par défaut ; `ip ospf priority 100` sur R1 G0/0 : deux affirmations vraies ? | **D**, après `clear ip ospf process` sur R4, R1 devient BDR ; **F**, DR et BDR inchangés | Non préemptif : R1 reste DROther (pas à cause de la priorité, C faux ; A, B faux). Si R4 est réinitialisé, le BDR R3 devient DR (E faux) et R1, priorité la plus haute, devient BDR. |
| Boson ExSim. `show ip ospf interface f0/1` sur Router1 (état DROTHER, type BROADCAST, timers par défaut, priorité 50, Neighbor Count 5, Adjacent neighbor count 2) : affirmation correcte ? | **D** (Router1, DROther, n'a d'adjacence qu'avec le DR et le BDR : 5 voisins, 2 adjacences) | A : Router1 n'est pas DR ; B : réseau broadcast, pas point-to-multipoint ; C : timers par défaut et 5 voisins ; E : le BDR peut avoir la même priorité 50 avec un router ID plus haut. |

---

## 🇬🇧 English version

### 1. Loopback interfaces

A **virtual** interface, **always up/up** unless manually shut down: its status does not depend on any physical interface (which can fail on hardware problems). It provides a **consistent IP address to reach and identify the router**: if R4 sends a packet to R1 at 10.0.13.1 (G1/0) and G1/0 goes down, the packet cannot be delivered; with loopback 1.1.1.1, R1 stays reachable through its other interfaces.

### 2. OSPF network types

The type of connection between neighbors influences OSPF's behavior. Three main types:

| Type | Default on | Neighbor discovery | DR/BDR | Hello/Dead timers |
| :--- | :--- | :--- | :--- | :--- |
| **Broadcast** (topic 3.4c) | **Ethernet**, FDDI | dynamic, Hello multicast 224.0.0.5 | **elected** on each subnet | **10 / 40 s** |
| **Point-to-point** (topic 3.4b) | serial links with **PPP** and **HDLC** | dynamic, 224.0.0.5 | **no election** (only two routers, direct Full adjacency) | **10 / 40 s** |
| Non-broadcast (not a CCNA topic) | Frame Relay, X.25 | neighbors configured **manually** | | 30 / 120 s |

#### 2.1 Broadcast: DR, BDR, DROther

- A **DR (Designated Router)** and a **BDR (Backup Designated Router)** must be elected on **each subnet**; on an interface with no neighbor (G1/0 of R1, R3, R4, R5) there is a DR but no BDR. The other routers on the subnet are **DROthers**.
- **Election**: 1) **highest OSPF interface priority** (default **1** on all interfaces, so a tie); 2) **highest router ID**. First place = DR, second = BDR. `ip ospf priority <0-255>` on the interface; **priority 0 = can never be DR/BDR**.
- The election is **non-preemptive**: after `ip ospf priority 255` on R2, R2 stays DROther; DR and BDR keep their roles until OSPF is reset, the interface fails or is shut down (preemption is revisited in Day 29 with FHRPs). After `clear ip ospf process` on R5 (the DR): **the BDR (R4) becomes DR** immediately, then an election picks the new BDR (R2, priority 255). R5 and R3 become DROthers.
- **DROthers only form a Full adjacency with the DR and BDR**; between DROthers the state stays **2-way** (R3 remains stable in 2-way with R5). The DR and BDR form a Full adjacency with **all** routers on the subnet. Purpose: reduce LSA flooding (6 routers all exchanging LSAs = lots of traffic; via DR/BDR, much less); all still have the same LSDB. Messages to the DR and BDR use multicast **224.0.0.6** (224.0.0.5 = all OSPF routers).
- `show ip ospf interface brief`: Nbrs column **F/C** = **Full** adjacencies / total neighbor **Count** (R3: 2 Full, 3 neighbors). `show ip ospf interface g0/0`: "Neighbor Count is 3, Adjacent neighbor count is 2", list of adjacent neighbors (BDR, DR). `show ip ospf interface` also shows State DR/BDR/DROTHER, Priority, Router ID and address of the DR and BDR.

#### 2.2 Point-to-point and serial links

- On a serial link (PPP or HDLC) between two routers, no DR/BDR: `show ip ospf neighbor` shows **a dash** instead of DR/BDR/DROTHER.
- Serial links (removed from the exam except for this network type): one side is **DCE (Data Communications Equipment)**, the other **DTE (Data Terminal Equipment)**. The **DCE sets the speed** with `clock rate <bits/s>` (e.g. 64000 = 64 kbps); Ethernet uses `speed`, serial uses `clock rate`. `show controllers s2/0` shows DCE or DTE (DTE side: "detected Tx and Rx clocks"). Default encapsulation **HDLC** (actually cHDLC, Cisco HDLC, displayed "HDLC"; frame with no MAC field); `encapsulation ppp` for PPP, **configured on both ends** or the interface goes down (two different "languages"). R1 config: clock rate, encapsulation, IP (`serial restart-delay 0` present by default); R2: no clock rate (DTE).
- `ip ospf network {broadcast | point-to-point | non-broadcast | point-to-multipoint}` on the interface to change the type (point-to-multipoint = a sub-type, not a CCNA topic). Two routers directly connected by Ethernet can use point-to-point (no needless DR/BDR), though not required. A serial link **cannot** use broadcast (no Layer 2 broadcast frames).

### 3. Requirements to become OSPF neighbors

1. **Same area** (area 0 on R1, area 1 on R2 → no neighbor; fix the network command).
2. **Same subnet** on the interfaces.
3. **OSPF process not shut down**: `shutdown` in OSPF mode disables OSPF without removing the config (neighbor FULL → DOWN); `no shutdown` restarts it.
4. **Unique router IDs**: with a duplicate `router-id 192.168.1.1` on R2 then `clear ip ospf process`, message "OSPF detected duplicate router-id 192.168.1.1 from 192.168.1.1 on interface GigabitEthernet0/0", neighbor stays down. `no router-id` (no value needed) fixes it; here with no clear because R2 had no other neighbor.
5. **Matching Hello and Dead timers**: `ip ospf hello-interval 5`, `ip ospf dead-interval 20` on the interface → neighbor down, even if only one of the two changes; `no ip ospf hello-interval`, `no ip ospf dead-interval` restore the defaults.
6. **Matching authentication**: `ip ospf authentication-key jeremy` configures the password on the interface, but only `ip ospf authentication` enables it; without a matching password on R1, neighbor down.
7. **Matching IP MTU** (special case: routers **do become neighbors** but OSPF does not work): `ip mtu 1400` on R2 (default 1500); after `clear ip ospf process`, neighbor stuck in **EXSTART**, repeating messages; `no ip mtu` → FULL.
8. **Same network type** (also a special case): R2 G0/0 point-to-point, R1 broadcast → neighbor **FULL** on both sides, but R2's loopback **does not appear** in R1's routing table. Troubleshooting trap: everything looks fine.

### 4. LSA types

11 types exist, 3 to know:

- **Type 1, Router LSA**: generated by **every OSPF router**; identifies the router by its router ID and lists the networks on its OSPF-activated interfaces.
- **Type 2, Network LSA**: generated by the **DR of each multi-access network** (e.g. Ethernet with the broadcast type); lists the routers attached to that network. Not generated when the DR has no neighbor on the interface (G1/0 of R1, R3, R5).
- **Type 5, AS-External LSA**: generated by an **ASBR** for destinations outside the OSPF domain (e.g. R4's default route after `default-information originate`).
- `show ip ospf database`: same output on every router in the area (same LSDB). Type 3 = Summary LSA, not covered.

### 5. Exam traps

- Point-to-point vs broadcast: **no DR/BDR election** in point-to-point; dynamic neighbor discovery is common to both.
- The DR has a Full adjacency with **all** its neighbors (4 neighbors on a 5-router segment = 4 adjacencies); a DROther has only 2 Full adjacencies (DR and BDR), other neighbors stay in 2-way: "Neighbor Count 5, Adjacent neighbor count 2" (Boson question).
- Election: highest priority then highest router ID; **non-preemptive**: raising the priority changes nothing while the current DR/BDR remain; if the DR goes down, the **BDR becomes DR** and the highest-priority router becomes BDR (Q5).
- Neighbor requirements: matching Hello/Dead timers and same area **yes**; matching process IDs **no**, matching router IDs **no** (they must be different).
- MTU and network type do not necessarily block the neighborship but break OSPF (stuck in Exstart; missing routes with a Full state).
- Type 2 = DR of a multi-access network; type 1 = every router; type 5 = ASBR.
- Serial: `clock rate` on the DCE side, HDLC by default, PPP on both ends, `show controllers`.
- Priority 0 = never DR/BDR. 224.0.0.6 = DR/BDR.

### 6. IOS commands

```
Router(config-if)# ip ospf priority 255                     ! interface priority (0-255, default 1; 0 = never DR/BDR)
Router(config-if)# ip ospf network point-to-point           ! change the network type (broadcast, non-broadcast, point-to-multipoint)
Router(config-if)# no ip ospf network point-to-point        ! back to the default type
Router(config-if)# ip ospf hello-interval 5                 ! Hello in seconds (default 10); no ... to restore
Router(config-if)# ip ospf dead-interval 20                 ! Dead in seconds (default 40); no ... to restore
Router(config-if)# ip ospf authentication-key jeremy        ! OSPF password
Router(config-if)# ip ospf authentication                   ! enables authentication on the interface
Router(config-if)# ip mtu 1400                              ! IP MTU in bytes (default 1500); no ip mtu to restore
Router(config-router)# shutdown                             ! stops the OSPF process without removing the config
Router(config-router)# no router-id                         ! removes the manual router ID
Router(config-if)# clock rate 64000                         ! speed in bits/s, DCE side only
Router(config-if)# encapsulation ppp                        ! replaces HDLC (default), on both ends
Router# show controllers s0/0/0                             ! DCE or DTE, clock rate
Router# show ip ospf interface [brief]                      ! network type, DR/BDR/DROTHER state, priority, timers, Nbrs F/C
Router# show ip ospf neighbor                               ! state, DR/BDR/DROTHER role or dash (point-to-point)
Router# show ip ospf database                               ! LSDB: Router (1), Net (2), Type-5 AS External (5)
Router# show running-config | section ospf                  ! filter the OSPF config
Router# clear ip ospf process                               ! resets OSPF (re-runs the DR/BDR election)
```

### 7. The lab (video 058, Configuring OSPF 3: configuration and troubleshooting)

Goal: a pre-configured network with a few errors; R1-R2 serial; R3-R4 Ethernet; R2, R4, R5 on 192.168.245.0/29; R5 to the Internet; PC1 and PC2 (10.0.2.0/24). Jeremy recommends trying it before watching.

1. **R1-R2 serial link**: R1 `interface s0/0/0`, `ip address 192.168.12.1 255.255.255.252`, `show controllers s0/0/0` → DCE → `clock rate 128000`, `no shutdown`. R2: IP 192.168.12.2, DTE confirmed, `no shutdown`. OSPF: R2 already runs OSPF on G0/0 (`show ip protocols`) → `ip ospf 1 area 0` on S0/0/0 (in a real network, stay consistent: all on interfaces or all with `network`). R1: `ip ospf 1 area 0` on S0/0/0 and G0/0. `show ip ospf interface s0/0/0`: **point-to-point** type by default (serial, HDLC), no DR/BDR, Hello 10 / Dead 40; G0/0: **broadcast**, R1 is DR, no BDR (no neighbor). `show ip route` on R1: two OSPF routes (192.168.34.0/30 and 192.168.245.0/29), some are missing.
2. **Only R3 has a route to 10.0.2.0/24**: on R4, `show ip ospf neighbor`: Full adjacency with R3, but no route. `show ip ospf interface g0/1`: R4 **broadcast**, R3 **point-to-point** → network type mismatch. On R3: `interface g0/1`, `no ip ospf network point-to-point`. R4 learns 10.0.2.0/24; ping PC1 → PC2 (10.0.2.1) succeeds.
3. **R2 and R4 do not become neighbors with R5**: `show ip ospf interface g0/0` on R2 and R4: subnet, area 0, default timers all correct. On R5: **Hello 5, Dead 20** → `no ip ospf hello-interval`, `no ip ospf dead-interval`; skip 30 s; `show ip ospf neighbor`: R2 and R4 are neighbors.
4. **PC1/PC2 cannot ping 8.8.8.8**: on R5, `show running-config | section ospf`: `default-information originate` is there, but `show ip route`: **no default route to advertise** → `ip route 0.0.0.0 0.0.0.0 203.0.113.2`. R5 then generates the type 5 LSA; R1 receives the default route; ping PC1 → 8.8.8.8 succeeds.
5. **LSDB**: `show ip ospf database` on R1 (identical everywhere): Router link states (type 1, one per router), Network link states (type 2, DR of multi-access networks), one Type-5 AS External (R5's default route).

Boson NetSim preview ("OSPF Routes"): hostnames, IPs, `show controllers s0/0` (DCE cable) and `clock rate 64000` on Router1, DTE on Router2; `router ospf 1`, `network ... 0.0.0.255 area 0` for each network; watching the states **INIT → EXSTART → EXCHANGE → (LOADING) → FULL** in `show ip ospf neighbor`; learned routes; ping HostA → HostB; lab grading.

### 8. The quiz (video 057: 5 questions, plus one Boson ExSim question)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Q1. Characteristic of the point-to-point type that differs from the broadcast type? | **B, DR and BDR elections are not held** | C (neighbors dynamically discovered) is true but also for broadcast. |
| Q2. Broadcast network with 5 routers, R1 is DR on G0/0: how many FULL adjacencies on the interface? | **C, 4, with all neighbors** | The DR is Full with all neighbors; no relationship with itself (B, D wrong); A counts only the BDR. |
| Q3. Requirements to become OSPF neighbors? (2) | **A, Hello and Dead timers must match; D, interfaces in the same area** | Process IDs need not match; router IDs must be **different**; same subnet required, not different. |
| Q4. LSA type generated only by the DR of a multi-access network? | **B, type 2** (Network LSA) | Type 1 = Router LSA (every router); type 5 = AS-External (ASBR); type 3 = Summary, not covered. |
| Q5. R4 DR, R3 BDR, default priorities; `ip ospf priority 100` on R1 G0/0: two true statements? | **D**, after `clear ip ospf process` on R4, R1 becomes BDR; **F**, DR and BDR unchanged | Non-preemptive: R1 stays DROther (not because of priority, C wrong; A, B wrong). If R4 is reset, BDR R3 becomes DR (E wrong) and R1, highest priority, becomes BDR. |
| Boson ExSim. `show ip ospf interface f0/1` on Router1 (state DROTHER, type BROADCAST, default timers, priority 50, Neighbor Count 5, Adjacent neighbor count 2): correct statement? | **D** (Router1, a DROther, only has adjacencies with the DR and BDR: 5 neighbors, 2 adjacencies) | A: Router1 is not the DR; B: broadcast network, not point-to-multipoint; C: default timers and 5 neighbors; E: the BDR may have the same priority 50 with a higher router ID. |
