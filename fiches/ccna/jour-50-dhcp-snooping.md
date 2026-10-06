# CCNA Day 50 : DHCP Snooping

> Source : Jeremy's IT Lab, « Free CCNA | DHCP Snooping | Day 50 » (28 min, vidéo n°101 de la playlist, cours) et « Free CCNA | DHCP Snooping | Day 50 Lab » (16 min, vidéo n°102, lab). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

Sujet d'examen 5.7 (fonctions de sécurité de couche 2 : DHCP snooping, dynamic ARP inspection, port security). Deuxième des trois vidéos.

### 1. Qu'est-ce que le DHCP snooping ?

- Fonction de sécurité des switches qui **filtre les messages DHCP reçus sur les ports non fiables** (*untrusted ports*). Seuls les messages DHCP sont filtrés ; les autres messages ne sont pas affectés.
- **Tous les ports sont untrusted par défaut** ; l'administrateur configure les ports fiables (*trusted*). En général : **ports uplink = trusted** (vers l'infrastructure réseau que l'administrateur contrôle, par exemple R1 serveur DHCP ou agent relais), **ports downlink = untrusted** (vers les hôtes finaux, que l'administrateur ne contrôle pas ; un utilisateur malveillant pourrait lancer une attaque DHCP).
- Sur un port trusted, le switch **n'inspecte pas** et transmet normalement. Sur un port untrusted, il inspecte et décide de transmettre ou de jeter.
- Exemple : DISCOVER de PC1 inspecté par SW1 (port untrusted), transmis ; inspecté par SW2, transmis à R1 ; la réponse de R1 revient **sans inspection** car reçue sur des ports trusted. Un message de PC2 jugé non conforme est jeté par SW1.

### 2. Attaques contre lesquelles le DHCP snooping protège

