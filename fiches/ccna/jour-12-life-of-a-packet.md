# CCNA Day 12 : The Life of a Packet / La vie d'un paquet

> Source : Jeremy's IT Lab, « Free CCNA | The Life of a Packet | Day 12 » (20 min), vidéo n°23 de la playlist (cours, sans configuration), et « Life of a Packet | Day 12 Lab » (16 min), vidéo n°24 (lab Packet Tracer en mode simulation, sans configuration). Pas de deck Anki pour ce jour : Jeremy n'y apporte aucune information nouvelle. Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Objectif de la vidéo

Suivre **tout le parcours d'un paquet** envoyé vers un réseau distant : **ARP**, **encapsulation** et **désencapsulation**, à un niveau suffisant pour le CCNA (pas CCNP ou CCIE). Presque rien n'est nouveau : il s'agit d'**assembler les pièces** des vidéos précédentes.

### 2. La topologie et les adresses MAC

Même topologie que le Day 11 (routage statique), avec des routes statiques pré-configurées pour que le paquet suive le chemin **PC1 → R1 → R2 → R4 → PC4** (le chemin via R3 serait valable aussi). On suit un paquet de PC1 (192.168.1.0/24) vers PC4 (192.168.4.0/24).

Les MAC sont abrégées à 4 caractères (une vraie MAC en a 12). **Chaque interface d'un équipement réseau a sa propre MAC.** Celles des switches ne sont pas utiles ici.

| Équipement / interface | IP | MAC |
| :--- | :--- | :--- |
| PC1 | 192.168.1.1 | 1111 |
| R1 G0/2 (passerelle de PC1) | 192.168.1.254 | AAAA |
| R1 G0/0 | 192.168.12.1 | BBBB |
| R2 G0/0 | 192.168.12.2 | CCCC |
| R2 G0/1 | 192.168.24.2 | DDDD |
| R4 G0/1 | 192.168.24.4 | EEEE |
| R4 G0/2 | 192.168.4.254 | **FFFE** (pas FFFF, pour ne pas confondre avec la MAC de broadcast FFFF.FFFF.FFFF) |
| PC4 | 192.168.4.1 | 4444 |

### 3. Le trajet aller, étape par étape

1. **PC1** encapsule ses données dans un en-tête IP : source 192.168.1.1, destination 192.168.4.1. Comme 192.168.4.1 n'est pas dans son réseau 192.168.1.0/24, il doit envoyer à sa **passerelle par défaut** R1. Il n'a encore rien envoyé : il lui faut la MAC de R1 → **ARP**.
   - **Requête ARP** : IP source PC1, IP destination 192.168.1.254 ; MAC destination **FFFF.FFFF.FFFF** (broadcast, MAC de R1 inconnue), MAC source 1111. En clair : « Bonjour 192.168.1.254, quelle est ta MAC ? ». Remarque : dans l'en-tête IPv4 la source vient avant la destination, dans l'en-tête Ethernet c'est la **destination qui vient d'abord**.
   - SW1 reçoit le broadcast et le diffuse sur tous ses ports sauf celui d'arrivée (ici seulement G0/0 vers R1) ; il **apprend la MAC de PC1** sur G0/1.
   - R1 voit que l'IP destination est la sienne et renvoie une **réponse ARP en unicast** (il connaît déjà l'IP et la MAC de PC1 grâce à la requête) : « Bonjour 192.168.1.1, ici 192.168.1.254, ma MAC est AAAA ». SW1 apprend la MAC de R1 sur G0/0.
   - PC1 encapsule le paquet : MAC destination AAAA, source 1111. **Le paquet n'est pas modifié** : l'IP destination reste celle de PC4, pas celle de R1. Seule la couche 2 vise R1.
2. **R1** retire l'en-tête Ethernet, cherche la route la plus spécifique : **192.168.4.0/24 via 192.168.12.2**. Il ne connaît pas la MAC de R2 → **ARP** : requête de 192.168.12.1 (MAC BBBB) vers 192.168.12.2, broadcast ; réponse unicast de R2 : « ma MAC est CCCC ». R1 ré-encapsule : destination CCCC, source BBBB.
3. **R2** retire l'en-tête, route la plus spécifique : **192.168.4.0/24 via 192.168.24.4**. Le réseau 192.168.24.0/24 est connecté, mais la MAC de R4 est inconnue → **ARP** par G0/1 ; réponse « ma MAC est EEEE ». Ré-encapsulation : destination EEEE, source DDDD.
4. **R4** retire l'en-tête, route la plus spécifique : **192.168.4.0/24, directement connecté par G0/2**. MAC de PC4 inconnue → **ARP** par G0/2 (SW4 apprend la MAC de R4 sur G0/0) ; réponse unicast de PC4 : « Bonjour 192.168.4.254, ici 192.168.4.1, ma MAC est 4444 » (SW4 apprend la MAC de PC4 sur G0/1). Ré-encapsulation : destination 4444, source FFFE. Le paquet arrive à **PC4**.

