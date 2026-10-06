# CCNA Day 45 : NAT (Part 2) / NAT dynamique et PAT

> Source : Jeremy's IT Lab, « Free CCNA | NAT (part 2) | Day 45 » (30 min, vidéo n°91 de la playlist, cours) et « Free CCNA | Dynamic NAT | Day 45 Lab » (15 min, vidéo n°92, lab Packet Tracer). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Complément sur le NAT statique

- Sujet d'examen **4.1**. Rappel : mappages un-à-un configurés statiquement (inside local 192.168.0.167 → inside global 100.0.0.1, 192.168.0.168 → 100.0.0.2) ; R1 traduit la source à l'aller, la destination au retour.
- Point non dit au Day 44 : le mappage un-à-un fonctionne **dans les deux sens**. Un hôte extérieur peut **initier** une communication vers l'adresse **inside global** (100.0.0.1) sans que PC1 ait commencé : R1 traduit en 192.168.0.167 et transmet à PC1, qui répond. Pas seulement inside → outside, mais aussi **outside → inside**.

### 2. NAT dynamique

- Le routeur **mappe automatiquement** les adresses inside local vers des adresses inside global **à la demande**, puis supprime le mappage quand il n'est plus nécessaire.
- Une **ACL identifie le trafic à traduire** : usage différent et très courant des ACL. Source **permise** par l'ACL → **traduite** ; source **refusée** → **non traduite, mais PAS jetée**. On n'applique pas l'ACL à une interface avec `ip access-group` : elle sert seulement à identifier le trafic.
- Un **pool NAT** définit les adresses inside global disponibles. Exemple : ACL 1 permet 192.168.0.0/24 ; POOL1 = 100.0.0.1 à 100.0.0.10 ; PC1 envoie un paquet, permis par l'ACL 1, R1 traduit la source en 100.0.0.1 (adresse du pool). Même résultat qu'en statique, mais le mappage est créé **automatiquement** à l'arrivée du paquet.
- Les mappages restent **un-à-un** : une inside local par inside global. Avec un /24 d'adresses internes et seulement 10 adresses dans le pool, **10 traductions actives au maximum**.
- **Épuisement du pool** (*NAT pool exhaustion*) : si toutes les adresses sont utilisées et qu'un nouvel hôte interne a besoin de NAT, **le routeur jette le paquet** ; l'hôte attend qu'une adresse se libère. Les entrées dynamiques **expirent** si elles ne sont pas utilisées, ou se suppriment avec `clear ip nat translation *`. Exemple : les dix adresses 100.0.0.1 à .10 sont prises, 192.168.0.98 est rejeté ; quand 192.168.0.167 cesse de communiquer, son mappage expire et 100.0.0.1 redevient disponible.
- Différence statique/dynamique : les deux sont un-à-un, mais les mappages statiques sont **permanents**, les dynamiques **temporaires**. Des hôtes ne peuvent toujours pas utiliser **la même adresse publique en même temps** : il faut **PAT**.

### 3. Configuration du NAT dynamique

1. Interfaces : `ip nat inside` / `ip nat outside`.
2. Trafic à traduire : `access-list 1 permit 192.168.0.0 0.0.0.255`.
3. Pool : `ip nat pool POOL1 100.0.0.0 100.0.0.255 prefix-length 24` (ou `netmask 255.255.255.0`) : nom, **première** et **dernière** adresse de la plage, puis **prefix-length ou netmask** obligatoire ; IOS vérifie que les deux adresses sont **dans le même sous-réseau**, sinon la commande est **rejetée**.
4. Mappage ACL → pool : `ip nat inside source list 1 pool POOL1` (**`list`** à la place de `static`).
- `show ip nat translations` après pings et DNS de PC1 et PC2 : **trois entrées par mappage** : l'entrée de mappage inside local → inside global (créée dynamiquement) plus les entrées de traduction UDP et ICMP. Les entrées UDP/ICMP s'effacent après **environ une minute** ; les mappages dynamiques ont un **timeout par défaut de 24 heures**, réinitialisé à chaque traduction (timers modifiables, hors CCNA). Bien qu'ils ressemblent aux entrées statiques, **`clear ip nat translation *` les efface** : ils sont dynamiques.
- `show ip nat statistics` : 6 traductions actives, 6 dynamiques, **4 extended** (les entrées temporaires UDP et ICMP ; détail hors CCNA) ; confirme le mappage **ACL 1 → POOL1**. Deux `show` à connaître : `show ip nat translations` et `show ip nat statistics`.

### 4. PAT (Port Address Translation), alias NAT overload

