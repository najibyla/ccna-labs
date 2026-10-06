# CCNA Day 39 : DHCP / Dynamic Host Configuration Protocol

> Source : Jeremy's IT Lab, « Free CCNA | DHCP | Day 39 » (37 min, vidéo n°79 de la playlist, cours) et « Free CCNA | DHCP | Day 39 Lab » (18 min, vidéo n°80, lab Packet Tracer). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Rôle de DHCP

- Sujets d'examen **4.3** (expliquer le rôle de DHCP et DNS) et **4.6** (configurer et vérifier **client DHCP et relais**). Aussi mentionné en section 5.0, sécurité (vu plus tard).
- DHCP permet aux hôtes d'apprendre **automatiquement et dynamiquement** leur configuration réseau : **adresse IP, masque de sous-réseau, passerelle par défaut, serveur DNS**, etc., sans configuration manuelle (exemple : connexion d'un téléphone au Wi-Fi).
- Utilisé typiquement pour les **équipements clients** (PC, téléphones). Routeurs, serveurs, etc. sont en général **configurés manuellement** : ils ont besoin d'une adresse fixe (une passerelle qui change d'adresse ne serait pas idéale).
- Petit réseau (domestique) : le **routeur** est le serveur DHCP. Grande entreprise : le serveur DHCP est en général un **serveur Windows ou Linux**.

### 2. Démonstration Windows

- Propriétés IPv4 de la connexion : « Obtain an IP address automatically » et « Obtain DNS server address automatically » = utilisation de DHCP.
- `ipconfig /all` : « DHCP Enabled: Yes » (« No » si adresse manuelle), adresse 192.168.0.167/24 marquée **« preferred »** : le PC avait déjà reçu cette adresse et l'a redemandée ; s'il n'était plus disponible, il en aurait reçu une autre.
- **Bail** (*lease*) : « Lease Obtained » et « Lease Expires ». Les serveurs DHCP **louent** les adresses ; le bail n'est en général **pas permanent**, le client doit rendre l'adresse à la fin, ou peut la **libérer** (*release*) avant. Un bail permanent est possible mais presque toujours déconseillé (café, aéroport : préserver les adresses disponibles ; le client redemandera une adresse si besoin).
- Passerelle, serveur DHCP et serveur DNS sont tous 192.168.0.1 (routeur domestique) : courant dans un réseau domestique.
- `ipconfig /release` : le PC envoie un **DHCP Release** au serveur, l'adresse redevient libre. Capture Wireshark : IPv4 de 192.168.0.167 vers 192.168.0.1, **UDP port source 68, destination 67**. **Les serveurs DHCP utilisent UDP 67, les clients UDP 68** (différent de DNS où seul le port du serveur est fixé, le client utilisant un port éphémère). **Option 53** = type de message DHCP. (Clin d'œil de Jeremy : le « magic cookie ».)
- `ipconfig /renew` : le PC contacte le serveur et retrouve sa configuration : processus en **quatre messages**.

### 3. Les quatre messages : DORA

