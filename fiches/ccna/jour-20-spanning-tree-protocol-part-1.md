# CCNA Day 20 : Spanning Tree Protocol (Part 1) / STP, partie 1

> Source : Jeremy's IT Lab, « Free CCNA | Spanning Tree Protocol (Part 1) | Day 20 » (39 min, vidéo n°37 de la playlist, cours) et « Analyzing STP | Day 20 Lab » (19 min, vidéo n°38, lab Packet Tracer avec aperçu Boson NetSim pour CCNP ENCOR). Flashcards disponibles. Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. La redondance dans les réseaux

- Un réseau doit tourner 24 h/24, 7 j/7, 365 j/an ; même une courte panne peut être désastreuse. Si un composant tombe, un autre doit prendre le relais ; **redondance à chaque point possible**.
- Mauvaise conception : un seul lien vers Internet, un seul lien switch–switch = points de défaillance uniques. Bonne conception : plusieurs routeurs, plusieurs chemins entre switches.
- Limite : un PC n'a généralement **qu'une seule carte réseau (NIC)**, donc un seul switch ; les serveurs importants ont **plusieurs NIC** pour se brancher sur plusieurs switches.
- STP est un protocole de **couche 2** : il permet des LAN redondants, pas le routage entre réseaux.

### 2. Le problème sans STP : la tempête de broadcast

- Trois switches en triangle, PC1 (10.0.0.1), PC2 (10.0.0.2), PC3 (10.0.0.3). PC1 envoie une **requête ARP** (broadcast, MAC destination tous à F). SW1 l'inonde vers SW2 et SW3, qui l'inondent à leur tour… PC2 répond, mais les copies du broadcast **continuent de tourner indéfiniment** entre les switches (dans les deux sens).
- L'en-tête IP a un **TTL** contre les boucles de couche 3 ; **l'en-tête Ethernet n'a pas de TTL**. Les broadcasts s'accumulent jusqu'à saturer le réseau : **tempête de broadcast** (*broadcast storm*).
- Deuxième problème : la même MAC source arrive sans cesse sur des interfaces différentes, le switch met à jour sa table en permanence : **MAC address flapping**.

### 3. Spanning Tree Protocol : principe

