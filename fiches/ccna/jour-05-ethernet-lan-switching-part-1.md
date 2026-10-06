# CCNA Day 5 : Ethernet LAN Switching (Part 1) / Commutation Ethernet, partie 1

> Source : Jeremy's IT Lab, « Free CCNA | Ethernet LAN Switching (Part 1) | Day 5 » (38 min), vidéo n°10 de la playlist (cours). **Pas de lab pour ce jour** : le lab Packet Tracer est reporté après la partie 2 (Day 6). Fiche rédigée à partir de la transcription le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Rappels des jours 2 et 3

- **Couche 1, physique** : caractéristiques du support (niveaux de tension, distances maximales comme les 100 m de l'UTP, connecteurs, spécifications des câbles) ; les bits deviennent des signaux électriques (filaire) ou radio (sans fil). Tout le Day 2 relève de la couche 1.
- **Couche 2, liaison de données** (*data link*) : connectivité **nœud à nœud** (PC–switch, switch–routeur, routeur–routeur), format des données pour le support, **détection et éventuellement correction des erreurs** de couche 1, **adressage de couche 2** distinct de la couche 3 (les adresses IP sont de couche 3). **Les switches opèrent à la couche 2.**
- Ethernet couvre les couches 1 et 2 ; ce jour traite la couche 2.

### 2. Qu'est-ce qu'un LAN ?

- Un **LAN** (*Local Area Network*) est un réseau contenu dans une zone relativement petite : un étage de bureaux, un réseau domestique.
- **Les routeurs relient des LAN séparés.** **Les switches ne séparent pas les LAN** : ajouter un switch **étend** le LAN existant. Deux switches reliés entre eux et à une seule interface de routeur = **un seul LAN** ; les mêmes switches branchés chacun sur une interface de routeur différente = **deux LAN**.
- Ce jour traite le trafic **à l'intérieur** d'un LAN ; le trafic entre LAN viendra plus tard.

### 3. Rappel de l'encapsulation

Données → + en-tête L4 = **segment** → + en-tête L3 = **paquet** → + en-tête et remorque L2 = **trame** (*frame*). Ces étapes sont des **PDU** (*protocol data units*) ; la trame est le PDU de couche 2. Le jour porte sur la façon dont les switches reçoivent et transmettent les trames Ethernet, protocole de couche 2 de pratiquement tous les LAN.

### 4. La trame Ethernet

**En-tête (5 champs)** puis paquet encapsulé puis **remorque (1 champ)**.

| Champ | Taille | Rôle |
| :--- | :--- | :--- |
| **Préambule** (*preamble*) | **7 octets** (56 bits) | 7 fois `10101010` ; **synchronise l'horloge du récepteur** pour qu'il soit prêt à recevoir le reste |
| **SFD** (*Start Frame Delimiter*) | **1 octet** | `10101011` (dernier bit à 1) ; marque la fin du préambule et le début du reste de la trame |
| **Destination** | **6 octets** | adresse MAC de destination |
| **Source** | **6 octets** | adresse MAC de l'émetteur |
| **Type / Longueur** | **2 octets** (16 bits) | valeur **≤ 1500** : **longueur** du paquet encapsulé en octets (ex. 1400) ; valeur **≥ 1536** : **type** du paquet, **0x0800** (2048) = **IPv4**, **0x86DD** (34525) = **IPv6** |
| **FCS** (*Frame Check Sequence*, remorque) | **4 octets** (32 bits) | détecte les données corrompues par un **CRC** (*Cyclic Redundancy Check*) sur les données reçues |

- En-tête + remorque = **26 octets** (en comptant préambule et SFD).
- Le `0x` indique l'hexadécimal. CRC : « cyclic » (codes cycliques), « redundancy » (les 4 octets n'ajoutent aucune information nouvelle), « check » (vérification). Retenir : **le FCS de la trame Ethernet est un CRC**.

### 5. Les adresses MAC

