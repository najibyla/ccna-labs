# CCNA Day 38 : DNS / Domain Name System

> Source : Jeremy's IT Lab, « Free CCNA | DNS | Day 38 » (30 min, vidéo n°77 de la playlist, cours) et « Free CCNA | DNS | Day 38 Lab » (17 min, vidéo n°78, lab Packet Tracer). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Rôle de DNS

- Sujet d'examen **4.3** : expliquer le rôle de DHCP et de DNS dans le réseau. Pas besoin de connaître DNS en profondeur, seulement son **objectif de base**.
- DNS **résout** (*resolve* = convertit) des noms lisibles par les humains comme `google.com` en **adresses IP**. Les machines utilisent des adresses, pas des noms ; les noms sont plus faciles à retenir.
- Quand on tape `youtube.com` dans un navigateur, l'appareil **demande à un serveur DNS** l'adresse IP. Le ou les serveurs DNS d'un hôte sont **configurés manuellement ou appris via DHCP** (*Dynamic Host Configuration Protocol*, vidéo future).

### 2. Fonctionnement de base (démonstration Windows, PC1 → serveur Google 8.8.8.8)

- `ipconfig /all` affiche le serveur DNS du PC (`ipconfig` seul ne le montre pas). « Vérifier les paramètres IP d'un OS client » est un sujet d'examen CCNA.
- `nslookup youtube.com` (*Name Server Lookup*) : demande au serveur DNS l'adresse IP du nom. Réponse : IPv4 172.217.25.110 et une adresse IPv6. Puis `ping youtube.com` fonctionne : le nom est converti en IP. `nslookup` n'est pas obligatoire avant un ping : l'appareil interroge automatiquement le serveur s'il ne connaît pas l'adresse.
- Échange : PC1 envoie une **requête DNS** (*DNS query*) à 8.8.8.8, le serveur **répond** avec l'adresse. **R1 n'est ni serveur ni client DNS, il transfère simplement les paquets : aucune configuration DNS n'est nécessaire sur le routeur.** Point important.
- Capture Wireshark : quatre messages. **Standard query** `A youtube.com` → **standard query response** avec une adresse IPv4 ; puis **standard query** `AAAA youtube.com` (*quadruple A*) → réponse avec une adresse IPv6.
  - Enregistrement **A** : nom → adresse **IPv4**.
  - Enregistrement **AAAA** (*quad A*) : nom → adresse **IPv6**.
- Couche 4 : **UDP**. DNS utilise **TCP et UDP** : les requêtes et réponses standard utilisent **UDP** ; **TCP** est utilisé pour les messages de **plus de 512 octets**. Dans les deux cas, **port 53**.
- **Cache DNS** : l'appareil enregistre les réponses localement pour ne pas réinterroger le serveur à chaque fois (moins de trafic). Windows : `ipconfig /displaydns`. L'entrée `youtube.com` y apparaît comme **CNAME** (*canonical name*), un enregistrement qui fait correspondre un nom à **un autre nom** ; l'enregistrement A de cet autre nom porte l'adresse 172.217.25.110. `ipconfig /flushdns` vide le cache (« DNS resolver cache was flushed ») : la prochaine requête repart vers le serveur.
- **Fichier hosts** : liste simple « adresse IP, espace, nom d'hôte », dans Windows `C:\Windows\System32\drivers\etc\hosts`, vide par défaut. Jeremy ajoute une entrée pour R1 et `ping R1` fonctionne. Ce **n'est pas DNS**, c'est une alternative antérieure à DNS, utilisable dans un petit réseau ; DNS est bien meilleur.

### 3. Configurer DNS dans Cisco IOS

Rappel : pour que les hôtes utilisent DNS, **rien à configurer sur les routeurs**. Un routeur Cisco peut toutefois être **serveur DNS** (rare ; un serveur DNS interne est en général un serveur Windows ou Linux ; « interne » = dans le réseau local) et **client DNS** (pour utiliser `ping` avec des noms).

**Routeur serveur DNS**

1. `ip dns server` : le routeur répond aux requêtes DNS s'il possède l'enregistrement.
2. `ip host <nom> <ip>` : construit la **table d'hôtes** (entrées pour R1, PC1, PC2, PC3).
3. `ip name-server 8.8.8.8` : serveur DNS externe que R1 interroge s'il n'a pas l'enregistrement demandé.
4. `ip domain lookup` : permet à R1 d'effectuer des requêtes DNS. **Activé par défaut.** Ancienne forme `ip domain-lookup` (avec tiret), toujours acceptée : connaître les deux.

