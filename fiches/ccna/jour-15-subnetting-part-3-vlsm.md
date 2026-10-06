# CCNA Day 15 : Subnetting (Part 3, VLSM) / Sous-réseaux, partie 3, VLSM

> Source : Jeremy's IT Lab, « Free CCNA | Subnetting (Part 3 - VLSM) | Day 15 » (24 min, vidéo n°27 de la playlist, cours) et « Subnetting (VLSM) | Day 15 Lab » (15 min, vidéo n°28, lab Packet Tracer). Pas de quiz ni de flashcards pour ce jour : devoir à la place (voir section 5). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Corrigé du quiz du Day 14

Voir la fiche `jour-14-subnetting-part-2.md`, section 7 : /23 ; 172.21.96.0/20 ; 192.168.91.127 ; 172.16.64.0 et 172.16.127.255 ; 64 sous-réseaux.

### 2. Classe A : même méthode, nombres plus grands

La classe A a **24 bits hôte** (champ « size of rest bit field ») : beaucoup de place pour créer des sous-réseaux. Le procédé est **exactement le même** qu'en classe B ou C.

**Exercice 1** : 10.0.0.0/8 (masque 255.0.0.0), créer **2 000 sous-réseaux** pour diverses entreprises. Préfixe ? Hôtes par sous-réseau ?

- 2 à la puissance combien donne au moins 2 000 ? En doublant : 2, 4, 8, 16, 32, 64, 128, 256, 512, 1 024, **2 048** → **11 bits empruntés** (2^11).
- 8 + 11 = **/19**.
- Il reste 32 − 19 = **13 bits hôte** → 2^13 − 2 = **8 190 hôtes** (adresses utilisables) par sous-réseau.

**Exercice 2** : PC1 a l'adresse **10.217.182.223/11**. Trouver pour son sous-réseau :

| Élément | Méthode | Réponse |
| :--- | :--- | :--- |
| Adresse réseau | /11 = 3 bits empruntés sur le /8 ; bits hôte à 0 | **10.192.0.0** |
| Première adresse utilisable | adresse réseau + 1 | **10.192.0.1** |
| Adresse de broadcast | bits hôte à 1 | **10.223.255.255** |
| Dernière adresse utilisable | broadcast − 1 | **10.223.255.254** |
| Nombre d'adresses utilisables | 21 bits hôte → 2^21 − 2 | **2 097 150** |

La conversion binaire ↔ décimal pointé est « absolument essentielle » pour le subnetting.

### 3. FLSM contre VLSM

- **FLSM** (*Fixed-Length Subnet Masks*) : tous les sous-réseaux ont la même longueur de préfixe (ce qu'on a fait jusqu'ici, par exemple une classe C en 4 × /26).
- **VLSM** (*Variable-Length Subnet Masks*) : créer des sous-réseaux **de tailles différentes** pour utiliser l'espace d'adressage plus efficacement. Plus compliqué que FLSM, mais facile si on suit les étapes.

**Les étapes VLSM** : 1) attribuer le **plus grand** sous-réseau au **début** de l'espace d'adressage ; 2) attribuer le deuxième plus grand juste après ; 3) répéter, du plus grand au plus petit, jusqu'au dernier.

### 4. L'exemple complet : 192.168.1.0/24 pour Tokyo et Toronto

Besoins : Tokyo LAN A **110 hôtes**, Tokyo LAN B **8 hôtes**, Toronto LAN A **29 hôtes**, Toronto LAN B **45 hôtes**, plus la **liaison point à point** entre les deux routeurs. 5 sous-réseaux au total.

- Avec FLSM : 5 sous-réseaux → 3 bits empruntés → 5 bits hôte → **30 hôtes** seulement, insuffisant pour Tokyo LAN A et Toronto LAN B. D'où VLSM.
- Ordre d'attribution : Tokyo LAN A, Toronto LAN B, Toronto LAN A, Tokyo LAN B, point à point.

| Ordre | Sous-réseau | Besoin | Préfixe | Adresse réseau | Broadcast | 1re utilisable | Dernière utilisable | Utilisables |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Tokyo LAN A | 110 | /25 (7 bits hôte, 128 adresses) | 192.168.1.0 | 192.168.1.127 | 192.168.1.1 | 192.168.1.126 | 126 |
| 2 | Toronto LAN B | 45 | /26 (/27 ne donnerait que 30) | 192.168.1.128 | 192.168.1.191 | 192.168.1.129 | 192.168.1.190 | 62 |
| 3 | Toronto LAN A | 29 | /27 (5 bits hôte) | 192.168.1.192 | 192.168.1.223 | 192.168.1.193 | 192.168.1.222 | 30 |
| 4 | Tokyo LAN B | 8 | /28 (**pas /29** : 8 adresses mais 6 utilisables) | 192.168.1.224 | 192.168.1.239 | 192.168.1.225 | 192.168.1.238 | 14 |
| 5 | Point à point | 2 | /30 | 192.168.1.240 | 192.168.1.243 | 192.168.1.241 | 192.168.1.242 | 2 |

