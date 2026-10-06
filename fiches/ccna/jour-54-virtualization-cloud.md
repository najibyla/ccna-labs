# CCNA Day 54 : Virtualization, Cloud, Containers & VRF / Virtualisation, cloud, conteneurs et VRF

> Source : Jeremy's IT Lab, « Free CCNA | Virtualization & Cloud | Day 54 (part 1) » (39 min, vidéo n°109 de la playlist), « Containers | Day 54 (part 2) » (14 min, vidéo n°110), « VRF | Day 54 (part 3) » (18 min, vidéo n°111) et « Oracle VirtualBox | Day 54 Lab » (9 min, vidéo n°112, lab : installation d'un hyperviseur de type 2 et d'une VM Ubuntu, pas de fichier Packet Tracer). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

## Partie 1 : virtualisation et cloud

Sujets d'examen 1.2.f (on-premises et cloud) et 1.12 (fondamentaux de la virtualisation, machines virtuelles). La virtualisation est une composante essentielle des services cloud.

### 1.1 Serveurs et virtualisation

- Cisco vend aussi des serveurs matériels (**UCS**, *Unified Computing System*) ; les plus gros vendeurs sont **Dell EMC, HPE** (Hewlett Packard Enterprise) et **IBM**.
- **Sans virtualisation** : relation **un à un** entre serveur physique et système d'exploitation ; un serveur physique par application (web, mail, base de données). Tout faire tourner sur un seul OS est possible mais mauvais : les applications ne sont pas **isolées**, un problème sur l'une affecte les autres. Un serveur par application est **inefficace** : coût, espace, énergie, et ressources (**CPU, RAM, stockage, NIC** – *Network Interface Card*) **sous-utilisées**.
- **Virtualisation** : rompt la relation un à un ; **plusieurs OS sur un serveur physique**, chaque instance est une **VM** (*virtual machine*). L'**hyperviseur** (ou **VMM**, *Virtual Machine Monitor*) gère et alloue les ressources matérielles (CPU, RAM) à chaque VM.
- **Hyperviseur de type 1** : tourne **directement sur le matériel**. Exemples : **VMware ESXi, Microsoft Hyper-V**. Aussi appelé **bare-metal** ou **natif** (*native*). Utilisé dans les centres de données ; efficace car il consomme peu de ressources lui-même.
- **Hyperviseur de type 2** : tourne **comme un programme sur un OS**. Exemples : **VMware Workstation, Oracle VirtualBox**. L'OS sur le matériel est l'**OS hôte** (*host OS*), celui dans la VM l'**OS invité** (*guest OS*). Aussi appelé **hosted hypervisor**. Rare en centre de données, courant sur les appareils personnels (faire tourner une application Windows sur Mac ou Linux).
- **Pourquoi virtualiser** (d'après VMware) : **partitionnement** (plusieurs OS sur une machine, ressources divisées : résout la sous-utilisation), **isolation** (isolation des pannes), **encapsulation** (une VM se sauvegarde, se déplace, se copie comme un fichier), **indépendance matérielle** (une VM se déplace sur n'importe quel serveur physique qui fait tourner l'hyperviseur). Bénéfices : **CapEx réduit** (moins de serveurs), **OpEx réduit** (espace, énergie, refroidissement, moins de travail de mise en place), **temps d'arrêt réduit ou éliminé** (déploiement sur plusieurs serveurs pour la redondance), productivité, efficacité, agilité, réactivité, **rapidité** (ajouter une VM vs commander, recevoir, monter, câbler un serveur).
- **Réseaux virtuels** : les VM se connectent entre elles et au réseau externe via un **switch virtuel** (*vSwitch*) sur l'hyperviseur (fourni par l'hyperviseur, ou un switch virtuel Cisco). Comme un switch réel : ports **access ou trunk**, **VLAN** pour séparer les VM en couche 2 (deux VM en VLAN 10, une en VLAN 20). Les interfaces du vSwitch se connectent aux **NIC physiques** du serveur. Entre les NIC et les switches physiques, un **vPC** (*virtual port channel*) vers deux switches distincts pour la redondance (courant en centre de données, hors programme).

### 1.2 Déploiements traditionnels : on-premises et colocation

- **On-premises** : tous les serveurs, équipements réseau et autres infrastructures sont **sur la propriété de l'entreprise**, achetés et possédés par elle ; elle assure espace, énergie et refroidissement.
- **Colocation** : centres de données qui **louent de l'espace** pour l'infrastructure des clients (serveurs, équipements réseau) ; le centre fournit espace, électricité, refroidissement et **sécurité physique** ; les équipements restent sous la responsabilité du client. PC et points d'accès restent dans les locaux de l'entreprise.

### 1.3 Définition du cloud computing (NIST SP 800-145)

Le NIST (*National Institute of Standards and Technology*) définit le cloud computing comme un modèle permettant un **accès réseau ubiquitaire, pratique, à la demande** à un **pool partagé de ressources informatiques configurables** (réseaux, serveurs, stockage, applications, services) pouvant être **rapidement provisionnées et libérées** avec un **effort de gestion ou une interaction avec le fournisseur minimaux**. Composé de **5 caractéristiques essentielles, 3 modèles de service, 4 modèles de déploiement** : c'est ce que Cisco attend pour le CCNA, pas les services précis de chaque fournisseur. Document de 2011, concepts toujours valables.

