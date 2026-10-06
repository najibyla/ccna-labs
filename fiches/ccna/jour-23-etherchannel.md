# CCNA Day 23 : EtherChannel

> Source : Jeremy's IT Lab, « Free CCNA | EtherChannel | Day 23 » (cours, 42 min, vidéo n°47 de la playlist, sujet 2.4 de la liste d'examen : configurer et vérifier des EtherChannels de couche 2 et 3 avec LACP) et « Configuring EtherChannel | Day 23 Lab » (lab, 25 min, vidéo n°48). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Le problème : STP bloque les liens redondants

- Scénario : un **switch d'accès (ASW1, access switch**, où se connectent les hôtes finaux) relié à un **switch de distribution (DSW1, distribution switch**, où se connectent les switches d'accès). 40 hôtes saturent le lien ; l'administrateur ajoute un 2e, 3e, 4e lien, sans amélioration. Sur DSW1 tous les voyants sont verts, sur ASW1 **un seul vert, les autres orange** : **STP** désactive tous les liens sauf un entre deux switches (sinon, boucle de couche 2 et tempête de broadcast). Les liens inutilisés ne servent que de secours.
- **Oversubscription** (sursouscription) : bande passante totale des ports hôtes supérieure à celle du lien vers la distribution ; acceptable dans une certaine mesure, trop cause de la congestion (détaillé plus tard dans le cours).

### 2. EtherChannel

- Regroupe plusieurs interfaces physiques en **une seule interface logique** ; **STP la traite comme une seule interface**. Résultat : redondance **et** bande passante additionnée (quatre Gigabit = comme une interface virtuelle à 4 Gbps). Représenté sur un schéma par un cercle autour des liens.
- Pas de boucle : un broadcast reçu par ASW1 est envoyé **une seule fois** vers DSW1 (une seule copie reçue), et DSW1 ne le renvoie pas par l'interface d'où il vient, donc pas par les autres liens du groupe.
- Autres noms : **Port Channel**, **LAG** (Link Aggregation Group).
- Analogie : comme les VLAN divisent virtuellement un switch physique, l'EtherChannel réunit virtuellement des interfaces physiques.

### 3. Load balancing par flux (flows)

- Un **flux** = une communication entre deux nœuds (PC1 ↔ SRV1). Toutes les trames d'un même flux utilisent **la même interface physique** du groupe, sinon elles pourraient arriver dans le désordre (certaines applications ne le supportent pas). Un autre flux (PC1 → PR1, PC2 → PR1) peut utiliser une autre interface : c'est le load balancing.
- Entrées possibles du calcul : MAC source, MAC destination, MAC source + destination ; IP source, IP destination, IP source + destination ; certains switches aussi les ports TCP/UDP de couche 4. Les méthodes disponibles dépendent du modèle.
- `show etherchannel load-balance` : sur le switch de la vidéo, défaut **src-dst-ip** (IPv4 et IPv6) ; le trafic **non-IP** est réparti par MAC source + destination. `port-channel load-balance src-dst-mac` pour changer. Note de Jeremy : `show etherchannel` pour voir, `port-channel` pour configurer, `channel-group` pour créer, trois mots-clés différents pour la même chose.

### 4. Trois méthodes de configuration

