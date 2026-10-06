# CCNA Day 32 : IPv6 Part 2 / IPv6, partie 2

> Source : Jeremy's IT Lab, vidéo n°65 « IPv6 Part 2 | Day 32 » (cours, 40 min) et vidéo n°66 « Configuring IPv6 (Part 2) | Day 32 Lab » (lab, 21 min) de la playlist. Fiche rédigée à partir des transcriptions le 6 octobre 2026. Les exercices EUI-64 de la vidéo, le tableau complet des adresses multicast et les adresses MAC du lab sont affichés à l'écran et absents de la transcription : seules les valeurs énoncées oralement figurent ici.

## 🇫🇷 Version française

### 1. Cadre

Sujet d'examen **1.9** : comparer les types d'adresses IPv6 : 1.9.a global unicast, 1.9.b unique local, 1.9.c link local, 1.9.d anycast, 1.9.e multicast, 1.9.f modified EUI-64. Vidéo très dense : utiliser les flashcards (tag Anki `ipv6` sur les cartes des Days 31 et 32).

### 2. EUI-64 (*Extended Unique Identifier*, 1.9.f)

- Terme exact : **modified EUI-64**, souvent abrégé EUI-64 ; pour le CCNA, c'est la même chose. Ce n'est **pas un type d'adresse** mais une **méthode** de génération automatique : convertir une **MAC de 48 bits** en un **identifiant d'interface de 64 bits**, qui devient la partie hôte d'une adresse **/64**.
- Trois étapes, à savoir faire à la main (le routeur le fait automatiquement) :
  1. **Couper la MAC en deux** : `1234 5678 90AB` → `123456` | `7890AB` (entre le 6 et le 7).
  2. **Insérer `FFFE` au milieu** : `1234 56FF FE78 90AB`.
  3. **Inverser le 7e bit** (0 → 1, 1 → 0). Chaque chiffre hexa = 4 bits : le `1` = bits 1 à 4, le `2` = bits 5 à 8, le 7e bit est donc le **3e bit du `2`** (0010). Il vaut 1 → 0, le `2` devient `0` : identifiant **1034:56FF:FE78:90AB**.
- Pourquoi inverser le 7e bit (hors CCNA) : c'est le bit **U/L** (*Universal/Local*) de la MAC. **UAA** (*universally administered address*, attribuée par le fabricant) : U/L = 0 ; **LAA** (*locally administered address*, fixée par un admin ou un protocole, commande `mac-address` sur l'interface) : U/L = 1. Dans EUI-64 le sens est **inversé** : 1 = issu d'une UAA, 0 = issu d'une LAA. Sans effet sur le fonctionnement de l'adresse.
- Configuration : `ipv6 address 2001:db8::/64 eui-64` ; vérification avec `show interfaces` (MAC) puis `show ipv6 interface brief`. Dans l'exemple de la vidéo, EUI-64 a changé un **C** de la MAC en **E** et inséré FFFE au milieu.

### 3. Les types d'adresses

