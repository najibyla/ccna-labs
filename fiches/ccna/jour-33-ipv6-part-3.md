# CCNA Day 33 : IPv6 Part 3 / IPv6, partie 3

> Source : Jeremy's IT Lab, vidéo n°67 « IPv6 Part 3 | Day 33 » (cours, 44 min) et vidéo n°68 « Configuring IPv6 (Part 3) | Day 33 Lab » (lab, 19 min) de la playlist. Fiche rédigée à partir des transcriptions le 6 octobre 2026. Les adresses des exemples d'écriture RFC 5952, du calcul solicited-node et les options des quiz Q4 et Q5 sont affichées à l'écran et absentes de la transcription.

## 🇫🇷 Version française

### 1. Cadre

Sujet d'examen **3.3** : configurer et vérifier en IPv6 les mêmes routes statiques qu'en IPv4 (réseau, hôte, par défaut, flottante). Au programme aussi : écriture correcte des adresses, en-tête IPv6, NDP, SLAAC, DAD.

### 2. Écrire une adresse IPv6 (RFC 5952)

- Un **RFC** (*Request for Comments*) est une publication de l'**ISOC** (*Internet Society*) et d'organisations associées comme l'**IETF** (*Internet Engineering Task Force*) : les documents officiels des spécifications d'Internet.
- **RFC 5952**, « A Recommendation for IPv6 Address Text Representation » :
  1. Les zéros de tête **DOIVENT** être supprimés.
  2. Le `::` **DOIT** abréger la **plus longue** série de quartets nuls ; **un seul quartet nul ne s'abrège pas** avec `::`.
  3. À longueur égale, on abrège la série **de gauche**.
  4. Les chiffres **a-f** s'écrivent en **minuscules**.
- Les routeurs Cisco affichent des majuscules : techniquement incorrect, mais sans gravité. Jeremy n'utilise plus que des minuscules.

### 3. L'en-tête IPv6

- **Taille fixe de 40 octets** (IPv4 : variable de 20 à 60 octets), donc pas de champ *header length* ; traitement plus simple pour les routeurs, meilleures performances. Peu probable à l'examen, mais fondamental.

| Champ | Taille | Rôle |
| :--- | :--- | :--- |
| Version | 4 bits | Toujours 6 (0110). |
| Traffic Class | 8 bits | QoS, priorité (téléphonie IP, visio). |
| Flow Label | 20 bits | Identifie un flux entre une source et une destination. |
| Payload Length | 16 bits | Longueur en octets du segment de couche 4 encapsulé, **sans** l'en-tête (toujours 40). |
| Next Header | 8 bits | Type de l'en-tête suivant (TCP, UDP) ; équivalent du champ *Protocol* d'IPv4. |
| Hop Limit | 8 bits | Décrémenté de 1 par chaque routeur, paquet jeté à 0 ; équivalent du **TTL**. |
| Source Address / Destination Address | 128 bits chacun | Adresses IPv6 source et destination. |

### 4. Adresse multicast solicited-node

- Calculée à partir d'une adresse unicast : préfixe fixe **ff02::1:ff** + les **6 derniers chiffres hexa** de l'adresse unicast.
- Exemple de `show ipv6 interface` : R1 a rejoint **FF02::1:FF36:8500**, dont les six derniers chiffres sont ceux de l'adresse global unicast de l'interface (avec FF02::1 et FF02::2).

### 5. NDP (*Neighbor Discovery Protocol*)

Protocole IPv6 aux fonctions multiples, pas listé explicitement à l'examen mais aussi essentiel qu'ARP en IPv4. **IPv6 n'utilise pas ARP.**

