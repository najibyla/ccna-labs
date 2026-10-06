# CCNA Day 7 : IPv4 Addressing (Part 1) / Adressage IPv4 (partie 1)

> Source : Jeremy's IT Lab, « Free CCNA | IPv4 Addressing (Part 1) | Day 7 » (40 min), vidéo n°13 de la playlist (cours). Pas de lab pour ce jour : le lab Packet Tracer vient après la partie 2 (Day 8). Fiche rédigée à partir de la transcription le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Rappel : la couche 3 (Network layer)

- Fournit la connectivité entre hôtes finaux de **réseaux différents**, hors du LAN.
- **Adressage logique** (*logical addressing*) : les adresses IP sont **configurées** par l'administrateur, alors que les adresses MAC (couche 2) sont attribuées à la fabrication.
- **Sélection de chemin** (*path selection*) : sur un grand réseau comme Internet, il existe plusieurs chemins possibles ; choisir le meilleur est une fonction de la couche 3.
- Les **routeurs** opèrent à la couche 3.

### 2. Un switch étend un réseau, un routeur en sépare

- Des switches ne séparent pas les réseaux : ils les **connectent et les étendent**. Quatre PC reliés par SW1 et SW2 forment un seul LAN, 192.168.1.0/24 (PC1 = 192.168.1.1, PC2 = .2, PC3 = .3, PC4 = .4). Un broadcast de PC1 (MAC destination tout F) est transmis par SW1 puis SW2 sur tous les ports sauf celui d'arrivée : tous les PC le reçoivent.
- Avec un **routeur R1 entre SW1 et SW2**, on obtient deux réseaux : 192.168.1.0/24 (SW1, PC1, PC2) et 192.168.2.0/24 (SW2, PC3 = 192.168.2.1, PC4 = 192.168.2.2).
- Le routeur a besoin d'**une adresse IP par réseau connecté** : G0/0 = 192.168.1.254, G0/1 = 192.168.2.254.
- Un broadcast envoyé par R1 sur G0/0 atteint PC2 et… s'arrête là : **le broadcast reste dans le réseau local, il ne traverse pas le routeur**.

### 3. L'adresse IPv4 : 32 bits en « dotted decimal »

- Dans l'en-tête IPv4, les champs *source IP address* et *destination IP address* font chacun **32 bits = 4 octets**.
- Une adresse est écrite en **décimal pointé** (*dotted decimal*) : quatre nombres séparés par des points, chacun représentant **8 bits**. 192.168.1.254 = 11000000.10101000.00000001.11111110.
- Chaque groupe de 8 bits s'appelle un **octet** (*octet*). Un octet va de **0** (tous les bits à 0) à **255** (tous à 1 : 128+64+32+16+8+4+2+1).

### 4. Décimal, hexadécimal, binaire

- **Décimal** (base 10) : chaque position vaut 10 fois la précédente. 3294 = 3×1000 + 2×100 + 9×10 + 4.
- **Hexadécimal** (base 16) : 3294 s'écrit **CDE** : E (14)×1 + D (13)×16 = 208 + C (12)×256 = 3072 ; total 3294.
- **Binaire** (base 2) : chaque position double. Valeurs d'un octet, de gauche à droite : **128 64 32 16 8 4 2 1**.
  - 192 = 11000000 (128+64) ; 168 = 10101000 (128+32+8) ; 1 = 00000001 ; 254 = 11111110 (128+64+32+16+8+4+2).

### 5. Convertir binaire → décimal

Écrire la valeur de chaque bit au-dessus de l'octet (1 à droite puis ×2 vers la gauche, ou 128 à gauche puis ÷2), puis **additionner les valeurs des bits à 1**.

- 10001111 = 128+8+4+2+1 = **143**
- 01110110 = 64+32+16+4+2 = **118**
- 11101100 = 128+64+32+8+4 = **236**

### 6. Convertir décimal → binaire

Écrire 128 64 32 16 8 4 2 1, puis de gauche à droite : si on peut soustraire la valeur sans passer en négatif, écrire 1 et soustraire ; sinon écrire 0.

- 127 : pas de 128 → 0 ; 64 → 63 ; 32 → 31 ; 16 → 15 ; 8 → 7 ; 4 → 3 ; 2 → 1 ; 1 → 0. **127 = 01111111**.
- 207 : 128 → 79 ; 64 → 15 ; pas de 32, pas de 16 ; 8 → 7 ; 4 → 3 ; 2 → 1 ; 1 → 0. **207 = 11001111**.
- 221 : **erratum signalé dans la transcription**. Jeremy annonce 93−64 = 28 (au lieu de 29) et conclut 11011100, ce qui est faux. Le bon résultat est **221 = 11011101** (128+64+16+8+4+1).

