# CCNA Day 16 : VLANs (Part 1) / VLAN, partie 1

> Source : Jeremy's IT Lab, « Free CCNA | VLANs (Part 1) | Day 16 » (24 min, vidéo n°29 de la playlist, cours) et « VLANs (Part 1) | Day 16 Lab » (11 min, vidéo n°30, lab Packet Tracer). Flashcards disponibles. Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Qu'est-ce qu'un LAN ? Le domaine de broadcast

- Définition précédente : un groupe d'équipements (PC, serveurs, routeurs, switches…) en un seul lieu. Définition plus précise : **un LAN est un domaine de broadcast** (*broadcast domain*).
- **Domaine de broadcast** : le groupe d'équipements qui recevront une trame de broadcast (adresse MAC de destination **FFFF.FFFF.FFFF**, « tous à F ») envoyée par l'un de ses membres.
- Un **switch** inonde (*flood*) la trame de broadcast sur toutes ses interfaces sauf celle de réception ; un **routeur** la reçoit mais **ne la transmet pas** à d'autres réseaux.
- Exemple de la vidéo : PC1-PC2-SW1 + une interface de R1 = 1 domaine ; PC3-PC4-PC5-SW2 + une interface de R1 = 1 ; PC6-PC7-PC8-SW3 + une interface de R2 = 1 ; **la liaison R1–R2 est aussi un domaine de broadcast** même avec deux équipements seulement. Total : **4 domaines de broadcast, donc 4 LAN**.

### 2. Pourquoi séparer les départements ?

Un LAN d'entreprise 192.168.1.0/24 avec trois services : ingénierie (*engineering*), ventes (*sales*), RH (*human resources*). Deux raisons de les séparer :

- **Performance** : le trafic de broadcast inutile (et les trames *unknown unicast* inondées) réduit les performances. Un broadcast destiné aux PC d'ingénierie est reçu par TOUS les PC et par le routeur.
- **Sécurité** : limiter qui accède à quoi. Les politiques de sécurité se configurent sur un routeur ou un pare-feu ; dans un même LAN, les PC communiquent **directement, sans passer par le routeur**, donc ces politiques n'ont aucun effet.

