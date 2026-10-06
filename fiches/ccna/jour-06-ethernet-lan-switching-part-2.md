# CCNA Day 6 : Ethernet LAN Switching (Part 2) / Commutation Ethernet, partie 2

> Source : Jeremy's IT Lab, « Free CCNA | Ethernet LAN Switching (Part 2) | Day 6 » (34 min), vidéo n°11 de la playlist (cours) ; « Analyzing Ethernet Switching | Day 6 Lab » (10 min), vidéo n°12 (lab Packet Tracer, couvre les jours 5 et 6). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Compléments sur la trame Ethernet

- **Préambule + SFD ne sont généralement pas comptés dans l'en-tête Ethernet**, bien qu'envoyés avec chaque trame. L'en-tête se réduit alors à **destination, source, type** ; **en-tête + remorque (FCS) = 18 octets**.
- **Taille minimale d'une trame : 64 octets**, charge utile (le paquet) comprise, préambule et SFD exclus. 64 − 18 = **46 octets de charge utile minimum**.
- Charge utile plus petite → ajout d'octets de **bourrage** (*padding*), tous à **0**. Exemple : paquet de 34 octets → **12 octets** de bourrage.

### 2. Topologie du jour

PC1, PC2 sur SW1 ; PC3, PC4 sur SW2 ; interfaces **G0/0, G0/1, G0/2** (GigabitEthernet). MAC réalistes avec l'OUI **0C2F.B0** commun (même fabricant) ; Jeremy ne cite que les 4 derniers caractères : PC1 = **9D00**, PC2 = **6200**. Réseau **192.168.1.0/24** : PC1 = 192.168.1.1, PC2 = .2, PC3 = .3, PC4 = .4 (détail des IP dans une vidéo ultérieure).

Une trame ne porte pas que des MAC : elle encapsule un **paquet IP** avec IP source et destination. **L'utilisateur saisit l'IP de destination, pas la MAC** ; or les switches sont des équipements de **couche 2** qui travaillent avec les MAC. PC1 doit donc **découvrir la MAC de PC3** avant d'envoyer : c'est le rôle d'**ARP**.

### 3. ARP, Address Resolution Protocol

