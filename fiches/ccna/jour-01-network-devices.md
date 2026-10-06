# CCNA Day 1 : Network Devices / Équipements réseau

> Source : Jeremy's IT Lab, « Free CCNA | Network Devices | Day 1 » (30 min), vidéo n°1 de la playlist. Fiche initiale générée avec NotebookLM, vérifiée et complétée contre la transcription le 6 octobre 2026. Les ajouts par rapport à la fiche initiale sont marqués **[+]**.

## 🇫🇷 Version française

### 1. Qu'est-ce qu'un réseau informatique ?

Un **réseau informatique** est un réseau de télécommunications numériques permettant à des **nœuds** (*nodes*) de partager des ressources.

**[+]** Deux PC reliés par un câble forment déjà un réseau. Routeur, switch, pare-feu, serveur et client sont tous des **nœuds**. Le mot **hôte** (*host*) peut désigner n'importe quel nœud ; **hôte final** (*end host*, *endpoint*) désigne spécifiquement les clients et serveurs, aux extrémités du réseau.

### 2. Le modèle client-serveur

- **Client :** équipement qui **accède à un service** fourni par un serveur (votre PC qui regarde la vidéo).
- **Serveur :** équipement qui **fournit des fonctions ou des services** aux clients (serveur de fichiers, serveur YouTube). Pas forcément une machine de datacenter : n'importe quel PC ou téléphone peut être serveur.
- **Rôle dynamique :** le même équipement est client dans une situation et serveur dans une autre (AirDrop entre deux iPhone : celui qui envoie le fichier est le serveur).
- **[+]** Le rôle est défini par la transaction, pas par la machine : « PC1 demande image.jpg à PC2 » fait de PC1 le client et de PC2 le serveur.

### 3. Les équipements réseau principaux

**Commutateur (*switch*)**