| Type | Plage | Caractéristiques |
| :--- | :--- | :--- |
| **Global unicast** (1.9.a) | À l'origine **2000::/3** (2000:: à 3FFF:FFFF:…) ; aujourd'hui toute adresse non réservée | **Publiques**, routables sur Internet, **enregistrement obligatoire**, globalement uniques. Structure : **global routing prefix** (/48, attribué par le FAI) + **subnet identifier** (16 bits, plus de 65 000 sous-réseaux) + **interface identifier** (64 bits, EUI-64 ou manuel). |
| **Unique local** (1.9.b) | **FC00::/7**, mais une mise à jour impose le 8e bit à 1 : en pratique **FD** | **Privées**, non routables sur Internet (le FAI jette les paquets), **sans enregistrement**, utilisables librement en interne. Structure : **FD** + **global ID** (40 bits, **à générer aléatoirement** pour éviter les doublons de sous-réseaux lors d'une fusion d'entreprises) + subnet identifier (16 bits) + interface ID (64 bits). |
| **Link local** (1.9.c) | **FE80::/10** ; les 54 bits suivants doivent être à 0, donc toujours **FE8** (jamais FE9, FEA, FEB) | **Générées automatiquement** sur toute interface où IPv6 est activé (adresse configurée ou `ipv6 enable`), identifiant d'interface par **EUI-64**. Communication **dans un seul lien/sous-réseau** : les routeurs **ne routent pas** les paquets vers une destination link-local. Usages : adjacences **OSPFv3**, **next-hop des routes statiques**, **NDP** (*Neighbor Discovery Protocol*, remplaçant d'ARP, Day 33). |
| **Multicast** (1.9.e) | **FF00::/8** | « Un vers plusieurs ». **IPv6 n'a pas de broadcast** : l'adresse **all nodes / all hosts FF02::1** en tient lieu. |
| **Anycast** (1.9.d) | **Pas de plage dédiée** : une adresse unicast ordinaire (global unicast ou unique local) déclarée anycast | « Un vers un parmi plusieurs » : plusieurs routeurs portent la même adresse, l'annoncent par un protocole de routage, et le trafic va au **plus proche** (métrique la plus faible). Configurée en **/128** (équivalent du /32 IPv4) avec le mot-clé `anycast` ; `show ipv6 interface g0/0` l'affiche sous *global unicast addresses* avec **ANY** à la fin (**EUI** pour une adresse EUI-64). |
| **Unspecified** | **::** (tout à zéro) | Quand l'équipement ne connaît pas encore son adresse ; route par défaut IPv6 **::/0**. Équivalent IPv4 : 0.0.0.0. |
| **Loopback** | **::1** (127 zéros puis un 1) | Test de la pile locale, jamais envoyé à d'autres équipements. Équivalent IPv4 : 127.0.0.0/8 (IPv6 n'utilise qu'une seule adresse). |

Exemple link-local : PC1 (2001:DB8:0:1::/64) envoie à PC2 (2001:DB8:0:2::2) via R1 → next-hop FE80::3 (R2) → FE80::5 (R3) → FE80::7 (R4) → PC2. Entre les routeurs, seules des link-local : R1 ne pourrait pas pinger R3 à FE80::5 (paquet jeté, pas routé), mais comme next-hop elles conviennent parfaitement.

### 4. Adresses multicast à connaître

- Le dernier chiffre est identique en IPv4 et IPv6 : **all OSPF routers FF02::5 / 224.0.0.5** ; **all EIGRP routers FF02::A / 224.0.0.10** (A = 10) ; **all nodes FF02::1** ; **all routers FF02::2**. Le tableau de la vidéo (à mémoriser intégralement) comprend aussi RIP, valeurs non lues à l'oral.
- **Scopes** (portées), identifiés par le **4e caractère hexadécimal** :

| Scope | Préfixe | Portée |
| :--- | :--- | :--- |
| Interface-local (ou node-local) | **FF01** | Ne quitte pas l'équipement (service local). |
| Link-local | **FF02** | Reste dans le sous-réseau local, non routé. Concept distinct de l'adresse link-local FE80. |
| Site-local | **FF05** | Peut être transféré par les routeurs, limité à un site physique, pas sur le WAN ; frontières configurées par l'ingénieur. |
| Organization-local | **FF08** | Plus large : tous les sous-réseaux de l'organisation, y compris via WAN. |
| Global | **FF0E** | « Sans frontières », routable jusque sur l'Internet public. |

- `show ipv6 interface g0/0`, rubrique **joined group addresses** : R1 a rejoint automatiquement **FF02::1** (all nodes, il est hôte du sous-réseau), **FF02::2** (all routers) et une adresse spéciale vue au Day 33 (solicited-node).

### 5. Pièges d'examen

