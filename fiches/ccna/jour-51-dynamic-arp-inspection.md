# CCNA Day 51 : Dynamic ARP Inspection / Inspection ARP dynamique

> Source : Jeremy's IT Lab, « Free CCNA | Dynamic ARP Inspection | Day 51 » (33 min, vidéo n°103 de la playlist, cours) et « Free CCNA | Dynamic ARP Inspection | Day 51 Lab » (21 min, vidéo n°104, lab). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

Dernière des trois vidéos du sujet d'examen 5.7 (DHCP snooping, DAI, port security). **DAI** (*Dynamic ARP Inspection*) inspecte les messages ARP comme le DHCP snooping inspecte les messages DHCP.

### 1. Rappel sur ARP

- ARP sert à apprendre la **MAC** d'un appareil dont on connaît l'**IP** (passerelle par défaut, autres hôtes du LAN). Échange en deux messages : **requête** (*request*) puis **réponse** (*reply*).
- Exemple : PC1 veut envoyer une requête DNS à 8.8.8.8, hors de son réseau : il doit l'envoyer à sa passerelle 192.168.1.1 (R1), dont il ignore la MAC. Il diffuse une requête ARP (MAC de destination **broadcast, tout F**) ; tous les appareils du LAN la reçoivent.
- Dans Wireshark : le message ARP est encapsulé dans une trame Ethernet, **sans en-tête IP** (ARP reste dans le LAN, pas routé). Les champs **sender MAC / sender IP** (source) et **target MAC / target IP** (destination) sont dans le message ARP lui-même ; ils jouent un rôle dans DAI.
- R1 répond par une réponse ARP (**unicast**) ; PC1 ajoute R1 à sa table ARP. R1 avait déjà ajouté PC1 à sa table en recevant la requête.
- **Gratuitous ARP** (GARP) : réponse ARP envoyée **sans requête préalable**, à l'adresse **broadcast** (les réponses ARP normales sont unicast). Permet aux autres appareils d'apprendre la MAC de l'émetteur sans requête. Selon le fabricant, envoyé automatiquement à l'activation d'une interface, au changement d'IP ou de MAC. Les autres hôtes mettent à jour leur table ARP, les switches leur table MAC.

### 2. Qu'est-ce que DAI ?

- Fonction de sécurité des switches qui **filtre les messages ARP reçus sur les ports untrusted**. Seuls les messages ARP sont filtrés.
- **Tous les ports sont untrusted par défaut.** En général, les ports vers d'autres **équipements réseau** (switches, routeurs) sont configurés **trusted**, ceux vers les hôtes finaux restent untrusted. Le port de SW2 vers SW1 pourrait aussi rester untrusted (downlink vers les hôtes) ; les deux conceptions fonctionnent ; la documentation Cisco recommande de trust toutes les interfaces vers switches et routeurs.
- Fonctionnement : même logique que le DHCP snooping : requête de PC1 inspectée par SW1 (untrusted), transmise ; SW2 ne l'inspecte pas (trusted) ; la réponse de R1 n'est pas inspectée. Un message de PC2 qui viole les règles est jeté.

### 3. L'attaque ARP poisoning

- Comme le DHCP poisoning : l'attaquant **manipule les tables ARP** des cibles pour que le trafic lui soit envoyé. Il peut envoyer des **GARP** avec l'IP d'un autre appareil, ou répondre aux requêtes ARP légitimes des cibles.
- Exemple : PC2 (attaquant) envoie un GARP avec l'IP de la passerelle R1 (192.168.1.1) ; il est inondé dans le réseau ; tous les appareils associent 192.168.1.1 à la MAC de PC2 (R1 ne met pas sa table à jour : c'est sa propre IP). Le trafic de PC1 vers l'extérieur passe par PC2, qui peut en garder une copie, le modifier, puis le transmettre à R1. **Homme du milieu**.

### 4. Fonctionnement de DAI

- DAI inspecte les champs **sender MAC et sender IP** des messages ARP reçus sur les ports untrusted et cherche une **entrée correspondante dans la table de bindings DHCP snooping**. Correspondance : transmis ; sinon **jeté**. Pas d'inspection sur les ports trusted.
- DAI dépend donc en général du DHCP snooping. Autre option : les **ARP ACL**, qui associent manuellement IP et MAC, utiles pour les hôtes **sans DHCP** (sans entrée dans la table, tous leurs messages ARP seraient jetés).
- Vérifications supplémentaires optionnelles (`validate`), voir section 6.
- **Rate-limiting** : DHCP snooping et DAI sollicitent le **CPU** du switch ; même bloqués, les messages d'un attaquant peuvent surcharger le CPU. Le rate-limiting désactive l'interface.