| Méthode | Protocole | Modes | Formation de l'EtherChannel |
| :--- | :--- | :--- | :--- |
| **PAgP** (Port Aggregation Protocol) | **propriétaire Cisco** (pas avec Juniper, etc.), négociation dynamique comme DTP pour les trunks | **desirable** (cherche activement), **auto** (seulement si l'autre est desirable) | desirable-desirable, desirable-auto : oui ; **auto-auto : non** |
| **LACP** (Link Aggregation Control Protocol) | **standard IEEE 802.3ad**, négociation dynamique, multi-vendeur, **méthode préférée** (seule citée dans la liste d'examen) | **active** (cherche activement), **passive** | active-active, active-passive : oui ; **passive-passive : non** (l'interface port-channel est créée mais ne fonctionne pas) |
| **Statique** | aucun protocole ; généralement évité (pas de retrait automatique d'un membre défaillant) | **on** | **on-on** seulement ; on-desirable et on-active ne fonctionnent pas |

- Jusqu'à **8 interfaces** par EtherChannel ; **LACP en accepte 16**, dont 8 actives et 8 en **standby**.
- Les modes ne se mélangent pas : active-desirable ne forme rien.

### 5. Configuration

- Utiliser `interface range` pour configurer tous les membres ensemble (les configurations doivent être identiques).
- `channel-group <n> mode {desirable | auto | active | passive | on}` : crée l'interface virtuelle **port-channel n** (Po n, visible dans `show ip interface brief`). Le numéro doit être identique entre les membres **du même switch**, mais **pas nécessairement** avec le switch voisin (channel-group 1 sur ASW1 peut former un EtherChannel avec channel-group 2 sur DSW1) : il identifie seulement l'interface virtuelle locale.
- `channel-protocol {lacp | pagp}` : fixe manuellement le protocole de négociation. Inutile en pratique (desirable/auto ⇒ PAgP, active/passive ⇒ LACP automatiquement), mais à connaître : après `channel-protocol lacp`, `channel-group 1 mode desirable` et `mode on` sont **rejetés**, seul `mode active` (ou passive) passe.
- Ensuite on configure **l'interface port-channel** (ex. `switchport mode trunk`) : la configuration est **appliquée automatiquement aux interfaces physiques** membres. `show interfaces trunk` liste Po1, pas les interfaces physiques.
- **Les membres doivent avoir la même configuration** : même **duplex**, même **vitesse**, même **mode switchport** (access ou trunk), mêmes **VLAN autorisés** et même **VLAN natif** si trunk. Une interface différente est **exclue** de l'EtherChannel.

### 6. Vérification

- `show etherchannel summary` (la commande la plus utile). Drapeaux : **S** = couche 2 (switchport), **R** = couche 3 (routed), **U** = in use, **D** = down, **P** = port bundled dans le port-channel (ce qu'on veut voir), **s** minuscule = suspended (membre exclu, ex. passé en mode access ; les autres continuent), **I** = stand-alone (configuré mais isolé, ex. l'autre switch pas encore configuré, vu dans le lab). Un EtherChannel de couche 2 opérationnel : **SU** et membres **P**.
- `show etherchannel port-channel` : nombre de ports, protocole et **mode du channel-group** (active...), absent de `summary`.
- `show spanning-tree` : seule l'interface port-channel apparaît, plus les interfaces physiques : STP la voit comme une seule interface, aucun membre bloqué.

### 7. EtherChannel de couche 3

- Les designs modernes préfèrent des **connexions de couche 3 (ports routés)** entre switches : plus de STP du tout. Même avec EtherChannel, une boucle reste possible entre plusieurs switches reliés en boucle à la couche 2 (STP bloquerait un port-channel) ; les ports routés ne transmettent pas les broadcasts de couche 2, donc pas de boucle.
- Configuration : sur les membres, `no switchport` **avant** `channel-group` ; l'interface port-channel créée reçoit automatiquement `no switchport`. L'**adresse IP se configure sur l'interface port-channel**, pas sur les membres. `show etherchannel summary` affiche **RU**. Les deux switches sont alors comme deux routeurs reliés, avec load balancing sur les membres.

### 8. Pièges d'examen

- Combinaisons valides : **on-on, desirable-auto (ou desirable-desirable), active-passive (ou active-active)**. Invalides : auto-auto, passive-passive, et tout mélange (on-desirable, active-desirable).
- PAgP = Cisco (desirable/auto) ; LACP = IEEE 802.3ad (active/passive).
- Drapeau **P** = bundled ; **S** majuscule = couche 2, **s** minuscule = suspended.
- Paramètres qui doivent correspondre : vitesse, duplex, mode switchport, VLAN autorisés/natif. Pas l'ID d'interface (unique) ni l'adresse IP (sur le port-channel seulement).
- Le numéro de channel-group n'a pas à correspondre entre les deux switches.
- `channel-protocol lacp` puis `channel-group 1 mode on` : commande rejetée, pas d'EtherChannel (question Boson).
- Après EtherChannel, les trois mots-clés : `channel-group` (config membres), `port-channel` (interface et load-balance), `show etherchannel`.

### 9. Commandes IOS

```
Switch# show etherchannel load-balance                        ! méthode de load balancing actuelle
Switch(config)# port-channel load-balance src-dst-ip          ! changer la méthode (src-mac, dst-mac, src-dst-mac, src-ip, dst-ip, src-dst-ip...)
Switch(config)# interface range g0/1 - 2                      ! configurer les membres ensemble
Switch(config-if-range)# channel-group 1 mode active          ! LACP (active/passive) ; desirable/auto = PAgP ; on = statique
Switch(config-if-range)# channel-protocol lacp                ! forcer le protocole (optionnel, rarement utile)
Switch(config-if-range)# no switchport                        ! avant channel-group : EtherChannel de couche 3
Switch(config)# interface port-channel 1                      ! l'interface virtuelle (Po1)
Switch(config-if)# switchport trunk encapsulation dot1q       ! sur un switch supportant ISL et dot1q
Switch(config-if)# switchport mode trunk                      ! appliqué aussi aux membres
Switch(config-if)# ip address 10.0.0.1 255.255.255.252        ! EtherChannel de couche 3 : IP sur le port-channel
Switch(config)# ip routing                                    ! switch multicouche : activer la table de routage
Switch(config)# ip route 172.16.2.0 255.255.255.0 10.0.0.2    ! route statique
Switch# show etherchannel summary                             ! drapeaux SU/RU, P, D, s, I
Switch# show etherchannel port-channel                        ! protocole, mode du channel-group
Switch# show interfaces trunk                                 ! Po1 apparaît comme trunk
Switch# show spanning-tree                                    ! seul Po1 apparaît
Switch# show cdp neighbors                                    ! (NetSim) interfaces locales et distantes des voisins Cisco
```

### 10. Le lab (vidéo 048)

Objectif : deux switches d'accès (ASW1, ASW2) reliés chacun par deux liens à un switch de distribution (DSW1, DSW2) ; EtherChannels de couche 2 (LACP puis PAgP), EtherChannel de couche 3 statique entre DSW1 et DSW2, routes statiques, load balancing.

1. **ASW1-DSW1 en LACP** : sur ASW1, `show spanning-tree` : G0/1 root port, G0/2 **alternate**. `interface range g0/1 - 2`, `channel-group 1 mode active` ; `interface po1`, `switchport mode trunk`. `show run` : Po1 créée, `switchport mode trunk` aussi sur G0/1 et G0/2. `show etherchannel summary` : Po1 **SD** (couche 2, down), membres **I** (stand-alone) car DSW1 n'est pas configuré. Sur DSW1 : `interface range g1/0/3 - 4`, `channel-group 1 mode active` (passive marcherait aussi), `interface po1`, `switchport trunk encapsulation dot1q` (ce modèle supporte ISL et dot1q), `switchport mode trunk`. Vérifier : **SU**, membres **P** ; `show interface trunk` : Po1 trunk ; sur ASW1, `show spanning-tree` : G0/1 et G0/2 ont disparu, **Port-channel 1 est root port**, F0/1-2 désignés (hôtes).
2. **ASW2-DSW2 en PAgP** : identique avec `channel-group 1 mode desirable` des deux côtés, Po1 en trunk (encapsulation dot1q sur DSW2). Vérifier SU / P.
3. **DSW1-DSW2 en couche 3 statique** : `interface range g1/0/1 - 2`, `no switchport`, `channel-group 2 mode on` (le groupe 1 est déjà pris) ; `interface po2`, `ip address 10.0.0.2 255.255.255.252` sur DSW2 et 10.0.0.1 sur DSW1. `show etherchannel summary` : **RU**, membres P. `ping 10.0.0.2` depuis DSW1 : OK.
4. **Routes statiques** : `show ip route` vide sur le switch multicouche : il faut `ip routing` (le ping direct marchait car directement connecté). DSW1 : `ip route 172.16.2.0 255.255.255.0 10.0.0.2` ; DSW2 : `ip routing`, `ip route 172.16.1.0 255.255.255.0 10.0.0.1`. Ping PC1 → SRV1 (172.16.2.1) via la SVI VLAN 1 de DSW1 puis le port-channel de couche 3 : quelques timeouts au début (ARP), puis succès.
5. **Load balancing** : `show etherchannel load-balance` : défaut **src-mac** sur les deux modèles ; `port-channel load-balance src-dst-ip` sur les quatre switches, puis vérification.

Aperçu Boson NetSim (lab CCNA « Layer 2 EtherChannel », tâche 1 planification) : `show cdp neighbors` (CDP, Cisco Discovery Protocol, propriétaire : interface locale et port ID du voisin), `show ip interface brief` (up/up), `show interfaces trunk` (desirable, ISL négocié par DTP), `show running-config` (membres sans configuration), quiz STP : DSW2 F0/5 root port (même coût 19, même voisin, port ID voisin le plus bas), bande passante 100 000 Kbit par lien (`show interface f0/5`) → 200 Mbps avec EtherChannel, F0/6 bloqué par STP sinon ; jusqu'à 8 membres actifs, 16 avec LACP.

### 11. Le quiz (vidéo 047 : 3 questions, plus une question Boson ExSim)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Q1. Combinaisons de modes channel-group qui forment un EtherChannel opérationnel ? (3) | **A on-on, C desirable-auto, G active-active** | on-on = statique ; desirable-auto = PAgP ; active-active = LACP. passive-passive et auto-auto : aucun côté ne cherche activement. active-desirable et on-desirable mélangent des modes différents. |
| Q2. Dans `show etherchannel summary`, les interfaces physiques ont le drapeau (P) : signification ? | **B, les interfaces sont bundled dans le port-channel** | C'est le drapeau attendu pour les membres. Pas « passive », pas « paused », pas « couche 2 » (c'est S). |
| Q3. Paramètres des membres qui doivent correspondre ? (2) | **C vitesse, D mode switchport (access/trunk)** | L'ID d'interface est unique ; l'adresse IP se configure sur le port-channel, pas sur les membres, même en couche 3. |
| Boson ExSim. SwitchA : `interface port-channel 1`, `interface range f0/5 - 6`, `channel-protocol lacp`, `channel-group 1 mode on` ; SwitchB : idem avec `channel-protocol pagp` et `mode on`. Résultat ? | **B, aucun lien n'est formé** | Après `channel-protocol lacp`, seuls active/passive sont acceptés ; après `pagp`, seuls desirable/auto : `mode on` est rejeté des deux côtés, les interfaces ne rejoignent pas le port-channel (créé à l'avance mais vide). |