**Fonction 1 : remplacer ARP**, avec **ICMPv6** et les adresses solicited-node (multicast, plus efficace qu'un broadcast ARP).

| Message | Type ICMPv6 | Équivalent | Adresses (exemple `ping 2001:db8::78:9abc` de R1 vers R2) |
| :--- | :--- | :--- | :--- |
| **Neighbor Solicitation (NS)** | **135** | ARP request | IP source R1 ; IP destination = **solicited-node de R2** (calculée depuis l'adresse tapée) ; MAC source R1 ; MAC destination = MAC multicast dérivée de la solicited-node (Wireshark : IPv6mcast_ff:78:9a:bc). |
| **Neighbor Advertisement (NA)** | **136** | ARP reply | Unicast de R2 vers R1 (R2 connaît l'IP et la MAC de R1, sources du NS). |

- Pas de table ARP mais une **table de voisins** : `show ipv6 neighbor` : colonnes IPv6 address (R1 a l'adresse global unicast **et** la link-local de R2, apprise automatiquement), **Age** (minutes depuis le dernier trafic), **Link-layer Address** (MAC), **Interface**, **State** (REACH = joignable). Tous les équipements IPv6 utilisent NDP, pas seulement Cisco.

**Fonction 2 : découverte des routeurs.**

| Message | Type ICMPv6 | Destination | Rôle |
| :--- | :--- | :--- | :--- |
| **Router Solicitation (RS)** | **133** | **FF02::2** (all routers) | Demande aux routeurs du lien de s'identifier ; envoyé à l'activation d'une interface ou à la connexion au réseau. Tous les hôtes IPv6 en envoient. |
| **Router Advertisement (RA)** | **134** | **FF02::1** (all nodes) | Le routeur annonce sa présence et des informations sur le lien ; en réponse à un RS **et** périodiquement. Seuls les routeurs en envoient. Permet aux hôtes d'apprendre leur default gateway. |

**Fonction 3 : SLAAC** (*Stateless Address Auto-configuration*) : l'hôte apprend le **préfixe** du lien par RS/RA, puis génère son adresse (identifiant d'interface par **EUI-64** ou aléatoire selon le fabricant). Commande `ipv6 address autoconfig`, **sans préfixe** (contrairement à `eui-64`). Fonction standard d'IPv6, pas propre à Cisco.

**Fonction 4 : DAD** (*Duplicate Address Detection*) : à chaque initialisation d'interface (`no shutdown`) ou configuration d'adresse (manuelle ou SLAAC), l'hôte envoie un **NS vers sa propre adresse solicited-node**. Pas de réponse = adresse unique ; un **NA** en réponse = adresse déjà utilisée (message d'erreur sur le routeur Cisco). Pas de nouveau type de message.

### 6. Routage statique IPv6

- Même principe qu'IPv4 : correspondance **la plus spécifique** dans la table. Processus et **tables séparés** (`show ipv6 route`). IPv4 routé par défaut, **IPv6 non** : `ipv6 unicast-routing` obligatoire, sinon le routeur envoie et reçoit de l'IPv6 mais **ne route pas**. « Si tout semble correct mais ne marche pas, c'est probablement cette commande. »
- Table IPv6 : une route **connected** (/64, *network route*) et une route **local** (/128, *host route*) par interface ; une route **FF00::/8 via Null0** (jette le multicast, hors CCNA) ; **les link-local n'apparaissent pas** dans la table.
- Syntaxe Cisco : `ipv6 route <destination>/<préfixe> {<next-hop> | <interface-sortie> [<next-hop>]} [AD]`. Accolades = choix obligatoire ; crochets = optionnel.

| Type (IPv4 et IPv6) | Ce qu'on indique | Exemple sur R1 |
| :--- | :--- | :--- |
| **Directly attached** | Interface de sortie seule | `ipv6 route 2001:db8:0:3::/64 g0/0` |
| **Recursive** | Next-hop seul (**double recherche** : destination, puis next-hop pour trouver l'interface) | `ipv6 route 2001:db8:0:3::/64 2001:db8:0:12::2` |
| **Fully specified** | Interface **et** next-hop | `ipv6 route 2001:db8:0:3::/64 g0/0 2001:db8:0:12::2` |

- **Piège IPv6** : une route *directly attached* **ne fonctionne pas sur une interface Ethernet** (la commande est acceptée mais le paquet n'est pas envoyé) ; elle fonctionne sur une interface série. Utiliser recursive ou fully specified.
- Types de l'examen : **network** (`2001:db8:0:3::/64`), **host** (**/128**, comme /32 en IPv4), **default** (**::/0**, comme 0.0.0.0/0), **floating** (AD élevée : **> 110** si la route principale vient d'OSPF, **> 90** si EIGRP ; AD d'une statique normale = **1**).
- **Next-hop link-local** : erreur « Interface has to be specified for a link-local nexthop » → obligatoirement **fully specified**, car le routeur ne peut pas deviner l'interface reliée à cette link-local.

### 7. Pièges d'examen

- NS = 135, NA = 136, RS = 133, RA = 134 ; RS → FF02::2, RA → FF02::1.
- DAD utilise un **NS** (vers sa propre solicited-node), pas un nouveau message.
- Route avec interface **et** next-hop = fully specified ; destination /64 = network, /128 = host.
- Directly attached impossible sur Ethernet en IPv6 ; link-local comme next-hop impose l'interface de sortie.
- Un ping exige une route **retour** : si RouterC n'a pas de route vers le réseau de RouterA, le ping échoue (bonus Boson).

### 8. Commandes IOS

```
R1(config)# ipv6 unicast-routing                      ! obligatoire pour router et pour envoyer des RA (SLAAC)
R2(config-if)# ipv6 address autoconfig                 ! SLAAC : préfixe appris par RS/RA, pas de préfixe à saisir
R1# show ipv6 neighbor                                 ! table de voisins (remplace la table ARP)
R1# show ipv6 route                                    ! table de routage IPv6
R1(config)# ipv6 route 2001:db8:0:3::/64 2001:db8:0:12::2          ! route réseau recursive
R2(config)# ipv6 route 2001:db8:0:1::2/128 2001:db8:0:12::1        ! route hôte (/128), forme vue dans la vidéo
R3(config)# ipv6 route ::/0 2001:db8:0:13::1                       ! route par défaut
R1(config)# ipv6 route 2001:db8:0:3::/64 g0/1 2001:db8:0:13::2     ! fully specified
R1(config)# ipv6 route 2001:db8:0:3::/64 s0/0/0 fe80::... 5        ! next-hop link-local + AD 5 = floating
R1# show run | include ipv6 route                      ! voir les routes flottantes absentes de la table
```

### 9. Le lab (vidéo n°68)

Objectif : PC1 et PC2 se pinguent via R1-R3 (chemin principal), secours par R2 (liens série, link-local seulement) ; adresses des PC par SLAAC.

1. `ipv6 unicast-routing` sur R1, R2, R3 : sans lui, pas de routage **ni de RA**, donc pas de SLAAC.
2. PC1 et PC2, onglet Config : gateway sur **Automatic** → link-local du routeur apprise par RA ; sur FastEthernet0, Packet Tracer active SLAAC : préfixe appris du routeur, identifiant EUI-64. `ipconfig` dans le CLI du PC pour copier l'adresse.
3. **R1** : `ipv6 route 2001:db8:0:3::/64 g0/1 2001:db8:0:13::2` (fully specified ; directly attached impossible sur Ethernet). Secours : `do show ipv6 interface brief` sur R2 pour copier la link-local de s0/0/0, puis `ipv6 route 2001:db8:0:3::/64 s0/0/0 <link-local R2> 5` (AD 5 > 1 : flottante). `do show ipv6 route` ne montre que la route via R3 ; `do show run | include ipv6 route` montre les deux.
4. **R2** : `ipv6 route 2001:db8:0:1::/64 s0/0/0 <link-local R1>` et `ipv6 route 2001:db8:0:3::/64 s0/0/1 <link-local R3>`.
5. **R3** : `ipv6 route 2001:db8:0:1::/64 g0/1 2001:db8:0:13::1` puis `ipv6 route 2001:db8:0:1::/64 s0/0/0 <link-local R2> 5`.
6. Test : `ping` PC1 → PC2 OK ; `tracert` : gateway, puis **13::2** (R3), puis PC2. Suppression du câble R1-R3 : ping toujours OK ; le traceroute bute au 2e saut (R2 n'a que des link-local, non routables) puis affiche R3 et PC2. Sans importance : les PC se joignent.

Bonus NetSim (Configuring IPv6 2) : Router4 pinge l'interface série de Router3 mais pas son loopback6 (pas de route, `show ipv6 route`). RIPng : `ipv6 router rip boson` en global ne suffit pas (aucune route tant que RIP n'est pas activé sur les interfaces), puis `ipv6 rip boson enable` sur s0/1, s0/0 et loopback6 ; après convergence, routes RIP présentes et ping OK ; `show ipv6 protocols` liste l'interface série.

### 10. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| R2 informe R1 de la MAC de son G0/0 : quel message ? | **NA** (neighbor advertisement) | R1 avait envoyé un NS ; RS et RA servent à la découverte des routeurs. |
| Adresse configurée sur G0/0 de R1 : message envoyé pour DAD ? | **NS** | Envoyé à sa propre adresse solicited-node ; réponse = doublon. |
| R1 envoie un RA : adresse de destination ? | **FF02::1** | All-nodes link-local multicast ; FF02::2 est la destination des RS ; FF01 ne quitte pas l'équipement. |
| Route statique affichée : quels types (deux réponses) ? | **Fully specified** et **network** | Interface et next-hop spécifiés ; destination = réseau, pas hôte. |
| Quelle commande configure une route **hôte recursive** ? | **C** | A = directly attached ; B = fully specified ; D = recursive mais route réseau ; seule C est /128 et next-hop seul. |

Bonus Boson : `ipv6 route 2001:db8:2::/64 2001:db8:1::2` sur RouterA mais le ping vers RouterC échoue → **RouterC n'a pas de route vers 2001:db8:1::/64** (retour impossible). RouterB a ces deux réseaux en connected ; RouterA n'a pas besoin de route par défaut.

---

## 🇬🇧 English version

### 1. Scope

Exam topic **3.3**: configure and verify in IPv6 the same static routes as in IPv4 (network, host, default, floating). Also covered: proper address representation, the IPv6 header, NDP, SLAAC, DAD.

### 2. Writing an IPv6 address (RFC 5952)

- An **RFC** (Request for Comments) is a publication from the **ISOC** (Internet Society) and associated organizations such as the **IETF** (Internet Engineering Task Force): the official documents of Internet specifications.
- **RFC 5952**, "A Recommendation for IPv6 Address Text Representation":
  1. Leading 0s **MUST** be removed.
  2. `::` **MUST** shorten the **longest** string of all-0 quartets; **a single all-0 quartet is not shortened** with `::`.
  3. With two equal-length choices, shorten the one **on the left**.
  4. Hex digits **a-f** are written in **lower-case**.
- Cisco routers display upper-case: technically incorrect, but not a big deal. Jeremy now uses lower-case only.

### 3. The IPv6 header

- **Fixed size of 40 bytes** (IPv4: variable, 20 to 60 bytes), so no header length field; simpler processing for routers, better performance. Unlikely on the exam, but foundational.

| Field | Size | Role |
| :--- | :--- | :--- |
| Version | 4 bits | Always 6 (0110). |
| Traffic Class | 8 bits | QoS, priority (IP phones, live video). |
| Flow Label | 20 bits | Identifies a flow between a source and a destination. |
| Payload Length | 16 bits | Length in bytes of the encapsulated Layer 4 segment, **excluding** the header (always 40). |
| Next Header | 8 bits | Type of the next header (TCP, UDP); same function as IPv4's Protocol field. |
| Hop Limit | 8 bits | Decremented by 1 by each router, discarded at 0; same as **TTL**. |
| Source Address / Destination Address | 128 bits each | Source and destination IPv6 addresses. |

### 4. Solicited-node multicast address

- Calculated from a unicast address: fixed prefix **ff02::1:ff** + the **last 6 hex digits** of the unicast address.
- `show ipv6 interface` example: R1 joined **FF02::1:FF36:8500**, whose last six digits match the interface's global unicast address (along with FF02::1 and FF02::2).

### 5. NDP (Neighbor Discovery Protocol)

An IPv6 protocol with several functions, not explicitly listed on the exam but as essential as ARP in IPv4. **IPv6 does not use ARP.**

**Function 1: replacing ARP**, using **ICMPv6** and solicited-node addresses (multicast, more efficient than an ARP broadcast).

| Message | ICMPv6 type | Equivalent | Addresses (example `ping 2001:db8::78:9abc` from R1 to R2) |
| :--- | :--- | :--- | :--- |
| **Neighbor Solicitation (NS)** | **135** | ARP request | Source IP R1; destination IP = **R2's solicited-node** (computed from the typed address); source MAC R1; destination MAC = multicast MAC derived from the solicited-node address (Wireshark: IPv6mcast_ff:78:9a:bc). |
| **Neighbor Advertisement (NA)** | **136** | ARP reply | Unicast from R2 to R1 (R2 knows R1's IP and MAC, sources of the NS). |

- No ARP table but a **neighbor table**: `show ipv6 neighbor`: columns IPv6 address (R1 has R2's global unicast **and** link-local, learned automatically), **Age** (minutes since last traffic), **Link-layer Address** (MAC), **Interface**, **State** (REACH = reachable). All IPv6 devices use NDP, not only Cisco.

**Function 2: router discovery.**

| Message | ICMPv6 type | Destination | Role |
| :--- | :--- | :--- | :--- |
| **Router Solicitation (RS)** | **133** | **FF02::2** (all routers) | Asks routers on the link to identify themselves; sent when an interface is enabled or the host connects. All IPv6 hosts send them. |
| **Router Advertisement (RA)** | **134** | **FF02::1** (all nodes) | The router announces its presence and link information; in response to an RS **and** periodically. Only routers send them. Lets hosts learn their default gateway. |

**Function 3: SLAAC** (Stateless Address Auto-configuration): the host learns the link **prefix** via RS/RA, then generates its address (interface ID via **EUI-64** or random, depending on the maker). Command `ipv6 address autoconfig`, **no prefix** needed (unlike `eui-64`). A standard IPv6 function, not Cisco-specific.

**Function 4: DAD** (Duplicate Address Detection): whenever an interface initializes (`no shutdown`) or an address is configured (manual or SLAAC), the host sends an **NS to its own solicited-node address**. No reply = unique address; an **NA** reply = address already in use (error message on a Cisco router). No new message types.

### 6. IPv6 static routing

- Same principle as IPv4: **most specific match** in the table. Separate processes and **separate tables** (`show ipv6 route`). IPv4 routing is on by default, **IPv6 is not**: `ipv6 unicast-routing` is required, otherwise the router sends and receives IPv6 but **does not route**. "If everything looks correct but it doesn't work, you probably forgot that command."
- IPv6 table: a **connected** route (/64, network route) and a **local** route (/128, host route) per interface; a **FF00::/8 via Null0** route (discards multicast, beyond the CCNA); **link-local addresses do not appear** in the table.
- Cisco syntax: `ipv6 route <destination>/<prefix> {<next-hop> | <exit-interface> [<next-hop>]} [AD]`. Curly brackets = required choice; square brackets = optional.

| Type (IPv4 and IPv6) | What is specified | Example on R1 |
| :--- | :--- | :--- |
| **Directly attached** | Exit interface only | `ipv6 route 2001:db8:0:3::/64 g0/0` |
| **Recursive** | Next hop only (**recursive lookup**: destination, then next hop to find the interface) | `ipv6 route 2001:db8:0:3::/64 2001:db8:0:12::2` |
| **Fully specified** | Exit interface **and** next hop | `ipv6 route 2001:db8:0:3::/64 g0/0 2001:db8:0:12::2` |

- **IPv6 trap**: a directly attached route **does not work on an Ethernet interface** (the command is accepted but the packet is not sent); it works on a serial interface. Use recursive or fully specified.
- Exam route types: **network** (`2001:db8:0:3::/64`), **host** (**/128**, like /32 in IPv4), **default** (**::/0**, like 0.0.0.0/0), **floating** (higher AD: **> 110** if the main route is from OSPF, **> 90** if EIGRP; a normal static route has AD **1**).
- **Link-local next hop**: error "Interface has to be specified for a link-local nexthop" → must be **fully specified**, because the router cannot figure out which interface that link-local is connected to.

### 7. Exam traps

- NS = 135, NA = 136, RS = 133, RA = 134; RS → FF02::2, RA → FF02::1.
- DAD uses an **NS** (to its own solicited-node address), not a new message.
- Route with interface **and** next hop = fully specified; /64 destination = network, /128 = host.
- Directly attached impossible on Ethernet in IPv6; a link-local next hop requires the exit interface.
- A ping needs a **return** route: if RouterC has no route to RouterA's network, the ping fails (Boson bonus).

### 8. IOS commands

```
R1(config)# ipv6 unicast-routing                      ! required for routing and for sending RAs (SLAAC)
R2(config-if)# ipv6 address autoconfig                 ! SLAAC: prefix learned via RS/RA, no prefix to type
R1# show ipv6 neighbor                                 ! neighbor table (replaces the ARP table)
R1# show ipv6 route                                    ! IPv6 routing table
R1(config)# ipv6 route 2001:db8:0:3::/64 2001:db8:0:12::2          ! recursive network route
R2(config)# ipv6 route 2001:db8:0:1::2/128 2001:db8:0:12::1        ! host route (/128), form shown in the video
R3(config)# ipv6 route ::/0 2001:db8:0:13::1                       ! default route
R1(config)# ipv6 route 2001:db8:0:3::/64 g0/1 2001:db8:0:13::2     ! fully specified
R1(config)# ipv6 route 2001:db8:0:3::/64 s0/0/0 fe80::... 5        ! link-local next hop + AD 5 = floating
R1# show run | include ipv6 route                      ! see floating routes absent from the table
```

### 9. The lab (video 68)

Goal: PC1 and PC2 ping each other via R1-R3 (main path), backup via R2 (serial links, link-local only); PC addresses via SLAAC.

1. `ipv6 unicast-routing` on R1, R2, R3: without it, no routing **and no RAs**, so no SLAAC.
2. PC1 and PC2, Config tab: gateway set to **Automatic** → router's link-local learned from RAs; on FastEthernet0, Packet Tracer enables SLAAC: prefix learned from the router, EUI-64 interface ID. `ipconfig` in the PC CLI to copy the address.
3. **R1**: `ipv6 route 2001:db8:0:3::/64 g0/1 2001:db8:0:13::2` (fully specified; directly attached impossible on Ethernet). Backup: `do show ipv6 interface brief` on R2 to copy s0/0/0's link-local, then `ipv6 route 2001:db8:0:3::/64 s0/0/0 <R2 link-local> 5` (AD 5 > 1: floating). `do show ipv6 route` shows only the route via R3; `do show run | include ipv6 route` shows both.
4. **R2**: `ipv6 route 2001:db8:0:1::/64 s0/0/0 <R1 link-local>` and `ipv6 route 2001:db8:0:3::/64 s0/0/1 <R3 link-local>`.
5. **R3**: `ipv6 route 2001:db8:0:1::/64 g0/1 2001:db8:0:13::1` then `ipv6 route 2001:db8:0:1::/64 s0/0/0 <R2 link-local> 5`.
6. Test: `ping` PC1 → PC2 OK; `tracert`: gateway, then **13::2** (R3), then PC2. Delete the R1-R3 cable: ping still OK; traceroute struggles at the 2nd hop (R2 has only link-locals, not routable) then shows R3 and PC2. Not a problem: the PCs reach each other.

NetSim bonus (Configuring IPv6 2): Router4 pings Router3's serial interface but not its loopback6 (no route, `show ipv6 route`). RIPng: `ipv6 router rip boson` globally is not enough (no routes until RIP is enabled on interfaces), then `ipv6 rip boson enable` on s0/1, s0/0 and loopback6; after convergence, RIP routes present and ping OK; `show ipv6 protocols` lists the serial interface.

### 10. The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| R2 tells R1 about the MAC of its G0/0: which message? | **NA** (neighbor advertisement) | R1 had sent an NS; RS and RA are for router discovery. |
| Address configured on R1's G0/0: message sent to perform DAD? | **NS** | Sent to its own solicited-node address; a reply = duplicate. |
| R1 sends an RA: destination address? | **FF02::1** | All-nodes link-local multicast; FF02::2 is the RS destination; FF01 never leaves the device. |
| Static route shown: which types (select two)? | **Fully specified** and **network** | Both interface and next hop specified; destination is a network, not a host. |
| Which command configures a **recursive host** route? | **C** | A = directly attached; B = fully specified; D = recursive but a network route; only C is /128 with next hop only. |

Boson bonus: `ipv6 route 2001:db8:2::/64 2001:db8:1::2` on RouterA but the ping to RouterC fails → **RouterC has no route to 2001:db8:1::/64** (no return path). RouterB has both networks connected; RouterA does not need a default route.
