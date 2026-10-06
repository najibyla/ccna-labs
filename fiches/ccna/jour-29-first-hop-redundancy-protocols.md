# CCNA Day 29 : First Hop Redundancy Protocols / Protocoles de redondance du premier saut

> Source : Jeremy's IT Lab, vidéo n°59 « First Hop Redundancy Protocols | Day 29 » (cours, 40 min) et vidéo n°60 « Configuring HSRP | Day 29 Lab » (lab, 22 min) de la playlist. Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Pourquoi un FHRP ?

- Sujet d'examen 3.5 : « décrire le rôle des protocoles de redondance du premier saut ». **Aucune configuration n'est exigée à l'examen**, mais Jeremy montre une configuration de base de HSRP pour le lab.
- Problème : les PC ont un **default gateway** fixe (R1, 172.16.0.254). Si R1 tombe, R2 est disponible mais **les PC ne le savent pas** et continuent d'envoyer le trafic à R1.
- Définition (Wikipedia, citée par Jeremy) : un FHRP est conçu pour **protéger le default gateway d'un sous-réseau** en permettant à deux routeurs ou plus d'assurer la relève pour cette adresse ; en cas de panne du routeur actif, le routeur de secours reprend l'adresse, en général en quelques secondes.
- « Premier saut » (*first hop*) : le default gateway est le premier routeur sur le chemin vers la destination.

### 2. Fonctionnement commun à tous les FHRP