- Traduit **l'adresse IP et, si nécessaire, le numéro de port**. En utilisant un **port unique par flux**, **une seule adresse publique** sert à de nombreux hôtes internes. Ports TCP/UDP sur **16 bits** : plus de **65 000** ports. Le routeur suit quel inside local utilise quel couple inside global:port.
- Exemple : PC1 (192.168.0.167, port source 54321) et PC2 (192.168.0.168, **même** port 54321 par hasard) envoient du DNS à 8.8.8.8. R1 traduit PC1 en 100.0.0.1:54321 et PC2 en 100.0.0.1:**54322** : sans ports distincts il ne saurait pas à qui renvoyer les réponses. Si PC2 avait choisi un port différent, **aucune traduction de port** ne serait nécessaire.
- PAT est **le type le plus utilisé** : économise les adresses publiques, employé dans le monde entier (le routeur domestique de Jeremy a une seule adresse publique pour tous ses appareils).
- **Configuration avec pool** : identique au NAT dynamique plus le mot-clé **`overload`** : `ip nat inside source list 1 pool POOL1 overload`. Pool plus petit (100.0.0.0 à 100.0.0.3, `prefix-length 24` : la longueur importe peu tant que la plage est dans le même sous-réseau) ; une seule adresse suffit souvent, le pool donne de la marge. `show ip nat translations` : **pas d'entrées de mappage un-à-un** (c'est du **plusieurs-vers-un**), .167 et .168 utilisent tous deux 100.0.0.1 avec leurs ports source différents (63925, 59549), non traduits.
- **Configuration avec l'interface** (probablement la plus courante) : `ip nat inside source list 1 interface g0/0 overload` : traduit vers l'adresse de l'**interface outside** (203.0.113.1), un port unique par flux. Exemple : ports 65205 (PC1) et 59641 (PC2), déjà différents, non traduits ; la table montre les deux inside local vers 203.0.113.1.

### 5. Pièges d'examen

- **ACL de NAT** : permit = traduit, deny = **non traduit mais pas jeté**.
- **Pool épuisé** : le paquet est **jeté** (*discarded*).
- `ip nat pool` : première et dernière adresse **dans le même sous-réseau** que le `netmask`/`prefix-length` (203.0.113.0 à 203.0.113.255 avec masque /25 → rejeté) ; dans l'ACL, **masque générique** (0.0.0.255 pour /24, 0.0.0.31 pour /27), pas un masque de sous-réseau.
- PAT vers l'interface : traduire vers l'adresse de l'**interface externe** (publique), jamais l'interface interne (question Boson). Inside local = adresse réelle de l'hôte source, pas celle de l'interface interne du routeur.
- **PAT / NAT overload** = le type qui **préserve le mieux les adresses publiques**.
- Statique = permanent et bidirectionnel ; dynamique = temporaire, 24 h par défaut ; PAT = plusieurs-vers-un.
- Une nouvelle commande `ip nat inside source list 1 ...` **remplace** la précédente dans la running-config (lab).

### 6. Commandes IOS

```text
R1(config-if)# ip nat inside / ip nat outside                   ! interfaces, comme en statique
R1(config)# access-list 1 permit 192.168.0.0 0.0.0.255          ! trafic à traduire (masque générique)
R1(config)# ip nat pool POOL1 100.0.0.0 100.0.0.255 prefix-length 24 ! pool : première, dernière adresse, prefix-length ou netmask
R1(config)# ip nat inside source list 1 pool POOL1              ! NAT dynamique : ACL -> pool
R1(config)# ip nat inside source list 1 pool POOL1 overload     ! PAT avec pool
R1(config)# ip nat inside source list 1 interface g0/0 overload ! PAT avec l'adresse de l'interface outside
R1# show ip nat translations                                    ! mappages dynamiques + entrées UDP/ICMP (ports)
R1# show ip nat statistics                                      ! dynamic, extended, ACL -> pool
R1# clear ip nat translation *                                  ! efface aussi les mappages dynamiques
R1# show run | include nat                                      ! vérifier les commandes NAT
```

### 7. Le lab (vidéo n°92)

Même topologie que le lab statique (PC1-PC3 en 172.16.0.0/24, R1 G0/0 vers Internet 203.0.113.1, G0/1 interne).