- Chaque adresse réseau = broadcast du sous-réseau précédent + 1.
- Le /25 consomme la moitié de l'espace, le /26 un quart de plus (trois quarts utilisés après deux sous-réseaux) : « pas de problème », les petits sous-réseaux tiennent dans le reste, et il reste même un peu d'espace à la fin.
- **Pour la liaison point à point à l'examen CCNA** : /31 est possible, mais Jeremy recommande de **ne pas répondre /31** à une question « quel préfixe pour 2 hôtes ? » ; la réponse attendue est **/30**.

### 5. Devoir (à la place du quiz)

Trois sites d'entraînement cités par Jeremy : subnettingquestions.com, subnetting.org et subnettingpractice.com (son préféré, questions plus difficiles qui vont au-delà de celles des vidéos). **Faire au moins UNE question de CHAQUE site chaque jour pendant au moins une semaine.**

### 6. Pièges d'examen

- Le piège /29 contre /28 pour 8 hôtes : 2^3 = 8 adresses, mais **6** utilisables → il faut /28.
- Le routeur a besoin d'une adresse dans chaque sous-réseau.
- Répondre /30 (pas /31) pour une liaison à 2 hôtes à l'examen.
- Dans la vraie vie, garder de la marge pour la croissance ; **à l'examen, faire exactement ce que dit l'énoncé** (le lab utilise un /28 pour exactement 14 hôtes).

### 7. Commandes IOS

```
Router> enable                                   ! mode privilégié
Router# configure terminal                       ! mode de configuration globale
Router(config)# interface g0/1                   ! configurer une interface
Router(config-if)# ip address 192.168.5.126 255.255.255.128   ! adresse + masque décimal pointé (/25)
Router(config-if)# no shutdown                   ! activer l'interface
Router(config-if)# do show ip interface g0/1     ! infos couche 3 de l'interface (adresse, masque, broadcast)
Router(config-if)# exit                          ! retour en configuration globale
Router(config)# ip route 192.168.5.128 255.255.255.192 192.168.5.225   ! route statique : réseau, masque, next hop (ou interface de sortie)
Router(config)# do show ip route                 ! table de routage (routes connected, local, static)
```

Sur un PC Packet Tracer : onglet Config, Gateway, puis FastEthernet0, IP address ; la touche Tab remplit un masque **classful**, à corriger pour le sous-réseau.

### 8. Le lab (vidéo n°28)

**Objectif** : découper **192.168.5.0/24** en VLSM pour 4 LAN et la liaison point à point R1–R2 ; PC = **première** adresse utilisable, routeur = **dernière** ; routes statiques pour la connectivité entre LAN. Ordre : LAN2, LAN1, LAN3, LAN4, point à point.

