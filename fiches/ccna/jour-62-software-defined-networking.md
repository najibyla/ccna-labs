# CCNA Day 62 : Software-Defined Networking / Réseau défini par logiciel

> Source : Jeremy's IT Lab, « Free CCNA | Software-Defined Networking | Day 62 » (28 min), vidéo n°123 de la playlist. Pas de lab pour ce jour. Fiche rédigée à partir de la transcription le 6 octobre 2026. Sujets d'examen : 6.3 et 6.4.

## 🇫🇷 Version française

### 1. Rappel SDN et les trois couches de l'architecture

- Le **SDN** centralise le plan de contrôle dans une application, le **contrôleur**. Plan de contrôle traditionnel = **distribué** (chaque équipement a le sien, OSPF, ACL…). Le contrôleur centralise des fonctions comme le **calcul des routes** ; les équipements partagent leurs informations avec lui au lieu d'utiliser OSPF entre eux. Selon la solution, tout ou partie du plan de contrôle est centralisé. Le contrôleur agit sur les équipements par la **SBI** (API) ; les scripts et applications agissent sur le contrôleur par la **NBI**.
- Les trois **couches** (*layers*) de l'architecture SDN (rien à voir avec les couches OSI) :
  - **Application layer** : scripts et applications qui indiquent au contrôleur le comportement réseau souhaité.
  - **Control layer** : le **contrôleur SDN**, qui reçoit et traite les instructions de la couche application ; contient le plan de contrôle centralisé.
  - **Infrastructure layer** : les **équipements réseau** qui transfèrent les messages.

### 2. Cisco SD-Access

- **SD-Access** (*Software-Defined Access*) : solution SDN de Cisco pour **automatiser les LAN de campus** (filaires et sans fil). Autres solutions Cisco : **ACI** (*Application Centric Infrastructure*) pour les **datacenters** (architecture spine-leaf), **SD-WAN** pour les **WAN**.
- **Cisco DNA Center** (*Digital Network Architecture*) est le **contrôleur** au centre de SD-Access (couche contrôle). Les équipements du campus (couche infrastructure) forment la **fabric**. Les scripts et apps (couche application) peuvent être maison, tiers ou de Cisco ; DNA Center a aussi un **GUI**.

### 3. Underlay, overlay, fabric

- **Underlay** : le **réseau physique** sous-jacent, équipements et connexions (filaires et sans fil), qui fournit la **connectivité IP**, par exemple avec le protocole de routage **IS-IS**. En pratique, des switches multicouches et leurs liens.
- **Overlay** : le **réseau virtuel** construit **au-dessus** de l'underlay. SD-Access utilise **VXLAN** (*Virtual Extensible LAN*) pour créer des **tunnels** ; le trafic des hôtes passe par ces tunnels.
- **Fabric** : la combinaison **overlay + underlay**, le réseau physique et virtuel dans son ensemble. Les deux sont nécessaires.

### 4. L'underlay en détail

- Rôle : **supporter les tunnels VXLAN** de l'overlay ; les équipements doivent d'abord pouvoir se joindre.
- Trois **rôles de switch** dans SD-Access :
  - **Edge node** : connecte les **hôtes finaux**, comme un switch d'accès traditionnel.
  - **Border node** : connecte aux équipements **hors du domaine SD-Access**, par exemple un routeur WAN.
  - **Control node** : utilise **LISP** (*Locator ID Separation Protocol*) pour les fonctions de plan de contrôle.
- **Brownfield** : ajouter SD-Access à un **réseau existant** (si le matériel et le logiciel le permettent, voir la « Cisco SD-Access compatibility matrix ») ; dans ce cas **DNA Center ne configure pas l'underlay**, trop risqué pour la production.
- **Greenfield** : **nouveau réseau** construit pour SD-Access ; DNA Center configure l'underlay optimal : **tous les switches sont de couche 3 et utilisent IS-IS**, **tous les liens entre switches sont des ports routés** (plus besoin de **STP**), et les **edge nodes sont la passerelle par défaut** des hôtes : **routed access layer** (couche 3 descendue jusqu'aux switches d'accès). Comparaison : un LAN traditionnel a besoin de STP contre les boucles L2 et d'un **FHRP** (HSRP, IP virtuelle 192.168.1.1) sur les switches de distribution ; dans l'underlay SD-Access, **ni STP ni FHRP**.

