# CCNA Day 11 : Routing Fundamentals, Static Routing / Bases du routage, routage statique

> Source : Jeremy's IT Lab, « Free CCNA | Routing Fundamentals | Day 11 (part 1) » (31 min), vidéo n°19 de la playlist (cours, partie 1) ; « Static Routing | Day 11 (part 2) » (38 min), vidéo n°20 (cours, partie 2) ; « Configuring Static Routes | Day 11 Lab 1 » (12 min), vidéo n°21 (lab de configuration) ; « Troubleshooting Static Routes | Day 11 Lab 2 » (10 min), vidéo n°22 (lab de dépannage). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Qu'est-ce que le routage ? (partie 1)

- Le **routage** (*routing*) est le processus par lequel un routeur **détermine le chemin** que les paquets IP doivent suivre pour atteindre leur destination. Les destinations connues sont stockées dans la **table de routage** (*routing table*) : l'équivalent de la table MAC d'un switch, mais qui fonctionne différemment.
- Deux méthodes pour apprendre des routes : le **routage dynamique** (*dynamic routing*, protocoles comme OSPF, vus plus tard) et le **routage statique** (*static routing*, routes configurées à la main par l'administrateur). Les routes **connectées** et **locales** de cette vidéo ne relèvent d'aucune des deux : elles sont ajoutées automatiquement.
- Une **route est une instruction** : « pour envoyer un paquet à la destination X, envoie-le au **prochain saut** (*next hop*) Y », Y étant le routeur suivant sur le chemin ; ou « si la destination est directement connectée, envoie-le directement » ; ou « si la destination est ma propre adresse, garde le paquet ».

### 2. La topologie des deux vidéos

Quatre routeurs forment un **WAN** (*Wide Area Network*, réseau étendu sur une grande zone géographique : villes ou pays différents), deux LAN sur R1 et R4. Jeremy donne à chaque routeur un dernier octet égal à son numéro (schéma simplifié pour le cours, pas réaliste).

| Réseau | Interfaces |
| :--- | :--- |
| 192.168.1.0/24 (LAN) | R1 G0/2 = .1, PC1 = .10 |
| 192.168.12.0/24 | R1 G0/1 = .1, R2 G0/0 = .2 |
| 192.168.13.0/24 | R1 G0/0 = .1, R3 G0/0 = .3 |
| 192.168.24.0/24 | R2 G0/1 = .2, R4 G0/0 = .4 |
| 192.168.34.0/24 | R3 G0/1 = .3, R4 G0/1 = .4 |
| 192.168.4.0/24 (LAN) | R4 G0/2 = .4, PC4 = .10 |

Sur R1, Jeremy configure `ip address 192.168.13.1 255.255.255.0` + `no shutdown` sur G0/0, puis passe à G0/1 et G0/2 avec `interface g0/1` **directement depuis le mode interface**, sans `exit`.

### 3. Routes connectées et locales dans `show ip route`

- La sortie a deux parties : la **légende des codes** en haut, les **routes** en bas.
- **C, connected** : route vers le **réseau** auquel l'interface est connectée, avec le masque configuré sur l'interface (192.168.1.1/24 → route vers **192.168.1.0/24**, « is directly connected, GigabitEthernet0/2 »). Elle couvre tous les hôtes du réseau (.10, .100, .232…) : « pour ce réseau, sors par G0/2 ».
- **L, local** : route vers l'**adresse exacte** de l'interface, avec un masque **/32** (192.168.1.1/32) : tous les bits sont fixés, une seule adresse. « Un paquet pour cette adresse est pour moi. »
- Quand on configure une adresse et qu'on active l'interface, **deux routes par interface** sont ajoutées automatiquement : R1 a déjà six routes sans aucune configuration de routage. Si l'interface est désactivée, elles n'apparaissent pas.
- Les lignes « 192.168.1.0/24 is variably subnetted, 2 subnets, 2 masks » **ne sont pas des routes** : elles indiquent qu'il y a deux routes vers des sous-réseaux de ce réseau avec deux masques (/24 et /32). Le subnetting sera vu plus tard ; ignorer ces lignes.

### 4. Correspondance et sélection de route

- Une route **correspond** (*matches*) à une destination si l'adresse IP destination du paquet fait partie du réseau de la route. /24 = masque 255.255.255.0 : les trois premiers octets sont fixés, le dernier libre, donc 192.168.1.0/24 couvre 192.168.1.0 à .255 : 192.168.1.2, .7, .89 correspondent ; 192.168.2.1 ne correspond pas (autre route, ou abandon).
- Un paquet pour 192.168.1.1 correspond à **deux routes** (1.0/24 et 1.1/32). Le routeur choisit la route **la plus spécifique** : la route correspondante avec la **plus longue longueur de préfixe** (*longest prefix length*). /32 ne couvre qu'une adresse contre 256 pour /24 : R1 **garde le paquet pour lui** et le désencapsule.
- Exemples sur R1 : 192.168.1.1 → local, reçu pour lui-même ; 192.168.13.3 → connectée 13.0/24, envoyé par G0/0 ; 192.168.1.244 → connectée 1.0/24 ; 192.168.12.1 → local 12.1/32 (deux routes correspondent, la /32 gagne) ; 192.168.4.10 → **aucune route : paquet abandonné**.
- **Un routeur n'inonde jamais** (*flood*) : sans route correspondante, il **abandonne** le paquet. Le switch, lui, inonde les trames à destination inconnue et cherche une correspondance **exacte** dans sa table MAC, sans notion de « plus spécifique ».

### 5. Passerelle par défaut et route par défaut (partie 2)

- R2, R3 et R4 ont aussi leurs routes automatiques (4, 4 et 6 routes) : chacun connaît ses propres adresses et ses réseaux connectés, mais pas les réseaux **distants** (*remote*). R4 peut livrer un paquet à PC4 (route vers 4.0/24) mais abandonne un paquet pour PC1 (192.168.1.10).
- Un hôte final envoie directement dans son réseau ; pour toute autre destination, il envoie à sa **passerelle par défaut** (*default gateway* ; *gateway* est un vieux mot pour routeur). PC1 et PC4 sont des hôtes Linux (interface **eth0**), configurés dans un fichier texte : `address 192.168.1.10/24`, `gateway 192.168.1.1`.
- La passerelle par défaut est une **route par défaut** : route vers **0.0.0.0/0**, aucun bit fixé, de 0.0.0.0 à 255.255.255.255 (plus de 4 milliards d'adresses) : la route **la moins spécifique** possible, à l'opposé d'une /32. Elle dit : « s'il n'y a pas de correspondance plus spécifique, n'abandonne pas, envoie par ici ». Les hôtes finaux n'ont en général besoin de rien d'autre.

### 6. Pourquoi des routes statiques, et lesquelles

- PC1 envoie à PC4 : IP source 192.168.1.10, IP destination 192.168.4.10 ; mais la **MAC destination** de la trame est celle de **R1 G0/2**, apprise par une **requête ARP** vers 192.168.1.1 (détail dans « Life of a Packet »). R1 désencapsule, cherche la route la plus spécifique : avec seulement ses routes C et L, **aucune correspondance → paquet abandonné**. Il lui faut une route vers 192.168.4.0/24.
- Deux chemins possibles (via R3 ou via R2). On peut les utiliser tous les deux (**load-balancing**) ou l'un en secours de l'autre (vu plus tard) ; ici on choisit le **chemin via R3**.
- **Réciprocité** (*two-way reachability*) : chaque routeur du chemin doit avoir une route vers 192.168.1.0/24 **et** vers 192.168.4.0/24, sinon les réponses de PC4 sont abandonnées (par R4, sans route vers 1.0/24). En revanche, un routeur n'a **pas besoin** des réseaux intermédiaires : R1 n'a pas besoin de 34.0/24, il suffit qu'il envoie vers R3, qui prend le relais.

| Routeur | Destination | Prochain saut |
| :--- | :--- | :--- |
| R1 | 192.168.1.0/24 | connectée |
| R1 | 192.168.4.0/24 | **192.168.13.3** (R3 G0/0) |
| R3 | 192.168.1.0/24 | **192.168.13.1** (R1 G0/0) |
| R3 | 192.168.4.0/24 | **192.168.34.4** (R4 G0/1) |
| R4 | 192.168.1.0/24 | **192.168.34.3** (R3 G0/1) |
| R4 | 192.168.4.0/24 | connectée |

- Commande (mode de configuration globale) : `ip route <réseau> <masque> <prochain saut>`, par exemple sur R1 `ip route 192.168.4.0 255.255.255.0 192.168.13.3`. Dans `show ip route`, code **S** (static) ; entre crochets **[1/0]** = **distance administrative** et **métrique** (vus plus tard).
- Test : ping de PC1 vers PC4, **5 packets transmitted, 5 received, 0% packet loss** : un ping réussi prouve la réciprocité.
- Aperçu de l'encapsulation : les IP source et destination **ne changent jamais** ; à chaque routeur, le paquet est désencapsulé puis ré-encapsulé dans une **nouvelle trame** dont la MAC destination est celle du prochain saut (R3 G0/0, puis R4 G0/1, puis PC4). Seul le dernier tronçon a IP et MAC destination du **même équipement**.

### 7. Trois façons d'écrire une route statique, et la route par défaut

- **Prochain saut seul** : `ip route 192.168.4.0 255.255.255.0 192.168.13.3` (l'option que Jeremy utilise d'habitude).
- **Interface de sortie seule** (*exit interface*), démontrée sur R2 : `ip route 192.168.1.0 255.255.255.0 g0/0`. La table affiche alors « 192.168.1.0/24 **is directly connected**, GigabitEthernet0/0 » alors que ce réseau n'est pas connecté à R2. Ces routes reposent sur le **proxy ARP** (hors programme CCNA), en général sans problème.
- **Les deux** : `ip route 192.168.4.0 255.255.255.0 g0/1 192.168.24.4`.
- Aucune méthode n'est meilleure ; il faut connaître les trois.
- **Route par défaut sur un routeur** : même commande avec réseau et masque à **0.0.0.0** : `ip route 0.0.0.0 0.0.0.0 203.0.113.2`. Usage courant : envoyer vers **Internet** tout ce qui ne correspond pas aux routes internes (exemple : 10.0.0.0/8 via R2 et 172.16.0.0/16 via R3 restent internes). Avant : « **Gateway of last resort is not set** » (*gateway of last resort* = autre nom de la passerelle par défaut). Après : code **S\*** où l'astérisque signifie **candidate default** (il peut y en avoir plusieurs), et « Gateway of last resort is 203.0.113.2 to network 0.0.0.0 ».

### Pièges d'examen

- **C** = route vers le réseau connecté (masque de l'interface) ; **L** = adresse exacte de l'interface en **/32**. Deux routes par interface, seulement si l'interface est **activée**.
- Route choisie = **correspondante** et **au préfixe le plus long**. Un routeur **abandonne** un paquet sans route ; il n'inonde jamais (contrairement au switch, qui cherche une correspondance exacte).
- Dans `ip route`, le masque s'écrit en **décimal pointé**, jamais en /N. Route par défaut = **0.0.0.0 0.0.0.0** (pas 255.255.255.255).
- Une route statique avec interface de sortie seule s'affiche « directly connected » mais porte le code **S** ; on ne peut pas configurer une adresse réseau (172.20.0.0) sur une interface.
- Réciprocité : chaque routeur du chemin doit connaître **les deux** réseaux d'extrémité ; les réseaux intermédiaires ne sont pas nécessaires.
- Dans une trame, la **MAC destination** est celle du prochain saut ; l'**IP destination** reste celle de l'hôte final.
- Lab 2 : ajouter une route correcte **ne remplace pas** la mauvaise (les deux restent, load-balancing) ; il faut `no ip route …`. À l'inverse, `ip address` **écrase** l'adresse précédente.

### Commandes IOS

```text
R1# show ip route                                   ! table de routage : codes (C, L, S, S*), routes, gateway of last resort
R1(config)# ip route 192.168.4.0 255.255.255.0 192.168.13.3     ! route statique, prochain saut (masque en décimal pointé)
R2(config)# ip route 192.168.1.0 255.255.255.0 g0/0             ! route statique, interface de sortie seule (proxy ARP)
R2(config)# ip route 192.168.4.0 255.255.255.0 g0/1 192.168.24.4 ! interface de sortie + prochain saut
R1(config)# ip route 0.0.0.0 0.0.0.0 203.0.113.2                ! route par défaut (S*, candidate default)
R1(config)# no ip route 192.168.3.0 255.255.255.0 192.168.12.3  ! supprimer une route (no devant la commande complète)
R1(config)# ip route ?                              ! aide contextuelle : destination prefix, mask, forwarding router's address ou interface, distance metric, <cr>
R1# show running-config | include ip route          ! filtrer la configuration : seules les lignes « ip route »
R1(config-if)# ip address 192.168.13.3 255.255.255.0 ! une nouvelle adresse écrase l'ancienne, pas besoin de no
R1(config-if)# do show ip route                     ! do : commande show depuis un mode de configuration
PC> ipconfig                                        ! Windows : adresse, masque, passerelle par défaut
PC> ipconfig /all                                   ! plus de détail, dont la « physical address » (MAC)
```

### Le lab 1 : configurer des routes statiques (vidéo n°21)

**Objectif** : PC1 et PC2 doivent se pinguer à travers R1, R2, R3. Rien n'est pré-configuré (répétition volontaire des bases).

1. **PC1** (*Config*) : passerelle **192.168.1.254** (R1), *FastEthernet0* : 192.168.1.1, Tab remplit 255.255.255.0. Les switches ne sont pas à configurer.
2. **R1** : `enable`, `configure terminal`, `hostname R1`. `interface g0/1` (LAN) : `ip address 192.168.1.254 255.255.255.0`, `description ## to SW1 ##`, `no shutdown`. `interface g0/0` (vers R2) : `ip address 192.168.12.1 255.255.255.0`, `description ## to R2 ##`, `no shutdown`. `do show ip interface brief` : G0/1 up/up, G0/0 **up/down** parce que R2 G0/0 est encore shutdown (normal).
3. **R2** : `hostname R2` ; G0/0 : `ip address 192.168.12.2 255.255.255.0`, `description ## to R1 ##`, `no shutdown` ; G0/1 : `ip address 192.168.13.2 255.255.255.0`, `description ## to R3 ##`, `no shutdown`. G0/1 up/down tant que R3 n'est pas configuré.
4. **R3** : `hostname R3` ; G0/0 : `ip address 192.168.13.3 255.255.255.0`, `description ## to R2 ##`, `no shutdown` ; G0/1 : `ip address 192.168.3.254 255.255.255.0`, `description ## to SW2 ##`, `no shutdown`. Les deux up/up.
5. **PC2** : passerelle **192.168.3.254**, adresse 192.168.3.1.
6. **Routes** (quatre au total, réciprocité) : R1 est connecté à 1.0/24, il lui faut 3.0/24 ; R3 est connecté à 3.0/24, il lui faut 1.0/24 ; R2 a besoin des deux.
   - R1 : `exit` pour revenir en config globale, `ip route 192.168.3.0 255.255.255.0 192.168.12.2`. L'aide `?` montre successivement *destination prefix*, *mask*, puis *forwarding router's address* ou un type d'interface, puis *distance metric* (vu plus tard) et `<cr>`. `do show ip route` : la route **S**, plus les routes C et L.
   - R2 : `ip route 192.168.1.0 255.255.255.0 g0/0` (interface de sortie, pour pratiquer ; un message sur les interfaces non point-à-point apparaît, à ignorer : ici la liaison est bien point à point, contrairement à plusieurs routeurs sur un même switch, un *shared segment*) ; `ip route 192.168.3.0 255.255.255.0 192.168.13.3`.
   - R3 : `ip route 192.168.1.0 255.255.255.0 192.168.13.2`.
7. **Vérification** : sur PC1, `ping 192.168.3.1`. Le premier ping peut échouer à cause d'ARP, les suivants réussissent : PC1 atteint PC2 et PC2 répond.

### Le lab 2 : dépanner des routes statiques (vidéo n°22)

**Objectif** : même topologie, **une erreur de configuration par routeur** ; PC1 et PC2 ne se pinguent plus. Jeremy conseille de chercher soi-même avant de regarder la vidéo (le dépannage tombe aussi à l'examen).

1. **Confirmer le problème** : sur PC1, `ping 192.168.3.1` échoue. `ipconfig` (adresse, masque, passerelle), `ipconfig /all` (la *physical address* = MAC). `ping 192.168.1.254` vers la passerelle réussit.
2. **R1** : `show ip interface brief` correct (up/up). `show ip route` : la route vers 192.168.3.0/24 passe **via 192.168.12.3** au lieu de **192.168.12.2**. `show running-config | include ip route`, clic droit pour copier la ligne, `configure terminal`, coller, **Ctrl+A**, taper `no ` devant, Entrée : la route est supprimée (vérifier avec `do show running-config | include ip route`). Recoller la ligne en remplaçant le 3 par un 2. `do show ip route` : route correcte.
3. **R2** : interfaces correctes. `show ip route` : 192.168.1.0/24 via 192.168.12.1 est bonne, mais 192.168.3.0/24 sort par **G0/0** au lieu de **G0/1**. Jeremy ajoute d'abord la bonne route (`ip route 192.168.3.0 255.255.255.0 g0/1`) sans retirer la mauvaise : **les deux restent** dans la table, le routeur ferait du **load-balancing** entre G0/0 et G0/1. Il faut donc supprimer la mauvaise avec la même méthode (copier, `no `), puis vérifier qu'il ne reste qu'une route par G0/1.
4. **R3** : interfaces up/up mais G0/0 a l'adresse **192.168.23.3** au lieu de **192.168.13.3**. `interface g0/0`, `ip address 192.168.13.3 255.255.255.0` : contrairement aux routes, **la nouvelle adresse écrase l'ancienne** (comparer `do show running-config` avant et après). La route statique vers 1.0/24 via 192.168.13.2 est bien là.
5. **Vérification** : `ping 192.168.3.1` depuis PC1 ; les un ou deux premiers peuvent échouer, puis tout passe.

### Le quiz de la partie 1 (5 questions)

Pour certaines questions, les choix ne sont pas lus dans la transcription ; seule la bonne réponse et son explication le sont.

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| 1. L'adresse configurée sur une interface de routeur apparaît dans la table de routage comme quel type de route ? | **C, local** | Deux routes sont ajoutées quand on configure une adresse et que l'interface est activée : une connectée vers le réseau, une **locale** vers l'adresse exacte. Si l'interface est shutdown, aucune n'apparaît. |
| 2. D'après la table de R1, que fait-il d'un paquet pour 192.168.3.25 ? | **B, il le reçoit pour lui-même** | R1 a une route locale 192.168.3.25/32 : cette adresse est configurée sur son G0/2. |
| 3. Affirmations vraies sur routeurs et switches (deux réponses) | **B et C** | Les switches inondent les trames à destination inconnue (*unknown unicast*) ; les routeurs n'inondent jamais, ils abandonnent les paquets sans route. |
| 4. Quels deux types de routes sont ajoutés automatiquement quand on configure une adresse sur une interface et qu'on l'active ? | **A, C et L** | C = connected, L = local, comme le montre la sortie de `show ip route`. |
| 5. D'après la table de R1, combien de routes correspondent à 10.0.1.23, et laquelle est la plus spécifique ? | **C** | Deux routes correspondent : 10.0.1.0/24 et 10.0.1.23/32 ; la /32 est la plus spécifique et sera choisie. C'est une route locale : R1 garde le paquet. |

### Le quiz de la partie 2 (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| 1. Quelle commande configure une route par défaut ? A `ip route 0.0.0.0 0.0.0.0 10.1.1.255` ; B et D avec un préfixe en /N ; C `ip route 0.0.0.0 255.255.255.255 …` | **A** | Sur Cisco on ne peut pas écrire le préfixe avec un slash, il faut le masque (B et D faux). Dans une route par défaut, tous les bits du masque sont à 0 ; C met tout à 1. |
| 2. D'après la table de R1, quelle interface pour un paquet vers 8.8.8.8 ? | **C, GigabitEthernet0/2** | Seule la route par défaut correspond ; elle indique le prochain saut 203.0.113.2 sans interface. La route vers 203.0.113.0/24 est connectée à G0/2, donc R1 sort par G0/2. |
| 3. Compléter le tableau des routes statiques pour que PC1 et PC4 communiquent (chemin R1, R2, R4) | R1 : 192.168.4.0/24 via **192.168.12.2** ; R2 : 192.168.1.0/24 via **192.168.12.1** et 192.168.4.0/24 via **192.168.24.4** ; R4 : 192.168.1.0/24 via **192.168.24.2** | Chaque routeur du chemin a besoin d'une route vers 1.0/24 et vers 4.0/24 ; R1 et R4 ont déjà une route connectée vers leur LAN. |
| 4. Route « S 172.20.0.0/16 is directly connected, GigabitEthernet0/1 » dans la table de R1 : quelle commande l'a créée ? | **D, `ip route 172.20.0.0 255.255.0.0 g0/1`** | « Directly connected » fait penser à une route connectée (option B, `ip address`), mais le code est **S**, et 172.20.0.0/16 est une adresse réseau, impossible à configurer sur une interface. Une statique avec interface de sortie seule s'affiche ainsi ; le proxy ARP trouve le prochain saut. |
| 5. Combien de routes statiques configurer sur R3 pour qu'il connaisse tous les réseaux du schéma ? | **D, quatre** | R3 connaît ses réseaux connectés 192.168.13.0/24 et 192.168.34.0/24 ; il lui manque 192.168.1.0/24, 4.0/24, 12.0/24 et 24.0/24. |

---

## 🇬🇧 English version

### 1. What is routing? (part 1)

- **Routing** is the process routers use to **determine the path** IP packets should take to reach their destination. Known destinations are stored in the **routing table**: the counterpart of a switch's MAC address table, but it works differently.
- Two main ways to learn routes: **dynamic routing** (protocols such as OSPF, covered later) and **static routing** (routes configured manually by the admin). The **connected** and **local** routes of this video fit neither category: they are added automatically.
- A **route is an instruction**: "to send a packet to destination X, send it to **next hop** Y", Y being the next router in the path; or "if the destination is directly connected, send it directly"; or "if the destination is my own address, receive the packet".

### 2. The topology used in both videos

Four routers form a **WAN** (*Wide Area Network*, spanning a large geographical area: different cities or countries), with two LANs on R1 and R4. Jeremy gives every router a last octet equal to its number (simplified for the lesson, not realistic).

| Network | Interfaces |
| :--- | :--- |
| 192.168.1.0/24 (LAN) | R1 G0/2 = .1, PC1 = .10 |
| 192.168.12.0/24 | R1 G0/1 = .1, R2 G0/0 = .2 |
| 192.168.13.0/24 | R1 G0/0 = .1, R3 G0/0 = .3 |
| 192.168.24.0/24 | R2 G0/1 = .2, R4 G0/0 = .4 |
| 192.168.34.0/24 | R3 G0/1 = .3, R4 G0/1 = .4 |
| 192.168.4.0/24 (LAN) | R4 G0/2 = .4, PC4 = .10 |

On R1, Jeremy configures `ip address 192.168.13.1 255.255.255.0` + `no shutdown` on G0/0, then moves to G0/1 and G0/2 with `interface g0/1` **directly from interface config mode**, no `exit`.

### 3. Connected and local routes in `show ip route`

- The output has two parts: the **codes legend** at the top, the **routes** below.
- **C, connected**: route to the **network** the interface is attached to, with the mask configured on the interface (192.168.1.1/24 → route to **192.168.1.0/24**, "is directly connected, GigabitEthernet0/2"). It covers every host in that network (.10, .100, .232…): "for this network, send out of G0/2".
- **L, local**: route to the **exact address** of the interface, with a **/32** mask (192.168.1.1/32): all bits fixed, a single address. "A packet for this address is for me."
- When you configure an address and enable the interface, **two routes per interface** are added automatically: R1 already has six routes with no routing configuration. If the interface is shut down, they do not appear.
- The lines "192.168.1.0/24 is variably subnetted, 2 subnets, 2 masks" **are not routes**: they mean there are two routes to subnets within that network, with two masks (/24 and /32). Subnetting comes later; ignore these lines.

### 4. Matching and route selection

- A route **matches** a destination if the packet's destination IP is part of the network in the route. /24 = mask 255.255.255.0: the first three octets are fixed, the last is free, so 192.168.1.0/24 covers 192.168.1.0 to .255: 192.168.1.2, .7, .89 match; 192.168.2.1 does not (another route, or drop).
- A packet for 192.168.1.1 matches **two routes** (1.0/24 and 1.1/32). The router picks the **most specific** route: the matching route with the **longest prefix length**. /32 covers one address versus 256 for /24: R1 **receives the packet for itself** and de-encapsulates it.
- Examples on R1: 192.168.1.1 → local, received for itself; 192.168.13.3 → connected 13.0/24, out of G0/0; 192.168.1.244 → connected 1.0/24; 192.168.12.1 → local 12.1/32 (two matches, /32 wins); 192.168.4.10 → **no route: packet dropped**.
- **Routers never flood**: with no matching route, they **drop** the packet. Switches flood frames with an unknown destination and look for an **exact** match in the MAC table; there is no "most specific match" on a switch.

### 5. Default gateway and default route (part 2)

- R2, R3 and R4 also have their automatic routes (4, 4 and 6): each knows its own addresses and its connected networks, but not **remote** networks. R4 can deliver a packet to PC4 (route to 4.0/24) but drops a packet for PC1 (192.168.1.10).
- An end host sends directly within its own network; for any other destination it sends to its **default gateway** (*gateway* is an old word for router). PC1 and PC4 are Linux hosts (interface **eth0**), configured in a text file: `address 192.168.1.10/24`, `gateway 192.168.1.1`.
- The default gateway is a **default route**: a route to **0.0.0.0/0**, no bits fixed, from 0.0.0.0 to 255.255.255.255 (over 4 billion addresses): the **least specific** route possible, the opposite of a /32. It says: "if there is no more specific match, don't drop, send it this way". End hosts usually need nothing else.

### 6. Why static routes, and which ones

- PC1 sends to PC4: source IP 192.168.1.10, destination IP 192.168.4.10; but the frame's **destination MAC** is that of **R1 G0/2**, learned through an **ARP request** to 192.168.1.1 (detailed in "Life of a Packet"). R1 de-encapsulates and looks for the most specific route: with only C and L routes, **no match → packet dropped**. It needs a route to 192.168.4.0/24.
- Two possible paths (via R3 or via R2). Both could be used (**load-balancing**) or one as backup for the other (covered later); here we choose the **path via R3**.
- **Two-way reachability**: every router in the path needs a route to 192.168.1.0/24 **and** to 192.168.4.0/24, otherwise PC4's replies are dropped (by R4, with no route to 1.0/24). But a router does **not** need the intermediate networks: R1 does not need 34.0/24, it only needs to send to R3, which takes over.

| Router | Destination | Next hop |
| :--- | :--- | :--- |
| R1 | 192.168.1.0/24 | connected |
| R1 | 192.168.4.0/24 | **192.168.13.3** (R3 G0/0) |
| R3 | 192.168.1.0/24 | **192.168.13.1** (R1 G0/0) |
| R3 | 192.168.4.0/24 | **192.168.34.4** (R4 G0/1) |
| R4 | 192.168.1.0/24 | **192.168.34.3** (R3 G0/1) |
| R4 | 192.168.4.0/24 | connected |

- Command (global config mode): `ip route <network> <netmask> <next hop>`, e.g. on R1 `ip route 192.168.4.0 255.255.255.0 192.168.13.3`. In `show ip route`, code **S** (static); in square brackets **[1/0]** = **administrative distance** and **metric** (covered later).
- Test: ping from PC1 to PC4, **5 packets transmitted, 5 received, 0% packet loss**: a successful ping proves two-way reachability.
- Encapsulation preview: source and destination IPs **never change**; at each router the packet is de-encapsulated and re-encapsulated in a **new frame** whose destination MAC is the next hop's (R3 G0/0, then R4 G0/1, then PC4). Only on the last leg are the destination IP and MAC those of the **same device**.

### 7. Three ways to write a static route, and the default route

- **Next hop only**: `ip route 192.168.4.0 255.255.255.0 192.168.13.3` (what Jeremy usually uses).
- **Exit interface only**, demonstrated on R2: `ip route 192.168.1.0 255.255.255.0 g0/0`. The table then shows "192.168.1.0/24 **is directly connected**, GigabitEthernet0/0" although that network is not connected to R2. Such routes rely on **proxy ARP** (beyond the CCNA), usually not a problem.
- **Both**: `ip route 192.168.4.0 255.255.255.0 g0/1 192.168.24.4`.
- No method is better than the others; know all three.
- **Default route on a router**: same command with network and mask both **0.0.0.0**: `ip route 0.0.0.0 0.0.0.0 203.0.113.2`. Common use: send everything that does not match internal routes to the **Internet** (example: 10.0.0.0/8 via R2 and 172.16.0.0/16 via R3 stay internal). Before: "**Gateway of last resort is not set**" (*gateway of last resort* = another name for default gateway). After: code **S\*** where the asterisk means **candidate default** (there can be several), and "Gateway of last resort is 203.0.113.2 to network 0.0.0.0".

### Exam traps

- **C** = route to the connected network (interface mask); **L** = exact interface address in **/32**. Two routes per interface, only if the interface is **enabled**.
- Selected route = **matching** and **longest prefix**. A router **drops** a packet with no route; it never floods (unlike a switch, which looks for an exact match).
- In `ip route`, the mask is written in **dotted decimal**, never /N. Default route = **0.0.0.0 0.0.0.0** (not 255.255.255.255).
- A static route with exit interface only shows "directly connected" but carries code **S**; a network address (172.20.0.0) cannot be configured on an interface.
- Two-way reachability: every router in the path must know **both** end networks; intermediate networks are not needed.
- In a frame, the **destination MAC** is the next hop's; the **destination IP** stays the end host's.
- Lab 2: adding a correct route **does not replace** the wrong one (both stay, load-balancing); use `no ip route …`. Conversely, `ip address` **overwrites** the previous address.

### IOS commands

```text
R1# show ip route                                   ! routing table: codes (C, L, S, S*), routes, gateway of last resort
R1(config)# ip route 192.168.4.0 255.255.255.0 192.168.13.3     ! static route, next hop (dotted decimal mask)
R2(config)# ip route 192.168.1.0 255.255.255.0 g0/0             ! static route, exit interface only (proxy ARP)
R2(config)# ip route 192.168.4.0 255.255.255.0 g0/1 192.168.24.4 ! exit interface + next hop
R1(config)# ip route 0.0.0.0 0.0.0.0 203.0.113.2                ! default route (S*, candidate default)
R1(config)# no ip route 192.168.3.0 255.255.255.0 192.168.12.3  ! remove a route (no in front of the full command)
R1(config)# ip route ?                              ! context help: destination prefix, mask, forwarding router's address or interface, distance metric, <cr>
R1# show running-config | include ip route          ! filter the config: only the "ip route" lines
R1(config-if)# ip address 192.168.13.3 255.255.255.0 ! a new address overwrites the old one, no need for no
R1(config-if)# do show ip route                     ! do: show command from a configuration mode
PC> ipconfig                                        ! Windows: address, mask, default gateway
PC> ipconfig /all                                   ! more detail, including the "physical address" (MAC)
```

### Lab 1: configuring static routes (video #21)

**Goal**: PC1 and PC2 must ping each other across R1, R2, R3. Nothing is pre-configured (deliberate repetition of the basics).

1. **PC1** (*Config*): gateway **192.168.1.254** (R1), *FastEthernet0*: 192.168.1.1, Tab fills in 255.255.255.0. The switches need no configuration.
2. **R1**: `enable`, `configure terminal`, `hostname R1`. `interface g0/1` (LAN): `ip address 192.168.1.254 255.255.255.0`, `description ## to SW1 ##`, `no shutdown`. `interface g0/0` (to R2): `ip address 192.168.12.1 255.255.255.0`, `description ## to R2 ##`, `no shutdown`. `do show ip interface brief`: G0/1 up/up, G0/0 **up/down** because R2 G0/0 is still shut down (normal).
3. **R2**: `hostname R2`; G0/0: `ip address 192.168.12.2 255.255.255.0`, `description ## to R1 ##`, `no shutdown`; G0/1: `ip address 192.168.13.2 255.255.255.0`, `description ## to R3 ##`, `no shutdown`. G0/1 up/down until R3 is configured.
4. **R3**: `hostname R3`; G0/0: `ip address 192.168.13.3 255.255.255.0`, `description ## to R2 ##`, `no shutdown`; G0/1: `ip address 192.168.3.254 255.255.255.0`, `description ## to SW2 ##`, `no shutdown`. Both up/up.
5. **PC2**: gateway **192.168.3.254**, address 192.168.3.1.
6. **Routes** (four in total, two-way reachability): R1 is connected to 1.0/24 and needs 3.0/24; R3 is connected to 3.0/24 and needs 1.0/24; R2 needs both.
   - R1: `exit` back to global config, `ip route 192.168.3.0 255.255.255.0 192.168.12.2`. The `?` help shows in turn *destination prefix*, *mask*, then *forwarding router's address* or an interface type, then *distance metric* (covered later) and `<cr>`. `do show ip route`: the **S** route plus the C and L routes.
   - R2: `ip route 192.168.1.0 255.255.255.0 g0/0` (exit interface, for practice; a message about non point-to-point interfaces appears, ignore it: this link is point-to-point, unlike several routers on one switch, a *shared segment*); `ip route 192.168.3.0 255.255.255.0 192.168.13.3`.
   - R3: `ip route 192.168.1.0 255.255.255.0 192.168.13.2`.
7. **Verification**: on PC1, `ping 192.168.3.1`. The first ping may fail because of ARP, the rest succeed: PC1 reaches PC2 and PC2 replies.

### Lab 2: troubleshooting static routes (video #22)

**Goal**: same topology, **one misconfiguration per router**; PC1 and PC2 can no longer ping. Jeremy recommends trying it yourself before watching (troubleshooting also appears on the exam).

1. **Confirm the problem**: on PC1, `ping 192.168.3.1` fails. `ipconfig` (address, mask, gateway), `ipconfig /all` (the *physical address* = MAC). `ping 192.168.1.254` to the gateway works.
2. **R1**: `show ip interface brief` is fine (up/up). `show ip route`: the route to 192.168.3.0/24 goes **via 192.168.12.3** instead of **192.168.12.2**. `show running-config | include ip route`, right-click to copy the line, `configure terminal`, paste, **Ctrl+A**, type `no ` in front, Enter: the route is removed (check with `do show running-config | include ip route`). Paste the line again changing the 3 to a 2. `do show ip route`: correct route.
3. **R2**: interfaces fine. `show ip route`: 192.168.1.0/24 via 192.168.12.1 is right, but 192.168.3.0/24 exits via **G0/0** instead of **G0/1**. Jeremy first adds the correct route (`ip route 192.168.3.0 255.255.255.0 g0/1`) without removing the wrong one: **both stay** in the table, the router would **load-balance** between G0/0 and G0/1. So remove the wrong one the same way (copy, `no `), then check only the G0/1 route remains.
4. **R3**: interfaces up/up but G0/0 has address **192.168.23.3** instead of **192.168.13.3**. `interface g0/0`, `ip address 192.168.13.3 255.255.255.0`: unlike routes, **the new address overwrites the old one** (compare `do show running-config` before and after). The static route to 1.0/24 via 192.168.13.2 is there.
5. **Verification**: `ping 192.168.3.1` from PC1; the first one or two may fail, then all succeed.

### Part 1 quiz (5 questions)

For some questions the answer choices are not read aloud in the transcript; only the correct answer and its explanation are.

| Question | Answer | Why |
| :--- | :--- | :--- |
| 1. The IP address configured on a router interface appears in the routing table as what kind of route? | **C, local** | Two routes are added when you configure an address and the interface is enabled: a connected route to the network and a **local** route to the exact address. If the interface is shut down, neither appears. |
| 2. From R1's routing table, what does it do with a packet for 192.168.3.25? | **B, it receives the packet for itself** | R1 has a local route 192.168.3.25/32: that address is configured on its G0/2. |
| 3. True statements about routers and switches (select two) | **B and C** | Switches flood frames with an unknown destination (*unknown unicast*); routers never flood, they drop packets with no route. |
| 4. Which two route types are automatically added when you configure an IP address on an interface and enable it? | **A, C and L** | C = connected, L = local, as shown in the `show ip route` output. |
| 5. From R1's routing table, how many routes match 10.0.1.23, and which is the most specific? | **C** | Two routes match: 10.0.1.0/24 and 10.0.1.23/32; the /32 is the most specific and will be selected. It is a local route: R1 keeps the packet. |

### Part 2 quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| 1. Which command configures a default route? A `ip route 0.0.0.0 0.0.0.0 10.1.1.255`; B and D with a /N prefix; C `ip route 0.0.0.0 255.255.255.255 …` | **A** | On Cisco you cannot write the prefix with a slash, you must write the netmask (B and D wrong). In a default route all mask bits are 0; C sets them all to 1. |
| 2. From R1's routing table, which interface for a packet to 8.8.8.8? | **C, GigabitEthernet0/2** | Only the default route matches; it gives next hop 203.0.113.2 with no interface. The route to 203.0.113.0/24 is connected to G0/2, so R1 sends out of G0/2. |
| 3. Complete the static-route table so PC1 and PC4 can communicate (path R1, R2, R4) | R1: 192.168.4.0/24 via **192.168.12.2**; R2: 192.168.1.0/24 via **192.168.12.1** and 192.168.4.0/24 via **192.168.24.4**; R4: 192.168.1.0/24 via **192.168.24.2** | Each router in the path needs a route to 1.0/24 and to 4.0/24; R1 and R4 already have a connected route to their LAN. |
| 4. Route "S 172.20.0.0/16 is directly connected, GigabitEthernet0/1" in R1's table: which command created it? | **D, `ip route 172.20.0.0 255.255.0.0 g0/1`** | "Directly connected" suggests a connected route (option B, `ip address`), but the code is **S**, and 172.20.0.0/16 is a network address, which cannot be configured on an interface. A static route with exit interface only displays this way; proxy ARP finds the next hop. |
| 5. How many static routes must be configured on R3 for it to know all destination networks in the diagram? | **D, four** | R3 knows its connected networks 192.168.13.0/24 and 192.168.34.0/24; it still needs 192.168.1.0/24, 4.0/24, 12.0/24 and 24.0/24. |