**Les cinq caractéristiques essentielles** (un service qui n'en a que certaines n'est généralement pas un vrai cloud) :
1. **Libre-service à la demande** (*on-demand self-service*) : le client provisionne seul (temps serveur, stockage) sans interaction humaine avec le fournisseur ; portail web (créer des VM sur AWS sans contacter AWS).
2. **Large accès réseau** (*broad network access*) : disponible via des mécanismes standard (Internet, WAN privé) depuis des clients légers ou lourds hétérogènes (téléphones, tablettes, portables, stations).
3. **Mutualisation des ressources** (*resource pooling*) : ressources du fournisseur regroupées pour servir plusieurs clients (**multi-tenant**), assignées dynamiquement ; **indépendance de localisation** (le client ne contrôle pas l'emplacement exact, mais peut le choisir à un niveau d'abstraction supérieur : pays, état, centre de données).
4. **Élasticité rapide** (*rapid elasticity*) : extension et réduction rapides, parfois automatiques, selon la demande ; les capacités **semblent illimitées** au client (pas infinies en réalité).
5. **Service mesuré** (*measured service*) : usage **mesuré, contrôlé, rapporté** ; transparence pour le fournisseur et le client, facturation à l'usage (X dollars par Go par jour) ; pas de surprise en fin de mois.

**Les trois modèles de service** (« quelque chose as a Service ») :
- **SaaS** (*Software as a Service*) : utiliser les **applications du fournisseur** sur son infrastructure cloud, via un client léger (navigateur, messagerie web) ou une interface de programme ; le client ne gère rien en dessous, sauf quelques réglages utilisateur. Exemples : **Microsoft Office 365**, **Google G Suite** (Gmail). Le fournisseur contrôle tout, du centre de données à l'application.
- **PaaS** (*Platform as a Service*) : déployer des applications **créées ou acquises par le client** avec les langages, bibliothèques et outils du fournisseur ; le client ne gère ni réseau, ni serveurs, ni OS, ni stockage, mais contrôle ses applications déployées. Exemples : **AWS Lambda**, **Google App Engine**. Plateforme pour développeurs ; les applications hébergées ne sont pas dans le périmètre du fournisseur.
- **IaaS** (*Infrastructure as a Service*) : provisionner **traitement, stockage, réseaux** et autres ressources fondamentales pour déployer n'importe quel logiciel, y compris OS et applications ; le client contrôle OS, stockage, applications, éventuellement certains composants réseau (pare-feu d'hôte). Exemples : **Amazon EC2**, **Google Compute Engine**. Le **plus de contrôle** pour le client.

**Les quatre modèles de déploiement** :
- **Cloud privé** : infrastructure pour **l'usage exclusif d'une seule organisation** (plusieurs unités) ; possédée et exploitée par l'organisation, un tiers ou les deux ; **sur site ou hors site**. Grandes entreprises et gouvernements (AWS fournit un cloud privé au département de la Défense américain). **Cloud ne veut pas toujours dire hors site.**
- **Cloud communautaire** : usage exclusif d'une **communauté d'organisations** aux préoccupations communes (mission, sécurité, conformité) ; sur ou hors site. Le **moins courant**.
- **Cloud public** : **ouvert au grand public** ; possédé par une entreprise, un organisme académique ou gouvernemental ; **sur les locaux du fournisseur**. De loin le plus courant : **AWS, Azure, GCP, OCI, IBM, Alibaba** (AWS numéro un depuis longtemps).
- **Cloud hybride** : **combinaison** de deux clouds distincts ou plus (privé, communautaire, public), entités uniques liées par une technologie permettant la portabilité des données et applications (ex. **cloud bursting** : un cloud privé déborde vers un public en cas de manque de ressources).

### 1.4 Bénéfices du cloud et connexion au cloud

- **Coût** : CapEx (*capital expenses*) réduits ou éliminés, remplacés par de l'**OpEx** (*operating expenses*, petits coûts réguliers). **Échelle mondiale** rapide (choisir pays et région proches des utilisateurs). **Rapidité et agilité** (ressources en minutes). **Productivité** (plus de serveurs à acheter, monter, câbler, mettre à jour). **Fiabilité** (sauvegardes faciles, données **mirrorées** sur plusieurs sites pour la reprise après sinistre). Liste partielle de bénéfices potentiels : la plupart des entreprises combinent on-premises, colocation et cloud public ; ne pas choisir le cloud parce que c'est à la mode.
- **Connexion à un cloud public** : via un **WAN privé** (VPN MPLS) ou via **Internet** (bon marché, flexible, moins sûr : utiliser un **VPN**). Les connexions **redondantes** restent préférables ; éviter le point unique de défaillance.

### 1.5 Pièges d'examen (partie 1)

