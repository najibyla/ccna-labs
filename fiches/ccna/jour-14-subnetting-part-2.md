# CCNA Day 14 : Subnetting (Part 2) / Sous-réseaux, partie 2

> Source : Jeremy's IT Lab, « Free CCNA | Subnetting (Part 2) | Day 14 » (25 min), vidéo n°26 de la playlist. Pas de lab ni de flashcards pour ce jour (le lab de subnetting arrive au Day 15). Les réponses du quiz sont données au début du Day 15 (vidéo n°27). Fiche rédigée à partir de la transcription le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Corrigé du quiz du Day 13 : 192.168.1.0/24 en 4 sous-réseaux /26

Convention de couleurs de Jeremy : bleu = partie réseau d'origine, rouge = partie hôte, violet = bits **empruntés** (*borrowed*) à la partie hôte pour agrandir la partie réseau.

Méthode : adresse de broadcast = tous les bits hôte à **1** (adresse la plus haute du sous-réseau) ; adresse réseau du sous-réseau suivant = broadcast + 1 ; adresse réseau = tous les bits hôte à **0**.

| Sous-réseau | Adresse réseau | Broadcast | Plage |
| :--- | :--- | :--- | :--- |
| 1 | 192.168.1.0/26 | 192.168.1.63 | .0 à .63 |
| 2 | 192.168.1.64/26 | 192.168.1.127 | .64 à .127 |
| 3 | 192.168.1.128/26 | 192.168.1.191 | .128 à .191 |
| 4 | 192.168.1.192/26 | 192.168.1.255 | .192 à .255 |

Dans le sous-réseau 4, les deux bits empruntés valent 1 1 : c'est le dernier sous-réseau, il n'y a plus de place.

**L'astuce** : 0 + 64 = 64, 64 + 64 = 128, 128 + 64 = 192. Valeurs des bits du dernier octet, de droite à gauche : 1, 2, 4, 8, 16, 32, 64, 128. **Le dernier bit de la partie réseau vaut 64 : il suffit d'ajouter 64 pour trouver le sous-réseau suivant.**

### 2. Combien de sous-réseaux ? La formule 2^X

Exercice : 192.168.255.0/24 à diviser en **5 sous-réseaux de taille égale**, aussi grands que possible.

- **Nombre de sous-réseaux = 2^X, X = nombre de bits empruntés.** Contrairement aux hôtes (2^N − 2), **on ne retire pas 2**.
- Les bits bleus d'origine ne changent pas (c'est le réseau reçu) ; chaque bit emprunté peut valoir 0 ou 1.
- 0 bit emprunté : un seul réseau. 1 bit (/25) : 2 sous-réseaux, 192.168.255.0/25 et 192.168.255.128/25. 2 bits (/26) : 4, insuffisant. **3 bits (/27) : 8 sous-réseaux**, c'est la réponse.
- Dernier bit de la partie réseau = **32**. Sous-réseau 1 : 192.168.255.0/27 ; 2 : .32/27 ; 3 : .64/27 ; 4 : .96/27 ; 5 : .128/27. Les trois sous-réseaux restants : .160, .192 et .224/27.

### 3. À quel sous-réseau appartient un hôte ?

Méthode : écrire l'adresse en binaire, repérer où finit la partie réseau (bits empruntés compris), mettre tous les bits hôte à **0**, reconvertir en décimal.

- 192.168.5.57/27 : 3 bits empruntés ; dernier octet 57 = 0011 1001 → hôte à 0 → 0010 0000 = 32. **Sous-réseau 192.168.5.32/27.**
- 192.168.29.219/29 : 5 bits empruntés → **sous-réseau 192.168.29.216/29.**

### 4. Tableau de référence pour la classe C (à mémoriser selon Jeremy)

| Préfixe | Sous-réseaux | Hôtes utilisables |
| :--- | :--- | :--- |
| /25 | 2 | 126 |
| /26 | 4 | 62 |
| /27 | 8 | 30 |
| /28 | 16 | 14 |
| /29 | 32 | 6 |
| /30 | 64 | 2 |
| /31 | 128 | 0 (mais utilisable en point à point, sans adresse réseau ni broadcast) |
| /32 | 256 | 0 (identifie un hôte précis dans une route, etc.) |

Chaque bit emprunté **double** le nombre de sous-réseaux ; chaque bit hôte **double** le nombre d'adresses, moins 2.

### 5. Classe B : exactement la même méthode

**Exercice 1** : 172.16.0.0/16, créer **80 sous-réseaux**. Quel préfixe ?

| Bits empruntés | Sous-réseaux | Préfixe | Masque décimal pointé |
| :--- | :--- | :--- | :--- |
| 1 | 2 | /17 | 255.255.128.0 |
| 2 | 4 | /18 | 255.255.192.0 |
| 3 | 8 | /19 | 255.255.224.0 |
| 4 | 16 | /20 | 255.255.240.0 |
| 5 | 32 | /21 | 255.255.248.0 |
| 6 | 64 | /22 | 255.255.252.0 |
| 7 | **128** | **/23** | **255.255.254.0** |