### 4. Ce qu'il faut retenir du trajet

- Le **paquet d'origine ne change jamais** : même en-tête IP, source 192.168.1.1 et destination 192.168.4.1, de bout en bout.
- Les **switches ne modifient pas les trames** : ils les transmettent et apprennent les MAC, sans désencapsuler ni ré-encapsuler.
- Chaque **routeur** désencapsule, consulte sa table de routage, puis ré-encapsule avec **sa propre MAC en source** et **la MAC du prochain saut en destination**.
- Chaque réponse ARP est **unicast**, parce que la requête contenait déjà l'IP et la MAC de l'émetteur.
- **Trajet retour** (PC4 → PC1 par le même chemin, R4, R2, R1) : la grande différence est qu'**il n'y a plus d'ARP**, tous les équipements ont déjà fait le processus ; le paquet est simplement désencapsulé et ré-encapsulé à chaque routeur.

### Pièges d'examen

- Hôte final vers un **réseau distant** : la MAC destination est celle de la **passerelle par défaut**, pas celle de l'hôte distant. Vers le **même réseau** : la MAC destination est directement celle de l'hôte.
- **IP source et destination inchangées** sur tout le trajet ; **MAC source et destination changent à chaque routeur**.
- Un **switch n'insère jamais sa propre MAC** dans une trame qu'il transmet.
- Requête ARP = broadcast (FFFF.FFFF.FFFF) ; réponse ARP = unicast.
- Les premiers pings vers une nouvelle destination peuvent **expirer** le temps que l'ARP se fasse sur chaque tronçon ; sous Windows, `ping` envoie **4 pings** par défaut.
- Dans `show interfaces`, l'adresse affichée peut différer de la **BIA** (*burned-in address*) : la BIA est la MAC attribuée par le fabricant, mais une MAC différente peut être **configurée** avec `mac-address` et c'est elle qui est utilisée.

### Commandes IOS

```text
PC> ping 192.168.3.1                     ! Windows : 4 pings par défaut ; les premiers expirent le temps de l'ARP
PC> ipconfig /all                        ! Windows : « Physical Address » de FastEthernet0 = la MAC du PC
R1# show interface g0/0                  ! « address is 0000.01aa.aaaa (bia …) » : MAC utilisée, puis MAC d'usine
R1# show running-config                  ! sous l'interface : mac-address <MAC> si une MAC a été configurée
R1(config-if)# mac-address 0000.01aa.aaaa   ! configurer une MAC différente de la BIA (fait par Jeremy pour la lisibilité)
```

### Le lab (vidéo n°24)

**Objectif** : aucune configuration ; identifier les **MAC source et destination** à chaque point du trajet, puis vérifier dans le **mode simulation** de Packet Tracer. Topologie : PC1 et PC3 dans 192.168.1.0/24 (SW1), PC4 = 192.168.3.1 dans 192.168.3.0/24 (SW2), chemin **PC1 → SW1 → R1 → R2 → R3 → SW2 → PC4**. Les IP source et destination ne changeront jamais (192.168.1.1 → 192.168.3.1). Les réponses se donnent par équipement et interface (par exemple « R1 G0/1 »).

**Question 1 : PC1 pingue PC4.**

| Segment | MAC source | MAC destination |
| :--- | :--- | :--- |
| A. PC1 → SW1 | PC1 (…1111) | R1 G0/0, passerelle de PC1 (…aaaa) |
| B. SW1 → R1 | identique : SW1 ne change rien, il apprend la MAC de PC1 et transmet (ou inonde) | identique |
| C. R1 → R2 | R1 G0/1 (…bbbb) | R2 G0/0, prochain saut (…cccc) |
| D. R2 → R3 | R2 G0/1 (…dddd) | R3 G0/0 (…eeee) |
| E. R3 → SW2 | R3 G0/1 (…ffff) : 192.168.3.0/24 est connecté, R3 envoie directement à PC4 | PC4 (…4444) |
| F. SW2 → PC4 | identique à E | identique à E |

