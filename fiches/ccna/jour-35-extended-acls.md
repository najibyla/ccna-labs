# CCNA Day 35 : Extended ACLs / ACL étendues

> Source : Jeremy's IT Lab, vidéo n°71 « Extended ACLs | Day 35 » (cours, 41 min) et vidéo n°72 « Extended ACLs | Day 35 Lab » (lab, 22 min) de la playlist. Fiche rédigée à partir des transcriptions le 6 octobre 2026. Les ACL affichées à l'écran dans les quiz Q1, Q3, Q4 et Q5 ne sont pas dans la transcription : seule la logique de la réponse est reprise.

## 🇫🇷 Version française

### 1. Cadre

Sujet d'examen **5.6** : tout ce qui a été vu au Day 34 (rôle, logique, application aux interfaces, implicit deny) vaut pour les ACL étendues. Seule différence : elles font une **correspondance plus précise** que les ACL standard (IP source seulement).

### 2. Configurer une ACL numérotée en mode « nommé »

- Sur un IOS moderne, `ip access-list standard 1` accepte un **numéro** aussi bien qu'un nom : on configure l'ACL numérotée avec les sous-commandes du mode d'ACL nommée. La config courante l'affiche ensuite **comme si** elle avait été tapée en mode global (`access-list 1 ...`).
- Avantages du mode d'ACL nommée, même pour une ACL numérotée :
  1. **Supprimer une entrée** : `no <n° de séquence>` (ex. `no 30`). En mode global, `no access-list 1 deny 192.168.3.0 0.0.0.255` **supprime toute l'ACL**, pas seulement l'entrée : il faudrait la recréer de zéro.
  2. **Insérer une entrée** au milieu en précisant le numéro de séquence (ex. `30 deny 192.168.2.0 0.0.0.255` entre 20 et 40). En mode global, l'entrée va toujours à la fin, avec un numéro **10 de plus** que le plus haut.
