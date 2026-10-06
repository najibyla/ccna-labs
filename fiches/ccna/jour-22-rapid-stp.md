# CCNA Day 22 : Rapid Spanning Tree Protocol / Rapid STP

> Source : Jeremy's IT Lab, « Free CCNA | Rapid Spanning Tree Protocol | Day 22 » (cours, 43 min, vidéo n°45 de la playlist) et « Rapid STP | Day 22 Lab » (lab, 20 min, vidéo n°46). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Les versions de STP

| Standard IEEE | Version Cisco | Caractéristique |
| :--- | :--- | :--- |
| **802.1D** STP classique (publié en 1990, créé en 1985) | **PVST+** (Per-VLAN Spanning Tree Plus ; l'ancien PVST ne supportait qu'ISL) | 802.1D : **une seule instance** STP partagée par tous les VLAN, donc pas de load balancing. PVST+ : une instance par VLAN (d'où `spanning-tree vlan 1 root primary`), load balancing possible. Lent : jusqu'à 50 s (Max Age 20 s + Listening 15 s + Learning 15 s). |
| **802.1w** Rapid STP | **Rapid PVST+** | Convergence beaucoup plus rapide. 802.1w standard : une seule instance, pas de load balancing. Rapid PVST+ : une instance par VLAN. C'est la version de la liste des sujets d'examen et celle qu'on utilise sur les réseaux petits et moyens. |
| **802.1s** MSTP (Multiple Spanning Tree) | aucune (Cisco utilise le standard) | Mécanique RSTP modifiée ; regroupe plusieurs VLAN par instance (ex. VLAN 1-100 instance 1, 101-200 instance 2) : load balancing standard, bien plus simple à gérer avec de nombreux VLAN. Préférable pour les grands réseaux. |

Jeremy utilise RSTP et Rapid PVST+ de façon interchangeable : Rapid PVST+ = RSTP + une instance par VLAN.

### 2. RSTP : une évolution, pas une révolution

Résumé Cisco : RSTP n'est **pas un algorithme basé sur des timers** comme 802.1D. Le cœur du protocole est un **handshake (négociation) bridge à bridge** qui permet aux ports de passer directement en Forwarding. Jeremy ne détaille pas la négociation (pas nécessaire au CCNA).

**Identique à STP :**
- Même but : bloquer des ports pour éviter les boucles de couche 2.
- **Root bridge** : le switch avec le **bridge ID le plus bas**.
- **Root port** : l'interface avec le **coût vers la racine le plus bas** ; tiebreakers : **bridge ID du voisin**, puis **port ID du voisin**.
- **Designated port** : l'interface du switch avec le coût vers la racine le plus bas ; en cas d'égalité, le switch avec le **bridge ID le plus bas**.

**Différent :**
- **Coûts de port RSTP** (étendus pour les hauts débits ; STP classique définit jusqu'à 10 Gbps, au-delà coût 1) : 10 Mbps = **2 000 000** ; 100 Mbps = **200 000** ; 1 Gbps = **20 000** ; 10 Gbps = **2 000** ; 100 Gbps = **200** ; 1 Tbps = **20** ; 10 Tbps = 2.
- **États de port** : trois seulement. Blocking et Disabled fusionnés en **Discarding** ; Listening supprimé. Reste **Discarding, Learning, Forwarding**. Un port en `shutdown` est Discarding, un port actif qui bloque est Discarding.
- **Rôles de port** : quatre. **Root** (inchangé : port le plus proche de la racine, le root bridge n'en a pas), **Designated** (inchangé : port qui envoie la meilleure BPDU sur le segment = domaine de collision, un seul par segment), et le rôle non désigné divisé en deux :
  - **Alternate** : port Discarding qui reçoit une BPDU supérieure **d'un autre switch**. Backup du **root port** : si le root port tombe, le meilleur port alternate devient immédiatement root port, sans état transitoire (fonction équivalente à **UplinkFast**).
  - **Backup** : port Discarding qui reçoit une BPDU supérieure **d'une autre interface du même switch**. Seulement avec un **hub** (deux interfaces dans le même domaine de collision). Backup du **designated port** : si celui-ci tombe, le port backup devient immédiatement designated. Entre les deux, le **port ID le plus bas** devient designated.
- **BPDU** : Protocol Version **2** (0 en STP classique), BPDU Type **2** ; les **8 bits de flags** sont utilisés (STP classique n'utilise que le 1er et le 8e), pour la négociation.
- **Tous les switches émettent leurs propres BPDU** depuis leurs ports désignés (en STP classique, seul le root en émet, les autres les transfèrent).
- **Vieillissement** : STP classique attend 10 intervalles Hello (20 s) ; RSTP considère un voisin perdu après **3 BPDU manquées (6 s)** et **efface (flush)** les adresses MAC apprises sur cette interface.
- Fonctions classiques **intégrées à RSTP** sans configuration : **UplinkFast**, **BackboneFast** (quand un switch perd son root port et se déclare root, le voisin fait expirer son Max Age et transmet rapidement les BPDU supérieures) et **PortFast** (edge port). Connaître leurs noms et leur but : aider les ports bloqués à passer en Forwarding sans délai.
- **Compatibilité** : RSTP est compatible avec STP classique ; les interfaces reliées à un vieux switch 802.1D fonctionnent en mode classique (mêmes timers, Blocking→Listening→Learning→Forwarding), les autres restent en RSTP.

### 3. Les types de lien (link types) RSTP

Ne pas confondre avec les rôles et les états.

- **Edge** : port relié à un **hôte final**, passe directement en Forwarding sans négociation. C'est PortFast : on configure un edge port avec `spanning-tree portfast`.
- **Point-to-point** : connexion directe à un autre switch, **full-duplex**. Détecté automatiquement ; configurable avec `spanning-tree link-type point-to-point`.
- **Shared** : connexion à un **hub**, **half-duplex** (collisions). Détecté automatiquement ; `spanning-tree link-type shared`. Pratiquement jamais vu (plus de hubs).

Précision du lab : point-to-point et shared distinguent full/half duplex, et **l'un ou l'autre peut aussi être edge** ; sur un switch réel, `show spanning-tree` affiche « P2p Edge » ou « Shr Edge » (pas dans Packet Tracer).

### 4. CLI

`spanning-tree mode rapid-pvst` (défaut des switches modernes). `show spanning-tree` affiche « Spanning tree enabled protocol **rstp** » (« ieee » en STP classique) ; les rôles **Altn** et **Back** apparaissent, mais l'état est toujours écrit **BLK** (blocking) alors que son nom RSTP est discarding.

### 5. Pièges d'examen

- Version de protocole dans la BPDU : **0** = STP classique, **2** = RSTP.
- En RSTP **tous les switches** envoient des BPDU, pas seulement le root.
- Trois états (Discarding, Learning, Forwarding), quatre rôles (Root, Designated, Alternate, Backup).
- Alternate = BPDU supérieure d'un **autre switch** ; Backup = BPDU supérieure du **même switch** (hub).
- Coûts RSTP : 20 000 pour 1 Gbps, 200 000 pour 100 Mbps, 2 000 000 pour 10 Mbps.
- UplinkFast, BackboneFast, PortFast sont intégrés à RSTP ; Root Guard, BPDU Guard, Loop Guard ne le sont pas. « RootFast » n'existe pas.
- Un edge port se configure avec `spanning-tree portfast`, pas `spanning-tree link-type edge` (la commande link-type n'a pas d'option edge).
- Le root bridge a un **designated port par domaine de collision**, pas forcément sur toutes ses interfaces : avec un hub, sa deuxième interface est backup.
- Un hub ne participe pas à STP et **n'ajoute aucun coût** : la sélection se fait alors sur le bridge ID du voisin.

### 6. Commandes IOS

```
Switch(config)# spanning-tree mode rapid-pvst             ! Rapid PVST+ (défaut sur les switches modernes)
Switch(config-if)# spanning-tree portfast                 ! edge port (= PortFast)
Switch(config-if)# spanning-tree link-type point-to-point ! lien full-duplex vers un switch (détecté par défaut)
Switch(config-if)# spanning-tree link-type shared         ! lien half-duplex vers un hub (détecté par défaut)
Switch(config)# interface range f0/1 - 2                  ! configurer plusieurs interfaces à la fois
Switch# show spanning-tree                                ! protocol rstp, rôles Root/Desg/Altn/Back, type P2p/Shr/Edge
```

### 7. Le lab (vidéo 046)

Objectif : analyser une topologie RSTP (rôles, types de lien), un seul VLAN, quatre switches, un hub relié à SW1 (F0/2, F0/3, F0/24) et à SW3 (F0/2), des PC.

1. **Root bridge** : toutes les priorités valent 32769 (32768 + VLAN 1), on compare les MAC : SW1 (000**5**...) est plus basse que SW3 (000**C**..., C = 12). `show spanning-tree` sur SW1 : F0/2, F0/1, F0/24 désignés Forwarding, **F0/3 backup, Discarding** (affiché blocking) : F0/2 et F0/3 sont dans le même domaine de collision via le hub, un seul designated port par domaine. En STP classique F0/3 serait non désigné.
2. **Rôles sans le CLI** : SW2 root port F0/1 (coût 19). SW3 root port F0/2 (le hub n'ajoute pas de coût, 19). SW4 : coûts égaux, voisin au bridge ID le plus bas = SW3 → root port F0/1. Designated : SW3 F0/1 ; sur le lien Gigabit SW2-SW3 (même coût 19), SW3 a le bridge ID le plus bas → SW3 G0/1 designated ; sur SW2-SW4, SW2 a le coût le plus bas → SW2 F0/2 designated. Donc SW2 G0/1 et SW4 F0/2 sont **alternate**, Discarding. Les ports vers les PC sont désignés. Vérification `show spanning-tree` sur SW2, SW3, SW4 : conforme.
3. **Types de lien** : sur SW4, `interface range f0/1 - 2`, `spanning-tree link-type point-to-point` (déjà le cas par défaut) ; `interface f0/24`, `spanning-tree portfast` : le type reste « P2p » dans Packet Tracer (sur un vrai switch : edge et point-to-point). SW3 : F0/2 vers le hub est déjà **Shr** automatiquement ; seul PortFast doit être configuré (F0/24). SW2 : tout est P2p, PortFast sur F0/23-24. SW1 : F0/2, F0/3, F0/24 sont **shared** ; F0/24 relie des hôtes via le hub : c'est quand même un **edge port** (le hub n'existe pas pour STP) → `spanning-tree portfast` ; sur un vrai switch, « Shr Edge ».

Aperçu Boson NetSim (lab ENCOR « Spanning Tree 1 ») : tâche 1 = VLAN 3, trunks (`interface range f0/1 - 3`, `switchport mode trunk`, `vlan 3`, `interface range f0/1 , f0/3` pour des interfaces non contiguës), `ipconfig` et `ping` sur les PC ; tâches 2-3 = router-on-a-stick et observation de STP ; fonction de notation du lab.

### 8. Le quiz (vidéo 045 : Q1 en cours de vidéo, Q2 à Q4, plus une question Boson ExSim)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Q1. Topologie avec un hub entre SW3 et SW4 : root bridge et rôle RSTP de chaque port ? | Root = **SW1** (mêmes priorités, MAC la plus basse), ses ports designated. SW4 choisit G0/1 (voisin SW2, bridge ID plus bas que SW3 ; le hub n'ajoute pas de coût). Sur SW3-hub-SW4 : SW3 a le coût le plus bas, **SW3 G0/0** (port ID le plus bas) designated, **SW3 G0/1 backup** (BPDU supérieure du même switch), **SW4 G0/0 alternate** (BPDU supérieure d'un autre switch). | Mêmes règles que STP pour root, root port, designated ; backup vs alternate selon l'origine de la BPDU supérieure. |
| Q2. Fonctions optionnelles 802.1D intégrées à 802.1w qui permettent le passage rapide en Forwarding ? (3) | **B PortFast, D UplinkFast, E BackboneFast** | Root Guard, BPDU Guard, Loop Guard sont des fonctions optionnelles mais pas intégrées pour accélérer le Forwarding ; RootFast n'existe pas. |
| Q3. Configurer un edge port 802.1w : quelle commande ? | **D, `spanning-tree portfast`** | « edge » est un type de lien mais ne se configure pas avec `link-type` ; `spanning-tree mode edge` et `link-type portfast` n'existent pas. |
| Q4. Topologie plus grande avec hub : root bridge, rôle de chaque port, type de lien de chaque connexion ? | Root = **SW1** (priorité la plus basse). SW4 choisit G0/0 car SW3 a un bridge ID plus bas que SW2 (même coût, hub sans coût). SW2 designated plutôt que SW4 (coût plus bas). **SW2 G0/2 backup** (BPDU supérieure de son propre G0/1). Ports vers PC = **edge** ; liens switch-switch full-duplex = **point-to-point** ; liens vers le hub, half-duplex = **shared**. | Si difficulté, revoir les vidéos STP. |
| Boson ExSim. Fonction STP optionnelle qui réduit la convergence en plaçant immédiatement les **edge ports** en Forwarding ? | **C, PortFast** | Un edge port est relié à un hôte final ; Root Guard, BPDU Guard, BPDU Filter, Loop Guard ont d'autres rôles. |

---

## 🇬🇧 English version

### 1. STP versions

| IEEE standard | Cisco version | Characteristic |
| :--- | :--- | :--- |
| **802.1D** classic STP (published 1990, created 1985) | **PVST+** (Per-VLAN Spanning Tree Plus; the older PVST only supported ISL) | 802.1D: **one STP instance** shared by all VLANs, so no load balancing. PVST+: one instance per VLAN (hence `spanning-tree vlan 1 root primary`), load balancing possible. Slow: up to 50 s (Max Age 20 s + Listening 15 s + Learning 15 s). |
| **802.1w** Rapid STP | **Rapid PVST+** | Much faster convergence. Standard 802.1w: one instance, no load balancing. Rapid PVST+: one instance per VLAN. The version in the exam topics list, and the one used in small to medium networks. |
| **802.1s** MSTP (Multiple Spanning Tree) | none (Cisco runs the standard) | Modified RSTP mechanics; groups several VLANs per instance (e.g. VLANs 1-100 in instance 1, 101-200 in instance 2): standard load balancing, much easier to manage with many VLANs. Best for large networks. |

Jeremy uses RSTP and Rapid PVST+ interchangeably: Rapid PVST+ = RSTP + one instance per VLAN.

### 2. RSTP: an evolution, not a revolution

Cisco's summary: RSTP is **not a timer-based** algorithm like 802.1D. The heart of the protocol is a **bridge-to-bridge handshake** that lets ports move directly to Forwarding. Jeremy does not detail the negotiation (not needed for the CCNA).

**Same as STP:**
- Same purpose: block specific ports to prevent Layer 2 loops.
- **Root bridge**: the switch with the **lowest bridge ID**.
- **Root port**: the interface with the **lowest root cost**; tiebreakers: **neighbor bridge ID**, then **neighbor port ID**.
- **Designated port**: the interface on the switch with the lowest root cost; on a tie, the switch with the **lowest bridge ID**.

**Different:**
- **RSTP port costs** (expanded for faster speeds; classic STP defines up to 10 Gbps, faster is cost 1): 10 Mbps = **2,000,000**; 100 Mbps = **200,000**; 1 Gbps = **20,000**; 10 Gbps = **2,000**; 100 Gbps = **200**; 1 Tbps = **20**; 10 Tbps = 2.
- **Port states**: only three. Blocking and Disabled merged into **Discarding**; Listening removed. Remaining: **Discarding, Learning, Forwarding**. A shut down port is Discarding, an enabled port blocking traffic is Discarding.
- **Port roles**: four. **Root** (unchanged: port closest to the root, the root bridge has none), **Designated** (unchanged: port sending the best BPDU on the segment = collision domain, only one per segment), and the non-designated role split in two:
  - **Alternate**: a Discarding port receiving a superior BPDU **from another switch**. Backup for the **root port**: if the root port fails, the best alternate port immediately becomes root port, no transitional states (works like **UplinkFast**).
  - **Backup**: a Discarding port receiving a superior BPDU **from another interface on the same switch**. Only with a **hub** (two interfaces in the same collision domain). Backup for the **designated port**: if it fails, the backup port immediately becomes designated. Between the two, the **lowest port ID** is designated.
- **BPDU**: Protocol Version **2** (0 in classic STP), BPDU Type **2**; all **8 flag bits** are used (classic STP uses only the 1st and 8th), for the negotiation.
- **All switches originate their own BPDUs** from their designated ports (in classic STP only the root originates them, the others forward them).
- **Aging**: classic STP waits 10 hello intervals (20 s); RSTP considers a neighbor lost after **3 missed BPDUs (6 s)** and **flushes** the MAC addresses learned on that interface.
- Classic features **built into RSTP** with no configuration: **UplinkFast**, **BackboneFast** (when a switch loses its root port and claims to be root, the neighbor expires its Max Age and rapidly forwards the superior BPDUs) and **PortFast** (edge port). Know their names and purpose: help blocking/discarding ports move to Forwarding without delay.
- **Compatibility**: RSTP is compatible with classic STP; interfaces connected to an old 802.1D switch operate in classic mode (same timers, Blocking→Listening→Learning→Forwarding), the others stay in RSTP.

### 3. RSTP link types

Do not confuse with port roles and states.

- **Edge**: port connected to an **end host**, moves directly to Forwarding without negotiation. This is PortFast: an edge port is configured with `spanning-tree portfast`.
- **Point-to-point**: direct connection to another switch, **full-duplex**. Detected automatically; configurable with `spanning-tree link-type point-to-point`.
- **Shared**: connection to a **hub**, **half-duplex** (collisions). Detected automatically; `spanning-tree link-type shared`. Practically never seen (no more hubs).

Lab clarification: point-to-point and shared distinguish full/half duplex, and **either can also be edge**; on a real switch `show spanning-tree` shows "P2p Edge" or "Shr Edge" (not in Packet Tracer).

### 4. CLI

`spanning-tree mode rapid-pvst` (default on modern switches). `show spanning-tree` shows "Spanning tree enabled protocol **rstp**" ("ieee" in classic STP); the **Altn** and **Back** roles appear, but the state is still written **BLK** (blocking) although its RSTP name is discarding.

### 5. Exam traps

- Protocol version in the BPDU: **0** = classic STP, **2** = RSTP.
- In RSTP **all switches** send BPDUs, not just the root.
- Three states (Discarding, Learning, Forwarding), four roles (Root, Designated, Alternate, Backup).
- Alternate = superior BPDU from **another switch**; Backup = superior BPDU from the **same switch** (hub).
- RSTP costs: 20,000 for 1 Gbps, 200,000 for 100 Mbps, 2,000,000 for 10 Mbps.
- UplinkFast, BackboneFast, PortFast are built into RSTP; Root Guard, BPDU Guard, Loop Guard are not. "RootFast" does not exist.
- An edge port is configured with `spanning-tree portfast`, not `spanning-tree link-type edge` (the link-type command has no edge option).
- The root bridge has **one designated port per collision domain**, not necessarily on all its interfaces: with a hub, its second interface is backup.
- A hub does not participate in STP and **adds no cost**: selection then falls to the neighbor bridge ID.

### 6. IOS commands

```
Switch(config)# spanning-tree mode rapid-pvst             ! Rapid PVST+ (default on modern switches)
Switch(config-if)# spanning-tree portfast                 ! edge port (= PortFast)
Switch(config-if)# spanning-tree link-type point-to-point ! full-duplex link to a switch (detected by default)
Switch(config-if)# spanning-tree link-type shared         ! half-duplex link to a hub (detected by default)
Switch(config)# interface range f0/1 - 2                  ! configure several interfaces at once
Switch# show spanning-tree                                ! protocol rstp, roles Root/Desg/Altn/Back, type P2p/Shr/Edge
```

### 7. The lab (video 046)

Goal: analyse an RSTP topology (roles, link types), single VLAN, four switches, a hub connected to SW1 (F0/2, F0/3, F0/24) and SW3 (F0/2), PCs.

1. **Root bridge**: all priorities are 32769 (32768 + VLAN 1), compare MACs: SW1 (000**5**...) is lower than SW3 (000**C**..., C = 12). `show spanning-tree` on SW1: F0/2, F0/1, F0/24 designated Forwarding, **F0/3 backup, Discarding** (shown as blocking): F0/2 and F0/3 are in the same collision domain via the hub, one designated port per domain. In classic STP F0/3 would be non-designated.
2. **Roles without the CLI**: SW2 root port F0/1 (cost 19). SW3 root port F0/2 (the hub adds no cost, 19). SW4: equal costs, neighbor with the lowest bridge ID = SW3 → root port F0/1. Designated: SW3 F0/1; on the Gigabit SW2-SW3 link (same cost 19), SW3 has the lower bridge ID → SW3 G0/1 designated; on SW2-SW4, SW2 has the lower cost → SW2 F0/2 designated. So SW2 G0/1 and SW4 F0/2 are **alternate**, Discarding. Ports to PCs are designated. Checked with `show spanning-tree` on SW2, SW3, SW4: correct.
3. **Link types**: on SW4, `interface range f0/1 - 2`, `spanning-tree link-type point-to-point` (already the default); `interface f0/24`, `spanning-tree portfast`: the type stays "P2p" in Packet Tracer (on a real switch: edge and point-to-point). SW3: F0/2 to the hub is already **Shr** automatically; only PortFast needs configuring (F0/24). SW2: all P2p, PortFast on F0/23-24. SW1: F0/2, F0/3, F0/24 are **shared**; F0/24 reaches hosts through the hub: still an **edge port** (the hub does not exist for STP) → `spanning-tree portfast`; on a real switch "Shr Edge".

Boson NetSim preview (ENCOR lab "Spanning Tree 1"): task 1 = VLAN 3, trunks (`interface range f0/1 - 3`, `switchport mode trunk`, `vlan 3`, `interface range f0/1 , f0/3` for non-contiguous interfaces), `ipconfig` and `ping` on the PCs; tasks 2-3 = router-on-a-stick and observing STP; lab grading function.

### 8. The quiz (video 045: Q1 mid-video, Q2 to Q4, plus one Boson ExSim question)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Q1. Topology with a hub between SW3 and SW4: root bridge and RSTP role of each port? | Root = **SW1** (same priorities, lowest MAC), its ports designated. SW4 picks G0/1 (neighbor SW2, lower bridge ID than SW3; the hub adds no cost). On SW3-hub-SW4: SW3 has the lower root cost, **SW3 G0/0** (lower port ID) designated, **SW3 G0/1 backup** (superior BPDU from the same switch), **SW4 G0/0 alternate** (superior BPDU from another switch). | Same rules as STP for root, root port, designated; backup vs alternate depends on where the superior BPDU comes from. |
| Q2. Which 802.1D optional features were built into 802.1w and allow ports to move rapidly to Forwarding? (3) | **B PortFast, D UplinkFast, E BackboneFast** | Root Guard, BPDU Guard, Loop Guard are optional features but not built in to speed up Forwarding; RootFast is not real. |
| Q3. Configure an 802.1w edge port: which command? | **D, `spanning-tree portfast`** | "edge" is a link type but is not configured with `link-type`; `spanning-tree mode edge` and `link-type portfast` do not exist. |
| Q4. Larger topology with a hub: root bridge, role of each port, link type of each connection? | Root = **SW1** (lowest priority). SW4 picks G0/0 because SW3 has a lower bridge ID than SW2 (same cost, hub adds none). SW2 designated rather than SW4 (lower root cost). **SW2 G0/2 backup** (superior BPDU from its own G0/1). Ports to PCs = **edge**; full-duplex switch-switch links = **point-to-point**; half-duplex links to the hub = **shared**. | If this is hard, review the STP videos. |
| Boson ExSim. Optional STP feature that reduces convergence time by immediately placing **edge ports** in Forwarding? | **C, PortFast** | An edge port connects to an end host; Root Guard, BPDU Guard, BPDU Filter, Loop Guard have other roles. |