### 5. L'overlay en détail

- **LISP** fournit le **plan de contrôle** : une liste de correspondances **EID → RLOC**. **EID** (*Endpoint Identifier*) identifie un hôte final connecté à un edge switch ; **RLOC** (*Routing Locator*) identifie l'**edge switch** par lequel l'hôte est joignable. Système de correspondances **à la DNS** plutôt qu'une table de routage classique.
- **Cisco TrustSec (CTS)** fournit le **contrôle des politiques** (QoS, sécurité) ; retenir le nom seulement.
- **VXLAN** fournit le **plan de données** : les tunnels qui transportent le trafic. Le « extensible » du nom est important : VXLAN apporte de nombreuses fonctions à SD-Access.
- Exemple : SW3 est control node. SW2 lui indique que PC2 est joignable via SW2 (correspondance créée). PC1 envoie à sa passerelle SW1 ; SW1 demande à SW3 comment joindre PC2 ; SW3 répond « via SW2 » ; le message est transféré dans un **tunnel VXLAN SW1 → SW2**.

### 6. Cisco DNA Center

- Deux rôles : **contrôleur SDN** de SD-Access, et **gestionnaire réseau** d'un réseau traditionnel sans SD-Access (supervision, analyse, configuration centralisées).
- Application logicielle installée sur du matériel **Cisco UCS**. Possède une **API REST** (NBI). Sa SBI prend en charge **NETCONF et RESTCONF**, ainsi que **Telnet, SSH et SNMP**.
- **Intent-Based Networking (IBN)** : l'ingénieur communique son **intention** (ce groupe d'utilisateurs ne peut pas joindre ce groupe, ce groupe accède à ce serveur mais pas à cet autre) et DNA Center se charge des **configurations et politiques** sur les équipements. Exemple : les ACL traditionnelles peuvent avoir des milliers d'entrées dont l'intention s'oublie avec le temps et les départs d'ingénieurs ; dans DNA Center, une **grille de politiques** groupes source × groupes destination (Developers → Test_Servers permis, Guest → serveurs refusé, Employees → politique personnalisée), avec une **explication** par politique.
- Menus du GUI : **Design** (hiérarchie des sites sur une carte, adresses IP et sous-réseaux, serveurs DHCP et DNS), **Policy** (contrôle d'accès par groupe), **Provision** (inventaire et ajout d'équipements ; nouveaux équipements sous **Global** jusqu'à affectation à un site ; statut **managed** par défaut ; **conformité** : un équipement non conforme parce que sa version IOS est 16.11.1c au lieu de 17.03.03 attendu, et par rapport à des avis de sécurité), **Assurance** (santé des équipements : 3 sur 4 en bonne santé, 1 sans données). Sandbox DevNet : sandboxdnac.cisco.com.

### 7. Gestion traditionnelle vs DNA Center (sujet d'examen)

| Gestion traditionnelle | Gestion avec DNA Center |
| :--- | :--- |
| Équipements configurés **un par un** via SSH ou console | Équipements **gérés et supervisés centralement** depuis le GUI de DNA Center ou d'autres apps via son **API REST** |
| Configuration **manuelle par console avant déploiement** | L'administrateur communique son **intention** ; DNA Center la traduit en configurations |
| Configurations et politiques gérées **par équipement**, de façon distribuée | Configurations et politiques **gérées centralement** ; **versions logicielles** gérées centralement (surveillance des nouvelles versions, mise à jour des équipements) |
| Nouveaux déploiements **longs**, erreurs et pannes plus probables à cause de l'effort manuel | Déploiements **beaucoup plus rapides** : les nouveaux équipements reçoivent automatiquement leur configuration ; **moins d'erreurs humaines** |

### 8. Pièges d'examen

- **Underlay = physique**, **overlay = virtuel (tunnels VXLAN)**, **fabric = les deux**.
- **Trois rôles de nœuds : edge, border, control** ; il n'existe pas de « management node ».
- Underlay optimal : **tous les liens entre switches en couche 3**, IS-IS, pas de STP, routed access layer.
- **LISP = plan de contrôle, VXLAN = plan de données, Cisco TrustSec = politiques.**
- Couches SDN : **application** (scripts, apps), **control** (contrôleur), **infrastructure** (équipements).
- DNA Center = contrôleur SD-Access **et** outil de gestion d'un réseau traditionnel.

### 9. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quel terme désigne le réseau d'équipements et de connexions physiques ? | **Underlay** | L'overlay virtuel est construit dessus ; underlay + overlay = fabric. |
| Dans quelle couche trouve-t-on les scripts qui interagissent avec le contrôleur ? | **Application** | Le contrôleur est dans la couche control, les équipements dans la couche infrastructure. |
| Caractéristique d'un underlay SD-Access optimal configuré par DNA Center ? | **Tous les liens entre switches sont de couche 3** | Plus besoin de spanning tree, aucun lien désactivé car aucun risque de boucle L2. |
| Quel protocole crée les tunnels virtuels de l'overlay SD-Access ? | **VXLAN** | Virtual Extensible LAN ; « extensible » car il apporte de nombreuses fonctions à SD-Access. |
| Rôles de switch valides dans Cisco SD-Access ? (trois réponses) | **Control**, **border** et **edge** nodes | Il n'existe pas de « management node ». |

---

## 🇬🇧 English version

### 1. SDN review and the three architecture layers

- **SDN** centralizes the control plane in an application, the **controller**. Traditional control plane = **distributed** (each device has its own: OSPF, ACLs...). The controller centralizes functions such as **calculating routes**; devices share information with it instead of running OSPF with each other. Depending on the solution, all or part of the control plane is centralized. The controller interacts with devices via the **SBI** (APIs); scripts and applications interact with the controller via the **NBI**.
- The three **layers** of SDN architecture (unrelated to the OSI model):
  - **Application layer**: scripts and applications that tell the controller what network behaviors are desired.
  - **Control layer**: the **SDN controller**, which receives and processes instructions from the application layer; contains the centralized control plane.
  - **Infrastructure layer**: the **network devices** that forward messages.

### 2. Cisco SD-Access

- **SD-Access** (Software-Defined Access): Cisco's SDN solution for **automating campus LANs** (wired and wireless). Other Cisco solutions: **ACI** (Application Centric Infrastructure) for **data centers** (spine-leaf architecture), **SD-WAN** for **WANs**.
- **Cisco DNA Center** (Digital Network Architecture) is the **controller** at the center of SD-Access (control layer). The campus devices (infrastructure layer) form the **fabric**. Scripts and apps (application layer) may be home-grown, third-party or from Cisco; DNA Center also has a **GUI**.

### 3. Underlay, overlay, fabric

- **Underlay**: the underlying **physical network** of devices and connections (wired and wireless) providing **IP connectivity**, e.g. with the **IS-IS** routing protocol. Basically multilayer switches and their links.
- **Overlay**: the **virtual network** built **on top** of the underlay. SD-Access uses **VXLAN** (Virtual Extensible LAN) to build **tunnels**; host traffic is sent over these tunnels.
- **Fabric**: the combination of **overlay + underlay**, the physical and virtual network as a whole. Both are necessary.

### 4. The underlay in detail

- Purpose: **support the VXLAN tunnels** of the overlay; devices first need to reach each other.
- Three **switch roles** in SD-Access:
  - **Edge node**: connects to **end hosts**, like a traditional access switch.
  - **Border node**: connects to devices **outside the SD-Access domain**, e.g. a WAN router.
  - **Control node**: uses **LISP** (Locator ID Separation Protocol) for control plane functions.
- **Brownfield**: adding SD-Access to an **existing network** (if hardware and software support it; see the "Cisco SD-Access compatibility matrix"); in that case **DNA Center does not configure the underlay**, too risky for production.
- **Greenfield**: a **totally new network** built for SD-Access; DNA Center configures the optimal underlay: **all switches are Layer 3 and use IS-IS**, **all links between switches are routed ports** (no need for **STP**), and **edge nodes are the default gateway** of end hosts: a **routed access layer** (Layer 3 brought down to the access switches). Comparison: a traditional LAN needs STP against L2 loops and an **FHRP** (HSRP, virtual IP 192.168.1.1) on the distribution switches; the SD-Access underlay needs **neither STP nor an FHRP**.

### 5. The overlay in detail

- **LISP** provides the **control plane**: a list of **EID → RLOC** mappings. **EID** (Endpoint Identifier) identifies an end host connected to an edge switch; **RLOC** (Routing Locator) identifies the **edge switch** through which the host is reachable. A **DNS-like** mapping system rather than a traditional routing table.
- **Cisco TrustSec (CTS)** provides **policy control** (QoS, security); just remember the name.
- **VXLAN** provides the **data plane**: the tunnels that actually forward traffic. The "extensible" in the name matters: VXLAN provides many features to SD-Access.
- Example: SW3 is a control node. SW2 tells it PC2 is reachable via SW2 (mapping created). PC1 sends to its gateway SW1; SW1 asks SW3 how to reach PC2; SW3 answers "via SW2"; the message is forwarded over a **VXLAN tunnel SW1 → SW2**.

### 6. Cisco DNA Center

- Two roles: **SDN controller** for SD-Access, and **network manager** in a traditional network without SD-Access (central monitoring, analysis, configuration).
- A software application installed on **Cisco UCS** server hardware. Has a **REST API** (NBI). Its SBI supports **NETCONF and RESTCONF**, plus **Telnet, SSH and SNMP**.
- **Intent-Based Networking (IBN)**: the engineer communicates their **intent** (this user group cannot talk to that group; this group can access this server but not that one) and DNA Center takes care of the **configurations and policies** on the devices. Example: traditional ACLs can have thousands of entries whose intent is forgotten over time and as engineers leave; in DNA Center, a **policy grid** of source groups × destination groups (Developers → Test_Servers permitted, Guest → servers denied, Employees → custom policy), with an **explanation** per policy.
- GUI menus: **Design** (site hierarchy on a map, IP addresses and subnets, DHCP and DNS servers), **Policy** (group-based access control), **Provision** (device inventory and onboarding; new devices under **Global** until assigned to a site; **managed** status by default; **compliance**: a device non-compliant because its IOS version is 16.11.1c instead of the expected 17.03.03, and against security advisories), **Assurance** (device health: 3 of 4 healthy, 1 with no health data). DevNet sandbox: sandboxdnac.cisco.com.

### 7. Traditional vs DNA Center management (exam topic)

| Traditional management | DNA Center-based management |
| :--- | :--- |
| Devices configured **one by one** via SSH or console | Devices **centrally managed and monitored** from the DNA Center GUI or other apps via its **REST API** |
| **Manual console configuration before deployment** | The administrator communicates their **intent**; DNA Center turns it into configurations |
| Configurations and policies managed **per device**, distributed | Configurations and policies **centrally managed**; **software versions** centrally managed (monitors for new versions, updates devices) |
| New deployments take **a long time**; errors and failures more likely due to manual effort | Deployments **much quicker**: new devices automatically receive their configuration; **reduced human error** |

### 8. Exam traps

- **Underlay = physical**, **overlay = virtual (VXLAN tunnels)**, **fabric = both**.
- **Three node roles: edge, border, control**; there is no "management node".
- Optimal underlay: **all links between switches are Layer 3**, IS-IS, no STP, routed access layer.
- **LISP = control plane, VXLAN = data plane, Cisco TrustSec = policy.**
- SDN layers: **application** (scripts, apps), **control** (controller), **infrastructure** (devices).
- DNA Center = SD-Access controller **and** a management tool for traditional networks.

### 9. Quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which term describes the network of devices and physical connections? | **Underlay** | The virtual overlay is built on top of it; underlay + overlay = fabric. |
| In which layer would you find scripts that interact with the controller? | **Application** | The controller is in the control layer, devices in the infrastructure layer. |
| Characteristic of an optimal SD-Access underlay configured by DNA Center? | **All links between switches are Layer 3** | Spanning tree is not needed; no links disabled because there is no risk of L2 loops. |
| Which protocol creates virtual tunnels in the SD-Access overlay? | **VXLAN** | Virtual Extensible LAN; "extensible" because it supports many features used by SD-Access. |
| Valid switch roles in Cisco SD-Access? (select three) | **Control**, **border** and **edge** nodes | There is no such thing as a management node. |