Démonstration (PC1 configuré avec R1 comme serveur DNS) : `ping PC2 -n 1` → PC1 interroge R1, qui a l'entrée PC2 et répond ; le ping part ; PC1 met PC2 en cache. `ping youtube.com -n 1` → R1 n'a pas l'entrée, il **agit en client** et interroge 8.8.8.8, puis répond à PC1. `show hosts` affiche les hôtes configurés (**flag perm**, permanents) et ceux appris par DNS (**flag temp**, temporaires, à réapprendre après expiration).

**Routeur client DNS** : `ip name-server 8.8.8.8` et `ip domain lookup` (déjà actif). Sans ces réglages, `ping youtube.com` échoue (« unable to translate »). Dans ce cas R1 n'est **pas** serveur : il ne répond pas aux requêtes de PC1.

**Commande optionnelle** : `ip domain name jeremysitlab.com` (ancienne forme `ip domain-name`). Un **nom de domaine** définit un domaine de contrôle administratif (`mail.google.com`, `dns.google.com`, `time.google.com` sont sous l'administration de Google). Nom de domaine par défaut ajouté aux noms d'hôtes sans domaine : `ping PC1` devient `ping PC1.jeremysitlab.com`. Nécessaire pour activer **SSH** (vidéo ultérieure).

### 4. Pièges d'examen

- **Aucune configuration DNS n'est nécessaire sur un routeur** pour que les hôtes utilisent un serveur DNS externe : il transfère les paquets.
- **A = IPv4, AAAA = IPv6** (pas « triple A »). **CNAME** = nom vers nom.
- **UDP 53** pour les requêtes standard ; **TCP 53** au-delà de **512 octets**. Pas de connexion TCP avec le serveur DNS pour une requête standard (question Boson).
- `ip domain lookup` est **activé par défaut** ; formes avec et sans tiret (`ip domain-lookup`, `ip domain-name`).
- `show hosts` (IOS) ≠ `ipconfig /displaydns` (Windows). `ipconfig` seul n'affiche pas le serveur DNS ; `ipconfig /all` et `nslookup` l'affichent.
- Les hôtes apprennent leur serveur DNS via **DHCP**.
- Un routeur Cisco peut être **serveur et client DNS en même temps**.

### 5. Commandes

```text
C:\> ipconfig /all            ! Windows : paramètres IP dont le serveur DNS
C:\> nslookup youtube.com     ! interroge le serveur DNS, affiche le serveur et les adresses
C:\> ipconfig /displaydns     ! affiche le cache DNS
C:\> ipconfig /flushdns       ! vide le cache DNS
C:\> ping youtube.com -n 1    ! un seul ping, par nom

Router(config)# ip dns server             ! le routeur agit en serveur DNS (absent de Packet Tracer)
Router(config)# ip host PC1 192.168.0.1   ! entrée de la table d'hôtes
Router(config)# ip name-server 8.8.8.8    ! serveur DNS à interroger (client DNS)
Router(config)# ip domain lookup          ! autorise les requêtes DNS (défaut ; ancien : ip domain-lookup)
Router(config)# ip domain name jeremysitlab.com ! domaine par défaut (ancien : ip domain-name)
Router# show hosts                        ! table d'hôtes : perm (configurés) et temp (appris par DNS)
```

### 6. Le lab (vidéo n°78)

Objectif : R1 et PC1-PC3 utilisent **1.1.1.1** (serveur DNS public Cloudflare, simulé) comme serveur DNS. `ip dns server` **n'existe pas dans Packet Tracer**. Le nuage « INTERNET » est un simple routeur avec une autre icône.

1. **Route par défaut** sur R1 : `ip route 0.0.0.0 0.0.0.0 203.0.113.2` ; `do ping 1.1.1.1` (un ou deux échecs possibles, ARP lent dans Packet Tracer).
2. **PC1, PC2, PC3** : onglet Config, champ DNS server = 1.1.1.1 (choix Static ; DHCP sera vu bientôt).
3. **R1** : `ip name-server 1.1.1.1` ; table d'hôtes `ip host R1 192.168.0.254`, `ip host PC1 192.168.0.1`, `ip host PC2 192.168.0.2`, `ip host PC3 192.168.0.3`. Vérification `do show hosts`, puis `do ping PC1` réussi (nécessite `ip domain lookup`, actif par défaut).
4. **Mode simulation** : `ping youtube.com` depuis PC1. Pas d'ARP (R1 a déjà pingé PC1 et 1.1.1.1). La requête DNS va PC1 → R1 → Internet → 1.1.1.1 et revient ; dans « inbound PDU details », la réponse donne 172.217.6.78. PC1 crée alors l'ICMP vers cette adresse ; le routeur Internet doit faire un ARP vers youtube.com, donc le **premier ping échoue**, les trois suivants réussissent. Leçon : un ping par nom implique des messages **DNS et ARP**, pas seulement ICMP.

Bonus Boson NetSim « Configuring DNS 1 » : commandes NetSim `ipconfig /ip`, `/dg`, `/dns` sur les PC ; adresse sur le **SVI VLAN 1** du switch (10.0.0.2/24, utile pour SSH/Telnet, vidéo ultérieure) ; `show ip interface f0/0` pour voir le masque (pas `show ip interface brief`). `ping Router1` depuis Switch1 échoue (« unrecognized host or address ») ; sur Router1 `ip dns server` + `ip host Router1 10.0.0.1` + `ip host Switch1 10.0.0.2` ; sur Switch1 `ip name-server 10.0.0.1` + `ip domain-lookup` ; le ping par nom réussit (« translating Router1... domain server 10.0.0.1 »).

### 7. Le quiz (5 questions + 1 Boson)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quelles commandes Windows affichent le serveur DNS du PC ? (deux) | **`ipconfig /all`** (B) et **`nslookup`** (D) | A, `ipconfig`, montre IP, masque, passerelle mais pas le serveur DNS ; C, `ipconfig /displaydns`, montre le cache, pas l'adresse du serveur. |
| Quelles affirmations sur DNS sont vraies ? (deux) | **Les enregistrements A associent un nom à une IPv4** (B) ; **un routeur Cisco peut être serveur et client DNS en même temps** (D) | A : les messages de plus de 512 octets utilisent TCP, pas UDP ; C : ce sont les enregistrements AAAA, pas « triple A », qui associent un nom à une IPv6. |
| PC1 utilise le serveur externe 8.8.8.8 : quelle commande DNS est nécessaire sur R1 ? | **Aucune** (D) | Pour transférer requêtes et réponses DNS, un routeur n'a besoin d'aucune configuration DNS. |
| Quelle commande IOS affiche les correspondances nom/IP mises en cache via DNS ? | **`show hosts`** (A) | Affiche les hôtes appris par DNS et les entrées configurées. B et D n'existent pas ; C est la commande Windows. |
| Quel protocole permet aux hôtes d'apprendre automatiquement leur serveur DNS ? | **DHCP** (C) | DHCP fournit adresse IP, masque, passerelle par défaut et serveur DNS. |
| Boson : HostA envoie sa première requête HTTP à WWW_server, sans fichier hosts. Avec quels équipements établit-il une connexion TCP ? | **Seulement WWW_server** (D) | Pas Default_GW (il transfère seulement). Pas DNS_server : requête DNS standard en UDP, pas de connexion TCP. HTTP utilise TCP port 80, donc connexion TCP avec le serveur web. |

---

## 🇬🇧 English version

### 1. Purpose of DNS

- Exam topic **4.3**: explain the role of DHCP and DNS within the network. No need to know DNS in depth, just its **basic purpose**.
- DNS **resolves** (= converts) human-readable names like `google.com` to **IP addresses**. Machines use addresses, not names; names are easier to remember.
- When you type `youtube.com` in a browser, the device **asks a DNS server** for the IP address. A host's DNS server(s) are **manually configured or learned via DHCP** (Dynamic Host Configuration Protocol, future video).

### 2. Basic functions (Windows demo, PC1 → Google's server 8.8.8.8)

- `ipconfig /all` shows the PC's DNS server (`ipconfig` alone does not). "Verify IP parameters for client operating systems" is a CCNA exam topic.
- `nslookup youtube.com` (Name Server Lookup): asks the DNS server for the name's IP address. Answer: IPv4 172.217.25.110 and an IPv6 address. Then `ping youtube.com` works: the name is converted. `nslookup` is not required before a ping: the device queries the server automatically if it doesn't know the address.
- Exchange: PC1 sends a **DNS query** to 8.8.8.8, the server **replies** with the address. **R1 is neither DNS server nor client, it simply forwards packets: no DNS configuration is required on the router.** Important point.
- Wireshark capture: four messages. **Standard query** `A youtube.com` → **standard query response** with an IPv4 address; then **standard query** `AAAA youtube.com` (quadruple A) → response with an IPv6 address.
  - **A** record: name → **IPv4** address.
  - **AAAA** record (quad A): name → **IPv6** address.
- Layer 4: **UDP**. DNS uses **both TCP and UDP**: standard queries and responses use **UDP**; **TCP** is used for messages **greater than 512 bytes**. Either way, **port 53**.
- **DNS cache**: the device saves responses locally so it doesn't query the server every time (less traffic). Windows: `ipconfig /displaydns`. The `youtube.com` entry shows as **CNAME** (canonical name), a record mapping a name to **another name**; that other name's A record carries 172.217.25.110. `ipconfig /flushdns` clears the cache ("DNS resolver cache was flushed"): the next access requires a new query.
- **hosts file**: a simple list "IP address, space, host name", in Windows `C:\Windows\System32\drivers\etc\hosts`, empty by default. Jeremy adds an entry for R1 and `ping R1` works. This **is not DNS**, it is an older alternative, usable in a small network; DNS is much better.

### 3. Configuring DNS in Cisco IOS

Reminder: for hosts to use DNS, **nothing to configure on routers**. A Cisco router can still be a **DNS server** (rare; an internal DNS server is usually Windows or Linux; "internal" = in the local network) and a **DNS client** (to `ping` using names).

**Router as DNS server**

1. `ip dns server`: the router responds to DNS queries if it has the record.
2. `ip host <name> <ip>`: builds the **host table** (entries for R1, PC1, PC2, PC3).
3. `ip name-server 8.8.8.8`: external DNS server R1 queries when it lacks the requested record.
4. `ip domain lookup`: lets R1 perform DNS queries. **Enabled by default.** Old form `ip domain-lookup` (hyphen) still supported: know both.

Demo (PC1 configured with R1 as DNS server): `ping PC2 -n 1` → PC1 queries R1, which has the PC2 entry and replies; the ping goes; PC1 caches PC2. `ping youtube.com -n 1` → R1 lacks the entry, **acts as a client** and queries 8.8.8.8, then replies to PC1. `show hosts` shows configured hosts (**perm** flag, permanent) and hosts learned via DNS (**temp** flag, temporary, re-learned after expiry).

**Router as DNS client**: `ip name-server 8.8.8.8` and `ip domain lookup` (already on). Without them, `ping youtube.com` fails (unable to translate). In this case R1 is **not** a server: it won't answer PC1's queries.

**Optional command**: `ip domain name jeremysitlab.com` (old form `ip domain-name`). A **domain name** defines a realm of administrative control (`mail.google.com`, `dns.google.com`, `time.google.com` all fall under Google's administration). Default domain name appended to hostnames without one: `ping PC1` becomes `ping PC1.jeremysitlab.com`. Needed to enable **SSH** (later video).

### 4. Exam traps

- **No DNS configuration is needed on a router** for hosts to use an external DNS server: it forwards packets.
- **A = IPv4, AAAA = IPv6** (not "triple A"). **CNAME** = name to name.
- **UDP 53** for standard queries; **TCP 53** above **512 bytes**. No TCP connection with the DNS server for a standard query (Boson question).
- `ip domain lookup` is **enabled by default**; forms with and without hyphen (`ip domain-lookup`, `ip domain-name`).
- `show hosts` (IOS) vs `ipconfig /displaydns` (Windows). `ipconfig` alone doesn't show the DNS server; `ipconfig /all` and `nslookup` do.
- Hosts learn their DNS server via **DHCP**.
- A Cisco router can be **DNS server and client at the same time**.

### 5. Commands

```text
C:\> ipconfig /all            ! Windows: IP parameters including DNS server
C:\> nslookup youtube.com     ! query the DNS server, shows server and addresses
C:\> ipconfig /displaydns     ! show the DNS cache
C:\> ipconfig /flushdns       ! clear the DNS cache
C:\> ping youtube.com -n 1    ! single ping, by name

Router(config)# ip dns server             ! router acts as DNS server (missing in Packet Tracer)
Router(config)# ip host PC1 192.168.0.1   ! host table entry
Router(config)# ip name-server 8.8.8.8    ! DNS server to query (DNS client)
Router(config)# ip domain lookup          ! allow DNS queries (default; old: ip domain-lookup)
Router(config)# ip domain name jeremysitlab.com ! default domain (old: ip domain-name)
Router# show hosts                        ! host table: perm (configured) and temp (learned via DNS)
```

### 6. The lab (video #78)

Goal: R1 and PC1-PC3 use **1.1.1.1** (Cloudflare's public DNS server, simulated) as DNS server. `ip dns server` **does not exist in Packet Tracer**. The "INTERNET" cloud is just a router with a different icon.

1. **Default route** on R1: `ip route 0.0.0.0 0.0.0.0 203.0.113.2`; `do ping 1.1.1.1` (one or two pings may fail, ARP is slow in Packet Tracer).
2. **PC1, PC2, PC3**: Config tab, DNS server field = 1.1.1.1 (Static; DHCP comes soon).
3. **R1**: `ip name-server 1.1.1.1`; host table `ip host R1 192.168.0.254`, `ip host PC1 192.168.0.1`, `ip host PC2 192.168.0.2`, `ip host PC3 192.168.0.3`. Check with `do show hosts`, then `do ping PC1` succeeds (requires `ip domain lookup`, on by default).
4. **Simulation mode**: `ping youtube.com` from PC1. No ARP needed (R1 already pinged PC1 and 1.1.1.1). The DNS query goes PC1 → R1 → Internet → 1.1.1.1 and back; in "inbound PDU details", the answer gives 172.217.6.78. PC1 then creates the ICMP message to that address; the Internet router must ARP for youtube.com, so the **first ping fails**, the next three succeed. Lesson: a ping by name involves **DNS and ARP** messages, not just ICMP.

Boson NetSim bonus "Configuring DNS 1": NetSim commands `ipconfig /ip`, `/dg`, `/dns` on PCs; an address on the switch's **VLAN 1 SVI** (10.0.0.2/24, used for SSH/Telnet, later video); `show ip interface f0/0` to see the mask (not `show ip interface brief`). `ping Router1` from Switch1 fails ("unrecognized host or address"); on Router1 `ip dns server` + `ip host Router1 10.0.0.1` + `ip host Switch1 10.0.0.2`; on Switch1 `ip name-server 10.0.0.1` + `ip domain-lookup`; the ping by name succeeds ("translating Router1... domain server 10.0.0.1").

### 7. The quiz (5 questions + 1 Boson)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which Windows commands display the PC's DNS server? (select two) | **`ipconfig /all`** (B) and **`nslookup`** (D) | A, `ipconfig`, shows IP, mask, default gateway but not the DNS server; C, `ipconfig /displaydns`, shows the cache, not the server address. |
| Which statements about DNS are true? (select two) | **A records map hostnames to IPv4 addresses** (B); **a Cisco router can be DNS server and client at the same time** (D) | A: messages greater than 512 bytes use TCP, not UDP; C: AAAA records, not "triple A", map hostnames to IPv6. |
| PC1 uses external server 8.8.8.8: what DNS command is necessary on R1? | **None** (D) | To forward DNS queries and replies, a router needs no DNS configuration. |
| Which IOS command shows the cached name/IP mappings learned via DNS? | **`show hosts`** (A) | Shows hosts learned via DNS and manually configured entries. B and D are not real commands; C is the Windows command. |
| Which protocol lets hosts automatically learn their DNS server's address? | **DHCP** (C) | DHCP provides IP address, subnet mask, default gateway and DNS server. |
| Boson: HostA sends its first HTTP request to WWW_server, no hosts file. With which devices does it establish a TCP connection? | **Only WWW_server** (D) | Not Default_GW (it only forwards). Not DNS_server: standard DNS queries use UDP, no TCP connection. HTTP uses TCP port 80, so a TCP connection with the web server. |