- **DHCP starvation / exhaustion** : l'attaquant inonde le serveur de DISCOVER avec des **MAC usurpées** ; le pool se remplit, déni de service pour les autres clients. Détail : le message DHCP contient un champ **CHADDR** (*Client Hardware Address*) indiquant la MAC du client. Il est nécessaire parce que, si le serveur DHCP est distant et que les messages passent par un **agent relais**, la MAC source de la trame reçue par le serveur n'est plus celle du client.
- **DHCP poisoning** (attaque de **l'homme du milieu**, comme l'ARP poisoning) : un **serveur DHCP illégitime** (*spurious DHCP server*) répond aux DISCOVER et attribue des adresses, mais donne **sa propre adresse comme passerelle par défaut**. Les clients acceptent en général **la première OFFER reçue** ; si le serveur légitime est distant (R1 simple agent relais), l'OFFER de l'attaquant, local, arrive presque sûrement en premier. Déroulé : PC1 DISCOVER (broadcast), OFFER de l'attaquant arrive avant celle de R1, PC1 envoie **DECLINE** à R1 et termine le DORA avec l'attaquant : IP 172.16.1.10, passerelle 172.16.1.2 (l'attaquant). Le trafic vers l'extérieur passe par l'attaquant, qui l'examine ou le modifie avant de le transmettre à la vraie passerelle ; PC1 ne remarque rien.

### 3. Types de messages DHCP : serveur ou client

| Envoyés par le **serveur** | Envoyés par le **client** |
| :--- | :--- |
| **OFFER**, **ACK** (échange DORA), **NAK** (contraire d'ACK : refuse la REQUEST d'un client) | **DISCOVER**, **REQUEST** (DORA), **RELEASE** (le client n'a plus besoin de son adresse), **DECLINE** (refuse l'adresse offerte par un serveur) |

Il est important de savoir quels messages viennent du serveur et lesquels viennent du client.

### 4. Fonctionnement du filtrage

1. Message DHCP reçu sur un port **trusted** : transmis sans inspection, jamais jeté.
2. Message reçu sur un port **untrusted** :
   - **Message serveur (OFFER, ACK, NAK) : jeté sans autre vérification.** Les serveurs DHCP ne doivent pas être sur des ports untrusted.
   - **Message client** : vérifications selon le type :
     - **DISCOVER et REQUEST** : la **MAC source de la trame** doit correspondre au champ **CHADDR** du message DHCP. Correspondance : transmis ; sinon jeté. Protège contre l'usurpation du CHADDR, mais pas parfait : l'attaquant peut aussi usurper la MAC source de la trame.
     - **RELEASE et DECLINE** : l'**adresse IP source** du paquet et l'**interface de réception** doivent correspondre à l'entrée de la **table de bindings DHCP snooping** (*DHCP snooping binding table*). Correspondance : transmis ; sinon jeté. Empêche un attaquant d'envoyer ces messages au nom d'autres hôtes pour faire croire au serveur qu'ils n'ont plus besoin de leur adresse.
- **Table de bindings** : créée par le switch quand DHCP snooping est activé ; une entrée par client qui obtient un bail : **adresse MAC, adresse IP, durée de bail, VLAN, interface**. `show ip dhcp snooping binding`.

### 5. Configuration de base

- `ip dhcp snooping` active la fonction **globalement**, mais ce n'est pas suffisant : `ip dhcp snooping vlan 1` l'active **par VLAN** (un seul VLAN dans l'exemple ; répéter pour chaque VLAN nécessaire).
- `no ip dhcp snooping information option` : voir section 7.
- `ip dhcp snooping trust` sur l'interface vers le serveur DHCP (G0/0 de SW2 vers R1 ; G0/0 de SW1 vers R1). Tous les ports sont untrusted par défaut.

### 6. Limitation de débit (*rate-limiting*)

- `ip dhcp snooping limit rate 1` sur une interface limite les messages DHCP à **1 par seconde** ; au-delà, l'interface passe en **err-disabled**. 1/s est trop bas pour un réseau réel (même un échange légitime désactiverait le port) ; choisi pour la démonstration.
- Réactivation : `shutdown` puis `no shutdown`, ou errdisable recovery : `errdisable recovery cause dhcp-rate-limit` ; `show errdisable recovery` montre la cause activée et G0/1 en attente d'expiration du timer.
- Utilité : l'attaquant peut usurper à la fois la MAC source de la trame et le CHADDR pour contourner la vérification des DISCOVER/REQUEST, mais le rate-limiting l'empêche d'épuiser le serveur : son interface est désactivée.

### 7. Option 82 (*DHCP relay agent information option*)

- Une des nombreuses options DHCP : informations sur **l'agent relais** qui a reçu le message du client (interface, VLAN…), ajoutées par les agents relais aux messages transmis à un serveur distant.
- Avec DHCP snooping, les switches Cisco **ajoutent l'option 82 par défaut** aux messages clients, même s'ils ne sont pas agents relais. Et par défaut, ils **jettent les messages avec option 82 reçus sur un port untrusted**. Exemple : SW1 ajoute l'option 82 au DISCOVER de PC1 ; SW2 le reçoit sur un port untrusted et le jette (message Syslog).
- Avec `no ip dhcp snooping information option` sur SW1 seulement : SW1 n'ajoute plus l'option, mais SW2 l'ajoute avant de transmettre à R1, qui jette le message : log « inconsistent relay information » (un message qui ne vient pas d'un agent relais ne devrait pas avoir l'option 82). Il faut la commande sur **les deux switches** : R1 répond alors normalement.
- Les réglages par défaut conviennent si le switch est un switch de couche 3 agent relais ; sinon il faut cette commande. Peut-être pas à l'examen, mais indispensable dans les labs.

### 8. Pièges d'examen

- Deux commandes pour activer : **globalement** (`ip dhcp snooping`) **et par VLAN** (`ip dhcp snooping vlan`).
- Les messages **serveur (OFFER, ACK, NAK)** reçus sur un port untrusted sont **toujours jetés**.
- DISCOVER/REQUEST : vérification **MAC source de la trame = CHADDR**. RELEASE/DECLINE : vérification **IP source + interface = table de bindings**.
- La table de bindings contient MAC, IP, bail, VLAN, interface ; **pas la passerelle par défaut**.
- Le DHCP snooping ne filtre **pas tous** les messages DHCP, seulement ceux reçus sur des **ports untrusted**.
- Dépassement du rate limit = **interface désactivée** (err-disabled).
- **Option 82** : penser à `no ip dhcp snooping information option` quand le switch n'est pas agent relais.

### 9. Commandes IOS

```
SW1(config)# ip dhcp snooping                        ! active DHCP snooping globalement
SW1(config)# ip dhcp snooping vlan 1                 ! l'active sur le VLAN 1 (obligatoire, par VLAN)
SW1(config)# no ip dhcp snooping information option  ! ne pas ajouter l'option 82 (switch non agent relais)
SW1(config)# interface g0/0
SW1(config-if)# ip dhcp snooping trust               ! port fiable (uplink vers le serveur DHCP) ; tous untrusted par défaut
SW1(config-if)# ip dhcp snooping limit rate 1        ! limite à 1 message DHCP par seconde, sinon err-disabled
SW1(config)# errdisable recovery cause dhcp-rate-limit   ! récupération automatique après dépassement du débit
SW1# show ip dhcp snooping binding                   ! table de bindings : MAC, IP, bail, VLAN, interface
SW1# show errdisable recovery                        ! causes activées et interfaces en attente
```

### 10. Le lab : DHCP Snooping

- **Topologie** identique au cours : PC1, PC2, PC3 derrière SW2, SW2 relié à SW1 (G0/1 de SW2, G0/1 de SW1), SW1 relié à R1 par G0/2. Un seul VLAN.
- **R1 serveur DHCP** :

```
R1(config)# ip dhcp excluded-address 192.168.1.1 192.168.1.9   ! hors du pool
R1(config)# ip dhcp pool POOL1
R1(dhcp-config)# network 192.168.1.0 255.255.255.0
R1(dhcp-config)# default-router 192.168.1.1
```

- **SW1** : `ip dhcp snooping`, `ip dhcp snooping vlan 1`, `interface g0/2`, `ip dhcp snooping trust` (port vers R1). **SW2** : `ip dhcp snooping`, `ip dhcp snooping vlan 1`, `interface g0/1`, `ip dhcp snooping trust` (uplink vers R1).
- **Test** : `ipconfig /renew` sur PC1 **échoue**. En mode simulation, le message DHCP va à SW2 puis SW1 et s'arrête. Dans « Inbound PDU Details » sur SW1 : **DHCP Agent Information Option** ajoutée par SW2 ; SW1 l'a reçue sur un port untrusted et l'a jetée. Syslog sur SW1 : « option82 value on untrusted port ».
- **Correction** : `no ip dhcp snooping information option` sur **SW1 et SW2**. `ipconfig /renew` fonctionne : PC1 obtient une adresse.
- Conclusion : configuration simple ; la seule difficulté est de **penser à désactiver l'option 82**.

### 11. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quels types de messages DHCP sont toujours jetés s'ils arrivent sur une interface untrusted ? (trois réponses) | **C** NAK, **D** OFFER, **G** ACK | Ce sont les messages envoyés par les **serveurs** DHCP, qui ne doivent pas être connectés à des interfaces untrusted. |
| Qu'est-ce qui n'est PAS stocké dans la base de bindings DHCP snooping ? | **D** : la passerelle par défaut | La table affiche MAC, IP, bail, VLAN, interface ; pas la passerelle. |
| Quelles sont des fonctions du DHCP snooping ? (deux réponses) | **A** : limiter le débit des messages DHCP ; **C** : filtrer les messages sur les ports untrusted | Il ne filtre pas les messages sur les ports trusted, ni **tous** les messages DHCP. |
| Que vérifie DHCP snooping sur un DISCOVER reçu sur une interface untrusted ? (deux réponses) | **A** : l'adresse MAC source ; **B** : le client hardware address | MAC source de la trame Ethernet et champ CHADDR du message DHCP : s'ils correspondent, le message passe ; sinon il est jeté. |
| Rate-limiting configuré sur G0/1 : que se passe-t-il si les messages DHCP dépassent la limite ? | **B** : l'interface est désactivée | Réactivation par `shutdown`/`no shutdown` ou errdisable recovery pour la cause dhcp-rate-limit. |

---

## 🇬🇧 English version

Exam topic 5.7 (Layer 2 security features: DHCP snooping, dynamic ARP inspection, port security). Second of three videos.

### 1. What is DHCP snooping?

- A switch security feature that **filters DHCP messages received on untrusted ports**. Only DHCP messages are filtered; other messages are unaffected.
- **All ports are untrusted by default**; the admin configures which ports are trusted. Usually: **uplink ports = trusted** (pointing toward network infrastructure the admin controls, e.g. R1 as DHCP server or relay agent), **downlink ports = untrusted** (pointing toward end hosts, which the admin does not control; a malicious user could launch a DHCP-based attack).
- On a trusted port the switch **does not inspect** and forwards as normal. On an untrusted port it inspects and decides to forward or discard.
- Example: PC1's DISCOVER is inspected by SW1 (untrusted port), forwarded; inspected by SW2, forwarded to R1; R1's reply comes back **without inspection** because it arrives on trusted ports. A message from PC2 judged not OK is discarded by SW1.

### 2. Attacks DHCP snooping protects against

- **DHCP starvation / exhaustion**: the attacker floods DISCOVER messages with **spoofed MACs**; the pool fills up, denial of service to other clients. Detail: the DHCP message has a **CHADDR** (Client Hardware Address) field holding the client's MAC. It is needed because, if the DHCP server is remote and messages go through a **relay agent**, the source MAC of the frame received by the server is no longer the client's.
- **DHCP poisoning** (a **man-in-the-middle** attack, like ARP poisoning): a **spurious (illegitimate) DHCP server** replies to DISCOVERs and assigns addresses, but makes clients use **its own IP as default gateway**. Clients usually accept **the first OFFER received**; if the legitimate server is remote (R1 only a relay agent), the attacker's local OFFER almost certainly arrives first. Flow: PC1 DISCOVER (broadcast), attacker's OFFER arrives before R1's, PC1 sends **DECLINE** to R1 and completes DORA with the attacker: IP 172.16.1.10, gateway 172.16.1.2 (the attacker). External traffic goes through the attacker, who examines or modifies it before forwarding to the real gateway; PC1 notices nothing.

### 3. DHCP message types: server or client

| Sent by the **server** | Sent by the **client** |
| :--- | :--- |
| **OFFER**, **ACK** (DORA exchange), **NAK** (opposite of ACK: declines a client's REQUEST) | **DISCOVER**, **REQUEST** (DORA), **RELEASE** (client no longer needs its address), **DECLINE** (declines the address offered by a server) |

Make sure you learn which messages are sent by servers and which by clients.

### 4. How the filtering works

1. DHCP message received on a **trusted** port: forwarded without inspection, never dropped.
2. Message received on an **untrusted** port:
   - **Server message (OFFER, ACK, NAK): discarded with no further checks.** DHCP servers should not be on untrusted ports.
   - **Client message**: checks depend on the type:
     - **DISCOVER and REQUEST**: the **frame's source MAC** must match the DHCP message's **CHADDR** field. Match: forward; otherwise discard. Protects against CHADDR spoofing, but not perfect: the attacker can spoof the frame's source MAC too.
     - **RELEASE and DECLINE**: the packet's **source IP** and the **receiving interface** must match the entry in the **DHCP snooping binding table**. Match: forward; otherwise discard. Prevents an attacker from sending these messages on behalf of other hosts to make the server think they no longer need their addresses.
- **Binding table**: built by the switch when DHCP snooping is enabled; one entry per client that successfully leases an address: **MAC address, IP address, lease time, VLAN, interface**. `show ip dhcp snooping binding`.

### 5. Basic configuration

- `ip dhcp snooping` enables the feature **globally**, but that is not enough: `ip dhcp snooping vlan 1` enables it **per VLAN** (only one VLAN in the example; repeat for each VLAN needed).
- `no ip dhcp snooping information option`: see section 7.
- `ip dhcp snooping trust` on the interface toward the DHCP server (SW2's G0/0 to R1; SW1's G0/0 to R1). All ports are untrusted by default.

### 6. Rate limiting

- `ip dhcp snooping limit rate 1` on an interface limits DHCP messages to **1 per second**; above that, the interface is **err-disabled**. 1/s is too low for a real network (even legitimate exchanges would disable the port); chosen for the demo.
- Re-enable: `shutdown` then `no shutdown`, or errdisable recovery: `errdisable recovery cause dhcp-rate-limit`; `show errdisable recovery` shows the cause enabled and G0/1 waiting for the timer.
- Purpose: an attacker can spoof both the frame's source MAC and the CHADDR to bypass the DISCOVER/REQUEST check, but rate limiting stops them exhausting the server: their interface is disabled.

### 7. Option 82 (DHCP relay agent information option)

- One of many DHCP options: information about **the relay agent** that received the client's message (interface, VLAN...), added by relay agents to messages forwarded to a remote server.
- With DHCP snooping enabled, Cisco switches **add Option 82 by default** to client messages, even when not acting as relay agents. And by default they **drop messages with Option 82 received on an untrusted port**. Example: SW1 adds Option 82 to PC1's DISCOVER; SW2 receives it on an untrusted port and drops it (Syslog message).
- With `no ip dhcp snooping information option` on SW1 only: SW1 no longer adds the option, but SW2 adds it before forwarding to R1, which drops the message: log "inconsistent relay information" (a message not sent by a relay agent should not have Option 82). The command is needed on **both switches**: R1 then responds normally.
- Default settings work if the switch is a Layer 3 switch acting as relay agent; otherwise this command is needed. Maybe not on the exam, but essential in labs.

### 8. Exam traps

- Two commands to enable: **globally** (`ip dhcp snooping`) **and per VLAN** (`ip dhcp snooping vlan`).
- **Server messages (OFFER, ACK, NAK)** received on an untrusted port are **always discarded**.
- DISCOVER/REQUEST: check **frame source MAC = CHADDR**. RELEASE/DECLINE: check **source IP + interface = binding table**.
- The binding table holds MAC, IP, lease, VLAN, interface; **not the default gateway**.
- DHCP snooping does **not filter all** DHCP messages, only those received on **untrusted ports**.
- Exceeding the rate limit = **interface disabled** (err-disabled).
- **Option 82**: remember `no ip dhcp snooping information option` when the switch is not a relay agent.

### 9. IOS commands

```
SW1(config)# ip dhcp snooping                        ! enable DHCP snooping globally
SW1(config)# ip dhcp snooping vlan 1                 ! enable it on VLAN 1 (required, per VLAN)
SW1(config)# no ip dhcp snooping information option  ! do not add Option 82 (switch is not a relay agent)
SW1(config)# interface g0/0
SW1(config-if)# ip dhcp snooping trust               ! trusted port (uplink toward the DHCP server); all untrusted by default
SW1(config-if)# ip dhcp snooping limit rate 1        ! limit to 1 DHCP message per second, else err-disabled
SW1(config)# errdisable recovery cause dhcp-rate-limit   ! automatic recovery after rate limit violation
SW1# show ip dhcp snooping binding                   ! binding table: MAC, IP, lease, VLAN, interface
SW1# show errdisable recovery                        ! enabled causes and interfaces waiting
```

### 10. The lab: DHCP Snooping

- **Topology** same as the lecture: PC1, PC2, PC3 behind SW2, SW2 connected to SW1 (SW2's G0/1, SW1's G0/1), SW1 connected to R1 via G0/2. One VLAN.
- **R1 as DHCP server**:

```
R1(config)# ip dhcp excluded-address 192.168.1.1 192.168.1.9   ! outside the pool
R1(config)# ip dhcp pool POOL1
R1(dhcp-config)# network 192.168.1.0 255.255.255.0
R1(dhcp-config)# default-router 192.168.1.1
```

- **SW1**: `ip dhcp snooping`, `ip dhcp snooping vlan 1`, `interface g0/2`, `ip dhcp snooping trust` (port to R1). **SW2**: `ip dhcp snooping`, `ip dhcp snooping vlan 1`, `interface g0/1`, `ip dhcp snooping trust` (uplink toward R1).
- **Test**: `ipconfig /renew` on PC1 **fails**. In simulation mode, the DHCP message goes to SW2 then SW1 and stops. In "Inbound PDU Details" on SW1: **DHCP Agent Information Option** added by SW2; SW1 received it on an untrusted port and discarded it. Syslog on SW1: "option82 value on untrusted port".
- **Fix**: `no ip dhcp snooping information option` on **SW1 and SW2**. `ipconfig /renew` works: PC1 gets an address.
- Conclusion: simple to configure; the only tricky part is **remembering to disable Option 82**.

### 11. The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which DHCP message types are always discarded if received on an untrusted interface? (select three) | **C** NAK, **D** OFFER, **G** ACK | They are sent by DHCP **servers**, which should not be connected to untrusted interfaces. |
| Which is NOT stored in the DHCP snooping binding database? | **D**: default gateway | The table shows MAC, IP, lease, VLAN, interface; no gateway. |
| Which are functions of DHCP snooping? (select two) | **A**: limiting the rate of DHCP messages; **C**: filtering messages on untrusted ports | It does not filter messages on trusted ports, nor **all** DHCP messages. |
| What does DHCP snooping check on a DISCOVER received on an untrusted interface? (select two) | **A**: source MAC address; **B**: client hardware address | Source MAC of the Ethernet frame and CHADDR field of the DHCP message: if they match, the message is permitted; otherwise discarded. |
| Rate limiting configured on G0/1: what happens if DHCP messages exceed the limit? | **B**: the interface is disabled | Re-enable with `shutdown`/`no shutdown` or errdisable recovery for the dhcp-rate-limit cause. |