---

## 🇬🇧 English version

### 1. The problem: STP blocks redundant links

- Scenario: an **access switch (ASW1**, where end hosts connect) linked to a **distribution switch (DSW1**, where access switches connect). 40 hosts congest the link; the admin adds a 2nd, 3rd, 4th link, no improvement. On DSW1 all lights are green, on ASW1 **only one green, the others orange**: **STP** disables all but one link between two switches (otherwise Layer 2 loop and broadcast storm). Unused links are only backups.
- **Oversubscription**: total bandwidth of host ports greater than the link to distribution; some is acceptable, too much causes congestion (covered later in the course).

### 2. EtherChannel

- Groups several physical interfaces into **one logical interface**; **STP treats it as a single interface**. Result: redundancy **and** combined bandwidth (four Gigabit = like a virtual 4 Gbps interface). Drawn as a circle around the links.
- No loop: a broadcast received by ASW1 is sent **once** toward DSW1 (one copy received), and DSW1 does not send it back out the interface it came in on, so not out the other links of the group.
- Other names: **Port Channel**, **LAG** (Link Aggregation Group).
- Analogy: as VLANs virtually divide a physical switch, EtherChannel virtually combines physical interfaces.

### 3. Flow-based load balancing

- A **flow** = a communication between two nodes (PC1 ↔ SRV1). All frames of one flow use **the same physical interface** of the group, otherwise they could arrive out of order (some applications cannot handle that). Another flow (PC1 → PR1, PC2 → PR1) may use another interface: that is the load balancing.
- Possible inputs to the calculation: source MAC, destination MAC, source + destination MAC; source IP, destination IP, source + destination IP; some switches also Layer 4 TCP/UDP ports. Available methods depend on the model.
- `show etherchannel load-balance`: on the video's switch, default **src-dst-ip** (IPv4 and IPv6); **non-IP** traffic is balanced by source + destination MAC. `port-channel load-balance src-dst-mac` to change. Jeremy's note: `show etherchannel` to view, `port-channel` to configure, `channel-group` to create, three different keywords for the same thing.

