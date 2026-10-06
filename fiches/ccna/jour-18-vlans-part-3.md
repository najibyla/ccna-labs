# CCNA Day 18 : VLANs (Part 3) / VLAN, partie 3 : VLAN natif sur routeur, Wireshark, switch multicouche

> Source : Jeremy's IT Lab, « Free CCNA | VLANs (Part 3) | Day 18 » (33 min, vidéo n°33 de la playlist, cours) et « VLANs (Part 3) | Day 18 Lab » (25 min, vidéo n°34, lab Packet Tracer suivi d'un aperçu Boson NetSim). Flashcards disponibles. DTP et VTP, prévus pour cette vidéo, sont reportés au Day 19. Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Le VLAN natif sur un routeur (router on a stick)

- Bonne pratique rappelée : mettre le VLAN natif sur un **VLAN inutilisé** (raisons de sécurité, vues plus tard). Avantage du VLAN natif si on l'utilise quand même : les trames **non étiquetées sont plus petites**, l'équipement envoie plus de trames par seconde.
- Démonstration : le VLAN natif est remis à **VLAN10** sur SW1 G0/0, SW2 G0/0 et SW2 G0/1 (il était à 1001 au Day 17). Deux méthodes côté routeur :
  1. Sur la sous-interface : `encapsulation dot1q 10 native`. Le routeur suppose que les trames non étiquetées appartiennent à ce VLAN et n'étiquette pas les trames qu'il y envoie, comme un switch.
  2. **Pas de sous-interface** : configurer l'adresse IP du VLAN natif **directement sur l'interface physique** (`no interface g0/0.10`, puis `interface g0/0`, `ip address ...`). La commande `encapsulation dot1q` est inutile dans ce cas. Dans `show running-config`, l'interface physique porte l'adresse du VLAN10, les autres sous-interfaces restent avec `encapsulation dot1q` et leur adresse.
- Les deux méthodes fonctionnent pareil : SW2 envoie les trames VLAN10 non étiquetées à R1, et R1 fait de même. « Vous pourriez en avoir besoin à l'examen. »

### 2. Captures Wireshark de l'étiquette dot1q

Ping d'un PC VLAN20 (192.168.1.65) vers un PC VLAN10 (192.168.1.1), capture sur le lien R1–SW2 (dans les deux sens).

- **Requête ICMP de SW2 vers R1 (VLAN20, pas natif)** : dans l'en-tête Ethernet, « Type: 802.1Q Virtual LAN » avec la valeur hexadécimale **8100** = champ **TPID** ; puis **PCP = 0** (aucune priorité), **DEI = 0** (ne sera pas abandonnée en cas de congestion), **VLAN ID = 20** ; puis le champ Type normal (IPv4), repoussé après l'étiquette.
- **Même requête de R1 vers SW2 (VLAN10 = natif)** : nouvel en-tête Ethernet **sans étiquette dot1q**. La trame reste non étiquetée jusqu'à la destination car VLAN10 est natif sur tous les équipements. La réponse ICMP revient non étiquetée jusqu'à R1, qui l'étiquette VLAN20.

### 3. Le switch de couche 3 (*Layer 3 switch*, *multilayer switch*)

- Icône différente du switch de couche 2 (icônes officielles Cisco mentionnées). Les deux noms sont à connaître.
- Capable de **commuter ET router** : il est « conscient » de la couche 3, contrairement à un switch de couche 2 qui ne regarde que les MAC.
- On peut : assigner des adresses IP à ses interfaces comme un routeur (**ports routés**, *routed ports*) ; créer des **interfaces virtuelles par VLAN** avec adresse IP ; configurer des **routes** (statiques…) ; faire du **routage inter-VLAN**.
- Les trois méthodes de routage inter-VLAN : 1) une liaison routeur–switch par VLAN (Day 16 ; pas assez d'interfaces si beaucoup de VLAN) ; 2) router on a stick (Day 17 ; une seule interface, mais tout le trafic fait l'aller-retour vers le routeur, risque de congestion) ; 3) **switch multicouche, méthode préférée dans les grands réseaux**.

### 4. Les SVI (*Switch Virtual Interfaces*)

