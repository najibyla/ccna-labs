# CCNA Day 13 : Subnetting (Part 1) / Sous-réseaux, partie 1

> Source : Jeremy's IT Lab, « Free CCNA | Subnetting (Part 1) | Day 13 » (29 min), vidéo n°25 de la playlist. Pas de lab pour ce jour (le lab de subnetting arrive au Day 15), flashcards disponibles. Fiche rédigée à partir de la transcription le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Rappel : les classes d'adresses IPv4 (adressage « classful »)

Une adresse IPv4 fait 32 bits, soit 4 octets de 8 bits. La classe est donnée par les premiers bits du premier octet.

| Classe | Premiers bits | 1er octet | Plage d'adresses | Préfixe | Nombre de réseaux | Adresses par réseau |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A | 0 | 0 à 127 | 0.0.0.0 à 127.255.255.255 | /8 | 128 (moins les réservés, ex. 127.0.0.0/8 loopback) | 16 777 216 (2^24) |
| B | 10 | 128 à 191 | 128.0.0.0 à 191.255.255.255 | /16 | 16 384 | 65 536 |
| C | 110 | 192 à 223 | 192.0.0.0 à 223.255.255.255 | /24 | 2 097 152 | 256 |
| D | 1110 | 224 à 239 | 224.0.0.0 à 239.255.255.255 | – | usage spécial (multicast) | – |
| E | 1111 | 240 à 255 | 240.0.0.0 à 255.255.255.255 | – | usage spécial | – |

- Seules les classes A, B et C peuvent être attribuées à des équipements.
- /8 : le premier octet identifie le réseau, les trois autres les hôtes. /16 : deux octets réseau, deux octets hôtes. /24 : trois octets réseau, un octet hôtes.
- Les adresses sont attribuées aux organisations par l'**IANA** (*Internet Assigned Numbers Authority*), société américaine à but non lucratif, selon la taille de l'organisation : classe A ou B pour les grandes, classe C pour les petites.

### 2. Le problème : le gaspillage d'adresses

- **Liaison point à point** (*point-to-point network*) entre R1 et R2 (San Francisco ↔ New York) avec un réseau de classe C 203.0.113.0/24 : 256 adresses, moins l'adresse réseau 203.0.113.0, moins l'adresse de broadcast 203.0.113.255, moins R1 (203.0.113.1), moins R2 (203.0.113.2). **4 adresses utilisées, 252 gaspillées.**
- **Entreprise X** avec 5 000 hôtes : une classe C ne suffit pas, il faut une classe B (environ 65 000 adresses), soit **environ 60 000 adresses gaspillées**.
- L'espace IPv4 total dépasse 4 milliards d'adresses, ce qui semblait énorme à la création d'IPv4, mais l'**épuisement des adresses** (*address space exhaustion*) est aujourd'hui un vrai problème.

### 3. CIDR (*Classless Inter-Domain Routing*)

- Introduit par l'**IETF** (*Internet Engineering Task Force*) en **1993** pour remplacer l'adressage « classful ».
- Supprime l'obligation « classe A = /8, classe B = /16, classe C = /24 » : un grand réseau peut être découpé en réseaux plus petits, les **sous-réseaux** (*subnetworks*, *subnets*).
- La notation « /25, /26… » (barre oblique + longueur de préfixe) s'appelle **notation CIDR**. Avant, seule la notation décimale pointée (*dotted decimal*) du masque existait.

### 4. La méthode de calcul : combien d'adresses utilisables ?

- Dans le masque de réseau (*network mask*, *subnet mask*), tous les bits à **1** marquent la **partie réseau** de l'adresse ; les bits à **0** marquent la **partie hôte**.
- **Formule : 2^(nombre de bits hôte) − 2 = adresses utilisables.** Le « −2 » retire l'adresse réseau et l'adresse de broadcast, qu'on ne peut pas attribuer à un équipement.
- Exemple 203.0.113.0/24, masque 255.255.255.0 : 8 bits hôte, 2^8 − 2 = **254** adresses utilisables, alors qu'on en a besoin de 2.

Exercice de la vidéo : la même adresse 203.0.113.0 avec un préfixe de plus en plus long.

| Préfixe | Masque décimal pointé | Bits hôte | Adresses utilisables | Gaspillées pour la liaison point à point |
| :--- | :--- | :--- | :--- | :--- |
| /24 | 255.255.255.0 | 8 | 254 | 252 |
| /25 | 255.255.255.128 | 7 | 126 | 124 |
| /26 | 255.255.255.192 | 6 | 62 | 60 |
| /27 | 255.255.255.224 | 5 | 30 | – |
| /28 | 255.255.255.240 | 4 | 14 | 12 |
| /29 | 255.255.255.248 | 3 | 6 | 4 |
| /30 | 255.255.255.252 | 2 | 2 | **0** |
| /31 | 255.255.255.254 | 1 | 0 selon la formule | cas spécial |
| /32 | 255.255.255.255 | 0 | −1 selon la formule | cas spécial |