**Première tentative** : trois sous-réseaux, 192.168.1.0/26 pour l'ingénierie, 192.168.1.64/26 pour les RH, 192.168.1.128/26 pour les ventes. Le routeur a besoin d'une adresse (donc d'une interface) dans chaque sous-réseau : on remplace le lien unique switch–routeur par **trois liens** (il existe une méthode plus efficace, vue plus tard).

- Un trafic unicast PC1 (192.168.1.1) → PC2 (192.168.1.129) passe bien par R1 : PC1 voit que PC2 est dans un autre sous-réseau, met la MAC de destination = R1 (passerelle), R1 réécrit la MAC source (la sienne) et la MAC destination (PC2) et renvoie la trame au switch.
- **Mais** un broadcast (IP destination = broadcast du sous-réseau ingénierie, MAC destination tous à F) est quand même inondé partout : **le switch ne connaît que la couche 2**, il ignore les sous-réseaux. Séparés en couche 3, les trois services restent **dans le même domaine de broadcast**, le même LAN.
- Acheter un switch par service : peu flexible et coûteux.

### 3. Les VLAN (*Virtual LAN*)

- Un VLAN sépare les hôtes **en couche 2**, logiquement, bien qu'ils soient physiquement sur le même switch. Ingénierie = **VLAN10**, RH = **VLAN20**, ventes = **VLAN30**.
- Les VLAN se configurent **sur le switch, interface par interface** : l'hôte branché sur une interface en VLAN10 appartient au VLAN10.
- Le switch traite chaque VLAN comme un LAN distinct : **il ne transmet jamais de trafic directement entre deux VLAN**, ni broadcast, ni unknown unicast, ni unicast. Un broadcast arrivé sur une interface VLAN10 n'est inondé que vers les interfaces VLAN10.
- Le **routage inter-VLAN** (*inter-VLAN routing*) est fait par le **routeur**, pas par le switch (d'autres méthodes viendront). Même si PC1 et PC2 étaient dans le même sous-réseau, le switch ne transmettrait pas entre VLAN différents.

### 4. Configuration de base

- `show vlan brief` : VLAN existants et interfaces de chacun. Par défaut : **VLAN 1, nom « default », toutes les interfaces** (G0/0 à G3/3), plus **VLAN 1002 à 1005** (FDDI et Token Ring, technologies anciennes). **VLAN 1 et 1002-1005 existent par défaut et ne peuvent pas être supprimés.**
- **Port d'accès** (*access port*) : interface qui appartient à **un seul VLAN**, connecte en général un hôte final (il lui donne « accès » au réseau). **Port trunk** : transporte **plusieurs VLAN** (Day 17).
- Une interface reliée à un hôte devrait passer en mode access toute seule, mais **il faut le configurer explicitement** plutôt que compter sur l'autonégociation.
- `switchport access vlan 10` sur un VLAN inexistant : message « %Access VLAN does not exist. Creating vlan 10 », le switch **crée le VLAN automatiquement**.
- `vlan 10` crée aussi un VLAN (ou entre dans sa configuration) ; `name ENGINEERING` le nomme.
- Test : `ping 255.255.255.255` depuis PC1 (MAC destination tous à F) n'atteint que les hôtes du VLAN10.

### 5. Pièges d'examen

- Compter les domaines de broadcast : chaque interface de routeur et tout ce qui y est connecté, **plus la liaison routeur–routeur**.
- Un switch ne transmet **jamais** entre VLAN ; il faut un routeur.
- VLAN 1 et 1002-1005 : **par défaut, non supprimables** (3 VLAN créés → 8 affichés).
- Le VLAN est créé automatiquement quand on y affecte une interface.

### 6. Commandes IOS

```
Switch# show vlan brief                                 ! VLAN existants et interfaces d'accès de chaque VLAN
Switch(config)# interface range g1/0 - 3               ! configurer plusieurs interfaces à la fois
Switch(config)# interface range g0/1, f3/1, f4/1       ! variante avec virgules (lab)
Switch(config-if-range)# switchport mode access        ! port d'accès (un seul VLAN), à configurer explicitement
Switch(config-if-range)# switchport access vlan 10     ! affecte l'interface au VLAN 10 (le crée s'il n'existe pas)
Switch(config)# vlan 10                                ! crée le VLAN 10 / entre dans sa configuration
Switch(config-vlan)# name ENGINEERING                  ! nomme le VLAN
Router(config)# interface g0/0                         ! une interface de routeur par VLAN (lab)
Router(config-if)# ip address 10.0.0.62 255.255.255.192
Router(config-if)# no shutdown
Router(config-if)# do show ip interface brief           ! vérifie les adresses des interfaces
```

### 7. Le lab (vidéo n°30)

**Objectif** : ports d'accès sur SW1 pour trois VLAN (10 ingénierie, 20 RH, 30 ventes), un lien switch–routeur par VLAN, R1 passerelle de chaque sous-réseau (/26 de 10.0.0.0, masque 255.255.255.192).

| VLAN | PC | Adresses PC | Passerelle = R1 (dernière utilisable) | Interfaces SW1 | Lien vers R1 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 10 | PC1, PC2 | 10.0.0.1, 10.0.0.2 | 10.0.0.62 sur G0/0 | G0/1, F3/1, F4/1 | SW1 G0/1 – R1 G0/0 |
| 20 | PC3, PC4 | 10.0.0.65, 10.0.0.66 | 10.0.0.126 sur G0/1 | G1/1, F5/1, F6/1 | SW1 G1/1 – R1 G0/1 |
| 30 | PC5, PC6 | 10.0.0.129, 10.0.0.130 | 10.0.0.190 sur G0/2 | G2/1, F7/1, F8/1 | SW1 G2/1 – R1 G0/2 |

1. **PC** : onglet Config, Gateway, puis interface, IP et masque 255.255.255.192.
2. **Câblage** : trois câbles droits (*straight-through*) entre SW1 et R1 ; sur R1, `ip address` + `no shutdown` sur G0/0, G0/1, G0/2 ; `do show ip interface brief`.
3. **SW1** : `interface range ...`, `switchport mode access`, `switchport access vlan N` pour chaque VLAN ; `do show vlan brief` ; puis `vlan 10` / `name ENGINEERING`, `vlan 20` / `name HR`, `vlan 30` / `name SALES` ; `do show vlan brief`.
4. **Tests** depuis PC1 : `ping 10.0.0.65` (PC3, VLAN20) et `ping 10.0.0.129` (PC5, VLAN30) réussissent ; en mode simulation, le ping va PC1 → SW1 → R1 → SW1 → PC3 : **R1 fait le routage inter-VLAN** car il a une interface dans chaque VLAN. `ping 10.0.0.63` (broadcast du VLAN10) : SW1 ne l'envoie qu'à R1 et PC2.

### 8. Le quiz du Day 16 (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Combien de domaines de broadcast dans le schéma (aucun VLAN configuré, tout en VLAN1) ? | **6** | Chaque interface de routeur et ce qui y est connecté forme un domaine. |
| Combien de domaines de broadcast dans le schéma avec les VLAN configurés ? | **5** | Un par VLAN configuré, plus la liaison entre les deux routeurs. |
| Affecter une interface à un VLAN inexistant ? A) la commande échoue, B) le switch crée le VLAN, C) l'interface est désactivée, D) tous les VLAN existent par défaut | **B** | Le switch crée automatiquement le VLAN, comme montré dans la vidéo. |
| PC3 envoie un broadcast : combien d'équipements le reçoivent ? | **3** | Le switch, puis le routeur et l'autre PC du VLAN20. Sans VLAN, tous les PC le recevraient. |
| VLAN 10, 20 et 30 créés : combien de VLAN dans `show vlan brief` ? A) 3, B) 5, C) 8, D) 10 | **C, 8** | VLAN 1 et 1002-1005 existent par défaut et ne peuvent pas être supprimés : 5 + 3 = 8. |

