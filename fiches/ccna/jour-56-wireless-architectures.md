# CCNA Day 56 : Wireless Architectures / Architectures sans fil

> Source : Jeremy's IT Lab, « Free CCNA | Wireless Architectures | Day 56 » (38 min), vidéo n°114 de la playlist. Pas de lab pour ce jour. Fiche rédigée à partir de la transcription le 6 octobre 2026. Sujets d'examen : 1.1.d (access points), 1.1.e (controllers), 2.6, 2.7, 2.8.

## 🇫🇷 Version française

### 1. Le format de trame 802.11

Plus complexe qu'une trame 802.3 ; vue d'ensemble seulement. Selon la version 802.11 et le type de message, **certains champs peuvent être absents**.

- **Frame Control** (2 octets, 16 bits) : type et sous-type du message.
- **Duration/ID** (2 octets) : selon le type de message, soit le **temps en microsecondes** pendant lequel le canal est réservé à la transmission, soit un **identifiant de l'association** client-AP. Comparable au champ Type/Length d'Ethernet (deux usages).
- **Jusqu'à quatre adresses**, présence et ordre selon le type de message : **DA** (*Destination Address*, destinataire final), **SA** (*Source Address*, émetteur d'origine), **RA** (*Receiver Address*, destinataire immédiat), **TA** (*Transmitter Address*, émetteur immédiat).
- **Sequence Control** : réassemblage des fragments et élimination des doublons.
- **QoS Control** : priorisation du trafic.
- **HT Control** (*High Throughput*) : ajouté dans **802.11n**. 802.11n (Wi-Fi 4) = **High Throughput**, 802.11ac (Wi-Fi 5) = **Very High Throughput (VHT)**.
- **Frame Body** : le paquet encapsulé. **FCS** (*Frame Check Sequence*) en remorque, contrôle d'erreurs comme en Ethernet.

### 2. Le processus d'association

Trois **états de connexion** : 1) ni authentifié ni associé ; 2) **authentifié mais pas associé** ; 3) **authentifié et associé** (seul état permettant d'envoyer du trafic via l'AP).