### 5. Configuration de base et rate-limiting

- `ip arp inspection vlan 1` active DAI sur le VLAN (à répéter pour chaque VLAN, sinon seul le VLAN indiqué est inspecté). **Différence avec le DHCP snooping** : pas de commande d'activation globale, seulement par VLAN.
- `ip arp inspection trust` sur les interfaces fiables (G0/0 et G0/1 de SW2 ; G0/0 de SW1).
- `show ip arp inspection interfaces` : état trust de chaque interface, et réglages de rate-limiting.
- **Rate-limiting DAI vs DHCP snooping** :
  - DAI : **activé par défaut sur les ports untrusted à 15 paquets par seconde**, **désactivé sur les ports trusted**. DHCP snooping : désactivé sur toutes les interfaces par défaut.
  - DAI a un **burst interval** : X paquets par **Y secondes** ; DHCP snooping : X paquets par seconde seulement.
- `ip arp inspection limit rate 25 burst interval 2` (G0/1-2 de SW1) : 25 paquets par 2 secondes. `ip arp inspection limit rate 10` (G0/3) : burst interval optionnel, défaut **1 seconde**, donc 10 paquets par seconde.
- Le rate-limiting concerne les messages ARP **reçus** sur l'interface, pas envoyés. Dépassement : **err-disabled**. Réactivation : `shutdown`/`no shutdown` ou `errdisable recovery cause arp-inspection`.

### 6. Vérifications supplémentaires : `ip arp inspection validate`

- **dst-mac** : pour les **réponses** ARP, compare la **MAC de destination de l'en-tête Ethernet** à la **target MAC** du message ARP ; différentes : trame jetée.
- **ip** : cherche des adresses IP invalides ou inattendues dans les messages ARP : **0.0.0.0, 255.255.255.255, adresses multicast**. Sender IP vérifiée dans les requêtes et les réponses ; target IP vérifiée **seulement dans les réponses**.
- **src-mac** : compare la **MAC source de l'en-tête Ethernet** à la **sender MAC** du message ARP ; différentes : jeté.
- Ces vérifications s'ajoutent à la vérification standard (table de bindings) : un message doit **passer toutes** les vérifications configurées.
- **Point important** : chaque commande `validate` **écrase la précédente**. Après `validate dst-mac`, puis `validate ip`, puis `validate src-mac`, `show run | include validate` n'affiche que **src-mac**. Pour les trois : **une seule commande** `ip arp inspection validate ip src-mac dst-mac` (une, deux ou trois options, ordre sans importance).

### 7. ARP ACL (au-delà du CCNA, aperçu)

- SRV1 a une **IP statique** 192.168.1.100 : pas d'entrée dans la table de bindings de SW2 ; ses requêtes ARP sont jetées (log « 1 Invalid ARP Request on G0/2, vlan 1 »).
- `arp access-list ARP-ACL-1` puis `permit ip host 192.168.1.100 mac host <MAC SRV1>` ; appliquer avec `ip arp inspection filter ARP-ACL-1 vlan 1`. SRV1 peut alors envoyer ses requêtes ARP.
- `show ip arp inspection` : résumé de la configuration (validations src-mac, dst-mac, ip activées ; VLAN 1 configuré et opérationnel ; ACL ARP-ACL-1 en vigueur ; champ **Static ACL** : à « Yes », le **deny implicite** de l'ARP ACL s'applique et seule l'ACL est vérifiée, pas la table DHCP snooping ; à « No » (défaut, habituel), le deny implicite est ignoré) et statistiques : 4 messages jetés (**DHCP drops**, pas d'entrée dans la table, pings de SRV1 avant l'ACL), 1 **ACL permit** (requête de SRV1 après l'ACL).

### 8. Pièges d'examen