- **MAC** = *Media Access Control* : adresse **physique** de **6 octets / 48 bits**, **attribuée à la fabrication** (d'où **BIA**, *Burned-In Address*), contrairement à l'adresse IP logique configurée en CLI.
- **Globalement unique** : deux équipements au monde ne devraient pas avoir la même (il existe des adresses « localement uniques », rares).
- **3 premiers octets = OUI** (*Organizationally Unique Identifier*), attribué au fabricant (Cisco a plusieurs OUI que lui seul peut utiliser) ; **3 derniers octets = unique à l'équipement**.
- Écrite en **12 caractères hexadécimaux**, par exemple `AAAA.AA00.0001` (point tous les 4 caractères) ou `AA.AA.AA.00.00.01` (tous les 2).

### 6. L'hexadécimal

- Décimal : 10 chiffres (0 à 9) ; quand une colonne est pleine, on en ajoute une (dizaines, centaines…).
- Hexadécimal : **16 chiffres**, 0 à 9 puis **A = 10, B = 11, C = 12, D = 13, E = 14, F = 15**. Après F vient « 10 » = 1 seizaine et 0 unité = 16 en décimal ; « 11 » = 17 ; « 12 » = 18… « 19 » = 25, puis 1A, 1B, 1C…
- Une compréhension générale suffit ici ; IPv6 approfondira.

### 7. Comment un switch apprend et transmet

Réseau : PC1, PC2, PC3 sur SW1, interfaces **F0/1, F0/2, F0/3** (FastEthernet, 100 Mbit/s). MAC simplifiées `AAAA.AA00.0001`, `.0002`, `.0003` (même OUI AAAA.AA = même fabricant).

1. **PC1 → PC2** : trame **unicast** (destinée à une seule cible). SW1 la reçoit et **lit l'adresse MAC source** pour **apprendre** où est PC1 : il ajoute `AAAA.AA00.0001` associée à **F0/1** dans sa **table d'adresses MAC** (*MAC address table*). Adresse **apprise dynamiquement** (*dynamic MAC address*), non configurée à la main.
2. La destination `.0002` est inconnue de la table : c'est une **trame unicast inconnue** (*unknown unicast*). Le switch **inonde** (*flood*) : il la copie sur **toutes ses interfaces sauf celle de réception** (F0/2 et F0/3, pas F0/1).
3. **PC3 ignore** la trame (MAC de destination différente de la sienne) ; **PC2 la traite** en remontant la pile. Tant que PC2 n'envoie rien, SW1 ne peut pas apprendre sa MAC : une deuxième trame PC1 → PC2 est **encore inondée**.
4. **PC2 → PC1** (adresses inversées) : SW1 apprend `.0002` sur **F0/2**. La destination `.0001` est connue : **trame unicast connue** (*known unicast*), **transmise uniquement** vers F0/1. PC1 la décapsule.
5. **Vieillissement** : sur un switch Cisco, une MAC dynamique est **retirée après 5 minutes d'inactivité** ; elle est réapprise si l'hôte réémet.

**Deux switches** (PC1, PC2 sur SW1 ; PC3, PC4 sur SW2 ; SW1 F0/3 ↔ SW2 F0/3), tables vides, **PC1 → PC3** :

- SW1 apprend PC1 sur F0/1 ; unicast inconnue → inondée sur F0/2 et F0/3. PC2 l'ignore.
- SW2 reçoit la trame sur F0/3 et apprend **PC1 sur F0/3** : l'interface de la table est **celle par laquelle la MAC est joignable**, pas forcément une connexion directe. Unicast inconnue → inondée sur F0/1 et F0/2. PC4 l'ignore, PC3 la reçoit.
- **PC3 → PC1** : SW2 apprend PC3 sur F0/1 ; PC1 est connue sur F0/3 → transmise sans inondation. SW1 apprend PC3 sur F0/3 ; PC1 connue sur F0/1 → transmise. **Le switch remplit sa table avec le champ MAC source** parce qu'une trame reçue de cette source sur cette interface prouve que la source est joignable par là.

### 8. Pièges d'examen

- **Préambule** = synchronisation d'horloge ; **SFD** = fin du préambule (ne pas confondre).
- MAC = **48 bits** (6 octets), **pas 48 octets** (384 bits) ; une adresse IP fait 32 bits.
- **OUI = première moitié** (24 bits, 6 caractères hexa), ex. `E8BA.70` dans `E8BA.7011.2874`.
- Le switch apprend avec la **MAC source**, jamais la destination.
- **Unicast inconnue → inondée** (sauf port de réception) ; **unicast connue → transmise** sur un seul port. « Allcast » n'existe pas.
- Un switch **n'inonde pas** sur l'interface de réception.
- Un switch **ne sépare pas** les LAN ; seul un routeur le fait.
- Champ Type : **0x0800 IPv4, 0x86DD IPv6** ; ≤ 1500 = longueur, ≥ 1536 = type.

### 9. Commandes IOS

Aucune commande dans cette vidéo (les commandes `show mac address-table` et `clear mac address-table` arrivent au Day 6).

### 10. Le lab

Pas de lab pour le Day 5 : le lab « Analyzing Ethernet Switching » couvre les jours 5 et 6 et se trouve dans la fiche du Day 6.

### 11. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quel champ de la trame Ethernet synchronise l'horloge du récepteur ? | **Préambule** | Le SFD marque la fin du préambule ; Type indique le type de paquet encapsulé ; FCS détecte les erreurs de transmission. |
| Longueur de l'adresse physique d'un équipement ? | **48 bits** | 48 octets feraient 384 bits ; 32 bits est la taille d'une adresse IP. |
| OUI de `E8BA.7011.2874` ? | **`E8BA.70`** | L'OUI est la première moitié (24 bits) de la MAC, attribuée au fabricant ; `E8BA`, `7011` ou `E8BA.7011` n'ont pas la bonne longueur. |
| Quel champ un switch utilise-t-il pour remplir sa table MAC ? | **MAC source** | Préambule et longueur n'y servent pas ; la MAC de destination est une adresse mais n'aide pas à apprendre. La source est associée à l'interface de réception. |
| Quel type de trame est inondé sur toutes les interfaces sauf celle de réception ? | **Unicast inconnue** | L'unicast connue est dans la table, pas besoin d'inonder ; « allcast » n'est pas un type de trame. |

---

## 🇬🇧 English version

### 1. Review of Days 2 and 3

- **Layer 1, Physical**: characteristics of the medium (voltage levels, maximum distances such as UTP's 100 m, connectors, cable specifications); bits become electrical (wired) or radio (wireless) signals. Everything in Day 2 is Layer 1.
- **Layer 2, Data Link**: **node-to-node** connectivity (PC–switch, switch–router, router–router), how data is formatted for the medium, **detects and possibly corrects** Physical Layer errors, **Layer 2 addressing** separate from Layer 3 (IP addresses are Layer 3). **Switches operate at Layer 2.**
- Ethernet involves Layers 1 and 2; this day is about Layer 2.

### 2. What is a LAN?

- A **LAN** (*Local Area Network*) is a network contained within a relatively small area: an office floor, a home network.
- **Routers connect separate LANs.** **Switches do not separate LANs**: adding a switch **expands** the existing LAN. Two switches linked together and to a single router interface = **one LAN**; the same switches each on a different router interface = **two LANs**.
- This day covers traffic **within** a LAN; traffic between LANs comes later.

### 3. Encapsulation review

Data → + L4 header = **segment** → + L3 header = **packet** → + L2 header and trailer = **frame**. These stages are **PDUs** (*protocol data units*); the frame is the Layer 2 PDU. The day focuses on how switches receive and forward Ethernet frames, the Layer 2 protocol of virtually every LAN.

### 4. The Ethernet frame

**Header (5 fields)**, then the encapsulated packet, then **trailer (1 field)**.

| Field | Size | Role |
| :--- | :--- | :--- |
| **Preamble** | **7 bytes** (56 bits) | 7 times `10101010`; **synchronizes the receiver's clock** so it is ready for the rest |
| **SFD** (*Start Frame Delimiter*) | **1 byte** | `10101011` (last bit is 1); marks the end of the preamble and the start of the rest of the frame |
| **Destination** | **6 bytes** | destination MAC address |
| **Source** | **6 bytes** | sender's MAC address |
| **Type / Length** | **2 bytes** (16 bits) | value **1500 or less**: **length** of the encapsulated packet in bytes (e.g. 1400); value **1536 or greater**: **type** of packet, **0x0800** (2048) = **IPv4**, **0x86DD** (34525) = **IPv6** |
| **FCS** (*Frame Check Sequence*, trailer) | **4 bytes** (32 bits) | detects corrupted data by running a **CRC** (*Cyclic Redundancy Check*) over the received data |

- Header + trailer = **26 bytes** (counting preamble and SFD).
- `0x` means hexadecimal. CRC: "cyclic" (cyclic codes), "redundancy" (the 4 bytes add no new information), "check" (verification). Remember: **the Ethernet FCS is a CRC**.

### 5. MAC addresses

- **MAC** = *Media Access Control*: a **physical** address of **6 bytes / 48 bits**, **assigned when the device is made** (hence **BIA**, *Burned-In Address*), unlike the logical IP address configured in the CLI.
- **Globally unique**: no two devices in the world should share one ("locally unique" addresses exist but are rare).
- **First 3 bytes = OUI** (*Organizationally Unique Identifier*), assigned to the maker (Cisco has several OUIs only it can use); **last 3 bytes = unique to the device**.
- Written as **12 hexadecimal characters**, e.g. `AAAA.AA00.0001` (period every 4 characters) or `AA.AA.AA.00.00.01` (every 2).

### 6. Hexadecimal

- Decimal: 10 digits (0 to 9); when a column is full you add one (tens, hundreds...).
- Hexadecimal: **16 digits**, 0 to 9 then **A = 10, B = 11, C = 12, D = 13, E = 14, F = 15**. After F comes "10" = 1 sixteen and 0 ones = decimal 16; "11" = 17; "12" = 18... "19" = 25, then 1A, 1B, 1C...
- A general understanding is enough for now; IPv6 will go deeper.

### 7. How a switch learns and forwards

Network: PC1, PC2, PC3 on SW1, interfaces **F0/1, F0/2, F0/3** (FastEthernet, 100 Mbps). Simplified MACs `AAAA.AA00.0001`, `.0002`, `.0003` (same OUI AAAA.AA = same maker).

1. **PC1 → PC2**: a **unicast** frame (destined for a single target). SW1 receives it and **reads the source MAC** to **learn** where PC1 is: it adds `AAAA.AA00.0001` associated with **F0/1** to its **MAC address table**. A **dynamically learned** (*dynamic*) MAC address, not manually configured.
2. Destination `.0002` is not in the table: an **unknown unicast** frame. The switch **floods** it: a copy out of **all interfaces except the one it was received on** (F0/2 and F0/3, not F0/1).
3. **PC3 drops** the frame (destination MAC does not match its own); **PC2 processes** it up the stack. Until PC2 sends something, SW1 cannot learn its MAC: a second PC1 → PC2 frame is **flooded again**.
4. **PC2 → PC1** (addresses reversed): SW1 learns `.0002` on **F0/2**. Destination `.0001` is known: a **known unicast** frame, **forwarded only** out of F0/1. PC1 decapsulates it.
5. **Aging**: on a Cisco switch, a dynamic MAC is **removed after 5 minutes of inactivity**; it is learned again if the host sends traffic.

**Two switches** (PC1, PC2 on SW1; PC3, PC4 on SW2; SW1 F0/3 ↔ SW2 F0/3), empty tables, **PC1 → PC3**:

- SW1 learns PC1 on F0/1; unknown unicast → flooded out of F0/2 and F0/3. PC2 drops it.
- SW2 receives the frame on F0/3 and learns **PC1 on F0/3**: the interface in the table is **the one through which the MAC is reachable**, not necessarily a direct connection. Unknown unicast → flooded out of F0/1 and F0/2. PC4 drops it, PC3 receives it.
- **PC3 → PC1**: SW2 learns PC3 on F0/1; PC1 is known on F0/3 → forwarded without flooding. SW1 learns PC3 on F0/3; PC1 known on F0/1 → forwarded. **The switch fills its table from the source MAC field** because a frame received from that source on that interface proves the source is reachable there.

### 8. Exam traps

- **Preamble** = clock synchronization; **SFD** = end of the preamble (do not mix them up).
- MAC = **48 bits** (6 bytes), **not 48 bytes** (384 bits); an IP address is 32 bits.
- **OUI = first half** (24 bits, 6 hex characters), e.g. `E8BA.70` in `E8BA.7011.2874`.
- The switch learns from the **source MAC**, never the destination.
- **Unknown unicast → flooded** (except the receiving port); **known unicast → forwarded** out of one port. "Allcast" does not exist.
- A switch **never floods** out of the interface the frame arrived on.
- A switch **does not separate** LANs; only a router does.
- Type field: **0x0800 IPv4, 0x86DD IPv6**; 1500 or less = length, 1536 or greater = type.

### 9. IOS commands

No commands in this video (`show mac address-table` and `clear mac address-table` come on Day 6).

### 10. The lab

No lab for Day 5: the "Analyzing Ethernet Switching" lab covers Days 5 and 6 and is in the Day 6 sheet.

### 11. The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which Ethernet frame field provides receiver clock synchronization? | **Preamble** | The SFD marks the end of the preamble; Type indicates the encapsulated packet type; FCS detects transmission errors. |
| How long is a network device's physical address? | **48 bits** | 48 bytes would be 384 bits; 32 bits is an IP address. |
| OUI of `E8BA.7011.2874`? | **`E8BA.70`** | The OUI is the first half (24 bits) of the MAC, assigned to the maker; `E8BA`, `7011` or `E8BA.7011` are the wrong length. |
| Which field does a switch use to populate its MAC address table? | **Source MAC address** | Preamble and length are not used; the destination MAC is an address but does not help learning. The source is associated with the receiving interface. |
| Which kind of frame is flooded out of all interfaces except the receiving one? | **Unknown unicast** | A known unicast is in the table, no need to flood; "allcast" is not a frame type. |