### 4. Three configuration methods

| Method | Protocol | Modes | EtherChannel forms |
| :--- | :--- | :--- | :--- |
| **PAgP** (Port Aggregation Protocol) | **Cisco proprietary** (not with Juniper etc.), dynamic negotiation like DTP for trunks | **desirable** (actively tries), **auto** (only if the other side is desirable) | desirable-desirable, desirable-auto: yes; **auto-auto: no** |
| **LACP** (Link Aggregation Control Protocol) | **IEEE 802.3ad standard**, dynamic negotiation, multi-vendor, **preferred method** (the only one in the exam topics list) | **active** (actively tries), **passive** | active-active, active-passive: yes; **passive-passive: no** (the port-channel interface is created but does not function) |
| **Static** | no protocol; usually avoided (no automatic removal of a failed member) | **on** | **on-on** only; on-desirable and on-active do not work |

- Up to **8 interfaces** per EtherChannel; **LACP allows 16**, 8 active and 8 in **standby**.
- Modes do not mix: active-desirable forms nothing.

### 5. Configuration

- Use `interface range` to configure all members together (their configurations must match).
- `channel-group <n> mode {desirable | auto | active | passive | on}`: creates the virtual **port-channel n** interface (Po n, visible in `show ip interface brief`). The number must match between members **on the same switch**, but **not necessarily** with the neighbor switch (channel-group 1 on ASW1 can form an EtherChannel with channel-group 2 on DSW1): it only identifies the local virtual interface.
- `channel-protocol {lacp | pagp}`: manually sets the negotiation protocol. Not useful in practice (desirable/auto ⇒ PAgP, active/passive ⇒ LACP automatically), but worth knowing: after `channel-protocol lacp`, `channel-group 1 mode desirable` and `mode on` are **rejected**, only `mode active` (or passive) works.
- Then configure **the port-channel interface** (e.g. `switchport mode trunk`): the configuration is **automatically applied to the physical member interfaces**. `show interfaces trunk` lists Po1, not the physical interfaces.
- **Members must have matching configurations**: same **duplex**, same **speed**, same **switchport mode** (access or trunk), same **allowed VLANs** and **native VLAN** if trunk. A differing interface is **excluded** from the EtherChannel.

