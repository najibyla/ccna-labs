# CCNA Day 31 : IPv6 Part 1 / IPv6, partie 1

> Source : Jeremy's IT Lab, vidéo n°63 « IPv6 Part 1 | Day 31 » (cours, 39 min) et vidéo n°64 « Configuring IPv6 (Part 1) | Day 31 Lab » (lab, 18 min) de la playlist. Fiche rédigée à partir des transcriptions le 6 octobre 2026. Les exercices d'abréviation, d'expansion et de calcul de préfixe de la vidéo sont affichés à l'écran et absents de la transcription : seuls les exemples énoncés oralement figurent ici.

## 🇫🇷 Version française

### 1. Cadre

- Sujets d'examen **1.8** (configurer et vérifier adressage et préfixes IPv6) et **1.9** (comparer les types d'adresses IPv6), plus les routes statiques IPv6 comme en IPv4. Jeremy répartit IPv6 sur trois vidéos (Days 31, 32, 33).
- **Pourquoi pas IPv5 ?** L'*Internet Stream Protocol* (fin des années 1970, jamais public) utilisait la valeur 5 dans le champ **Version** de l'en-tête IP ; le successeur d'IPv4 a donc été nommé IPv6 (valeur 6).

### 2. Rappel hexadécimal

- Trois systèmes à connaître : **binaire** (base 2, préfixe `0b`, chiffres 0-1), **décimal** (base 10, préfixe `0d`), **hexadécimal** (base 16, préfixe `0x`, chiffres 0-9 puis **A=10, B=11, C=12, D=13, E=14, F=15**). Sans préfixe, « 10 » est ambigu (dix, deux ou seize).
- **Chaque chiffre hexadécimal contient 4 bits** (1111 = F). C'est la clé des conversions.
- **Binaire → hexa** : découper en groupes de 4 bits, convertir chaque groupe en décimal, puis en hexa. `1101 1011` → 13, 11 → **DB**. `0010 1111` → **2F**. `1000 0001` → **81**.
- **Hexa → binaire** : chaque chiffre en décimal puis en 4 bits. `EC` → 14, 12 → **1110 1100**. `2B` → **0010 1011**. `D7` → **1101 0111**.
- Vérification possible avec la calculatrice Windows en mode **Programmeur** (hex, déc, octal = base 8, bin). Savoir le faire à la main reste indispensable.

### 3. Pourquoi IPv6 ?

- IPv4 = 32 bits = **4 294 967 296** adresses. Insuffisant pour le monde moderne.
- Mesures de conservation (court terme) : **VLSM**, **adresses privées** et **NAT** (*Network Address Translation*, vus plus tard). Solution de long terme : **IPv6**.
- Attribution : **IANA** distribue l'espace aux **RIR** (*Regional Internet Registries*) qui l'attribuent aux entreprises et FAI : **AFRINIC** (Afrique), **APNIC** (Asie-Pacifique), **ARIN** (États-Unis, Canada, îles des Caraïbes et de l'Atlantique Nord), **LACNIC** (Amérique latine et Caraïbes), **RIPE NCC** (Europe, Moyen-Orient, une partie de l'Asie centrale).
- Épuisement : ARIN a déclaré son pool IPv4 épuisé en **septembre 2015** ; LACNIC a annoncé sa dernière allocation en **août 2020**.

### 4. L'adresse IPv6

- **128 bits**, 4 fois IPv4, mais **chaque bit supplémentaire double** le nombre d'adresses (33 bits ≈ 8 milliards, 34 ≈ 16 milliards) : environ **340 undécillions** d'adresses (3,4 × 10^38, pas à mémoriser).
- Écriture : **32 caractères hexadécimaux en 8 groupes de 4** (*quartets*) séparés par des deux-points. 128 / 4 = 32.
- Longueur de préfixe en **notation slash**, y compris dans l'IOS (plus de masque en décimal pointé). **/64** : première moitié = partie réseau, seconde moitié = partie hôte.

### 5. Abréger une adresse IPv6 (deux règles)

1. **Supprimer les zéros de tête** (*leading 0s*) de chaque quartet : les zéros au **début** d'un quartet. Les zéros à l'intérieur ou à la fin ne se suppriment pas (sinon, en les rajoutant, on obtient une autre adresse).
2. **Remplacer des quartets consécutifs entièrement à zéro par `::`**, **une seule fois** par adresse : on sait qu'il y a 8 quartets, donc on déduit combien le `::` en représente. Avec deux `::` (ex. 5 quartets nuls répartis 2+3 ou 3+2), impossible de savoir. S'il y a deux séries de quartets nuls, on abrège la plus longue avec `::` et on retire seulement les zéros de tête de l'autre.
- Les deux règles se combinent.