- Le rôle de l'hyperviseur : **gérer et allouer les ressources matérielles aux VM**. **Type 1 = natif / bare-metal, directement sur le matériel ; type 2 = hosted, sur un OS hôte.** Pas de type 3. Plusieurs VM sur un seul serveur.
- Les cinq caractéristiques : **on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service**. Un « pool de ressources infini » n'en fait pas partie.
- **SaaS** = utiliser les applications du fournisseur.
- **Tous** les modèles de déploiement peuvent exister hors site ; un cloud privé peut être **sur site**.

### 1.6 Quiz de la partie 1 (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quelle affirmation sur les VM est vraie ? | **A** : l'hyperviseur gère et alloue les ressources matérielles aux VM | B et C inversent les définitions (type 2 sur un OS hôte, type 1 sur le matériel) ; D est faux car plusieurs VM peuvent tourner sur un serveur. |
| Quel type d'hyperviseur est appelé hyperviseur natif ? | **A** : type 1 | Type 2 = hosted ; le type 3 n'existe pas comme terme reconnu. |
| Laquelle n'est PAS une caractéristique essentielle du cloud ? | **D** : pool de ressources infini | Le pool semble infini mais ne l'est pas. Les autres options sont des caractéristiques essentielles ; seule on-demand self-service n'est pas listée. |
| Quel type de service permet d'utiliser des applications tournant sur l'infrastructure du fournisseur ? | **C** : SaaS | Le fournisseur fournit tout, du centre de données à l'application ; le client paie pour utiliser l'application. |
| Quels types de déploiement peuvent exister hors site ? | **D** : tous | Public, privé, communautaire, hybride peuvent être hors site, et le sont en général ; mais un cloud privé peut aussi être sur site. |

## Partie 2 : conteneurs

### 2.1 Rappel : VM et hyperviseurs

- Sans virtualisation : un OS (Windows Server, Red Hat Linux) et toutes les applications dessus, **non isolées** ; un serveur physique par application est trop coûteux.
- VM : plusieurs OS sur un serveur ; hyperviseur pour allouer les ressources. **Type 1** (natif, bare-metal) directement sur le matériel, en centre de données. **Type 2** (hosted) sur un OS hôte, sur les appareils personnels : exemple de Jeremy : Windows, **VMware Workstation**, et **Cisco Modeling Labs (CML)** en VM pour les labs virtuels.
- Les OS des VM peuvent être identiques ou différents (Windows, Linux, macOS). Les **binaires et bibliothèques** sont les logiciels nécessaires aux applications. Une VM isole ses applications ; un problème dans une VM n'affecte pas les autres ; les VM se créent, suppriment, déplacent facilement.

### 2.2 Les conteneurs

- **Conteneur** : paquet logiciel contenant **une application et toutes ses dépendances** (binaires, bibliothèques). Plusieurs applications par conteneur sont possibles mais inhabituelles : **un conteneur = une application**.
- Les conteneurs tournent sur un **moteur de conteneurs** (*container engine*), par exemple **Docker Engine** (le plus populaire), qui tourne sur un **OS hôte** (en général Linux), sur le matériel.
- **Légers** : seulement les dépendances nécessaires, **pas d'OS dans chaque conteneur**. C'est **la différence majeure** avec les VM, d'où découlent tous les coûts et bénéfices.
- **Orchestrateur de conteneurs** : plateforme automatisant déploiement, gestion, mise à l'échelle. **Kubernetes** (le plus populaire), **Docker Swarm**. Nécessaire car les grands systèmes (**microservices**) peuvent compter des milliers de conteneurs.
- **Architecture microservices** : diviser une grande solution en petites parties (microservices) plutôt qu'une **application monolithique** ; des centaines de microservices en conteneurs, orchestrés.

### 2.3 VM vs conteneurs

| | VM | Conteneurs |
| :--- | :--- | :--- |
| Démarrage | **minutes** | **millisecondes** (plus agiles ; un conteneur qui plante est remplacé très vite) |
| Espace disque | **dizaines de Go** | **dizaines de Mo** |
| CPU et RAM | plus | moins |
| Portabilité | bonne (entre systèmes avec le même hyperviseur) | **meilleure** (plus petits, un conteneur Docker tourne sur presque tout service de conteneurs) |
| Isolation | **meilleure** (un OS par VM ; avantage aussi pour la sécurité) | moindre : si l'OS partagé plante, tous les conteneurs sont affectés |

- Forte tendance vers les conteneurs avec les microservices, l'automatisation et le **DevOps** (développement logiciel + opérations IT), mais les VM restent largement utilisées.

### 2.4 Quiz de la partie 2 (3 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Les trois composants sur lesquels tournent les conteneurs ? | **Matériel, OS, moteur de conteneurs** | Le matériel, l'OS dessus, le moteur de conteneurs sur l'OS, puis les conteneurs. |
| Exemples d'orchestrateurs de conteneurs ? (deux réponses) | **B** Docker Swarm, **C** Kubernetes | Docker Engine est un moteur, pas un orchestrateur ; Hyper-V est un hyperviseur de type 1 de Microsoft, sans rapport. |
| Affirmations vraies sur VM et conteneurs ? (trois réponses) | **A, C, F** | Les VM consomment plus de ressources (un OS chacune) ; les VM sont plus isolées (même raison) ; les conteneurs tournent sur un OS hôte avec un moteur de conteneurs. |