### 6. Verification

- `show etherchannel summary` (the most useful command). Flags: **S** = Layer 2 (switchport), **R** = Layer 3 (routed), **U** = in use, **D** = down, **P** = port bundled in the port-channel (what you want to see), lower-case **s** = suspended (member excluded, e.g. changed to access mode; the others keep working), **I** = stand-alone (configured but isolated, e.g. the other switch not configured yet, seen in the lab). An operational Layer 2 EtherChannel: **SU** and members **P**.
- `show etherchannel port-channel`: number of ports, protocol and **channel-group mode** (active...), not shown in `summary`.
- `show spanning-tree`: only the port-channel interface appears, the physical interfaces no longer do: STP sees a single interface, no member blocked.

### 7. Layer 3 EtherChannel

- Modern designs lean toward **Layer 3 connections (routed ports)** between switches: no STP at all. Even with EtherChannel, a loop is still possible among several switches connected in a Layer 2 loop (STP would block one port-channel); routed ports do not forward Layer 2 broadcasts, so no loop.
- Configuration: on the members, `no switchport` **before** `channel-group`; the created port-channel interface automatically gets `no switchport`. The **IP address is configured on the port-channel interface**, not the members. `show etherchannel summary` shows **RU**. The two switches are then like two routers connected, with load balancing over the members.