**Développer** une adresse abrégée : remettre les zéros de tête pour que chaque quartet ait 4 caractères, puis remplacer `::` par autant de quartets `0000` qu'il faut pour en avoir 8 (5 quartets écrits → `::` = 3 quartets).

### 6. Trouver le préfixe (adresse réseau)

- Comme en IPv4 : **mettre tous les bits d'hôte à 0**.
- Une entreprise reçoit typiquement un **bloc /48** de son FAI (le **global routing prefix**, pour une adresse *global unicast*) ; les sous-réseaux IPv6 utilisent typiquement **/64**. Les **16 bits** entre les deux (4 chiffres hexa) sont le **subnet identifier** : 16 bits pour créer des sous-réseaux, 64 bits d'hôte. Préfixe global + identifiant de sous-réseau = partie réseau.
- **/64** : seconde moitié à zéro (ex. `2001:db8:...::/64`).
- **Préfixe multiple de 4** (ex. /56) : chaque quartet = 16 bits, chaque caractère = 4 bits ; on compte 16, 32, 48, 52, 56 → les **14 premiers caractères** sont le réseau, le reste passe à 0. Attention : les zéros de la partie hôte qui ne sont pas des zéros de tête ne se suppriment pas.
- **Préfixe non multiple de 4** (ex. **/93**) : la frontière tombe au milieu d'un chiffre. 16, 32, 48, 64, 80, 84, 88, 92 bits ; le caractère suivant, **B** = 1011, n'a que son **premier bit** dans la partie réseau → 1000 = **8**. Le B devient un 8 dans le préfixe. Sans le binaire, impossible de le voir.

### 7. Pièges d'examen

- Une adresse valide : seulement **0-9 et A-F** (pas de G), **8 quartets** exactement (pas 9), `::` **une seule fois**.
- On ne supprime que les zéros **de tête**.
- `ipv6 unicast-routing` se tape en **mode de configuration globale** ; sans lui le routeur **ne transfère pas** les paquets IPv6 (il peut encore répondre aux pings sur ses interfaces).
- `2001:db8::/32` est réservé à la **documentation et aux exemples**, jamais en production.
- Les commandes IPv6 reprennent celles d'IPv4 avec `ipv6` à la place de `ip` (ex. `ipv6 route <réseau/préfixe> <next-hop>`, question bonus Boson).

### 8. Commandes IOS

```
R1(config)# ipv6 unicast-routing              ! active le routage IPv6 (indispensable, pas activé par défaut)
R1(config)# interface g0/0
R1(config-if)# ipv6 address 2001:db8:0:0::1/64  ! adresse + longueur de préfixe ; forme complète, abrégée ou partielle acceptée
R1(config-if)# no shutdown
R1# show ipv6 interface brief                  ! adresses abrégées ; une link-local automatique par interface
R1(config)# ipv6 route 2001:db8:2::/64 2001:db8:1::2   ! route statique IPv6 (bonus Boson)
R4# ping ipv6 2001:1:3:1::1                    ! ping IPv6 (bonus NetSim)
```

Chaque interface affiche **deux** adresses : celle configurée et une **link-local** générée automatiquement dès qu'IPv6 est activé sur l'interface (détaillée au Day 32).

### 9. Le lab (vidéo n°64)

Objectif : ajouter IPv6 à un réseau IPv4 déjà fonctionnel (R1 et trois PC) sans retirer IPv4 : solution **dual-stack**, une méthode de transition.

1. Étape 1 (routage IPv6) **volontairement sautée** pour montrer l'effet.
2. R1 : `interface g0/0` → `ipv6 address 2001:db8:0:1::1/64` ; g0/1 → `2001:db8:0:2::1/64` ; g0/2 → `2001:db8:0:3::1/64`. Pas de `no shutdown`, les interfaces sont déjà actives.
3. `do show ipv6 interface brief` : adresses configurées + link-local automatiques.
4. PC (onglet Config) : passerelle IPv6 `2001:db8:0:1::1`, puis sur FastEthernet0 l'adresse `2001:db8:0:1::2/64`. Idem PC2 (`:2::1` / `:2::2`), PC3 (`:3::1` / `:3::2`).
5. Pings depuis PC1 : gateway `2001:db8:0:1::1` OK, autre interface de R1 `2001:db8:0:2::1` OK, **PC2 `2001:db8:0:2::2` échoue**. Même chose depuis PC2. Cause : `ipv6 unicast-routing` absent.
6. R1 : `exit`, `ipv6 unicast-routing`. Le ping PC1 → PC2 fonctionne. `ping 192.168.2.2` : IPv4 fonctionne aussi.

Bonus (courseware Boson) : les adresses IPv4 des routeurs sont publiques ; max ≈ 4 milliards en IPv4, 3,4 × 10^38 en IPv6 ; coexistence par dual-stack ; `ipv6 unicast-routing` sur Router3 et Router4, puis `ipv6 address 2001:1:3:1::1/64` (S0/1 de Router3, après avoir annulé avec `no` une saisie sur la mauvaise interface) et `2001:1:3:1::2/64` (S0/0 de Router4) ; `ping ipv6 2001:1:3:1::1` réussit.

