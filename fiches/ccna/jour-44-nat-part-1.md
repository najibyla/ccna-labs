# CCNA Day 44 : NAT (Part 1) / Network Address Translation, adresses privées et NAT statique

> Source : Jeremy's IT Lab, « Free CCNA | NAT (Part 1) | Day 44 » (32 min, vidéo n°89 de la playlist, cours) et « Free CCNA | Static NAT | Day 44 Lab » (14 min, vidéo n°90, lab Packet Tracer). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Vue d'ensemble

- Sujet d'examen **4.1** : configurer et vérifier le **NAT source interne** (*inside source NAT*) **statique et par pools**. Sujet très important pour l'examen et le métier.
- **NAT** traduit l'adresse IP **source et/ou destination** d'un paquet en une autre adresse. NAT est réparti sur deux vidéos (Day 44 : adresses privées, introduction, NAT statique ; Day 45 : NAT dynamique et PAT).

### 2. Adresses IPv4 privées

- IPv4 ne fournit pas assez d'adresses. Solution à long terme : **IPv6**. Solutions à court terme qui ont prolongé la vie d'IPv4 : **CIDR** (*Classless Inter-Domain Routing*), les **adresses privées** et **NAT**.
- **RFC 1918** (RFC = *Request For Comments*, documents de standardisation d'Internet) définit trois plages privées :

| Plage | Adresses | Classe d'origine |
| :--- | :--- | :--- |
| **10.0.0.0/8** | 10.0.0.0 à 10.255.255.255 | A |
| **172.16.0.0/12** | 172.16.0.0 à 172.31.255.255 | B |
| **192.168.0.0/16** | 192.168.0.0 à 192.168.255.255 | C |

- Ce sont de simples **plages** : /12 et /16 ne sont pas des masques de classe, on découpe ces adresses comme on veut (CIDR ; les classes appartiennent au passé).
- Les adresses privées **n'ont pas besoin d'être uniques mondialement** ; votre PC a presque certainement une adresse privée (ex. 192.168.0.167, passerelle 192.168.0.1).
- **Les adresses privées ne peuvent pas être utilisées sur Internet : le FAI (ISP) jette le trafic** vers ou depuis ces adresses.
- Sans NAT, deux problèmes : **adresses dupliquées** (deux PC 192.168.0.167 dans deux foyers : à qui livrer le paquet ?) et **impossibilité d'accéder à Internet**. NAT résout les deux : les adresses **publiques** des routeurs (ex. 203.0.113.1 et 203.0.113.5) **doivent être uniques** ; le PC « emprunte » l'adresse publique du routeur (ou une autre adresse publique configurée pour NAT), et tous les appareils du foyer peuvent partager la même adresse publique en même temps.
- À retenir : **RFC 1918**, les **trois plages**, **inutilisables sur Internet**.

### 3. NAT et NAT source

- NAT modifie les adresses source et/ou destination. Raison la plus courante : permettre aux hôtes en adresses privées de communiquer sur Internet (et partager une seule adresse publique, Day 45). Pour le CCNA : **NAT source** (*source NAT*).
- Exemple : PC1 (192.168.0.167) → 8.8.8.8. R1 (passerelle) **traduit l'adresse source** en 203.0.113.1 (son interface externe), d'où « source NAT ». La réponse de 8.8.8.8 arrive à destination 203.0.113.1 ; R1 **inverse la traduction** vers 192.168.0.167. Même si l'adresse de destination est modifiée au retour, **ce n'est pas du NAT destination** : R1 ne fait que rétablir l'adresse réelle.
- Utiliser l'adresse de l'interface du routeur n'est qu'une option (Day 45). Le **NAT statique** utilise une **adresse séparée**.

### 4. NAT statique

- **Correspondances un-à-un** (*one-to-one*) configurées statiquement, en pratique une adresse **privée** vers une adresse **publique** (on peut en fait traduire n'importe quelle adresse en n'importe quelle autre).
- Terminologie fondamentale, valable pour tous les types de NAT :
  - **Inside** / **outside** : **emplacement** de l'hôte, réseau interne du routeur ou réseau extérieur (Internet).
  - **Local** / **global** : **point de vue**, celui du réseau local interne ou celui du réseau extérieur.
  - **Inside local** : adresse de l'hôte interne **vue du réseau local** = adresse réellement configurée sur l'hôte, en général **privée** (192.168.0.167).
  - **Inside global** : adresse de l'hôte interne **vue des hôtes extérieurs** = adresse **après NAT**, en général **publique** (100.0.0.1). Pour le serveur, il communique avec 100.0.0.1.
  - **Outside local** : adresse de l'hôte extérieur vue du réseau local (8.8.8.8 du point de vue de PC1).
  - **Outside global** : adresse de l'hôte extérieur vue du réseau extérieur, son adresse réelle (8.8.8.8). **Outside local et outside global sont toujours identiques sauf NAT destination**, hors programme CCNA.
- PC2 (192.168.0.168) a besoin de **sa propre** adresse publique (100.0.0.2) : le routeur **refuse** de mapper deux adresses internes vers la même adresse publique en NAT statique.
- Limite : un-à-un, donc **n'économise pas les adresses publiques** ; si chaque hôte a besoin de sa propre adresse publique, autant la configurer directement. Utile dans certains cas, mais pas le type le plus utile ici.

### 5. Configuration du NAT statique

1. **Interfaces** : `ip nat inside` sur l'interface interne (G0/1), `ip nat outside` sur l'interface externe (G0/0). NAT s'applique au trafic allant de l'interface inside vers l'interface outside.
2. **Mappages** : `ip nat inside source static <inside-local> <inside-global>`, ex. `ip nat inside source static 192.168.0.167 100.0.0.1` et `... 192.168.0.168 100.0.0.2`. Les adresses publiques doivent **vous appartenir** (enregistrées à votre nom ou votre entreprise), contrairement aux adresses privées.
3. **`show ip nat translations`** : les entrées statiques apparaissent **en permanence** ; colonnes **Inside global** puis **Inside local** (dans cet ordre), puis **Outside local**, **Outside global**. Quand une traduction est réellement utilisée, des **entrées dynamiques** s'ajoutent : colonne **Pro** (protocole, ex. UDP), adresse**:port**. En NAT statique, **les ports ne sont pas traduits** (importance des ports au Day 45 avec PAT). Exemple : port 53 = DNS (UDP 53, parfois TCP 53).
4. **`clear ip nat translation *`** : supprime les entrées **dynamiques** (qui expirent sinon d'elles-mêmes) ; les entrées **statiques restent** et ne disparaissent qu'en retirant les commandes `ip nat inside source static`.
5. **`show ip nat statistics`** : « Total active translations » (ex. 2, static 2, dynamic 0, extended 0 : *extended* expliqué au Day 45), « Peak translations » (maximum atteint, ex. 4), interfaces outside (g0/0) et inside (g0/1).

### 6. Pièges d'examen

- **RFC 1918** : 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16. Vérifier qu'une adresse tombe dans la plage (172.20.2.3 oui, 172.32.x.x non).
- `ip nat inside source static <local> <global>` : **inside local d'abord** (privée), **inside global ensuite** (publique). Dans `show ip nat translations`, l'ordre des colonnes est inversé.
- Deux adresses internes vers la **même** adresse globale en statique : **seconde commande rejetée**.
- `clear ip nat translation *` ne supprime **que** les dynamiques : les N statiques restent.
- Outside local = outside global (sans NAT destination).
- Question Boson : « l'adresse IP de HostA » = l'adresse **réellement configurée** = **inside local**, pas l'inside global ; identifier la bonne entrée par le protocole et le port (TFTP = UDP 69, Telnet = TCP 23).

### 7. Commandes IOS

```text
R1(config-if)# ip nat inside                      ! interface interne (G0/1)
R1(config-if)# ip nat outside                     ! interface externe (G0/0)
R1(config)# ip nat inside source static 192.168.0.167 100.0.0.1 ! mappage un-à-un inside local -> inside global
R1# show ip nat translations                      ! table : Pro, Inside global, Inside local, Outside local, Outside global
R1# clear ip nat translation *                    ! efface les entrées dynamiques (statiques conservées)
R1# show ip nat statistics                        ! totaux static/dynamic/extended, peak, interfaces inside/outside
```

### 8. Le lab (vidéo n°90)

Objectif : NAT statique sur R1 pour PC1, PC2, PC3 (172.16.0.1 à .3, adresses privées) vers 100.0.0.1 à .3, afin d'atteindre 8.8.8.8 (serveur DNS) et google.com.

1. `ping 8.8.8.8` depuis PC1 : **les quatre pings échouent** (le FAI jette le trafic en adresse privée).
2. R1 : `interface g0/0` (vers Internet) `ip nat outside` ; `interface g0/1` (réseau interne) `ip nat inside`. Puis `ip nat inside source static 172.16.0.1 100.0.0.1`, `172.16.0.2 100.0.0.2`, `172.16.0.3 100.0.0.3` (même partie hôte pour simplifier).
3. `show ip nat translations` : trois mappages statiques ; `show ip nat statistics` : 3 traductions, interfaces inside/outside.
4. `ping 8.8.8.8` depuis PC1 : réussit. `ping google.com` depuis PC1, PC2, PC3 (DNS = 8.8.8.8) : réussit. `show ip nat translations` : entrées statiques, **trois entrées UDP vers 8.8.8.8:53** (requêtes DNS) et des entrées pour les pings ; inside local traduit en inside global, **outside local = outside global** (NAT source seulement).
5. `clear ip nat translation *` puis `show ip nat translations` : seules les statiques restent.

Bonus Boson NetSim « Static NAT 1 » : ping PC1 → Router3 (routeur « Internet », 180.10.1.1) échoue ; sur Router4 `ip nat inside source static 192.168.1.2 180.10.1.15`, `interface fastethernet0/1` `ip nat inside`, `interface serial0/0` `ip nat outside` ; le ping réussit ; `do show ip nat translation` (inside global = adresse normalement **publique**) ; `ip nat inside source static 192.168.1.3 180.10.1.16` pour PC3 ; ping Router3 → PC1 (192.168.1.2) : **U, unreachable** (adresse privée) ; ping Switch2 → Router3 échoue (pas de NAT pour l'adresse de Switch2).

### 9. Le quiz (5 questions + 1 Boson)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quelle commande configure un mappage NAT source statique de 192.168.10.10 vers 203.0.113.10 ? | **`ip nat inside source static 192.168.10.10 203.0.113.10`** (D) | Inside local (privée) puis inside global (publique). |
| Après `ip nat inside source static 10.0.0.1 20.0.0.1`, que se passe-t-il avec `ip nat inside source static 10.0.0.2 20.0.0.1` ? | **Seule 10.0.0.1 est traduite en 20.0.0.1** (B) | La seconde commande est rejetée : une adresse publique déjà mappée ne peut pas l'être à une autre adresse privée ; il faut une autre adresse publique pour 10.0.0.2. |
| D'après la sortie `show`, combien de traductions actives après `clear ip nat translation *` ? | **3** (B) | La commande n'efface que les dynamiques ; les 3 statiques restent. |
| Quelles adresses sont privées ? (toutes celles qui s'appliquent) | **10.254.255.0** (A), **172.20.2.3** (E), **10.11.12.13** (F) | Seules adresses dans les plages RFC 1918 : 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16. |
| PC1 pinge 8.8.8.8 : identifier outside global, outside local, inside local, inside global du point de vue de R1 | **Outside global = outside local = 8.8.8.8 ; inside local = 172.20.0.101 ; inside global = 200.0.0.1** | Outside local et global ne diffèrent qu'avec le NAT destination (hors CCNA) ; inside local = adresse de PC1 vue du réseau interne, inside global = adresse de PC1 vue de l'extérieur. |
| Boson : HostA établit une connexion TFTP avec HostB via RouterA ; d'après `show ip nat translations`, quelle est l'adresse IP de HostA ? | **10.20.30.55** | L'entrée TFTP est celle en **UDP** port **69** (pas TCP 23) ; « l'adresse de HostA » = adresse réelle = **inside local**, pas l'inside global. |

---

## 🇬🇧 English version

### 1. Overview

- Exam topic **4.1**: configure and verify **inside source NAT** using **static and pools**. Very important for the exam and real-world engineering.
- **NAT** translates the **source and/or destination** IP address of a packet to a different address. NAT is split over two videos (Day 44: private addresses, introduction, static NAT; Day 45: dynamic NAT and PAT).

### 2. Private IPv4 addresses

- IPv4 doesn't provide enough addresses. Long-term solution: **IPv6**. Short-term solutions that extended IPv4's lifespan: **CIDR** (Classless Inter-Domain Routing), **private addresses** and **NAT**.
- **RFC 1918** (RFC = Request For Comments, Internet standards documents) specifies three private ranges:

| Range | Addresses | Original class |
| :--- | :--- | :--- |
| **10.0.0.0/8** | 10.0.0.0 to 10.255.255.255 | A |
| **172.16.0.0/12** | 172.16.0.0 to 172.31.255.255 | B |
| **192.168.0.0/16** | 192.168.0.0 to 192.168.255.255 | C |

- These are simply **ranges**: /12 and /16 are not class masks, you divide these addresses however you want (CIDR; classes are a thing of the past).
- Private addresses **don't have to be globally unique**; your PC almost certainly uses one (e.g. 192.168.0.167, gateway 192.168.0.1).
- **Private addresses cannot be used over the Internet: the ISP drops traffic** to or from them.
- Without NAT, two problems: **duplicate addresses** (two PCs 192.168.0.167 in two homes: which one gets the packet?) and **no Internet access**. NAT solves both: the routers' **public** addresses (e.g. 203.0.113.1 and 203.0.113.5) **must be unique**; the PC "borrows" the router's public address (or another public address configured for NAT), and all devices in the home can share that single public address at the same time.
- Remember: **RFC 1918**, the **three ranges**, **not usable over the Internet**.

### 3. NAT and source NAT

- NAT modifies source and/or destination addresses. Most common reason: let hosts with private addresses communicate over the Internet (and share a single public address, Day 45). For the CCNA: **source NAT**.
- Example: PC1 (192.168.0.167) → 8.8.8.8. R1 (default gateway) **translates the source address** to 203.0.113.1 (its external interface), hence "source NAT". The reply from 8.8.8.8 arrives with destination 203.0.113.1; R1 **reverses the translation** to 192.168.0.167. Although the destination address changes on the way back, **this is not destination NAT**: R1 is just reverting to the real address.
- Using the router's interface address is only one option (Day 45). **Static NAT** uses a **separate address**.

### 4. Static NAT

- Statically configured **one-to-one mappings**, in practice a **private** address to a **public** address (any address can actually be translated to any other).
- Fundamental terminology, valid for all NAT types:
  - **Inside** / **outside**: the host's **location**, the router's internal network or outside networks (Internet).
  - **Local** / **global**: the **perspective**, that of the local inside network or that of the outside network.
  - **Inside local**: the inside host's address **from the local network's perspective** = the address actually configured on the host, usually **private** (192.168.0.167).
  - **Inside global**: the inside host's address **from outside hosts' perspective** = the address **after NAT**, usually **public** (100.0.0.1). From the server's perspective it is talking to 100.0.0.1.
  - **Outside local**: the outside host's address from the local network's perspective (8.8.8.8 from PC1's view).
  - **Outside global**: the outside host's address from the outside network's perspective, its real address (8.8.8.8). **Outside local and outside global are always the same unless destination NAT is used**, which is beyond the CCNA.
- PC2 (192.168.0.168) needs **its own** public address (100.0.0.2): the router **won't allow** mapping two inside addresses to the same public address with static NAT.
- Limitation: one-to-one, so it **doesn't really preserve public addresses**; if every host needs its own public address anyway, you might as well configure it on the device. There are reasons to use static NAT, but it's not the most useful type here.

### 5. Static NAT configuration

1. **Interfaces**: `ip nat inside` on the inside interface (G0/1), `ip nat outside` on the outside interface (G0/0). NAT applies to traffic from the inside interface to the outside interface.
2. **Mappings**: `ip nat inside source static <inside-local> <inside-global>`, e.g. `ip nat inside source static 192.168.0.167 100.0.0.1` and `... 192.168.0.168 100.0.0.2`. Public addresses must be **owned by you** (registered to you or your company), unlike private addresses.
3. **`show ip nat translations`**: static entries are **permanently displayed**; columns **Inside global** then **Inside local** (in that order), then **Outside local**, **Outside global**. When a translation is actually used, **dynamic entries** are added: **Pro** column (protocol, e.g. UDP), address**:port**. With static NAT, **port numbers are not translated** (ports matter in Day 45 with PAT). Example: port 53 = DNS (UDP 53, sometimes TCP 53).
4. **`clear ip nat translation *`**: removes **dynamic** entries (which otherwise time out); **static entries remain** and only go away when the `ip nat inside source static` commands are removed.
5. **`show ip nat statistics`**: "Total active translations" (e.g. 2, static 2, dynamic 0, extended 0: *extended* explained in Day 45), "Peak translations" (highest number reached, e.g. 4), outside (g0/0) and inside (g0/1) interfaces.

### 6. Exam traps

- **RFC 1918**: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16. Check whether an address falls in the range (172.20.2.3 yes, 172.32.x.x no).
- `ip nat inside source static <local> <global>`: **inside local first** (private), **inside global second** (public). In `show ip nat translations`, the column order is reversed.
- Two inside addresses to the **same** global address with static NAT: **second command rejected**.
- `clear ip nat translation *` only removes dynamic entries: the N static ones remain.
- Outside local = outside global (without destination NAT).
- Boson question: "the IP address of HostA" = the address **actually configured** = **inside local**, not inside global; find the right entry by protocol and port (TFTP = UDP 69, Telnet = TCP 23).

### 7. IOS commands

```text
R1(config-if)# ip nat inside                      ! inside interface (G0/1)
R1(config-if)# ip nat outside                     ! outside interface (G0/0)
R1(config)# ip nat inside source static 192.168.0.167 100.0.0.1 ! one-to-one mapping inside local -> inside global
R1# show ip nat translations                      ! table: Pro, Inside global, Inside local, Outside local, Outside global
R1# clear ip nat translation *                    ! clear dynamic entries (static ones kept)
R1# show ip nat statistics                        ! static/dynamic/extended totals, peak, inside/outside interfaces
```

### 8. The lab (video #90)

Goal: static NAT on R1 for PC1, PC2, PC3 (172.16.0.1 to .3, private addresses) to 100.0.0.1 to .3, to reach 8.8.8.8 (DNS server) and google.com.

1. `ping 8.8.8.8` from PC1: **all four pings fail** (the ISP drops private-address traffic).
2. R1: `interface g0/0` (to the Internet) `ip nat outside`; `interface g0/1` (internal network) `ip nat inside`. Then `ip nat inside source static 172.16.0.1 100.0.0.1`, `172.16.0.2 100.0.0.2`, `172.16.0.3 100.0.0.3` (same host portion for simplicity).
3. `show ip nat translations`: three static mappings; `show ip nat statistics`: 3 translations, inside/outside interfaces.
4. `ping 8.8.8.8` from PC1: works. `ping google.com` from PC1, PC2, PC3 (DNS = 8.8.8.8): works. `show ip nat translations`: static entries, **three UDP entries to 8.8.8.8:53** (DNS queries) and entries for the pings; inside local translated to inside global, **outside local = outside global** (source NAT only).
5. `clear ip nat translation *` then `show ip nat translations`: only the static entries remain.

Boson NetSim bonus "Static NAT 1": ping PC1 → Router3 ("Internet" router, 180.10.1.1) fails; on Router4 `ip nat inside source static 192.168.1.2 180.10.1.15`, `interface fastethernet0/1` `ip nat inside`, `interface serial0/0` `ip nat outside`; the ping works; `do show ip nat translation` (inside global normally a **public** address); `ip nat inside source static 192.168.1.3 180.10.1.16` for PC3; ping Router3 → PC1 (192.168.1.2): **U, unreachable** (private address); ping Switch2 → Router3 fails (no NAT for Switch2's address).

### 9. The quiz (5 questions + 1 Boson)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which command configures a static source NAT mapping of 192.168.10.10 to 203.0.113.10? | **`ip nat inside source static 192.168.10.10 203.0.113.10`** (D) | Inside local (private) then inside global (public). |
| After `ip nat inside source static 10.0.0.1 20.0.0.1`, what happens with `ip nat inside source static 10.0.0.2 20.0.0.1`? | **Only 10.0.0.1 is translated to 20.0.0.1** (B) | The second command is rejected: a public address already mapped can't be mapped to another private address; 10.0.0.2 needs a different public address. |
| Given the `show` output, how many active translations after `clear ip nat translation *`? | **3** (B) | The command only clears dynamic translations; the 3 static ones remain. |
| Which addresses are private? (select all that apply) | **10.254.255.0** (A), **172.20.2.3** (E), **10.11.12.13** (F) | The only addresses within the RFC 1918 ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16. |
| PC1 pings 8.8.8.8: identify outside global, outside local, inside local, inside global from R1's perspective | **Outside global = outside local = 8.8.8.8; inside local = 172.20.0.101; inside global = 200.0.0.1** | Outside local and global only differ with destination NAT (beyond the CCNA); inside local = PC1's address from the inside network's view, inside global = PC1's address from the outside's view. |
| Boson: HostA establishes a TFTP connection with HostB through RouterA; from `show ip nat translations`, what is HostA's IP address? | **10.20.30.55** | The TFTP entry is the **UDP** port **69** one (not TCP 23); "HostA's address" = the real address = **inside local**, not inside global. |