1. **NAT dynamique** : `interface g0/0` `ip nat outside`, `interface g0/1` `ip nat inside` ; `access-list 1 permit 172.16.0.0 0.0.0.255` ; pool à **deux adresses** : `ip nat pool POOL1 100.0.0.1 100.0.0.2 netmask 255.255.255.0` (sous-réseau 100.0.0.0/24) ; `ip nat inside source list 1 pool POOL1`.
2. Tests : `ping 8.8.8.8` puis `ping google.com` depuis PC1 (OK), PC2 (OK), **PC3 : aucune réponse** : les deux adresses du pool sont prises par PC1 et PC2 (**épuisement du pool**). `do show ip nat translations` : 172.16.0.1 → 100.0.0.1, 172.16.0.2 → 100.0.0.2, entrées ICMP et UDP ; dans Packet Tracer, les entrées de mappage simples du cours **n'apparaissent pas** (différence avec l'IOS réel ; à l'examen on interprète une table, on ne prédit pas ses entrées).
3. **Passage à PAT sur l'interface** : `do clear ip nat translation *` ; `do show run | include nat` ; sans supprimer l'ancienne commande, `ip nat inside source list 1 interface g0/0 overload` : la commande précédente est **remplacée** dans la running-config (le pool reste, à supprimer si on veut).
4. `ping google.com` depuis PC1, PC2 et **PC3 : réussit cette fois**. `do show ip nat translations` : 172.16.0.1, .2 et .3 traduits vers **203.0.113.1** ; R1 distingue les flux par **protocole et ports**.

Note : la vidéo annonce un lab bonus Boson NetSim, mais la transcription passe directement aux remerciements ; aucune information sur ce lab.

### 8. Le quiz (5 questions + 1 Boson)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quel type de NAT préserve le mieux les adresses IPv4 publiques ? | **NAT Overload (PAT)** (D) | De nombreux hôtes partagent une seule adresse publique, le routeur suivant les flux par le port de couche 4 ; la plupart des réseaux n'ont besoin que d'une adresse publique. |
| Quelle configuration NAT dynamique traduit 172.16.1.0/24 vers des adresses de 203.0.113.0/25 ? | **B** | A : netmask 255.255.255.128 correct mais plage 203.0.113.0 à .255, et .255 n'est pas dans /25 → rejeté. C : l'ACL utilise 255.255.255.0 au lieu du masque générique 0.0.0.255. |
| Pool de 10 adresses toutes utilisées, un autre hôte interne envoie un paquet vers Internet : que fait R1 ? | **Il jette le paquet** (B) | Sans adresse disponible dans le pool, le routeur supprime le paquet. |
| Quelle configuration traduit 10.0.1.0/27 vers l'adresse de l'interface G0/1 du routeur ? | **A** | Seule option avec le bon masque générique /27 dans l'ACL, la bonne commande `ip nat` et les interfaces inside/outside correctement assignées. |
| Après les interfaces, ACL qui **refuse** 192.168.1.0/24 : que deviennent les paquets de ces hôtes ? | **Ils ne sont pas traduits par R1** (C) | Permis = traduit, refusé = non traduit ; le refus par l'ACL ne signifie pas que le routeur jette les paquets. |
| Boson : HostA (10.1.7.7) ouvre une connexion HTTP vers HostB (192.0.2.28) via RouterA (interne 10.1.7.1, externe 203.0.113.62) ; quelle ligne de `show ip nat translations` ? | **C** : inside global 203.0.113.62, inside local 10.1.7.7, outside local = outside global 192.0.2.28 | Inside local = adresse réelle de HostA (pas 10.1.7.1, interface interne du routeur) ; en PAT vers l'interface, l'inside global est l'adresse de l'**interface externe**, publique. |

---

## 🇬🇧 English version

### 1. One more point about static NAT

- Exam topic **4.1**. Review: statically configured one-to-one mappings (inside local 192.168.0.167 → inside global 100.0.0.1, 192.168.0.168 → 100.0.0.2); R1 translates the source outbound, the destination on the reply.
- Not mentioned in Day 44: the one-to-one mapping works **both ways**. An external host can **initiate** communication to the **inside global** address (100.0.0.1) without PC1 starting it: R1 translates it to 192.168.0.167 and forwards it to PC1, which replies. Not just inside → outside, but also **outside → inside**.

### 2. Dynamic NAT