- Découverte : **scan actif** (la station envoie des **probe requests** et attend un **probe response**) ou **scan passif** (elle écoute les **beacons** envoyés périodiquement par l'AP pour annoncer le BSS).
- Puis **échange d'authentification** (mot de passe par exemple) → état 2. Puis **association request / response** → état 3.

### 3. Les trois types de messages 802.11

- **Management** : gestion du BSS. **Beacon, probe, authentication, association** (il y en a d'autres).
- **Control** : contrôle de l'accès au support radio, aide à la livraison des trames de gestion et de données. **RTS, CTS, ACK**.
- **Data** : les paquets de données proprement dits.

### 4. Les architectures d'AP

**AP autonomes (*autonomous*)**

- Systèmes autonomes, **sans WLC** (*Wireless LAN Controller*), **configurés individuellement** : câble console, Telnet/SSH, ou GUI web HTTP/HTTPS. Il faut leur configurer une adresse IP de gestion.
- Paramètres RF (puissance d'émission, canal), politiques de sécurité (ACL), QoS : tout **manuel, par AP**. **Aucune supervision ni gestion centralisée.**
- Chaque AP se connecte au réseau filaire par un **trunk**, même avec un seul SSID : le trafic de gestion doit être dans un **VLAN séparé** (bonne pratique : VLAN et sous-réseau de gestion distincts). Exemple : VLAN 10 et 20 pour les clients, **VLAN 99** pour la gestion.
- Le trafic a un chemin **direct** vers le réseau filaire ou vers les clients du même AP (pas besoin de passer par le filaire).
- Inconvénient : chaque VLAN doit **s'étendre sur tout le LAN**, mauvaise pratique : **grands domaines de broadcast**, **STP désactive des liens** (perte de bande passante), **ajout/suppression de VLAN très laborieux** sur des dizaines de switches.
- Convient aux petits réseaux, pas aux réseaux moyens à grands (des milliers d'AP). Peuvent aussi fonctionner en **repeater, outdoor bridge, workgroup bridge**.

**AP légers (*lightweight*) et architecture split-MAC**

- Les fonctions sont **réparties entre l'AP et le WLC** : **split-MAC** (*split media access control*).
  - **AP léger** : opérations **temps réel** (émission/réception RF, chiffrement/déchiffrement, beacons et probes).
  - **WLC** : gestion RF, gestion de la sécurité et de la QoS, **authentification des clients**, **association et roaming**, et **configuration centralisée** des AP.
- Le WLC peut être dans le même sous-réseau/VLAN que les AP ou dans un autre.
- WLC et AP **s'authentifient mutuellement par certificats numériques X.509** (même norme que les sites web) : seuls les AP autorisés rejoignent le réseau.
- Protocole **CAPWAP** (*Control And Provisioning of Wireless Access Points*), basé sur l'ancien **LWAPP** (*Lightweight Access Point Protocol*). **Deux tunnels** entre chaque AP et le WLC :
  - **Tunnel de contrôle : UDP 5246**. Configuration et gestion des AP. **Chiffré par défaut.**
  - **Tunnel de données : UDP 5247**. **Tout le trafic des clients** passe par ce tunnel vers le WLC, même entre deux clients du même AP. **Non chiffré par défaut**, chiffrable avec **DTLS** (*Datagram Transport Layer Security*, TLS sur UDP alors que TLS classique utilise TCP).
- Conséquence : les AP légers se connectent à des **ports access** du switch (un trunk n'est pas nécessaire) ; c'est le **WLC** qui se connecte en **trunk** et fait la correspondance SSID ↔ VLAN, et qui forme la frontière entre filaire et sans-fil. L'architecture AP autonome est parfois appelée **local-MAC**.
- Trajet du trafic en split-MAC : client → AP → tunnel → WLC → passerelle par défaut. Même pour un hôte associé au même AP : tunnel vers le WLC puis retour.
- **Avantages** (à connaître, pas à mémoriser) : **scalabilité** (milliers d'AP), **attribution dynamique des canaux**, **puissance d'émission automatique**, **couverture auto-réparatrice** (*self-healing* : si un AP tombe, le WLC augmente la puissance des voisins), **roaming transparent**, **équilibrage de charge des clients** (association à l'AP le moins chargé), **gestion centralisée de la sécurité et de la QoS**.

**Modes des AP légers** (connaître le rôle de base de chacun)

- **Local** : mode par défaut, offre un ou plusieurs BSS.
- **FlexConnect** : offre des BSS **et** peut **commuter localement** le trafic entre filaire et sans-fil si les tunnels vers le WLC tombent.
- **Sniffer** : pas de BSS ; capture les trames 802.11 et les envoie à un logiciel comme **Wireshark**.
- **Monitor** : pas de BSS ; reçoit les trames 802.11 pour **détecter les appareils malveillants** (*rogue*) et peut envoyer des messages de **désauthentification**.
- **Rogue detector** : **n'utilise pas sa radio** ; écoute le réseau **filaire** (messages ARP) et corrèle avec la liste de MAC suspectes reçue du WLC.
- **SE-Connect** (*Spectrum Expert Connect*) : pas de BSS ; **analyse du spectre RF** sur tous les canaux, données envoyées à un logiciel comme Cisco Spectrum Expert pour trouver les sources d'interférence.
- **Bridge/Mesh** : pont dédié entre sites, éventuellement sur longue distance, ou maillage entre AP.
- **Flex+Bridge** : ajoute FlexConnect au mode bridge/mesh (commutation locale si le WLC est injoignable).

**AP cloud (*cloud-based*)**

- Entre l'autonome et le split-MAC : **AP autonomes gérés de façon centralisée dans le cloud**. Exemple : **Cisco Meraki** et son **dashboard** (site web) pour configurer les AP, superviser, générer des rapports ; il indique à chaque AP le canal et la puissance.
- **Seul le trafic de gestion/contrôle va vers le cloud** ; le **trafic de données** va **directement** au réseau filaire comme avec des AP autonomes.

### 5. Les modèles de déploiement du WLC (split-MAC uniquement)

| Modèle | Où est le WLC | AP pris en charge (environ) | Usage |
| :--- | :--- | :--- | :--- |
| **Unified** | Appareil matériel dédié, en un point central | **6000** (ajouter des WLC au-delà) | Grand campus d'entreprise |
| **Cloud-based** | **VM sur un serveur**, en général dans un **cloud privé** en datacenter | **3000** | ≠ architecture AP cloud : ici les AP sont des AP légers, « cloud » désigne l'emplacement du WLC |
| **Embedded** | **Intégré dans un switch** | **200** (ajouter des switches) | Petits campus |
| **Cisco Mobility Express** | **Intégré dans un AP** ; les autres AP (et l'AP lui-même, en interne) forment des tunnels CAPWAP vers lui | **100** | Petite agence |

### 6. Pièges d'examen

- **CAPWAP : contrôle UDP 5246 (chiffré par défaut), données UDP 5247 (non chiffré par défaut, DTLS en option).**
- AP autonome → **trunk** vers le switch ; AP léger → **port access**, c'est le **WLC** qui est en trunk.
- **Cloud-based AP** (Meraki, AP autonomes gérés dans le cloud) ≠ **cloud-based WLC** (WLC en VM, AP légers).
- Seuls **Local** et **FlexConnect** offrent un BSS aux clients.
- Beacon, probe, authentication, association = **management** ; RTS/CTS/ACK = **control**.

### 7. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Un probe request 802.11 est quel type de message ? | **Management** | Beacon, probe, authentication, association sont des trames de gestion. |
| Quels types d'AP sont gérés de façon centralisée ? (deux réponses) | **Lightweight** et **cloud-based** | Les AP légers sont gérés par un WLC, les AP cloud par un serveur cloud comme Cisco Meraki. Un AP autonome est géré individuellement. |
| Quel type d'AP utilise CAPWAP ? | **Lightweight** | CAPWAP relie les AP légers au WLC via deux tunnels, contrôle et données. |
| Quels modes d'AP léger offrent un BSS aux clients ? (deux réponses) | **Local** et **FlexConnect** | Local est le mode standard par défaut ; FlexConnect ajoute la commutation locale si les tunnels vers le WLC tombent. Les autres modes n'offrent pas de BSS. |
| Quel déploiement de WLC prend en charge le plus d'AP ? | **Unified** | Embedded ≈ 200, cloud-based ≈ 3000, Mobility Express ≈ 100, unified ≈ 6000. |

---

## 🇬🇧 English version

### 1. The 802.11 frame format

More complex than an 802.3 frame; high-level overview only. Depending on the 802.11 version and message type, **some fields may be absent**.

- **Frame Control** (2 bytes, 16 bits): message type and subtype.
- **Duration/ID** (2 bytes): depending on the message type, either the **time in microseconds** the channel is dedicated to the transmission, or an **identifier for the association** between client and AP. Similar to the Ethernet Type/Length field (two purposes).
- **Up to four addresses**, presence and order depending on the message type: **DA** (Destination Address, final recipient), **SA** (Source Address, original sender), **RA** (Receiver Address, immediate recipient), **TA** (Transmitter Address, immediate sender).
- **Sequence Control**: reassemble fragments and eliminate duplicates.
- **QoS Control**: traffic prioritization.
- **HT Control** (High Throughput): added in **802.11n**. 802.11n (Wi-Fi 4) = **High Throughput**, 802.11ac (Wi-Fi 5) = **Very High Throughput (VHT)**.
- **Frame Body**: the encapsulated packet. **FCS** (Frame Check Sequence) in the trailer, error checking as in Ethernet.

### 2. The association process

Three **connection states**: 1) not authenticated, not associated; 2) **authenticated but not associated**; 3) **authenticated and associated** (the only state in which the station can send traffic through the AP).

- Discovery: **active scanning** (the station sends **probe requests** and listens for a **probe response**) or **passive scanning** (it listens for **beacons** sent periodically by the AP to advertise the BSS).
- Then an **authentication exchange** (e.g. a password) → state 2. Then **association request / response** → state 3.

### 3. The three 802.11 message types

- **Management**: manage the BSS. **Beacon, probe, authentication, association** (there are more).
- **Control**: control access to the medium (RF), assist delivery of management and data frames. **RTS, CTS, ACK**.
- **Data**: the actual data packets.

### 4. AP architectures

**Autonomous APs**

- Self-contained, **no WLC** (Wireless LAN Controller), **configured individually**: console cable, Telnet/SSH, or HTTP/HTTPS web GUI. A management IP address must be configured.
- RF parameters (transmit power, channel), security policies (ACLs), QoS: all **manual, per AP**. **No central monitoring or management.**
- Each AP connects to the wired network with a **trunk**, even with a single SSID: management traffic should be in a **separate VLAN** (best practice: separate management subnet and VLAN). Example: VLANs 10 and 20 for clients, **VLAN 99** for management.
- Data traffic takes a **direct** path to the wired network or to clients on the same AP (no need to enter the wired network).
- Drawback: each VLAN must **stretch across the whole LAN**, a bad practice: **large broadcast domains**, **spanning tree disables links** (less total bandwidth), **adding/deleting VLANs is labor-intensive** across dozens of switches.
- Fine for small networks, not viable for medium to large ones (thousands of APs). Can also operate as **repeater, outdoor bridge, workgroup bridge**.

**Lightweight APs and split-MAC architecture**

- Functions are **split between the AP and the WLC**: **split-MAC** (split media access control).
  - **Lightweight AP**: **real-time** operations (RF transmit/receive, encryption/decryption, beacons and probes).
  - **WLC**: RF management, security and QoS management, **client authentication**, **association and roaming management**, and **central configuration** of the APs.
- The WLC can be in the same subnet/VLAN as the APs or a different one.
- WLC and APs **authenticate each other with X.509 digital certificates** (same standard as websites): only authorized APs join.
- **CAPWAP** protocol (Control And Provisioning of Wireless Access Points), based on the older **LWAPP** (Lightweight Access Point Protocol). **Two tunnels** between each AP and the WLC:
  - **Control tunnel: UDP 5246**. Configures and manages the APs. **Encrypted by default.**
  - **Data tunnel: UDP 5247**. **All client traffic** goes through this tunnel to the WLC, even between two clients on the same AP. **Not encrypted by default**, can be encrypted with **DTLS** (Datagram Transport Layer Security; TLS over UDP, whereas regular TLS uses TCP).
- Consequence: lightweight APs connect to switch **access ports** (a trunk is not needed); the **WLC** connects via a **trunk** and maps SSIDs to VLANs, forming the border between wired and wireless. The autonomous architecture is sometimes called **local-MAC**.
- Split-MAC traffic path: client → AP → tunnel → WLC → default gateway. Even for a host on the same AP: tunneled to the WLC, then back.
- **Benefits** (be aware, no need to memorize): **scalability** (thousands of APs), **dynamic channel assignment**, **automatic transmit power**, **self-healing coverage** (if an AP fails, the WLC raises nearby APs' power), **seamless roaming**, **client load balancing** (associate with the least-used AP), **central security and QoS management**.

**Lightweight AP modes** (know the basic purpose of each)

- **Local**: default mode, offers one or more BSSs.
- **FlexConnect**: offers BSSs **and** can **locally switch** traffic between wired and wireless if the tunnels to the WLC go down.
- **Sniffer**: no BSS; captures 802.11 frames and sends them to software such as **Wireshark**.
- **Monitor**: no BSS; receives 802.11 frames to **detect rogue devices** and can send **de-authentication** messages.
- **Rogue detector**: **does not use its radio**; listens to the **wired** network (ARP messages) and correlates with the suspected MAC list from the WLC.
- **SE-Connect** (Spectrum Expert Connect): no BSS; **RF spectrum analysis** on all channels, data sent to software such as Cisco Spectrum Expert to find interference sources.
- **Bridge/Mesh**: dedicated bridge between sites, possibly long distance, or a mesh between APs.
- **Flex+Bridge**: adds FlexConnect to bridge/mesh mode (local forwarding if the WLC is unreachable).

**Cloud-based APs**

- In between autonomous and split-MAC: **autonomous APs centrally managed in the cloud**. Example: **Cisco Meraki** and its **dashboard** (website) to configure APs, monitor, generate reports; it tells each AP which channel and transmit power to use.
- **Only management/control traffic goes to the cloud**; **data traffic** goes **directly** to the wired network, as with autonomous APs.

### 5. WLC deployment models (split-MAC only)

| Model | Where the WLC is | APs supported (about) | Use |
| :--- | :--- | :--- | :--- |
| **Unified** | Dedicated hardware appliance in a central location | **6000** (add WLCs beyond that) | Large enterprise campus |
| **Cloud-based** | **VM on a server**, usually in a **private cloud** in a data center | **3000** | ≠ cloud-based AP architecture: APs are lightweight here, "cloud" refers to where the WLC is |
| **Embedded** | **Integrated in a switch** | **200** (add switches) | Smaller campuses |
| **Cisco Mobility Express** | **Integrated within an AP**; the other APs (and the AP itself, internally) build CAPWAP tunnels to it | **100** | Small branch office |

### 6. Exam traps

- **CAPWAP: control UDP 5246 (encrypted by default), data UDP 5247 (not encrypted by default, DTLS optional).**
- Autonomous AP → **trunk** to the switch; lightweight AP → **access port**, the **WLC** is on the trunk.
- **Cloud-based AP** (Meraki, autonomous APs managed in the cloud) ≠ **cloud-based WLC** (WLC as a VM, lightweight APs).
- Only **Local** and **FlexConnect** offer a BSS to clients.
- Beacon, probe, authentication, association = **management**; RTS/CTS/ACK = **control**.

### 7. Quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| What kind of message is an 802.11 probe request? | **Management** | Beacon, probe, authentication, association are management frames. |
| Which AP types are centrally managed? (select two) | **Lightweight** and **cloud-based** | Lightweight APs are managed by a WLC, cloud-based APs by a cloud server such as Cisco Meraki. Autonomous APs are managed individually. |
| Which AP type uses CAPWAP? | **Lightweight** | CAPWAP connects lightweight APs to the WLC via two tunnels, control and data. |
| Which lightweight AP modes offer a BSS for clients? (select two) | **Local** and **FlexConnect** | Local is the default standard mode; FlexConnect adds local forwarding if the tunnels to the WLC go down. The other modes offer no BSS. |
| Which WLC deployment supports the most APs? | **Unified** | Embedded about 200, cloud-based about 3000, Mobility Express about 100, unified about 6000. |