## Partie 3 : VRF (*Virtual Routing and Forwarding*)

### 3.1 Concept

- **VRF** divise **un routeur physique en plusieurs routeurs virtuels** : « les VLAN des routeurs ». Les VLAN divisent un switch en switches virtuels avec chacun son **domaine de broadcast** ; VRF divise un routeur en routeurs virtuels avec chacun **sa table de routage**.
- Par défaut toutes les interfaces d'un routeur sont dans le même « domaine de routage » : le trafic reçu sur une interface peut sortir par n'importe quelle autre. Avec VRF, G0/0 dans VRF1 et G1/2 dans VRF3 ne peuvent pas échanger de trafic.
- Les **interfaces de couche 3** sont assignées à une VRF (**instance VRF**) : interfaces de routeur, **SVI** et **ports routés** des switches multicouches ; pas les interfaces de couche 2. Concept de **couche 3**.
- Exception : le **VRF leaking** permet le passage entre VRF (avancé, non couvert).
- VRF sert souvent à **MPLS**, mais ici il s'agit de **VRF-lite** (VRF sans MPLS). Usage : un fournisseur fait passer le trafic de **plusieurs clients** sur un même équipement : **trafic isolé** (chaque client sur son routeur virtuel) et **adresses IP qui peuvent se chevaucher** (trois clients utilisant chacun 192.168.1.0/24 et 192.168.2.0/24).
- VRF n'est pas supporté dans Packet Tracer : utiliser CML ou du matériel réel.

### 3.2 Configuration (démonstration, hors programme)

- Réseau : SPR1 (fournisseur) relié à C1R1, C1R2 (client 1) et C2R1, C2R2 (client 2) ; les deux clients utilisent **192.168.1.0/30**.
- **Sans VRF** : après G0/0 et G0/1, configurer G0/2 en 192.168.1.1 échoue : « **192.168.1.0 overlaps with G0/0** ». Même avec 192.168.1.2, échec : deux interfaces d'un même routeur ne peuvent pas être dans le même sous-réseau.
- **Avec VRF** : `ip vrf CUSTOMER1` et `ip vrf CUSTOMER2` (config globale) ; `show ip vrf` liste les VRF. Sur G0/0 : `ip vrf forwarding CUSTOMER1` ; message : « **Interface G0/0 IPv4 disabled and addresses removed due to enabling VRF CUSTOMER1** » : l'adresse IP existante est **supprimée**, il faut la reconfigurer (configurer l'IP **après** l'assignation à la VRF). Idem G0/1. G0/2 en 192.168.1.1/30 dans CUSTOMER2 : accepté malgré le chevauchement avec G0/0. Idem G0/3. `show ip vrf` montre les interfaces par VRF.
- `show ip route` : **vide** : il affiche la **table de routage globale**, et toutes les interfaces sont dans des VRF (un mélange est possible ; une interface hors VRF apparaît dans la table globale et est isolée des VRF). `show ip route vrf CUSTOMER1` : routes connectées et locales de G0/0 et G0/1 ; `show ip route vrf CUSTOMER2` : celles de G0/2 et G0/3. Tables séparées entre elles et de la globale.
- **Pings** : `ping 192.168.1.2` échoue (table globale vide). `ping vrf CUSTOMER1 192.168.1.2` réussit : atteint **C1R1** (deux appareils ont cette IP, la VRF choisit). Dans CUSTOMER1, 192.168.11.2 (C1R2) réussit, 192.168.12.2 (C2R2) échoue (pas de route). `ping vrf CUSTOMER2 192.168.1.2` atteint **C2R1** ; 192.168.12.2 réussit. Les hôtes d'une même VRF communiquent, pas ceux de VRF différentes.

### 3.3 Commandes IOS

```
SPR1(config)# ip vrf CUSTOMER1                          ! crée la VRF
SPR1(config)# interface g0/0
SPR1(config-if)# ip vrf forwarding CUSTOMER1            ! assigne l'interface à la VRF (supprime l'adresse IP existante)
SPR1(config-if)# ip address 192.168.1.1 255.255.255.252 ! à (re)configurer après l'assignation
SPR1# show ip vrf                                       ! liste des VRF et de leurs interfaces
SPR1# show ip route                                     ! table de routage globale (vide si tout est en VRF)
SPR1# show ip route vrf CUSTOMER1                       ! table de routage de la VRF
SPR1# ping vrf CUSTOMER1 192.168.1.2                    ! ping depuis une VRF
```