- Après `ip arp inspection vlan 1`, **toutes les interfaces du VLAN sont untrusted** ; trust à configurer manuellement.
- Les options de `validate` doivent être dans **une seule commande** : sinon seule la **dernière** reste.
- Rate-limiting DAI : **activé par défaut sur les ports untrusted, 15 paquets/seconde** ; burst interval possible (par exemple 45 paquets par 3 secondes = moyenne de 15/s, mais tolère des rafales : 30, puis 10, puis 0 ; 15 par 1 seconde est strict chaque seconde).
- DAI vérifie sender IP/MAC contre la **table de bindings DHCP snooping** et les **ARP ACL**.
- DAI s'active **par VLAN seulement** ; DHCP snooping globalement **et** par VLAN.
- Un GARP est une **réponse** ARP en **broadcast** sans requête ; les réponses ARP normales sont unicast.

### 9. Commandes IOS

```
SW1(config)# ip arp inspection vlan 1                       ! active DAI sur le VLAN 1 (pas de commande globale)
SW1(config)# interface g0/0
SW1(config-if)# ip arp inspection trust                     ! port fiable (vers switch/routeur) ; tous untrusted par défaut
SW1(config-if)# ip arp inspection limit rate 25 burst interval 2   ! 25 paquets ARP par 2 secondes
SW1(config-if)# ip arp inspection limit rate 10             ! 10 paquets par seconde (burst interval défaut 1 s)
SW1(config)# errdisable recovery cause arp-inspection       ! récupération automatique des ports désactivés par DAI
SW1(config)# ip arp inspection validate ip src-mac dst-mac  ! vérifications supplémentaires, en une seule commande
SW1(config)# arp access-list ARP-ACL-1                      ! ARP ACL pour les hôtes sans DHCP
SW1(config-arp-nacl)# permit ip host 192.168.1.100 mac host 0000.0000.0000   ! association IP/MAC autorisée
SW1(config)# ip arp inspection filter ARP-ACL-1 vlan 1      ! applique l'ARP ACL au VLAN 1
SW1# show ip arp inspection interfaces                      ! état trust, rate limit, burst interval par interface
SW1# show ip arp inspection                                 ! résumé de la configuration et statistiques forwarded/dropped
SW1# show run | include validate                            ! vérifier les validations actives
SW1# show errdisable recovery
```

### 10. Le lab : DAI (avec DHCP et DHCP snooping en révision)

- **Topologie** : PC1-3 derrière SW2 ; SW2 G0/1 vers SW1 G0/1 ; SW1 G0/2 vers R1. Packet Tracer ne supporte pas toutes les commandes DAI.
- **R1 serveur DHCP** : `ip dhcp excluded-address 192.168.1.1 192.168.1.9`, `ip dhcp pool POOL1`, `network 192.168.1.0 255.255.255.0`, `default-router 192.168.1.1`.
- **DHCP snooping** : sur SW1 : `ip dhcp snooping`, `ip dhcp snooping vlan 1`, `no ip dhcp snooping information option`, `interface g0/2`, `ip dhcp snooping trust` ; G0/1 laissé untrusted (plus sûr : attrape les messages qui auraient échappé à SW2 ; coûte plus de CPU). Sur SW2 : mêmes commandes, trust sur G0/1.
- **DAI sur SW2** : `ip arp inspection vlan 1` ; `ip arp inspection validate dst-mac ip src-mac` (une seule commande) ; `interface g0/1`, `ip arp inspection trust` ; `end`.
- **Vérifications SW2** : `show run` : configuration DAI et DHCP snooping en haut, G0/1 trusted pour les deux. `show ip arp inspection interfaces` : seul G0/1 trusted. **Anomalie Packet Tracer** : rate-limiting à 15 pps affiché aussi sur le port trusted, alors que la documentation Cisco et les tests de Jeremy sur switches réels et virtuels montrent qu'il est désactivé par défaut sur les ports trusted.
- **DAI sur SW1** : `ip arp inspection vlan 1` ; `ip arp inspection validate dst-mac ip src-mac` ; `interface range g0/1 - 2`, `ip arp inspection trust` ; `end`. `show run` : G0/2 trusted pour DAI et DHCP snooping, G0/1 trusted seulement pour DAI. L'essentiel : le port vers le routeur (G0/2) trusted pour les deux ; G0/1 au choix.
- **Test** : sur PC1, PC2, PC3, passer la passerelle de statique à DHCP (FastEthernet0 passe aussi en DHCP). PC1 obtient une adresse ; `ping 192.168.1.1` fonctionne (sinon, problème probable de DAI).