- The router **dynamically maps** inside local addresses to inside global addresses **as needed**, then clears the mapping when no longer needed.
- An **ACL identifies which traffic should be translated**: a different, very common use of ACLs. Source **permitted** by the ACL → **translated**; source **denied** → **not translated, but NOT dropped**. The ACL is not applied to an interface with `ip access-group`: it only identifies traffic.
- A **NAT pool** defines the available inside global addresses. Example: ACL 1 permits 192.168.0.0/24; POOL1 = 100.0.0.1 to 100.0.0.10; PC1 sends a packet, permitted by ACL 1, R1 translates the source to 100.0.0.1 (from the pool). Same result as static NAT, but the mapping is created **automatically** when the packet arrives.
- Mappings are still **one-to-one**: one inside local per inside global. With a /24 of inside addresses and only 10 pool addresses, **10 active translations at most**.
- **NAT pool exhaustion**: if all addresses are in use and another inside host needs NAT, **the router drops the packet**; the host waits until an address frees up. Dynamic entries **time out** if unused, or are cleared with `clear ip nat translation *`. Example: all ten addresses 100.0.0.1 to .10 are used, 192.168.0.98 is dropped; when 192.168.0.167 stops communicating, its mapping times out and 100.0.0.1 becomes available again.
- Static vs dynamic: both one-to-one, but static mappings are **permanent**, dynamic ones **temporary**. Hosts still can't use **the same public address at the same time**: that requires **PAT**.

### 3. Dynamic NAT configuration

1. Interfaces: `ip nat inside` / `ip nat outside`.
2. Traffic to translate: `access-list 1 permit 192.168.0.0 0.0.0.255`.
3. Pool: `ip nat pool POOL1 100.0.0.0 100.0.0.255 prefix-length 24` (or `netmask 255.255.255.0`): name, **first** and **last** address of the range, then a mandatory **prefix-length or netmask**; IOS checks that both addresses are **in the same subnet**, otherwise the command is **rejected**.
4. Map ACL → pool: `ip nat inside source list 1 pool POOL1` (**`list`** instead of `static`).
- `show ip nat translations` after pings and DNS from PC1 and PC2: **three entries per mapping**: the dynamically created inside local → inside global mapping entry plus the UDP and ICMP translation entries. UDP/ICMP entries clear after **about a minute**; the dynamic mappings have a **default timeout of 24 hours**, reset at each translation (timers can be changed, beyond the CCNA). Although they look like static entries, **`clear ip nat translation *` clears them**: they are dynamic.
- `show ip nat statistics`: 6 active translations, 6 dynamic, **4 extended** (the temporary UDP and ICMP entries; details beyond the CCNA); confirms the mapping **ACL 1 → POOL1**. Two `show` commands to know: `show ip nat translations` and `show ip nat statistics`.

### 4. PAT (Port Address Translation), aka NAT overload