### 8. Exam traps

- Valid combinations: **on-on, desirable-auto (or desirable-desirable), active-passive (or active-active)**. Invalid: auto-auto, passive-passive, and any mix (on-desirable, active-desirable).
- PAgP = Cisco (desirable/auto); LACP = IEEE 802.3ad (active/passive).
- Flag **P** = bundled; upper-case **S** = Layer 2, lower-case **s** = suspended.
- Parameters that must match: speed, duplex, switchport mode, allowed/native VLANs. Not the interface ID (unique) nor the IP address (on the port-channel only).
- The channel-group number need not match between the two switches.
- `channel-protocol lacp` then `channel-group 1 mode on`: command rejected, no EtherChannel (Boson question).
- Three keywords: `channel-group` (member config), `port-channel` (interface and load-balance), `show etherchannel`.

### 9. IOS commands

```
Switch# show etherchannel load-balance                        ! current load-balancing method
Switch(config)# port-channel load-balance src-dst-ip          ! change the method (src-mac, dst-mac, src-dst-mac, src-ip, dst-ip, src-dst-ip...)
Switch(config)# interface range g0/1 - 2                      ! configure the members together
Switch(config-if-range)# channel-group 1 mode active          ! LACP (active/passive); desirable/auto = PAgP; on = static
Switch(config-if-range)# channel-protocol lacp                ! force the protocol (optional, rarely useful)
Switch(config-if-range)# no switchport                        ! before channel-group: Layer 3 EtherChannel
Switch(config)# interface port-channel 1                      ! the virtual interface (Po1)
Switch(config-if)# switchport trunk encapsulation dot1q       ! on a switch supporting ISL and dot1q
Switch(config-if)# switchport mode trunk                      ! also applied to the members
Switch(config-if)# ip address 10.0.0.1 255.255.255.252        ! Layer 3 EtherChannel: IP on the port-channel
Switch(config)# ip routing                                    ! multilayer switch: enable the routing table
Switch(config)# ip route 172.16.2.0 255.255.255.0 10.0.0.2    ! static route
Switch# show etherchannel summary                             ! flags SU/RU, P, D, s, I
Switch# show etherchannel port-channel                        ! protocol, channel-group mode
Switch# show interfaces trunk                                 ! Po1 appears as a trunk
Switch# show spanning-tree                                    ! only Po1 appears
Switch# show cdp neighbors                                    ! (NetSim) local and remote interfaces of Cisco neighbors
```

### 10. The lab (video 048)

Goal: two access switches (ASW1, ASW2) each linked by two links to a distribution switch (DSW1, DSW2); Layer 2 EtherChannels (LACP then PAgP), static Layer 3 EtherChannel between DSW1 and DSW2, static routes, load balancing.