### 7. Partie réseau et partie hôte : la longueur de préfixe

- **/24** signifie que les **24 premiers bits** (3 octets) sont la partie réseau (*network portion*), les 8 derniers la partie hôte (*host portion*). Dans 192.168.1.254/24 : réseau 192.168.1, hôte 254.
- Les hôtes d'un même LAN ont la **même partie réseau** et une partie hôte différente : PC1, PC2 et R1 G0/0 sont 192.168.1.1/24, 192.168.1.2/24 et 192.168.1.254/24.
- Exemples avec d'autres préfixes : 154.78.111.32**/16** → réseau 154.78, hôte 111.32 ; 12.128.251.23**/8** → réseau 12, hôte 128.251.23.

### 8. Les classes d'adresses

La classe est déterminée par le **premier octet**.

| Classe | Premiers bits | Premier octet | Préfixe | Usage |
| :--- | :--- | :--- | :--- | :--- |
| A | 0 | 0 à 127 | /8 | unicast |
| B | 10 | 128 à 191 | /16 | unicast |
| C | 110 | 192 à 223 | /24 | unicast |
| D | 1110 | 224 à 239 | — | réservée au **multicast** (vu plus tard) |
| E | 1111 | 240 à 255 | — | réservée aux usages expérimentaux (hors cours) |

