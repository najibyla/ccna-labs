# CCNA Day 17 : VLANs (Part 2) / VLAN, partie 2 : trunks, 802.1Q, router on a stick

> Source : Jeremy's IT Lab, « Free CCNA | VLANs (Part 2) | Day 17 » (40 min, vidéo n°31 de la playlist, cours) et « VLANs (Part 2) | Day 17 Lab » (23 min, vidéo n°32, lab Packet Tracer suivi d'un aperçu Boson NetSim). Flashcards disponibles. Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Pourquoi des ports trunk ?

- Nouvelle topologie : deux switches, VLAN10 (ingénierie) **réparti sur les deux switches** (fréquent : un service n'est pas toujours regroupé au même endroit). Avec seulement des ports d'accès, il faut **un lien par VLAN** entre SW1 et SW2 : un en VLAN10 (PC VLAN10 sur les deux switches, et accès à R1 via SW2), un en VLAN30. Pas de lien VLAN20 : aucun PC VLAN20 sur SW1 ; un PC VLAN20 joint quand même un PC VLAN10 de SW1 grâce au **routage inter-VLAN de R1** (le trafic revient de R1 sur l'interface VLAN10 de SW2, puis passe par le lien VLAN10).
- Avec beaucoup de VLAN, cette méthode gaspille des interfaces et le routeur n'en a pas assez. Solution : le **port trunk**, qui transporte le trafic de **plusieurs VLAN sur une seule interface** (switch–switch et switch–routeur). Un port d'accès n'appartient qu'à un seul VLAN.

### 2. L'étiquetage des trames (*VLAN tagging*)

- Problème : SW1 reçoit une trame sur le trunk où les VLAN 10 et 30 sont permis ; comment sait-il à quel VLAN elle appartient ? Les switches **étiquettent** (*tag*) toutes les trames envoyées sur un trunk. Autre nom : port trunk = **port tagged**, port d'accès = **port untagged** (pas besoin d'étiquette, le port n'a qu'un VLAN).
- Deux protocoles : **ISL** (*Inter-Switch Link*), ancien, propriétaire Cisco, et **IEEE 802.1Q** (« dot1q »), standard de l'industrie (IEEE, comme 802.3 Ethernet). ISL n'est pratiquement jamais utilisé, les équipements Cisco modernes ne le supportent même plus ; pour le CCNA, seul dot1q compte (savoir ce qu'est ISL suffit).

### 3. L'étiquette 802.1Q

- Insérée **entre le champ MAC source et le champ Type/Longueur** de l'en-tête Ethernet. Taille : **4 octets (32 bits)**. Deux champs principaux : **TPID** et **TCI**.

| Champ | Taille | Rôle |
| :--- | :--- | :--- |
| **TPID** (*Tag Protocol Identifier*) | 16 bits (2 octets) | Toujours **0x8100** (4 chiffres hexadécimaux × 4 bits). Se trouve là où est normalement le champ Type : cette valeur indique au switch que la trame est étiquetée dot1q. |
| **TCI** (*Tag Control Information*) | 16 bits | Trois sous-champs ci-dessous. |
| PCP (*Priority Code Point*) | 3 bits | **Class of Service (CoS)** : priorise le trafic important en cas de congestion. Connaître le nom et l'usage suffit. |
| DEI (*Drop Eligible Indicator*) | 1 bit | Trames **pouvant être abandonnées** en cas de congestion. Nom et usage suffisent. |
| **VID** (*VLAN ID*) | 12 bits | **Identifie le VLAN** : le champ le plus important. 2^12 = 4 096 VLAN ; 0 et 4 095 réservés → **plage utilisable 1 à 4 094** (ISL : même plage). |

- **VLAN normaux** : 1 à 1005. **VLAN étendus** (*extended*) : 1006 à 4094 ; certains vieux équipements ne les supportent pas, les switches modernes oui.

### 4. Le VLAN natif (*native VLAN*)

- Fonctionnalité de dot1q (ISL ne l'a pas). Par défaut **VLAN 1** sur tous les ports trunk, configurable **port trunk par port trunk** (pas un réglage global).
- Le switch **n'ajoute pas d'étiquette** aux trames du VLAN natif. Un switch qui reçoit une **trame non étiquetée sur un trunk** suppose qu'elle appartient au VLAN natif.
- **Le VLAN natif doit correspondre entre les deux switches.** Exemple de désaccord : SW2 natif = VLAN10, SW1 natif = VLAN30 ; la trame VLAN10 part sans étiquette, SW1 la croit en VLAN30, la destination est en VLAN10 → **trame non transmise**. Les switches continuent de transmettre en cas de désaccord, mais des problèmes apparaissent.
- Bonne pratique de sécurité : changer le VLAN natif pour un **VLAN inutilisé** (ex. 1001), et le faire correspondre entre switches.

### 5. Configuration des trunks

- `switchport mode trunk` peut être **rejeté** : « Command rejected: An interface whose trunk encapsulation is "Auto" can not be configured to "trunk" mode. » Sur les switches supportant ISL **et** dot1q, l'encapsulation est « Auto » par défaut : il faut d'abord `switchport trunk encapsulation dot1q` (options : dot1q, isl, negotiate = auto). Sur les switches dot1q seulement, `switchport mode trunk` suffit.
- `show interfaces trunk` : **Mode « on »** = trunk configuré manuellement ; Encapsulation 802.1q ; Status trunking ; **Native vlan 1** ; « Vlans allowed on trunk » : **par défaut tous, 1-4094** ; « Vlans allowed and active in management domain » : les VLAN permis **qui existent sur le switch** (1, 10, 30 ; les 1002-1005 n'y apparaissent pas) ; « Vlans in spanning tree forwarding state and not pruned » (vu plus tard).
- Limiter les VLAN permis (sécurité, et performance : les broadcasts des autres VLAN ne traversent pas le trunk) :
  - `switchport trunk allowed vlan 10,30` : liste exacte.
  - `... add 20` : ajoute à la liste. VLAN20 non créé sur le switch → il apparaît dans « allowed » mais **pas** dans « allowed and active ».
  - `... remove 20` : retire. `... all` : tous (= défaut). `... except 1-5,10` : tous sauf (6-9 et 11-4094). `... none` : aucun, plus aucun trafic ne passe.
- `switchport trunk native vlan 1001` : change le VLAN natif.
- **`show vlan brief` ne liste pas les ports trunk** (G0/0 n'apparaît ni en VLAN10 ni en VLAN30) : il montre les ports d'accès. Pour les trunks, `show interfaces trunk`.
- SW2 : G0/0 (vers SW1) permet 10,30 ; G0/1 (vers R1) permet 10,20,30.

### 6. Router on a stick (ROAS)

- Une **seule interface physique** entre le routeur et le switch (elle ressemble à un « bâton » sur le schéma), divisée en **sous-interfaces** (*subinterfaces*) : G0/0.10 pour VLAN10, G0/0.20 pour VLAN20, G0/0.30 pour VLAN30. Côté switch : **un trunk ordinaire** qui permet les VLAN 10, 20 et 30, rien de plus.
- Routeur : `no shutdown` sur l'interface physique (désactivée par défaut) ; `interface g0/0.10` ; `encapsulation dot1q 10` ; `ip address` (dernière adresse utilisable du sous-réseau). Le numéro de sous-interface **n'a pas** à égaler le numéro de VLAN, mais c'est **fortement recommandé**.
- `encapsulation dot1q 10` : le routeur traite toute trame **étiquetée VLAN10** comme arrivée sur G0/0.10, et **étiquette VLAN10** toutes les trames qui en sortent.
- `show ip interface brief` : les sous-interfaces apparaissent, l'interface physique n'a pas d'adresse. Table de routage : routes connected et local, comme pour des interfaces physiques. Un paquet pour 192.168.1.64/26 sort par G0/0 étiqueté VLAN20.
- Trajet PC VLAN10 → PC VLAN30 : SW2 envoie à R1 étiqueté VLAN10 ; R1 le reçoit « sur G0/0.10 », route vers 192.168.1.128/26 (G0/0.30), renvoie étiqueté VLAN30 ; SW2 → SW1 étiqueté VLAN30 ; SW1 → destination.

### 7. Pièges d'examen

- Étiquette dot1q : **4 octets, entre MAC source et Type**, TPID **0x8100**, VID **12 bits**, VLAN **1-4094**.
- VLAN natif : **non étiqueté**, défaut **1**, **doit correspondre** des deux côtés.
- `switchport trunk allowed vlan 10` **remplace** la liste ; `add` ajoute.
- Un VLAN permis mais **inexistant** sur le switch n'est pas « active » : le trunk ne le transporte pas tant qu'on n'a pas fait `vlan N`.
- `show vlan brief` ne montre pas les trunks.
- `encapsulation dot1q` est une commande **de sous-interface de routeur**, pas de switch.

### 8. Commandes IOS

```
Switch(config-if)# switchport trunk encapsulation dot1q    ! requis avant « mode trunk » sur les switches ISL+dot1q
Switch(config-if)# switchport mode trunk                   ! configure manuellement un trunk
Switch(config-if)# switchport trunk allowed vlan 10,30     ! liste exacte des VLAN permis
Switch(config-if)# switchport trunk allowed vlan add 20    ! ajoute à la liste
Switch(config-if)# switchport trunk allowed vlan remove 20 ! retire de la liste
Switch(config-if)# switchport trunk allowed vlan all       ! tous (état par défaut)
Switch(config-if)# switchport trunk allowed vlan except 1-5,10   ! tous sauf ceux-là
Switch(config-if)# switchport trunk allowed vlan none      ! aucun
Switch(config-if)# switchport trunk native vlan 1001       ! VLAN natif (VLAN inutilisé recommandé)
Switch# show interfaces trunk                              ! trunks, mode, encapsulation, natif, VLAN permis/actifs
Switch(config)# vlan 30                                    ! crée un VLAN manquant pour qu'il soit « active »
Router(config)# interface g0/0
Router(config-if)# no shutdown                             ! interface physique activée
Router(config)# interface g0/0.10                          ! sous-interface (numéro = VLAN recommandé)
Router(config-subif)# encapsulation dot1q 10               ! trames étiquetées VLAN10 ↔ cette sous-interface
Router(config-subif)# ip address 10.0.0.62 255.255.255.192 ! passerelle du VLAN10
Router# show ip interface brief                            ! sous-interfaces et leurs adresses
Router# show ip route                                      ! routes connected/local des sous-interfaces
```

### 9. Le lab (vidéo n°32)

**Objectif** : même topologie que le cours (adresses dans 10.0.0.0/26 ×3) : ports d'accès, trunk SW1–SW2, ROAS entre SW2 et R1.

1. **Ports d'accès** : SW1 `interface range f0/1-2` → VLAN10, `f0/3-4` → VLAN30 ; SW2 `f0/1` → VLAN20, `interface range f0/2-3` → VLAN10. Le switch crée les VLAN.
2. **Trunk SW1–SW2 (G0/1)** : `switchport trunk ?` ne propose pas « encapsulation » : ce modèle ne supporte que dot1q (ce n'est pas une limite de Packet Tracer). `switchport mode trunk`, `switchport trunk allowed vlan 10,30` (pas de VLAN20 : aucun hôte VLAN20 sur SW1 ; PC5 en VLAN20 passe par R1), `switchport trunk native vlan 1001`. `do show vlan brief` : VLAN 10 et 30 existent sur SW1. Même configuration sur SW2 G0/1. **Sur SW2, `do show interfaces trunk` montre seulement VLAN10 en « allowed and active »** : VLAN30 n'existe pas sur SW2 (seuls 10 et 20 ont été créés par les ports d'accès) → `vlan 30`, `exit`, revérifier.
3. **ROAS** : SW2 `interface g0/2`, `switchport mode trunk`, `switchport trunk allowed vlan 10,20,30`, `switchport trunk native vlan 1001`. R1 : `interface g0/0`, `no shutdown` ; `interface g0/0.10`, `encapsulation dot1q 10`, `ip address 10.0.0.62 255.255.255.192` ; `g0/0.20` → 10.0.0.126 ; `g0/0.30` → 10.0.0.190. Pourquoi la dernière adresse utilisable ? Pas obligatoire, mais **adopter un système cohérent** (première ou dernière) dans tout le réseau.
4. **Tests** depuis PC7 (VLAN10) : `ping 10.0.0.1` (PC1, même VLAN : trame envoyée directement, sans routage) ; `ping 10.0.0.65` (PC5, VLAN20 : passe par R1 puis revient à SW2) ; `ping 10.0.0.129` (PC3, VLAN30 : R1, puis SW2, SW1). À observer en mode simulation.

**Aperçu Boson NetSim « Inter-VLAN Routing 1 »** (tâche 1 seulement) : `ipconfig /all` sur les PC (vérifier IP /25, masque, passerelle) ; `hostname Switch1` ; `vlan 10` et `vlan 12` ; trouver le port de chaque PC via sa « Physical Address » (MAC) et `show mac-address-table` (avec trait d'union sur ce switch ; `show mac address-table` sur les plus récents) : PC1 sur F0/3 → VLAN10, PC2 sur F0/4 → VLAN12 ; le ping PC1 → PC2 échoue car **aucun routage inter-VLAN n'est configuré** (F0/1 n'est pas trunk d'après `show interfaces trunk`, pas de sous-interfaces sur R1 d'après `show ip interface brief`).

### 10. Le quiz du Day 17 (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Envoyer les trames VLAN10 **non étiquetées** sur le trunk G0/1 de SW1 : A) encapsulation dot1q 10, B) switchport trunk allowed vlan 10, C) … add 10, D) switchport trunk native vlan 10 | **D** | Le VLAN natif est envoyé sans étiquette. A est une commande de sous-interface de routeur ; B et C modifient les VLAN permis. |
| Revenir à l'état par défaut des VLAN permis : A) … default, B) … all, C) … none, D) … 1,1001-1005 | **B** | Par défaut tous les VLAN sont permis. D liste les VLAN existant par défaut sur le switch, ce qui est différent. |
| `switchport mode trunk` rejeté, quelle commande peut corriger ? A) switch port mode trunk, B) … encapsulation 802.1q, C) switchport trunk encapsulation dot1q, D) … encapsulation auto | **C** | Sur les switches supportant ISL et dot1q il faut fixer l'encapsulation d'abord (ISL possible mais quasi jamais utilisé). |
| Quel champ de l'étiquette 802.1Q identifie le VLAN ? A) TPID, B) VID, C) TCI, D) VLN | **B** | VID = VLAN ID, 12 bits. TPID = 0x8100 identifie la trame comme étiquetée ; PCP sert au CoS ; VLN n'existe pas. |
| `switchport trunk allowed vlan add 10` fait, mais VLAN10 absent de « allowed and active in management domain » : A) VLAN10 n'existe pas sur le switch, B) commande invalide, C) il fallait « allowed vlan 10 », D) VLAN10 réservé | **A** | Un VLAN permis mais inexistant sur le switch n'apparaît pas dans cette section. |

---

## 🇬🇧 English version

### 1. Why trunk ports?

- New topology: two switches, VLAN10 (engineering) **split between both switches** (very common: departments are not always in one place). With access ports only, **one link per VLAN** is needed between SW1 and SW2: one in VLAN10 (VLAN10 PCs on both switches, and access to R1 via SW2), one in VLAN30. No VLAN20 link: no VLAN20 PCs on SW1; a VLAN20 PC still reaches a VLAN10 PC on SW1 thanks to **R1's inter-VLAN routing** (traffic comes back from R1 on SW2's VLAN10 interface, then crosses the VLAN10 link).
- With many VLANs this wastes interfaces and routers run out of them. Solution: the **trunk port**, which carries traffic from **multiple VLANs over a single interface** (switch-to-switch and switch-to-router). An access port belongs to a single VLAN only.

### 2. VLAN tagging

- Problem: SW1 receives a frame on the trunk where VLANs 10 and 30 are allowed; how does it know which VLAN it belongs to? Switches **tag** all frames sent over a trunk link. Other names: trunk port = **tagged port**, access port = **untagged port** (no tag needed, the port has only one VLAN).
- Two trunking protocols: **ISL** (Inter-Switch Link), old, Cisco proprietary, and **IEEE 802.1Q** ("dot1q"), the industry standard (IEEE, like 802.3 Ethernet). ISL is almost never used, even modern Cisco equipment does not support it; for the CCNA only dot1q matters (just know what ISL is).

### 3. The 802.1Q tag

- Inserted **between the Source MAC and the Type/Length fields** of the Ethernet header. Size: **4 bytes (32 bits)**. Two main fields: **TPID** and **TCI**.

| Field | Size | Role |
| :--- | :--- | :--- |
| **TPID** (Tag Protocol Identifier) | 16 bits (2 bytes) | Always **0x8100** (4 hex digits × 4 bits). Located where the Type field usually is: this value tells the switch the frame is dot1q-tagged. |
| **TCI** (Tag Control Information) | 16 bits | Three sub-fields below. |
| PCP (Priority Code Point) | 3 bits | **Class of Service (CoS)**: prioritizes important traffic in congested networks. Know the name and purpose. |
| DEI (Drop Eligible Indicator) | 1 bit | Marks frames that **can be dropped** when the network is congested. Name and purpose are enough. |
| **VID** (VLAN ID) | 12 bits | **Identifies the VLAN**: the most important field. 2^12 = 4,096 VLANs; 0 and 4,095 reserved → **usable range 1 to 4,094** (ISL: same range). |

- **Normal VLANs**: 1 to 1005. **Extended VLANs**: 1006 to 4094; some older devices cannot use them, modern switches support the whole range.

### 4. The native VLAN

- A dot1q feature (ISL does not have it). Default **VLAN 1** on all trunk ports, configurable **per trunk port** (not a global switch setting).
- The switch **does not add a tag** to frames in the native VLAN. A switch receiving an **untagged frame on a trunk port** assumes it belongs to the native VLAN.
- **The native VLAN must match between switches.** Mismatch example: SW2 native = VLAN10, SW1 native = VLAN30; the VLAN10 frame leaves untagged, SW1 assumes VLAN30, the destination is in VLAN10 → **frame not forwarded**. Switches still forward traffic with a mismatch, but problems may occur.
- Security best practice: change the native VLAN to an **unused VLAN** (e.g. 1001), and make it match between switches.

### 5. Trunk configuration

- `switchport mode trunk` can be **rejected**: "Command rejected: An interface whose trunk encapsulation is "Auto" can not be configured to "trunk" mode." On switches supporting both ISL **and** dot1q, the encapsulation is "Auto" by default: first use `switchport trunk encapsulation dot1q` (options: dot1q, isl, negotiate = auto). On dot1q-only switches, `switchport mode trunk` is enough.
- `show interfaces trunk`: **Mode "on"** = manually configured trunk; Encapsulation 802.1q; Status trunking; **Native vlan 1**; "Vlans allowed on trunk": **by default all, 1-4094**; "Vlans allowed and active in management domain": the allowed VLANs **that exist on the switch** (1, 10, 30; 1002-1005 do not appear); "Vlans in spanning tree forwarding state and not pruned" (later).
- Limiting allowed VLANs (security, and performance: broadcasts in other VLANs are not sent over the trunk):
  - `switchport trunk allowed vlan 10,30`: exact list.
  - `... add 20`: adds to the list. VLAN20 not created on the switch → appears in "allowed" but **not** in "allowed and active".
  - `... remove 20`: removes. `... all`: all (= default). `... except 1-5,10`: all except those (6-9 and 11-4094). `... none`: no VLANs, no traffic passes.
- `switchport trunk native vlan 1001`: changes the native VLAN.
- **`show vlan brief` does not list trunk ports** (G0/0 appears neither in VLAN10 nor VLAN30): it shows access ports. Use `show interfaces trunk` for trunks.
- SW2: G0/0 (to SW1) allows 10,30; G0/1 (to R1) allows 10,20,30.

### 6. Router on a stick (ROAS)

- A **single physical interface** between router and switch (it looks like a "stick" on the diagram), divided into **subinterfaces**: G0/0.10 for VLAN10, G0/0.20 for VLAN20, G0/0.30 for VLAN30. Switch side: **a regular trunk** allowing VLANs 10, 20 and 30, nothing more.
- Router: `no shutdown` on the physical interface (router interfaces are disabled by default); `interface g0/0.10`; `encapsulation dot1q 10`; `ip address` (last usable address of the subnet). The subinterface number **does not have to** match the VLAN number, but it is **highly recommended**.
- `encapsulation dot1q 10`: the router treats any frame **tagged VLAN10** as if it arrived on G0/0.10, and **tags with VLAN10** all frames leaving that subinterface.
- `show ip interface brief`: subinterfaces appear, the physical interface has no IP address. Routing table: connected and local routes, just like physical interfaces. A packet for 192.168.1.64/26 leaves G0/0 tagged VLAN20.
- Path VLAN10 PC → VLAN30 PC: SW2 sends to R1 tagged VLAN10; R1 receives it "on G0/0.10", routes to 192.168.1.128/26 (G0/0.30), sends it back tagged VLAN30; SW2 → SW1 tagged VLAN30; SW1 → destination.

### 7. Exam traps

- dot1q tag: **4 bytes, between Source MAC and Type**, TPID **0x8100**, VID **12 bits**, VLANs **1-4094**.
- Native VLAN: **untagged**, default **1**, **must match** on both ends.
- `switchport trunk allowed vlan 10` **replaces** the list; `add` appends.
- An allowed VLAN that **does not exist** on the switch is not "active": the trunk does not carry it until you run `vlan N`.
- `show vlan brief` does not show trunks.
- `encapsulation dot1q` is a **router subinterface** command, not a switch command.

### 8. IOS commands

```
Switch(config-if)# switchport trunk encapsulation dot1q    ! required before "mode trunk" on ISL+dot1q switches
Switch(config-if)# switchport mode trunk                   ! manually configure a trunk
Switch(config-if)# switchport trunk allowed vlan 10,30     ! exact list of allowed VLANs
Switch(config-if)# switchport trunk allowed vlan add 20    ! add to the list
Switch(config-if)# switchport trunk allowed vlan remove 20 ! remove from the list
Switch(config-if)# switchport trunk allowed vlan all       ! all (default state)
Switch(config-if)# switchport trunk allowed vlan except 1-5,10   ! all except these
Switch(config-if)# switchport trunk allowed vlan none      ! none
Switch(config-if)# switchport trunk native vlan 1001       ! native VLAN (unused VLAN recommended)
Switch# show interfaces trunk                              ! trunks, mode, encapsulation, native, allowed/active VLANs
Switch(config)# vlan 30                                    ! create a missing VLAN so it becomes "active"
Router(config)# interface g0/0
Router(config-if)# no shutdown                             ! enable the physical interface
Router(config)# interface g0/0.10                          ! subinterface (number = VLAN recommended)
Router(config-subif)# encapsulation dot1q 10               ! frames tagged VLAN10 <-> this subinterface
Router(config-subif)# ip address 10.0.0.62 255.255.255.192 ! VLAN10 gateway
Router# show ip interface brief                            ! subinterfaces and their addresses
Router# show ip route                                      ! connected/local routes of the subinterfaces
```

### 9. The lab (video 32)

**Objective**: same topology as the lecture (addresses in three /26 of 10.0.0.0): access ports, SW1–SW2 trunk, ROAS between SW2 and R1.

1. **Access ports**: SW1 `interface range f0/1-2` → VLAN10, `f0/3-4` → VLAN30; SW2 `f0/1` → VLAN20, `interface range f0/2-3` → VLAN10. The switch creates the VLANs.
2. **SW1–SW2 trunk (G0/1)**: `switchport trunk ?` offers no "encapsulation" option: this switch model only supports dot1q (not a Packet Tracer limitation). `switchport mode trunk`, `switchport trunk allowed vlan 10,30` (no VLAN20: no VLAN20 hosts on SW1; PC5 in VLAN20 goes through R1), `switchport trunk native vlan 1001`. `do show vlan brief`: VLANs 10 and 30 exist on SW1. Same configuration on SW2 G0/1. **On SW2, `do show interfaces trunk` shows only VLAN10 as "allowed and active"**: VLAN30 does not exist on SW2 (only 10 and 20 were created by the access ports) → `vlan 30`, `exit`, check again.
3. **ROAS**: SW2 `interface g0/2`, `switchport mode trunk`, `switchport trunk allowed vlan 10,20,30`, `switchport trunk native vlan 1001`. R1: `interface g0/0`, `no shutdown`; `interface g0/0.10`, `encapsulation dot1q 10`, `ip address 10.0.0.62 255.255.255.192`; `g0/0.20` → 10.0.0.126; `g0/0.30` → 10.0.0.190. Why the last usable address? Not required, but **use a consistent system** (first or last) across the network.
4. **Tests** from PC7 (VLAN10): `ping 10.0.0.1` (PC1, same VLAN: frame sent directly, no routing); `ping 10.0.0.65` (PC5, VLAN20: goes to R1 then back to SW2); `ping 10.0.0.129` (PC3, VLAN30: R1, then SW2, SW1). Watch them in simulation mode.

**Boson NetSim preview "Inter-VLAN Routing 1"** (task 1 only): `ipconfig /all` on the PCs (check IP /25, mask, gateway); `hostname Switch1`; `vlan 10` and `vlan 12`; find each PC's port from its "Physical Address" (MAC) and `show mac-address-table` (with hyphen on this switch; `show mac address-table` on newer ones): PC1 on F0/3 → VLAN10, PC2 on F0/4 → VLAN12; the ping PC1 → PC2 fails because **no inter-VLAN routing is configured** (F0/1 is not a trunk per `show interfaces trunk`, no subinterfaces on R1 per `show ip interface brief`).

### 10. Day 17 quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Send VLAN10 frames **untagged** over SW1's G0/1 trunk: A) encapsulation dot1q 10, B) switchport trunk allowed vlan 10, C) ... add 10, D) switchport trunk native vlan 10 | **D** | Native VLAN traffic is sent untagged. A is a router subinterface command; B and C modify the allowed VLANs. |
| Return the allowed VLANs to the default state: A) ... default, B) ... all, C) ... none, D) ... 1,1001-1005 | **B** | By default all VLANs are allowed. D lists the VLANs that exist by default on a switch, which is different. |
| `switchport mode trunk` rejected, which command might fix it? A) switch port mode trunk, B) ... encapsulation 802.1q, C) switchport trunk encapsulation dot1q, D) ... encapsulation auto | **C** | On switches supporting ISL and dot1q you must set the encapsulation first (ISL possible but almost never used). |
| Which 802.1Q tag field identifies the VLAN ID? A) TPID, B) VID, C) TCI, D) VLN | **B** | VID = VLAN ID, 12 bits. TPID = 0x8100 identifies the frame as tagged; PCP is for CoS; VLN is not a real field. |
| `switchport trunk allowed vlan add 10` done, but VLAN10 missing from "allowed and active in management domain": A) VLAN10 doesn't exist on the switch, B) invalid command, C) should be "allowed vlan 10", D) VLAN10 is reserved | **A** | A VLAN that is allowed but does not exist on the switch does not appear in that section. |