1. **ASW1-DSW1 with LACP**: on ASW1, `show spanning-tree`: G0/1 root port, G0/2 **alternate**. `interface range g0/1 - 2`, `channel-group 1 mode active`; `interface po1`, `switchport mode trunk`. `show run`: Po1 created, `switchport mode trunk` also on G0/1 and G0/2. `show etherchannel summary`: Po1 **SD** (Layer 2, down), members **I** (stand-alone) because DSW1 is not configured. On DSW1: `interface range g1/0/3 - 4`, `channel-group 1 mode active` (passive would work too), `interface po1`, `switchport trunk encapsulation dot1q` (this model supports ISL and dot1q), `switchport mode trunk`. Check: **SU**, members **P**; `show interface trunk`: Po1 trunk; on ASW1, `show spanning-tree`: G0/1 and G0/2 gone, **Port-channel 1 is the root port**, F0/1-2 designated (hosts).
2. **ASW2-DSW2 with PAgP**: same with `channel-group 1 mode desirable` on both sides, Po1 as trunk (dot1q encapsulation on DSW2). Check SU / P.
3. **DSW1-DSW2 static Layer 3**: `interface range g1/0/1 - 2`, `no switchport`, `channel-group 2 mode on` (group 1 already used); `interface po2`, `ip address 10.0.0.2 255.255.255.252` on DSW2 and 10.0.0.1 on DSW1. `show etherchannel summary`: **RU**, members P. `ping 10.0.0.2` from DSW1: OK.
4. **Static routes**: `show ip route` empty on the multilayer switch: `ip routing` is needed (the direct ping worked because directly connected). DSW1: `ip route 172.16.2.0 255.255.255.0 10.0.0.2`; DSW2: `ip routing`, `ip route 172.16.1.0 255.255.255.0 10.0.0.1`. Ping PC1 → SRV1 (172.16.2.1) via DSW1's VLAN 1 SVI then the Layer 3 port-channel: a few timeouts at first (ARP), then success.
5. **Load balancing**: `show etherchannel load-balance`: default **src-mac** on both models; `port-channel load-balance src-dst-ip` on all four switches, then verify.

Boson NetSim preview (CCNA lab "Layer 2 EtherChannel", task 1 planning): `show cdp neighbors` (CDP, Cisco Discovery Protocol, proprietary: local interface and neighbor port ID), `show ip interface brief` (up/up), `show interfaces trunk` (desirable, ISL negotiated by DTP), `show running-config` (members unconfigured), STP quiz: DSW2 F0/5 root port (same cost 19, same neighbor, lowest neighbor port ID), bandwidth 100,000 Kbit per link (`show interface f0/5`) → 200 Mbps with EtherChannel, F0/6 blocked by STP otherwise; up to 8 active members, 16 with LACP.

### 11. The quiz (video 047: 3 questions, plus one Boson ExSim question)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Q1. Channel-group mode combinations that result in an operational EtherChannel? (3) | **A on-on, C desirable-auto, G active-active** | on-on = static; desirable-auto = PAgP; active-active = LACP. passive-passive and auto-auto: neither side actively tries. active-desirable and on-desirable mix different modes. |
| Q2. In `show etherchannel summary`, the physical interfaces have flag (P): meaning? | **B, the interfaces are bundled in the port-channel** | The flag you want on members. Not "passive", not "paused", not "Layer 2" (that is S). |
| Q3. Member parameters that must match? (2) | **C interface speed, D switchport mode (access/trunk)** | The interface ID is unique; the IP address goes on the port-channel, not the members, even for Layer 3. |
| Boson ExSim. SwitchA: `interface port-channel 1`, `interface range f0/5 - 6`, `channel-protocol lacp`, `channel-group 1 mode on`; SwitchB: same with `channel-protocol pagp` and `mode on`. Result? | **B, no link is formed** | After `channel-protocol lacp` only active/passive are accepted; after `pagp` only desirable/auto: `mode on` is rejected on both sides, the interfaces never join the port-channel (created in advance but empty). |