| Sous-réseau | Besoin | Préfixe / masque | Réseau | Broadcast | Routeur (dernière utilisable) | PC (première utilisable) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| LAN2 | 64 | /25, 255.255.255.128 (/26 = 62, insuffisant) | 192.168.5.0 | 192.168.5.127 | R1 G0/1 = 192.168.5.126 | PC2 = 192.168.5.1 |
| LAN1 | 45 | /26, 255.255.255.192 | 192.168.5.128 | 192.168.5.191 | R1 G0/0 = 192.168.5.190 | PC1 = 192.168.5.129 |
| LAN3 | 14 | /28, 255.255.255.240 | 192.168.5.192 | 192.168.5.207 | R2 G0/0 = 192.168.5.206 | PC3 = 192.168.5.193 |
| LAN4 | 9 | /28 (/29 = 6, insuffisant) | 192.168.5.208 | 192.168.5.223 | R2 G0/1 = 192.168.5.222 | PC4 = 192.168.5.209 |
| R1–R2 | 2 | /30, 255.255.255.252 (« option sûre » à l'examen) | 192.168.5.224 | 192.168.5.227 | R1 G0/0/0 = .225, R2 G0/0/0 = .226 | – |

**Étapes** :

1. Sur chaque routeur : `enable`, `configure terminal`, `interface ...`, `ip address ...`, `no shutdown`, puis `do show ip interface ...` pour vérifier. Le champ « broadcast address 255.255.255.255 » affiché fonctionne comme le broadcast du sous-réseau et vaut pour tout réseau ; un broadcast vers 255.255.255.255 **reste dans le sous-réseau local**, un routeur ne le route pas. Le broadcast de sous-réseau (192.168.5.127) peut, lui, être utilisé depuis d'autres sous-réseaux (expliqué plus tard dans le cours).
2. Sur chaque PC : Gateway = adresse du routeur, puis IP et masque (corriger le masque proposé par Tab).
3. Routes statiques (chaque routeur a 3 réseaux connectés, il lui manque 2 LAN) :
   - R2 : `ip route 192.168.5.128 255.255.255.192 192.168.5.225` (LAN1) et `ip route 192.168.5.0 255.255.255.128 192.168.5.225` (LAN2). Le `?` montre qu'on peut indiquer l'interface de sortie ou le next hop.
   - R1 : `ip route 192.168.5.192 255.255.255.240 192.168.5.226` (LAN3) et `ip route 192.168.5.208 255.255.255.240 192.168.5.226` (LAN4).
4. **Vérifications** : `do show ip route` sur chaque routeur (routes connected, local, puis les 2 statiques) ; depuis PC1, `ping 192.168.5.209` (PC4) : les premiers pings peuvent échouer tant qu'ARP n'est pas terminé. Idéalement, pinger tous les PC.

---

## 🇬🇧 English version

### 1. Day 14 quiz answers

See `jour-14-subnetting-part-2.md`, section 7: /23; 172.21.96.0/20; 192.168.91.127; 172.16.64.0 and 172.16.127.255; 64 subnets.

### 2. Class A: same process, bigger numbers

Class A has **24 host bits** ("size of rest bit field"): lots of room to make subnets. The process is **exactly the same** as for class B and C.

**Exercise 1**: 10.0.0.0/8 (mask 255.0.0.0), create **2,000 subnets** for various enterprises. Prefix length? Hosts per subnet?

- 2 to the power of what is at least 2,000? Doubling: 2, 4, 8, 16, 32, 64, 128, 256, 512, 1,024, **2,048** → **11 borrowed bits** (2^11).
- 8 + 11 = **/19**.
- 32 − 19 = **13 host bits** remain → 2^13 − 2 = **8,190 hosts** (usable addresses) per subnet.

**Exercise 2**: PC1 has IP address **10.217.182.223/11**. Identify for PC1's subnet:

| Item | Method | Answer |
| :--- | :--- | :--- |
| Network address | /11 = 3 borrowed bits on the /8; host bits to 0 | **10.192.0.0** |
| First usable address | network address + 1 | **10.192.0.1** |
| Broadcast address | host bits to 1 | **10.223.255.255** |
| Last usable address | broadcast − 1 | **10.223.255.254** |
| Number of usable addresses | 21 host bits → 2^21 − 2 | **2,097,150** |

Converting between binary and dotted decimal is "absolutely essential" for subnetting.

### 3. FLSM versus VLSM

- **FLSM** (Fixed-Length Subnet Masks): all subnets use the same prefix length (what we did so far, e.g. a class C into 4 × /26).
- **VLSM** (Variable-Length Subnet Masks): creating subnets **of different sizes** to use address space more efficiently. More complicated than FLSM, but easy if you follow the steps.

**The VLSM steps**: 1) assign the **largest** subnet at the **start** of the address space; 2) assign the second-largest after it; 3) repeat, from largest to smallest, until all subnets are assigned.

### 4. The full example: 192.168.1.0/24 for Tokyo and Toronto

Requirements: Tokyo LAN A **110 hosts**, Tokyo LAN B **8 hosts**, Toronto LAN A **29 hosts**, Toronto LAN B **45 hosts**, plus the **point-to-point connection** between the two routers. 5 subnets in total.

- With FLSM: 5 subnets → 3 borrowed bits → 5 host bits → only **30 hosts**, not enough for Tokyo LAN A or Toronto LAN B. Hence VLSM.
- Assignment order: Tokyo LAN A, Toronto LAN B, Toronto LAN A, Tokyo LAN B, point-to-point.

| Order | Subnet | Needs | Prefix | Network address | Broadcast | First usable | Last usable | Usable |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Tokyo LAN A | 110 | /25 (7 host bits, 128 addresses) | 192.168.1.0 | 192.168.1.127 | 192.168.1.1 | 192.168.1.126 | 126 |
| 2 | Toronto LAN B | 45 | /26 (/27 would only give 30) | 192.168.1.128 | 192.168.1.191 | 192.168.1.129 | 192.168.1.190 | 62 |
| 3 | Toronto LAN A | 29 | /27 (5 host bits) | 192.168.1.192 | 192.168.1.223 | 192.168.1.193 | 192.168.1.222 | 30 |
| 4 | Tokyo LAN B | 8 | /28 (**not /29**: 8 addresses but 6 usable) | 192.168.1.224 | 192.168.1.239 | 192.168.1.225 | 192.168.1.238 | 14 |
| 5 | Point-to-point | 2 | /30 | 192.168.1.240 | 192.168.1.243 | 192.168.1.241 | 192.168.1.242 | 2 |

