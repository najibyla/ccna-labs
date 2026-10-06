# CCNA Day 36 : CDP & LLDP

> Source : Jeremy's IT Lab, vidéo n°73 « CDP & LLDP | Day 36 » (cours, 39 min) et vidéo n°74 « CDP & LLDP | Day 36 Lab » (lab, 25 min) de la playlist. Fiche rédigée à partir des transcriptions le 6 octobre 2026. Les options des quiz Q3 et Q4 sont affichées à l'écran et absentes de la transcription.

## 🇫🇷 Version française

### 1. Protocoles de découverte de couche 2

- Sujet d'examen **2.3** : configurer et vérifier les protocoles de découverte de couche 2 CDP et LLDP.
- Ils **partagent des informations avec les équipements voisins directement connectés** et en apprennent sur eux : nom d'hôte, adresse IP, type d'équipement, etc. « Couche 2 » parce que le protocole lui-même n'utilise **pas d'adresse IP** (les trames ne contiennent pas de paquet IP), mais il peut transporter des informations de couche 3 comme des adresses IP.
- **CDP** (*Cisco Discovery Protocol*) : **propriétaire Cisco**. **LLDP** (*Link Layer Discovery Protocol*) : **standard industriel IEEE 802.1AB**, obligatoire en réseau multi-constructeurs (Cisco, Juniper, Palo Alto...).
- Ils peuvent être considérés comme un **risque de sécurité** (informations divulguées) et sont souvent désactivés ; c'est le choix de l'administrateur.
- Un switch n'inclut pas d'adresse IP dans ses messages si son interface n'en a pas.

### 2. CDP