- Translates **the IP address and, if necessary, the port number**. By using a **unique port per flow**, **a single public address** serves many inside hosts. TCP/UDP ports are **16 bits**: over **65,000** ports. The router tracks which inside local uses which inside global:port pair.
- Example: PC1 (192.168.0.167, source port 54321) and PC2 (192.168.0.168, **same** port 54321 by chance) send DNS to 8.8.8.8. R1 translates PC1 to 100.0.0.1:54321 and PC2 to 100.0.0.1:**54322**: without distinct ports it wouldn't know where to send the replies. If PC2 had picked a different port, **no port translation** would be needed.
- PAT is **the most widely used** type: preserves public addresses, used worldwide (Jeremy's home router has a single public address for all its devices).
- **Pool configuration**: same as dynamic NAT plus the **`overload`** keyword: `ip nat inside source list 1 pool POOL1 overload`. Smaller pool (100.0.0.0 to 100.0.0.3, `prefix-length 24`: the length doesn't really matter as long as the range is in the same subnet); one address is often enough, the pool gives room for growth. `show ip nat translations`: **no one-to-one mapping entries** (it's **many-to-one**), .167 and .168 both use 100.0.0.1 with their different source ports (63925, 59549), not translated.
- **Interface configuration** (probably the more common way): `ip nat inside source list 1 interface g0/0 overload`: translates to the **outside interface's** address (203.0.113.1), a unique port per flow. Example: ports 65205 (PC1) and 59641 (PC2), already different, not translated; the table shows both inside locals to 203.0.113.1.

### 5. Exam traps

- **NAT ACL**: permit = translated, deny = **not translated but not dropped**.
- **Pool exhausted**: the packet is **discarded**.
- `ip nat pool`: first and last address **in the same subnet** as the `netmask`/`prefix-length` (203.0.113.0 to 203.0.113.255 with a /25 mask → rejected); in the ACL, a **wildcard mask** (0.0.0.255 for /24, 0.0.0.31 for /27), not a subnet mask.
- PAT to the interface: translate to the **external interface's** (public) address, never the internal one (Boson question). Inside local = the source host's real address, not the router's internal interface.
- **PAT / NAT overload** = the type that **best preserves public addresses**.
- Static = permanent and two-way; dynamic = temporary, 24 h by default; PAT = many-to-one.
- A new `ip nat inside source list 1 ...` command **replaces** the previous one in the running-config (lab).

### 6. IOS commands

```text
R1(config-if)# ip nat inside / ip nat outside                   ! interfaces, as with static NAT
R1(config)# access-list 1 permit 192.168.0.0 0.0.0.255          ! traffic to translate (wildcard mask)
R1(config)# ip nat pool POOL1 100.0.0.0 100.0.0.255 prefix-length 24 ! pool: first, last address, prefix-length or netmask
R1(config)# ip nat inside source list 1 pool POOL1              ! dynamic NAT: ACL -> pool
R1(config)# ip nat inside source list 1 pool POOL1 overload     ! PAT with a pool
R1(config)# ip nat inside source list 1 interface g0/0 overload ! PAT with the outside interface's address
R1# show ip nat translations                                    ! dynamic mappings + UDP/ICMP entries (ports)
R1# show ip nat statistics                                      ! dynamic, extended, ACL -> pool
R1# clear ip nat translation *                                  ! also clears dynamic mappings
R1# show run | include nat                                      ! check the NAT commands
```

### 7. The lab (video #92)

Same topology as the static NAT lab (PC1-PC3 in 172.16.0.0/24, R1 G0/0 to the Internet 203.0.113.1, G0/1 internal).

1. **Dynamic NAT**: `interface g0/0` `ip nat outside`, `interface g0/1` `ip nat inside`; `access-list 1 permit 172.16.0.0 0.0.0.255`; pool with **two addresses**: `ip nat pool POOL1 100.0.0.1 100.0.0.2 netmask 255.255.255.0` (subnet 100.0.0.0/24); `ip nat inside source list 1 pool POOL1`.
2. Tests: `ping 8.8.8.8` then `ping google.com` from PC1 (OK), PC2 (OK), **PC3: no response**: both pool addresses are used by PC1 and PC2 (**pool exhaustion**). `do show ip nat translations`: 172.16.0.1 → 100.0.0.1, 172.16.0.2 → 100.0.0.2, ICMP and UDP entries; in Packet Tracer the simple mapping entries from the lecture **don't appear** (differs from real IOS; on the exam you interpret a table, you aren't asked to predict its entries).
3. **Switch to PAT on the interface**: `do clear ip nat translation *`; `do show run | include nat`; without deleting the old command, `ip nat inside source list 1 interface g0/0 overload`: the previous statement is **replaced** in the running-config (the pool remains, remove it if you like).
4. `ping google.com` from PC1, PC2 and **PC3: works this time**. `do show ip nat translations`: 172.16.0.1, .2 and .3 translated to **203.0.113.1**; R1 tracks flows by **protocol and port numbers**.

Note: the video announces a Boson NetSim bonus lab, but the transcript jumps straight to the channel-member thanks; no information about that lab.

### 8. The quiz (5 questions + 1 Boson)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which NAT type best fulfills the goal of preserving public IPv4 addresses? | **NAT Overload (PAT)** (D) | Many hosts share a single public address, the router tracking flows by Layer 4 port; most networks only need one public address. |
| Which dynamic NAT configuration translates 172.16.1.0/24 to addresses from 203.0.113.0/25? | **B** | A: netmask 255.255.255.128 is correct but the range 203.0.113.0 to .255 includes .255, outside /25 → rejected. C: the ACL uses 255.255.255.0 instead of the wildcard mask 0.0.0.255. |
| Pool of 10 addresses all in use, another inside host sends a packet to the Internet: what does R1 do? | **It discards the packet** (B) | With no available pool address, the router simply drops the packet. |
| Which configuration translates 10.0.1.0/27 to the router's G0/1 interface address? | **A** | The only option with the correct /27 wildcard mask in the ACL, the correct `ip nat` command, and correctly assigned inside/outside interfaces. |
| After the interfaces, an ACL that **denies** 192.168.1.0/24: what happens to those hosts' packets? | **They are not translated by R1** (C) | Permitted = translated, denied = not translated; the ACL denying packets doesn't mean the router drops them. |
| Boson: HostA (10.1.7.7) opens an HTTP connection to HostB (192.0.2.28) through RouterA (internal 10.1.7.1, external 203.0.113.62); which `show ip nat translations` line? | **C**: inside global 203.0.113.62, inside local 10.1.7.7, outside local = outside global 192.0.2.28 | Inside local = HostA's real address (not 10.1.7.1, the router's internal interface); with PAT to the interface, the inside global is the **external interface's** public address. |