- SVI = interface virtuelle à laquelle on assigne une adresse IP sur un switch multicouche. **Les PC utilisent la SVI (et non le routeur) comme passerelle.** Dans l'exemple, SW2 reçoit les mêmes adresses que R1 avait en ROAS (dernière utilisable de chaque sous-réseau), donc **rien à changer sur les PC**.
- Trajet PC VLAN20 → PC VLAN10 : la trame arrive à SW2, qui a désormais sa **propre table de routage**, voit que 192.168.1.0/26 est connecté à sa SVI VLAN10, route la trame, puis la transmet (ou l'inonde dans VLAN10 si la MAC est inconnue) vers SW1 par le trunk, étiquetée VLAN10. **Plus besoin d'envoyer à R1.**
- Vers l'extérieur du LAN (Internet derrière R1) : le lien SW2–R1 devient une **liaison point à point de couche 3** 192.168.1.192/30 (SW2 G0/1 = .193, R1 G0/0 = .194), plus de VLAN dessus, et SW2 a une **route par défaut** vers R1.

### 5. Configuration

**R1** : `no interface g0/0.10` (idem .20, .30) supprime les sous-interfaces ; `default interface g0/0` remet l'interface à ses réglages par défaut ; `show ip interface brief` montre encore les sous-interfaces avec le statut **« deleted »** jusqu'au redémarrage (sans conséquence) ; `interface g0/0`, `ip address 192.168.1.194 255.255.255.252`.

**SW2, port routé** : `default interface g0/1` (il était trunk) ; **`ip routing`, commande à ne jamais oublier** : active le routage de couche 3 et la table de routage, sans elle le routage inter-VLAN ne marche pas ; `interface g0/1`, **`no switchport`** : passe l'interface de port de couche 2 à **port routé** de couche 3, ce qui permet `ip address 192.168.1.193 255.255.255.252` ; `ip route 0.0.0.0 0.0.0.0 192.168.1.194` ; `show ip route` (route par défaut + connected/local) ; `show interfaces status` : colonne VLAN = **« routed »** pour G0/1.

**SW2, SVI** : `interface vlan10`, `ip address ...`, **`no shutdown` (les SVI sont shutdown par défaut)** ; idem VLAN20, VLAN30. `show ip route` : routes connected/local « directly connected, Vlan10 », etc.

**Conditions pour qu'une SVI soit up/up** (démonstration : SVI VLAN40 avec 40.40.40.40/24 et `no shutdown` reste **down/down**) :

1. **Le VLAN doit exister** sur le switch. Créer une SVI **ne crée pas** le VLAN (contrairement à l'affectation d'un port d'accès).
2. Le switch doit avoir **au moins un port d'accès dans ce VLAN en up/up, et/ou un port trunk permettant ce VLAN en up/up** (ex. VLAN30 sans hôte sur SW2 est up grâce au trunk G0/0).
3. **Le VLAN lui-même ne doit pas être shutdown** (mode `vlan N` puis `shutdown` ; pas possible dans Packet Tracer, il faut un vrai switch).
4. La SVI ne doit pas être shutdown : `no shutdown` après création.

### 6. Pièges d'examen

- `ip routing` obligatoire sur le switch multicouche ; `no switchport` pour un port routé ; `ip routing` n'affecte **pas** un port individuel.
- SVI **shutdown par défaut** ; une SVI ne crée pas son VLAN.
- Les deux méthodes de VLAN natif sur routeur : `encapsulation dot1q N native` sur la sous-interface **ou** IP sur l'interface physique sans `encapsulation dot1q`.
- Le trafic du VLAN natif n'est **pas étiqueté** (question Boson : `switchport trunk native vlan 44` → VLAN 44 non étiqueté ; par défaut ce serait VLAN 1).

### 7. Commandes IOS

```
Router(config-subif)# encapsulation dot1q 10 native   ! méthode 1 : cette sous-interface est le VLAN natif
Router(config)# no interface g0/0.10                  ! supprime une sous-interface
Router(config)# default interface g0/0                ! remet l'interface à ses réglages par défaut
Router(config-if)# ip address 192.168.1.194 255.255.255.252   ! méthode 2 (sans sous-interface) ou lien L3 point à point
Router# show running-config                           ! voir l'interface physique et ses sous-interfaces
Switch(config)# ip routing                            ! active le routage de couche 3 sur le switch (indispensable)
Switch(config)# default interface g0/1                ! réinitialise l'interface (était trunk)
Switch(config-if)# no switchport                      ! port de couche 2 -> port routé de couche 3
Switch(config-if)# ip address 192.168.1.193 255.255.255.252   ! adresse du port routé
Switch(config)# ip route 0.0.0.0 0.0.0.0 192.168.1.194        ! route par défaut vers R1
Switch(config)# interface vlan10                      ! crée/configure la SVI du VLAN 10
Switch(config-if)# ip address 192.168.1.62 255.255.255.192    ! passerelle du VLAN
Switch(config-if)# no shutdown                        ! les SVI sont shutdown par défaut
Switch# show ip route                                 ! table de routage du switch
Switch# show interfaces status                        ! colonne VLAN : « routed » pour un port routé
Switch# show ip interface brief                       ! statut up/up ou down/down des SVI
Switch# show interfaces f0/3 switchport               ! mode administratif/opérationnel d'un port (aperçu NetSim)
```

### 8. Le lab (vidéo n°34)

**Objectif** : réseau du Day 17 avec SW2 remplacé par un switch multicouche ; remplacer le router on a stick par un lien L3 point à point et des SVI sur SW2.

1. **R1** : `show run` (Entrée = une ligne, Espace = un écran) montre G0/0 (seulement `no shutdown`) et ses 3 sous-interfaces ; `show ip interface brief` : tout up/up. `no interface g0/0.10`, `.20`, `.30` (flèche haut pour rappeler la commande). Dans Packet Tracer les sous-interfaces disparaissent immédiatement, alors que dans GNS3 (vrai IOS, utilisé pour les cours) elles restent « deleted » jusqu'au redémarrage. `interface g0/0`, `ip address 10.0.0.194 255.255.255.252`. `default interface` inutile ici, l'interface est déjà par défaut.
2. **SW2 G1/0/2** : `show run` montre que **ce switch L3 exige `switchport trunk encapsulation dot1q`** (le modèle du lab précédent non). `default interface g1/0/2` (dans Packet Tracer il a fallu la taper deux fois). `interface g1/0/2`, `ip ?` : **pas d'option « address »** car le port est encore en couche 2 → `no switchport`, puis `ip address 10.0.0.193 255.255.255.252`. `do show ip route` : **vide**, car `ip routing` n'est pas activé → `ip routing` ; seule la route connected apparaît (pas de route local : probable bug Packet Tracer). `ip route 0.0.0.0 0.0.0.0 10.0.0.194`.
3. **SVI** : `do show vlan brief` (VLAN 10, 20, 30 existent) ; `interface vlan 10`, `ip address 10.0.0.62 255.255.255.192` ; `vlan 20` → 10.0.0.126 ; `vlan 30` → 10.0.0.190 ; `do show ip interface brief` : les trois SVI up/up.
4. **Tests** : PC7 (VLAN10) `ping 10.0.0.129` (PC3, VLAN30) ; les premiers échouent le temps de l'ARP vers la passerelle. En simulation, le ping va à SW2 qui l'envoie **directement à SW1**, sans passer par R1. `ping 1.1.1.1` (Internet) fonctionne grâce à la route par défaut (routes déjà configurées sur R1 et le routeur Internet).

**Aperçu Boson NetSim « Inter-VLAN Routing 2 »** (dépannage, tâches 1 et 2) : PC3 ne pinge personne ; `ipconfig /all` → masque /24 au lieu de /25 → `ipconfig /ip 192.168.100.3 255.255.255.128` (commande propre aux PC NetSim) ; les pings échouent encore. Deux causes possibles sur un switch L2 : port dans le mauvais VLAN, trunk mal configuré (`switchport mode trunk` oublié ou VLAN non permis). PC1 (même VLAN) pinge les deux sous-interfaces de Router1, PC3 non → problème sur Switch2 ou le trunk. `show vlan brief` sur Switch2 : F0/3 en VLAN12 au lieu de VLAN10 ; `show interfaces f0/3 switchport` : « static access » ; `switchport access vlan 10` corrige. `show interfaces trunk` : F0/1 trunk, natif 1, VLAN 1, 10, 12 actifs, identique à Switch1. PC3 pinge désormais sa passerelle et PC1, mais pas PC2/PC4 ; PC2 ne pinge pas sa passerelle .129 : problème restant pour la tâche 3 (non traitée).

### 9. Le quiz du Day 18 (3 questions + 1 question Boson ExSim)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Deux options valides pour configurer le VLAN natif sur un routeur en ROAS (choisir deux ; options A à D montrées à l'écran). | **B et C** | B : `encapsulation dot1q N native` sur la sous-interface. C : adresse IP sur l'interface physique, sans `encapsulation dot1q`. |
| SVI VLAN225 créée, adresse et `no shutdown`, mais down/down. Deux causes possibles ? A) VLAN225 n'existe pas, B) pas de `switchport mode trunk` sur la SVI, C) pas de `switchport access vlan 225` sur la SVI, D) aucune interface en VLAN225 n'est up/up | **A et D** | Le VLAN doit exister et avoir un port d'accès up/up ou un trunk le permettant up/up. Les commandes switchport ne s'appliquent pas à une SVI. |
| Commande pour configurer une interface de switch en port routé ? A) no switchport, B) ip address + masque, C) ip routing, D) switchport mode route | **A** | `no switchport` fait le port routé et permet ensuite l'adresse IP. `ip routing` active le routage global, pas un port. |
| Boson ExSim : sur un Catalyst 2950, `switchport trunk encapsulation dot1q`, `switchport mode trunk`, `switchport trunk native vlan 44` sur F0/7. Vrai ? A) VLAN 1 non étiqueté, B) VLAN 44 non étiqueté, C) tout étiqueté, D) rien étiqueté | **B** | Le VLAN natif n'est pas étiqueté sur un trunk ; il a été changé de 1 (défaut, où A serait vrai) à 44. `show interfaces trunk` affiche natif et VLAN permis. |