1. Les deux routeurs partagent une **VIP** (*virtual IP*, ex. 172.16.0.252) et une **MAC virtuelle** (*virtual MAC*), générée pour la VIP. Chaque FHRP a son propre format de MAC virtuelle.
2. Ils négocient leurs rôles avec des messages **Hello multicast** : un routeur **actif** (*active*, fait office de default gateway) et un routeur **de secours** (*standby*). Les termes varient selon le protocole.
3. Les hôtes sont configurés avec la **VIP comme default gateway**.
4. PC1 envoie une **requête ARP** (broadcast) pour 172.16.0.252 ; les deux routeurs la reçoivent, mais **seul le routeur actif répond** (réponse ARP unicast) avec la **MAC virtuelle**.
5. Trame vers 8.8.8.8 : IP source PC1, IP destination 8.8.8.8, MAC source PC1, **MAC destination = MAC virtuelle**. La trame va vers R1.
6. Si R1 tombe : après quelques secondes sans Hello, R2 devient actif. **Les PC n'ont rien à changer** dans leur table ARP (VIP → MAC virtuelle). Ce sont les **switches** qui doivent mettre à jour leur table d'adresses MAC : R2 envoie des **gratuitous ARP** (réponses ARP envoyées sans requête, **en broadcast** vers FFFF.FFFF.FFFF, alors qu'une réponse ARP normale est unicast). Les switches apprennent la MAC virtuelle sur le port vers R2.
7. Si R1 revient : il devient **standby**. Les FHRP sont **non préemptifs** par défaut, comme le DR/BDR d'OSPF. On peut activer la **préemption** (*preemption*) pour que R1 reprenne le rôle actif.

### 3. Les trois FHRP

| | HSRP (*Hot Standby Router Protocol*) | VRRP (*Virtual Router Redundancy Protocol*) | GLBP (*Gateway Load Balancing Protocol*) |
| :--- | :--- | :--- | :--- |
| Propriété | **Propriétaire Cisco** | **Standard ouvert** | **Propriétaire Cisco** |
| Rôles | **Active / Standby** | **Master / Backup** | **AVG** (*Active Virtual Gateway*) + jusqu'à **4 AVF** (*Active Virtual Forwarders*) |
| Multicast IPv4 | **224.0.0.2** (v1), **224.0.0.102** (v2) | **224.0.0.18** | **224.0.0.102** (même que HSRPv2) |
| MAC virtuelle | v1 : **0000.0c07.acXX** (XX = groupe) ; v2 : **0000.0c9f.fXXX** | **0000.5e00.01XX** | **0007.b400.XXYY** (XX = groupe, YY = n° AVF) |
| Répartition de charge | Entre sous-réseaux seulement | Entre sous-réseaux seulement | **Dans un même sous-réseau** |

- **HSRP** : version 2 ajoute le support IPv6 et augmente le nombre de groupes (3 chiffres hexa pour le groupe dans la MAC au lieu de 2). Groupe 1 : v1 → 0000.0c07.ac01 ; v2 → 0000.0c9f.f001. Une VIP par sous-réseau, chacune dans un **groupe HSRP** distinct. Pour répartir la charge, on configure un routeur actif différent dans chaque sous-réseau/VLAN (R1 actif en VLAN1, R2 actif en VLAN2, chacun standby dans l'autre), comme le root bridge différent par VLAN en spanning tree.
- **VRRP** : fonctionnellement presque identique à HSRP. Groupe 200 → 0000.5e00.01**c8** (200 en hexadécimal = c8).
- **GLBP** : un seul AVG élu par sous-réseau ; l'AVG assigne jusqu'à quatre AVF (l'AVG peut lui-même être AVF). Chaque AVF sert de default gateway à une partie des hôtes du sous-réseau. AVF 1 du groupe 1 → 0007.b400.0101.
- Remarque de Jeremy : chaque VLAN correspond à un sous-réseau. Les sous-réseaux divisent le réseau en couche 3, les VLAN en couche 2.

### 4. Élection HSRP et préemption

- L'actif est le routeur avec la **priorité la plus haute** (défaut **100**, plage 0 à 255) ; à égalité, celui avec l'**adresse IP la plus haute**.
- `standby <groupe> preempt` : le routeur reprend le rôle actif s'il a la priorité (ou l'IP) la plus haute. **À configurer seulement sur le routeur qu'on veut actif.**
- Groupes : **0 à 255** en version 1, **0 à 4095** en version 2. Le **numéro de groupe doit être identique** sur les deux routeurs. Jeremy aime faire correspondre le numéro de groupe au numéro de VLAN (pas une règle).
- **Les versions 1 et 2 ne sont pas compatibles.**

### 5. Pièges d'examen

- **Mémoriser le tableau** : terminologie, adresses multicast et formats de MAC virtuelle de chaque FHRP (Jeremy insiste : « definitely remember the IP and MAC addresses »).
- HSRP et VRRP ne répartissent pas la charge **dans un même sous-réseau** ; seul GLBP le fait.
- Lors du basculement, le nouveau routeur actif envoie des **gratuitous ARP** (meilleure réponse qu'« ARP reply » ou « HSRP hello », qui ne sont pas totalement fausses mais moins précises). Choisir **la meilleure réponse**.
- Les FHRP sont **non préemptifs** par défaut.
- Un seul groupe HSRP = une seule VIP et **une seule MAC virtuelle** (question bonus Boson).

### 6. Commandes IOS

```
R1(config)# interface g0/0            ! HSRP se configure sur l'interface côté LAN servi
R1(config-if)# standby version 2      ! HSRP version 2 (s'applique à tous les groupes)
R1(config-if)# standby 1 ip 172.16.0.254   ! VIP du groupe 1 (sans numéro de groupe : groupe 0)
R1(config-if)# standby 1 priority 200      ! priorité (défaut 100, plage 0-255)
R1(config-if)# standby 1 preempt           ! reprend le rôle actif au retour
R1# show standby                            ! groupe, version, état, VIP, MAC virtuelle, timers, préemption, actif/standby, priorité
```

### 7. Le lab (vidéo n°60)

Objectif : fournir un default gateway redondant 10.0.1.254 pour PC1 et PC2 avec HSRP v2, R1 actif (10.0.1.253), R2 standby (10.0.1.252).

1. **Avant** : `ping 8.8.8.8` et `ipconfig` sur les PC (gateway = 10.0.1.253, R1). `tracert 8.8.8.8` sur PC2 : premier saut 10.0.1.253 (8.8.8.8 est un loopback de R3). Sur un PC la commande est `tracert`, sur IOS `traceroute`.
2. **R1** : `interface g0/0`, `standby version 2`, `standby 1 ip 10.0.1.254`, `standby 1 priority 200`, `standby 1 preempt`.
3. **R2** : laissé volontairement en version 1 avec `standby 1 priority 50` et `standby 1 ip 10.0.1.254`. Après 30 s : messages de **duplicate address**, les deux routeurs se croient actifs à cause du **version mismatch**. Correction : `standby version 2`. `do show standby` : état standby, routeur actif 10.0.1.253.
4. **PC** : default gateway = 10.0.1.254 (onglet Config). `ping 8.8.8.8` fonctionne. `arp -a` montre 10.0.1.254 → **0000.0C9F.F001** (MAC virtuelle HSRPv2, groupe 1). `tracert` : premier saut **10.0.1.253**, l'IP de l'interface de R1, pas la VIP. Traceroute permet donc de vérifier quel routeur sert de gateway.
5. **Panne de R1** : `end`, `write` (sinon la config est perdue au redémarrage), onglet Physical, bouton d'alimentation. Après 30 s, ping OK depuis PC1 ; `tracert` montre **10.0.1.252** (R2).
6. **Retour de R1** : grâce à la préemption, `tracert` montre de nouveau 10.0.1.253.

Bonus NetSim (CCNP ENCOR) : HSRP sur des **switches de couche 3** (`interface vlan 1`, `standby 3 ip 172.16.3.1`) ; sur un switch de couche 2, le gateway se configure avec `ip default-gateway 172.16.3.1` (pas de table de routage).

### 8. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Laquelle est une MAC virtuelle HSRP version 1 ? | **0000.0c07.acab** (groupe AB = 171) | Les options A et C sont des MAC HSRP v2 ; B ne suit aucun format FHRP. |
| Laquelle est une MAC virtuelle VRRP ? | **0000.5e00.010a** (groupe 0a = 10) | B est une MAC GLBP, C une MAC HSRP v2, D ne suit aucun format. |
| Rôles valides en VRRP (deux réponses) ? | **Backup** et **Master** | Active et standby sont des rôles HSRP ; AVG et AVF sont des rôles GLBP. |
| Quand le standby HSRP devient actif, quels messages envoie-t-il ? | **Gratuitous ARP** | Les Hello HSRP sont envoyés en permanence ; « ARP reply » n'est pas faux mais moins précis. Choisir la meilleure réponse. |
| Quelle affirmation décrit HSRP ? | **Il fournit un default gateway redondant pour les hôtes d'un sous-réseau** | Il ne répartit pas la charge dans un sous-réseau (GLBP le fait) ; les routeurs partagent une VIP et une MAC, ils n'en choisissent pas d'uniques. |

---

## 🇬🇧 English version

### 1. Why an FHRP?

- Exam topic 3.5: "describe the purpose of first hop redundancy protocol". **No configuration is required for the exam**, but Jeremy shows basic HSRP configuration for the lab.
- Problem: PCs have a fixed **default gateway** (R1, 172.16.0.254). If R1 fails, R2 is available but **the PCs do not know it** and keep sending traffic to R1.
- Definition (Wikipedia, quoted by Jeremy): an FHRP is designed to **protect the default gateway used on a subnetwork** by allowing two or more routers to provide backup for that address; if the active router fails, the backup router takes over the address, usually within a few seconds.
- "First hop": the default gateway is the first router in the path to the destination.

### 2. How every FHRP works

1. The two routers share a **VIP** (virtual IP, e.g. 172.16.0.252) and a **virtual MAC** generated for the VIP. Each FHRP uses its own virtual MAC format.
2. They negotiate roles with **multicast Hello** messages: one **active** router (acts as the default gateway) and one **standby** router. Terms vary by protocol.
3. End hosts are configured with the **VIP as their default gateway**.
4. PC1 sends an **ARP request** (broadcast) for 172.16.0.252; both routers receive it, but **only the active router replies** (unicast ARP reply) with the **virtual MAC**.
5. Frame to 8.8.8.8: source IP PC1, destination IP 8.8.8.8, source MAC PC1, **destination MAC = virtual MAC**. The frame goes to R1.
6. If R1 fails: after a few seconds without Hellos, R2 becomes active. **The PCs do not change** their ARP tables (VIP → virtual MAC). The **switches** must update their MAC address tables: R2 sends **gratuitous ARP** messages (ARP replies sent without a request, **broadcast** to all Fs, whereas normal ARP replies are unicast). The switches learn the virtual MAC on the port toward R2.
7. If R1 comes back: it becomes **standby**. FHRPs are **non-preemptive** by default, like OSPF's DR/BDR. **Preemption** can be configured so that R1 takes back the active role.

### 3. The three FHRPs

| | HSRP (Hot Standby Router Protocol) | VRRP (Virtual Router Redundancy Protocol) | GLBP (Gateway Load Balancing Protocol) |
| :--- | :--- | :--- | :--- |
| Ownership | **Cisco proprietary** | **Open standard** | **Cisco proprietary** |
| Roles | **Active / Standby** | **Master / Backup** | **AVG** (Active Virtual Gateway) + up to **4 AVFs** (Active Virtual Forwarders) |
| IPv4 multicast | **224.0.0.2** (v1), **224.0.0.102** (v2) | **224.0.0.18** | **224.0.0.102** (same as HSRPv2) |
| Virtual MAC | v1: **0000.0c07.acXX** (XX = group); v2: **0000.0c9f.fXXX** | **0000.5e00.01XX** | **0007.b400.XXYY** (XX = group, YY = AVF number) |
| Load balancing | Between subnets only | Between subnets only | **Within a single subnet** |

- **HSRP**: version 2 adds IPv6 support and increases the number of groups (3 hex digits for the group in the MAC instead of 2). Group 1: v1 → 0000.0c07.ac01; v2 → 0000.0c9f.f001. One VIP per subnet, each in a separate **HSRP group**. To load balance, configure a different active router in each subnet/VLAN (R1 active in VLAN1, R2 active in VLAN2, each standby in the other), like a different root bridge per VLAN in spanning tree.
- **VRRP**: functionally nearly identical to HSRP. Group 200 → 0000.5e00.01**c8** (200 in hexadecimal = c8).
- **GLBP**: a single AVG is elected per subnet; the AVG assigns up to four AVFs (the AVG can be an AVF too). Each AVF acts as the default gateway for a portion of the hosts in the subnet. AVF 1 in group 1 → 0007.b400.0101.
- Jeremy's side note: each VLAN maps to a subnet. Subnets divide the network at Layer 3, VLANs at Layer 2.

### 4. HSRP election and preemption

- The active router is the one with the **highest priority** (default **100**, range 0 to 255); if tied, the **highest IP address**.
- `standby <group> preempt`: the router takes the active role if it has the higher priority (or IP). **Only needed on the router you want to be active.**
- Groups: **0 to 255** in version 1, **0 to 4095** in version 2. The **group number must match** on both routers. Jeremy likes matching the group number to the VLAN number (not a rule).
- **Versions 1 and 2 are not compatible.**

### 5. Exam traps

- **Memorize the chart**: terminology, multicast addresses and virtual MAC formats of each FHRP (Jeremy: "definitely remember the IP and MAC addresses").
- HSRP and VRRP do not load balance **within a single subnet**; only GLBP does.
- On failover, the new active router sends **gratuitous ARP** (better answer than "ARP reply" or "HSRP hello", which are not totally wrong but less specific). Pick **the best answer**.
- FHRPs are **non-preemptive** by default.
- One HSRP group = one VIP and **one virtual MAC** (Boson bonus question).

### 6. IOS commands

```
R1(config)# interface g0/0            ! HSRP is configured on the interface facing the served LAN
R1(config-if)# standby version 2      ! HSRP version 2 (applies to all groups)
R1(config-if)# standby 1 ip 172.16.0.254   ! VIP for group 1 (without a group number: group 0)
R1(config-if)# standby 1 priority 200      ! priority (default 100, range 0-255)
R1(config-if)# standby 1 preempt           ! take back the active role on recovery
R1# show standby                            ! group, version, state, VIP, virtual MAC, timers, preemption, active/standby, priority
```

### 7. The lab (video 60)

Goal: provide a redundant default gateway 10.0.1.254 for PC1 and PC2 with HSRP v2, R1 active (10.0.1.253), R2 standby (10.0.1.252).

1. **Before**: `ping 8.8.8.8` and `ipconfig` on the PCs (gateway = 10.0.1.253, R1). `tracert 8.8.8.8` on PC2: first hop 10.0.1.253 (8.8.8.8 is a loopback on R3). On a PC the command is `tracert`, in IOS `traceroute`.
2. **R1**: `interface g0/0`, `standby version 2`, `standby 1 ip 10.0.1.254`, `standby 1 priority 200`, `standby 1 preempt`.
3. **R2**: deliberately left on version 1 with `standby 1 priority 50` and `standby 1 ip 10.0.1.254`. After 30 s: **duplicate address** messages, both routers think they are active because of the **version mismatch**. Fix: `standby version 2`. `do show standby`: state standby, active router 10.0.1.253.
4. **PCs**: default gateway = 10.0.1.254 (Config tab). `ping 8.8.8.8` works. `arp -a` shows 10.0.1.254 → **0000.0C9F.F001** (HSRPv2 virtual MAC, group 1). `tracert`: first hop **10.0.1.253**, R1's interface IP, not the VIP. Traceroute is therefore a useful tool to check which router is acting as gateway.
5. **R1 failure**: `end`, `write` (otherwise the config is lost on restart), Physical tab, power switch. After 30 s, ping OK from PC1; `tracert` shows **10.0.1.252** (R2).
6. **R1 recovery**: thanks to preemption, `tracert` shows 10.0.1.253 again.

NetSim bonus (CCNP ENCOR): HSRP on **Layer 3 switches** (`interface vlan 1`, `standby 3 ip 172.16.3.1`); on a Layer 2 switch, the gateway is set with `ip default-gateway 172.16.3.1` (no routing table).

### 8. The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which is an HSRP version 1 virtual MAC address? | **0000.0c07.acab** (group AB = 171) | Options A and C are HSRP v2 MACs; B follows no FHRP format. |
| Which is a VRRP virtual MAC address? | **0000.5e00.010a** (group 0a = 10) | B is a GLBP MAC, C an HSRP v2 MAC, D follows no format. |
| Valid VRRP router roles (select two)? | **Backup** and **Master** | Active and standby are HSRP roles; AVG and AVF are GLBP roles. |
| When the HSRP standby becomes the new active router, what messages does it send? | **Gratuitous ARP** | HSRP Hellos are always sent; "ARP reply" is not wrong but less specific. Select the best answer. |
| Which statement accurately describes HSRP? | **It provides a redundant default gateway address for hosts in a subnet** | It does not load balance within a subnet (GLBP does); routers share one VIP and MAC, they do not select unique ones. |