Réponse : **/23** (/22 ne donne que 64). Premiers sous-réseaux : 172.16.0.0/23, 172.16.2.0/23, 172.16.4.0/23, 172.16.6.0, 172.16.8.0, etc. **Rappel : dans la CLI Cisco on ne peut pas taper /17, il faut le masque décimal pointé 255.255.128.0.**

**Exercice 2** : 172.22.0.0/16, **500 sous-réseaux** → emprunter 9 bits (2^9 = 512) → **/25**. On peut emprunter des bits jusque dans le dernier octet, même sur une classe B.

**Exercice 3** : 172.18.0.0/16, **250 sous-réseaux et 250 hôtes par sous-réseau** → **/24** : 8 bits empruntés = 256 sous-réseaux, 8 bits hôte = 254 hôtes.

**Identifier le sous-réseau** : 172.25.217.192/21 → binaire, bits hôte à 0 → **172.25.216.0/21**. Même procédé qu'en classe C, juste plus de bits hôte.

Le tableau équivalent pour la classe B n'est **pas** à mémoriser (« ce serait un gaspillage d'effort ») : il suffit de connaître le motif 2, 4, 8, 16, 32… pour les sous-réseaux et le doublement moins 2 pour les hôtes.

### 6. Pièges d'examen

- Sous-réseaux : **2^X sans −2**. Hôtes : **2^N − 2**.
- /29 donne 8 adresses mais seulement **6** utilisables.
- Pour le broadcast, bits hôte à **1** ; pour l'adresse réseau, bits hôte à **0**.
- Savoir écrire chaque préfixe en décimal pointé (255.255.254.0 pour /23, etc.), c'est ce que la CLI exige.

### 7. Le quiz du Day 14 (5 questions, réponses données au Day 15)

| Question | Réponse | Méthode |
| :--- | :--- | :--- |
| 172.30.0.0/16 : 100 sous-réseaux avec au moins 500 hôtes chacun. Quel préfixe ? | **/23** (255.255.254.0) | Compter sur les doigts : 2, 4, 8, 16, 32, 64, 128 → 7 bits empruntés. Il reste 9 bits hôte → 2^9 − 2 = 510 ≥ 500. |
| À quel sous-réseau appartient 172.21.111.201/20 ? | **172.21.96.0/20** | Binaire, bits hôte à 0, retour en décimal. |
| Adresse de broadcast du réseau auquel appartient 192.168.91.78/26 ? | **192.168.91.127** | Même méthode mais bits hôte à 1. |
| 172.16.0.0/16 divisé en 4 sous-réseaux égaux : adresses réseau et broadcast du 2e sous-réseau ? | **172.16.64.0** et **172.16.127.255** | 4 sous-réseaux = 2 bits empruntés = /18. Dernier bit emprunté à 1 → .64.0 ; bits hôte à 1 → .127.255. |
| 172.30.0.0/16 en sous-réseaux de 1 000 hôtes : combien de sous-réseaux ? | **64** | 1 000 hôtes → 10 bits hôte (2^10 − 2 = 1 022). 16 − 10 = 6 bits empruntés → 2^6 = 64. |

---

## 🇬🇧 English version

### 1. Day 13 quiz solution: 192.168.1.0/24 into 4 /26 subnets

Jeremy's colors: blue = original network portion, red = host portion, purple = bits **borrowed** from the host portion to extend the network portion.

Method: broadcast address = all host bits set to **1** (highest address of the subnet); network address of the next subnet = broadcast + 1; network address = all host bits set to **0**.

| Subnet | Network address | Broadcast | Range |
| :--- | :--- | :--- | :--- |
| 1 | 192.168.1.0/26 | 192.168.1.63 | .0 to .63 |
| 2 | 192.168.1.64/26 | 192.168.1.127 | .64 to .127 |
| 3 | 192.168.1.128/26 | 192.168.1.191 | .128 to .191 |
| 4 | 192.168.1.192/26 | 192.168.1.255 | .192 to .255 |

In subnet 4 the two borrowed bits are 1 1: it is the last subnet, there is no room for more.

**The trick**: 0 + 64 = 64, 64 + 64 = 128, 128 + 64 = 192. Bit values of the last octet, from the right: 1, 2, 4, 8, 16, 32, 64, 128. **The last bit of the network portion is 64: just add 64 to find the next subnet.**

### 2. How many subnets? The 2^X formula

Exercise: divide 192.168.255.0/24 into **5 equal-sized subnets**, as large as possible.