---

## 🇬🇧 English version

### 1. The native VLAN on a router (router on a stick)

- Best practice reminder: set the native VLAN to an **unused VLAN** (security reasons, covered later). Benefit of the native VLAN if you do use it: **untagged frames are smaller**, so the device can send more frames per second.
- Demonstration: the native VLAN is set back to **VLAN10** on SW1 G0/0, SW2 G0/0 and SW2 G0/1 (it was 1001 in Day 17). Two methods on the router:
  1. On the subinterface: `encapsulation dot1q 10 native`. The router assumes untagged frames belong to that VLAN and does not tag frames it sends in it, just like a switch.
  2. **No subinterface**: configure the native VLAN's IP address **directly on the physical interface** (`no interface g0/0.10`, then `interface g0/0`, `ip address ...`). The `encapsulation dot1q` command is not necessary in this case. In `show running-config`, the physical interface carries the VLAN10 address, the other subinterfaces keep `encapsulation dot1q` and their own address.
- Both methods work the same: SW2 sends VLAN10 frames untagged to R1, and R1 does the same. "You might also need to know this for your exam."

### 2. Wireshark captures of the dot1q tag

Ping from a VLAN20 PC (192.168.1.65) to a VLAN10 PC (192.168.1.1), captured on the R1–SW2 link (both directions).