### 11. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Après `ip arp inspection vlan 1` sur SW1, quelle affirmation est vraie ? | **A** : toutes les interfaces du VLAN 1 sont untrusted | Comme pour DHCP snooping, tout est untrusted par défaut ; les ports fiables se configurent manuellement. |
| Après `validate dst-mac`, puis `validate ip`, puis `validate src-mac` en commandes séparées, qu'est-ce qui est vrai ? | **C** : la validation n'est activée que pour l'adresse MAC de destination (dernière commande saisie dans l'énoncé) | Chaque commande écrase la précédente ; seule la dernière reste. Pour plusieurs vérifications, une seule commande. |
| Qu'est-ce qui est vrai du rate-limiting DAI ? (deux réponses) | **B** : activé par défaut sur les ports untrusted ; **D** : 15 paquets par seconde par défaut | Contrairement au DHCP snooping. DAI permet aussi un burst interval (par exemple 50 paquets sur 3 secondes). |
| DAI compare sender IP et MAC à quoi ? (deux réponses) | **B** : la table de bindings DHCP snooping ; **D** : les ARP ACL | La table se construit automatiquement avec les baux DHCP ; les ARP ACL servent aux hôtes sans DHCP. |
| Quelles commandes limitent les messages ARP à une moyenne de 15 par seconde ? (deux réponses) | **A** : `ip arp inspection limit rate 15` ; **C** : `ip arp inspection limit rate 45 burst interval 3` | Même moyenne. 45 par 3 s tolère des rafales (30, 10, 0) ; 15 par 1 s est contrôlé strictement chaque seconde. |

---

## 🇬🇧 English version

Last of the three videos on exam topic 5.7 (DHCP snooping, DAI, port security). **DAI** (Dynamic ARP Inspection) inspects ARP messages the way DHCP snooping inspects DHCP messages.

### 1. ARP review

- ARP learns the **MAC** of a device with a known **IP** (default gateway, other LAN hosts). Two-message exchange: **request** then **reply**.
- Example: PC1 wants to send a DNS query to 8.8.8.8, outside its network: it must send it to its gateway 192.168.1.1 (R1), whose MAC it doesn't know. It broadcasts an ARP request (destination MAC **broadcast, all Fs**); every LAN device receives it.
- In Wireshark: the ARP message is encapsulated in an Ethernet frame, **no IP header** (ARP stays in the LAN, not routed). The **sender MAC / sender IP** (source) and **target MAC / target IP** (destination) fields are in the ARP message itself; they play a role in DAI.
- R1 sends an ARP reply (**unicast**); PC1 adds R1 to its ARP table. R1 already added PC1 when it received the request.
- **Gratuitous ARP** (GARP): an ARP reply sent **without a request**, to the **broadcast** MAC (standard replies are unicast). Lets other devices learn the sender's MAC without sending requests. Depending on the vendor, sent automatically when an interface is enabled, IP changes, MAC changes. Other hosts update their ARP tables, switches their MAC tables.

### 2. What is DAI?

- A switch security feature that **filters ARP messages received on untrusted ports**. Only ARP messages are filtered.
- **All ports are untrusted by default.** Typically, ports to other **network devices** (switches, routers) are configured **trusted**, ports to end hosts stay untrusted. SW2's port to SW1 could also stay untrusted (downlink toward the hosts); either design works; Cisco documentation recommends trusting all interfaces to switches and routers.
- Operation: same logic as DHCP snooping: PC1's request inspected by SW1 (untrusted), forwarded; SW2 does not inspect (trusted); R1's reply is not inspected. A message from PC2 violating the rules is discarded.

### 3. The ARP poisoning attack

- Like DHCP poisoning: the attacker **manipulates targets' ARP tables** so traffic is sent to the attacker. Can send **GARP** messages using another device's IP, or reply to targets' legitimate ARP requests.
- Example: PC2 (attacker) sends a GARP with the gateway's IP (192.168.1.1); it is flooded; all devices map 192.168.1.1 to PC2's MAC (R1 does not update: it is its own IP). PC1's external traffic goes to PC2, which can save a copy, modify it, then forward to R1. **Man in the middle**.

### 4. How DAI works