- **Activé par défaut** sur les équipements Cisco (routeurs, switches, pare-feu, téléphones IP), globalement et sur chaque interface.
- Messages envoyés à la **MAC multicast 0100.0CCC.CCCC** (à mémoriser ; Wireshark l'affiche comme CDP/VTP/DTP/PAgP/UDLD car plusieurs protocoles la partagent). Un équipement qui reçoit un message CDP le **traite et le jette**, il ne le transmet pas : seuls les **voisins directement connectés** deviennent voisins CDP.
- **Timer 60 s** (envoi sur toutes les interfaces up), **holdtime 180 s** (voisin retiré de la table sans message pendant 180 s), **version 2 par défaut** (v2 détecte par exemple les mismatches de VLAN natif).
- `show cdp` : timer, holdtime, version (« CDP is not enabled » si désactivé). `show cdp traffic` : nombre de messages envoyés/reçus, par version. `show cdp interface [int]` : timer, holdtime, encapsulation **ARPA** (= Ethernet II, hors CCNA), nombre d'interfaces CDP up/down.
- `show cdp neighbors`, colonnes : **Device ID** (nom d'hôte du voisin), **Local Interface** (interface sur **cet** équipement), **Holdtime** (compte à rebours depuis 180, remis à 180 à chaque message, descend à 120 avec les timers par défaut), **Capability** (**R** router, **S** switch ; un switch multicouche affiche R et S ; I = IGMP et B = source route bridge, hors CCNA), **Platform** (modèle, ex. C2900, Catalyst 2960 ; vide sur les VM GNS3), **Port ID** (interface sur **le voisin**). Bien distinguer Local Interface et Port ID.
- `show cdp neighbors detail` : en plus, **version logicielle (IOS)**, **informations VTP** (seul CDP le peut, VTP étant propriétaire Cisco), **VLAN natif**, **duplex** (CDP signale les mismatches), **adresse IP** du voisin. `show cdp entry <nom>` : même sortie pour un seul voisin.

### 3. LLDP

- Standard industriel créé après CDP. **Généralement désactivé par défaut** sur Cisco ; CDP et LLDP peuvent tourner **en même temps**.
- MAC multicast **0180.C200.000E**. Traité et jeté sans retransmission : voisins directement connectés seulement.
- **Timer 30 s** (moitié de CDP), **holdtime 120 s**, **reinitialization delay 2 s** (retarde le démarrage de LLDP après activation, contre le flapping ; probablement hors CCNA mais visible dans les sorties).
- Activation : `lldp run` en global, puis **deux commandes par interface** : `lldp transmit` (envoi, Tx) et `lldp receive` (réception, Rx). CDP n'avait qu'une commande `cdp enable`. Remarque du lab : sur les équipements testés, `lldp run` active aussi Tx/Rx sur les interfaces ; cela dépend du modèle et de l'IOS, et dans le lab elles ont été désactivées exprès.
- `show lldp` (statut, timers 30/120/2), `show lldp traffic`, `show lldp interface` (Tx/Rx enabled ou disabled ; états **Tx = IDLE** en attente d'envoi, **Rx = WAIT FOR FRAME**).
- `show lldp neighbors` : Device ID, Local Intf, **Hold-time = valeur configurée (120), ne décompte pas**, Capability (**R** router, **B = Bridge**, c'est-à-dire switch ; **pas de code S** en LLDP), Port ID.
- `show lldp neighbors detail` / `show lldp entry <nom>` : version de l'OS, **Time remaining** (le holdtime qui décompte, visible seulement en detail), **deux champs** de capacités : **System Capabilities** (ce que l'équipement sait faire, ex. B,R pour un switch multicouche) et **Enabled Capabilities** (ce qui est actif ; R apparaît après `ip routing` sur le switch). **Pas d'informations VTP**. Le **chassis ID** du voisin est son adresse MAC (bonus NetSim).
- Captures Wireshark : trame CDP (v2, TTL = holdtime, device ID, version, platform, addresses, port ID, capabilities Router + Source Route Bridge), trame LLDP (TTL 120, system name, capabilities Bridge et Router, enabled Router) ; **aucun paquet IP** dans les trames.

### 4. Pièges d'examen

- Défauts CDP : **activé**, timer **60**, holdtime **180**, **v2**. Défauts LLDP : **désactivé**, timer **30**, holdtime **120**, reinit **2**.
- Les timers configurés se lisent dans `show cdp` et `show cdp interface`, pas dans `show cdp neighbors` (qui montre seulement le holdtime qui décompte).
- `show cdp neighbors` n'affiche **ni l'adresse IP ni la version logicielle** du voisin : il faut `show cdp neighbors detail` (bonus Boson).
- En LLDP, un switch est un **Bridge (B)**, jamais S ; capacités système d'un switch multicouche : **B,R**.
- LLDP exige **transmit et receive séparément** ; il peut donner la version de l'OS du voisin, mais pas ses réglages OSPF ni VTP (quiz Q4).
- `cdp run` / `lldp run` en global ; `cdp enable` / `lldp transmit` + `lldp receive` sur l'interface.
- MAC : CDP **0100.0CCC.CCCC**, LLDP **0180.C200.000E** (flashcards).

### 5. Commandes IOS

```
R1(config)# cdp run                      ! active CDP globalement (défaut) ; no cdp run pour désactiver
R1(config-if)# cdp enable                ! active CDP sur l'interface (défaut) ; no cdp enable pour désactiver
R1(config)# cdp timer 60                 ! intervalle d'envoi (défaut 60 s)
R1(config)# cdp holdtime 180             ! holdtime (défaut 180 s)
R1(config)# cdp advertise-v2             ! version 2 (défaut) ; no ... pour la version 1
R1# show cdp                             ! timer, holdtime, version
R1# show cdp traffic                     ! messages envoyés / reçus
R1# show cdp interface [g0/0]            ! timers par interface, nombre d'interfaces CDP
R1# show cdp neighbors                   ! table des voisins
R1# show cdp neighbors detail            ! + IOS, VTP, VLAN natif, duplex, adresse IP
R1# show cdp entry R2                    ! détail d'un seul voisin
R1(config)# lldp run                     ! active LLDP globalement (désactivé par défaut)
R1(config-if)# lldp transmit             ! envoi LLDP sur l'interface (Tx)
R1(config-if)# lldp receive              ! réception LLDP sur l'interface (Rx)
R1(config)# lldp timer 30                ! intervalle (défaut 30 s)
R1(config)# lldp holdtime 120            ! holdtime (défaut 120 s)
R1(config)# lldp reinit 2                ! délai de réinitialisation (défaut 2 s)
R1# show lldp | show lldp traffic | show lldp interface
R1# show lldp neighbors | show lldp neighbors detail | show lldp entry SW1
SW1# show interfaces status              ! interfaces « connected » (pour trouver le port d'un PC, lab)
```

### 6. Le lab (vidéo n°74)

Objectif : cartographier un réseau sans étiquettes (R1, R2, R3, SW1-3, PC1-3) avec CDP, désactiver CDP sur les ports des PC, puis passer tout le réseau à LLDP. Les commandes de timers CDP/LLDP ne sont **pas supportées par Packet Tracer**.

1. **PC** : `ipconfig` donne l'adresse, le masque et la passerelle : PC1 192.168.1.1/24, gateway 192.168.1.254 (R1) ; PC2 192.168.2.1/24 → R2 .254 ; PC3 192.168.3.1/24 → R3 .254.
2. **Switches** : `show cdp neighbors` donne les paires d'interfaces (SW1 G0/1 ↔ R1 G0/2 ; SW2 G0/2 ↔ R2 G0/1 ; SW3 G0/1 ↔ R3 G0/0). Le PC n'utilise pas CDP : `show interfaces status` montre la seule autre interface **connected** (SW1 F0/10, SW2 F0/1, SW3 F0/24) ; avec plusieurs PC on comparerait les MAC avec la table d'adresses MAC. Puis `interface f0/10`, `do show cdp interface f0/10` (activé), `no cdp enable`, nouvelle vérification (aucune sortie = désactivé).
3. **Routeurs** : `show cdp neighbors` sur R1 (G0/0 ↔ R3 G0/1 ; G0/1 ↔ R2 G0/0), sur R2 (G0/2 ↔ R3 G0/2). `show interfaces g0/0` donne l'IP **avec la longueur de préfixe** (contrairement à `show ip interface brief`) : 10.0.13.1/30, donc R3 = .2 (seule autre adresse d'un /30), confirmé par `show cdp entry R3` ; 10.0.12.1/30 (R2 = .2) ; 10.0.23.1/30 sur R2 (R3 = .2).
4. **Passage à LLDP** sur chaque équipement : `no cdp run`, `lldp run`, puis sur les interfaces reliées à un autre équipement réseau (`interface g0/1` sur un switch, `interface range g0/0 - 2` sur un routeur) : `lldp transmit`, `lldp receive`.
5. Mode simulation : on voit passer EIGRP (préconfiguré), STP, **LLDP**, parfois DTP, plus de CDP. Exercice supplémentaire : refaire les étiquettes avec LLDP.

Bonus NetSim (Link-Layer Discovery Protocol) : `show lldp` (non actif) → `lldp run` → `show lldp` (status ACTIVE) ; `show lldp neighbors` (Router2) ; `show lldp neighbors detail` : chassis ID = MAC du voisin, time remaining 97 puis 93 s ; `show lldp interface f0/0` (Tx IDLE, Rx WAIT FOR FRAME) ; `no lldp transmit` (Tx disabled, Rx toujours enabled) puis `lldp transmit` ; `lldp holdtime 60`, `lldp timer 15`, vérifiés avec `show lldp`.

### 7. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Commandes qui montrent les timers CDP configurés (deux réponses) ? | **`show cdp`** et **`show cdp interface`** | `show cdp neighbors` montre le holdtime qui décompte, pas les valeurs configurées ni le timer ; `show cdp traffic` compte les messages. |
| Commandes correspondant à l'état CDP par défaut (deux réponses) ? | **`cdp enable`** (interface) et **`cdp timer 60`** | `no cdp run` désactive CDP (activé par défaut) ; le holdtime par défaut est 180, pas 120. |
| `show lldp entry SW1` (switch multicouche) : champ System Capabilities ? | **B,R** | B = bridge (switch), R = router ; S n'existe pas en LLDP. |
| Affirmations vraies sur LLDP (deux réponses) ? | **Transmit et receive s'activent séparément par interface** ; **LLDP permet d'apprendre la version de l'OS du voisin** | LLDP est un standard (pas propriétaire), timer par défaut 30 s, il ne donne ni les réglages OSPF ni VTP. |
| Sur quelle interface de R2 est connecté SW2 (table CDP de R2) ? | **G0/1** | Colonne **Local Interface** = interface de R2 ; Port ID serait l'interface de SW2. |

Bonus Boson (`show cdp neighbors`, quatre réponses) : interface du voisin (Port ID), device ID, interface locale, capacités et modèle. **Pas** l'adresse IP ni la version logicielle (réservées à `show cdp neighbors detail`).

---

## 🇬🇧 English version

### 1. Layer 2 discovery protocols

- Exam topic **2.3**: configure and verify Layer 2 discovery protocols CDP and LLDP.
- They **share information with, and discover information about, directly connected neighbors**: host name, IP address, device type, etc. "Layer 2" because the protocols themselves use **no IP addresses** (the frames contain no IP packet), but they can carry Layer 3 information such as IP addresses.
- **CDP** (Cisco Discovery Protocol): **Cisco proprietary**. **LLDP** (Link Layer Discovery Protocol): **industry standard IEEE 802.1AB**, required in multi-vendor networks (Cisco, Juniper, Palo Alto...).
- They can be considered a **security risk** (information shared) and are often disabled; it is the admin's choice.
- A switch does not include an IP address in its messages if its interface has none.

### 2. CDP

- **Enabled by default** on Cisco devices (routers, switches, firewalls, IP phones), globally and on each interface.
- Messages sent to **multicast MAC 0100.0CCC.CCCC** (memorize; Wireshark labels it CDP/VTP/DTP/PAgP/UDLD since several protocols share it). A device receiving a CDP message **processes and discards** it, never forwards it: only **directly connected neighbors** become CDP neighbors.
- **Timer 60 s** (sent out of all up interfaces), **holdtime 180 s** (neighbor removed from the table after 180 s without a message), **version 2 by default** (v2 can detect native VLAN mismatches, for example).
- `show cdp`: timer, holdtime, version ("CDP is not enabled" if disabled). `show cdp traffic`: messages sent/received, per version. `show cdp interface [int]`: timer, holdtime, encapsulation **ARPA** (= Ethernet II, beyond the CCNA), number of CDP interfaces up/down.
- `show cdp neighbors`, columns: **Device ID** (neighbor's host name), **Local Interface** (interface on **this** device), **Holdtime** (counts down from 180, reset to 180 on each message, reaches 120 with default timers), **Capability** (**R** router, **S** switch; a multilayer switch shows R and S; I = IGMP and B = source route bridge, beyond the CCNA), **Platform** (model, e.g. C2900, Catalyst 2960; empty on GNS3 VMs), **Port ID** (interface on **the neighbor**). Distinguish Local Interface from Port ID.
- `show cdp neighbors detail`: also **software (IOS) version**, **VTP information** (only CDP can, VTP being Cisco proprietary), **native VLAN**, **duplex** (CDP reports mismatches), neighbor's **IP address**. `show cdp entry <name>`: same output for a single neighbor.

### 3. LLDP

- Industry standard created after CDP. **Usually disabled by default** on Cisco; CDP and LLDP can run **at the same time**.
- Multicast MAC **0180.C200.000E**. Processed and discarded, not forwarded: directly connected neighbors only.
- **Timer 30 s** (half of CDP), **holdtime 120 s**, **reinitialization delay 2 s** (delays LLDP start-up after enabling, against flapping; probably beyond the CCNA but visible in outputs).
- Enabling: `lldp run` globally, then **two commands per interface**: `lldp transmit` (send, Tx) and `lldp receive` (receive, Rx). CDP had a single `cdp enable`. Lab note: on the devices tested, `lldp run` also enabled Tx/Rx on interfaces; it depends on the model and IOS, and in the lab they were deliberately disabled.
- `show lldp` (status, timers 30/120/2), `show lldp traffic`, `show lldp interface` (Tx/Rx enabled or disabled; states **Tx = IDLE** waiting to send, **Rx = WAIT FOR FRAME**).
- `show lldp neighbors`: Device ID, Local Intf, **Hold-time = configured value (120), does not count down**, Capability (**R** router, **B = Bridge**, i.e. switch; **no S code** in LLDP), Port ID.
- `show lldp neighbors detail` / `show lldp entry <name>`: OS version, **Time remaining** (the holdtime counting down, only visible in detail), **two capability fields**: **System Capabilities** (what the device can do, e.g. B,R for a multilayer switch) and **Enabled Capabilities** (what is active; R appears after `ip routing` on the switch). **No VTP information**. The neighbor's **chassis ID** is its MAC address (NetSim bonus).
- Wireshark captures: CDP frame (v2, TTL = holdtime, device ID, version, platform, addresses, port ID, capabilities Router + Source Route Bridge), LLDP frame (TTL 120, system name, capabilities Bridge and Router, enabled Router); **no IP packet** in the frames.

### 4. Exam traps

- CDP defaults: **enabled**, timer **60**, holdtime **180**, **v2**. LLDP defaults: **disabled**, timer **30**, holdtime **120**, reinit **2**.
- Configured timers are read with `show cdp` and `show cdp interface`, not `show cdp neighbors` (which only shows the holdtime counting down).
- `show cdp neighbors` shows **neither the neighbor's IP address nor its software version**: use `show cdp neighbors detail` (Boson bonus).
- In LLDP a switch is a **Bridge (B)**, never S; system capabilities of a multilayer switch: **B,R**.
- LLDP requires **transmit and receive separately**; it can give the neighbor's OS version, but not its OSPF or VTP settings (quiz Q4).
- `cdp run` / `lldp run` globally; `cdp enable` / `lldp transmit` + `lldp receive` on the interface.
- MACs: CDP **0100.0CCC.CCCC**, LLDP **0180.C200.000E** (flashcards).

### 5. IOS commands

```
R1(config)# cdp run                      ! enables CDP globally (default); no cdp run to disable
R1(config-if)# cdp enable                ! enables CDP on the interface (default); no cdp enable to disable
R1(config)# cdp timer 60                 ! message interval (default 60 s)
R1(config)# cdp holdtime 180             ! holdtime (default 180 s)
R1(config)# cdp advertise-v2             ! version 2 (default); no ... for version 1
R1# show cdp                             ! timer, holdtime, version
R1# show cdp traffic                     ! messages sent / received
R1# show cdp interface [g0/0]            ! per-interface timers, number of CDP interfaces
R1# show cdp neighbors                   ! neighbor table
R1# show cdp neighbors detail            ! + IOS, VTP, native VLAN, duplex, IP address
R1# show cdp entry R2                    ! detail for a single neighbor
R1(config)# lldp run                     ! enables LLDP globally (disabled by default)
R1(config-if)# lldp transmit             ! LLDP sending on the interface (Tx)
R1(config-if)# lldp receive              ! LLDP receiving on the interface (Rx)
R1(config)# lldp timer 30                ! interval (default 30 s)
R1(config)# lldp holdtime 120            ! holdtime (default 120 s)
R1(config)# lldp reinit 2                ! reinitialization delay (default 2 s)
R1# show lldp | show lldp traffic | show lldp interface
R1# show lldp neighbors | show lldp neighbors detail | show lldp entry SW1
SW1# show interfaces status              ! "connected" interfaces (to find a PC's port, lab)
```

### 6. The lab (video 74)

Goal: map an unlabeled network (R1, R2, R3, SW1-3, PC1-3) with CDP, disable CDP on PC-facing ports, then switch the whole network to LLDP. CDP/LLDP timer commands are **not supported in Packet Tracer**.

1. **PCs**: `ipconfig` gives address, mask and gateway: PC1 192.168.1.1/24, gateway 192.168.1.254 (R1); PC2 192.168.2.1/24 → R2 .254; PC3 192.168.3.1/24 → R3 .254.
2. **Switches**: `show cdp neighbors` gives the interface pairs (SW1 G0/1 ↔ R1 G0/2; SW2 G0/2 ↔ R2 G0/1; SW3 G0/1 ↔ R3 G0/0). PCs do not use CDP: `show interfaces status` shows the only other **connected** interface (SW1 F0/10, SW2 F0/1, SW3 F0/24); with many PCs you would compare MACs with the MAC address table. Then `interface f0/10`, `do show cdp interface f0/10` (enabled), `no cdp enable`, check again (no output = disabled).
3. **Routers**: `show cdp neighbors` on R1 (G0/0 ↔ R3 G0/1; G0/1 ↔ R2 G0/0), on R2 (G0/2 ↔ R3 G0/2). `show interfaces g0/0` gives the IP **with the prefix length** (unlike `show ip interface brief`): 10.0.13.1/30, so R3 = .2 (only other address in a /30), confirmed by `show cdp entry R3`; 10.0.12.1/30 (R2 = .2); 10.0.23.1/30 on R2 (R3 = .2).
4. **Switch to LLDP** on every device: `no cdp run`, `lldp run`, then on interfaces connected to another network device (`interface g0/1` on a switch, `interface range g0/0 - 2` on a router): `lldp transmit`, `lldp receive`.
5. Simulation mode: EIGRP (preconfigured), STP, **LLDP**, sometimes DTP, no more CDP. Extra practice: redo the labels using LLDP.

NetSim bonus (Link-Layer Discovery Protocol): `show lldp` (not running) → `lldp run` → `show lldp` (status ACTIVE); `show lldp neighbors` (Router2); `show lldp neighbors detail`: chassis ID = neighbor's MAC, time remaining 97 then 93 s; `show lldp interface f0/0` (Tx IDLE, Rx WAIT FOR FRAME); `no lldp transmit` (Tx disabled, Rx still enabled) then `lldp transmit`; `lldp holdtime 60`, `lldp timer 15`, checked with `show lldp`.

### 7. The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Commands showing the configured CDP timers (select two)? | **`show cdp`** and **`show cdp interface`** | `show cdp neighbors` shows the holdtime counting down, not the configured values or the timer; `show cdp traffic` counts messages. |
| Commands representing the default CDP state (select two)? | **`cdp enable`** (interface) and **`cdp timer 60`** | `no cdp run` disables CDP (enabled by default); the default holdtime is 180, not 120. |
| `show lldp entry SW1` (multilayer switch): System Capabilities field? | **B,R** | B = bridge (switch), R = router; S does not exist in LLDP. |
| True statements about LLDP (select two)? | **Transmit and receive are enabled separately per interface**; **LLDP can learn the neighbor's OS version** | LLDP is a standard (not proprietary), default timer 30 s, it gives neither OSPF nor VTP settings. |
| Which R2 interface is SW2 connected to (R2's CDP table)? | **G0/1** | **Local Interface** column = R2's interface; Port ID would be SW2's interface. |

Boson bonus (`show cdp neighbors`, select four): neighbor's interface (Port ID), device ID, local interface, capabilities and model. **Not** the IP address or software version (only in `show cdp neighbors detail`).
