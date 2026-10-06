# CCNA Day 53 : WAN Architectures / Architectures WAN

> Source : Jeremy's IT Lab, « Free CCNA | WAN Architectures | Day 53 » (38 min, vidéo n°107 de la playlist, cours) et « Free CCNA | GRE Tunnels | Day 53 Lab » (22 min, vidéo n°108, lab). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

Sujets d'examen 1.2.d (WAN) et 5.5 (décrire les VPN d'accès distant et site à site). Le verbe est « décrire » : pas de configuration, seulement une compréhension de base. Point de vue de l'**entreprise cliente** d'un fournisseur de services, pas du fournisseur (voir CCNP Service Provider).

### 1. Qu'est-ce qu'un WAN ?

- **WAN** (*Wide Area Network*) : réseau qui s'étend sur une **grande zone géographique** (villes, pays) pour relier des **LAN géographiquement séparés** (bureaux de New York, Toronto, Londres).
- Internet peut être considéré comme un WAN, mais le terme désigne en général les **connexions privées** d'une entreprise entre ses bureaux, centres de données et sites. Sur des connexions publiques et partagées comme Internet, les **VPN** (*Virtual Private Networks*) créent des connexions privées.
- Beaucoup de technologies WAN selon les lieux ; une technologie **legacy** (ancienne, peu utilisée) dans un pays peut rester utilisée ailleurs.
- Exemple : centre de données central et bureaux A, B, C, chacun relié au centre par une **ligne louée** (*leased line*). Topologie **hub and spoke** (terme WAN pour l'étoile) : le centre de données est le **hub**, les bureaux sont les **spokes**. Avantage par rapport au maillage complet : **contrôle central** du trafic (un pare-feu au centre filtre tout le trafic inter-bureaux).
- Représentation plus exacte : chaque site se connecte à un **fournisseur de services** qui relie les sites. Lignes louées en **câbles série** (encapsulation couche 2 **HDLC ou PPP**, pas Ethernet) ; aujourd'hui les WAN **Ethernet sur fibre optique** sont de plus en plus courants (câbles bien plus longs que le cuivre UTP).
- Internet peut aussi servir de WAN, mais c'est un réseau public partagé : les sites montent des **VPN** : paquets **chiffrés** puis **encapsulés** dans un nouveau paquet.

### 2. Lignes louées (*leased lines*)

- Lien physique **dédié**, typiquement entre deux sites. Connexions **série** avec encapsulation **PPP ou HDLC**.
- Standards de débits différents selon les pays (tableau Wikipedia). Amérique du Nord : noms en **T** (**T1, T2, T3**) ; Europe et autres régions : noms en **E** (**E1, E2, E3**). Flashcards fournies pour ces six ; mémoriser le reste n'est probablement pas nécessaire. Quiz : **T1 = 1,544 Mbps**.
- Remplacées de plus en plus par l'Ethernet WAN : **coût plus élevé**, **délai d'installation plus long**, **débits plus faibles**.

### 3. MPLS (*Multi Protocol Label Switching*)

- Réseau MPLS du fournisseur = **infrastructure partagée** entre de nombreux clients (comme Internet), mais les **labels** permettent de créer des **VPN** en séparant le trafic des différents clients.
- Termes : **CE router** (*Customer Edge*, routeur du client connecté au fournisseur), **PE router** (*Provider Edge*, routeur du fournisseur connecté aux CE), **P router** (*Provider core*, cœur du fournisseur, pas connecté aux clients).
- Les PE **ajoutent un label** aux trames reçues des CE, placé **entre l'en-tête Ethernet (couche 2) et l'en-tête IP (couche 3)** : MPLS est parfois appelé protocole de **couche 2.5**. Les décisions de transmission dans le réseau du fournisseur sont prises **sur le label, pas sur l'IP de destination**. **Les CE ne font pas tourner MPLS** (seuls PE et P).
- **VPN MPLS de couche 3** : les CE et PE forment des **voisinages** (OSPF par exemple, ou autre protocole, ou routes statiques avec le PE en next hop). Le CE du bureau A apprend les routes du bureau B via le PE.
- **VPN MPLS de couche 2** : **pas de voisinage CE-PE** ; le réseau du fournisseur est **transparent** : tout se passe comme si les deux CE étaient **directement connectés** (interfaces WAN dans le même sous-réseau, voisinage OSPF direct entre CE). Le réseau fournisseur agit comme un **gros switch**.
- De nombreux types de connexion peuvent mener au réseau MPLS : fibre Ethernet, sans fil **4G/5G**, **CATV**, ligne louée série.

### 4. Accès à Internet

- Options : technologies WAN privées (lignes louées, VPN MPLS) vers l'infrastructure Internet du fournisseur ; **CATV** et **DSL** (grand public, utilisables par les entreprises) ; **Ethernet fibre optique** de plus en plus populaire.
- **DSL** (*Digital Subscriber Line*) : Internet sur les **lignes téléphoniques** déjà installées. Nécessite un **modem** (*modulator-demodulator*) qui convertit les données pour la ligne téléphonique ; séparé ou intégré au routeur domestique. Permet d'utiliser Internet et le téléphone en même temps.
- **Câble** (*cable Internet*) : Internet sur les lignes **CATV** (télévision par câble) déjà installées ; **modem câble** séparé ou intégré au routeur.
- **Redondance des connexions Internet** (essentiel pour beaucoup d'entreprises) :
  - **Single homed** : 1 connexion vers 1 ISP (comme à la maison, pas de redondance).
  - **Dual homed** : 2 connexions vers le **même** ISP.
  - **Multihomed** : 1 connexion vers chacun de **2 ISP**.
  - **Dual multihomed** : 2 connexions vers chacun de 2 ISP (redondance maximale, pas toujours justifiée par le coût).

### 5. VPN sur Internet

Les WAN privés (lignes louées, MPLS) séparent le trafic des clients (liens dédiés ou labels). Internet n'a **aucune sécurité intégrée** : on utilise des VPN. Deux types : **site à site avec IPsec** et **accès distant avec TLS**.

**VPN site à site (IPsec)**
- VPN entre **deux équipements** (routeurs ou pare-feu) pour relier deux sites via Internet. Un **tunnel** est créé en encapsulant le paquet IP d'origine avec un **en-tête VPN et un nouvel en-tête IP** ; avec IPsec, le paquet d'origine est **chiffré** avant encapsulation.
- Processus : le routeur combine le paquet d'origine et une **clé de session** (clé de chiffrement) dans une formule de chiffrement ; encapsule le paquet chiffré avec en-tête VPN + nouvel en-tête IP ; l'envoie à l'autre extrémité ; le routeur récepteur déchiffre et transmet à la destination.
- Le tunnel n'existe qu'entre les **deux extrémités** ; les autres hôtes des sites envoient leurs données **non chiffrées** à leur routeur.
- Limites d'IPsec : **pas de broadcast ni de multicast** (unicast seulement), donc **pas de protocole de routage** (OSPF) dans le tunnel ; solution : **GRE over IPsec**. Configurer un **maillage complet** de tunnels entre de nombreux sites est laborieux ; solution : **DMVPN**.
- **GRE** (*Generic Routing Encapsulation*) : crée des tunnels comme IPsec mais **ne chiffre pas** (pas sécurisé) ; encapsule une grande variété de protocoles de couche 3 ainsi que le **broadcast et le multicast**. **GRE over IPsec** : paquet d'origine + en-tête GRE + nouvel en-tête IP, puis ce paquet GRE est **chiffré** et encapsulé dans un en-tête IPsec + nouvel en-tête IP.
- **DMVPN** (*Dynamic Multipoint VPN*, Cisco) : les routeurs créent **dynamiquement un maillage complet** de tunnels IPsec sans configurer chaque tunnel. Étape 1 : tunnels IPsec vers un **hub**. Étape 2 : le hub donne à chaque routeur les informations pour former des tunnels avec les autres. **Simplicité du hub-and-spoke** (un seul tunnel à configurer par routeur) et **efficacité du spoke-to-spoke** (trafic direct sans passer par le hub). Certaines entreprises préfèrent tout faire passer par le hub pour un pare-feu central.

**VPN d'accès distant (TLS)**
- Permet aux **appareils finaux** (PC, téléphones) d'accéder aux ressources internes de l'entreprise de façon sécurisée via Internet. Utilise typiquement **TLS** (*Transport Layer Security*), qui sécurise aussi **HTTPS** ; anciennement **SSL** (*Secure Sockets Layer*, Netscape), renommé TLS lors de la standardisation par l'IETF.
- Un **logiciel client VPN** (par exemple **Cisco AnyConnect**) est installé sur l'appareil ; il forme un tunnel sécurisé vers un routeur ou pare-feu de l'entreprise agissant comme **serveur TLS**. Comme IPsec, TLS chiffre et ajoute des en-têtes.

**Comparaison**

| | Site à site | Accès distant |
| :--- | :--- | :--- |
| Protocole | **IPsec** | **TLS** |
| Sert | **Tous les hôtes** des sites reliés (un tunnel entre deux routeurs/pare-feu) | **Un seul appareil** (celui où le client est installé) |
| Usage | Connexion **permanente** de deux sites via Internet | Accès **à la demande** aux ressources de l'entreprise depuis un réseau non sécurisé |

### 6. Pièges d'examen

- **T1 = 1,544 Mbps**.
- Les routeurs **CE ne font pas tourner MPLS** ; PE et P oui.
- VPN MPLS de **couche 2** : les CE forment des voisinages OSPF **directement entre eux** ; en couche 3, le voisinage est **CE-PE**. Il n'existe pas de « VPN MPLS couche 2.5 » (2.5 ne désigne que la position du label).
- **DSL = lignes téléphoniques** ; câble = lignes CATV.
- **GRE** ajoute le multicast/broadcast à IPsec (GRE over IPsec) ; GRE seul n'est pas sécurisé.
- Single homed / dual homed / multihomed / dual multihomed.
- Site à site = IPsec ; accès distant = TLS.

### 7. Commandes IOS

```
R1(config)# interface tunnel 0                        ! interface virtuelle de tunnel (comme un loopback)
R1(config-if)# tunnel source g0/0/0                   ! interface physique source (vers le fournisseur)
R1(config-if)# tunnel destination 200.0.0.2           ! IP de l'interface WAN de l'autre extrémité
R1(config-if)# ip address 192.168.1.1 255.255.255.252 ! adresse de l'interface tunnel
R1(config)# ip route 0.0.0.0 0.0.0.0 100.0.0.1        ! route (ici par défaut) vers la destination du tunnel, sinon le tunnel reste down
R1(config)# router ospf 1
R1(config-router)# network 192.168.1.1 0.0.0.0 area 0 ! OSPF sur l'interface tunnel
R1(config-router)# network 10.0.1.1 0.0.0.0 area 0    ! OSPF sur le LAN
R1(config-router)# passive-interface g0/0             ! pas de voisin sur le LAN
R1# show ip interface brief                           ! Tunnel0 up/up ou up/down
R1# show ip route                                     ! route connectée du tunnel, routes OSPF via Tunnel0
```

### 8. Le lab : tunnel GRE

- **Topologie** : R1 (G0/0/0 100.0.0.2, LAN 10.0.1.0/24 sur G0/0) et R2 (G0/0/0 200.0.0.2, LAN 10.0.2.0/24) reliés via un réseau fournisseur ; PC1 et PC2 dans les LAN. Le tunnel GRE crée une **connexion directe virtuelle** ; le trafic traverse physiquement le fournisseur, encapsulé dans des en-têtes supplémentaires. GRE ne chiffre pas ; choisi pour sa simplicité, pour montrer comment fonctionne un tunnel.
- **R1** : `interface tunnel 0`, `tunnel source g0/0/0`, `tunnel destination 200.0.0.2`, `ip address 192.168.1.1 255.255.255.252`. `do show ip interface brief` : Tunnel0 **up/down**.
- **R2** : `interface tunnel 0`, `tunnel source g0/0/0`, `tunnel destination 100.0.0.2`, `ip address 192.168.1.2 255.255.255.252`. Toujours down. `do show ip route` : R2 n'a **aucune route vers 100.0.0.2**, la destination du tunnel : il ne peut pas le construire. `ip route 0.0.0.0 0.0.0.0 200.0.0.1` : le tunnel monte, route connectée du tunnel visible. `do ping 192.168.1.1` échoue encore : R1 n'a pas non plus de route vers 200.0.0.2.
- **R1** : `ip route 0.0.0.0 0.0.0.0 100.0.0.1` ; le tunnel monte ; `do ping 192.168.1.2` réussit (les premiers pings peuvent échouer, ARP lent dans Packet Tracer).
- **Mode simulation**, « Outbound PDU Details » du ping : message ICMP, en-tête IP source 192.168.1.1 destination 192.168.1.2 (interfaces tunnel), puis **en-tête GRE**, puis **en-tête IP externe** source 100.0.0.2 (G0/0/0 de R1) destination 200.0.0.2 (G0/0/0 de R2). Le paquet d'origine est transporté dans un en-tête IP supplémentaire à travers le fournisseur.
- **OSPF via le tunnel** : `ping 10.0.2.100` de PC1 échoue d'abord. R1 : `router ospf 1`, `network 192.168.1.1 0.0.0.0 area 0`, `network 10.0.1.1 0.0.0.0 area 0`, `passive-interface g0/0`. R2 : `router ospf 1`, `network 192.168.1.2 0.0.0.0 area 0`, `network 10.0.2.1 0.0.0.0 area 0`, `passive-interface g0/0`. R1 et R2 deviennent **voisins OSPF** ; `show ip route` : R2 apprend 10.0.1.0/24 **via Tunnel0**, R1 apprend 10.0.2.0/24 via Tunnel0. `ping 10.0.2.100` de PC1 fonctionne : R1 encapsule en GRE et envoie dans le tunnel. Hors programme CCNA, mais illustre les tunnels.

### 9. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quel standard de ligne louée fournit 1,544 Mbps ? | **B** : T1 | D'après le tableau des standards ; mémoriser tout le tableau n'est probablement pas nécessaire. |
| Avec un VPN MPLS, quel routeur ne fait PAS tourner MPLS ? | **C** : CE | PE et P font tourner MPLS ; le routeur du client (customer edge) n'en a pas besoin. |
| Quel type de VPN MPLS permet aux CE de former des voisinages OSPF directement entre eux ? | **A** : VPN MPLS de couche 2 | Il n'existe pas de VPN MPLS couche 2.5 ; en couche 3 les voisinages sont avec les PE. En couche 2 le réseau fournisseur est transparent, comme un switch entre les CE. |
| Quelle technologie d'accès Internet exploite les lignes téléphoniques déjà installées ? | **B** : DSL | Digital Subscriber Line ; permet Internet et téléphone en même temps, contrairement aux technologies précédentes sur ligne téléphonique. |
| Quel protocole combiné à IPsec permet de transporter du multicast dans le tunnel ? | **C** : GRE | GRE encapsule multicast et broadcast, mais ne chiffre pas ; le paquet GRE est chiffré et encapsulé par IPsec pour cumuler les avantages. |

---

## 🇬🇧 English version

Exam topics 1.2.d (WAN) and 5.5 (describe remote access and site-to-site VPNs). The verb is "describe": no configuration, just a basic understanding. Perspective of the **enterprise customer** of a service provider, not the provider (see CCNP Service Provider).

### 1. What is a WAN?

- **WAN** (Wide Area Network): a network extending over a **large geographic area** (cities, countries) to connect **geographically separate LANs** (offices in New York, Toronto, London).
- The Internet can be considered a WAN, but the term usually refers to an enterprise's **private connections** between its offices, data centers and sites. Over public, shared connections like the Internet, **VPNs** (Virtual Private Networks) create private connections.
- Many WAN technologies depending on location; a **legacy** technology (old, rarely used) in one country may still be used elsewhere.
- Example: a central data center and offices A, B, C, each connected to the data center by a **leased line**. **Hub and spoke** topology (the WAN term for a star): the data center is the **hub**, the offices are **spokes**. Advantage over full mesh: **central control** of traffic (a firewall at the data center filters all inter-office traffic).
- More accurate picture: each site connects to a **service provider** that connects the sites. Leased lines use **serial cables** (Layer 2 encapsulation **HDLC or PPP**, not Ethernet); today **Ethernet over fiber optic** WANs are more and more common (much longer cables than copper UTP).
- The Internet can also serve as a WAN, but it is a shared public network: sites set up **VPNs**: packets are **encrypted** then **encapsulated** in a new packet.

### 2. Leased lines

- A **dedicated** physical link, typically between two sites. **Serial** connections with **PPP or HDLC** encapsulation.
- Various standards with different speeds in different countries (Wikipedia chart). North America: names starting with **T** (**T1, T2, T3**); Europe and other regions: **E** (**E1, E2, E3**). Flashcards provided for these six; memorizing the rest is probably unnecessary. Quiz: **T1 = 1.544 Mbps**.
- Increasingly replaced by Ethernet WAN: **higher cost**, **longer installation lead time**, **slower speeds**.

### 3. MPLS (Multi Protocol Label Switching)

- The provider's MPLS network is **shared infrastructure** among many customers (like the Internet), but **labels** allow **VPNs** to be created by separating different customers' traffic.
- Terms: **CE router** (Customer Edge, the customer's router connected to the provider), **PE router** (Provider Edge, the provider's router connected to CEs), **P router** (Provider core, not connected to customers).
- PEs **add a label** to frames received from CEs, placed **between the Ethernet (Layer 2) header and the IP (Layer 3) header**: MPLS is sometimes called a **Layer 2.5** protocol. Forwarding decisions inside the provider network are made **on the label, not the destination IP**. **CE routers do not run MPLS** (only PE and P).
- **Layer 3 MPLS VPN**: CE and PE routers form **peerings** (OSPF for example, or another protocol, or static routes with the PE as next hop). Office A's CE learns office B's routes via the PE.
- **Layer 2 MPLS VPN**: **no CE-PE peering**; the provider network is **transparent**: as if the two CEs were **directly connected** (WAN interfaces in the same subnet, direct OSPF peering between CEs). The provider network acts like a **big switch**.
- Many connection types can reach the MPLS network: Ethernet fiber, **4G/5G** wireless, **CATV**, serial leased line.

### 4. Internet access

- Options: private WAN technologies (leased lines, MPLS VPNs) to the provider's Internet infrastructure; **CATV** and **DSL** (consumer technologies, also usable by enterprises); **fiber optic Ethernet** growing in popularity.
- **DSL** (Digital Subscriber Line): Internet over already-installed **phone lines**. Requires a **modem** (modulator-demodulator) converting data for the phone line; separate or built into the home router. Allows Internet and phone at the same time.
- **Cable Internet**: Internet over already-installed **CATV** (cable TV) lines; **cable modem** separate or built into the router.
- **Redundant Internet connections** (essential for many companies):
  - **Single homed**: 1 connection to 1 ISP (like a home connection, no redundancy).
  - **Dual homed**: 2 connections to the **same** ISP.
  - **Multihomed**: 1 connection to each of **2 ISPs**.
  - **Dual multihomed**: 2 connections to each of 2 ISPs (most redundancy, not always worth the cost).

### 5. Internet VPNs

Private WANs (leased lines, MPLS) separate customers' traffic (dedicated links or labels). The Internet has **no built-in security**: VPNs are used. Two kinds: **site-to-site with IPsec** and **remote-access with TLS**.

**Site-to-site VPN (IPsec)**
- A VPN between **two devices** (routers or firewalls) connecting two sites over the Internet. A **tunnel** is created by encapsulating the original IP packet with a **VPN header and a new IP header**; with IPsec, the original packet is **encrypted** before encapsulation.
- Process: the router combines the original packet and a **session key** (encryption key) in an encryption formula; encapsulates the encrypted packet with a VPN header + new IP header; sends it to the other end; the receiving router decrypts and forwards to the destination.
- The tunnel exists only between the **two endpoints**; other hosts in the sites send **unencrypted** data to their router.
- IPsec limitations: **no broadcast or multicast** (unicast only), so **no routing protocol** (OSPF) over the tunnel; solution: **GRE over IPsec**. Configuring a **full mesh** of tunnels between many sites is labor-intensive; solution: **DMVPN**.
- **GRE** (Generic Routing Encapsulation): creates tunnels like IPsec but **does not encrypt** (not secure); encapsulates a wide variety of Layer 3 protocols as well as **broadcast and multicast**. **GRE over IPsec**: original packet + GRE header + new IP header, then that GRE packet is **encrypted** and encapsulated in an IPsec header + new IP header.
- **DMVPN** (Dynamic Multipoint VPN, Cisco): routers **dynamically create a full mesh** of IPsec tunnels without configuring each one. Step 1: IPsec tunnels to a **hub**. Step 2: the hub gives each router the information to form tunnels with the others. **Hub-and-spoke configuration simplicity** (one tunnel to configure per router) and **spoke-to-spoke efficiency** (direct traffic without passing through the hub). Some companies prefer all traffic through the hub for a central firewall.

**Remote-access VPN (TLS)**
- Lets **end devices** (PCs, phones) securely access the company's internal resources over the Internet. Typically uses **TLS** (Transport Layer Security), which also secures **HTTPS**; formerly **SSL** (Secure Sockets Layer, Netscape), renamed TLS when standardized by the IETF.
- **VPN client software** (e.g. **Cisco AnyConnect**) is installed on the device; it forms a secure tunnel to a company router or firewall acting as a **TLS server**. Like IPsec, TLS encrypts and adds headers.

**Comparison**

| | Site-to-site | Remote-access |
| :--- | :--- | :--- |
| Protocol | **IPsec** | **TLS** |
| Serves | **All hosts** in the connected sites (one tunnel between two routers/firewalls) | **One device** (where the client is installed) |
| Use | **Permanent** connection of two sites over the Internet | **On-demand** access to company resources from an insecure network |

### 6. Exam traps

- **T1 = 1.544 Mbps**.
- **CE routers do not run MPLS**; PE and P do.
- **Layer 2** MPLS VPN: CEs form OSPF peerings **directly with each other**; in Layer 3, peerings are **CE-PE**. There is no "Layer 2.5 MPLS VPN" (2.5 only refers to the label's position).
- **DSL = phone lines**; cable = CATV lines.
- **GRE** adds multicast/broadcast to IPsec (GRE over IPsec); GRE alone is not secure.
- Single homed / dual homed / multihomed / dual multihomed.
- Site-to-site = IPsec; remote-access = TLS.

### 7. IOS commands

```
R1(config)# interface tunnel 0                        ! virtual tunnel interface (like a loopback)
R1(config-if)# tunnel source g0/0/0                   ! physical source interface (toward the provider)
R1(config-if)# tunnel destination 200.0.0.2           ! IP of the other end's WAN interface
R1(config-if)# ip address 192.168.1.1 255.255.255.252 ! tunnel interface address
R1(config)# ip route 0.0.0.0 0.0.0.0 100.0.0.1        ! route (default here) to the tunnel destination, else the tunnel stays down
R1(config)# router ospf 1
R1(config-router)# network 192.168.1.1 0.0.0.0 area 0 ! OSPF on the tunnel interface
R1(config-router)# network 10.0.1.1 0.0.0.0 area 0    ! OSPF on the LAN
R1(config-router)# passive-interface g0/0             ! no neighbors on the LAN
R1# show ip interface brief                           ! Tunnel0 up/up or up/down
R1# show ip route                                     ! tunnel connected route, OSPF routes via Tunnel0
```

### 8. The lab: GRE tunnel

- **Topology**: R1 (G0/0/0 100.0.0.2, LAN 10.0.1.0/24 on G0/0) and R2 (G0/0/0 200.0.0.2, LAN 10.0.2.0/24) connected through a provider network; PC1 and PC2 in the LANs. The GRE tunnel creates a **virtual direct connection**; traffic physically crosses the provider, encapsulated in extra headers. GRE does not encrypt; chosen for simplicity to show how tunnels work.
- **R1**: `interface tunnel 0`, `tunnel source g0/0/0`, `tunnel destination 200.0.0.2`, `ip address 192.168.1.1 255.255.255.252`. `do show ip interface brief`: Tunnel0 **up/down**.
- **R2**: `interface tunnel 0`, `tunnel source g0/0/0`, `tunnel destination 100.0.0.2`, `ip address 192.168.1.2 255.255.255.252`. Still down. `do show ip route`: R2 has **no route to 100.0.0.2**, the tunnel destination: it cannot build the tunnel. `ip route 0.0.0.0 0.0.0.0 200.0.0.1`: the tunnel comes up, connected tunnel route visible. `do ping 192.168.1.1` still fails: R1 has no route to 200.0.0.2 either.
- **R1**: `ip route 0.0.0.0 0.0.0.0 100.0.0.1`; the tunnel comes up; `do ping 192.168.1.2` succeeds (first pings may fail, ARP is slow in Packet Tracer).
- **Simulation mode**, "Outbound PDU Details" of the ping: ICMP message, IP header source 192.168.1.1 destination 192.168.1.2 (tunnel interfaces), then a **GRE header**, then an **outer IP header** source 100.0.0.2 (R1's G0/0/0) destination 200.0.0.2 (R2's G0/0/0). The original packet is transported in an additional IP header across the provider.
- **OSPF over the tunnel**: `ping 10.0.2.100` from PC1 fails at first. R1: `router ospf 1`, `network 192.168.1.1 0.0.0.0 area 0`, `network 10.0.1.1 0.0.0.0 area 0`, `passive-interface g0/0`. R2: `router ospf 1`, `network 192.168.1.2 0.0.0.0 area 0`, `network 10.0.2.1 0.0.0.0 area 0`, `passive-interface g0/0`. R1 and R2 become **OSPF neighbors**; `show ip route`: R2 learns 10.0.1.0/24 **via Tunnel0**, R1 learns 10.0.2.0/24 via Tunnel0. `ping 10.0.2.100` from PC1 works: R1 encapsulates with GRE and sends it over the tunnel. Not on the CCNA, but illustrates tunnels.

### 9. The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which leased line standard provides 1.544 Mbps? | **B**: T1 | From the standards chart; memorizing the whole chart is probably unnecessary. |
| With an MPLS VPN, which router does NOT run MPLS? | **C**: CE | PE and P routers run MPLS; the customer edge router does not need to. |
| Which MPLS VPN type lets CE routers form OSPF peerings directly with each other? | **A**: Layer 2 MPLS VPN | There is no Layer 2.5 MPLS VPN; in Layer 3 the peerings are with PE routers. In Layer 2 the provider network is transparent, like a switch between the CEs. |
| Which Internet access technology takes advantage of already-installed phone lines? | **B**: DSL | Digital Subscriber Line; allows Internet and phone at the same time, unlike earlier phone-line technologies. |
| Which protocol combined with IPsec allows multicast traffic in the tunnel? | **C**: GRE | GRE encapsulates multicast and broadcast but does not encrypt; the GRE packet is encrypted and encapsulated with IPsec to get both benefits. |