| Message | Sens | Adressage |
| :--- | :--- | :--- |
| **Discover** | client → serveur | **Broadcast** : MAC destination FFFF.FFFF.FFFF, IP source **0.0.0.0** (pas encore d'adresse), destination **255.255.255.255**, UDP 68 → 67. Le client ne sait pas s'il y a un serveur ni où. Option « Requested IP Address » si le PC avait déjà une adresse. |
| **Offer** | serveur → client | **Unicast ou broadcast selon le client** (champ **Bootp flags** : 0000 = unicast). Propose une adresse plus passerelle, DNS, etc. UDP 67 → 68. Options : **51** = lease time, **6** = DNS server, **3** = router (passerelle). Certains clients n'acceptent pas l'unicast avant d'avoir configuré leur adresse, d'où le broadcast parfois. |
| **Request** | client → serveur | **Broadcast**, IP source toujours 0.0.0.0. Le client dit **quelle offre il accepte** (plusieurs serveurs peuvent répondre ; en général la **première** offre reçue) ; **option 54** = adresse du serveur choisi. |
| **Ack** | serveur → client | **Unicast ou broadcast** selon le client. Confirme ; **le client configure alors l'adresse** sur son interface. |

Message **Release** : **unicast**, client → serveur. **Bootp** est le prédécesseur de DHCP (pas au programme). Les numéros d'options ne sont pas à mémoriser.

### 4. Relais DHCP (*DHCP relay agent*)

- Les grandes entreprises utilisent souvent un **serveur DHCP centralisé** pour tous les sous-réseaux. Problème : **les broadcasts ne quittent pas le sous-réseau local, les routeurs ne les transfèrent pas**.
- Solution : configurer le routeur en **relais DHCP** : il transfère les messages DHCP broadcast des clients au serveur distant **en unicast**.
- Déroulement : PC1 broadcast Discover → R1 le relaie à SRV1 avec **source = adresse de l'interface G0/1 de R1** (192.168.1.1), destination = SRV1 ; SRV1 envoie l'Offer à 192.168.1.1 → R1 le transmet à PC1 (unicast ou broadcast) ; idem Request et Ack ; PC1 configure par exemple 192.168.1.100.

### 5. Configuration dans Cisco IOS

**Serveur DHCP** (R1 pour 192.168.1.0/24) :

- `ip dhcp excluded-address 192.168.1.1 192.168.1.10` (config globale) : plage **non attribuée** aux clients, réservée aux équipements réseau et serveurs. Facultatif mais recommandé.
- `ip dhcp pool <nom>` : un **pool** = un sous-réseau d'adresses attribuables plus les autres infos ; **un pool par réseau** servi.
  - `network 192.168.1.0 /24` ou `255.255.255.0` (les deux formes marchent).
  - `dns-server 8.8.8.8`.
  - `domain-name jeremysitlab.com`.
  - `default-router 192.168.1.1` : la **passerelle par défaut**.
  - `lease 0 5 30` : jours heures minutes ; `lease infinite` possible mais déconseillé.
- PC1 reçoit **.11**, première adresse disponible (.1 à .10 réservées).
- `show ip dhcp binding` : clients ayant une adresse (IP, MAC, expiration du bail, type de binding ; les bindings peuvent aussi être configurés manuellement).

**Relais DHCP** : sur l'**interface connectée aux clients** (G0/1), `ip helper-address <ip-serveur-DHCP>`. Le routeur doit avoir une **route vers le serveur** (statique ou OSPF). Vérification `show ip interface g0/1` : « Helper address is 192.168.10.10 ».

**Client DHCP** (rare) : sur l'interface, `ip address dhcp`. Vérification `show ip interface g0/1` : « Address determined by DHCP ».

### 6. Pièges d'examen

- Ordre **D-O-R-A** : Discover, Offer, Request, Ack. Discover et Request : **toujours broadcast** (client → serveur). Offer et Ack : **unicast ou broadcast** selon le champ Bootp flags (serveur → client). Release : **unicast**.
- **UDP 67 serveur, UDP 68 client.**
- `ipconfig /renew` déclenche un Discover ; `ipconfig /release` envoie un Release.
- Relais nécessaire quand : le routeur **n'est pas** serveur DHCP, il y a des clients DHCP dans son LAN, et **aucun autre serveur DHCP dans ce LAN**. `ip helper-address` se met sur **l'interface côté clients** du routeur **connecté aux clients**, avec l'**adresse du serveur DHCP**.
- `ip dhcp excluded-address` est en **config globale**, pas en mode pool.
- Bonus NetSim : `service dhcp` est **activé par défaut** ; `no service dhcp` fait ignorer tous les messages DHCP.

### 7. Commandes

```text
C:\> ipconfig /all        ! DHCP Enabled, adresse preferred, bail, passerelle, serveurs DHCP et DNS
C:\> ipconfig /release    ! envoie DHCP Release
C:\> ipconfig /renew      ! relance DORA

R1(config)# ip dhcp excluded-address 192.168.1.1 192.168.1.10 ! plage réservée (une seule adresse possible)
R1(config)# ip dhcp pool POOL1                     ! crée le pool
R1(dhcp-config)# network 192.168.1.0 255.255.255.0 ! sous-réseau attribué (/24 accepté)
R1(dhcp-config)# dns-server 8.8.8.8                ! serveur DNS annoncé
R1(dhcp-config)# domain-name jeremysitlab.com      ! domaine annoncé
R1(dhcp-config)# default-router 192.168.1.1        ! passerelle par défaut annoncée
R1(dhcp-config)# lease 0 5 30                      ! bail : jours heures minutes (ou lease infinite)
R1# show ip dhcp binding                           ! adresses louées, MAC, expiration
R1# show ip dhcp pool                              ! taille du pool, adresses louées (NetSim)
R1# show ip dhcp server statistics                 ! messages DHCP reçus/envoyés (NetSim)
R1(config)# service dhcp                           ! défaut ; no service dhcp = DHCP ignoré (NetSim)
R1(config-if)# ip helper-address 192.168.10.10     ! relais DHCP, sur l'interface côté clients
R1# show ip interface g0/1                         ! « Helper address is ... » / « Address determined by DHCP »
R2(config-if)# ip address dhcp                     ! client DHCP sur l'interface
R2# show run | section dhcp                        ! filtrer la running-config
```

### 8. Le lab (vidéo n°80)

Objectif : R2 serveur DHCP, R1 client DHCP sur G0/0 et relais DHCP pour 192.168.1.0/24 ; PC1, PC2 et G0/0 de R1 sans adresse au départ.

1. **R2, trois pools.** Réserver les 10 premières adresses : `ip dhcp excluded-address 192.168.1.1 192.168.1.10`, idem `192.168.2.1 192.168.2.10`, et l'adresse seule `ip dhcp excluded-address 203.0.113.1` (R2). `ip dhcp pool POOL1` : `network 192.168.1.0 255.255.255.0`, `dns-server 8.8.8.8`, `domain-name jeremysitlab.com`, `default-router 192.168.1.1`. `POOL2` : idem avec 192.168.2.0 et `default-router 192.168.2.1`. `POOL3` : `network 203.0.113.0 255.255.255.252` seulement. Vérifier `do show run | section dhcp`. Sur PC2 : `ipconfig /renew` → 192.168.2.11 ; `ipconfig /all` : domaine, passerelle R2, serveur DHCP R2, DNS 8.8.8.8.
2. **R1 client** : `interface g0/0`, `ip address dhcp`, `no shutdown` → R1 reçoit 203.0.113.2/30.
3. **R1 relais** : `interface g0/1` (côté clients), `ip helper-address 203.0.113.1`. Sur PC1 : `ipconfig /renew` (parfois plusieurs essais, ARP lent dans Packet Tracer) → adresse dans 192.168.1.0/24 ; `ipconfig /all` : domaine, masque, passerelle, DNS corrects.

Bonus Boson NetSim « Troubleshooting DHCP » : PC en 0.0.0.0, `show ip dhcp binding` vide, pings vers les SVI des switches OK, ports F0/12 up/up ; `show run | section dhcp`, `show ip dhcp pool` (254 adresses, 0 louée), `show ip dhcp server statistics` (aucun message) ; cause : **`no service dhcp`** ; correction `service dhcp` ; PC2 et PC3 obtiennent .10 (VLAN100 reste en panne, tâche 3 non faite).

### 9. Le quiz (5 questions + 1 Boson)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Ordre correct des messages quand un client DHCP obtient une adresse ? | **Discover, Offer, Request, Ack** (B) | Mnémonique DORA. |
| Quelle commande Windows fait émettre un DHCP Discover en broadcast ? | **`ipconfig /renew`** (D) | C, `ipconfig /release`, envoie un DHCP Release. A et B n'existent pas. |
| Offer de SRV1 vers R2 : quelle IP de destination ? | **255.255.255.255** (D) | Le drapeau **broadcast** est positionné dans le champ Bootp flags, donc le serveur envoie en broadcast (dans les exemples précédents il était en unicast). |
| Quels messages DHCP peuvent être envoyés en unicast ? (tous ceux qui s'appliquent) | **Ack** (A), **Release** (C), **Offer** (E) | A et E, serveur → client, unicast si le client l'indique dans Bootp flags ; C, client → serveur, toujours unicast. B et D (Discover, Request) sont toujours broadcast. |
| Dans quelle situation configurer un routeur en relais DHCP ? | **Routeur non serveur DHCP, clients DHCP dans son LAN, aucun autre serveur DHCP dans ce LAN** (A) | B, C et D ne nécessitent pas de relais. |
| Boson : serveur DHCP sur NetworkB (10.10.3.5), DHCP non actif sur les routeurs ; quelle commande pour que les clients de NetworkA reçoivent des adresses ? | **`ip helper-address 10.10.3.5` sur RouterA** (F) | RouterA reçoit les Discover broadcast de NetworkA : c'est lui le relais (C, D, F) ; l'adresse est celle du serveur DHCP. `ip helper-address` ne sert pas qu'à DHCP. |

---

## 🇬🇧 English version

### 1. Purpose of DHCP

- Exam topics **4.3** (explain the role of DHCP and DNS) and **4.6** (configure and verify **DHCP client and relay**). Also mentioned in section 5.0, security (covered later).
- DHCP lets hosts **automatically and dynamically** learn their network configuration: **IP address, subnet mask, default gateway, DNS server**, etc., without manual configuration (e.g. connecting a phone to WiFi).
- Typically used for **client devices** (PCs, phones). Routers, servers, etc. are usually **manually configured**: they need a fixed address (a default gateway that keeps changing would not be ideal).
- Small (home) network: the **router** is the DHCP server. Large enterprise: usually a **Windows or Linux server**.

### 2. Windows demonstration

- IPv4 properties of the connection: "Obtain an IP address automatically" and "Obtain DNS server address automatically" = DHCP in use.
- `ipconfig /all`: "DHCP Enabled: Yes" ("No" if manually configured), address 192.168.0.167/24 marked **"preferred"**: the PC was previously assigned it and asked for it again; if unavailable, it would get a different one.
- **Lease**: "Lease Obtained" and "Lease Expires". DHCP servers **lease** addresses; leases are usually **not permanent**, the client must give the address up at the end, or can **release** it earlier. Permanent assignment is possible but almost always a bad idea (cafe, airport: preserve available addresses; the client simply requests a new address if it stays longer).
- Default gateway, DHCP server and DNS server are all 192.168.0.1 (the home router): common in home networks.
- `ipconfig /release`: the PC sends a **DHCP Release** to the server, the address is free again. Wireshark: IPv4 from 192.168.0.167 to 192.168.0.1, **UDP source port 68, destination 67**. **DHCP servers use UDP 67, clients use UDP 68** (unlike DNS, where only the server port is fixed and the client uses a random ephemeral port). **Option 53** = DHCP message type. (Jeremy's favorite: the "magic cookie".)
- `ipconfig /renew`: the PC contacts the server and gets its configuration back: a **four-message** process.

### 3. The four messages: DORA

| Message | Direction | Addressing |
| :--- | :--- | :--- |
| **Discover** | client → server | **Broadcast**: destination MAC FFFF.FFFF.FFFF, source IP **0.0.0.0** (no address yet), destination **255.255.255.255**, UDP 68 → 67. The client doesn't know if or where a server exists. "Requested IP Address" option if the PC previously had an address. |
| **Offer** | server → client | **Unicast or broadcast depending on the client** (**Bootp flags** field: 0000 = unicast). Offers an address plus gateway, DNS, etc. UDP 67 → 68. Options: **51** = lease time, **6** = DNS server, **3** = router (default gateway). Some clients won't accept unicast before their address is configured, hence broadcast sometimes. |
| **Request** | client → server | **Broadcast**, source IP still 0.0.0.0. The client says **which offer it accepts** (several servers may answer; typically the **first** offer received); **option 54** = selected server's address. |
| **Ack** | server → client | **Unicast or broadcast** depending on the client. Confirms; **the client then configures the address** on its interface. |

**Release** message: **unicast**, client → server. **Bootp** is DHCP's predecessor (not on the exam). Option numbers need not be memorized.

### 4. DHCP relay agent

- Large enterprises often use a **centralized DHCP server** for all subnets. Problem: **broadcasts don't leave the local subnet, routers don't forward them**.
- Solution: configure the router as a **DHCP relay agent**: it forwards the clients' broadcast DHCP messages to the remote server **as unicast**.
- Flow: PC1 broadcasts Discover → R1 relays it to SRV1 with **source = R1's G0/1 address** (192.168.1.1), destination = SRV1; SRV1 sends the Offer to 192.168.1.1 → R1 forwards it to PC1 (unicast or broadcast); same for Request and Ack; PC1 configures e.g. 192.168.1.100.

### 5. Configuration in Cisco IOS

**DHCP server** (R1 for 192.168.1.0/24):

- `ip dhcp excluded-address 192.168.1.1 192.168.1.10` (global config): range **not given** to clients, reserved for network devices and servers. Optional but a good idea.
- `ip dhcp pool <name>`: a **pool** = a subnet of assignable addresses plus other info; **one pool per network** served.
  - `network 192.168.1.0 /24` or `255.255.255.0` (either works).
  - `dns-server 8.8.8.8`.
  - `domain-name jeremysitlab.com`.
  - `default-router 192.168.1.1`: the **default gateway**.
  - `lease 0 5 30`: days hours minutes; `lease infinite` possible but not recommended.
- PC1 gets **.11**, the first available address (.1 to .10 reserved).
- `show ip dhcp binding`: clients currently assigned addresses (IP, MAC, lease expiration, binding type; bindings can also be configured manually).

**DHCP relay agent**: on the **interface connected to the clients** (G0/1), `ip helper-address <DHCP-server-ip>`. The router must have a **route to the server** (static or OSPF). Verify with `show ip interface g0/1`: "Helper address is 192.168.10.10".

**DHCP client** (rare): on the interface, `ip address dhcp`. Verify with `show ip interface g0/1`: "Address determined by DHCP".

### 6. Exam traps

- Order **D-O-R-A**: Discover, Offer, Request, Ack. Discover and Request: **always broadcast** (client → server). Offer and Ack: **unicast or broadcast** depending on the Bootp flags field (server → client). Release: **unicast**.
- **UDP 67 server, UDP 68 client.**
- `ipconfig /renew` triggers a Discover; `ipconfig /release` sends a Release.
- Relay needed when: the router **is not** a DHCP server, there are DHCP clients in its LAN, and **no other DHCP server in that LAN**. `ip helper-address` goes on the **client-facing interface** of the router **connected to the clients**, with the **DHCP server's address**.
- `ip dhcp excluded-address` is in **global config**, not pool mode.
- NetSim bonus: `service dhcp` is **enabled by default**; `no service dhcp` makes the router drop all DHCP messages.

### 7. Commands

```text
C:\> ipconfig /all        ! DHCP Enabled, preferred address, lease, gateway, DHCP and DNS servers
C:\> ipconfig /release    ! sends DHCP Release
C:\> ipconfig /renew      ! restarts DORA

R1(config)# ip dhcp excluded-address 192.168.1.1 192.168.1.10 ! reserved range (single address allowed)
R1(config)# ip dhcp pool POOL1                     ! create the pool
R1(dhcp-config)# network 192.168.1.0 255.255.255.0 ! assigned subnet (/24 accepted)
R1(dhcp-config)# dns-server 8.8.8.8                ! advertised DNS server
R1(dhcp-config)# domain-name jeremysitlab.com      ! advertised domain
R1(dhcp-config)# default-router 192.168.1.1        ! advertised default gateway
R1(dhcp-config)# lease 0 5 30                      ! lease: days hours minutes (or lease infinite)
R1# show ip dhcp binding                           ! leased addresses, MAC, expiration
R1# show ip dhcp pool                              ! pool size, leased addresses (NetSim)
R1# show ip dhcp server statistics                 ! DHCP messages received/sent (NetSim)
R1(config)# service dhcp                           ! default; no service dhcp = DHCP ignored (NetSim)
R1(config-if)# ip helper-address 192.168.10.10     ! DHCP relay, on the client-facing interface
R1# show ip interface g0/1                         ! "Helper address is ..." / "Address determined by DHCP"
R2(config-if)# ip address dhcp                     ! DHCP client on the interface
R2# show run | section dhcp                        ! filter the running-config
```

### 8. The lab (video #80)

Goal: R2 as DHCP server, R1 as DHCP client on G0/0 and DHCP relay agent for 192.168.1.0/24; PC1, PC2 and R1's G0/0 have no address at first.

1. **R2, three pools.** Reserve the first 10 addresses: `ip dhcp excluded-address 192.168.1.1 192.168.1.10`, same for `192.168.2.1 192.168.2.10`, and the single address `ip dhcp excluded-address 203.0.113.1` (R2). `ip dhcp pool POOL1`: `network 192.168.1.0 255.255.255.0`, `dns-server 8.8.8.8`, `domain-name jeremysitlab.com`, `default-router 192.168.1.1`. `POOL2`: same with 192.168.2.0 and `default-router 192.168.2.1`. `POOL3`: `network 203.0.113.0 255.255.255.252` only. Check with `do show run | section dhcp`. On PC2: `ipconfig /renew` → 192.168.2.11; `ipconfig /all`: domain, gateway R2, DHCP server R2, DNS 8.8.8.8.
2. **R1 client**: `interface g0/0`, `ip address dhcp`, `no shutdown` → R1 gets 203.0.113.2/30.
3. **R1 relay**: `interface g0/1` (client side), `ip helper-address 203.0.113.1`. On PC1: `ipconfig /renew` (may take a few tries, ARP is slow in Packet Tracer) → address in 192.168.1.0/24; `ipconfig /all`: domain, mask, gateway, DNS all correct.

Boson NetSim bonus "Troubleshooting DHCP": PCs at 0.0.0.0, `show ip dhcp binding` empty, pings to switch SVIs OK, F0/12 ports up/up; `show run | section dhcp`, `show ip dhcp pool` (254 addresses, 0 leased), `show ip dhcp server statistics` (no messages); cause: **`no service dhcp`**; fix `service dhcp`; PC2 and PC3 get .10 (VLAN100 still broken, task 3 not done).

### 9. The quiz (5 questions + 1 Boson)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Correct order of messages when a DHCP client gets an address? | **Discover, Offer, Request, Ack** (B) | Remember DORA. |
| Which Windows command makes a PC broadcast a DHCP Discover? | **`ipconfig /renew`** (D) | C, `ipconfig /release`, sends a DHCP Release. A and B are not real commands. |
| Offer from SRV1 to R2: what destination IP? | **255.255.255.255** (D) | The **broadcast** flag is set in the Bootp flags field, so the server broadcasts (in earlier examples it was unicast). |
| Which DHCP messages can be sent using unicast? (select all that apply) | **Ack** (A), **Release** (C), **Offer** (E) | A and E, server → client, unicast if the client indicates it in Bootp flags; C, client → server, sent unicast. B and D (Discover, Request) are always broadcast. |
| In which situation would you configure a router as a DHCP relay agent? | **Router not a DHCP server, DHCP clients in its connected LAN, no other DHCP server in that LAN** (A) | B, C and D don't require a relay agent. |
| Boson: DHCP server on NetworkB (10.10.3.5), DHCP not running on routers; which command lets NetworkA clients get addresses? | **`ip helper-address 10.10.3.5` on RouterA** (F) | RouterA receives NetworkA's broadcast Discovers: it is the relay (C, D, F); the address is the DHCP server's. `ip helper-address` is not only for DHCP. |