- **/30 pour une liaison point à point** : 4 adresses au total, 203.0.113.0 (réseau), 203.0.113.1 (R1), 203.0.113.2 (R2), 203.0.113.3 (broadcast). Zéro gaspillage. Les adresses restantes du bloc, 203.0.113.4 à 203.0.113.255, sont disponibles pour d'autres sous-réseaux : c'est « la magie du subnetting ».
- **/31** : 2^1 − 2 = 0 adresse utilisable, donc longtemps inutilisable. Mais sur une liaison point à point dédiée entre deux routeurs, **on n'a besoin ni d'adresse réseau ni de broadcast** : on attribue les deux seules adresses, 203.0.113.0 à R1 et 203.0.113.1 à R2. Un routeur Cisco affiche un avertissement rappelant de vérifier qu'il s'agit bien d'une liaison point à point, mais la configuration est valide. Les adresses 203.0.113.2 à 255 restent disponibles. /30 reste utilisé, mais Jeremy **recommande /31**, plus efficace.
- **/32** : toute l'adresse est la partie réseau, aucun bit hôte. On ne configure pratiquement jamais une interface en /32, mais ce masque sert par exemple à écrire une **route statique vers un hôte précis** (vu plus tard dans le cours).

### 5. Deuxième exemple : découper 192.168.1.0/24 en 4 sous-réseaux

Scénario : 4 réseaux connectés à R1, **45 hôtes par réseau, adresse de R1 comprise**.

1. Y a-t-il assez d'adresses ? 45 hôtes + adresse réseau + broadcast = **47 adresses par sous-réseau** ; 47 × 4 = **188** ≤ 256 adresses d'une classe C : oui.
2. Chercher le préfixe en partant de /30 (/31 et /32 exclus, ce ne sont pas des liaisons point à point) :
   - /30 : 2 bits hôte, 2^2 − 2 = 4 − 2 = **2**, insuffisant.
   - /29 : 3 bits hôte, 2^3 − 2 = 8 − 2 = **6**, insuffisant.
   - /28 : 4 bits hôte, 2^4 − 2 = 16 − 2 = **14**, insuffisant.
   - /27 : 5 bits hôte, 2^5 − 2 = 32 − 2 = **30**, insuffisant.
   - /26 : 6 bits hôte, 2^6 − 2 = 64 − 2 = **62** : suffisant.
3. **Sous-réseau 1 = 192.168.1.0/26.** On ne peut pas toujours tomber exactement sur le nombre voulu ; l'espace inutilisé laisse de la marge pour la croissance, ce qui est bien.

### 6. Pièges d'examen

- **Toujours −2** pour l'adresse réseau et le broadcast (sauf /31 point à point).
- /31 est **valide et recommandé** pour une liaison point à point entre deux routeurs ; /32 sert aux routes vers un hôte, pas aux interfaces.
- Savoir **convertir binaire ↔ décimal pointé** est indispensable : « révisez-le si vous ne vous en souvenez pas ».
- Compter l'adresse du routeur parmi les hôtes nécessaires, puis ajouter 2.

### 7. Le quiz du Day 13 (1 exercice, corrigé au Day 14)

| Question | Réponse (donnée au Day 14) | Méthode |
| :--- | :--- | :--- |
| Le sous-réseau 1 est 192.168.1.0/26. Quels sont les sous-réseaux 2, 3 et 4 ? | **192.168.1.64/26, 192.168.1.128/26, 192.168.1.192/26** | Indice de Jeremy : trouver l'adresse de broadcast du sous-réseau 1 (192.168.1.63) ; l'adresse suivante est l'adresse réseau du sous-réseau 2 ; répéter. |

---

## 🇬🇧 English version

### 1. Review: IPv4 address classes (classful addressing)

An IPv4 address is 32 bits, 4 octets of 8 bits. The class is given by the first bits of the first octet.

| Class | First bits | 1st octet | Address range | Prefix | Number of networks | Addresses per network |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A | 0 | 0 to 127 | 0.0.0.0 to 127.255.255.255 | /8 | 128 (fewer, some reserved, e.g. 127.0.0.0/8 loopback) | 16,777,216 (2^24) |
| B | 10 | 128 to 191 | 128.0.0.0 to 191.255.255.255 | /16 | 16,384 | 65,536 |
| C | 110 | 192 to 223 | 192.0.0.0 to 223.255.255.255 | /24 | 2,097,152 | 256 |
| D | 1110 | 224 to 239 | 224.0.0.0 to 239.255.255.255 | – | special purpose | – |
| E | 1111 | 240 to 255 | 240.0.0.0 to 255.255.255.255 | – | special purpose | – |

- Only classes A, B and C can be assigned to devices.
- /8: first octet identifies the network, the other three the hosts. /16: two network octets, two host octets. /24: three network octets, one host octet.
- Addresses are assigned to organizations by the **IANA** (Internet Assigned Numbers Authority), a non-profit American corporation, according to size: class A or B for large companies, class C for small ones.

### 2. The problem: wasted addresses