- DAI inspects the **sender MAC and sender IP** fields of ARP messages received on untrusted ports and looks for a **matching entry in the DHCP snooping binding table**. Match: forwarded; otherwise **discarded**. No inspection on trusted ports.
- So DAI usually relies on DHCP snooping. Alternative: **ARP ACLs**, which manually map IP to MAC, useful for hosts **without DHCP** (no entry in the table, so all their ARP messages would be dropped).
- Optional additional checks (`validate`), see section 6.
- **Rate limiting**: DHCP snooping and DAI require switch **CPU** work; even when blocked, an attacker's messages can overload the CPU. Rate limiting disables the interface.

### 5. Basic configuration and rate limiting

- `ip arp inspection vlan 1` enables DAI on the VLAN (repeat for each VLAN, otherwise only the specified VLAN is inspected). **Difference from DHCP snooping**: no global enable command, per VLAN only.
- `ip arp inspection trust` on trusted interfaces (SW2's G0/0 and G0/1; SW1's G0/0).
- `show ip arp inspection interfaces`: trust state of each interface and rate limiting settings.
- **DAI vs DHCP snooping rate limiting**:
  - DAI: **enabled by default on untrusted ports at 15 packets per second**, **disabled on trusted ports**. DHCP snooping: disabled on all interfaces by default.
  - DAI has a **burst interval**: X packets per **Y seconds**; DHCP snooping: X packets per second only.