- `ipv6 enable` crée une adresse **link-local** (pas « EUI-64 » : c'est le procédé, pas le type). Une interface IPv6 a **toujours** une link-local en plus des autres adresses.
- Quiz Q3 : « message à tous les **routeurs** du sous-réseau » = **FF02::2** ; FF02::1 vise **tous les hôtes** ; FF01 ne sort pas de l'équipement.
- Unique local : le **global ID** = 40 bits (10 caractères hexa) après **FD**, à générer aléatoirement.
- Non routables : **FE80::/10** et les multicasts **FF02** ; les unique local (FC/FD) sont routables en interne, pas sur Internet ; les multicasts FF05 (site-local) peuvent être routés (bonus Boson).
- Unicast = un vers un ; broadcast = un vers tous ; multicast = un vers plusieurs ; anycast = un vers un parmi plusieurs.

### 6. Commandes IOS

```
R1(config-if)# ipv6 address 2001:db8::/64 eui-64      ! préfixe + identifiant d'interface généré depuis la MAC
R1(config-if)# ipv6 enable                              ! active IPv6 sans adresse : seule une link-local est créée
R1(config-if)# ipv6 address 2001:db8:1::1/128 anycast   ! adresse anycast (exemple de la vidéo : /128 avec le mot-clé anycast)
R1(config-if)# mac-address <mac>                        ! MAC administrée localement (LAA), mentionnée seulement
R1# show interfaces g0/1                                ! MAC de l'interface, pour calculer EUI-64
R1# show ipv6 interface brief                           ! adresses configurées + link-local
R1# show ipv6 interface g0/0                            ! détail : EUI/ANY, joined group addresses
R1(config)# ipv6 route 2001:db8:0:1::/64 g0/0 fe80::...   ! next-hop link-local : l'interface de sortie est obligatoire
```

### 7. Le lab (vidéo n°66)

Objectif : adresses EUI-64 sur G0/1 de R1 et R2, PC1 et PC2 avec gateway, `ipv6 enable` sur G0/0, routes statiques pour que PC1 pinge PC2.

1. **R1** : `show interfaces g0/1` pour lire la MAC ; calcul à la main (couper, FFFE, inversion du 7e bit : ici un **0 devient 2**) ; `ipv6 unicast-routing` ; `interface g0/1`, `ipv6 address 2001:db8::/64 eui-64`. `do show ipv6 interface brief` : l'adresse calculée, plus une link-local avec le **même identifiant EUI-64** et le préfixe FE80.
2. **R2** : même méthode, `ipv6 address 2001:db8:0:1::/64 eui-64`.
3. **PC** : copier l'adresse du routeur comme gateway ; PC2 = `2001:db8:0:1::2/64`, PC1 = `2001:db8::2/64`. Le PC a déjà une link-local dérivée de sa MAC.
4. **G0/0** de R1 et R2 : `ipv6 enable` → link-local seulement, identifiant différent de G0/1 (MAC différente).
5. **Routes** : sur R1, `ipv6 route 2001:db8:0:1::/64 <link-local de R2>` renvoie **« Interface has to be specified for a link-local nexthop »** : il faut `ipv6 route 2001:db8:0:1::/64 g0/0 <link-local de R2>` (interface **avant** le next-hop). Sur R2 : `ipv6 route 2001:db8::/64 g0/0 <link-local de R1>`.
6. Test : `ping 2001:db8:0:1::2` depuis PC1 réussit.

Bonus NetSim (Configuring IPv6 1) : `ipv6 unicast-routing` et adresses `2001:0:1:x::y/64` sur les liens WAN de Tampa, Orlando, Daytona, Miami ; **RIPng** (hors sujets CCNA) : `ipv6 router rip <nom>` en global, puis `ipv6 rip <nom> enable` sur chaque interface ; activer sur l'interface suffit, le processus est créé automatiquement. Vérification `show ipv6 protocols`, `show ipv6 route`. En RIPv4 il n'y a qu'un processus et on utilise `network` ; en RIPng on active par interface avec un nom de processus.

### 8. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| MAC `0D2A.4FA3.00B1`, commande `ipv6 address 2001:db8:0:1::/64 eui-64` : adresse obtenue ? | **D** : le 7e bit passe à 1, le **D devient F**, et **FFFE** est inséré au milieu (soit `2001:db8:0:1:f2a:4fff:fea3:b1`) | Les autres options n'inversent pas le 7e bit ou n'insèrent pas FFFE correctement. |
| Quelle partie de l'adresse unique local est le global ID ? | **B** : les **40 bits** (10 caractères) qui suivent **FD** | Le global ID doit être aléatoire pour éviter les chevauchements en cas de fusion. |
| R3 envoie un multicast à tous les autres **routeurs** du sous-réseau : adresse de destination ? | **FF02::2** | FF01::1 et FF01::2 sont interface-local (ne sortent pas de l'équipement) ; FF02::1 vise tous les hôtes, pas seulement les routeurs. |
| Type d'adresse créé automatiquement par `ipv6 enable` ? | **Link-local** | Unique local et node-local sont faux ; EUI-64 est le procédé de génération, pas un type. |
| Associer les schémas aux types de message | Unicast = 3, broadcast = 2, multicast = 4, **anycast = 1** | Un vers un ; un vers tous ; un vers plusieurs ; un vers un parmi plusieurs. |

Bonus Boson (non routables, deux réponses) : **FE80::/10** (link-local) et **FF02::/16** (multicast link-local). 2000::/3 est routable ; FC/FD routables en interne ; FF05 (site-local) peut être routé hors du sous-réseau.

---

## 🇬🇧 English version

### 1. Scope

Exam topic **1.9**: compare IPv6 address types: 1.9.a global unicast, 1.9.b unique local, 1.9.c link local, 1.9.d anycast, 1.9.e multicast, 1.9.f modified EUI-64. Very information-dense video: use the flashcards (Anki tag `ipv6` on Day 31 and 32 cards).

### 2. EUI-64 (Extended Unique Identifier, 1.9.f)

- Technically **modified EUI-64**, usually just EUI-64; for the CCNA they are the same. It is **not an address type** but a **method** of automatic generation: converting a **48-bit MAC** into a **64-bit interface identifier**, which becomes the host portion of a **/64** address.
- Three steps, to know by hand (the router does it automatically):
  1. **Split the MAC in half**: `1234 5678 90AB` → `123456` | `7890AB` (between the 6 and the 7).
  2. **Insert `FFFE` in the middle**: `1234 56FF FE78 90AB`.
  3. **Invert the 7th bit** (0 → 1, 1 → 0). Each hex digit = 4 bits: the `1` = bits 1 to 4, the `2` = bits 5 to 8, so the 7th bit is the **3rd bit of the `2`** (0010). It is a 1 → 0, the `2` becomes `0`: interface ID **1034:56FF:FE78:90AB**.
- Why invert the 7th bit (beyond the CCNA): it is the MAC's **U/L** (Universal/Local) bit. **UAA** (universally administered address, assigned by the manufacturer): U/L = 0; **LAA** (locally administered address, set by an admin or protocol, `mac-address` command on the interface): U/L = 1. In EUI-64 the meaning is **reversed**: 1 = made from a UAA, 0 = made from an LAA. No effect on how the address works.
- Configuration: `ipv6 address 2001:db8::/64 eui-64`; verify with `show interfaces` (MAC) then `show ipv6 interface brief`. In the video's example, EUI-64 changed a **C** of the MAC to an **E** and inserted FFFE in the middle.

### 3. Address types

| Type | Range | Characteristics |
| :--- | :--- | :--- |
| **Global unicast** (1.9.a) | Originally **2000::/3** (2000:: to 3FFF:FFFF:…); now every address not reserved for other purposes | **Public**, routable over the Internet, **registration required**, globally unique. Structure: **global routing prefix** (/48, assigned by the ISP) + **subnet identifier** (16 bits, over 65,000 subnets) + **interface identifier** (64 bits, EUI-64 or manual). |
| **Unique local** (1.9.b) | **FC00::/7**, but a later update requires the 8th bit set to 1: in practice **FD** | **Private**, not routable over the Internet (the ISP drops the packets), **no registration**, free to use internally. Structure: **FD** + **global ID** (40 bits, **randomly generated** to avoid overlapping subnets when companies merge) + subnet identifier (16 bits) + interface ID (64 bits). |
| **Link local** (1.9.c) | **FE80::/10**; the next 54 bits must be 0, so always **FE8** (never FE9, FEA, FEB) | **Automatically generated** on every IPv6-enabled interface (configured address or `ipv6 enable`), interface ID via **EUI-64**. Communication **within a single link/subnet**: routers **do not route** packets to a link-local destination. Uses: **OSPFv3** adjacencies, **static route next hops**, **NDP** (Neighbor Discovery Protocol, IPv6's replacement for ARP, Day 33). |
| **Multicast** (1.9.e) | **FF00::/8** | "One-to-many". **IPv6 has no broadcast**: the **all nodes / all hosts FF02::1** address serves that purpose. |
| **Anycast** (1.9.d) | **No dedicated range**: a regular unicast address (global unicast or unique local) specified as anycast | "One-to-one-of-many": several routers carry the same address, advertise it with a routing protocol, and traffic goes to the **nearest** one (lowest metric). Configured as **/128** (like an IPv4 /32) with the `anycast` keyword; `show ipv6 interface g0/0` lists it under *global unicast addresses* with **ANY** at the end (**EUI** for an EUI-64 address). |
| **Unspecified** | **::** (all 0s) | When a device does not know its address yet; IPv6 default route **::/0**. IPv4 equivalent: 0.0.0.0. |
| **Loopback** | **::1** (127 zeros then a 1) | Tests the local protocol stack, never sent to other devices. IPv4 equivalent: 127.0.0.0/8 (IPv6 uses a single address). |

Link-local example: PC1 (2001:DB8:0:1::/64) sends to PC2 (2001:DB8:0:2::2) via R1 → next hop FE80::3 (R2) → FE80::5 (R3) → FE80::7 (R4) → PC2. Between the routers only link-locals exist: R1 could not ping R3 at FE80::5 (dropped, not routed), but as next hops they work fine.

### 4. Multicast addresses to know

- The last digit is the same in IPv4 and IPv6: **all OSPF routers FF02::5 / 224.0.0.5**; **all EIGRP routers FF02::A / 224.0.0.10** (A = 10); **all nodes FF02::1**; **all routers FF02::2**. The video's chart (memorize all of it) also includes RIP, values not read aloud.
- **Scopes**, identified by the **4th hexadecimal character**:

| Scope | Prefix | Reach |
| :--- | :--- | :--- |
| Interface-local (or node-local) | **FF01** | Does not leave the device (local service). |
| Link-local | **FF02** | Stays in the local subnet, not routed. Different concept from the FE80 link-local address. |
| Site-local | **FF05** | Can be forwarded by routers, limited to one physical site, not over the WAN; boundaries configured by the engineer. |
| Organization-local | **FF08** | Wider: all subnets in the organization, including over WAN links. |
| Global | **FF0E** | "No boundaries", routable even over the public Internet. |

- `show ipv6 interface g0/0`, **joined group addresses**: R1 automatically joined **FF02::1** (all nodes, it is a host in the subnet), **FF02::2** (all routers) and a special address covered on Day 33 (solicited-node).

### 5. Exam traps

- `ipv6 enable` creates a **link-local** address (not "EUI-64": that is the process, not the type). An IPv6-enabled interface **always** has a link-local in addition to any other addresses.
- Quiz Q3: "message to all **routers** on the subnet" = **FF02::2**; FF02::1 targets **all hosts**; FF01 never leaves the device.
- Unique local: the **global ID** = 40 bits (10 hex characters) after **FD**, randomly generated.
- Not routable: **FE80::/10** and **FF02** multicasts; unique local (FC/FD) are routable internally, not over the Internet; FF05 (site-local) multicasts can be routed (Boson bonus).
- Unicast = one-to-one; broadcast = one-to-all; multicast = one-to-many; anycast = one-to-one-of-many.

### 6. IOS commands

```
R1(config-if)# ipv6 address 2001:db8::/64 eui-64      ! prefix + interface ID generated from the MAC
R1(config-if)# ipv6 enable                              ! enables IPv6 without an address: only a link-local is created
R1(config-if)# ipv6 address 2001:db8:1::1/128 anycast   ! anycast address (video example: /128 with the anycast keyword)
R1(config-if)# mac-address <mac>                        ! locally administered MAC (LAA), only mentioned
R1# show interfaces g0/1                                ! interface MAC, to compute EUI-64
R1# show ipv6 interface brief                           ! configured addresses + link-local
R1# show ipv6 interface g0/0                            ! details: EUI/ANY, joined group addresses
R1(config)# ipv6 route 2001:db8:0:1::/64 g0/0 fe80::...   ! link-local next hop: the exit interface is required
```

### 7. The lab (video 66)

Goal: EUI-64 addresses on G0/1 of R1 and R2, PC1 and PC2 with gateways, `ipv6 enable` on G0/0, static routes so PC1 can ping PC2.

1. **R1**: `show interfaces g0/1` to read the MAC; compute by hand (split, FFFE, invert the 7th bit: here a **0 becomes 2**); `ipv6 unicast-routing`; `interface g0/1`, `ipv6 address 2001:db8::/64 eui-64`. `do show ipv6 interface brief`: the computed address, plus a link-local with the **same EUI-64 interface ID** and the FE80 prefix.
2. **R2**: same method, `ipv6 address 2001:db8:0:1::/64 eui-64`.
3. **PCs**: paste the router's address as gateway; PC2 = `2001:db8:0:1::2/64`, PC1 = `2001:db8::2/64`. The PC already has a link-local based on its MAC.
4. **G0/0** on R1 and R2: `ipv6 enable` → link-local only, interface ID different from G0/1 (different MAC).
5. **Routes**: on R1, `ipv6 route 2001:db8:0:1::/64 <R2 link-local>` returns **"Interface has to be specified for a link-local nexthop"**: use `ipv6 route 2001:db8:0:1::/64 g0/0 <R2 link-local>` (interface **before** the next hop). On R2: `ipv6 route 2001:db8::/64 g0/0 <R1 link-local>`.
6. Test: `ping 2001:db8:0:1::2` from PC1 succeeds.

NetSim bonus (Configuring IPv6 1): `ipv6 unicast-routing` and `2001:0:1:x::y/64` addresses on the WAN links of Tampa, Orlando, Daytona, Miami; **RIPng** (not a CCNA topic): `ipv6 router rip <name>` globally, then `ipv6 rip <name> enable` on each interface; enabling on the interface is enough, the process is created automatically. Verify with `show ipv6 protocols`, `show ipv6 route`. In IPv4 RIP there is one process and the `network` command; in RIPng you enable per interface with a process name.

### 8. The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| MAC `0D2A.4FA3.00B1`, command `ipv6 address 2001:db8:0:1::/64 eui-64`: resulting address? | **D**: the 7th bit is inverted to 1, the **D becomes F**, and **FFFE** is inserted in the middle (i.e. `2001:db8:0:1:f2a:4fff:fea3:b1`) | The other options do not invert the 7th bit or do not insert FFFE correctly. |
| Which portion of the unique local address is the global ID? | **B**: the **40 bits** (10 characters) after **FD** | The global ID should be random to avoid overlap when companies merge. |
| R3 sends a multicast to all other **routers** on the subnet: destination address? | **FF02::2** | FF01::1 and FF01::2 are interface-local (never leave the device); FF02::1 targets all hosts, not just routers. |
| Address type automatically configured by `ipv6 enable`? | **Link-local** | Unique local and node-local are wrong; EUI-64 is the generation process, not a type. |
| Match the diagrams with the message types | Unicast = 3, broadcast = 2, multicast = 4, **anycast = 1** | One-to-one; one-to-all; one-to-many; one-to-one-of-many. |

Boson bonus (not routable, select two): **FE80::/10** (link-local) and **FF02::/16** (link-local multicast). 2000::/3 is routable; FC/FD routable internally; FF05 (site-local) can be routed outside the subnet.
