# CCNA Day 3 : How the TCP/IP Model Actually Works / Le modèle TCP/IP

> Source : Jeremy's IT Lab, « How the TCP/IP Model Actually Works | CCNA Day 3 » (43 min), vidéo n°6 de la playlist (cours, version récente, **sans quiz de fin**) ; « OSI Model | Day 3 Lab » (8 min), vidéo n°7 (lab Packet Tracer, version ancienne basée sur le modèle OSI). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Protocoles et normes

- Un **protocole** (*protocol*) est un ensemble de règles définissant comment les données sont communiquées entre équipements : le « langage » des ordinateurs. Deux machines qui parlent des protocoles différents ne peuvent pas échanger.
- Au début, les protocoles étaient **propriétaires** (IBM, par exemple), donc incompatibles entre vendeurs. Aujourd'hui, les réseaux utilisent des protocoles **standard et neutres** (*vendor-neutral*).
- Une **norme** (*standard*) est une spécification convenue décrivant comment un protocole ou une technologie doit fonctionner. Un MacBook peut ainsi lire un site hébergé sur Linux, un PC Windows envoyer un e-mail lu sur Android.

### 2. Un peu d'histoire

- Années 1960, États-Unis : l'**ARPA** (Advanced Research Projects Agency, Département de la Défense) finance **ARPANET**, en ligne en **1969**, qui utilise le protocole **NCP** (Network Control Program). Pas de TCP/IP à l'origine.
- **1974** : **Vint Cerf et Bob Kahn** développent **TCP, Transmission Control *Program***, protocole d'interconnexion de réseaux. Après révisions, il est scindé en deux protocoles toujours utilisés : **TCP** (Transmission Control *Protocol*) et **IP** (Internet Protocol).
- ARPANET bascule entièrement sur TCP/IP le **1er janvier 1983**. TCP/IP s'impose face aux solutions propriétaires car il est publié en **normes ouvertes** que tout vendeur peut implémenter et fonctionne sur de nombreux types de réseaux.

### 3. Qui définit les normes ?

- **IEEE** (Institute of Electrical and Electronics Engineers) : technologies de LAN, **Ethernet (802.3)** et **Wi-Fi (802.11)**. Spécifications physiques (câbles, fréquences radio, signaux) et format des messages.
- **IETF** (Internet Engineering Task Force) : communauté ouverte, protocoles de l'Internet (**TCP, IP, UDP, HTTP, DNS**). Publie ses normes dans des **RFC** (*Requests for Comments*), librement disponibles.
- IEEE et IETF créent les normes ; les vendeurs comme Cisco les implémentent.

### 4. Le modèle en couches

- Un réseau fait plusieurs métiers : transmission physique des signaux, livraison locale sur un LAN, routage entre réseaux, conversations de bout en bout, applications. Un **modèle** regroupe ces métiers en **couches** (*layers*). **Chaque couche utilise les services de la couche du dessous et sert la couche du dessus.**
- Un protocole vit « surtout » à une couche (les frontières sont parfois floues). IP, TCP, HTTP forment une **pile** (*stack*) de protocoles.
- Pile de la **RFC 791** (définit IP, 1981, toujours la norme actuelle) : **Application** (Telnet, FTP, TFTP), **Transport** (TCP, UDP), **Internet** (IPv4, IPv6 ; « internet » = *internetwork*, plusieurs réseaux reliés), **Lien** (*Link* : Ethernet, Wi-Fi). C'est **une** version du modèle TCP/IP, à 4 couches.
- **Le modèle est une description, pas une loi** : selon les livres, 4, 5 couches ou plus. Jeremy utilise un **modèle à 5 couches**.

### 5. L'analogie du courrier

Lettre à Bob, via le bureau de poste A puis B. Trois destinations différentes voyagent en même temps : la voiture va au bureau A, l'enveloppe à la maison de Bob, la lettre à Bob lui-même. Chaque camion a sa propre destination (prochain arrêt), l'enveloppe et la lettre gardent la leur.