- `ip arp inspection limit rate 25 burst interval 2` (SW1's G0/1-2): 25 packets per 2 seconds. `ip arp inspection limit rate 10` (G0/3): burst interval optional, default **1 second**, so 10 packets per second.
- Rate limiting applies to ARP messages **received** on the interface, not sent. Exceeded: **err-disabled**. Re-enable: `shutdown`/`no shutdown` or `errdisable recovery cause arp-inspection`.

### 6. Additional checks: `ip arp inspection validate`

- **dst-mac**: for ARP **replies**, compares the **destination MAC of the Ethernet header** to the **target MAC** in the ARP message; different: frame dropped.
- **ip**: looks for invalid or unexpected IPs in ARP messages: **0.0.0.0, 255.255.255.255, multicast addresses**. Sender IP checked in requests and replies; target IP checked **only in replies**.
- **src-mac**: compares the **source MAC of the Ethernet header** to the **sender MAC** in the ARP message; different: dropped.
- These are in addition to the standard check (binding table): a message must **pass all** configured checks.
- **Important**: each `validate` command **overwrites the previous one**. After `validate dst-mac`, then `validate ip`, then `validate src-mac`, `show run | include validate` shows only **src-mac**. For all three: **one command** `ip arp inspection validate ip src-mac dst-mac` (one, two or three options, order does not matter).

### 7. ARP ACLs (beyond the CCNA, quick look)

- SRV1 has a **static IP** 192.168.1.100: no entry in SW2's binding table; its ARP requests are dropped (log "1 Invalid ARP Request on G0/2, vlan 1").
- `arp access-list ARP-ACL-1` then `permit ip host 192.168.1.100 mac host <SRV1 MAC>`; apply with `ip arp inspection filter ARP-ACL-1 vlan 1`. SRV1 can then send ARP requests.
- `show ip arp inspection`: configuration summary (src-mac, dst-mac, ip validation enabled; VLAN 1 configured and operational; ACL ARP-ACL-1 in effect; **Static ACL** field: "Yes" means the ARP ACL's **implicit deny** takes effect and only the ACL is checked, not the DHCP snooping table; "No" (default, usual) ignores the implicit deny) and statistics: 4 messages dropped (**DHCP drops**, no table entry, SRV1's pings before the ACL), 1 **ACL permit** (SRV1's request after the ACL).

### 8. Exam traps

- After `ip arp inspection vlan 1`, **all interfaces in the VLAN are untrusted**; trust must be configured manually.
- `validate` options must be in **a single command**: otherwise only the **last** one remains.
- DAI rate limiting: **enabled by default on untrusted ports, 15 packets/second**; burst interval possible (e.g. 45 packets per 3 seconds = 15/s average but allows bursts: 30, then 10, then 0; 15 per 1 second is strictly checked each second).
- DAI checks sender IP/MAC against the **DHCP snooping binding table** and **ARP ACLs**.
- DAI is enabled **per VLAN only**; DHCP snooping globally **and** per VLAN.
- A GARP is an ARP **reply** sent as **broadcast** without a request; standard ARP replies are unicast.

### 9. IOS commands

```
SW1(config)# ip arp inspection vlan 1                       ! enable DAI on VLAN 1 (no global command)
SW1(config)# interface g0/0
SW1(config-if)# ip arp inspection trust                     ! trusted port (to switch/router); all untrusted by default
SW1(config-if)# ip arp inspection limit rate 25 burst interval 2   ! 25 ARP packets per 2 seconds
SW1(config-if)# ip arp inspection limit rate 10             ! 10 packets per second (default burst interval 1 s)
SW1(config)# errdisable recovery cause arp-inspection       ! automatic recovery for ports disabled by DAI
SW1(config)# ip arp inspection validate ip src-mac dst-mac  ! additional checks, in a single command
SW1(config)# arp access-list ARP-ACL-1                      ! ARP ACL for hosts without DHCP
SW1(config-arp-nacl)# permit ip host 192.168.1.100 mac host 0000.0000.0000   ! permitted IP/MAC mapping
SW1(config)# ip arp inspection filter ARP-ACL-1 vlan 1      ! apply the ARP ACL to VLAN 1
SW1# show ip arp inspection interfaces                      ! trust state, rate limit, burst interval per interface
SW1# show ip arp inspection                                 ! configuration summary and forwarded/dropped statistics
SW1# show run | include validate                            ! check active validations
SW1# show errdisable recovery
```

### 10. The lab: DAI (with DHCP and DHCP snooping review)

- **Topology**: PC1-3 behind SW2; SW2 G0/1 to SW1 G0/1; SW1 G0/2 to R1. Packet Tracer does not support all DAI commands.
- **R1 as DHCP server**: `ip dhcp excluded-address 192.168.1.1 192.168.1.9`, `ip dhcp pool POOL1`, `network 192.168.1.0 255.255.255.0`, `default-router 192.168.1.1`.
- **DHCP snooping**: on SW1: `ip dhcp snooping`, `ip dhcp snooping vlan 1`, `no ip dhcp snooping information option`, `interface g0/2`, `ip dhcp snooping trust`; G0/1 left untrusted (more secure: catches messages that slipped past SW2; costs more CPU). On SW2: same commands, trust on G0/1.
- **DAI on SW2**: `ip arp inspection vlan 1`; `ip arp inspection validate dst-mac ip src-mac` (single command); `interface g0/1`, `ip arp inspection trust`; `end`.
- **SW2 verification**: `show run`: DAI and DHCP snooping config at the top, G0/1 trusted for both. `show ip arp inspection interfaces`: only G0/1 trusted. **Packet Tracer anomaly**: rate limiting at 15 pps also shown on the trusted port, whereas Cisco documentation and Jeremy's tests on real and virtual switches show it disabled by default on trusted ports.
- **DAI on SW1**: `ip arp inspection vlan 1`; `ip arp inspection validate dst-mac ip src-mac`; `interface range g0/1 - 2`, `ip arp inspection trust`; `end`. `show run`: G0/2 trusted for DAI and DHCP snooping, G0/1 trusted for DAI only. Key point: the port to the router (G0/2) trusted for both; G0/1 is up to you.
- **Test**: on PC1, PC2, PC3, change the gateway setting from static to DHCP (FastEthernet0 switches to DHCP too). PC1 gets an address; `ping 192.168.1.1` works (if not, DAI is the likely problem).

### 11. The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| After `ip arp inspection vlan 1` on SW1, which statement is true? | **A**: all interfaces in VLAN 1 are untrusted | As with DHCP snooping, everything is untrusted by default; trusted ports are configured manually. |
| After `validate dst-mac`, then `validate ip`, then `validate src-mac` as separate commands, what is true? | **C**: DAI validation is only enabled for destination MAC addresses (the last command entered in the question) | Each command overwrites the previous one; only the last remains. For multiple checks, use a single command. |
| Which are true about DAI rate limiting? (select two) | **B**: enabled on untrusted ports by default; **D**: 15 packets per second by default | Unlike DHCP snooping. DAI also allows a burst interval (e.g. 50 packets over 3 seconds). |
| DAI checks sender IP and MAC against what? (select two) | **B**: DHCP snooping binding table; **D**: ARP ACLs | The table is built automatically from DHCP leases; ARP ACLs serve hosts without DHCP. |
| Which commands limit ARP messages to an average of 15 per second? (select two) | **A**: `ip arp inspection limit rate 15`; **C**: `ip arp inspection limit rate 45 burst interval 3` | Same average. 45 per 3 s allows bursts (30, 10, 0); 15 per 1 s is strictly checked every second. |