- STP « classique » = standard **IEEE 802.1D**. Tous les constructeurs l'activent **par défaut**.
- STP évite les boucles en mettant les ports redondants en état **blocking** (interface quasi désactivée, ne reçoit et n'envoie que des **BPDU**, *Bridge Protocol Data Units*, messages STP, et quelques trafics spécifiques). Ces ports sont des **secours** qui passent en **forwarding** (fonctionnement normal) si un port actif tombe.
- « **Bridge** » (pont) : ancien équipement entre le hub et le switch ; dans STP, bridge = switch.
- STP crée **un chemin unique** vers chaque point du réseau. Les switches envoient des **Hello BPDU** sur toutes leurs interfaces, **toutes les 2 secondes** par défaut ; recevoir un Hello BPDU sur une interface = elle est reliée à un autre switch (routeurs et PC n'en envoient pas).

### 4. Étape 1 : élire le root bridge

- Le switch avec le **bridge ID le plus bas** devient **root bridge**. **Tous ses ports sont designated, en forwarding** ; tous les autres switches doivent avoir un chemin vers lui.
- **Bridge ID traditionnel** = **bridge priority (16 bits) + adresse MAC (48 bits)**. Priorité par défaut **32768** sur tous les switches → la **MAC la plus basse** départage.
- **Bridge ID actuel** : la priorité est divisée en **bridge priority (4 bits) + extended system ID (12 bits) = VLAN ID**. Cisco utilise **PVST** (*Per-VLAN Spanning Tree*) : une instance STP par VLAN, un port peut être forwarding en VLAN1 et blocking en VLAN2 ; le bridge ID diffère donc par VLAN.
- 32768 = bit de poids fort du champ de 16 bits. Avec l'extended system ID, **la priorité par défaut en VLAN1 est 32769** (32768 + 1), 32770 en VLAN2, 32771 en VLAN3…
- La priorité ne se change que **par pas de 4096** (valeur du bit de poids faible de la partie priorité) : valeurs valides **0, 4096, 8192, 12288, 16384, 20480, 24576, 28672, 32768, …** ; ex. 28673 = 16384 + 8192 + 4096 + 1. On peut avoir un root bridge différent par VLAN (SW1 en VLAN1, SW2 en VLAN2…), configuration vue au Day 21.
- À l'allumage, chaque switch **se croit root** et n'abandonne que s'il reçoit un **BPDU supérieur** (bridge ID plus bas). Une fois convergé, **seul le root envoie des BPDU**, les autres les **relaient** sans en générer.
- Exercices : priorités 12289 identiques entre SW1 et SW3, MAC 014A.38F… contre 014A.382… → **SW3** (2 < F). Autre : **SW4** avec la priorité la plus basse, 4097.

### 5. Étape 2 : un root port par switch (sauf le root)

- Chaque autre switch choisit **UN root port** : l'interface avec le **root cost le plus bas**, en forwarding.
- **Coûts STP à mémoriser** : **Ethernet 10 Mbps = 100 ; FastEthernet 100 Mbps = 19 ; GigabitEthernet = 4 ; 10 Gigabit = 2.**
- **Root cost** = somme des coûts des **interfaces sortantes** sur le chemin vers le root (on ne compte pas l'interface qui reçoit). Le root annonce un coût **0** ; chaque switch ajoute le coût de son interface sortante en relayant. Exemple : SW2 reçoit 0 sur G0/1 (+4 = 4) et 4 depuis SW3 sur G0/0 (+4 = 8) → root port G0/1.
- **Le port en face d'un root port est toujours designated** (un autre switch ne doit pas bloquer le chemin vers le root).
- **Égalité de coût** → l'interface reliée au **voisin au bridge ID le plus bas** (exercice : SW2 root avec la plus basse priorité ; SW3 a 8 par G0/0 et G0/1, choisit G0/0 vers SW1 dont la MAC est plus basse que SW4).
- **Encore égalité** (deux liens vers le même voisin) → l'interface reliée au **port ID le plus bas du VOISIN**. Port ID = **port priority (défaut 128) + numéro de port** (colonne « Prio.Nbr » de `show spanning-tree`, ex. 128.1 pour G0/0, 128.2 pour G0/1). Exercice : SW3 choisit **G0/2** parce qu'il est relié à un port ID plus bas sur SW1 ; c'est le port ID du **voisin** qui compte, pas le port local.

### 6. Étape 3 : un designated port par domaine de collision

- Chaque lien (domaine de collision) a **exactement un designated port**. Sur le dernier lien SW2–SW3, on ne bloque pas les deux côtés.
- Designated = le port du switch au **root cost le plus bas** ; égalité → **bridge ID le plus bas** (SW2 : G0/0 designated). L'autre port devient **non-designated, en blocking** (SW3 G0/1).
- Les ports vers les PC sont designated/forwarding (les PC ne participent pas à STP).

**Résumé du processus** :

1. Root bridge = bridge ID le plus bas ; tous ses ports designated.
2. Chaque autre switch : UN root port = root cost le plus bas → voisin au bridge ID le plus bas → port ID le plus bas du voisin.
3. Chaque domaine de collision restant : UN designated port = switch au root cost le plus bas → bridge ID le plus bas ; l'autre est non-designated (blocking).

Exercices de fin : topologie 1, root **SW3** (même priorité, MAC la plus basse) ; SW2 choisit G0/2 (relié au port G0/0 de SW1, numéro plus bas) ; les ports de SW2 sur les liens restants sont non-designated (root cost plus élevé) ; vérifier **un designated port par lien**. Topologie 2 (certaines interfaces FastEthernet, coût **19**) : root **SW4** (priorité la plus basse) ; SW1 prend G0/1 comme root port car ses deux autres interfaces sont FastEthernet ; SW1 F1/0 et F2/0 non-designated (SW2 a un root cost plus bas) ; SW2 G0/1 non-designated car en face du root.

### 7. Pièges d'examen

- Coûts : **100 / 19 / 4 / 2**. Hello BPDU toutes les **2 s**.
- Priorité par défaut **32768** mais **32769 en VLAN1** (extended system ID) ; incréments de **4096**.
- Le départage du root port se fait sur le **port ID du voisin**, pas le sien.
- Ne pas compter le coût de l'interface réceptrice.
- Après convergence, seul le root génère des BPDU.
- Dans `show spanning-tree`, « **Altn** » (alternate) = non-designated ; la colonne **Cost** = coût de l'interface, pas le root cost total (voir `show spanning-tree detail`).

### 8. Commandes IOS

```
Switch# show spanning-tree                 ! par VLAN : protocole (ieee = STP classique/PVST), Root ID, Bridge ID (priority + sys-id-ext), timers, rôle/état/coût/Prio.Nbr de chaque port
Switch# show spanning-tree vlan 1          ! même sortie filtrée sur un VLAN
Switch# show spanning-tree detail          ! plus de détails, dont « cost of root path » (root cost total)
Switch# show spanning-tree vlan 1 detail   ! idem pour un VLAN (aperçu NetSim)
Switch# show spanning-tree summary         ! par VLAN : nombre de ports Blocking / Listening / Learning / Forwarding / STP Active
```

### 9. Le lab (vidéo n°38)

**Objectif** : identifier le root bridge et le rôle (root, designated, non-designated) de chaque port, puis vérifier dans la CLI. **Désactiver les voyants de lien** (Options → Preferences → « Show Link Lights ») pour ne pas tricher. Étiquettes « D », « R », « ND » posées avec l'outil Note.

1. **Root bridge** : SW3, priorité **24577**, la plus basse. Ses 4 ports sont designated.
2. **Root ports** :
   - SW1 : via F0/1 ou F0/2 : 19 + 4 (SW2 G0/1) + 4 (SW4 G0/2) = **27** ; via F0/3 ou F0/4 : **19**. Égalité F0/3/F0/4, même voisin SW3 → port ID du voisin : SW3 F0/1 plus bas → **root port SW1 F0/4**.
   - SW2 : F0/3 directement sur le root = **19**, mais via G0/1 : 4 + 4 = **8** → **root port G0/1** ; donc SW4 G0/1 designated (en face d'un root port).
   - SW4 : G0/1 étant designated, **G0/2 est le root port** (coût 4).
3. **Designated / non-designated** : SW1 F0/3 et SW2 F0/3 sont **non-designated** (reliés au root, dont les ports sont designated). Liens SW1–SW2 (F0/1, F0/2) : root cost SW2 = 8 < SW1 = 19 → **SW2 F0/1 et F0/2 designated, SW1 F0/1 et F0/2 non-designated** (blocking).
4. **Vérification** sur SW3 : `show spanning-tree` : « VLAN0001 », « Spanning tree enabled protocol ieee » (STP classique, en fait PVST), **Root ID** et **Bridge ID** identiques (priorité 24577 = **24576 + sys-id-ext 1**), « This bridge is the root », timers (Day 21), ports tous **Desg FWD**. `show spanning-tree detail`, `show spanning-tree summary` (listening et learning = états transitoires, Day 21 ; « STP Active » = ports STP actifs). SW1 : F0/4 **Root FWD**, les autres **Altn BLK**, Root ID = SW3, Bridge ID = SW1. SW2 : F0/1 et F0/2 Desg FWD (lien de fait inactif car SW1 bloque), F0/3 BLK, G0/1 Root ; coût affiché 4 = coût de l'interface, `show spanning-tree detail` donne « cost of root path is 8 ». SW4 : G0/1 Desg, G0/2 Root.

**Aperçu Boson NetSim** : NetSim pour CCNA n'a pas de lab STP, car le sujet 2.5 de l'examen 200-301 dit « **describe** / **identify** » Rapid PVST+, pas « configure » (le CCNP ENCOR 350-401, sujet 3.1c, demande de configurer). Lab « Spanning Tree Protocol » du NetSim CCNP : switches ASW (access) et DSW (distribution). `show spanning-tree vlan 1 detail` sur P1DSW1 : « VLAN 1 is executing the ieee compatible Spanning Tree Protocol » (classique) ; priorité **24576, sysid 1** (24577 au total) + MAC ; aucun root port ni port bloqué car « **We are the root of the spanning tree** » ; timers par défaut : **hello 2 s, max age 20 s, forward delay 15 s** (expliqués au Day 21).

### 10. Le quiz du Day 20 (questions d'entraînement du cours + 1 question Boson ExSim)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| 4 switches : lequel devient root bridge ? (SW1 et SW3 priorité 12289) | **SW3** | Priorités égales ; MAC 014A.38**2**… plus basse que 014A.38**F**…. |
| 4 switches : lequel devient root bridge ? | **SW4** | Priorité la plus basse, 4097. |
| Root bridge et root ports (tous ports Gigabit) ? | **SW2** root ; SW1 G0/0 et SW4 G0/1 (coût 4) ; **SW3 G0/0** | SW3 : 8 par G0/0 et 8 par G0/1 → voisin au bridge ID le plus bas = SW1 (même priorité, MAC plus basse) ; SW1 G0/1 devient designated. |
| Deux liens SW1–SW3 : root port de SW3 ? | **G0/2** | Relié au port ID le plus bas sur SW1 (le voisin) ; G0/0 est relié à un port ID plus élevé. SW1 G0/1 designated. |
| Topologie 1 : root et rôle de chaque port ? | Root **SW3** ; SW2 root port **G0/2** ; ports de SW2 sur les autres liens non-designated | Priorité égale, MAC la plus basse ; G0/2 relié au port G0/0 de SW1 (numéro plus bas) ; SW2 a un root cost plus élevé. Un designated port par lien. |
| Topologie 2 (interfaces FastEthernet, coût 19) : root et rôles ? | Root **SW4** ; SW1 root port **G0/1** ; SW1 F1/0, F2/0 et SW2 G0/1 non-designated | SW4 priorité la plus basse ; les autres interfaces de SW1 sont FastEthernet (19) ; SW2 a un root cost plus bas que SW1 ; SW2 G0/1 est en face du root. |
| Boson ExSim : `spanning-tree portfast default` en configuration globale sur Switch A, PortFast non configuré ailleurs : quels ports utilisent PortFast ? A) aucun, B) tous, C) tous les ports d'accès, D) tous les ports trunk | **Réponse donnée au Day 21** | PortFast n'est pas encore vu ; Jeremy invite à chercher « spanning tree portfast » ou à répondre en commentaire. |

---

## 🇬🇧 English version

### 1. Redundancy in networks

- A network must run 24 hours a day, 7 days a week, 365 days a year; even a short downtime can be disastrous. If one component fails, another must take over; **redundancy at every possible point**.
- Poor design: a single link to the Internet, a single switch-to-switch link = single points of failure. Better design: multiple routers, multiple paths between switches.
- Limitation: most PCs have **only one network interface card (NIC)**, so one switch; important servers have **multiple NICs** to connect to multiple switches.
- STP is a **Layer 2** protocol: it enables redundant LANs, not routing between networks.

### 2. The problem without STP: broadcast storms

- Three switches in a triangle, PC1 (10.0.0.1), PC2 (10.0.0.2), PC3 (10.0.0.3). PC1 sends an **ARP request** (broadcast, destination MAC all Fs). SW1 floods it to SW2 and SW3, which flood it in turn... PC2 replies, but the broadcast copies **keep looping forever** between the switches (clockwise and counter-clockwise).
- The IP header has a **TTL** against Layer 3 loops; **the Ethernet header has no TTL**. Looped broadcasts accumulate until the network is too congested for legitimate traffic: a **broadcast storm**.
- Second problem: the same source MAC keeps arriving on different interfaces, the switch continuously updates its MAC address table: **MAC address flapping**.

### 3. Spanning Tree Protocol: principle

- "Classic" STP = **IEEE 802.1D** standard. Switches from all vendors run it **by default**.
- STP prevents loops by placing redundant ports in a **blocking** state (essentially disabled, only sends/receives **BPDUs**, Bridge Protocol Data Units, the STP messages, and some other specific traffic). These ports are **backups** that enter the **forwarding** state (normal operation) if an active port fails.
- "**Bridge**": an old device between the hub and the switch; in STP, bridge = switch.
- STP creates **a single path** to and from each point in the network. Switches send **Hello BPDUs** out of all interfaces, **every 2 seconds** by default; receiving a Hello BPDU on an interface means it is connected to another switch (routers and PCs do not send them).

### 4. Step 1: elect the root bridge

- The switch with the **lowest bridge ID** becomes the **root bridge**. **All its ports are designated, in a forwarding state**; all other switches must have a path to reach it.
- **Traditional bridge ID** = **bridge priority (16 bits) + MAC address (48 bits)**. Default priority **32768** on all switches → the **lowest MAC address** is the tie-breaker.
- **Updated bridge ID**: the priority is split into **bridge priority (4 bits) + extended system ID (12 bits) = VLAN ID**. Cisco uses **PVST** (Per-VLAN Spanning Tree): a separate STP instance per VLAN, a port can be forwarding in VLAN1 and blocking in VLAN2; the bridge ID therefore differs per VLAN.
- 32768 = the most significant bit of the 16-bit field. With the extended system ID, **the default priority in VLAN1 is 32769** (32768 + 1), 32770 in VLAN2, 32771 in VLAN3...
- The priority can only be changed **in units of 4096** (value of the least significant bit of the priority portion): valid values **0, 4096, 8192, 12288, 16384, 20480, 24576, 28672, 32768, ...**; e.g. 28673 = 16384 + 8192 + 4096 + 1. Different root bridges per VLAN are possible (SW1 in VLAN1, SW2 in VLAN2...), configuration in Day 21.
- When powered on, every switch **assumes it is the root** and only gives up if it receives a **superior BPDU** (lower bridge ID). Once converged, **only the root bridge sends BPDUs**, the others **forward** them without generating their own.
- Practice: SW1 and SW3 both priority 12289, MACs 014A.38F... versus 014A.382... → **SW3** (2 < F). Another: **SW4** with the lowest priority, 4097.

### 5. Step 2: one root port per switch (except the root)

- Every other switch selects **ONE root port**: the interface with the **lowest root cost**, in a forwarding state.
- **STP costs to remember**: **Ethernet 10 Mbps = 100; FastEthernet 100 Mbps = 19; GigabitEthernet = 4; 10 Gigabit = 2.**
- **Root cost** = total cost of the **outgoing interfaces** along the path to the root (the receiving interface is not counted). The root advertises cost **0**; each switch adds its outgoing interface cost when forwarding. Example: SW2 receives 0 on G0/1 (+4 = 4) and 4 from SW3 on G0/0 (+4 = 8) → root port G0/1.
- **The port connected to another switch's root port MUST be designated** (another switch must not block the path to the root).
- **Cost tie** → the interface connected to the **neighbor with the lowest bridge ID** (practice: SW2 is root with the lowest priority; SW3 has 8 via G0/0 and G0/1, selects G0/0 toward SW1 whose MAC is lower than SW4's).
- **Still a tie** (two links to the same neighbor) → the interface connected to the **lowest port ID on the NEIGHBOR**. Port ID = **port priority (default 128) + port number** ("Prio.Nbr" column of `show spanning-tree`, e.g. 128.1 for G0/0, 128.2 for G0/1). Practice: SW3 selects **G0/2** because it is connected to a lower port ID on SW1; the **neighbor's** port ID is used, not the local one.

### 6. Step 3: one designated port per collision domain

- Every link (collision domain) has **exactly one designated port**. On the last link SW2–SW3, both sides are not blocked.
- Designated = the port on the switch with the **lowest root cost**; tie → **lowest bridge ID** (SW2: G0/0 designated). The other port becomes **non-designated, in a blocking state** (SW3 G0/1).
- Ports to PCs are designated/forwarding (PCs do not participate in STP).

**Process summary**:

1. Root bridge = lowest bridge ID; all its ports designated.
2. Each other switch: ONE root port = lowest root cost → neighbor with lowest bridge ID → lowest neighbor port ID.
3. Each remaining collision domain: ONE designated port = switch with the lowest root cost → lowest bridge ID; the other is non-designated (blocking).

Final practice: topology 1, root **SW3** (same priority, lowest MAC); SW2 selects G0/2 (connected to SW1's G0/0, lower number); SW2's ports on the remaining links are non-designated (higher root cost); check **one designated port per link**. Topology 2 (some FastEthernet interfaces, cost **19**): root **SW4** (lowest priority); SW1 uses G0/1 as root port because its other two interfaces are FastEthernet; SW1 F1/0 and F2/0 non-designated (SW2 has a lower root cost); SW2 G0/1 non-designated because it faces the root.

### 7. Exam traps

- Costs: **100 / 19 / 4 / 2**. Hello BPDU every **2 s**.
- Default priority **32768** but **32769 in VLAN1** (extended system ID); increments of **4096**.
- Root port tie-break uses the **neighbor's port ID**, not the local one.
- Do not count the receiving interface's cost.
- After convergence, only the root generates BPDUs.
- In `show spanning-tree`, "**Altn**" (alternate) = non-designated; the **Cost** column = the interface cost, not the total root cost (see `show spanning-tree detail`).

### 8. IOS commands

```
Switch# show spanning-tree                 ! per VLAN: protocol (ieee = classic STP/PVST), Root ID, Bridge ID (priority + sys-id-ext), timers, role/status/cost/Prio.Nbr of each port
Switch# show spanning-tree vlan 1          ! same output filtered to one VLAN
Switch# show spanning-tree detail          ! more details, including "cost of root path" (total root cost)
Switch# show spanning-tree vlan 1 detail   ! same for one VLAN (NetSim preview)
Switch# show spanning-tree summary         ! per VLAN: number of ports Blocking / Listening / Learning / Forwarding / STP Active
```

### 9. The lab (video 38)

**Objective**: identify the root bridge and the role (root, designated, non-designated) of every port, then confirm in the CLI. **Turn off link lights** (Options → Preferences → "Show Link Lights") so you cannot cheat. "D", "R", "ND" labels placed with the Note tool.

1. **Root bridge**: SW3, priority **24577**, the lowest. Its 4 ports are designated.
2. **Root ports**:
   - SW1: via F0/1 or F0/2: 19 + 4 (SW2 G0/1) + 4 (SW4 G0/2) = **27**; via F0/3 or F0/4: **19**. Tie between F0/3 and F0/4, same neighbor SW3 → neighbor port ID: SW3 F0/1 is lower → **root port SW1 F0/4**.
   - SW2: F0/3 directly to the root = **19**, but via G0/1: 4 + 4 = **8** → **root port G0/1**; so SW4 G0/1 is designated (facing a root port).
   - SW4: G0/1 being designated, **G0/2 is the root port** (cost 4).
3. **Designated / non-designated**: SW1 F0/3 and SW2 F0/3 are **non-designated** (connected to the root, whose ports are designated). SW1–SW2 links (F0/1, F0/2): SW2 root cost = 8 < SW1 = 19 → **SW2 F0/1 and F0/2 designated, SW1 F0/1 and F0/2 non-designated** (blocking).
4. **Verification** on SW3: `show spanning-tree`: "VLAN0001", "Spanning tree enabled protocol ieee" (classic STP, actually PVST), **Root ID** and **Bridge ID** identical (priority 24577 = **24576 + sys-id-ext 1**), "This bridge is the root", timers (Day 21), all ports **Desg FWD**. `show spanning-tree detail`, `show spanning-tree summary` (listening and learning = transitional states, Day 21; "STP Active" = total STP-enabled ports). SW1: F0/4 **Root FWD**, the others **Altn BLK**, Root ID = SW3, Bridge ID = SW1. SW2: F0/1 and F0/2 Desg FWD (links effectively disabled because SW1 blocks), F0/3 BLK, G0/1 Root; displayed cost 4 = interface cost, `show spanning-tree detail` says "cost of root path is 8". SW4: G0/1 Desg, G0/2 Root.

**Boson NetSim preview**: NetSim for CCNA has no STP labs, because exam topic 2.5 of the 200-301 says "**describe** / **identify**" Rapid PVST+, not "configure" (CCNP ENCOR 350-401, topic 3.1c, asks to configure). "Spanning Tree Protocol" lab from NetSim for CCNP: ASW (access) and DSW (distribution) switches. `show spanning-tree vlan 1 detail` on P1DSW1: "VLAN 1 is executing the ieee compatible Spanning Tree Protocol" (classic); priority **24576, sysid 1** (24577 total) + MAC; no root port and no blocked ports because "**We are the root of the spanning tree**"; default timers: **hello 2 s, max age 20 s, forward delay 15 s** (explained in Day 21).

### 10. Day 20 quiz (in-lecture practice questions + 1 Boson ExSim question)

| Question | Answer | Why |
| :--- | :--- | :--- |
| 4 switches: which becomes the root bridge? (SW1 and SW3 priority 12289) | **SW3** | Equal priorities; MAC 014A.38**2**... is lower than 014A.38**F**.... |
| 4 switches: which becomes the root bridge? | **SW4** | Lowest priority, 4097. |
| Root bridge and root ports (all Gigabit ports)? | **SW2** root; SW1 G0/0 and SW4 G0/1 (cost 4); **SW3 G0/0** | SW3: 8 via G0/0 and 8 via G0/1 → neighbor with the lowest bridge ID = SW1 (same priority, lower MAC); SW1 G0/1 becomes designated. |
| Two links SW1–SW3: SW3's root port? | **G0/2** | Connected to the lowest port ID on SW1 (the neighbor); G0/0 is connected to a higher port ID. SW1 G0/1 designated. |
| Topology 1: root and role of each port? | Root **SW3**; SW2 root port **G0/2**; SW2's ports on the other links non-designated | Equal priority, lowest MAC; G0/2 connected to SW1's G0/0 (lower number); SW2 has a higher root cost. One designated port per link. |
| Topology 2 (FastEthernet interfaces, cost 19): root and roles? | Root **SW4**; SW1 root port **G0/1**; SW1 F1/0, F2/0 and SW2 G0/1 non-designated | SW4 lowest priority; SW1's other interfaces are FastEthernet (19); SW2 has a lower root cost than SW1; SW2 G0/1 faces the root. |
| Boson ExSim: `spanning-tree portfast default` in global config on Switch A, PortFast not configured elsewhere: which ports use PortFast? A) none, B) all, C) all access ports, D) all trunk ports | **Answer given in Day 21** | PortFast has not been covered yet; Jeremy suggests researching "spanning tree portfast" or answering in the comments. |