| Couche de l'analogie | Rôle | Couche TCP/IP (Jeremy) |
| :--- | :--- | :--- |
| Contenu | le texte de la lettre | **Application** |
| Destinataire | « À : Bob », qui lit dans la maison | **Transport** |
| Adresse | la maison où livrer | **Internet** |
| Livraison locale | voiture/camion jusqu'au prochain arrêt | **Réseau local** (*Local Network*) |
| Infrastructure | routes, air, mer | **Physique** |

Les deux couches du bas travaillent toujours ensemble (route → camion, air → avion, mer → bateau) : on peut les fusionner ou les séparer, d'où les modèles à 4 ou 5 couches. **Chaque couche fait son travail sans changer celui des autres** : modifier le contenu ne change pas la livraison, et inversement.

### 6. Les cinq couches sur un vrai réseau

Réseau : PC1 — SW1 — R1 — R2 — SW2 — SRV1. PC1 (navigateur Chrome) veut une page web de SRV1, qui fait tourner un serveur web et un serveur de fichiers.

- **Couche 5, Application** (souvent appelée « couche 7 », explication plus bas) : protocoles entre processus applicatifs ; définit comment **formater, envoyer et interpréter** les données (HTTP/HTTPS pour le web, FTP/TFTP pour les fichiers, protocoles d'e-mail). Routeurs et switches ne regardent pas ce niveau ; seuls les hôtes communicants l'interprètent.
- **Couche 4, Transport** : communication **de bout en bout entre processus** (*process-to-process*, *service-to-service*) grâce aux **numéros de port** : **80** pour le serveur web, **21** pour le serveur de fichiers. Un « port » ici est un **numéro identifiant un processus**, pas un port physique. Tourne surtout sur les hôtes ; les routeurs travaillent normalement sur IP, pas sur la couche 4. Protocoles : **TCP** et **UDP**.
- **Couche 3, Internet** : livraison **de bout en bout entre hôtes** à travers plusieurs réseaux, grâce aux **adresses IP** (SRV1 : 10.1.1.1) et aux **routeurs**. Penser « adresses IP et routeurs ». Un **hôte** est tout équipement qui envoie et reçoit des données. Protocoles : **IPv4, IPv6, ICMP**.
- **Couche 2, Réseau local** : livraison **saut par saut** (*hop-to-hop*) sur un réseau local avec les **adresses MAC** et les **switches**. Un **saut** (*hop*) est une étape entre un routeur ou hôte et le suivant : PC1 → R1, R1 → R2, R2 → SRV1 = **3 sauts**. **Les switches ne comptent pas comme des sauts** : ils étendent le réseau local. Chaque interface a une MAC unique (R1 et R2 ont G1 et G2, GigabitEthernet à 1 Gbit/s). Protocoles : **Ethernet, Wi-Fi**.
- **Couche 1, Physique** : envoie les **bits** sous forme de signaux **électriques** (UTP cuivre), **optiques** (fibre) ou **radio** (Wi-Fi). Définit câbles, connecteurs, niveaux de signal, débits ; cartes réseau (**NIC**). Ingénierie complexe que l'ingénieur réseau n'a pas à maîtriser.

### 7. Encapsulation et décapsulation

- **Encapsulation** (émetteur, du haut vers le bas) : l'application prépare les données (requête HTTP) ; la couche 4 ajoute son **en-tête** (ports source et destination) ; la couche 3 ajoute le sien (IP source et destination) ; la couche 2 ajoute **un en-tête et une remorque** (*trailer*, utilisée par le récepteur pour détecter les erreurs de transmission) ; la couche 1 transmet les bits. L'en-tête de couche 2 part en premier, la remorque en dernier.
- **Décapsulation** (récepteur, du bas vers le haut) : couche 1 passe les bits ; chaque couche examine puis retire son en-tête (et remorque) jusqu'à livrer les données à l'application. La réponse refait le chemin inverse. **Chaque équipement a sa propre pile.**

### 8. Noms des PDU et charge utile

| Couche | PDU (*Protocol Data Unit*) | Nom |
| :--- | :--- | :--- |
| 4 | L4PDU | **segment** (TCP) ou **datagramme** (UDP) |
| 3 | L3PDU | **paquet** (*packet*) |
| 2 | L2PDU | **trame** (*frame*), la seule chose réellement envoyée sur le câble |

- **TCP crée des segments, UDP des datagrammes.** « Paquet » est le mot courant, mais désigne strictement le message à la couche 3.
- **Charge utile** (*payload*) : tout ce qui est encapsulé par l'en-tête (et la remorque) d'une couche, sans cet en-tête. Payload du segment = données applicatives ; du paquet = segment/datagramme ; de la trame = paquet.

### 9. Interactions entre couches et modularité

- **Interaction entre couches adjacentes** (*adjacent-layer interaction*) : chaque couche sert celle du dessus et s'appuie sur celle du dessous (couche 4 livre au bon processus via les ports ; 3 au bon hôte via IP ; 2 au prochain saut via MAC ; 1 transmet les bits).
- **Interaction de même couche** (*same-layer interaction*) : chaque couche dialogue avec son homologue sur l'autre équipement (segment adressé au port, paquet à l'IP de destination, trame à la MAC du prochain saut, signal reçu par le port physique d'en face).
- Les couches sont **modulaires** : HTTP sur TCP peut devenir TFTP sur UDP sans toucher IP et Ethernet ; Ethernet peut devenir Wi-Fi (couches 1 et 2) sans toucher les couches hautes. Tant que chaque couche respecte son « contrat », on remplace un protocole sans tout redessiner.

### 10. Le modèle OSI et les noms courants

- Fin des années 1970 et années 1980, l'**ISO** (International Organization for Standardization) conçoit **OSI** (*Open Systems Interconnection*), **7 couches** : **Application, Présentation, Session, Transport, Réseau, Liaison de données, Physique**, avec sa propre suite de protocoles, promue par les gouvernements (dont les États-Unis).
- Trop tardif, trop complexe, démarche descendante par comités : **TCP/IP a gagné**. OSI survit comme **modèle de référence et d'enseignement**.
- La plupart des ressources utilisent un **modèle à 5 couches avec les noms OSI** : couche **3 = Network** (Réseau), couche **2 = Data Link** (Liaison de données), et la couche Application est dite **couche 7** (son numéro OSI). Jeremy recommande son modèle, mais en pratique on dit juste « couche 2 », « couche 3 ». **Les noms de couches ne sont pas demandés à l'examen CCNA.**

### 11. Pièges d'examen

- « Port » de couche 4 = **numéro de processus**, rien à voir avec un port physique.
- **Les switches ne sont pas des sauts** ; seuls routeurs et hôtes comptent.
- **Segment = TCP, datagramme = UDP** ; ne jamais voir un paquet ou un segment « sur le câble » : seule la **trame** y circule.
- Le payload exclut l'en-tête de la couche considérée.
- Couche 2 = seule couche avec **en-tête et remorque**.
- Couche Application = « couche 7 » dans l'usage courant, même dans un modèle à 5 couches.
- Les routeurs travaillent sur la **couche 3**, pas sur les ports (sauf exceptions vues plus tard).

### 12. Le lab (Day 3 Lab, « OSI Model »)

**Objectif :** observer les couches en action avec le **mode simulation** de Packet Tracer (bouton en bas à droite). Ce lab, plus ancien, utilise les **7 couches OSI**.

- **Lire le schéma** : R1, R2, SW1, SW2, SRV1, PC1. **G0/0** = GigabitEthernet (1 Gbit/s ; aussi écrit Gi ou Gig), **F0/1** = FastEthernet (100 Mbit/s ; aussi Fa). Deux réseaux (*subnets*) : **192.168.1.0/24** (SRV1 en .100, PC1, SW1, SW2, R1 G0/0 en .1) et **10.0.0.0/24** (R1 G0/1 en .1, R2 G0/0 en .2). Les routeurs relient des réseaux différents ; IP et /24 expliqués dans une vidéo à venir.
- **STP** émis par SW2 (Spanning Tree Protocol, couche 2) : informations aux **couches 2 et 1 seulement**. En-tête « Layer 2: IEEE 802.3 header » (802.3 = Ethernet) ; le détail dit « the device encapsulates the PDU into an Ethernet frame » ; la couche 1 indique **les interfaces de sortie** (les ports physiques sont une information de couche 1).
- **OSPF** émis par R1 (couche 3, découverte des meilleurs chemins) : couches **3, 2 et 1** ; l'en-tête 3 porte **IP source et destination**.
- **DHCP** sur PC1 (couche 7, attribution automatique d'adresse) : Desktop > Command Prompt (fonctionne comme un invite Windows).

```text
PC> ipconfig              ! affiche l'adresse IP actuelle
PC> ipconfig /release     ! libère l'adresse (génère un message DHCP)
PC> ipconfig /renew       ! redemande une adresse
```

- Le message DHCP montre les couches **jusqu'à 7, sauf 5 et 6** : dans le modèle TCP/IP réellement utilisé, **5, 6 et 7 sont fusionnées en une seule couche Application**. En couche 4, Packet Tracer indique « encapsulates the PDU into a UDP segment » (le cours de la vidéo n°6 appelle « datagramme » le PDU d'UDP).
- Le bouton **Play** fait défiler lentement tous les messages du réseau.

### 13. Le quiz

**Pas de quiz** dans cette version de la vidéo du Day 3 : elle se termine par une récapitulation des points à retenir (modèle à 5 couches et noms OSI, encapsulation/décapsulation, noms des PDU, interactions adjacentes et de même couche).

---

## 🇬🇧 English version

### 1. Protocols and standards

- A **protocol** is a set of rules defining how data should be communicated between devices: the "language" computers use. Machines speaking different protocols cannot exchange data.
- Early protocols were **proprietary** (IBM, for instance), so different vendors' products could hardly talk. Today's networks use **standard, vendor-neutral** protocols.
- A **standard** is an agreed-upon specification describing how a protocol or technology should work. A MacBook can read a site hosted on Linux; a Windows PC can send an email read on Android.

### 2. A bit of history

- 1960s, USA: **ARPA** (Advanced Research Projects Agency, Department of Defense) funds **ARPANET**, online in **1969**, using **NCP** (Network Control Program). No TCP/IP at first.
- **1974**: **Vint Cerf and Bob Kahn** develop **TCP, Transmission Control *Program***, an internetworking protocol. After revisions it is split into two protocols still used today: **TCP** (Transmission Control *Protocol*) and **IP** (Internet Protocol).
- ARPANET fully switches to TCP/IP on **January 1st, 1983**. TCP/IP beat proprietary solutions because it was published as **open standards** any vendor could implement and ran over many network types.

### 3. Who defines the standards?

- **IEEE** (Institute of Electrical and Electronics Engineers): LAN technologies, **Ethernet (802.3)** and **Wi-Fi (802.11)**. Physical specs (cable types, radio frequencies, signalling) and message formats.
- **IETF** (Internet Engineering Task Force): an open community defining Internet protocols (**TCP, IP, UDP, HTTP, DNS**). Publishes its standards as **RFCs** (*Requests for Comments*), freely available.
- IEEE and IETF create the standards; vendors like Cisco implement them.

### 4. The layered model

- Networks do many jobs: physical transmission of signals, local delivery on a LAN, routing between networks, end-to-end conversations, the applications themselves. A **model** groups related jobs into **layers**. **Each layer uses the services of the layer below and provides services to the layer above.**
- Protocols live "mostly" at one layer (lines are sometimes blurred). IP, TCP and HTTP form a protocol **stack**.
- The stack in **RFC 791** (defines IP, 1981, still the current standard): **Application** (Telnet, FTP, TFTP), **Transport** (TCP, UDP), **Internet** (IPv4, IPv6; "internet" means *internetwork*, multiple networks connected), **Link** (Ethernet, Wi-Fi). That is **one** version of the TCP/IP model, with 4 layers.
- **The model is a description, not a law**: books use 4, 5 or more layers. Jeremy uses a **five-layer model**.

### 5. The mail analogy

A letter to Bob via post office A then B. Three destinations travel at once: the car goes to post office A, the envelope to Bob's house, the letter to Bob himself. Each truck has its own destination (the next stop); the envelope and letter keep theirs.

| Analogy layer | Role | TCP/IP layer (Jeremy) |
| :--- | :--- | :--- |
| Content | the text of the letter | **Application** |
| Recipient | "To: Bob", who reads it inside the house | **Transport** |
| Address | the house to deliver to | **Internet** |
| Local delivery | car/truck to the next stop | **Local Network** |
| Infrastructure | roads, air, sea | **Physical** |

The bottom two always work together (road → truck, air → plane, sea → ship): merge them or split them, hence 4- or 5-layer models. **Each layer does its own job without changing the others'**: changing the content does not change the delivery steps, and vice versa.

### 6. The five layers on a real network

Network: PC1 — SW1 — R1 — R2 — SW2 — SRV1. PC1 (Chrome) wants a web page from SRV1, which runs a web server and a file server.

- **Layer 5, Application** (usually called "Layer 7", see below): protocols between application processes; defines how to **format, send and interpret** data (HTTP/HTTPS for the web, FTP/TFTP for files, email protocols). Routers and switches ignore this level; only the communicating hosts interpret it.
- **Layer 4, Transport**: **end-to-end communication between processes** (*process-to-process*, *service-to-service*) using **port numbers**: **80** for the web server, **21** for the file server. A "port" here is a **number identifying a process**, not a physical port. Runs mainly on the hosts; routers normally work on IP, not Layer 4. Protocols: **TCP** and **UDP**.
- **Layer 3, Internet**: **end-to-end delivery between hosts** across multiple networks, using **IP addresses** (SRV1: 10.1.1.1) and **routers**. Think "IP addresses and routers". A **host** is any device that sends and receives data. Protocols: **IPv4, IPv6, ICMP**.
- **Layer 2, Local Network**: **hop-to-hop delivery** within a local network using **MAC addresses** and **switches**. A **hop** is one step from one router or host to the next: PC1 → R1, R1 → R2, R2 → SRV1 = **3 hops**. **Switches do not count as hops**: they just extend the local network. Each interface has a unique MAC (R1 and R2 have G1 and G2, GigabitEthernet at 1 Gbps). Protocols: **Ethernet, Wi-Fi**.
- **Layer 1, Physical**: sends **bits** as **electrical** (copper UTP), **optical** (fiber) or **radio** (Wi-Fi) signals. Defines cables, connectors, signal levels, link speeds; network interface cards (**NICs**). Complex engineering network engineers need not master.

### 7. Encapsulation and decapsulation

- **Encapsulation** (sender, top down): the application prepares the data (an HTTP request); Layer 4 adds its **header** (source and destination ports); Layer 3 adds its header (source and destination IPs); Layer 2 adds **a header and a trailer** (the trailer lets the receiver check for transmission errors); Layer 1 transmits the bits. The Layer 2 header is sent first, the trailer last.
- **Decapsulation** (receiver, bottom up): Layer 1 passes the bits up; each layer examines then removes its header (and trailer) until the data reaches the application. The reply does the same in reverse. **Each device has its own stack.**

### 8. PDU names and payload

| Layer | PDU (*Protocol Data Unit*) | Name |
| :--- | :--- | :--- |
| 4 | L4PDU | **segment** (TCP) or **datagram** (UDP) |
| 3 | L3PDU | **packet** |
| 2 | L2PDU | **frame**, the only thing actually sent over the wire |

- **TCP creates segments, UDP creates datagrams.** "Packet" is the everyday word, but strictly refers to the Layer 3 stage.
- **Payload**: everything encapsulated by a layer's header (and trailer), not including that header. A segment's payload = application data; a packet's = segment/datagram; a frame's = packet.

### 9. Layer interaction and modularity

- **Adjacent-layer interaction**: each layer serves the one above and relies on the one below (Layer 4 delivers to the right process via ports; 3 to the right host via IP; 2 to the next hop via MAC; 1 sends the bits).
- **Same-layer interaction**: each layer talks to its counterpart on the other device (segment addressed to a port, packet to the destination IP, frame to the next hop's MAC, signal received by the physical port on the other side).
- Layers are **modular**: HTTP over TCP can become TFTP over UDP without touching IP and Ethernet; Ethernet can become Wi-Fi (Layers 1 and 2) without affecting the upper layers. As long as each layer keeps its "contract", protocols can be replaced without redesigning everything.

### 10. The OSI model and the common names

- Late 1970s and 1980s, the **ISO** (International Organization for Standardization) designs **OSI** (*Open Systems Interconnection*), **7 layers**: **Application, Presentation, Session, Transport, Network, Data Link, Physical**, with a matching protocol suite promoted by governments (including the US).
- Developed too late, too complex, top-down by committees: **TCP/IP won**. OSI survives as a **reference and teaching model**.
- Most resources use a **5-layer model with OSI names**: Layer **3 = Network**, Layer **2 = Data Link**, and the Application layer is called **Layer 7** (its OSI number). Jeremy prefers his own names, but in practice people just say "Layer 2", "Layer 3". **Layer names are not quizzed on the CCNA exam.**

### 11. Exam traps

- A Layer 4 "port" is a **process number**, nothing to do with a physical port.
- **Switches are not hops**; only routers and hosts count.
- **Segment = TCP, datagram = UDP**; you never see a packet or segment "on the wire": only the **frame** travels there.
- The payload excludes the header of the layer in question.
- Layer 2 is the only layer with **both a header and a trailer**.
- The Application layer is "Layer 7" in common usage, even in a 5-layer model.
- Routers work at **Layer 3**, not on ports (exceptions come later).

### 12. The lab (Day 3 Lab, "OSI Model")

**Goal:** watch the layers at work in Packet Tracer's **simulation mode** (button bottom right). This older lab uses the **7 OSI layers**.

- **Reading the diagram**: R1, R2, SW1, SW2, SRV1, PC1. **G0/0** = GigabitEthernet (1 Gbps; also written Gi or Gig), **F0/1** = FastEthernet (100 Mbps; also Fa). Two networks (*subnets*): **192.168.1.0/24** (SRV1 at .100, PC1, SW1, SW2, R1 G0/0 at .1) and **10.0.0.0/24** (R1 G0/1 at .1, R2 G0/0 at .2). Routers connect different networks; IP and /24 explained in a coming video.
- **STP** sent by SW2 (Spanning Tree Protocol, Layer 2): information at **Layers 2 and 1 only**. Header "Layer 2: IEEE 802.3 header" (802.3 = Ethernet); the detail says "the device encapsulates the PDU into an Ethernet frame"; Layer 1 lists **the outgoing interfaces** (physical ports are Layer 1 information).
- **OSPF** sent by R1 (Layer 3, finds the best paths): Layers **3, 2 and 1**; the Layer 3 header carries **source and destination IP**.
- **DHCP** on PC1 (Layer 7, automatic IP assignment): Desktop > Command Prompt (works like a Windows prompt).

```text
PC> ipconfig              ! shows the current IP address
PC> ipconfig /release     ! releases the address (generates a DHCP message)
PC> ipconfig /renew       ! requests an address again
```

- The DHCP message shows layers **up to 7, except 5 and 6**: in the TCP/IP model actually in use, **5, 6 and 7 are combined into a single Application layer**. At Layer 4, Packet Tracer says "encapsulates the PDU into a UDP segment" (the lecture in video no. 6 calls UDP's PDU a datagram).
- The **Play** button slowly steps through every message on the network.

### 13. The quiz

**No quiz** in this version of the Day 3 video: it ends with a review of what to focus on (5-layer model and OSI names, encapsulation/decapsulation, PDU names, adjacent-layer and same-layer interaction).