Méthode : d'abord un `ping 192.168.3.1` depuis PC1 (*Desktop* > *Command Prompt*) pour laisser l'ARP et l'apprentissage MAC se terminer (les premiers pings expirent ; un second `ping` réussit à 100 %). Relever les MAC : `ipconfig /all` sur PC1 (…1111), puis sur R1 `enable`, `show interface g0/0` : « address is 0000.01aa.aaaa (bia …) ». Jeremy explique l'écart : la BIA est la MAC d'usine, mais il a configuré une MAC lisible avec `mac-address` (visible dans `show running-config` sous l'interface). De même `show interface g0/1` sur R1 (…bbbb), `show interface g0/0` et `g0/1` sur R2 (…cccc, …dddd), sur R3 (…eeee, …ffff), `ipconfig /all` sur PC4 (…4444). Ensuite **Simulation Mode** (en bas à droite), nouveau ping, et avancer le paquet ICMP d'un cran avec la flèche : cliquer sur l'enveloppe montre les **IN layers** (trame reçue) et **OUT layers** (trame émise) de chaque équipement, avec la MAC source et destination en couche 2 et l'interface physique en couche 1 (sur SW1 : entrée F0/1, sortie G0/1). Chaque segment confirme le tableau.

**Question 2 : PC1 pingue PC3** (même réseau, 192.168.1.3). PC1 n'utilise pas sa passerelle : il envoie **directement** à PC3. SW1 au milieu ne change rien. Pour A (PC1 → SW1) comme pour B (SW1 → PC3) : source PC1 (…1111), destination PC3 (…3333, relevée avec `ipconfig /all` sur PC3). Vérifié en simulation : entrée sur F0/1, sortie par F0/3 de SW1.

**Question 3** : même exercice dans le **sens inverse** (PC4 vers PC1) ; Jeremy demande de poster les réponses en commentaire de la vidéo, en nommant équipement et interface, sans recopier les MAC. Non corrigée dans la vidéo.

### Le quiz (5 questions, sur le schéma du cours, trajet retour PC4 → PC1)