---

## 🇬🇧 English version

### 1. What is a LAN? The broadcast domain

- Earlier definition: a group of devices (PCs, servers, routers, switches...) in a single location. More specific definition: **a LAN is a single broadcast domain**.
- **Broadcast domain**: the group of devices which will receive a broadcast frame (destination MAC **FFFF.FFFF.FFFF**, "all Fs") sent by any one of the members.
- A **switch** floods a broadcast frame out of all interfaces except the one it was received on; a **router** receives it but **does not forward it** to other networks.
- Video example: PC1-PC2-SW1 + one R1 interface = 1 domain; PC3-PC4-PC5-SW2 + one R1 interface = 1; PC6-PC7-PC8-SW3 + one R2 interface = 1; **the R1–R2 link is also a broadcast domain** even with only two devices. Total: **4 broadcast domains, therefore 4 LANs**.

### 2. Why separate the departments?

A company LAN 192.168.1.0/24 with three departments: engineering, sales, human resources. Two reasons to split them:

- **Performance**: unnecessary broadcast traffic (and flooded unknown unicast frames) reduces network performance. A broadcast intended for engineering PCs is received by ALL PCs and the router.
- **Security**: limit who has access to what. Security policies are applied on a router or firewall; within one LAN, PCs reach each other **directly, without passing through the router**, so those policies have no effect.

**First attempt**: three subnets, 192.168.1.0/26 for engineering, 192.168.1.64/26 for HR, 192.168.1.128/26 for sales. The router needs an IP address (so an interface) in each subnet: replace the single switch–router link with **three links** (a more efficient way exists, covered later).

- Unicast traffic PC1 (192.168.1.1) → PC2 (192.168.1.129) does go through R1: PC1 sees PC2 is in a different subnet, sets destination MAC = R1 (default gateway), R1 changes the source MAC (its own) and destination MAC (PC2) and sends the frame back to the switch.
- **But** a broadcast (destination IP = engineering subnet broadcast, destination MAC all Fs) is still flooded everywhere: **the switch is only aware up to Layer 2**, it does not know about subnets. Separated at Layer 3, the three departments are still **in the same broadcast domain**, the same LAN.
- Buying one switch per department: not flexible and expensive.

### 3. VLANs (Virtual LANs)

- A VLAN separates hosts **at Layer 2**, logically, even though they are physically connected to the same switch. Engineering = **VLAN10**, HR = **VLAN20**, sales = **VLAN30**.
- VLANs are configured **on the switch, per interface**: the host connected to an interface in VLAN10 is part of VLAN10.
- The switch considers each VLAN a separate LAN: **it never forwards traffic directly between two VLANs**, neither broadcast, unknown unicast nor unicast. A broadcast arriving on a VLAN10 interface is only flooded to VLAN10 interfaces.
- **Inter-VLAN routing** is performed by the **router**, not the switch (other methods come later). Even if PC1 and PC2 were in the same subnet, the switch would not forward between different VLANs.

### 4. Basic configuration

- `show vlan brief`: existing VLANs and the interfaces in each. By default: **VLAN 1, named "default", all interfaces** (G0/0 to G3/3), plus **VLANs 1002 to 1005** (FDDI and Token Ring, old technologies). **VLANs 1 and 1002-1005 exist by default and cannot be deleted.**
- **Access port**: a switchport that belongs to **a single VLAN**, usually connects to end hosts (it gives them "access" to the network). **Trunk port**: carries **multiple VLANs** (Day 17).
- A switchport connected to an end host should enter access mode by default, but **always configure it explicitly** rather than relying on autonegotiation of port type.
- `switchport access vlan 10` on a non-existent VLAN: message "%Access VLAN does not exist. Creating vlan 10", the switch **creates the VLAN automatically**.
- `vlan 10` also creates a VLAN (or enters its configuration mode); `name ENGINEERING` names it.
- Test: `ping 255.255.255.255` from PC1 (destination MAC all Fs) only reaches hosts in VLAN10.