- **Resequencing** : `ip access-list resequence <ACL> <début> <incrément>` en mode global, pour toutes les ACL (numérotées, nommées, standard, étendues). Exemple : des entrées 1, 2, 3, 4, 5 (aucun espace pour insérer) → `ip access-list resequence 1 10 10` → 10, 20, 30, 40, 50, même ordre conservé. (L'affichage 1, 3, 2, 4, 5 vient du réordonnancement IOS des entrées /32 vu au Day 34.)

### 3. ACL étendues

- Numérotées ou nommées. Plages : **100 à 199** et **2000 à 2699** (à mémoriser, avec 1-99 et 1300-1999 pour les standard). Traitement de haut en bas comme les standard.
- Critères du cours : **protocole de couche 4 et numéro de port, IP source, IP destination**. Un paquet doit correspondre à **tous** les paramètres de l'entrée pour la matcher.
- Syntaxe numérotée en mode global : `access-list <100-199|2000-2699> {permit | deny} <protocole> <source> <destination>`.
- Syntaxe nommée : `ip access-list extended <nom ou numéro>`, puis `{permit | deny} <protocole> <source> [port] <destination> [port]`.
- **Protocole** : nom (`tcp`, `udp`, `icmp`, `ospf`, `eigrp`...) ou **numéro de protocole IP** (champ *Protocol* de l'en-tête IPv4) : **1 = ICMP, 6 = TCP, 17 = UDP, 88 = EIGRP, 89 = OSPF** (à retenir). `ip` matche **tous** les paquets IP (pour un `permit ip any any` final). `icmp` sert à bloquer les pings.
- **Adresses** : `<ip> <wildcard>`, `any`, ou `host <ip>`. En ACL étendue, un /32 exige **`host` ou le wildcard 0.0.0.0** : écrire l'adresse seule n'est pas accepté (possible seulement en ACL standard).
- **Ports** (seulement avec `tcp` ou `udp`, optionnels ; sans port, tous les ports correspondent), après l'adresse source (port source) et/ou après l'adresse destination (port destination) : **`eq`** (égal, le plus courant), **`gt`** (supérieur, `gt 80` = 81 et plus), **`lt`** (inférieur, `lt 80` = 79 et moins), **`neq`** (différent), **`range`** (`range 80 100`). Un mot-clé peut remplacer le numéro (`www` = 80, `telnet` = 23, `tftp` = 69, IOS convertit 69 en `tftp`), mais beaucoup de ports n'en ont pas : apprendre les numéros.
- Autres options après la destination (hors CCNA) : `ack`, `fin`, `syn` (drapeaux TCP), `ttl`, `dscp`.

Exemples corrigés de la vidéo :

| Exigence | Entrée |
| :--- | :--- |
| Permettre tout le trafic | `permit ip any any` |
| Empêcher 10.0.0.0/16 d'envoyer de l'UDP à 192.168.1.1/32 | `deny udp 10.0.0.0 0.0.255.255 host 192.168.1.1` |
| Empêcher 172.16.1.1/32 de pinger 192.168.0.0/24 | `deny icmp host 172.16.1.1 192.168.0.0 0.0.0.255` |
| Refuser tout paquet vers 1.1.1.1/32, port TCP 80 | `deny tcp any host 1.1.1.1 eq 80` |
| Autoriser 10.0.0.0/16 vers le serveur 2.2.2.2/32 en HTTPS | `permit tcp 10.0.0.0 0.0.255.255 2.2.2.2 0.0.0.0 eq 443` |
| Interdire les ports source UDP 20000 à 30000 vers 3.3.3.3/32 | `deny udp any range 20000 30000 host 3.3.3.3` |
| 172.16.1.0/24, port source TCP > 9999, vers tous les ports TCP de 4.4.4.4/32 sauf 23 | `permit tcp 172.16.1.0 0.0.0.255 gt 9999 host 4.4.4.4 neq 23` |

### 4. Règle de placement

- **ACL standard : au plus près de la destination** (peu précises, elles bloqueraient trop de trafic près de la source).
- **ACL étendue : au plus près de la source**, pour que les paquets refusés voyagent le moins possible et ne gaspillent pas les ressources des routeurs ; bien configurées, elles ne risquent guère de bloquer plus que prévu.
- Exemple sur R1 (réseau du Day 34) : `deny tcp 192.168.1.0 0.0.0.255 host 10.0.1.100 eq 443` + `permit ip any any`, appliquée **inbound sur G0/1** (côté 192.168.1.0/24) ; `deny ip 192.168.2.0 0.0.0.255 10.0.2.0 0.0.0.255` + `permit ip any any`, **inbound sur G0/2** ; trois `deny icmp` (192.168.1.0/24 vers 10.0.1.0/24 et 10.0.2.0/24, 192.168.2.0/24 vers 10.0.1.0/24, le dernier cas étant déjà bloqué par l'ACL précédente) + `permit ip any any`, **outbound sur G0/0** pour couvrir les deux sous-réseaux sources. Pas la solution la plus efficace, Jeremy invite à en trouver une plus courte.
- **`show ip interface <int>`** (sans `brief`) indique l'ACL appliquée en *outgoing* et *inbound* (ou « not set »).

### 5. Pièges d'examen

- Plages : **100-199, 2000-2699** (étendues) ; **1-99, 1300-1999** (standard).
- `no access-list <n> ...` en mode global **supprime toute l'ACL** (quiz Q2).
- HTTP et HTTPS utilisent **TCP**, pas UDP ; pour filtrer le trafic venant d'un sous-réseau, appliquer **inbound** sur l'interface qui le reçoit (quiz Q5).
- Protocole **89 = OSPF**, **88 = EIGRP** (quiz Q4).
- Le port d'un service se met après l'adresse **destination** (serveur), pas après la source (quiz Q1 : `permit udp host PC1 host SRV1 eq 69`).
- Avec un wildcard, un seul `permit tcp any 10.10.10.0 0.0.0.3 eq ftp` couvre deux serveurs voisins, l'implicit deny bloquant le reste (bonus Boson).

### 6. Commandes IOS

```
R1(config)# ip access-list standard 1                     ! ACL numérotée configurée en mode d'ACL nommée
R1(config-std-nacl)# no 30                                ! supprime l'entrée 30 seulement
R1(config-std-nacl)# 30 deny 192.168.2.0 0.0.0.255        ! insère une entrée avec le numéro 30
R1(config)# no access-list 1 deny 192.168.3.0 0.0.0.255   ! ATTENTION : supprime toute l'ACL 1
R1(config)# ip access-list resequence 1 10 10             ! renumérote : première entrée 10, pas de 10
R1(config)# access-list 100 deny tcp any host 1.1.1.1 eq 80            ! ACL étendue numérotée, mode global
R1(config)# ip access-list extended HTTPS_SRV1            ! ACL étendue nommée (nom ou numéro 100-199, 2000-2699)
R1(config-ext-nacl)# deny tcp 192.168.1.0 0.0.0.255 host 10.0.1.100 eq 443
R1(config-ext-nacl)# deny ip 192.168.2.0 0.0.0.255 10.0.2.0 0.0.0.255   ! ip = tous les paquets
R1(config-ext-nacl)# deny icmp 192.168.1.0 0.0.0.255 10.0.1.0 0.0.0.255 ! bloque les pings
R1(config-ext-nacl)# deny udp any range 20000 30000 host 3.3.3.3        ! port source en plage
R1(config-ext-nacl)# permit tcp 172.16.1.0 0.0.0.255 gt 9999 host 4.4.4.4 neq 23
R1(config-ext-nacl)# permit ip any any                    ! équivalent du permit any standard
R1(config-if)# ip access-group HTTPS_SRV1 in              ! application, comme pour les ACL standard
R1# show ip interface g0/1                                ! ACL appliquées outgoing / inbound sur l'interface
R1# show access-lists                                     ! entrées, séquences, compteurs de correspondances
```

### 7. Le lab (vidéo n°72)

Objectif : deux ACL étendues sur R1. Exigences : 172.16.2.0/24 ne communique pas avec PC1 (172.16.1.1) ; 172.16.1.0/24 n'accède pas au service **DNS** de SRV1 (192.168.1.100) ; 172.16.2.0/24 n'accède pas aux services **HTTP/HTTPS** de SRV2 (192.168.2.100).

1. Aperçu de DNS : PC1 a SRV1 comme serveur DNS ; `ping PC2` résout le nom en 172.16.1.2 via SRV1 (les serveurs DNS tiennent la liste noms ↔ adresses IP).
2. **ACL 100** (`ip access-list extended 100`) : DNS utilise **UDP et parfois TCP**, port **53** → `deny udp 172.16.1.0 0.0.0.255 host 192.168.1.100 eq 53`, `deny tcp 172.16.1.0 0.0.0.255 host 192.168.1.100 eq 53`, `permit ip any any`. Appliquée au plus près de la source : `interface g0/0`, `ip access-group 100 in`. Test : `ping SRV2` sur PC1 → « could not find host SRV2 » après 30 s ; `ping 192.168.2.100` fonctionne (les premiers pings échouent le temps d'ARP).
3. **ACL 101** (même source pour les exigences 1 et 3) : `deny ip 172.16.2.0 0.0.0.255 host 172.16.1.1` ; `deny tcp 172.16.2.0 0.0.0.255 host 192.168.2.100 eq 80` ; même entrée avec `eq 443` ; `permit ip any any`. `interface g0/1`, `ip access-group 101 in`. Test sur PC3 : le navigateur n'affiche plus `cisco.com` (entrée DNS sur SRV1 pointant vers SRV2, requête expirée) ; `ping PC1` échoue ; `ping PC2` réussit (DNS toujours accessible pour ce sous-réseau).
4. `do show access-lists` : compteurs de correspondances par entrée.

Bonus NetSim (ACL étendues, jusqu'à l'étape 7) : ACL 101 sur **Router2** (au plus près des sources PC2 et PC3) en une seule règle : `access-list 101 permit tcp 10.10.2.0 0.0.1.255 1.1.1.1 0.0.0.0 eq telnet` (wildcard /23 couvrant les VLAN 2 et 3, Telnet = TCP 23). Appliquée **outbound sur F0/0** plutôt qu'inbound sur les deux sous-interfaces du router-on-a-stick (impossible sur l'interface physique). Résultat : Telnet vers 1.1.1.1 fonctionne depuis PC2 et PC3, mais les **pings échouent** à cause de l'implicit deny (une étape ultérieure du lab ajoute `permit icmp any any`).

### 8. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quelle ACL, appliquée outbound sur G0/0 de R1, n'autorise que PC1 vers le serveur TFTP de SRV1 ? | **ACL 103** : permit UDP de PC1 vers SRV1 port 69 (affiché `tftp`), deny UDP des autres hôtes vers SRV1 port 69, permit du reste | ACL 102 met le port 69 côté **source** au lieu de la destination. |
| Effet de `no access-list 1 deny 10.0.2.0 0.0.0.255` sur ACL 1 ? | **ACL 1 est supprimée** | En mode global on ne peut pas retirer une seule entrée ; il faut le mode d'ACL nommée. |
| Commande ayant renuméroté l'ACL 199 de 1, 2, 3, 4, 5 en 5, 15, 25, 35, 45 ? | **`ip access-list resequence 199 5 10`** | Premier numéro 5, incrément 10. |
| Quelle ACL empêche R1 de transmettre des paquets OSPF par G0/2 ? | **ACL 112** : `deny 89` (OSPF), `permit ip any any`, appliquée outbound sur G0/2 | Le protocole 88 (ACL 111 et 113) est EIGRP. |
| ACL 150 doit refuser HTTP et HTTPS de 192.168.1.0/24 vers 10.0.2.0/24 : deux corrections ? | **Appliquer inbound sur G0/1** et **protocole TCP, pas UDP** | On filtre le trafic entrant par G0/1 depuis 192.168.1.0/24 ; HTTP/HTTPS sont en TCP. Ports 88 et 404 n'ont rien à voir. |

Bonus Boson : après `access-list 101 permit tcp any host 10.10.10.20` (serveur web, outbound F0/0), n'autoriser que FTP vers Music Server1 et 2 → `access-list 101 permit tcp any 10.10.10.0 0.0.0.3 eq ftp` ; l'implicit deny bloque les autres serveurs du /24.

---

## 🇬🇧 English version

### 1. Scope

Exam topic **5.6**: everything from Day 34 (purpose, logic, applying to interfaces, implicit deny) applies to extended ACLs. The only difference: they can do **more specific matching** than standard ACLs (source IP only).

### 2. Configuring numbered ACLs in named ACL config mode

- On modern IOS, `ip access-list standard 1` accepts a **number** as well as a name: the numbered ACL is configured with named-mode subcommands. The running config then displays it **as if** it were typed in global config mode (`access-list 1 ...`).
- Advantages of named ACL config mode, even for numbered ACLs:
  1. **Delete one entry**: `no <sequence>` (e.g. `no 30`). In global mode, `no access-list 1 deny 192.168.3.0 0.0.0.255` **deletes the whole ACL**, not just the entry: it would have to be rebuilt from scratch.
  2. **Insert an entry** in the middle by specifying the sequence number (e.g. `30 deny 192.168.2.0 0.0.0.255` between 20 and 40). In global mode, entries always go to the end, numbered **10 higher** than the current highest.
- **Resequencing**: `ip access-list resequence <ACL> <start> <increment>` in global config, for all ACLs (numbered, named, standard, extended). Example: entries 1, 2, 3, 4, 5 (no room to insert) → `ip access-list resequence 1 10 10` → 10, 20, 30, 40, 50, same order kept. (The 1, 3, 2, 4, 5 display comes from the IOS /32 reordering seen on Day 34.)

### 3. Extended ACLs

- Numbered or named. Ranges: **100 to 199** and **2000 to 2699** (memorize, along with 1-99 and 1300-1999 for standard). Processed top to bottom like standard ACLs.
- Criteria in this course: **Layer 4 protocol and port number, source IP, destination IP**. A packet must match **all** parameters of an entry to match it.
- Numbered syntax in global config: `access-list <100-199|2000-2699> {permit | deny} <protocol> <source> <destination>`.
- Named syntax: `ip access-list extended <name or number>`, then `{permit | deny} <protocol> <source> [port] <destination> [port]`.
- **Protocol**: name (`tcp`, `udp`, `icmp`, `ospf`, `eigrp`...) or **IP protocol number** (Protocol field of the IPv4 header): **1 = ICMP, 6 = TCP, 17 = UDP, 88 = EIGRP, 89 = OSPF** (remember these). `ip` matches **all** IP packets (for a final `permit ip any any`). `icmp` is used to block pings.
- **Addresses**: `<ip> <wildcard>`, `any`, or `host <ip>`. In an extended ACL a /32 requires **`host` or the 0.0.0.0 wildcard**: the bare address is not accepted (only possible in standard ACLs).
- **Ports** (only with `tcp` or `udp`, optional; without a port all ports match), after the source address (source port) and/or after the destination address (destination port): **`eq`** (equal, most common), **`gt`** (greater than, `gt 80` = 81 and up), **`lt`** (less than, `lt 80` = 79 and below), **`neq`** (not equal), **`range`** (`range 80 100`). A keyword can replace the number (`www` = 80, `telnet` = 23, `tftp` = 69, IOS converts 69 to `tftp`), but many ports have none: learn the numbers.
- Other options after the destination (beyond the CCNA): `ack`, `fin`, `syn` (TCP flags), `ttl`, `dscp`.

Worked examples from the video:

| Requirement | Entry |
| :--- | :--- |
| Permit all traffic | `permit ip any any` |
| Prevent 10.0.0.0/16 from sending UDP to 192.168.1.1/32 | `deny udp 10.0.0.0 0.0.255.255 host 192.168.1.1` |
| Prevent 172.16.1.1/32 from pinging 192.168.0.0/24 | `deny icmp host 172.16.1.1 192.168.0.0 0.0.0.255` |
| Deny all packets to 1.1.1.1/32, TCP port 80 | `deny tcp any host 1.1.1.1 eq 80` |
| Allow 10.0.0.0/16 to reach server 2.2.2.2/32 using HTTPS | `permit tcp 10.0.0.0 0.0.255.255 2.2.2.2 0.0.0.0 eq 443` |
| Block UDP source ports 20000 to 30000 to 3.3.3.3/32 | `deny udp any range 20000 30000 host 3.3.3.3` |
| 172.16.1.0/24, TCP source port > 9999, to all TCP ports of 4.4.4.4/32 except 23 | `permit tcp 172.16.1.0 0.0.0.255 gt 9999 host 4.4.4.4 neq 23` |

### 4. Placement rule

- **Standard ACLs: as close to the destination as possible** (not specific, they would block too much near the source).
- **Extended ACLs: as close to the source as possible**, so denied packets travel as little as possible and routers do not waste resources; configured correctly, there is little risk of blocking more than intended.
- Example on R1 (Day 34 network): `deny tcp 192.168.1.0 0.0.0.255 host 10.0.1.100 eq 443` + `permit ip any any`, applied **inbound on G0/1** (192.168.1.0/24 side); `deny ip 192.168.2.0 0.0.0.255 10.0.2.0 0.0.0.255` + `permit ip any any`, **inbound on G0/2**; three `deny icmp` entries (192.168.1.0/24 to 10.0.1.0/24 and 10.0.2.0/24, 192.168.2.0/24 to 10.0.1.0/24, the remaining case being already blocked by the previous ACL) + `permit ip any any`, **outbound on G0/0** to cover both source subnets. Not the most efficient solution; Jeremy challenges you to find a shorter one.
- **`show ip interface <int>`** (without `brief`) shows the ACL applied *outgoing* and *inbound* (or "not set").

### 5. Exam traps

- Ranges: **100-199, 2000-2699** (extended); **1-99, 1300-1999** (standard).
- `no access-list <n> ...` in global config **deletes the whole ACL** (quiz Q2).
- HTTP and HTTPS use **TCP**, not UDP; to filter traffic coming from a subnet, apply **inbound** on the interface receiving it (quiz Q5).
- Protocol **89 = OSPF**, **88 = EIGRP** (quiz Q4).
- A service's port goes after the **destination** address (server), not the source (quiz Q1: `permit udp host PC1 host SRV1 eq 69`).
- With a wildcard, a single `permit tcp any 10.10.10.0 0.0.0.3 eq ftp` covers two adjacent servers, the implicit deny blocking the rest (Boson bonus).

### 6. IOS commands

```
R1(config)# ip access-list standard 1                     ! numbered ACL configured in named ACL config mode
R1(config-std-nacl)# no 30                                ! deletes entry 30 only
R1(config-std-nacl)# 30 deny 192.168.2.0 0.0.0.255        ! inserts an entry with sequence 30
R1(config)# no access-list 1 deny 192.168.3.0 0.0.0.255   ! WARNING: deletes all of ACL 1
R1(config)# ip access-list resequence 1 10 10             ! renumber: first entry 10, step 10
R1(config)# access-list 100 deny tcp any host 1.1.1.1 eq 80            ! extended numbered ACL, global mode
R1(config)# ip access-list extended HTTPS_SRV1            ! extended named ACL (name or number 100-199, 2000-2699)
R1(config-ext-nacl)# deny tcp 192.168.1.0 0.0.0.255 host 10.0.1.100 eq 443
R1(config-ext-nacl)# deny ip 192.168.2.0 0.0.0.255 10.0.2.0 0.0.0.255   ! ip = all packets
R1(config-ext-nacl)# deny icmp 192.168.1.0 0.0.0.255 10.0.1.0 0.0.0.255 ! blocks pings
R1(config-ext-nacl)# deny udp any range 20000 30000 host 3.3.3.3        ! source port range
R1(config-ext-nacl)# permit tcp 172.16.1.0 0.0.0.255 gt 9999 host 4.4.4.4 neq 23
R1(config-ext-nacl)# permit ip any any                    ! equivalent of a standard permit any
R1(config-if)# ip access-group HTTPS_SRV1 in              ! applied like standard ACLs
R1# show ip interface g0/1                                ! ACLs applied outgoing / inbound on the interface
R1# show access-lists                                     ! entries, sequences, match counters
```

### 7. The lab (video 72)

Goal: two extended ACLs on R1. Requirements: 172.16.2.0/24 cannot communicate with PC1 (172.16.1.1); 172.16.1.0/24 cannot access the **DNS** service on SRV1 (192.168.1.100); 172.16.2.0/24 cannot access the **HTTP/HTTPS** services on SRV2 (192.168.2.100).

1. DNS preview: PC1 has SRV1 as its DNS server; `ping PC2` resolves the name to 172.16.1.2 via SRV1 (DNS servers hold the list of names and IP addresses).
2. **ACL 100** (`ip access-list extended 100`): DNS uses **UDP and sometimes TCP**, port **53** → `deny udp 172.16.1.0 0.0.0.255 host 192.168.1.100 eq 53`, `deny tcp 172.16.1.0 0.0.0.255 host 192.168.1.100 eq 53`, `permit ip any any`. Applied close to the source: `interface g0/0`, `ip access-group 100 in`. Test: `ping SRV2` on PC1 → "could not find host SRV2" after 30 s; `ping 192.168.2.100` works (first pings fail while ARP completes).
3. **ACL 101** (same source for requirements 1 and 3): `deny ip 172.16.2.0 0.0.0.255 host 172.16.1.1`; `deny tcp 172.16.2.0 0.0.0.255 host 192.168.2.100 eq 80`; same entry with `eq 443`; `permit ip any any`. `interface g0/1`, `ip access-group 101 in`. Test on PC3: the browser no longer shows `cisco.com` (DNS entry on SRV1 pointing to SRV2, request times out); `ping PC1` fails; `ping PC2` succeeds (DNS still reachable for this subnet).
4. `do show access-lists`: match counters per entry.

NetSim bonus (extended ACLs, up to step 7): ACL 101 on **Router2** (closest to sources PC2 and PC3) in a single rule: `access-list 101 permit tcp 10.10.2.0 0.0.1.255 1.1.1.1 0.0.0.0 eq telnet` (/23 wildcard covering VLANs 2 and 3, Telnet = TCP 23). Applied **outbound on F0/0** rather than inbound on both router-on-a-stick subinterfaces (not possible on the physical interface). Result: Telnet to 1.1.1.1 works from PC2 and PC3, but **pings fail** because of the implicit deny (a later lab step adds `permit icmp any any`).

### 8. The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which ACL, applied outbound on R1 G0/0, permits only PC1 to access the TFTP server on SRV1? | **ACL 103**: permit UDP from PC1 to SRV1 port 69 (shown as `tftp`), deny UDP from other hosts to SRV1 port 69, permit the rest | ACL 102 puts port 69 on the **source** instead of the destination. |
| Effect of `no access-list 1 deny 10.0.2.0 0.0.0.255` on ACL 1? | **ACL 1 is deleted** | Global mode cannot remove a single entry; named ACL config mode is needed. |
| Command that resequenced ACL 199 from 1, 2, 3, 4, 5 to 5, 15, 25, 35, 45? | **`ip access-list resequence 199 5 10`** | First number 5, increment 10. |
| Which ACL prevents R1 from forwarding OSPF packets out of G0/2? | **ACL 112**: `deny 89` (OSPF), `permit ip any any`, applied outbound on G0/2 | Protocol 88 (ACLs 111 and 113) is EIGRP. |
| ACL 150 should deny HTTP and HTTPS from 192.168.1.0/24 to 10.0.2.0/24: two fixes? | **Apply inbound on G0/1** and **protocol TCP, not UDP** | We filter traffic entering G0/1 from 192.168.1.0/24; HTTP/HTTPS use TCP. Ports 88 and 404 are irrelevant. |

Boson bonus: after `access-list 101 permit tcp any host 10.10.10.20` (web server, outbound F0/0), allow only FTP to Music Server1 and 2 → `access-list 101 permit tcp any 10.10.10.0 0.0.0.3 eq ftp`; the implicit deny blocks the other servers in the /24.
