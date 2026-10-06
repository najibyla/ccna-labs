# CCNA Day 8 : IPv4 Addressing (Part 2) / Adressage IPv4 (partie 2)

> Source : Jeremy's IT Lab, « Free CCNA | IPv4 Addressing (Part 2) | Day 8 » (31 min), vidéo n°14 de la playlist (cours), et « Configuring IP Addresses | Day 8 Lab » (10 min), vidéo n°15 (lab Packet Tracer). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Retour sur les classes

- Le Day 7 a dit que la plage 127 (loopback) n'est pas vraiment en classe A. La plage **0** est elle aussi réservée, donc certains font commencer la classe A à 1 : plage **1 à 126**. Les sources divergent : **retenir 0 à 127**, en sachant que 0 et 127 sont réservés et que la plage utilisable est 1 à 126.
- Tableau Wikipédia : bits de tête 0 / 10 / 110 ; taille du champ réseau (*network number bit field*, c'est-à-dire la longueur de préfixe) 8 / 16 / 24 bits ; taille du reste (*rest bit field*, la partie hôte) 24 / 16 / 8 bits ; le nombre d'adresses par réseau vaut **2 puissance (longueur de la partie hôte)**, adresses réseau et broadcast comprises.

### 2. Nombre d'hôtes utilisables : 2^N − 2

N = nombre de bits de la partie hôte. On retire l'**adresse réseau** (*network address*, aussi appelée *network ID*, partie hôte tout à 0) et l'**adresse de broadcast** (partie hôte tout à 1), qui ne sont pas assignables.

| Réseau | Bits hôte | Adresses | Hôtes utilisables |
| :--- | :--- | :--- | :--- |
| 192.168.1.0/24 (classe C) | 8 | 256 | **254** |
| 172.16.0.0/16 (classe B) | 16 | 65 536 | **65 534** |
| 10.0.0.0/8 (classe A) | 24 | 16 777 216 | **16 777 214** |

### 3. Première et dernière adresse utilisable

- **Première utilisable = adresse réseau + 1** (dernier bit de la partie hôte passé à 1).
- **Dernière utilisable = adresse de broadcast − 1** (dernier bit passé à 0).

| Réseau | Adresse réseau | Première utilisable | Broadcast | Dernière utilisable |
| :--- | :--- | :--- | :--- | :--- |
| 192.168.1.0/24 | 192.168.1.0 | 192.168.1.1 | 192.168.1.255 | 192.168.1.254 |
| 172.16.0.0/16 | 172.16.0.0 | 172.16.0.1 | 172.16.255.255 | 172.16.255.254 |
| 10.0.0.0/8 | 10.0.0.0 | 10.0.0.1 | 10.255.255.255 | 10.255.255.254 |

### 4. Configurer des adresses IP sur un routeur Cisco (démo GNS3)

Topologie : R1 relié à trois réseaux, un PC par switch (irréaliste, c'est pour la démo). Classe A 10.0.0.0/8 : PC1 = 10.0.0.1 (première utilisable), R1 G0/0 = 10.255.255.254 (dernière). Classe B 172.16.0.0/16 : PC2 = 172.16.0.1, R1 G0/1 = 172.16.255.254. Classe C 192.168.0.0/24 : PC3 = 192.168.0.1, R1 G0/2 = 192.168.0.254.

**`show ip interface brief`**, colonne par colonne :

- **Interface** : les interfaces de l'équipement (ici G0/0 à G0/3).
- **IP-Address** : *unassigned* avant configuration.
- **OK?** : héritage, indique si l'adresse est valide ; les équipements modernes refusent une adresse invalide, on ne devrait jamais voir *NO*.
- **Method** : comment l'adresse a été attribuée. *unset* avant, **manual** après une configuration à la main.
- **Status** : état **couche 1**. *up* si l'interface est activée, câblée et bien connectée en face. **`administratively down`** = désactivée par la commande `shutdown`. C'est **l'état par défaut des interfaces de routeur Cisco**, même câblées. Les interfaces de switch, elles, ne sont pas `shutdown` par défaut : elles sont *up* si connectées, *down* sinon.
- **Protocol** : état **couche 2**. Si la couche 1 est *down*, la couche 2 l'est aussi. **On ne verra jamais status `down` avec protocol `up`** ; l'inverse est possible. Après configuration, on attend **up/up**.

Configuration de G0/0 : `conf t`, `interface gigabitethernet 0/0` (l'invite devient `(config-if)#`). Variantes acceptées : sans espace (`gigabitethernet0/0`), `in` est le raccourci le plus court de `interface` (un seul choix commençant par « in » ; Jeremy tape `int`), et `g0/0` fonctionne bien que `g` seul soit ambigu. Puis `ip address 10.255.255.254 255.0.0.0` : l'aide contextuelle `?` annonce le **subnet mask** (autre nom du *netmask*), à écrire en décimal pointé, pas en /8. Puis **`no shutdown`** : `no` devant une commande l'annule. Deux messages apparaissent : *Interface GigabitEthernet0/0, changed state to up* (couche 1, colonne Status) puis *Line protocol on Interface GigabitEthernet0/0, changed state to up* (couche 2, colonne Protocol). Vérification avec `do sh ip int br` (`do` permet une commande privilégiée depuis le mode de configuration).

G0/1 : on tape `int g0/1` **directement depuis `(config-if)#`**, sans `exit`. `ip add 172.16.255.254 255.255.0.0`, `no shut`. G0/2 : `ip address 192.168.0.254 255.255.255.0`, `no shut`. Résultat : trois adresses, method *manual*, up/up partout.

### 5. Autres commandes `show` sur les interfaces

- **`show interfaces g0/0`** : surtout de l'information couche 1 et 2, un peu de couche 3. *GigabitEthernet0/0 is up* (couche 1), *line protocol is up* (couche 2) : l'équivalent des colonnes Status et Protocol. *Hardware is 1GBE* (1 gigabit Ethernet), *address is 0c1b.8444.f000* : la MAC de l'interface, suivie de **BIA** (*burned-in address*) : la MAC physique réelle. Elle est affichée deux fois car on peut configurer une autre MAC dans la CLI (rare). *Internet address is 10.255.255.254/8*. Sans préciser l'interface, la sortie est très longue.
- **`show interfaces description`** : colonnes Status et Protocol comme `show ip interface brief`, plus la **description**. Les descriptions sont facultatives mais très utiles. Commande `description` (ou `desc`) en mode interface ; aucune règle de forme, Jeremy met des dièses et l'équipement en face.
- Retenir ces trois commandes : `show ip interface brief`, `show interfaces`, `show interfaces description`.

### Pièges d'examen

- **Interfaces de routeur : `shutdown` par défaut** (administratively down) ; **interfaces de switch : non**. Il faut `no shutdown` sur un routeur.
- Status = couche 1, Protocol = couche 2 ; **jamais down/up**, mais up/down est possible.
- Sur Cisco, le masque s'écrit en **décimal pointé** : /8 = 255.0.0.0, /16 = 255.255.0.0, /24 = 255.255.255.0.
- Hôtes utilisables = **2^N − 2**, où N est le nombre de bits hôte ; première utilisable = réseau + 1, dernière = broadcast − 1.
- Classe A : 0 à 127 pour l'examen, mais 0 et 127 sont réservés.

### Commandes IOS

```text
R1# show ip interface brief                  ! interfaces, IP, Method, Status (L1), Protocol (L2)
R1# configure terminal                       ! raccourci : conf t
R1(config)# hostname R1                      ! change l'invite
R1(config)# interface gigabitethernet 0/0    ! aussi : int g0/0, in g0/0, interface gigabitethernet0/0
R1(config-if)# ip address 10.255.255.254 255.0.0.0   ! adresse + masque en décimal pointé (ip add ...)
R1(config-if)# no shutdown                   ! active l'interface (no shut) ; shutdown est le défaut routeur
R1(config-if)# description ## to SW1 ##      ! description libre (desc ...)
R1(config-if)# interface g0/1                ! passer à une autre interface sans exit
R1(config-if)# do show ip interface brief    ! do : commande privilégiée depuis un mode de config
R1(config-if)# end                           ! retour direct au mode privilégié (ou exit deux fois)
R1# show interfaces g0/0                     ! détail L1/L2 d'une interface, MAC et BIA, adresse IP
R1# show interfaces description              ! Status, Protocol et description de chaque interface
R1# show running-config                      ! vérifier la configuration courante
R1# copy running-config startup-config       ! sauvegarder ; équivalents : write memory, write, wr
```

Raccourci clavier vu dans le lab : **Ctrl+A** ramène le curseur en début de ligne (pour ajouter `do` devant une commande rappelée avec la flèche haut).

### Le lab (vidéo n°15)

**Objectif** : configurer les adresses IP d'un routeur et de trois PC, puis vérifier avec ping. Même topologie que la démo, adresses changées : classe A **15.0.0.0/8**, classe B **182.98.0.0/16**, classe C **201.191.20.0/24**.

1. **Hostname** : `enable`, `conf t`, `hostname R1` (l'invite passe de *Router* à *R1*).
2. **Lister les interfaces** : `show ip interface brief` échoue en mode de configuration ; flèche haut, Ctrl+A, ajouter `do`. Tout est *unset* et *administratively down* / *down*.
3. **Interfaces** (adresse, description, activation) :
   - G0/0 : `ip address 15.255.255.254 255.0.0.0`, `description ## to SW1 ##`, `no shutdown` (deux messages « changed state to up »).
   - `interface g0/1` directement : `ip address 182.98.255.254 255.255.0.0`, `description ## to SW2 ##`, `no shut`.
   - `int g0/2` : `ip address 201.191.20.254 255.255.255.0`, `description ## to SW3 ##`, `no shut`.
   - `end` (ou `exit` deux fois), puis `show ip interface brief` : adresses présentes, method **manual**, **up/up**.
4. **`show running-config`** : on voit descriptions et adresses, les commandes par défaut `duplex auto` et `speed auto`, et sur l'interface *Vlan1* la commande `shutdown` appliquée par défaut.
5. **Sauvegarder** : `copy running-config startup-config`, `write memory` ou `write` ; Jeremy utilise `wr`.
6. **PC1, PC2, PC3** (onglet *Config*) : la passerelle (*gateway*) est pré-configurée avec l'adresse de R1 (rôle expliqué avec le routage). Dans *FastEthernet0*, saisir 15.0.0.1, 182.98.0.1, 201.191.20.1 : Packet Tracer **remplit le masque automatiquement** d'après la classe (255.0.0.0, 255.255.0.0, 255.255.255.0).
7. **Vérification** : sur PC1, *Desktop* > *Command Prompt*, `ping 182.98.0.1` (PC2) et `ping 201.191.20.1` (PC3) réussissent.

### Le quiz (5 questions)

Pour chaque adresse, trouver : adresse réseau, nombre maximal d'hôtes, broadcast, première et dernière utilisables. Raisonnement commun : le préfixe donne la partie réseau ; hôtes = 2^(bits hôte) − 2 ; première = réseau + 1 ; dernière = broadcast − 1.

| N° | Adresse | Réseau | Hôtes max | Broadcast | Première | Dernière |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | PC1 : 43.109.23.12/8 | 43.0.0.0 | 16 777 214 (2^24 − 2) | 43.255.255.255 | 43.0.0.1 | 43.255.255.254 |
| 2 | PC4 : 129.221.23.13/16 | 129.221.0.0 | 65 534 (2^16 − 2) | 129.221.255.255 | 129.221.0.1 | 129.221.255.254 |
| 3 | PC8 : 209.211.3.22/24 | 209.211.3.0 | 254 (2^8 − 2) | 209.211.3.255 | 209.211.3.1 | 209.211.3.254 |
| 4 | PC5 : 2.71.209.233/8 | 2.0.0.0 | 16 777 214 (2^24 − 2) | 2.255.255.255 | 2.0.0.1 | 2.255.255.254 |
| 5 | PC6 : 155.200.201.141/16 | 155.200.0.0 | 65 534 (2^16 − 2) | 155.200.255.255 | 155.200.0.1 | 155.200.255.254 |

---

## 🇬🇧 English version

### 1. Classes revisited

- Day 7 said the 127 range (loopback) is generally not considered part of class A. The **0** range is also reserved, so some say class A really begins at 1: range **1 to 126**. Sources differ: **remember 0 to 127**, while keeping in mind that 0 and 127 are reserved and the usable range is 1 to 126.
- Wikipedia chart: leading bits 0 / 10 / 110; *network number bit field* size (the prefix length) 8 / 16 / 24 bits; *rest bit field* size (the host portion) 24 / 16 / 8 bits; the number of addresses per network is **2 to the power of the host portion length**, including the network and broadcast addresses.

### 2. Usable hosts: 2^N − 2

N = number of host bits. Subtract the **network address** (also called *network ID*, host portion all 0s) and the **broadcast address** (host portion all 1s), which cannot be assigned.

| Network | Host bits | Addresses | Usable hosts |
| :--- | :--- | :--- | :--- |
| 192.168.1.0/24 (class C) | 8 | 256 | **254** |
| 172.16.0.0/16 (class B) | 16 | 65,536 | **65,534** |
| 10.0.0.0/8 (class A) | 24 | 16,777,216 | **16,777,214** |

### 3. First and last usable address

- **First usable = network address + 1** (last host bit switched to 1).
- **Last usable = broadcast address − 1** (last bit switched to 0).

| Network | Network address | First usable | Broadcast | Last usable |
| :--- | :--- | :--- | :--- | :--- |
| 192.168.1.0/24 | 192.168.1.0 | 192.168.1.1 | 192.168.1.255 | 192.168.1.254 |
| 172.16.0.0/16 | 172.16.0.0 | 172.16.0.1 | 172.16.255.255 | 172.16.255.254 |
| 10.0.0.0/8 | 10.0.0.0 | 10.0.0.1 | 10.255.255.255 | 10.255.255.254 |

### 4. Configuring IP addresses on a Cisco router (GNS3 demo)

Topology: R1 connected to three networks, one PC per switch (unrealistic, just for the demo). Class A 10.0.0.0/8: PC1 = 10.0.0.1 (first usable), R1 G0/0 = 10.255.255.254 (last). Class B 172.16.0.0/16: PC2 = 172.16.0.1, R1 G0/1 = 172.16.255.254. Class C 192.168.0.0/24: PC3 = 192.168.0.1, R1 G0/2 = 192.168.0.254.

**`show ip interface brief`**, column by column:

- **Interface**: the device's interfaces (here G0/0 to G0/3).
- **IP-Address**: *unassigned* before configuration.
- **OK?**: a legacy field saying whether the address is valid; modern devices refuse invalid addresses, so you should never see *NO*.
- **Method**: how the address was assigned. *unset* before, **manual** after manual configuration.
- **Status**: **Layer 1** status. *up* if the interface is enabled, cabled and properly connected at the other end. **`administratively down`** = disabled with the `shutdown` command. That is **the default state of Cisco router interfaces**, even when cabled. Switch interfaces are not shut down by default: *up* if connected, *down* if not.
- **Protocol**: **Layer 2** status. If Layer 1 is down, Layer 2 cannot operate. **You will never see status `down` with protocol `up`**; the reverse is possible. After configuration, expect **up/up**.

Configuring G0/0: `conf t`, `interface gigabitethernet 0/0` (prompt becomes `(config-if)#`). Accepted variants: no space (`gigabitethernet0/0`), `in` is the shortest form of `interface` (only one command starts with "in"; Jeremy types `int`), and `g0/0` works even though `g` alone is ambiguous. Then `ip address 10.255.255.254 255.0.0.0`: context-sensitive help `?` shows the next option is the **subnet mask** (another name for *netmask*), written in dotted decimal rather than /8. Then **`no shutdown`**: `no` in front of a command cancels it. Two messages appear: *Interface GigabitEthernet0/0, changed state to up* (Layer 1, Status column) then *Line protocol on Interface GigabitEthernet0/0, changed state to up* (Layer 2, Protocol column). Check with `do sh ip int br` (`do` runs a privileged exec command from a configuration mode).

G0/1: type `int g0/1` **directly from `(config-if)#`**, no `exit` needed. `ip add 172.16.255.254 255.255.0.0`, `no shut`. G0/2: `ip address 192.168.0.254 255.255.255.0`, `no shut`. Result: three addresses, method *manual*, up/up everywhere.

### 5. Other `show` commands for interfaces

- **`show interfaces g0/0`**: mainly Layer 1 and Layer 2 information, some Layer 3. *GigabitEthernet0/0 is up* (Layer 1), *line protocol is up* (Layer 2): same as the Status and Protocol columns. *Hardware is 1GBE* (1 gigabit Ethernet), *address is 0c1b.8444.f000*: the interface MAC, followed by **BIA** (*burned-in address*): the actual physical MAC. It is listed twice because a different MAC can be configured in the CLI (rarely done). *Internet address is 10.255.255.254/8*. Without an interface name the output is very long.
- **`show interfaces description`**: Status and Protocol columns like `show ip interface brief`, plus the **description**. Descriptions are optional but very helpful. The `description` (or `desc`) command in interface mode; no rules on format, Jeremy uses hashtags and the connected device.
- Remember these three: `show ip interface brief`, `show interfaces`, `show interfaces description`.

### Exam traps

- **Router interfaces: `shutdown` by default** (administratively down); **switch interfaces: not**. A router needs `no shutdown`.
- Status = Layer 1, Protocol = Layer 2; **never down/up**, but up/down is possible.
- On Cisco, the mask is written in **dotted decimal**: /8 = 255.0.0.0, /16 = 255.255.0.0, /24 = 255.255.255.0.
- Usable hosts = **2^N − 2**, N being the number of host bits; first usable = network + 1, last = broadcast − 1.
- Class A: 0 to 127 for the exam, but 0 and 127 are reserved.

### IOS commands

```text
R1# show ip interface brief                  ! interfaces, IP, Method, Status (L1), Protocol (L2)
R1# configure terminal                       ! shortcut: conf t
R1(config)# hostname R1                      ! changes the prompt
R1(config)# interface gigabitethernet 0/0    ! also: int g0/0, in g0/0, interface gigabitethernet0/0
R1(config-if)# ip address 10.255.255.254 255.0.0.0   ! address + dotted decimal mask (ip add ...)
R1(config-if)# no shutdown                   ! enables the interface (no shut); shutdown is the router default
R1(config-if)# description ## to SW1 ##      ! free-form description (desc ...)
R1(config-if)# interface g0/1                ! move to another interface without exit
R1(config-if)# do show ip interface brief    ! do: privileged exec command from a config mode
R1(config-if)# end                           ! straight back to privileged exec (or exit twice)
R1# show interfaces g0/0                     ! L1/L2 detail of one interface, MAC and BIA, IP address
R1# show interfaces description              ! Status, Protocol and description of each interface
R1# show running-config                      ! check the running configuration
R1# copy running-config startup-config       ! save; equivalents: write memory, write, wr
```

Keyboard shortcut seen in the lab: **Ctrl+A** moves the cursor to the beginning of the line (to add `do` in front of a command recalled with the up arrow).

### The lab (video #15)

**Goal**: configure IP addresses on a router and three PCs, then verify with ping. Same topology as the demo with new addresses: class A **15.0.0.0/8**, class B **182.98.0.0/16**, class C **201.191.20.0/24**.

1. **Hostname**: `enable`, `conf t`, `hostname R1` (prompt changes from *Router* to *R1*).
2. **List interfaces**: `show ip interface brief` fails in config mode; up arrow, Ctrl+A, add `do`. Everything is *unset* and *administratively down* / *down*.
3. **Interfaces** (address, description, enable):
   - G0/0: `ip address 15.255.255.254 255.0.0.0`, `description ## to SW1 ##`, `no shutdown` (two "changed state to up" messages).
   - `interface g0/1` directly: `ip address 182.98.255.254 255.255.0.0`, `description ## to SW2 ##`, `no shut`.
   - `int g0/2`: `ip address 201.191.20.254 255.255.255.0`, `description ## to SW3 ##`, `no shut`.
   - `end` (or `exit` twice), then `show ip interface brief`: addresses present, method **manual**, **up/up**.
4. **`show running-config`**: descriptions and addresses are there, plus the default `duplex auto` and `speed auto` commands, and on the *Vlan1* interface the `shutdown` command applied by default.
5. **Save**: `copy running-config startup-config`, `write memory` or `write`; Jeremy uses `wr`.
6. **PC1, PC2, PC3** (*Config* tab): the gateway is pre-configured with R1's address (its purpose is explained with routing). Under *FastEthernet0*, enter 15.0.0.1, 182.98.0.1, 201.191.20.1: Packet Tracer **fills in the subnet mask automatically** from the class (255.0.0.0, 255.255.0.0, 255.255.255.0).
7. **Verification**: on PC1, *Desktop* > *Command Prompt*, `ping 182.98.0.1` (PC2) and `ping 201.191.20.1` (PC3) both succeed.

### The quiz (5 questions)

For each address, find: network address, maximum hosts, broadcast, first and last usable addresses. Same reasoning each time: the prefix gives the network portion; hosts = 2^(host bits) − 2; first = network + 1; last = broadcast − 1.

| # | Address | Network | Max hosts | Broadcast | First | Last |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | PC1: 43.109.23.12/8 | 43.0.0.0 | 16,777,214 (2^24 − 2) | 43.255.255.255 | 43.0.0.1 | 43.255.255.254 |
| 2 | PC4: 129.221.23.13/16 | 129.221.0.0 | 65,534 (2^16 − 2) | 129.221.255.255 | 129.221.0.1 | 129.221.255.254 |
| 3 | PC8: 209.211.3.22/24 | 209.211.3.0 | 254 (2^8 − 2) | 209.211.3.255 | 209.211.3.1 | 209.211.3.254 |
| 4 | PC5: 2.71.209.233/8 | 2.0.0.0 | 16,777,214 (2^24 − 2) | 2.255.255.255 | 2.0.0.1 | 2.255.255.254 |
| 5 | PC6: 155.200.201.141/16 | 155.200.0.0 | 65,534 (2^16 − 2) | 155.200.255.255 | 155.200.0.1 | 155.200.255.254 |