- Interconnecte les hôtes finaux au sein d'un **même réseau local (LAN)** : un étage de bureaux, un petit bureau, un réseau domestique.
- **Nombreux ports** (interfaces réseau), **[+]** généralement **24 ou plus**.
- **[+] Piège d'examen : un switch ne relie pas des LAN entre eux et ne donne pas accès à Internet.** Il faut un routeur pour cela.
- Exemples : Cisco Catalyst 9200, Catalyst 3650 (gamme Catalyst = switches d'entreprise).

**Routeur (*router*)**

- Interconnecte **des LAN différents** et achemine le trafic **entre réseaux**, donc vers Internet (New York ↔ Tokyo via R1, Internet, R2).
- **Moins de ports** qu'un switch.
- **[+]** Peut offrir quelques fonctions de sécurité de base, mais ce n'est pas son rôle : la protection revient au pare-feu.
- Exemples : Cisco ISR 1000, ISR 4000, **[+]** ISR 900 (ISR = Integrated Services Router).

**Pare-feu (*firewall*)**

- Équipement de sécurité spécialisé qui **surveille et contrôle le trafic entrant et sortant** selon des **règles configurées explicitement** (ce qui est autorisé, ce qui est refusé).
- Placement **à l'extérieur** du routeur (filtre avant le routeur) ou **à l'intérieur** (filtre après), **[+]** et parfois les deux à la fois.
- **Pare-feu réseau (matériel) :** appareil dédié filtrant le trafic entre réseaux. C'est l'objet du cours.
- **Pare-feu d'hôte (logiciel) :** application sur chaque PC. **[+]** À garder actif même derrière un pare-feu matériel : c'est une ligne de défense supplémentaire.
- **NGFW (*Next-Generation Firewall*) :** pare-feu avec des capacités de filtrage avancées, par exemple l'**IPS** (*Intrusion Prevention System*). Les ASA modernes et les Firepower en sont.
- Exemples : Cisco ASA 5500-X (*Adaptive Security Appliance*, le pare-feu « classique » de Cisco), Firepower 2100.

### 4. Lecture d'un schéma

- **Le nuage (*cloud*) :** représente **Internet**, ou toute partie du réseau dont le détail n'est pas utile au schéma.

### 5. Méthode de travail (ce que Jeremy demande pour chaque vidéo)

1. **Quiz de fin de vidéo** : une seule meilleure réponse, même si plusieurs semblent possibles, comme à l'examen Cisco.
2. **Flashcards Anki** : un deck par vidéo. **[+] Conseil de Jeremy : un seul deck central « CCNA », dans lequel on déplace les cartes de chaque nouveau deck**, plutôt que des dizaines de decks séparés. Les decks sont dans `ressources/jeremy-it-lab/anki/`.
3. **Lab Packet Tracer** par vidéo (fichiers dans `ressources/jeremy-it-lab/labs/`, copies de travail dans `labs/dayNN/`). Celui du Day 1 est une prise en main de Packet Tracer.

### 6. [+] Le quiz du Day 1 (5 questions, à refaire de tête)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Connecter les 30 PC d'un service : quel équipement ? | **Switch** | Beaucoup de ports, hôtes du même LAN. Un routeur ou un pare-feu n'a pas 30 ports ; un serveur est un hôte final. |
| Vous recevez une vidéo par AirDrop : le téléphone de l'ami était… | **Serveur** | Il fournit le service. Un hôte final n'est pas un LAN. |
| Votre appareil pendant que vous regardez la vidéo est… | **Client** | Il reçoit un service. « Hôte final » est vrai mais ne décrit pas sa fonction. |
| Relier les réseaux séparés de l'entreprise : quel équipement ? | **Routeur** | Un pare-feu peut relier des réseaux mais son rôle est le filtrage. Un LAN n'est pas un équipement. |
| Remplacer un vieux pare-feu par un modèle aux fonctions avancées : quel type ? | **Next-generation firewall** | « Next-level » et « top-layer » n'existent pas ; un pare-feu d'hôte est un logiciel. |

---

## 🇬🇧 English version

### 1. What is a computer network?

A **computer network** is a digital telecommunications network that allows **nodes** to share resources.

**[+]** Two PCs connected by a cable already form a network. Routers, switches, firewalls, servers and clients are all **nodes**. The word **host** can refer to any node; **end host** (*endpoint*) specifically means clients and servers, at the edges of the network.

### 2. The client-server model

- **Client:** a device that **accesses a service** made available by a server (your PC watching the video).
- **Server:** a device that **provides functions or services** for clients (file server, YouTube server). Not necessarily a datacenter machine: any PC or phone can be a server.
- **Dynamic role:** the same device is a client in one transaction and a server in another (AirDrop between two iPhones: the one sending the file is the server).
- **[+]** The role is defined by the transaction, not the machine: "PC1 asks PC2 for image.jpg" makes PC1 the client and PC2 the server.

### 3. Key network devices

**Switch**

- Connects end hosts within the **same Local Area Network (LAN)**: one office floor, a small office, a home network.
- **Many ports** (network interfaces), **[+]** usually **24 or more**.
- **[+] Exam trap: switches do not provide connectivity between LANs or over the Internet.** A router is needed for that.
- Examples: Cisco Catalyst 9200, Catalyst 3650 (Catalyst = Cisco's enterprise-grade switches).

**Router**

- Connects **different LANs** and forwards traffic **between networks**, hence over the Internet (New York ↔ Tokyo via R1, the Internet, R2).
- **Fewer ports** than a switch.
- **[+]** Can provide some basic security features, but that is not its job: protection belongs to the firewall.
- Examples: Cisco ISR 1000, ISR 4000, **[+]** ISR 900 (ISR = Integrated Services Router).

**Firewall**

- A specialty security device that **monitors and controls traffic entering and exiting the network** based on **explicitly configured rules** (what is allowed, what is denied).
- Placed **outside** the router (filters before the router) or **inside** (filters after), **[+]** sometimes both.
- **Network firewall (hardware):** dedicated appliance filtering traffic between networks. The focus of this course.
- **Host-based firewall (software):** application on each PC. **[+]** Keep it on even behind a hardware firewall: an extra line of defense.
- **NGFW (Next-Generation Firewall):** firewall with more advanced filtering capabilities, e.g. **IPS** (Intrusion Prevention System). Modern ASAs and Firepower are NGFWs.
- Examples: Cisco ASA 5500-X (Adaptive Security Appliance, Cisco's classic firewall), Firepower 2100.

### 4. Reading a diagram

- **The cloud:** represents **the Internet**, or any part of the network whose details are not needed for the diagram.

### 5. Working method (what Jeremy asks for every video)

1. **End-of-video quiz**: one best answer, even when several look possible, as on the Cisco exam.
2. **Anki flashcards**: one deck per video. **[+] Jeremy's advice: keep a single central "CCNA" deck and move each new deck's cards into it**, rather than dozens of separate decks. Decks are in `ressources/jeremy-it-lab/anki/`.
3. **Packet Tracer lab** for every video (files in `ressources/jeremy-it-lab/labs/`, working copies in `labs/dayNN/`). Day 1's lab is a Packet Tracer walkthrough.

### 6. [+] Day 1 quiz (5 questions, redo from memory)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Hardware to connect the 30 PCs of a department? | **Switch** | Many ports, same-LAN hosts. A router or firewall lacks 30 ports; a server is an end host. |
| You received a video via AirDrop: the friend's phone was… | **Server** | It provided the service. An end host is not a LAN. |
| Your device while watching the video is… | **Client** | It receives a service. "End host" is true but does not describe its function. |
| Hardware to connect the company's separate networks? | **Router** | A firewall can connect networks but its purpose is filtering. A LAN is not a device. |
| Replace an old firewall with one offering advanced functions: which type? | **Next-generation firewall** | "Next-level" and "top-layer" do not exist; a host-based firewall is software. |