- Each network address = previous subnet's broadcast + 1.
- The /25 uses half of the address space, the /26 another quarter (three quarters used after two subnets): "no problem", the smaller subnets fit in the rest, and some space is even left at the end.
- **For the point-to-point link on the CCNA exam**: /31 is possible, but Jeremy recommends **not answering /31** to a question "which prefix length for 2 hosts?"; the expected answer is **/30**.

### 5. Homework (instead of a quiz)

Three practice websites named by Jeremy: subnettingquestions.com, subnetting.org and subnettingpractice.com (his favorite, with more challenging questions that go beyond those in the videos). **Do at least ONE practice question from EACH site every day for at least one week.**

### 6. Exam traps

- The /29 versus /28 trap for 8 hosts: 2^3 = 8 addresses, but **6** usable → /28 is needed.
- The router needs an address in every subnet.
- Answer /30 (not /31) for a 2-host link on the exam.
- In real networking leave room for growth; **on a test do EXACTLY what the instructions say** (the lab uses a /28 for exactly 14 hosts).

### 7. IOS commands

```
Router> enable                                   ! privileged exec mode
Router# configure terminal                       ! global configuration mode
Router(config)# interface g0/1                   ! configure an interface
Router(config-if)# ip address 192.168.5.126 255.255.255.128   ! address + dotted decimal mask (/25)
Router(config-if)# no shutdown                   ! enable the interface
Router(config-if)# do show ip interface g0/1     ! Layer 3 information about the interface (address, mask, broadcast)
Router(config-if)# exit                          ! back to global config
Router(config)# ip route 192.168.5.128 255.255.255.192 192.168.5.225   ! static route: network, mask, next hop (or exit interface)
Router(config)# do show ip route                 ! routing table (connected, local, static routes)
```

On a Packet Tracer PC: Config tab, Gateway, then FastEthernet0, IP address; the Tab key fills in a **classful** mask, which must be corrected for the subnet.

### 8. The lab (video 28)

**Objective**: subnet **192.168.5.0/24** with VLSM for 4 LANs and the R1–R2 point-to-point link; PC = **first** usable address, router = **last**; static routes so that hosts in each LAN can reach the others. Order: LAN2, LAN1, LAN3, LAN4, point-to-point.

| Subnet | Needs | Prefix / mask | Network | Broadcast | Router (last usable) | PC (first usable) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| LAN2 | 64 | /25, 255.255.255.128 (/26 = 62, not enough) | 192.168.5.0 | 192.168.5.127 | R1 G0/1 = 192.168.5.126 | PC2 = 192.168.5.1 |
| LAN1 | 45 | /26, 255.255.255.192 | 192.168.5.128 | 192.168.5.191 | R1 G0/0 = 192.168.5.190 | PC1 = 192.168.5.129 |
| LAN3 | 14 | /28, 255.255.255.240 | 192.168.5.192 | 192.168.5.207 | R2 G0/0 = 192.168.5.206 | PC3 = 192.168.5.193 |
| LAN4 | 9 | /28 (/29 = 6, not enough) | 192.168.5.208 | 192.168.5.223 | R2 G0/1 = 192.168.5.222 | PC4 = 192.168.5.209 |
| R1–R2 | 2 | /30, 255.255.255.252 ("the safe option" on a Cisco test) | 192.168.5.224 | 192.168.5.227 | R1 G0/0/0 = .225, R2 G0/0/0 = .226 | – |

**Steps**:

1. On each router: `enable`, `configure terminal`, `interface ...`, `ip address ...`, `no shutdown`, then `do show ip interface ...` to confirm. The displayed "broadcast address 255.255.255.255" functions the same as the subnet broadcast address and can be used for any network; a broadcast to 255.255.255.255 **stays in the local subnet**, a router will not route it. The subnet broadcast address (192.168.5.127) can be used by hosts in other subnets (explained later in the course).
2. On each PC: Gateway = router's address, then IP and mask (fix the mask proposed by Tab).
3. Static routes (each router has 3 connected networks, it is missing 2 LANs):
   - R2: `ip route 192.168.5.128 255.255.255.192 192.168.5.225` (LAN1) and `ip route 192.168.5.0 255.255.255.128 192.168.5.225` (LAN2). The `?` shows you can specify either the exit interface or the next hop.
   - R1: `ip route 192.168.5.192 255.255.255.240 192.168.5.226` (LAN3) and `ip route 192.168.5.208 255.255.255.240 192.168.5.226` (LAN4).
4. **Verification**: `do show ip route` on each router (connected, local, then the 2 static routes); from PC1, `ping 192.168.5.209` (PC4): the first pings may fail until ARP completes. Ideally, ping all other PCs.