### 10. Le quiz (3 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Lesquelles sont des adresses IPv6 valides (trois réponses) ? | **A, B, E** (options à l'écran) | C contient un **G** (pas hexadécimal) ; D a **neuf quartets** ; F utilise **deux fois `::`**. |
| Quelle abréviation correcte de l'adresse affichée ? | **D** | Les autres suppriment des zéros qui ne sont pas des zéros **de tête**. |
| Commande pour activer le routage IPv6 ? | **`ipv6 unicast-routing` en configuration globale** | Pas en mode interface ; `ipv6 routing` n'existe pas. |

Bonus Boson : route de RouterA vers `2001:db8:2::/64` via le next-hop `2001:db8:1::2` (RouterB) → `ipv6 route 2001:db8:2::/64 2001:db8:1::2`. Un next-hop `2001:db8:2::2` serait RouterC lui-même, que RouterA ne sait pas joindre.

---

## 🇬🇧 English version

### 1. Scope

- Exam topics **1.8** (configure and verify IPv6 addressing and prefixes) and **1.9** (compare IPv6 address types), plus IPv6 static routes as in IPv4. Jeremy splits IPv6 over three videos (Days 31, 32, 33).
- **Why no IPv5?** The Internet Stream Protocol (late 1970s, never public) used value 5 in the **Version** field of the IP header; IPv4's successor was therefore named IPv6 (value 6).

### 2. Hexadecimal review

- Three numbering systems to know: **binary** (base 2, prefix `0b`, digits 0-1), **decimal** (base 10, prefix `0d`), **hexadecimal** (base 16, prefix `0x`, digits 0-9 then **A=10, B=11, C=12, D=13, E=14, F=15**). Without a prefix, "10" is ambiguous (ten, two or sixteen).
- **Each hexadecimal digit contains 4 bits** (1111 = F). This is the key to conversions.
- **Binary → hex**: split into 4-bit groups, convert each group to decimal, then to hex. `1101 1011` → 13, 11 → **DB**. `0010 1111` → **2F**. `1000 0001` → **81**.
- **Hex → binary**: each digit to decimal then to 4 bits. `EC` → 14, 12 → **1110 1100**. `2B` → **0010 1011**. `D7` → **1101 0111**.
- Check with the Windows calculator in **Programmer** mode (hex, dec, octal = base 8, bin). Doing it by hand is still essential.

### 3. Why IPv6?

- IPv4 = 32 bits = **4,294,967,296** addresses. Not enough for the modern world.
- Preservation techniques (short-term): **VLSM**, **private addresses** and **NAT** (Network Address Translation, covered later). Long-term solution: **IPv6**.
- Assignment: **IANA** distributes address space to the **RIRs** (Regional Internet Registries), which assign it to companies and ISPs: **AFRINIC** (Africa), **APNIC** (Asia-Pacific), **ARIN** (US, Canada, Caribbean and North Atlantic islands), **LACNIC** (Latin America and Caribbean), **RIPE NCC** (Europe, Middle East, parts of Central Asia).
- Exhaustion: ARIN declared its IPv4 pool exhausted in **September 2015**; LACNIC announced its final allocation in **August 2020**.

### 4. The IPv6 address

- **128 bits**, 4 times IPv4, but **every additional bit doubles** the number of addresses (33 bits ≈ 8 billion, 34 ≈ 16 billion): about **340 undecillion** addresses (3.4 × 10^38, no need to memorize).
- Written as **32 hexadecimal characters in 8 groups of 4** (quartets) separated by colons. 128 / 4 = 32.
- Prefix length in **slash notation**, even in the IOS CLI (no more dotted-decimal masks). **/64**: first half = network portion, second half = host portion.

### 5. Shortening an IPv6 address (two rules)

1. **Remove leading 0s** from each quartet: the 0s at the **beginning** of a quartet. 0s inside or at the end cannot be removed (adding them back would give a different address).
2. **Replace consecutive all-0 quartets with `::`**, **only once** per address: we know there are 8 quartets, so we can deduce how many the `::` stands for. With two `::` (e.g. 5 zero quartets split 2+3 or 3+2) there is no way to know. With two runs of zero quartets, abbreviate the longer run with `::` and only remove leading 0s from the other.
- Both rules can be combined.

**Expanding** a shortened address: put back leading 0s so every quartet has 4 characters, then replace `::` with as many `0000` quartets as needed to reach 8 (5 quartets written → `::` = 3 quartets).

### 6. Finding the prefix (network address)