- **Point-to-point network** between R1 and R2 (San Francisco and New York) using class C 203.0.113.0/24: 256 addresses, minus the network address 203.0.113.0, minus the broadcast address 203.0.113.255, minus R1 (203.0.113.1), minus R2 (203.0.113.2). **4 addresses used, 252 wasted.**
- **Company X** needs 5,000 hosts: a class C is not enough, so a class B (about 65,000 addresses) must be assigned, **about 60,000 addresses wasted**.
- The total IPv4 space is over 4 billion addresses, which seemed huge when IPv4 was created, but **address space exhaustion** is now a big problem.

### 3. CIDR (Classless Inter-Domain Routing)

- Introduced by the **IETF** (Internet Engineering Task Force) in **1993** to replace classful addressing.
- Removes the requirement "class A must use /8, class B /16, class C /24": larger networks can be split into smaller ones called **subnetworks** or **subnets**.
- Writing a prefix as "/25, /26..." is called **CIDR notation**. Previously only the dotted decimal mask was used.

### 4. The calculation method: how many usable addresses?

- In the **network mask** (subnet mask), all **1** bits mark the **network portion** of the address; **0** bits mark the **host portion**.
- **Formula: 2^(number of host bits) − 2 = usable addresses.** The "−2" removes the network address and broadcast address, which cannot be assigned to a device.
- Example 203.0.113.0/24, mask 255.255.255.0: 8 host bits, 2^8 − 2 = **254** usable addresses, when we only need 2.

Video exercise: the same 203.0.113.0 with a longer and longer prefix.

| Prefix | Dotted decimal mask | Host bits | Usable addresses | Wasted on the point-to-point link |
| :--- | :--- | :--- | :--- | :--- |
| /24 | 255.255.255.0 | 8 | 254 | 252 |
| /25 | 255.255.255.128 | 7 | 126 | 124 |
| /26 | 255.255.255.192 | 6 | 62 | 60 |
| /27 | 255.255.255.224 | 5 | 30 | – |
| /28 | 255.255.255.240 | 4 | 14 | 12 |
| /29 | 255.255.255.248 | 3 | 6 | 4 |
| /30 | 255.255.255.252 | 2 | 2 | **0** |
| /31 | 255.255.255.254 | 1 | 0 by the formula | special case |
| /32 | 255.255.255.255 | 0 | −1 by the formula | special case |

- **/30 for a point-to-point link**: 4 addresses in total, 203.0.113.0 (network), 203.0.113.1 (R1), 203.0.113.2 (R2), 203.0.113.3 (broadcast). Zero waste. The remaining addresses of the block, 203.0.113.4 to 203.0.113.255, are available for other subnets: "that's the magic of subnetting".
- **/31**: 2^1 − 2 = 0 usable addresses, so it used to be unusable. But on a dedicated point-to-point connection between two routers **there is no need for a network address or a broadcast address**: assign the only two addresses, 203.0.113.0 to R1 and 203.0.113.1 to R2. A Cisco router shows a warning reminding you to make sure it is a point-to-point link, but the configuration is totally valid. 203.0.113.2 to 255 remain available. /30 is still used, but Jeremy **recommends /31**, which is more efficient.
- **/32**: the entire address is the network portion, no host bits. You will probably never configure an interface with /32, but it is used, for example, for a **static route to one specific host** (covered later in the course).

### 5. Second example: dividing 192.168.1.0/24 into 4 subnets

Scenario: 4 networks connected to R1, **45 hosts per network, R1's address included**.

1. Are there enough addresses? 45 hosts + network address + broadcast = **47 addresses per subnet**; 47 × 4 = **188** ≤ 256 addresses in a class C: yes.
2. Find the prefix starting from /30 (/31 and /32 skipped, these are not point-to-point links):
   - /30: 2 host bits, 2^2 − 2 = 4 − 2 = **2**, not enough.
   - /29: 3 host bits, 2^3 − 2 = 8 − 2 = **6**, not enough.
   - /28: 4 host bits, 2^4 − 2 = 16 − 2 = **14**, not enough.
   - /27: 5 host bits, 2^5 − 2 = 32 − 2 = **30**, not enough.
   - /26: 6 host bits, 2^6 − 2 = 64 − 2 = **62**: enough.
3. **Subnet 1 = 192.168.1.0/26.** You cannot always make subnets with exactly the number of addresses you want; unused space leaves room for growth, which is fine.

### 6. Exam traps

- **Always −2** for the network and broadcast addresses (except /31 point-to-point).
- /31 is **valid and recommended** for a point-to-point link between two routers; /32 is for host routes, not interfaces.
- **Binary to dotted decimal conversion** is essential: "make sure you review that".
- Count the router's address among the required hosts, then add 2.

### 7. Day 13 quiz (1 exercise, solved in Day 14)

| Question | Answer (given in Day 14) | Method |
| :--- | :--- | :--- |
| Subnet 1 is 192.168.1.0/26. What are the remaining subnets 2, 3 and 4? | **192.168.1.64/26, 192.168.1.128/26, 192.168.1.192/26** | Jeremy's hint: find the broadcast address of subnet 1 (192.168.1.63); the next address is the network address of subnet 2; repeat. |