- Le cours se concentre sur A, B et C.
- **La fin de la classe A est en général considérée comme 126, pas 127** : la plage 127 (127.0.0.0 à 127.255.255.255) est réservée aux **adresses de loopback**, qui servent à tester la **pile réseau** (*network stack*) de la machine elle-même. Un ping vers 127.0.0.1 (ou n'importe quelle adresse en 127, par exemple 127.23.68.241) est traité en remontant la pile TCP/IP comme s'il venait d'une autre machine : le PC se répond à lui-même, temps aller-retour **0 ms**.
- Nombre de réseaux et d'hôtes (tableau Wikipédia) : classe A, **128 réseaux** et environ **16,7 millions d'hôtes** par réseau ; classe B, environ **16 000 réseaux** et **65 000 hôtes** ; classe C, environ **2 millions de réseaux** et **256 adresses** par réseau. Comme la première adresse (réseau) et la dernière (broadcast) ne sont pas assignables, le nombre d'hôtes réel est **deux de moins** : 254 en classe C.

### 9. Deux écritures de la longueur de préfixe

- La notation **/N** (slash) est la plus récente et la plus simple ; les équipements **Juniper** l'utilisent.
- Les équipements **Cisco** utilisent encore le **masque de réseau en décimal pointé** (*dotted decimal netmask*) : partie réseau à 1, partie hôte à 0.
  - Classe A, /8 = **255.0.0.0** ; classe B, /16 = **255.255.0.0** ; classe C, /24 = **255.255.255.0**.
- Préfixe et masque sont **la même chose écrite différemment**.

### 10. Adresse réseau et adresse de broadcast

- **Adresse réseau** (*network address*) : partie hôte **tout à 0**. 192.168.1.0/24 identifie le réseau lui-même ; **non assignable** à un hôte. La **première adresse utilisable** est juste au-dessus : 192.168.1.1 (PC1).
- **Adresse de broadcast** : partie hôte **tout à 1**, 192.168.1.255 ; **non assignable**. La **dernière adresse utilisable** est juste en dessous : 192.168.1.254 (R1 G0/0).
- Un paquet envoyé à l'adresse de broadcast de couche 3 est encapsulé dans une trame dont la MAC destination est **FFFF.FFFF.FFFF**. Un ping de PC1 vers 192.168.1.255 est reçu par PC2 et par R1 G0/0.

### Pièges d'examen

- Un **broadcast ne traverse jamais un routeur** ; il est limité au réseau local.
- Classe A : retenir **0 à 127** d'après les premiers bits, mais la plage **127 est réservée au loopback**, donc la fin utile est 126.
- **Adresse réseau et adresse de broadcast ne sont jamais assignées** à un hôte : hôtes utilisables = total − 2 (254 en classe C).
- /24 et 255.255.255.0 sont **identiques** ; Cisco attend le masque en décimal pointé.
- Le décimal pointé n'est qu'une écriture pour les humains : l'adresse reste **32 bits**.
- Erratum de la vidéo : 221 = 11011101, pas 11011100.

### Le quiz (10 questions, conversion uniquement)

Jeremy annonce 10 questions au lieu de 5, toutes sur la conversion binaire ↔ décimal pointé. Les écritures binaires sont affichées à l'écran et non lues dans la transcription : elles ont été **reconstituées par calcul** à partir des valeurs décimales dites par Jeremy.

| N° | Énoncé | Réponse |
| :--- | :--- | :--- |
| 1 | 00111111.00111000.11100111.00010011 → décimal | **63.56.231.19** |
| 2 | 11110011.01111111.01100010.00000001 → décimal | **243.127.98.1** |
| 3 | 01101111.00000110.01011001.11000111 → décimal | **111.6.89.199** |
| 4 | 11001111.11000110.00101111.01001100 → décimal | **207.198.47.76** |
| 5 | 01100100.11001001.00100001.11111101 → décimal | **100.201.33.253** |
| 6 | 88.46.90.91 → binaire | **01011000.00101110.01011010.01011011** |
| 7 | 221.234.246.163 → binaire | **11011101.11101010.11110110.10100011** |
| 8 | 3.41.143.222 → binaire | **00000011.00101001.10001111.11011110** |
| 9 | 10.200.231.91 → binaire | **00001010.11001000.11100111.01011011** |
| 10 | 248.87.255.152 → binaire | **11111000.01010111.11111111.10011000** |

---

## 🇬🇧 English version

### 1. Review: Layer 3 (Network layer)

- Provides connectivity between end hosts on **different networks**, outside the LAN.
- **Logical addressing**: IP addresses are **configured** by the administrator, whereas MAC addresses (Layer 2) are assigned when the device is made.
- **Path selection**: on large networks such as the Internet there are many possible paths; selecting the best one is a Layer 3 function.
- **Routers** operate at Layer 3.

### 2. Switches expand a network, routers separate networks

- Switches do not separate networks: they **connect and expand** them. Four PCs linked by SW1 and SW2 form one LAN, 192.168.1.0/24 (PC1 = 192.168.1.1, PC2 = .2, PC3 = .3, PC4 = .4). A broadcast from PC1 (destination MAC all Fs) is forwarded by SW1 then SW2 out of every port except the one it arrived on: all PCs receive it.
- With **router R1 between SW1 and SW2**, there are two networks: 192.168.1.0/24 (SW1, PC1, PC2) and 192.168.2.0/24 (SW2, PC3 = 192.168.2.1, PC4 = 192.168.2.2).
- The router needs **one IP address per connected network**: G0/0 = 192.168.1.254, G0/1 = 192.168.2.254.
- A broadcast sent by R1 on G0/0 reaches PC2 and that is where it ends: **the broadcast is limited to the local network, it does not cross the router**.

### 3. The IPv4 address: 32 bits written in dotted decimal

- In the IPv4 header, the *source IP address* and *destination IP address* fields are each **32 bits = 4 bytes** long.
- An address is written in **dotted decimal**: four decimal numbers separated by dots, each representing **8 bits**. 192.168.1.254 = 11000000.10101000.00000001.11111110.
- Each 8-bit group is called an **octet**. An octet ranges from **0** (all bits 0) to **255** (all bits 1: 128+64+32+16+8+4+2+1).

### 4. Decimal, hexadecimal, binary

- **Decimal** (base 10): each digit increases by a factor of 10. 3294 = 3×1000 + 2×100 + 9×10 + 4.
- **Hexadecimal** (base 16): 3294 is written **CDE**: E (14)×1 + D (13)×16 = 208 + C (12)×256 = 3072; total 3294.
- **Binary** (base 2): each digit doubles. Bit values of an octet, left to right: **128 64 32 16 8 4 2 1**.
  - 192 = 11000000 (128+64); 168 = 10101000 (128+32+8); 1 = 00000001; 254 = 11111110 (128+64+32+16+8+4+2).

### 5. Converting binary to decimal

Write the value of each bit above the octet (start with 1 on the right and multiply by 2 leftwards, or 128 on the left and divide by 2 rightwards), then **add up the values of the 1 bits**.

- 10001111 = 128+8+4+2+1 = **143**
- 01110110 = 64+32+16+4+2 = **118**
- 11101100 = 128+64+32+8+4 = **236**

### 6. Converting decimal to binary

Write 128 64 32 16 8 4 2 1, then from left to right: if the value can be subtracted without going negative, write 1 and subtract; otherwise write 0.

- 127: no 128 → 0; 64 → 63; 32 → 31; 16 → 15; 8 → 7; 4 → 3; 2 → 1; 1 → 0. **127 = 01111111**.
- 207: 128 → 79; 64 → 15; no 32, no 16; 8 → 7; 4 → 3; 2 → 1; 1 → 0. **207 = 11001111**.
- 221: **erratum flagged in the transcript**. Jeremy says 93−64 = 28 (instead of 29) and ends with 11011100, which is wrong. The correct answer is **221 = 11011101** (128+64+16+8+4+1).

### 7. Network portion and host portion: the prefix length

- **/24** means the **first 24 bits** (3 octets) are the network portion and the remaining 8 are the host portion. In 192.168.1.254/24: network 192.168.1, host 254.
- Hosts on the same LAN share the **same network portion** and have different host portions: PC1, PC2 and R1 G0/0 are 192.168.1.1/24, 192.168.1.2/24 and 192.168.1.254/24.
- Other prefix lengths: 154.78.111.32**/16** → network 154.78, host 111.32; 12.128.251.23**/8** → network 12, host 128.251.23.

### 8. Address classes

The class is determined by the **first octet**.

| Class | Leading bits | First octet | Prefix | Use |
| :--- | :--- | :--- | :--- | :--- |
| A | 0 | 0 to 127 | /8 | unicast |
| B | 10 | 128 to 191 | /16 | unicast |
| C | 110 | 192 to 223 | /24 | unicast |
| D | 1110 | 224 to 239 | — | reserved for **multicast** (covered later) |
| E | 1111 | 240 to 255 | — | reserved for experimental use (not covered) |

- The course focuses on classes A, B and C.
- **The end of the class A range is usually considered 126, not 127**: the 127 range (127.0.0.0 to 127.255.255.255) is reserved for **loopback addresses**, used to test the **network stack** of the local device. A ping to 127.0.0.1 (or any 127 address, e.g. 127.23.68.241) is processed back up the TCP/IP stack as if received from another device: the PC replies to itself, round-trip time **0 ms**.
- Numbers of networks and hosts (Wikipedia chart): class A, **128 networks** and about **16.7 million hosts** per network; class B, about **16,000 networks** and **65,000 hosts**; class C, about **2 million networks** and **256 addresses** per network. Because the first address (network) and the last (broadcast) cannot be assigned, the real host count is **two less**: 254 in class C.

### 9. Two ways of writing the prefix length

- The **/N** (slash) notation is newer and easier; **Juniper** devices use it.
- **Cisco** devices still use the older **dotted decimal netmask**: network portion all 1s, host portion all 0s.
  - Class A, /8 = **255.0.0.0**; class B, /16 = **255.255.0.0**; class C, /24 = **255.255.255.0**.
- Prefix length and netmask are **the same thing written differently**.

### 10. Network address and broadcast address

- **Network address**: host portion **all 0s**. 192.168.1.0/24 identifies the network itself; it **cannot be assigned** to a host. The **first usable address** is one above it: 192.168.1.1 (PC1).
- **Broadcast address**: host portion **all 1s**, 192.168.1.255; **cannot be assigned**. The **last usable address** is one below it: 192.168.1.254 (R1 G0/0).
- A packet sent to the Layer 3 broadcast address is encapsulated in a frame whose destination MAC is **FFFF.FFFF.FFFF**. A ping from PC1 to 192.168.1.255 is received by PC2 and R1 G0/0.

### Exam traps

- A **broadcast never crosses a router**; it is limited to the local network.
- Class A: remember **0 to 127** from the leading bit, but the **127 range is reserved for loopback**, so the usable end is 126.
- **Network and broadcast addresses are never assigned** to hosts: usable hosts = total − 2 (254 in class C).
- /24 and 255.255.255.0 are **identical**; Cisco expects the dotted decimal netmask.
- Dotted decimal is only a human-friendly notation: the address is still **32 bits**.
- Video erratum: 221 = 11011101, not 11011100.

### The quiz (10 questions, conversion only)

Jeremy gives 10 questions instead of 5, all on converting between binary and dotted decimal. The binary strings are shown on screen and not read aloud in the transcript: they were **reconstructed by calculation** from the decimal values Jeremy states.

| # | Question | Answer |
| :--- | :--- | :--- |
| 1 | 00111111.00111000.11100111.00010011 → decimal | **63.56.231.19** |
| 2 | 11110011.01111111.01100010.00000001 → decimal | **243.127.98.1** |
| 3 | 01101111.00000110.01011001.11000111 → decimal | **111.6.89.199** |
| 4 | 11001111.11000110.00101111.01001100 → decimal | **207.198.47.76** |
| 5 | 01100100.11001001.00100001.11111101 → decimal | **100.201.33.253** |
| 6 | 88.46.90.91 → binary | **01011000.00101110.01011010.01011011** |
| 7 | 221.234.246.163 → binary | **11011101.11101010.11110110.10100011** |
| 8 | 3.41.143.222 → binary | **00000011.00101001.10001111.11011110** |
| 9 | 10.200.231.91 → binary | **00001010.11001000.11100111.01011011** |
| 10 | 248.87.255.152 → binary | **11111000.01010111.11111111.10011000** |