- **ICMP echo request from SW2 to R1 (VLAN20, not native)**: in the Ethernet header, "Type: 802.1Q Virtual LAN" with hex value **8100** = the **TPID** field; then **PCP = 0** (no special priority), **DEI = 0** (not dropped during congestion), **VLAN ID = 20**; then the normal Type field (IPv4), pushed after the tag.
- **Same echo request from R1 to SW2 (VLAN10 = native)**: new Ethernet header **without a dot1q tag**. The frame stays untagged all the way to the destination because VLAN10 is native on all devices. The ICMP echo reply comes back untagged until R1, which tags it VLAN20.

### 3. The Layer 3 switch (multilayer switch)

- Different icon from the Layer 2 switch (official Cisco icons mentioned). Know both names.
- Capable of both **switching AND routing**: it is Layer 3 aware, unlike a Layer 2 switch which only cares about MAC addresses.
- You can: assign IP addresses to its interfaces like a router (**routed ports**); create **virtual interfaces per VLAN** with IP addresses; configure **routes** (static...); perform **inter-VLAN routing**.
- The three inter-VLAN routing methods: 1) one router–switch link per VLAN (Day 16; not enough interfaces with many VLANs); 2) router on a stick (Day 17; one interface, but all traffic goes to the router and back, possible congestion); 3) **multilayer switch, the preferred method in large networks**.

### 4. SVIs (Switch Virtual Interfaces)