- **Number of subnets = 2^X, X = number of borrowed bits.** Unlike hosts (2^N − 2), **you do not subtract 2**.
- The original blue bits cannot change (that is the network we received); each borrowed bit can be 0 or 1.
- 0 borrowed bits: one network. 1 bit (/25): 2 subnets, 192.168.255.0/25 and 192.168.255.128/25. 2 bits (/26): 4, not enough. **3 bits (/27): 8 subnets**, that is the answer.
- Last bit of the network portion = **32**. Subnet 1: 192.168.255.0/27; 2: .32/27; 3: .64/27; 4: .96/27; 5: .128/27. The three remaining subnets: .160, .192 and .224/27.

### 3. Which subnet does a host belong to?

Method: write the address in binary, identify where the network part ends (borrowed bits included), set all host bits to **0**, convert back to dotted decimal.

- 192.168.5.57/27: 3 borrowed bits; last octet 57 = 0011 1001 → host bits to 0 → 0010 0000 = 32. **Subnet 192.168.5.32/27.**
- 192.168.29.219/29: 5 borrowed bits → **subnet 192.168.29.216/29.**

### 4. Class C reference table (Jeremy recommends memorizing it)

| Prefix | Subnets | Usable hosts |
| :--- | :--- | :--- |
| /25 | 2 | 126 |
| /26 | 4 | 62 |
| /27 | 8 | 30 |
| /28 | 16 | 14 |
| /29 | 32 | 6 |
| /30 | 64 | 2 |
| /31 | 128 | 0 (but usable on point-to-point, no network or broadcast address) |
| /32 | 256 | 0 (identifies a specific host in routes, etc.) |

Each borrowed bit **doubles** the number of subnets; each host bit **doubles** the number of addresses, minus 2.

### 5. Class B: exactly the same process

**Exercise 1**: 172.16.0.0/16, create **80 subnets**. Which prefix length?

| Borrowed bits | Subnets | Prefix | Dotted decimal mask |
| :--- | :--- | :--- | :--- |
| 1 | 2 | /17 | 255.255.128.0 |
| 2 | 4 | /18 | 255.255.192.0 |
| 3 | 8 | /19 | 255.255.224.0 |
| 4 | 16 | /20 | 255.255.240.0 |
| 5 | 32 | /21 | 255.255.248.0 |
| 6 | 64 | /22 | 255.255.252.0 |
| 7 | **128** | **/23** | **255.255.254.0** |

Answer: **/23** (/22 only allows 64). First subnets: 172.16.0.0/23, 172.16.2.0/23, 172.16.4.0/23, 172.16.6.0, 172.16.8.0, etc. **Reminder: in the Cisco CLI you cannot type /17, you must enter the dotted decimal mask 255.255.128.0.**

**Exercise 2**: 172.22.0.0/16, **500 subnets** → borrow 9 bits (2^9 = 512) → **/25**. You can borrow bits even from the last octet of a class B network.

**Exercise 3**: 172.18.0.0/16, **250 subnets with 250 hosts each** → **/24**: 8 borrowed bits = 256 subnets, 8 host bits = 254 hosts.

**Identify the subnet**: 172.25.217.192/21 → binary, host bits to 0 → **172.25.216.0/21**. Same process as class C, just more host bits.

The equivalent class B chart does **not** need to be memorized ("that would simply be a waste of effort"): just know the pattern 2, 4, 8, 16, 32... for subnets and doubling minus 2 for hosts.

### 6. Exam traps

- Subnets: **2^X without −2**. Hosts: **2^N − 2**.
- /29 gives 8 addresses but only **6** usable.
- Broadcast: host bits to **1**; network address: host bits to **0**.
- Know how to write every prefix length in dotted decimal (255.255.254.0 for /23, etc.), that is what the CLI requires.

### 7. Day 14 quiz (5 questions, answers given in Day 15)

| Question | Answer | Method |
| :--- | :--- | :--- |
| 172.30.0.0/16: 100 subnets with at least 500 hosts each. Which prefix length? | **/23** (255.255.254.0) | Count on your fingers: 2, 4, 8, 16, 32, 64, 128 → 7 borrowed bits. 9 host bits remain → 2^9 − 2 = 510 ≥ 500. |
| What subnet does 172.21.111.201/20 belong to? | **172.21.96.0/20** | Binary, host bits to 0, back to dotted decimal. |
| Broadcast address of the network 192.168.91.78/26 belongs to? | **192.168.91.127** | Same method but host bits to 1. |
| 172.16.0.0/16 divided into 4 equal subnets: network and broadcast addresses of the second subnet? | **172.16.64.0** and **172.16.127.255** | 4 subnets = 2 borrowed bits = /18. Last borrowed bit to 1 → .64.0; host bits to 1 → .127.255. |
| 172.30.0.0/16 into subnets of 1,000 hosts: how many subnets? | **64** | 1,000 hosts → 10 host bits (2^10 − 2 = 1,022). 16 − 10 = 6 borrowed bits → 2^6 = 64. |