### 3.4 Quiz de la partie 3 (3 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Après `ip address` puis `ip vrf forwarding VRF1` sur G0/0, `show ip interface brief` ne montre pas d'adresse IP. Pourquoi ? | **B** : l'adresse a été supprimée par `ip vrf forwarding VRF1` | Assigner une interface à une VRF supprime son adresse IP ; configurer les adresses après l'assignation. |
| Toutes les interfaces de R1 sont dans des VRF ; `ping 192.168.1.10` sur R1 : quel appareil répond ? | **D** : aucun | Un ping sans VRF utilise la table de routage globale, vide ici : R1 ne peut même pas envoyer les pings. |
| Affirmations vraies sur VLAN et VRF ? (trois réponses) | **C, D, F** : les VRF divisent les routeurs par des tables de routage séparées ; les VLAN divisent les switches par des domaines de broadcast séparés ; des interfaces de routeur dans des VRF différentes peuvent avoir la même IP | A faux : les VRF ne créent pas de domaines de broadcast (les interfaces de routeur sont déjà dans des domaines séparés). B faux : les VLAN ne créent pas de tables MAC séparées (une seule table MAC). E faux : VRF se configure aussi sur les SVI et ports routés des switches multicouches. |

## Le lab : Oracle VirtualBox

- Pas nécessaire pour le CCNA (il faut connaître les bases de la virtualisation, pas savoir créer une VM). Trois raisons : voir concrètement un **hyperviseur de type 2** (VirtualBox) sur un **OS hôte** (Windows) et un **OS invité** (Ubuntu) dessus ; montrer que c'est **simple** ; avoir un hyperviseur de type 2 (VirtualBox ou VMware Workstation) pour la suite des études (Jeremy fait tourner la **VM GNS3** dans VMware Workstation). Si le PC n'est pas assez puissant, regarder la vidéo et passer à la suite.
- **Étapes** : télécharger VirtualBox sur virtualbox.org (version Windows hosts, ou macOS/Linux selon l'hôte), installer avec les réglages par défaut. Télécharger la distribution Linux **Ubuntu** (version **LTS**, *Long Term Support*) sur ubuntu.com ; Linux est une famille d'OS utilisant le noyau Linux, chaque OS étant une **distribution** (*distro*).
- Dans VirtualBox : **New**, nom « Ubuntu 20.04 » (type Linux et version Ubuntu détectés automatiquement) ; mémoire **1 Go** (recommandation ; PC de 16 Go ; en donner plus pour un vrai usage) ; **créer un disque dur virtuel** : type de fichier par défaut, **allocation dynamique** (par défaut), **10 Go**. Puis **Settings > Storage**, cliquer sur le disque vide, **Choose a disk file**, sélectionner le **.iso** d'Ubuntu (insérer le disque d'installation dans l'ordinateur virtuel). **Start**.
- Installation Ubuntu : Install Ubuntu, clavier US, **installation minimale** sans téléchargement des mises à jour (pour aller vite), effacer le disque et installer (aucun OS détecté), fuseau horaire, nom, utilisateur, mot de passe (« cisco », faible), redémarrage, Entrée.
- Résultat : **Windows sur le matériel, VirtualBox sur Windows, Ubuntu sur VirtualBox**. La VM peut être supprimée ou gardée pour se familiariser avec Linux, compétence précieuse en IT.

---

## 🇬🇧 English version

## Part 1: virtualization and cloud

Exam topics 1.2.f (on-premises and cloud) and 1.12 (virtualization fundamentals, virtual machines). Virtualization is an essential part of cloud services.

### 1.1 Servers and virtualization

- Cisco also sells hardware servers (**UCS**, Unified Computing System); the largest vendors are **Dell EMC, HPE** (Hewlett Packard Enterprise) and **IBM**.
- **Without virtualization**: a **one-to-one** relationship between physical server and operating system; one physical server per app (web, email, database). Running everything on one OS is possible but bad: apps are not **isolated**, a problem in one affects the others. One server per app is **inefficient**: cost, space, power, and **under-used** resources (**CPU, RAM, storage, NIC** – Network Interface Card).
- **Virtualization** breaks the one-to-one relationship: **multiple OSs on one physical server**, each instance a **VM** (virtual machine). The **hypervisor** (or **VMM**, Virtual Machine Monitor) manages and allocates hardware resources (CPU, RAM) to each VM.
- **Type 1 hypervisor**: runs **directly on the hardware**. Examples: **VMware ESXi, Microsoft Hyper-V**. Also called **bare-metal** or **native**. Used in data centers; efficient because it needs few resources itself.
- **Type 2 hypervisor**: runs **as a program on an OS**. Examples: **VMware Workstation, Oracle VirtualBox**. The OS on the hardware is the **host OS**, the one in the VM the **guest OS**. Also called a **hosted hypervisor**. Rare in data centers, common on personal devices (running a Windows-only app on Mac or Linux).
- **Why virtualize** (from VMware): **partitioning** (multiple OSs on one machine, resources divided: solves under-use), **isolation** (fault isolation), **encapsulation** (a VM is saved, moved, copied like a file), **hardware independence** (move any VM to any physical server running the hypervisor). Benefits: **reduced capital costs** (fewer servers), **reduced operating costs** (space, power, cooling, less setup work), **reduced or eliminated downtime** (deploy to multiple servers for redundancy), productivity, efficiency, agility, responsiveness, **speed** (adding a VM vs ordering, receiving, racking, cabling a server).
- **Virtual networks**: VMs connect to each other and to the external network via a **virtual switch** (vSwitch) on the hypervisor (provided by the hypervisor, or a Cisco virtual switch). Like a real switch: **access or trunk** ports, **VLANs** to separate VMs at Layer 2 (two VMs in VLAN 10, one in VLAN 20). vSwitch interfaces connect to the server's **physical NICs**. Between the NICs and the physical switches, a **vPC** (virtual port channel) to two separate switches for redundancy (common in data centers, not on the exam).

### 1.2 Traditional deployments: on-premises and colocation

- **On-premises**: all servers, network devices and other infrastructure are **on company property**, purchased and owned by the company; it provides space, power and cooling.
- **Colocation**: data centers that **rent space** for customers' infrastructure (servers, network devices); the data center provides space, electricity, cooling and **physical security**; the devices remain the customer's responsibility. Desktops and access points stay in the company's building.

### 1.3 Cloud computing definition (NIST SP 800-145)

NIST (National Institute of Standards and Technology) defines cloud computing as a model for enabling **ubiquitous, convenient, on-demand network access** to a **shared pool of configurable computing resources** (networks, servers, storage, applications, services) that can be **rapidly provisioned and released** with **minimal management effort or service provider interaction**. Composed of **5 essential characteristics, 3 service models, 4 deployment models**: that is what Cisco expects for the CCNA, not specific providers' services. Published in 2011, still the foundational concepts.

**The five essential characteristics** (a service with only some of them is generally not a true cloud service):
1. **On-demand self-service**: the consumer unilaterally provisions (server time, storage) without human interaction with the provider; a web portal (creating VMs on AWS without contacting AWS).
2. **Broad network access**: available through standard mechanisms (Internet, private WAN) from heterogeneous thin or thick clients (phones, tablets, laptops, workstations).
3. **Resource pooling**: the provider's resources are pooled to serve multiple consumers (**multi-tenant**), dynamically assigned; **location independence** (the customer does not control the exact location but may specify it at a higher level: country, state, data center).
4. **Rapid elasticity**: capabilities scale rapidly outward and inward, sometimes automatically, with demand; they **appear unlimited** to the consumer (not actually infinite).
5. **Measured service**: usage is **monitored, controlled and reported**; transparency for provider and consumer, charged by usage (X dollars per GB per day); no surprise bill.

**The three service models** ("something as a Service"):
- **SaaS** (Software as a Service): use the **provider's applications** running on cloud infrastructure, via a thin client (browser, web email) or program interface; the consumer manages nothing underneath, except limited user settings. Examples: **Microsoft Office 365**, **Google G Suite** (Gmail). The provider controls everything from the data center to the application.
- **PaaS** (Platform as a Service): deploy **consumer-created or acquired applications** using the provider's languages, libraries and tools; the consumer manages neither network, servers, OS nor storage, but controls the deployed applications. Examples: **AWS Lambda**, **Google App Engine**. A platform for developers; hosted applications are outside the provider's scope.
- **IaaS** (Infrastructure as a Service): provision **processing, storage, networks** and other fundamental resources to run arbitrary software, including OSs and applications; the consumer controls OS, storage, applications, possibly some networking components (host firewalls). Examples: **Amazon EC2**, **Google Compute Engine**. The **most control** for the customer.

**The four deployment models**:
- **Private cloud**: infrastructure for **exclusive use by a single organization** (multiple business units); owned and operated by the organization, a third party or both; **on or off premises**. Large enterprises and governments (AWS provides a private cloud for the US Department of Defense). **Cloud does not always mean off premises.**
- **Community cloud**: exclusive use by a **community of organizations** with shared concerns (mission, security, compliance); on or off premises. The **least common**.
- **Public cloud**: **open use by the general public**; owned by a business, academic or government organization; **on the provider's premises**. By far the most common: **AWS, Azure, GCP, OCI, IBM, Alibaba** (AWS the dominant number one).
- **Hybrid cloud**: a **composition** of two or more distinct clouds (private, community, public) that remain unique entities but are bound by technology enabling data and application portability (e.g. **cloud bursting**: a private cloud offloads to a public one when resources run short).

### 1.4 Cloud benefits and connecting to the cloud

- **Cost**: CapEx (capital expenses) reduced or eliminated, replaced by **OpEx** (operating expenses, regular small costs). Rapid **global scale** (choose country and region close to users). **Speed and agility** (resources within minutes). **Productivity** (no procuring, racking, cabling, updating servers). **Reliability** (easy backups, data **mirrored** at multiple locations for disaster recovery). A partial list of potential benefits: most companies combine on-premises, colocation and public cloud; don't use the cloud just because it is popular.
- **Connecting to a public cloud**: via a **private WAN** (MPLS VPN) or via the **Internet** (cheap, flexible, less secure: use a **VPN**). **Redundant** connections are always preferable; avoid a single point of failure.

### 1.5 Exam traps (part 1)

- The hypervisor's role: **manage and allocate hardware resources to VMs**. **Type 1 = native / bare-metal, directly on hardware; Type 2 = hosted, on a host OS.** No Type 3. Many VMs on one server.
- The five characteristics: **on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service**. An "infinite resource pool" is not one.
- **SaaS** = using the provider's applications.
- **All** deployment models may exist off premises; a private cloud may be **on premises**.

### 1.6 Part 1 quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which statement about VMs is true? | **A**: the hypervisor manages and allocates hardware resources to VMs | B and C reverse the definitions (Type 2 on a host OS, Type 1 on hardware); D is wrong because many VMs can run on one server. |
| Which hypervisor type is known as a native hypervisor? | **A**: Type 1 | Type 2 = hosted; Type 3 does not exist as an accepted term. |
| Which is NOT an essential characteristic of cloud computing? | **D**: infinite resource pool | The pool appears infinite but is not. The other options are essential characteristics; only on-demand self-service is missing. |
| Which service type lets customers use applications running on the provider's cloud infrastructure? | **C**: SaaS | The provider provides everything from the data center to the app; the customer pays to use the app. |
| Which deployment types may exist off premises? | **D**: all of the above | Public, private, community and hybrid can and usually do exist off premises; but a private cloud may also be on premises. |

## Part 2: containers

### 2.1 Review: VMs and hypervisors

- Without virtualization: one OS (Windows Server, Red Hat Linux) and all apps on it, **not isolated**; one physical server per app is too costly.
- VMs: multiple OSs on one server; a hypervisor allocates resources. **Type 1** (native, bare-metal) directly on hardware, in data centers. **Type 2** (hosted) on a host OS, on personal devices: Jeremy's example: Windows, **VMware Workstation**, and **Cisco Modeling Labs (CML)** as a VM for virtual labs.
- VM OSs can be the same or different (Windows, Linux, macOS). **Binaries and libraries** are the software needed by the apps. A VM isolates its apps; an issue in one VM does not affect the others; VMs are easy to create, delete, move.

### 2.2 Containers

- **Container**: a software package containing **an app and all its dependencies** (binaries, libraries). Multiple apps per container are possible but unusual: **one container = one app**.
- Containers run on a **container engine**, e.g. **Docker Engine** (the most popular), which runs on a **host OS** (usually Linux), on the hardware.
- **Lightweight**: only the required dependencies, **no OS in each container**. That is **the major difference** from VMs, from which all costs and benefits stem.
- **Container orchestrator**: a platform automating deployment, management, scaling. **Kubernetes** (the most popular), **Docker Swarm**. Needed because large-scale systems (**microservices**) can require thousands of containers.
- **Microservice architecture**: divide a larger solution into smaller parts (microservices) instead of one **monolithic app**; hundreds of microservices in containers, orchestrated.

### 2.3 VMs vs containers

| | VMs | Containers |
| :--- | :--- | :--- |
| Boot time | **minutes** | **milliseconds** (more agile; a crashed container is replaced very quickly) |
| Disk space | **tens of GB** | **tens of MB** |
| CPU and RAM | more | less |
| Portability | good (between systems running the same hypervisor) | **better** (smaller, a Docker container runs on nearly any container service) |
| Isolation | **better** (one OS per VM; also a security benefit) | less: if the shared OS crashes, all containers are affected |

- A major movement toward containers with microservices, automation and **DevOps** (software development + IT operations), but VMs are still widely used.

### 2.4 Part 2 quiz (3 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| The three components containers run on top of? | **Hardware, OS, container engine** | The hardware, the OS on it, the container engine on the OS, then the containers. |
| Examples of container orchestrators? (select two) | **B** Docker Swarm, **C** Kubernetes | Docker Engine is a container engine, not an orchestrator; Hyper-V is a Microsoft Type 1 hypervisor, unrelated. |
| True statements about VMs and containers? (select three) | **A, C, F** | VMs require more resources (each runs its own OS); VMs are more isolated (same reason); containers all run on a host OS with a container engine on top. |

## Part 3: VRF (Virtual Routing and Forwarding)

### 3.1 Concept

- **VRF** divides **one physical router into multiple virtual routers**: "VLANs for routers". VLANs divide a switch into virtual switches each with its own **broadcast domain**; VRF divides a router into virtual routers each with **its own routing table**.
- By default all router interfaces are in the same "routing domain": traffic received on one interface can be forwarded out of any other. With VRF, G0/0 in VRF1 and G1/2 in VRF3 cannot exchange traffic.
- **Layer 3 interfaces** are assigned to a VRF (**VRF instance**): router interfaces, **SVIs** and **routed ports** on multilayer switches; not Layer 2 interfaces. A **Layer 3** concept.
- Exception: **VRF leaking** allows traffic between VRFs (advanced, not covered).
- VRF is commonly used for **MPLS**, but here it is **VRF-lite** (VRF without MPLS). Use: a service provider carries **multiple customers'** traffic on one device: **isolated traffic** (each customer on its own virtual router) and **overlapping IP addresses** allowed (three customers each using 192.168.1.0/24 and 192.168.2.0/24).
- VRF is not supported in Packet Tracer: use CML or real devices.

### 3.2 Configuration (demo, not on the exam)

- Network: SPR1 (provider) connected to C1R1, C1R2 (customer 1) and C2R1, C2R2 (customer 2); both customers use **192.168.1.0/30**.
- **Without VRF**: after G0/0 and G0/1, configuring G0/2 as 192.168.1.1 fails: "**192.168.1.0 overlaps with G0/0**". Even 192.168.1.2 fails: two interfaces on one router cannot be in the same subnet.
- **With VRF**: `ip vrf CUSTOMER1` and `ip vrf CUSTOMER2` (global config); `show ip vrf` lists the VRFs. On G0/0: `ip vrf forwarding CUSTOMER1`; message: "**Interface G0/0 IPv4 disabled and addresses removed due to enabling VRF CUSTOMER1**": the existing IP is **removed** and must be re-configured (configure IPs **after** assigning to the VRF). Same for G0/1. G0/2 as 192.168.1.1/30 in CUSTOMER2: accepted despite overlapping with G0/0. Same for G0/3. `show ip vrf` shows the interfaces per VRF.
- `show ip route`: **empty**: it shows the **global routing table**, and all interfaces are in VRFs (a mix is possible; an interface not in a VRF appears in the global table and is isolated from the VRFs). `show ip route vrf CUSTOMER1`: connected and local routes of G0/0 and G0/1; `show ip route vrf CUSTOMER2`: those of G0/2 and G0/3. Separate tables from each other and from the global one.
- **Pings**: `ping 192.168.1.2` fails (empty global table). `ping vrf CUSTOMER1 192.168.1.2` works: reaches **C1R1** (two devices have that IP, the VRF decides). In CUSTOMER1, 192.168.11.2 (C1R2) works, 192.168.12.2 (C2R2) fails (no route). `ping vrf CUSTOMER2 192.168.1.2` reaches **C2R1**; 192.168.12.2 works. Hosts in the same VRF communicate, hosts in different VRFs cannot.

### 3.3 IOS commands

```
SPR1(config)# ip vrf CUSTOMER1                          ! create the VRF
SPR1(config)# interface g0/0
SPR1(config-if)# ip vrf forwarding CUSTOMER1            ! assign the interface to the VRF (removes any existing IP address)
SPR1(config-if)# ip address 192.168.1.1 255.255.255.252 ! (re)configure after the assignment
SPR1# show ip vrf                                       ! list of VRFs and their interfaces
SPR1# show ip route                                     ! global routing table (empty if everything is in VRFs)
SPR1# show ip route vrf CUSTOMER1                       ! the VRF's routing table
SPR1# ping vrf CUSTOMER1 192.168.1.2                    ! ping from within a VRF
```

### 3.4 Part 3 quiz (3 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| After `ip address` then `ip vrf forwarding VRF1` on G0/0, `show ip interface brief` shows no IP address. Why? | **B**: the IP address was removed by `ip vrf forwarding VRF1` | Assigning an interface to a VRF removes its IP address; configure addresses after the assignment. |
| All of R1's interfaces are in VRFs; `ping 192.168.1.10` on R1: which device responds? | **D**: no device | A ping without a VRF uses the global routing table, empty here: R1 cannot even send the pings. |
| True statements about VLANs and VRFs? (select three) | **C, D, F**: VRFs divide routers with separate routing tables; VLANs divide switches with separate broadcast domains; router interfaces in different VRFs can have the same IP | A wrong: VRFs do not create broadcast domains (router interfaces are already in separate ones). B wrong: VLANs do not create separate MAC tables (one MAC table). E wrong: VRF can also be configured on SVIs and routed ports of multilayer switches. |

## The lab: Oracle VirtualBox

- Not necessary for the CCNA (know the basics of virtualization, not how to set up a VM). Three reasons: see a **Type 2 hypervisor** (VirtualBox) on a **host OS** (Windows) with a **guest OS** (Ubuntu) on top; show it is **simple**; have a Type 2 hypervisor (VirtualBox or VMware Workstation) for future studies (Jeremy runs the **GNS3 VM** in VMware Workstation). If your PC cannot run a VM, just watch the video and continue.
- **Steps**: download VirtualBox from virtualbox.org (Windows hosts, or the macOS/Linux version for your host), install with default settings. Download the **Ubuntu** Linux distribution (**LTS**, Long Term Support, version) from ubuntu.com; Linux is a family of OSs using the Linux kernel, each OS being a **distribution** (distro).
- In VirtualBox: **New**, name "Ubuntu 20.04" (type Linux and version Ubuntu detected automatically); memory **1 GB** (recommendation; 16 GB PC; give more for real use); **create a virtual hard disk**: default file type, **dynamically allocated** (default), **10 GB**. Then **Settings > Storage**, click the empty disk, **Choose a disk file**, select the Ubuntu **.iso** (inserting the install disk into the virtual computer). **Start**.
- Ubuntu installation: Install Ubuntu, US keyboard, **minimal installation** without downloading updates (to save time), erase disk and install (no OS detected), time zone, name, username, password ("cisco", weak), restart, Enter.
- Result: **Windows on the hardware, VirtualBox on Windows, Ubuntu on VirtualBox**. The VM can be deleted or kept to get familiar with Linux, a valuable IT skill.