- Sert à **découvrir l'adresse de couche 2 (MAC) correspondant à une adresse de couche 3 (IP) connue**.
- Deux messages : **ARP request** (envoyée par celui qui veut la MAC) et **ARP reply** (envoyée par le propriétaire de l'IP).
- **ARP request = trame broadcast** (vers tous les hôtes du réseau) : MAC de destination **FFFF.FFFF.FFFF**, l'**adresse broadcast**. IP source/destination et MAC source sont celles de la trame finale.
- **ARP reply = unicast**, directement au demandeur, car sa MAC figurait en source de la requête.

Déroulement PC1 → PC3 :

1. SW1 reçoit la requête, **apprend la MAC de PC1** (adresse dynamique) et, destination = tout F, l'envoie sur **toutes les interfaces sauf celle de réception** (G0/1, G0/2 ; pas G0/0), comme une unicast inconnue.
2. **PC2 ignore** la requête : l'**IP de destination** ne correspond pas à la sienne.
3. SW2 apprend PC1 sur **G0/2** et diffuse sur G0/0 et G0/1. PC4 ignore ; **PC3 reconnaît son IP** et envoie l'**ARP reply** (IP et MAC source de PC3, destination PC1).
4. SW2 apprend PC3 sur **G0/0** ; destination connue → **unicast connue, transmise** sur G0/2 (pas d'inondation). SW1 transmet sur G0/0. PC1 ajoute PC3 à sa **table ARP**.

**Table ARP** : associations IP ↔ MAC. Commande **`arp -a`** sous Windows, macOS et Linux. Colonnes **Internet address** (IP), **Physical address** (MAC), **Type** : **static** = entrée par défaut, non apprise ; **dynamic** = apprise par ARP request/reply (exemple : 192.168.0.1, le routeur domestique de Jeremy).

### 4. GNS3, Wireshark et ping

- **GNS3** (gns3.com) : émulateur qui fait tourner de **vraies images Cisco IOS** (à acheter, GNS3 lui-même est gratuit), à la différence de **Packet Tracer**, simulateur gratuit suffisant pour le CCNA. GNS3 s'intègre à **Wireshark** (icône loupe) pour capturer le trafic.
- **Ping** : utilitaire qui **teste la joignabilité** et mesure le **temps aller-retour** (*round-trip time*). Deux messages, **ICMP echo request** et **ICMP echo reply**, **unicast** : il faut connaître la MAC de destination, donc **ARP d'abord**. Commande : `ping 192.168.1.3`.
- Sur Cisco IOS (Jeremy utilise des routeurs pour simuler les PC) : « Sending 5, 100-byte ICMP Echos » : **5 requêtes de 100 octets par défaut**. **`.`** = ping échoué, **`!`** = réussi. **Le premier ping échoue** le temps que l'ARP se fasse : taux de réussite **80 % (4/5)**, puis min/moy/max du temps aller-retour.
- Table ARP en IOS : **`show arp`** (privileged EXEC) : entrée pour 192.168.1.1 (PC1 lui-même) et 192.168.1.3.
- **Wireshark** : colonne Protocol **ARP** puis **ICMP**. ARP request : source 0c2f.b011.9d00 (PC1), destination broadcast, info « **Who has 192.168.1.3? Tell 192.168.1.1** ». ARP reply : source 0c2f.b06a.3900 (PC3), info « **192.168.1.3 is at 0c2f.b06a.3900** ». Puis 4 echo requests (PC1 → PC3) et 4 echo replies (PC3 → PC1).
- Règle générale : pour envoyer à un équipement du même réseau, **ARP d'abord pour apprendre sa MAC, puis le trafic**.

### 5. La table d'adresses MAC sur un switch Cisco

- **`show mac address-table`** (anciens IOS : `show mac-address-table`, avec un tiret de plus). Colonnes : **VLAN** (*Virtual LAN*, vu plus tard ; **1** par défaut), **MAC address**, **Type** (**DYNAMIC** : apprise, non configurée), **Ports** (= interface).
- **Vieillissement** (*aging*) : entrée dynamique retirée après **5 minutes** sans trafic de cette MAC.
- Suppression manuelle : **`clear mac address-table dynamic`** (toutes), **`clear mac address-table dynamic address <mac>`** (une adresse), **`clear mac address-table dynamic interface gi0/0`** (toutes celles d'une interface).

### 6. Retour dans Wireshark : bourrage et champ Type

- `ping 192.168.1.3 size 36` : charge utile 36 octets < 46 → **10 octets de bourrage** = **20 zéros hexadécimaux** (1 chiffre hexa = 4 bits, 2 chiffres = 1 octet).
- Champ Type : **0x0800 = IPv4**, **0x86DD = IPv6**, **0x0806 = ARP**.

### 7. Pièges d'examen

- Taille minimale de trame **64 octets**, charge utile minimale **46 octets**, en-tête + remorque **18 octets** (sans préambule/SFD) ; bourrage = zéros.
- **ARP request = broadcast** ; ARP reply, echo request et echo reply sont **unicast**.
- Un switch inonde **broadcast et unicast inconnue**, jamais l'unicast connue.
- Colonnes de `show mac address-table` : **VLAN, MAC address, Type, Ports** ; « Internet address, Physical address, Type » est la sortie d'`arp -a` sur un PC, pas la table MAC.
- Syntaxe exacte : **`clear mac address-table dynamic interface <id>`** (espace après mac, tiret entre address et table). Ne pas confondre espace et tiret.
- Premier ping échoué = **ARP**, pas une panne.
- Un hôte ignore une ARP request d'après l'**IP** de destination (la MAC de destination est le broadcast pour tous).

### 8. Commandes IOS et commandes PC

```text
PC> arp -a                                         ! table ARP sous Windows, macOS, Linux
Router# ping 192.168.1.3                           ! 5 echo requests de 100 octets par défaut sur IOS
Router# ping 192.168.1.3 size 36                   ! ping de 36 octets (montre le bourrage)
Router# show arp                                   ! table ARP sur Cisco IOS
Switch# show mac address-table                     ! table MAC : VLAN, MAC address, Type, Ports
Switch# clear mac address-table dynamic            ! supprime toutes les MAC dynamiques
Switch# clear mac address-table dynamic address 0c2f.b011.9d00   ! une seule adresse
Switch# clear mac address-table dynamic interface gi0/0          ! toutes celles d'une interface
```

### 9. Le lab (Day 6 Lab, « Analyzing Ethernet Switching »)

**Objectif :** sur la topologie des cours (SW1 avec PC1, PC2 ; SW2 avec PC3, PC4), prédire puis observer les messages d'un ping, lire et vider les tables MAC. Hypothèse : **tables MAC et tables ARP vides** au départ.

1. **Prédire** : si PC1 pingue PC3, quels messages et qui les reçoit ? **ARP request** (broadcast, reçue par tous sauf PC1 ; PC2 et PC4 l'ignorent), **ARP reply** de PC3 (unicast via SW2, SW1, reçue par PC1 seul), **ICMP echo request** (unicast, PC3 seul), **ICMP echo reply** (unicast, PC1 seul). Un PC Windows envoie **4 pings** par défaut (Cisco : 5).
2. **Vérifier en mode simulation** (bouton en bas à droite) : sur PC1, Desktop > Command Prompt, `ping 192.168.1.3`. Deux messages apparaissent : ICMP et ARP. Sur l'ICMP, couche 2 : « next-hop address is a unicast… not in the ARP table… sends an ARP request and **buffers** this packet » (il garde le paquet pour plus tard). Sur l'ARP, **Outbound PDU details** : préambule, SFD, destination, source, type, data, FCS ; **type 0806** (ARP), destination **tout F**. Faire défiler : ARP diffusée par SW1 (PC2, SW2) puis SW2 (PC3, PC4) ; seule PC3 répond, en unicast ; puis echo request et reply. **Play** montre les pings suivants.
3. **Générer du trafic** pour que les switches apprennent toutes les MAC : repasser en mode temps réel, re-pinguer PC1 → PC3 (la simulation est parfois capricieuse), puis depuis PC2 : `ping 192.168.1.4`.
4. **Identifier la MAC de chaque PC** : sur SW1, `enable` (ou `en`), `show mac address-table` (**espace** après mac, **tiret** entre address et table). PC1 = entrée sur **Fa0/1**, PC2 = **Fa0/2**. PC3 et PC4 apparaissent toutes deux via **Gi0/1** : impossible de les distinguer depuis SW1, donc sur SW2 : PC3 = Fa0/1, PC4 = Fa0/2. Les MAC peuvent différer d'une machine à l'autre.
5. **Vider les tables** : `clear mac address-table dynamic` sur SW2 puis SW1. Le `?` (aide contextuelle) ne propose **aucune option** : Packet Tracer ne supporte pas `address` ni `interface`, il faut tout effacer. **Flèche haut** rappelle les commandes précédentes ; `show mac address-table` confirme une table vide.

### 10. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Ping de 36 octets ; la capture montre une longue série de `00000000` en fin de charge utile Ethernet. Explication ? | **Octets de bourrage** | La charge utile minimale est 46 octets : du bourrage complète les 36 octets. Les pings ne sont pas des zéros ; le FCS n'est pas une série de zéros. |
| Quel message est envoyé à tous les hôtes du réseau local ? | **ARP request** | ARP reply est unicast vers le demandeur ; ICMP echo request et reply (ping) sont unicast vers un hôte précis. |
| Champs de `show mac address-table` sur un switch Cisco ? | **VLAN, MAC address, Type, Ports** | « MAC address, Ports » et « VLAN, MAC address, Ports » sont incomplets ; « Internet address, Physical address, Type » est la sortie d'`arp -a` sur un PC. |
| Quels types de trames un switch envoie-t-il sur toutes les interfaces sauf celle de réception ? | **Broadcast et unicast inconnue** | L'unicast connue est dans la table, pas d'inondation : toute réponse l'incluant est fausse. Broadcast = destination FFFF.FFFF.FFFF. |
| Commande pour effacer les MAC dynamiques d'une interface précise ? | **`clear mac address-table dynamic interface <interface-id>`** | Les autres variantes mettent les tirets au mauvais endroit ou omettent `dynamic`. |

---

## 🇬🇧 English version

### 1. More on the Ethernet frame

- **The preamble + SFD are usually not considered part of the Ethernet header**, although they are sent with every frame. The header is then **destination, source, type**; **header + trailer (FCS) = 18 bytes**.
- **Minimum frame size: 64 bytes**, including the payload (the packet), excluding preamble and SFD. 64 − 18 = **46-byte minimum payload**.
- Smaller payload → **padding** bytes are added, all **0s**. Example: a 34-byte packet gets **12 bytes** of padding.

### 2. Today's topology

PC1, PC2 on SW1; PC3, PC4 on SW2; interfaces **G0/0, G0/1, G0/2** (GigabitEthernet). Realistic MACs sharing the OUI **0C2F.B0** (same maker); Jeremy uses only the last 4 digits: PC1 = **9D00**, PC2 = **6200**. Network **192.168.1.0/24**: PC1 = 192.168.1.1, PC2 = .2, PC3 = .3, PC4 = .4 (IP details in a later video).

A frame carries more than MACs: it encapsulates an **IP packet** with source and destination IPs. **The user enters the destination IP, not the MAC**; but switches are **Layer 2** devices working with MACs. PC1 must therefore **discover PC3's MAC** before sending: that is **ARP**'s job.

### 3. ARP, Address Resolution Protocol

- Used to **discover the Layer 2 address (MAC) of a known Layer 3 address (IP)**.
- Two messages: **ARP request** (sent by the device that wants the MAC) and **ARP reply** (sent by the owner of the IP).
- **ARP request = broadcast frame** (to all hosts on the network): destination MAC **FFFF.FFFF.FFFF**, the **broadcast address**. Source/destination IPs and source MAC are those of the final frame.
- **ARP reply = unicast**, straight back to the requester, since its MAC was the request's source.

PC1 → PC3 walkthrough:

1. SW1 receives the request, **learns PC1's MAC** (dynamic address) and, destination all Fs, sends it out of **all interfaces except the receiving one** (G0/1, G0/2; not G0/0), much like an unknown unicast.
2. **PC2 ignores** the request: the **destination IP** does not match its own.
3. SW2 learns PC1 on **G0/2** and broadcasts out of G0/0 and G0/1. PC4 ignores it; **PC3 recognizes its IP** and sends the **ARP reply** (PC3's IP and MAC as source, PC1 as destination).
4. SW2 learns PC3 on **G0/0**; destination known → **known unicast, forwarded** out of G0/2 (no flooding). SW1 forwards out of G0/0. PC1 adds PC3 to its **ARP table**.

**ARP table**: IP ↔ MAC associations. Command **`arp -a`** on Windows, macOS and Linux. Columns **Internet address** (IP), **Physical address** (MAC), **Type**: **static** = default entry, not learned; **dynamic** = learned via ARP request/reply (example: 192.168.0.1, Jeremy's home router).

### 4. GNS3, Wireshark and ping

- **GNS3** (gns3.com): an emulator running **real Cisco IOS images** (which you must buy; GNS3 itself is free), unlike **Packet Tracer**, a free simulator that is enough for the CCNA. GNS3 integrates with **Wireshark** (magnifying-glass icon) to capture traffic.
- **Ping**: a utility that **tests reachability** and measures the **round-trip time**. Two messages, **ICMP echo request** and **ICMP echo reply**, both **unicast**: the destination MAC must be known, hence **ARP first**. Command: `ping 192.168.1.3`.
- On Cisco IOS (Jeremy uses routers to simulate the PCs): "Sending 5, 100-byte ICMP Echos": **5 requests of 100 bytes by default**. **`.`** = failed ping, **`!`** = success. **The first ping fails** while ARP takes place: success rate **80% (4/5)**, then min/avg/max round-trip time.
- ARP table on IOS: **`show arp`** (privileged EXEC): entries for 192.168.1.1 (PC1 itself) and 192.168.1.3.
- **Wireshark**: Protocol column shows **ARP** then **ICMP**. ARP request: source 0c2f.b011.9d00 (PC1), destination broadcast, info "**Who has 192.168.1.3? Tell 192.168.1.1**". ARP reply: source 0c2f.b06a.3900 (PC3), info "**192.168.1.3 is at 0c2f.b06a.3900**". Then 4 echo requests (PC1 → PC3) and 4 echo replies (PC3 → PC1).
- General rule: to send to a device on the same network, **ARP first to learn its MAC, then the traffic**.

### 5. The MAC address table on a Cisco switch

- **`show mac address-table`** (older IOS: `show mac-address-table`, with an extra hyphen). Columns: **VLAN** (*Virtual LAN*, covered later; default **1**), **MAC address**, **Type** (**DYNAMIC**: learned, not configured), **Ports** (= interface).
- **Aging**: a dynamic entry is removed after **5 minutes** without traffic from that MAC.
- Manual removal: **`clear mac address-table dynamic`** (all), **`clear mac address-table dynamic address <mac>`** (one address), **`clear mac address-table dynamic interface gi0/0`** (all entries of one interface).

### 6. Back in Wireshark: padding and the Type field

- `ping 192.168.1.3 size 36`: 36-byte payload < 46 → **10 bytes of padding** = **20 hexadecimal zeros** (1 hex digit = 4 bits, 2 digits = 1 byte).
- Type field: **0x0800 = IPv4**, **0x86DD = IPv6**, **0x0806 = ARP**.

### 7. Exam traps

- Minimum frame **64 bytes**, minimum payload **46 bytes**, header + trailer **18 bytes** (without preamble/SFD); padding = zeros.
- **ARP request = broadcast**; ARP reply, echo request and echo reply are **unicast**.
- A switch floods **broadcast and unknown unicast**, never known unicast.
- `show mac address-table` columns: **VLAN, MAC address, Type, Ports**; "Internet address, Physical address, Type" is `arp -a` output on a PC, not the MAC table.
- Exact syntax: **`clear mac address-table dynamic interface <id>`** (space after mac, hyphen between address and table). Do not mix up the space and the hyphen.
- First ping failing = **ARP**, not an outage.
- A host ignores an ARP request based on the destination **IP** (the destination MAC is the broadcast for everyone).

### 8. IOS commands and PC commands

```text
PC> arp -a                                         ! ARP table on Windows, macOS, Linux
Router# ping 192.168.1.3                           ! 5 echo requests of 100 bytes by default on IOS
Router# ping 192.168.1.3 size 36                   ! 36-byte ping (shows the padding)
Router# show arp                                   ! ARP table on Cisco IOS
Switch# show mac address-table                     ! MAC table: VLAN, MAC address, Type, Ports
Switch# clear mac address-table dynamic            ! remove all dynamic MACs
Switch# clear mac address-table dynamic address 0c2f.b011.9d00   ! a single address
Switch# clear mac address-table dynamic interface gi0/0          ! all entries of one interface
```

### 9. The lab (Day 6 Lab, "Analyzing Ethernet Switching")

**Goal:** on the lecture topology (SW1 with PC1, PC2; SW2 with PC3, PC4), predict then observe the messages of a ping, read and clear the MAC tables. Assumption: **MAC tables and ARP tables empty** at the start.

1. **Predict**: if PC1 pings PC3, which messages are sent and who receives them? **ARP request** (broadcast, received by everyone except PC1; PC2 and PC4 ignore it), **ARP reply** from PC3 (unicast via SW2, SW1, received by PC1 only), **ICMP echo request** (unicast, PC3 only), **ICMP echo reply** (unicast, PC1 only). A Windows PC sends **4 pings** by default (Cisco: 5).
2. **Verify in simulation mode** (button bottom right): on PC1, Desktop > Command Prompt, `ping 192.168.1.3`. Two messages appear: ICMP and ARP. On the ICMP, Layer 2: "next-hop address is a unicast... not in the ARP table... sends an ARP request and **buffers** this packet" (holds it to send later). On the ARP, **Outbound PDU details**: preamble, SFD, destination, source, type, data, FCS; **type 0806** (ARP), destination **all Fs**. Step through: ARP broadcast by SW1 (PC2, SW2) then SW2 (PC3, PC4); only PC3 replies, unicast; then echo request and reply. **Play** shows the remaining pings.
3. **Generate traffic** so the switches learn every MAC: back to realtime mode, ping PC1 → PC3 again (simulation mode is sometimes flaky), then from PC2: `ping 192.168.1.4`.
4. **Identify each PC's MAC**: on SW1, `enable` (or `en`), `show mac address-table` (**space** after mac, **hyphen** between address and table). PC1 = entry on **Fa0/1**, PC2 = **Fa0/2**. PC3 and PC4 both show via **Gi0/1**: cannot be told apart from SW1, so on SW2: PC3 = Fa0/1, PC4 = Fa0/2. MACs may differ on your computer.
5. **Clear the tables**: `clear mac address-table dynamic` on SW2 then SW1. The `?` (context-sensitive help) offers **no options**: Packet Tracer does not support `address` or `interface`, you must clear everything. **Up arrow** recalls previous commands; `show mac address-table` confirms an empty table.

### 10. The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| 36-byte ping; the capture shows a long series of `00000000` at the end of the Ethernet payload. Explanation? | **Padding bytes** | The minimum payload is 46 bytes: padding fills out the 36 bytes. Pings are not series of zeros; the FCS is not a series of zeros. |
| Which message is sent to all hosts on the local network? | **ARP request** | ARP reply is unicast to the requester; ICMP echo request and reply (ping) are unicast to a specific host. |
| Fields in `show mac address-table` on a Cisco switch? | **VLAN, MAC address, Type, Ports** | "MAC address, Ports" and "VLAN, MAC address, Ports" are incomplete; "Internet address, Physical address, Type" is `arp -a` output on a PC. |
| Which frame types does a switch send out of all interfaces except the receiving one? | **Broadcast and unknown unicast** | Known unicast is in the table, no flooding: any answer including it is wrong. Broadcast = destination FFFF.FFFF.FFFF. |
| Command to clear the dynamic MACs of a specific interface? | **`clear mac address-table dynamic interface <interface-id>`** | The other variants put hyphens in the wrong place or omit `dynamic`. |