- SVI = virtual interface you assign an IP address to on a multilayer switch. **PCs use the SVI (NOT the router) as their gateway.** In the example, SW2 gets the same addresses R1 had with ROAS (last usable of each subnet), so **no change on the PCs**.
- Path VLAN20 PC → VLAN10 PC: the frame arrives at SW2, which now has its **own routing table**, sees that 192.168.1.0/26 is connected to its VLAN10 SVI, routes the frame, then forwards it (or floods it in VLAN10 if the MAC is unknown) to SW1 over the trunk, tagged VLAN10. **No need to send it to R1.**
- Outside the LAN (Internet behind R1): the SW2–R1 link becomes a **point-to-point Layer 3 link** 192.168.1.192/30 (SW2 G0/1 = .193, R1 G0/0 = .194), no more VLANs on it, and SW2 gets a **default route** to R1.

### 5. Configuration

**R1**: `no interface g0/0.10` (same for .20, .30) deletes the subinterfaces; `default interface g0/0` resets the interface to default settings; `show ip interface brief` still lists the subinterfaces with status **"deleted"** until the router reloads (no problem); `interface g0/0`, `ip address 192.168.1.194 255.255.255.252`.

**SW2, routed port**: `default interface g0/1` (it was a trunk); **`ip routing`, a command you must not forget**: enables Layer 3 routing and the routing table, without it inter-VLAN routing will not work; `interface g0/1`, **`no switchport`**: changes the interface from a Layer 2 switchport to a Layer 3 **routed port**, allowing `ip address 192.168.1.193 255.255.255.252`; `ip route 0.0.0.0 0.0.0.0 192.168.1.194`; `show ip route` (default route + connected/local); `show interfaces status`: VLAN column shows **"routed"** for G0/1.

**SW2, SVIs**: `interface vlan10`, `ip address ...`, **`no shutdown` (SVIs are shutdown by default)**; same for VLAN20, VLAN30. `show ip route`: connected/local routes "directly connected, Vlan10", etc.

**Conditions for an SVI to be up/up** (demonstration: SVI VLAN40 with 40.40.40.40/24 and `no shutdown` stays **down/down**):

1. **The VLAN must exist** on the switch. Creating an SVI **does not create** the VLAN (unlike assigning an access port).
2. The switch must have **at least one access port in the VLAN that is up/up, and/or one trunk port allowing the VLAN that is up/up** (e.g. VLAN30 with no hosts on SW2 is up thanks to trunk G0/0).
3. **The VLAN itself must not be shutdown** (`vlan N` mode then `shutdown`; not possible in Packet Tracer, needs a real switch).
4. The SVI must not be shutdown: `no shutdown` after creating it.

### 6. Exam traps

- `ip routing` is mandatory on the multilayer switch; `no switchport` makes a routed port; `ip routing` does **not** set an individual port.
- SVIs are **shutdown by default**; an SVI does not create its VLAN.
- The two native VLAN methods on a router: `encapsulation dot1q N native` on the subinterface **or** IP on the physical interface without `encapsulation dot1q`.
- Native VLAN traffic is **untagged** (Boson question: `switchport trunk native vlan 44` → VLAN 44 untagged; by default it would be VLAN 1).

### 7. IOS commands

```
Router(config-subif)# encapsulation dot1q 10 native   ! method 1: this subinterface is the native VLAN
Router(config)# no interface g0/0.10                  ! deletes a subinterface
Router(config)# default interface g0/0                ! resets the interface to default settings
Router(config-if)# ip address 192.168.1.194 255.255.255.252   ! method 2 (no subinterface) or L3 point-to-point link
Router# show running-config                           ! see the physical interface and its subinterfaces
Switch(config)# ip routing                            ! enables Layer 3 routing on the switch (essential)
Switch(config)# default interface g0/1                ! resets the interface (was a trunk)
Switch(config-if)# no switchport                      ! Layer 2 switchport -> Layer 3 routed port
Switch(config-if)# ip address 192.168.1.193 255.255.255.252   ! routed port address
Switch(config)# ip route 0.0.0.0 0.0.0.0 192.168.1.194        ! default route to R1
Switch(config)# interface vlan10                      ! creates/configures the VLAN 10 SVI
Switch(config-if)# ip address 192.168.1.62 255.255.255.192    ! VLAN gateway
Switch(config-if)# no shutdown                        ! SVIs are shutdown by default
Switch# show ip route                                 ! the switch's routing table
Switch# show interfaces status                        ! VLAN column: "routed" for a routed port
Switch# show ip interface brief                       ! up/up or down/down status of the SVIs
Switch# show interfaces f0/3 switchport               ! administrative/operational mode of a port (NetSim preview)
```

### 8. The lab (video 34)

