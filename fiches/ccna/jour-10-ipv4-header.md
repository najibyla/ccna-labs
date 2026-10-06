# CCNA Day 10 : IPv4 Header / L'en-tête IPv4

> Source : Jeremy's IT Lab, « Free CCNA | IPv4 Header | Day 10 » (30 min), vidéo n°18 de la playlist (cours). Pas de lab pour ce jour : le lab de routage vient après le Day 11. Fiche rédigée à partir de la transcription le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Cadre : le paquet dans la trame

- L'en-tête IPv4 est utilisé à la **couche 3** pour envoyer des données entre équipements de réseaux différents, jusqu'à l'autre bout du monde via Internet : c'est le **routage** (*routing*). Jeremy a découpé son introduction au routage en plusieurs vidéos ; celle-ci ne traite **que les champs de l'en-tête IPv4**.
- Encapsulation : données + en-tête de couche 4 (TCP ou UDP, vus plus tard) = **segment** ; segment + en-tête de couche 3 (IP) = **paquet** (*packet*) ; paquet + en-tête et trailer de couche 2 = **trame** (*frame*). Ces unités sont les **PDU** (*protocol data units*) : PDU de couche 3 = paquet, PDU de couche 2 = trame.
- Jeremy ne pense pas qu'il faille mémoriser la taille exacte de chaque champ pour l'examen, mais il ne garantit rien : **connaître le rôle de chaque champ**. Le schéma (Wikipédia) se lit de gauche à droite, de haut en bas.

### 2. Les champs de l'en-tête IPv4