- As in IPv4: **set all host bits to 0**.
- An enterprise typically receives a **/48 block** from its ISP (the **global routing prefix**, for a global unicast address); IPv6 subnets typically use **/64**. The **16 bits** in between (4 hex digits) are the **subnet identifier**: 16 bits to make subnets, 64 host bits. Global routing prefix + subnet identifier = network portion.
- **/64**: second half set to 0 (e.g. `2001:db8:...::/64`).
- **Prefix length multiple of 4** (e.g. /56): each quartet = 16 bits, each character = 4 bits; count 16, 32, 48, 52, 56 → the **first 14 characters** are the network, everything after becomes 0. Careful: host-portion 0s that are not leading 0s cannot be removed.
- **Prefix length not a multiple of 4** (e.g. **/93**): the boundary falls inside a digit. 16, 32, 48, 64, 80, 84, 88, 92 bits; the next character, **B** = 1011, has only its **first bit** in the network portion → 1000 = **8**. The B becomes an 8 in the prefix. Without binary you cannot see this.

### 7. Exam traps

- A valid address: only **0-9 and A-F** (no G), exactly **8 quartets** (not 9), `::` **only once**.
- Only **leading** 0s can be removed.
- `ipv6 unicast-routing` is entered in **global configuration mode**; without it the router **does not forward** IPv6 packets (it can still answer pings on its interfaces).
- `2001:db8::/32` is reserved for **documentation and examples**, never for real networks.
- IPv6 commands mirror IPv4 ones with `ipv6` instead of `ip` (e.g. `ipv6 route <network/prefix> <next-hop>`, Boson bonus question).

### 8. IOS commands

```
R1(config)# ipv6 unicast-routing              ! enables IPv6 routing (required, off by default)
R1(config)# interface g0/0
R1(config-if)# ipv6 address 2001:db8:0:0::1/64  ! address + prefix length; full, shortened or partially shortened form accepted
R1(config-if)# no shutdown
R1# show ipv6 interface brief                  ! shortened addresses; one automatic link-local per interface
R1(config)# ipv6 route 2001:db8:2::/64 2001:db8:1::2   ! IPv6 static route (Boson bonus)
R4# ping ipv6 2001:1:3:1::1                    ! IPv6 ping (NetSim bonus)
```

Each interface shows **two** addresses: the configured one and a **link-local** address generated automatically as soon as IPv6 is enabled on the interface (covered on Day 32).

### 9. The lab (video 64)

Goal: add IPv6 to an already working IPv4 network (R1 and three PCs) without removing IPv4: a **dual-stack** solution, one transition method.

1. Step 1 (IPv6 routing) **deliberately skipped** to show the effect.
2. R1: `interface g0/0` → `ipv6 address 2001:db8:0:1::1/64`; g0/1 → `2001:db8:0:2::1/64`; g0/2 → `2001:db8:0:3::1/64`. No `no shutdown`, the interfaces are already up.
3. `do show ipv6 interface brief`: configured addresses + automatic link-locals.
4. PCs (Config tab): IPv6 gateway `2001:db8:0:1::1`, then on FastEthernet0 the address `2001:db8:0:1::2/64`. Same for PC2 (`:2::1` / `:2::2`), PC3 (`:3::1` / `:3::2`).
5. Pings from PC1: gateway `2001:db8:0:1::1` OK, R1's other interface `2001:db8:0:2::1` OK, **PC2 `2001:db8:0:2::2` fails**. Same from PC2. Cause: `ipv6 unicast-routing` missing.
6. R1: `exit`, `ipv6 unicast-routing`. Ping PC1 → PC2 works. `ping 192.168.2.2`: IPv4 works too.

Bonus (Boson courseware): the routers' IPv4 addresses are public; max ≈ 4 billion in IPv4, 3.4 × 10^38 in IPv6; coexistence via dual-stack; `ipv6 unicast-routing` on Router3 and Router4, then `ipv6 address 2001:1:3:1::1/64` (Router3 S0/1, after cancelling with `no` an entry on the wrong interface) and `2001:1:3:1::2/64` (Router4 S0/0); `ping ipv6 2001:1:3:1::1` succeeds.

### 10. The quiz (3 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which are valid IPv6 addresses (select three)? | **A, B, E** (options on screen) | C contains a **G** (not hexadecimal); D has **nine quartets**; F uses `::` **twice**. |
| Which is a correctly abbreviated version of the address shown? | **D** | The others remove 0s that are not **leading** 0s. |
| Command to enable IPv6 routing? | **`ipv6 unicast-routing` in global config** | Not in interface mode; `ipv6 routing` does not exist. |

Boson bonus: route from RouterA to `2001:db8:2::/64` via next hop `2001:db8:1::2` (RouterB) → `ipv6 route 2001:db8:2::/64 2001:db8:1::2`. A next hop of `2001:db8:2::2` would be RouterC itself, which RouterA cannot reach yet.