**Objective**: Day 17 network with SW2 replaced by a multilayer switch; replace router on a stick with a point-to-point L3 link and SVIs on SW2.

1. **R1**: `show run` (Enter = one line, spacebar = one screen) shows G0/0 (only `no shutdown`) and its 3 subinterfaces; `show ip interface brief`: all up/up. `no interface g0/0.10`, `.20`, `.30` (up arrow to recall the command). In Packet Tracer the subinterfaces disappear immediately, whereas in GNS3 (real IOS, used for the lectures) they stay "deleted" until reload. `interface g0/0`, `ip address 10.0.0.194 255.255.255.252`. `default interface` is unnecessary here, the interface already has default settings.
2. **SW2 G1/0/2**: `show run` shows that **this L3 switch requires `switchport trunk encapsulation dot1q`** (the previous lab's model did not). `default interface g1/0/2` (in Packet Tracer it had to be issued twice). `interface g1/0/2`, `ip ?`: **no "address" option** because the port is still in Layer 2 mode → `no switchport`, then `ip address 10.0.0.193 255.255.255.252`. `do show ip route`: **empty**, because `ip routing` is not enabled → `ip routing`; only the connected route appears (no local route: probably a Packet Tracer issue). `ip route 0.0.0.0 0.0.0.0 10.0.0.194`.
3. **SVIs**: `do show vlan brief` (VLANs 10, 20, 30 exist); `interface vlan 10`, `ip address 10.0.0.62 255.255.255.192`; `vlan 20` → 10.0.0.126; `vlan 30` → 10.0.0.190; `do show ip interface brief`: the three SVIs are up/up.
4. **Tests**: PC7 (VLAN10) `ping 10.0.0.129` (PC3, VLAN30); the first pings fail while ARP resolves the gateway. In simulation mode the ping goes to SW2, which sends it **directly to SW1**, without going to R1. `ping 1.1.1.1` (Internet) works thanks to the default route (routes already configured on R1 and the Internet router).

**Boson NetSim preview "Inter-VLAN Routing 2"** (troubleshooting, tasks 1 and 2): PC3 cannot ping anyone; `ipconfig /all` → /24 mask instead of /25 → `ipconfig /ip 192.168.100.3 255.255.255.128` (NetSim PC command); pings still fail. Two possible causes on a L2 switch: port in the wrong VLAN, misconfigured trunk (`switchport mode trunk` missing or VLAN not allowed). PC1 (same VLAN) pings both Router1 subinterfaces, PC3 does not → problem on Switch2 or the trunk. `show vlan brief` on Switch2: F0/3 in VLAN12 instead of VLAN10; `show interfaces f0/3 switchport`: "static access"; `switchport access vlan 10` fixes it. `show interfaces trunk`: F0/1 trunk, native 1, VLANs 1, 10, 12 active, same as Switch1. PC3 now pings its gateway and PC1, but not PC2/PC4; PC2 cannot ping its gateway .129: remaining issue for task 3 (not covered).

### 9. Day 18 quiz (3 questions + 1 Boson ExSim question)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Two valid options to configure the native VLAN on a router in a ROAS configuration (select two; options A to D shown on screen). | **B and C** | B: `encapsulation dot1q N native` on the subinterface. C: IP address on the physical interface, without `encapsulation dot1q`. |
| SVI for VLAN225 created, IP assigned, `no shutdown`, but down/down. Two possible causes? A) VLAN225 doesn't exist, B) no `switchport mode trunk` on the SVI, C) no `switchport access vlan 225` on the SVI, D) no interfaces in VLAN225 are up/up | **A and D** | The VLAN must exist and have an up/up access port or an up/up trunk allowing it. Switchport commands do not apply to an SVI. |
| Command to configure a switch interface as a routed port? A) no switchport, B) ip address + mask, C) ip routing, D) switchport mode route | **A** | `no switchport` makes the routed port and then allows the IP address. `ip routing` enables routing globally, not on a port. |
| Boson ExSim: on a Catalyst 2950, `switchport trunk encapsulation dot1q`, `switchport mode trunk`, `switchport trunk native vlan 44` on F0/7. True? A) VLAN 1 untagged, B) VLAN 44 untagged, C) all tagged, D) all untagged | **B** | Native VLAN traffic is untagged on a trunk; it was changed from 1 (default, where A would be true) to 44. `show interfaces trunk` displays native and allowed VLANs. |