| Champ | Taille | Rôle |
| :--- | :--- | :--- |
| **Version** | 4 bits | Version d'IP. IPv4 = **4** (0100), IPv6 = 6 (0110). L'IPv5 « perdu » était l'Internet Stream Protocol, expérimental, jamais public. L'en-tête IPv6 a une autre structure. |
| **IHL** (*Internet Header Length*) | 4 bits | Longueur de l'en-tête, nécessaire parce que le champ Options est variable. Exprimée **par incréments de 4 octets** : valeur 5 → 20 octets (**minimum**, sans options) ; valeur 15 (maximum sur 4 bits : 1+2+4+8) → **60 octets** (maximum). Les options font donc au plus 40 octets. |
| **DSCP** (*Differentiated Services Code Point*) | 6 bits | **QoS** (*quality of service*) : prioriser le trafic sensible au délai (voix, vidéo en streaming). Une page web lente est tolérable, un appel Skype saccadé ne l'est pas. Vidéo dédiée plus tard. |
| **ECN** (*Explicit Congestion Notification*) | 2 bits | Signalement de bout en bout de la congestion **sans abandonner de paquets** (normalement, la congestion se signale par des pertes). Optionnel : il faut que les deux extrémités et l'infrastructure le supportent. |
| **Total Length** | 16 bits | Longueur totale du paquet (en-tête IPv4 + segment de couche 4, en-tête et données) **en octets**, pas en incréments de 4 comme l'IHL. Minimum **20** (en-tête seul, sans données), maximum **65 535** (16 bits à 1 : 1+2+4+…+32 768). |
| **Identification** | 16 bits | Si un paquet est **fragmenté** (plus grand que le **MTU**, *Maximum Transmission Unit*, en général **1500 octets**, lié à la charge utile maximale d'une trame Ethernet), tous ses fragments portent la **même valeur** ici pour être réassemblés. Le réassemblage est fait par l'**hôte destinataire**. |
| **Flags** | 3 bits | Bit 0 : réservé, toujours 0. Bit 1 : **DF** (*Don't Fragment*), à 1 le paquet ne doit pas être fragmenté. Bit 2 : **MF** (*More Fragments*), à 1 s'il reste des fragments, à 0 sur le dernier fragment et sur un paquet non fragmenté. |
| **Fragment Offset** | 13 bits | Position du fragment dans le paquet d'origine : permet le réassemblage même si les fragments arrivent **dans le désordre**. |
| **Time To Live** (TTL) | 8 bits | Un routeur **abandonne un paquet dont le TTL vaut 0** : évite les boucles infinies dues à une mauvaise configuration de routage (qui finiraient par saturer le réseau). Conçu comme une durée en secondes, en pratique c'est un **compteur de sauts** (*hop count*) : chaque routeur décrémente de 1. Valeur par défaut recommandée : **64**. |
| **Protocol** | 8 bits | Protocole du PDU de couche 4 encapsulé : **6 = TCP**, **17 = UDP**, **1 = ICMP** (utilisé par ping), **89 = OSPF** (*Open Shortest Path First*, protocole de routage dynamique vu plus tard). Retenir ces quatre valeurs. |
| **Header Checksum** | 16 bits | Somme de contrôle de l'**en-tête seulement**. Le routeur recalcule et compare ; si différent, il **abandonne** le paquet. Les erreurs dans les données encapsulées sont détectées par le protocole encapsulé (TCP et UDP ont leur propre checksum). |
| **Source IP Address** | 32 bits | Adresse IPv4 de l'émetteur. |
| **Destination IP Address** | 32 bits | Adresse IPv4 du destinataire prévu. |
| **Options** | 0 à 320 bits (40 octets) | Rarement utilisé. Présent si **IHL > 5**. Pas à connaître pour le CCNA. |

### 3. Lecture d'une capture Wireshark

- Ping entre deux routeurs (*echo (ping) request*). Sélectionner la trame, l'en-tête Ethernet, l'en-tête IP ou la charge utile ICMP surligne la zone correspondante dans la représentation **hexadécimale** en bas.
- En-tête IPv4 développé : Version 0100 = 4 ; Header Length 0101 = 5 → 20 octets ; champ *Differentiated Services* regroupant DSCP et ECN, tous deux à 0 ; Total Length **100** (le ping Cisco standard envoie des paquets de **100 octets**) ; Identification 5 ; Flags : bit réservé *not set* (= 0 ; *set* = 1), DF non positionné (fragmentation possible), MF non positionné, Fragment Offset 0 ; TTL **255** (maximum sur 8 bits) ; Protocol ICMP (1) ; Header Checksum en hexadécimal (**0x**, chaque chiffre hexa = 4 bits, 4 chiffres = 16 bits) ; adresses source et destination. Pas d'options.
- **`ping 192.168.1.2 size 10000`** : paquets de 10 000 octets, bien plus que le MTU de 1500 → **fragments IP** affichés « reassembled in #13 » (la requête echo). Chaque fragment : Total Length **1500** (taille du MTU), Identification **1** identique pour tous, bit **MF positionné** (pas le dernier), **Fragment Offset différent** (0 pour le premier).
- **`ping ... df-bit`** : le bit DF est positionné ; avec la taille par défaut de 100 octets, aucun problème. Avec une taille supérieure au MTU **et** DF, **les pings échouent** : trop grands pour passer entiers, interdits de fragmentation.

### Pièges d'examen

- **IHL en incréments de 4 octets** (5 = 20 octets, 15 = 60 octets) ; **Total Length en octets** (20 à 65 535).
- En-tête IPv4 : **20 octets minimum, 60 maximum** ; options 40 octets au plus.
- **TTL = 0 → paquet abandonné** ; c'est un compteur de sauts, décrémenté de 1 par routeur ; défaut recommandé 64.
- Le **Header Checksum ne couvre que l'en-tête** ; les erreurs dans les données relèvent de TCP/UDP.
- Numéros de protocole : **1 ICMP, 6 TCP, 17 UDP, 89 OSPF**.
- **MF = 1 sur tous les fragments sauf le dernier** ; Fragment Offset est un champ de 13 bits, pas un bit ; « packet fragment bit » n'existe pas.
- Le seul champ de longueur variable est **Options** ; Total Length et IHL décrivent des longueurs variables mais sont eux-mêmes de taille fixe.
- Version IPv4 = **0100** en binaire.

### Commandes IOS

```text
R1# ping 192.168.1.2                       ! ping Cisco standard : paquets de 100 octets, pas de fragmentation
R1# ping 192.168.1.2 size 10000            ! paquets de 10 000 octets > MTU 1500 : fragmentés en morceaux de 1500
R1# ping 192.168.1.2 df-bit                ! positionne le bit Don't Fragment ; échoue si la taille dépasse le MTU
```

### Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| 1. Valeur binaire fixe du premier champ d'un en-tête IPv4 ? A 0010 ; B 0110 ; C 0001 ; D 0100 | **D, 0100** | Le premier champ est Version ; dans un en-tête IP **version 4**, il vaut toujours 4 = 0100. 0110 serait 6 (IPv6). |
| 2. Quel champ provoque l'abandon du paquet s'il vaut 0 ? A TTL ; B DSCP ; C IHL ; D ECN | **A, TTL** | Time To Live, réduit de 1 à chaque routeur traversé ; à 0 le paquet est abandonné. DSCP et ECN à 0 signifient simplement « non utilisé » ; IHL ne peut pas être inférieur à 5. |
| 3. Comment les erreurs dans les données encapsulées d'un paquet IPv4 sont-elles détectées ? A le Header Checksum ; B le protocole encapsulé (TCP, UDP) ; C elles ne peuvent pas l'être | **B, le protocole encapsulé** | Le Header Checksum ne vérifie que l'en-tête IPv4 ; TCP et UDP ont leur propre checksum pour les données. |
| 4. Quel champ de l'en-tête IPv4 est de longueur variable ? A Options ; B Header Checksum ; C Total Length ; D IHL | **A, Options** | De 0 à 320 bits. Les autres champs sont de taille fixe : Total Length et IHL représentent des longueurs variables, mais les champs eux-mêmes font toujours 16 et 4 bits. |
| 5. Quel bit vaut 1 sur tous les fragments sauf le dernier ? A fragment offset bit ; B more fragments bit ; C don't fragment bit ; D packet fragment bit | **B, More Fragments** | Dans le champ Flags, MF indique que le fragment n'est pas le dernier (0 sur le dernier). Fragment Offset est un champ de 13 bits, pas un bit ; DF interdit la fragmentation ; « packet fragment bit » n'existe pas. |

---

## 🇬🇧 English version

### 1. Context: the packet inside the frame

- The IPv4 header is used at **Layer 3** to send data between devices on separate networks, even across the world over the Internet: this is **routing**. Jeremy split his routing introduction into several videos; this one covers **only the fields of the IPv4 header**.
- Encapsulation: data + Layer 4 header (TCP or UDP, covered later) = **segment**; segment + Layer 3 header (IP) = **packet**; packet + Layer 2 header and trailer = **frame**. These units are **PDUs** (*protocol data units*): the Layer 3 PDU is a packet, the Layer 2 PDU is a frame.
- Jeremy doubts you need to memorize each field's exact size for the exam, but makes no guarantees: **know the purpose of each field**. The (Wikipedia) chart reads left to right, top to bottom.

### 2. The IPv4 header fields

| Field | Size | Purpose |
| :--- | :--- | :--- |
| **Version** | 4 bits | IP version. IPv4 = **4** (0100), IPv6 = 6 (0110). The "lost IPv5" was the experimental Internet Stream Protocol, never publicly used. The IPv6 header has a different structure. |
| **IHL** (*Internet Header Length*) | 4 bits | Header length, needed because the Options field is variable. Expressed **in 4-byte increments**: value 5 → 20 bytes (**minimum**, no options); value 15 (maximum of 4 bits: 1+2+4+8) → **60 bytes** (maximum). So Options is at most 40 bytes. |
| **DSCP** (*Differentiated Services Code Point*) | 6 bits | **QoS** (*quality of service*): prioritize delay-sensitive traffic (voice, streaming video). A slow web page is tolerable, a freezing Skype call is not. Dedicated video later. |
| **ECN** (*Explicit Congestion Notification*) | 2 bits | End-to-end congestion notification **without dropping packets** (normally congestion is signalled by drops). Optional: both endpoints and the underlying network must support it. |
| **Total Length** | 16 bits | Total packet length (IPv4 header + Layer 4 segment, header and data) **in bytes**, not in 4-byte increments like IHL. Minimum **20** (header alone, no data), maximum **65,535** (16 bits all 1: 1+2+4+…+32,768). |
| **Identification** | 16 bits | If a packet is **fragmented** (larger than the **MTU**, *Maximum Transmission Unit*, usually **1500 bytes**, related to the maximum Ethernet payload), all its fragments carry the **same value** here so they can be reassembled. Reassembly is done by the **receiving host**. |
| **Flags** | 3 bits | Bit 0: reserved, always 0. Bit 1: **DF** (*Don't Fragment*), set to 1 means the packet must not be fragmented. Bit 2: **MF** (*More Fragments*), 1 if more fragments follow, 0 on the last fragment and on an unfragmented packet. |
| **Fragment Offset** | 13 bits | Position of the fragment within the original packet: allows reassembly even if fragments arrive **out of order**. |
| **Time To Live** (TTL) | 8 bits | A router **drops a packet whose TTL is 0**: prevents infinite loops caused by poor routing configuration (which could eventually congest the network). Designed as a lifetime in seconds, in practice a **hop count**: each router decreases it by 1. Current recommended default: **64**. |
| **Protocol** | 8 bits | Protocol of the encapsulated Layer 4 PDU: **6 = TCP**, **17 = UDP**, **1 = ICMP** (used by ping), **89 = OSPF** (*Open Shortest Path First*, a dynamic routing protocol covered later). Remember these four. |
| **Header Checksum** | 16 bits | Checksum of the **header only**. The router recalculates and compares; if different, it **drops** the packet. Errors in the encapsulated data are detected by the encapsulated protocol (TCP and UDP have their own checksums). |
| **Source IP Address** | 32 bits | IPv4 address of the sender. |
| **Destination IP Address** | 32 bits | IPv4 address of the intended receiver. |
| **Options** | 0 to 320 bits (40 bytes) | Rarely used. Present if **IHL > 5**. Not needed for the CCNA. |

### 3. Reading a Wireshark capture

- Ping between two routers (*echo (ping) request*). Selecting the frame, the Ethernet header, the IP header or the ICMP payload highlights the matching part of the **hexadecimal** representation at the bottom.
- Expanded IPv4 header: Version 0100 = 4; Header Length 0101 = 5 → 20 bytes; *Differentiated Services* field grouping DSCP and ECN, both 0; Total Length **100** (the standard Cisco ping sends **100-byte** packets); Identification 5; Flags: reserved bit *not set* (= 0; *set* = 1), DF not set (fragmentation allowed), MF not set, Fragment Offset 0; TTL **255** (8-bit maximum); Protocol ICMP (1); Header Checksum in hexadecimal (**0x**, each hex digit = 4 bits, 4 digits = 16 bits); source and destination addresses. No options.
- **`ping 192.168.1.2 size 10000`**: 10,000-byte packets, far above the 1500-byte MTU → **IP fragments** shown as "reassembled in #13" (the echo request). Each fragment: Total Length **1500** (MTU size), Identification **1** identical on all, **MF bit set** (not the last), **different Fragment Offset** (0 for the first).
- **`ping ... df-bit`**: DF bit set; with the default 100-byte size, no problem. With a size above the MTU **and** DF, **the pings fail**: too large to be sent whole, not allowed to be fragmented.

### Exam traps

- **IHL is in 4-byte increments** (5 = 20 bytes, 15 = 60 bytes); **Total Length is in bytes** (20 to 65,535).
- IPv4 header: **20 bytes minimum, 60 maximum**; Options at most 40 bytes.
- **TTL = 0 → packet dropped**; it is a hop count, decremented by 1 per router; recommended default 64.
- The **Header Checksum covers only the header**; errors in the data are up to TCP/UDP.
- Protocol numbers: **1 ICMP, 6 TCP, 17 UDP, 89 OSPF**.
- **MF = 1 on every fragment except the last**; Fragment Offset is a 13-bit field, not a bit; "packet fragment bit" does not exist.
- The only variable-length field is **Options**; Total Length and IHL describe variable lengths but are themselves fixed-size.
- IPv4 Version = **0100** in binary.

### IOS commands

```text
R1# ping 192.168.1.2                       ! standard Cisco ping: 100-byte packets, no fragmentation
R1# ping 192.168.1.2 size 10000            ! 10,000-byte packets > 1500 MTU: fragmented into 1500-byte pieces
R1# ping 192.168.1.2 df-bit                ! sets the Don't Fragment bit; fails if the size exceeds the MTU
```

### The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| 1. Fixed binary value of the first field of an IPv4 header? A 0010; B 0110; C 0001; D 0100 | **D, 0100** | The first field is Version; in an IP **version 4** header it is always 4 = 0100. 0110 would be 6 (IPv6). |
| 2. Which field causes the packet to be dropped if its value is 0? A TTL; B DSCP; C IHL; D ECN | **A, TTL** | Time To Live, reduced by 1 at each router; at 0 the packet is dropped. DSCP and ECN at 0 just mean "not used"; IHL cannot be below 5. |
| 3. How are errors in an IPv4 packet's encapsulated data detected? A the Header Checksum; B the encapsulated protocol (TCP, UDP); C they cannot be detected | **B, the encapsulated protocol** | The Header Checksum only checks the IPv4 header; TCP and UDP use their own checksum for the data. |
| 4. Which IPv4 header field is variable in length? A Options; B Header Checksum; C Total Length; D IHL | **A, Options** | 0 to 320 bits. The other fields are fixed-length: Total Length and IHL represent variable lengths, but the fields themselves are always 16 and 4 bits. |
| 5. Which bit is set to 1 on all fragments except the last? A fragment offset bit; B more fragments bit; C don't fragment bit; D packet fragment bit | **B, More Fragments** | In the Flags field, MF indicates the fragment is not the last (0 on the last). Fragment Offset is a 13-bit field, not a bit; DF prevents fragmentation; "packet fragment bit" is not real. |