Pas de QCM cette fois : les questions portent sur le schéma de la section 2.

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| 1. PC4 envoie un paquet à PC1 : MAC destination à la sortie de l'interface de PC4 ? | **FFFE** (R4 G0/2) | PC1 est dans un réseau distant : PC4 envoie d'abord à sa passerelle par défaut R4, donc la MAC destination est celle de la passerelle. |
| 2. MAC source du paquet reçu sur R1 Gi0/0 ? | **CCCC** (R2 G0/0) | Quand R2 transmet vers R1, il encapsule avec sa propre MAC en source. |
| 3. MAC source du paquet émis par SW1 Gi0/1 ? | **AAAA** (R1 G0/2) | SW1 ne remplace pas la MAC par la sienne : il transmet la trame telle quelle vers le bon port (ou l'inonde). |
| 4. IP destination du paquet émis par R4 Gi0/1 ? | **192.168.1.1** (PC1) | Les routeurs changent les MAC de l'en-tête Ethernet mais ne modifient pas le paquet : l'IP destination reste celle de PC1. |
| 5. IP source du paquet reçu sur R1 Gi0/0 ? | **192.168.4.1** (PC4) | Même raison : le paquet n'est pas modifié, l'IP source reste celle de PC4 sur tout le trajet. |

---

## 🇬🇧 English version

### 1. Purpose of the video

Follow **the entire journey of a packet** sent to a remote network: **ARP**, **encapsulation** and **de-encapsulation**, at a depth suitable for the CCNA (not CCNP or CCIE). Almost nothing is new: the point is to **put the pieces together** from previous videos.

### 2. Topology and MAC addresses

Same topology as Day 11 (static routing), with static routes pre-configured so the packet follows **PC1 → R1 → R2 → R4 → PC4** (the path via R3 would be valid too). We follow a packet from PC1 (192.168.1.0/24) to PC4 (192.168.4.0/24).

MACs are shortened to 4 characters (a real MAC has 12). **Each interface on a network device has its own MAC.** The switches' MACs are not needed here.

| Device / interface | IP | MAC |
| :--- | :--- | :--- |
| PC1 | 192.168.1.1 | 1111 |
| R1 G0/2 (PC1's gateway) | 192.168.1.254 | AAAA |
| R1 G0/0 | 192.168.12.1 | BBBB |
| R2 G0/0 | 192.168.12.2 | CCCC |
| R2 G0/1 | 192.168.24.2 | DDDD |
| R4 G0/1 | 192.168.24.4 | EEEE |
| R4 G0/2 | 192.168.4.254 | **FFFE** (not FFFF, to avoid confusion with the broadcast MAC FFFF.FFFF.FFFF) |
| PC4 | 192.168.4.1 | 4444 |

### 3. The outbound journey, step by step

1. **PC1** encapsulates its data in an IP header: source 192.168.1.1, destination 192.168.4.1. Since 192.168.4.1 is not in its 192.168.1.0/24 network, it must send to its **default gateway** R1. It has not sent anything yet, so it needs R1's MAC → **ARP**.
   - **ARP request**: source IP PC1, destination IP 192.168.1.254; destination MAC **FFFF.FFFF.FFFF** (broadcast, R1's MAC unknown), source MAC 1111. In plain English: "Hi 192.168.1.254, what's your MAC address?". Note: in the IPv4 header the source comes first, in the Ethernet header the **destination comes first**.
   - SW1 receives the broadcast and forwards it out of every port except the one it arrived on (here only G0/0 to R1); it **learns PC1's MAC** on G0/1.
   - R1 sees the destination IP is its own and sends a **unicast ARP reply** (it already learned PC1's IP and MAC from the request): "Hi 192.168.1.1, this is 192.168.1.254, my MAC is AAAA". SW1 learns R1's MAC on G0/0.
   - PC1 encapsulates the packet: destination MAC AAAA, source 1111. **The packet is not changed**: the destination IP is still PC4's, not R1's. Only Layer 2 targets R1.
2. **R1** removes the Ethernet header and looks up the most specific route: **192.168.4.0/24 via 192.168.12.2**. It does not know R2's MAC → **ARP**: request from 192.168.12.1 (MAC BBBB) to 192.168.12.2, broadcast; unicast reply from R2: "my MAC is CCCC". R1 re-encapsulates: destination CCCC, source BBBB.
3. **R2** removes the header, most specific route: **192.168.4.0/24 via 192.168.24.4**. 192.168.24.0/24 is a connected network, but R4's MAC is unknown → **ARP** out of G0/1; reply "my MAC is EEEE". Re-encapsulation: destination EEEE, source DDDD.
4. **R4** removes the header, most specific route: **192.168.4.0/24, directly connected via G0/2**. PC4's MAC unknown → **ARP** out of G0/2 (SW4 learns R4's MAC on G0/0); unicast reply from PC4: "Hi 192.168.4.254, this is 192.168.4.1, my MAC is 4444" (SW4 learns PC4's MAC on G0/1). Re-encapsulation: destination 4444, source FFFE. The packet reaches **PC4**.

### 4. What to remember from the journey

- The **original packet never changes**: same IP header, source 192.168.1.1 and destination 192.168.4.1, end to end.
- **Switches do not modify frames**: they forward them and learn MACs, without de-encapsulating or re-encapsulating.
- Each **router** de-encapsulates, checks its routing table, then re-encapsulates with **its own MAC as source** and **the next hop's MAC as destination**.
- Every ARP reply is **unicast**, because the request already carried the sender's IP and MAC.
- **Return trip** (PC4 → PC1 along the same path, R4, R2, R1): the one major difference is that **there is no more ARP**, every device has already done it; the packet is simply de-encapsulated and re-encapsulated at each router.

### Exam traps

- End host to a **remote network**: the destination MAC is the **default gateway's**, not the remote host's. To the **same network**: the destination MAC is the host's directly.
- **Source and destination IPs unchanged** along the whole path; **source and destination MACs change at every router**.
- A **switch never inserts its own MAC** into a frame it forwards.
- ARP request = broadcast (FFFF.FFFF.FFFF); ARP reply = unicast.
- The first pings to a new destination may **time out** while ARP completes on each segment; on Windows, `ping` sends **4 pings** by default.
- In `show interfaces`, the displayed address can differ from the **BIA** (*burned-in address*): the BIA is the MAC assigned by the maker, but a different MAC can be **configured** with `mac-address` and that one is used.

### IOS commands

```text
PC> ping 192.168.3.1                     ! Windows: 4 pings by default; the first ones time out while ARP completes
PC> ipconfig /all                        ! Windows: "Physical Address" of FastEthernet0 = the PC's MAC
R1# show interface g0/0                  ! "address is 0000.01aa.aaaa (bia …)": MAC in use, then factory MAC
R1# show running-config                  ! under the interface: mac-address <MAC> if a MAC was configured
R1(config-if)# mac-address 0000.01aa.aaaa   ! configure a MAC different from the BIA (Jeremy did it for readability)
```

### The lab (video #24)

**Goal**: no configuration; identify the **source and destination MACs** at each point of the path, then verify in Packet Tracer's **simulation mode**. Topology: PC1 and PC3 in 192.168.1.0/24 (SW1), PC4 = 192.168.3.1 in 192.168.3.0/24 (SW2), path **PC1 → SW1 → R1 → R2 → R3 → SW2 → PC4**. The source and destination IPs will never change (192.168.1.1 → 192.168.3.1). Answers are given as device and interface (e.g. "R1 G0/1").

**Question 1: PC1 pings PC4.**

| Segment | Source MAC | Destination MAC |
| :--- | :--- | :--- |
| A. PC1 → SW1 | PC1 (…1111) | R1 G0/0, PC1's gateway (…aaaa) |
| B. SW1 → R1 | same: SW1 changes nothing, it learns PC1's MAC and forwards (or floods) | same |
| C. R1 → R2 | R1 G0/1 (…bbbb) | R2 G0/0, the next hop (…cccc) |
| D. R2 → R3 | R2 G0/1 (…dddd) | R3 G0/0 (…eeee) |
| E. R3 → SW2 | R3 G0/1 (…ffff): 192.168.3.0/24 is connected, R3 sends directly to PC4 | PC4 (…4444) |
| F. SW2 → PC4 | same as E | same as E |

Method: first a `ping 192.168.3.1` from PC1 (*Desktop* > *Command Prompt*) to let ARP and MAC learning complete (the first pings time out; a second `ping` is 100% successful). Collect the MACs: `ipconfig /all` on PC1 (…1111), then on R1 `enable`, `show interface g0/0`: "address is 0000.01aa.aaaa (bia …)". Jeremy explains the difference: the BIA is the factory MAC, but he configured a readable MAC with `mac-address` (visible in `show running-config` under the interface). Likewise `show interface g0/1` on R1 (…bbbb), `show interface g0/0` and `g0/1` on R2 (…cccc, …dddd), on R3 (…eeee, …ffff), `ipconfig /all` on PC4 (…4444). Then **Simulation Mode** (bottom right), a new ping, and step the ICMP packet forward with the arrow: clicking the envelope shows each device's **IN layers** (frame received) and **OUT layers** (frame sent), with source and destination MAC at Layer 2 and the physical interface at Layer 1 (on SW1: in on F0/1, out on G0/1). Every segment confirms the table.

**Question 2: PC1 pings PC3** (same network, 192.168.1.3). PC1 does not use its gateway: it sends **directly** to PC3. SW1 in the middle changes nothing. For both A (PC1 → SW1) and B (SW1 → PC3): source PC1 (…1111), destination PC3 (…3333, collected with `ipconfig /all` on PC3). Verified in simulation: in on F0/1, out on F0/3 of SW1.

**Question 3**: same exercise in the **reverse direction** (PC4 to PC1); Jeremy asks for answers in the video's comment section, naming device and interface, without copying the MACs. Not answered in the video.

### The quiz (5 questions, on the lecture diagram, return trip PC4 → PC1)

No multiple choice this time: the questions use the diagram from section 2.

| Question | Answer | Why |
| :--- | :--- | :--- |
| 1. PC4 sends a packet to PC1: destination MAC when it leaves PC4's interface? | **FFFE** (R4 G0/2) | PC1 is in a remote network: PC4 first sends to its default gateway R4, so the destination MAC is the gateway's. |
| 2. Source MAC when received on R1 Gi0/0? | **CCCC** (R2 G0/0) | When R2 forwards to R1, it encapsulates with its own MAC as source. |
| 3. Source MAC when sent from SW1 Gi0/1? | **AAAA** (R1 G0/2) | SW1 does not swap in its own MAC: it forwards the frame unchanged out of the right port (or floods it). |
| 4. Destination IP when sent from R4 Gi0/1? | **192.168.1.1** (PC1) | Routers change the Ethernet header's MACs but do not modify the packet: the destination IP stays PC1's. |
| 5. Source IP when received on R1 Gi0/0? | **192.168.4.1** (PC4) | Same reason: the packet is not modified, the source IP stays PC4's along the whole path. |