### 5. Exam traps

- Counting broadcast domains: each router interface and everything connected to it, **plus the router-to-router link**.
- A switch **never** forwards between VLANs; a router is needed.
- VLANs 1 and 1002-1005: **exist by default, cannot be deleted** (3 VLANs created → 8 displayed).
- The VLAN is created automatically when an interface is assigned to it.

### 6. IOS commands

```
Switch# show vlan brief                                 ! existing VLANs and the access ports in each
Switch(config)# interface range g1/0 - 3               ! configure several interfaces at once
Switch(config)# interface range g0/1, f3/1, f4/1       ! comma variant (lab)
Switch(config-if-range)# switchport mode access        ! access port (single VLAN), configure it explicitly
Switch(config-if-range)# switchport access vlan 10     ! assigns the interface to VLAN 10 (creates it if needed)
Switch(config)# vlan 10                                ! creates VLAN 10 / enters its configuration
Switch(config-vlan)# name ENGINEERING                  ! names the VLAN
Router(config)# interface g0/0                         ! one router interface per VLAN (lab)
Router(config-if)# ip address 10.0.0.62 255.255.255.192
Router(config-if)# no shutdown
Router(config-if)# do show ip interface brief           ! check interface addresses
```

### 7. The lab (video 30)

**Objective**: access ports on SW1 for three VLANs (10 engineering, 20 HR, 30 sales), one switch–router link per VLAN, R1 as the gateway of each subnet (/26 of 10.0.0.0, mask 255.255.255.192).

| VLAN | PCs | PC addresses | Gateway = R1 (last usable) | SW1 interfaces | Link to R1 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 10 | PC1, PC2 | 10.0.0.1, 10.0.0.2 | 10.0.0.62 on G0/0 | G0/1, F3/1, F4/1 | SW1 G0/1 – R1 G0/0 |
| 20 | PC3, PC4 | 10.0.0.65, 10.0.0.66 | 10.0.0.126 on G0/1 | G1/1, F5/1, F6/1 | SW1 G1/1 – R1 G0/1 |
| 30 | PC5, PC6 | 10.0.0.129, 10.0.0.130 | 10.0.0.190 on G0/2 | G2/1, F7/1, F8/1 | SW1 G2/1 – R1 G0/2 |

1. **PCs**: Config tab, Gateway, then interface, IP and mask 255.255.255.192.
2. **Cabling**: three straight-through cables between SW1 and R1; on R1, `ip address` + `no shutdown` on G0/0, G0/1, G0/2; `do show ip interface brief`.
3. **SW1**: `interface range ...`, `switchport mode access`, `switchport access vlan N` for each VLAN; `do show vlan brief`; then `vlan 10` / `name ENGINEERING`, `vlan 20` / `name HR`, `vlan 30` / `name SALES`; `do show vlan brief`.
4. **Tests** from PC1: `ping 10.0.0.65` (PC3, VLAN20) and `ping 10.0.0.129` (PC5, VLAN30) succeed; in simulation mode the ping goes PC1 → SW1 → R1 → SW1 → PC3: **R1 does the inter-VLAN routing** because it has one interface in each VLAN. `ping 10.0.0.63` (VLAN10 broadcast): SW1 only forwards it to R1 and PC2.

### 8. Day 16 quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| How many broadcast domains in the diagram (no VLANs configured, all in VLAN1)? | **6** | Each router interface and everything connected to it is one broadcast domain. |
| How many broadcast domains in the diagram with the configured VLANs? | **5** | One for each configured VLAN, plus the connection between the two routers. |
| Assign a switch interface to a VLAN that doesn't exist? A) command fails, B) switch creates the VLAN, C) interface disabled, D) all VLANs exist by default | **B** | The switch creates the VLAN automatically, as shown in the video. |
| PC3 sends a broadcast: how many devices receive it? | **3** | The switch, then the router and the other PC in VLAN20. Without VLANs, all PCs would receive it. |
| VLANs 10, 20, 30 created: how many VLANs in `show vlan brief`? A) 3, B) 5, C) 8, D) 10 | **C, 8** | VLANs 1 and 1002-1005 exist by default and cannot be deleted: 5 + 3 = 8. |
