# CCNA Day 46 : QoS (Part 1), Voice VLANs & PoE / QoS (partie 1), VLAN voix et PoE

> Source : Jeremy's IT Lab, « Free CCNA | QoS (Part 1) | Day 46 » (33 min, vidéo n°93 de la playlist, cours) et « Free CCNA | Voice VLANs | Day 46 Lab » (20 min, vidéo n°94, lab). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Téléphones IP et VLAN voix

- Les téléphones traditionnels utilisent le **PSTN** (*Public Switched Telephone Network*), parfois appelé **POTS** (*Plain Old Telephone Service*). Les **téléphones IP** utilisent la **VoIP** (*Voice over IP*) : l'audio est encapsulé dans des paquets IP et envoyé sur un réseau IP comme Internet.
- Un téléphone IP se connecte au switch comme n'importe quel hôte final. On peut mettre un PC et un téléphone sur deux ports distincts, mais il existe une approche plus courante.
- **Switch interne à 3 ports** du téléphone IP : un port **uplink** vers le switch externe, un port **downlink** vers le PC, un port interne vers le téléphone lui-même. Le PC et le téléphone **partagent un seul port de switch** : avec le même nombre d'appareils, on utilise deux fois moins de ports, donc moins de switches.
- Recommandation : séparer le **trafic voix** (téléphone) et le **trafic données** (PC) dans des VLAN différents en configurant un **VLAN voix** (*voice VLAN*). Le trafic du PC est **non étiqueté** (*untagged*), celui du téléphone est **étiqueté** (*tagged*) avec un VLAN ID. Cela permet ensuite à la QoS de donner la priorité au trafic des téléphones.
- Configuration : un port d'accès classique plus **une seule commande supplémentaire** : `switchport voice vlan 11`. Le switch utilise **CDP** (*Cisco Discovery Protocol*) pour indiquer au téléphone d'étiqueter son trafic dans le VLAN 11.
- Le port accepte donc du trafic de deux VLAN (10 et 11), mais `show interfaces g0/0 switchport` montre un mode administratif et opérationnel **static access** : ce **n'est pas un trunk**. `show interfaces trunk` n'affiche rien ; `show interfaces g0/0 trunk` indique **not-trunking** (la ligne « Vlans allowed on trunk » apparaît toujours dans cette commande, même si ce n'est pas un trunk).
- Le VLAN d'accès des PC est parfois appelé **VLAN données** (*data VLAN*).

### 2. Power over Ethernet (PoE)

- Le **PSE** (*Power Sourcing Equipment*, typiquement le switch) fournit du courant aux **PD** (*Powered Devices* : téléphones IP, caméras IP, points d'accès sans fil) sur **le même câble Ethernet** que les données. Le switch reçoit du courant **AC** de la prise, le convertit en **DC** et l'envoie aux PD.
- Trop de courant endommage un appareil : le PSE envoie d'abord des **signaux de faible puissance**, observe la réponse, détermine si le PD a besoin de courant et combien, alimente le démarrage, puis continue à surveiller.
- **Power policing** : empêche un PD de tirer trop de courant. La configuration PoE n'est pas un sujet d'examen, mais il faut connaître le but de cette fonction.
  - `power inline police` = `power inline police action err-disable` (défaut) : le port passe en **err-disabled** et un message **Syslog** est généré. Réactivation par `shutdown` puis `no shutdown`.
  - `power inline police action log` : le port n'est pas désactivé, il **redémarre** et envoie un message Syslog ; le PD perd le courant, redémarre et renégocie ses besoins.
  - `show power inline police g0/0` : puissance fournie, capacité, et action configurée (err-disable par défaut même si on ne l'a pas précisée).
- Standards : d'abord **Cisco ILP** (*Inline Power*), propriétaire, **7 watts** par port sur **2 paires** (fils 4, 5, 7, 8, ceux que Ethernet/FastEthernet n'utilisent pas pour les données, qui passent sur 1, 2, 3, 6). Puis standardisation : **PoE (802.3af, Type 1)** et **PoE+ (802.3at, Type 2)**, plus de puissance que l'ILP. Puis **UPoE** (*Universal PoE*, Cisco, non standard), puis **802.3bt** avec **Type 3 (jusqu'à 60 W)** et **Type 4 (jusqu'à 100 W)**. Pas besoin de mémoriser le tableau pour l'examen ; il faut comprendre le concept et l'usage.
- Les PC restent branchés sur une prise ; les téléphones sont alimentés par le câble Ethernet.

### 3. Introduction à la QoS (*Quality of Service*)

- Historique : voix sur le **PSTN**, données sur les réseaux IP (WAN d'entreprise, Internet) : pas de concurrence pour la bande passante, pas besoin de QoS. Les réseaux modernes sont **convergés** (*converged networks*) : téléphones IP, vidéo, web partagent le même réseau IP (économies, intégration avec Cisco WebEx ou Microsoft Teams), mais les trafics sont en concurrence. Problème sur un réseau chargé pour la voix et la vidéo, sensibles au délai.
- **QoS** = ensemble d'outils des équipements réseau pour appliquer un **traitement différent à différents paquets** : priorité plus haute pour certains trafics, plus basse pour d'autres.
- Quatre caractéristiques gérées par la QoS :
  1. **Bande passante** (*bandwidth*) : capacité globale du lien en bits par seconde (kbps, Mbps, Gbps). La QoS permet de **réserver** une part du lien à certains trafics : par exemple 20 % voix, 30 % données importantes, 50 % le reste.
  2. **Délai** (*delay*) : **one-way delay** (source vers destination) ou **two-way delay** (aller et retour).
  3. **Gigue** (*jitter*) : **variation du délai aller** entre paquets d'une même application (10 ms pour certains, 100 ms pour d'autres = forte gigue). Les téléphones IP ont un **jitter buffer** qui impose un délai fixe aux paquets audio ; une gigue trop forte déborde le buffer.
  4. **Perte** (*loss*) : pourcentage de paquets qui n'arrivent pas. Causes : câbles défectueux, ou **files d'attente pleines** sur un réseau congestionné.
- Standards recommandés pour un **audio interactif** acceptable (appel téléphonique, audio d'un appel Zoom) : **délai aller ≤ 150 ms**, **gigue ≤ 30 ms**, **perte ≤ 1 %**.

### 4. Files d'attente (*queuing*), tail drop, RED et WRED

- Si un équipement reçoit plus vite qu'il ne peut transmettre sur l'interface de sortie, les messages vont dans une **file d'attente** (*queue*). Par défaut : **FIFO** (*First In First Out*), envoi dans l'ordre d'arrivée, aucun traitement particulier.
- File pleine : les nouveaux paquets sont **jetés** : **tail drop**.
- Le tail drop provoque la **synchronisation globale TCP** (*TCP global synchronization*). Rappel de la **fenêtre glissante** (*sliding window*) : l'émetteur augmente son débit, réduit quand un paquet est perdu, puis ré-augmente. Avec le tail drop, **tous** les hôtes TCP ralentissent en même temps (réseau sous-utilisé), puis ré-accélèrent en même temps (congestion), en **vagues** : congestion, baisse globale de la fenêtre, sous-utilisation, hausse globale, congestion…
- **RED** (*Random Early Detection*) : quand la file atteint un **seuil**, l'équipement jette **aléatoirement** des paquets de certains flux TCP : seuls ces flux ralentissent, pas tous en même temps. En RED standard, tous les trafics sont traités pareil (seuil global).
- **WRED** (*Weighted Random Early Detection*) : permet de choisir quels paquets jeter selon la **classe de trafic** (HTTP à tel niveau de remplissage, FTP à tel autre) ; les trafics de basse priorité sont jetés plus tôt. Les classes de trafic sont détaillées dans la vidéo suivante.

### 5. Pièges d'examen

- Un port avec `switchport voice vlan` transporte deux VLAN mais reste un **port d'accès** (static access), pas un trunk.
- Sans `switchport access vlan`, le trafic données est dans le **VLAN 1 par défaut** et arrive **non étiqueté** ; le trafic voix est étiqueté dans le VLAN voix appris par **CDP**.
- `power inline police` seul = action **err-disable** par défaut (port désactivé + Syslog) ; `action log` ne désactive pas le port.
- Les trois seuils de l'audio interactif : **150 ms / 30 ms / 1 %**.
- L'effet négatif du tail drop est la **synchronisation globale TCP** ; la fenêtre glissante n'est qu'un mécanisme de TCP, et RED/WRED sont des **outils pour éviter** le tail drop, pas des effets.
- **FIFO** est la méthode par défaut de **transmission** des paquets en file ; RED et WRED sont des méthodes de **suppression** de paquets, pas de transmission. CBWFQ est présenté dans la vidéo suivante.

### 6. Commandes IOS

```
SW1(config)# interface g0/0
SW1(config-if)# switchport mode access          ! port d'accès classique
SW1(config-if)# switchport access vlan 10       ! VLAN données (data VLAN) du PC
SW1(config-if)# switchport voice vlan 11        ! VLAN voix : le téléphone étiquette son trafic dans le VLAN 11 (appris par CDP)
SW1(config-if)# power inline police             ! power policing, action par défaut err-disable + Syslog
SW1(config-if)# power inline police action err-disable   ! identique à la commande précédente
SW1(config-if)# power inline police action log  ! redémarre l'interface et envoie un Syslog, sans err-disable
SW1# show interfaces g0/0 switchport            ! mode admin/opérationnel (static access), access VLAN, voice VLAN
SW1# show interfaces trunk                      ! rien d'affiché : le port n'est pas un trunk
SW1# show interfaces g0/0 trunk                 ! status not-trunking
SW1# show power inline police g0/0              ! puissance fournie, capacité, action de policing
```

### 7. Le lab : Voice VLANs

- **Topologie** : deux PC, chacun connecté à un téléphone IP ; les téléphones (phone1, phone2) connectés à SW1 (G1/0/2 et G1/0/3) ; SW1 (switch multicouche choisi parce qu'il supporte le **PoE**, couche 3 non utilisée) relié à R1 par G1/0/1 ; **router on a stick** entre SW1 et R1. Le câble d'alimentation des téléphones n'est pas branché : ils sont alimentés par PoE.
- **SW1** :

```
SW1(config)# interface range g1/0/2 - 3
SW1(config-if-range)# switchport mode access
SW1(config-if-range)# switchport access vlan 10     ! VLAN données
SW1(config-if-range)# switchport voice vlan 20      ! VLAN voix
SW1(config)# interface g1/0/1
SW1(config-if)# switchport trunk encapsulation dot1q
SW1(config-if)# switchport mode trunk
SW1(config-if)# switchport trunk allowed vlan 10,20   ! limiter aux VLAN nécessaires (tous autorisés par défaut)
```

- **R1** (les réglages de téléphonie sont pré-configurés sur R1, hors programme CCNA ; R1 attribue aux téléphones leur numéro, leur adresse IP, etc.) :

```
R1(config)# interface f0/0
R1(config-if)# no shutdown
R1(config)# interface f0/0.10
R1(config-subif)# encapsulation dot1q 10
R1(config-subif)# ip address 192.168.10.1 255.255.255.0   ! VLAN données
R1(config)# interface f0/0.20
R1(config-subif)# encapsulation dot1q 20
R1(config-subif)# ip address 192.168.20.1 255.255.255.0   ! VLAN voix
```

- **Vérifications** :
  - PC1 `ping 192.168.10.12` (PC2) fonctionne ; en mode simulation, « Outbound PDU Details » montre **aucun tag 802.1Q** sur la trame du PC. `ping 192.168.10.1` (R1) fonctionne aussi.
  - Onglet GUI de phone2 : numéro **2010**, attribué par R1. SW1 a dit aux téléphones leur VLAN, R1 leur a donné numéro et adresse IP.
  - Appel de phone1 vers 2010 en mode simulation : message **SCCP** (*Skinny Client Control Protocol*, hors programme). L'en-tête IP contient l'adresse de phone1 ; un **en-tête Dot1q** est présent : **TPID 8100** (dot1q) et dans le **TCI** (*Tag Control Information*) le VLAN ID **0x0014 = 20**.
- **Conclusion** : le trafic des PC n'est pas étiqueté, celui des téléphones l'est. Cela vaut aussi dans l'autre sens : SW1 n'étiquette pas ce qu'il envoie aux PC, mais étiquette ce qu'il envoie aux téléphones.

### 8. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Configuration de G0/0 avec `switchport voice vlan 99` et sans `switchport access vlan` : quelles affirmations sont vraies ? (deux réponses) | **A** : le trafic voix reçu sur G0/0 doit être étiqueté dans le VLAN 99 ; **D** : le trafic données reçu sur G0/0 doit être non étiqueté | Le téléphone apprend par CDP qu'il est dans le VLAN 99 et étiquette. Sans `switchport access vlan`, le port est dans le VLAN 1 par défaut ; le PC envoie non étiqueté et SW1 le place dans le VLAN 1. |
| Vous tapez `power inline police` sur un port PoE ; que se passe-t-il si l'appareil tire trop de courant ? | **C** : l'interface est err-disabled et un message Syslog est généré | L'action par défaut est err-disable (équivalent de `power inline police action err-disable`). Réactivation par `shutdown` puis `no shutdown`. |
| Standards recommandés pour un audio interactif acceptable ? (trois réponses) | **B** délai ≤ 150 ms, **C** gigue ≤ 30 ms, **E** perte ≤ 1 % | Les autres valeurs ne sont pas les seuils recommandés ; en dessous de ces standards, la qualité de l'appel se dégrade sensiblement. |
| Effet négatif du tail drop ? | **D** : synchronisation globale TCP | Tous les hôtes TCP ralentissent puis ré-accélèrent ensemble, en vagues. La fenêtre glissante TCP est un simple mécanisme, pas un effet négatif ; RED et WRED sont des outils pour éviter le tail drop. |
| Méthode par défaut de transmission des paquets en file d'attente ? | **A** : FIFO | First In First Out : ordre d'arrivée, pas de passage en tête pour les paquets prioritaires. CBWFQ est vu dans la vidéo suivante ; RED et WRED sont des méthodes de suppression, pas de transmission. |

---

## 🇬🇧 English version

### 1. IP phones and voice VLANs

- Traditional phones use the **PSTN** (Public Switched Telephone Network), sometimes called **POTS** (Plain Old Telephone Service). **IP phones** use **VoIP** (Voice over IP): audio is encapsulated in IP packets and sent over an IP network such as the Internet.
- An IP phone connects to a switch like any end host. A PC and a phone could each use their own switch port, but there is a better, more common approach.
- IP phones have an **internal 3-port switch**: one **uplink** port to the external switch, one **downlink** port to the PC, one port connected internally to the phone itself. The PC and phone **share a single switch port**: same number of devices, half the switch ports, fewer switches to buy.
- Recommended: separate **voice traffic** (from the phone) and **data traffic** (from the PC) in separate VLANs with a **voice VLAN**. PC traffic is **untagged**, phone traffic is **tagged** with a VLAN ID. This lets QoS give phone traffic higher priority later.
- Configuration: a regular access port plus **one extra command**: `switchport voice vlan 11`. The switch uses **CDP** (Cisco Discovery Protocol) to tell the phone to tag its traffic in VLAN 11.
- The port now accepts traffic from two VLANs (10 and 11), but `show interfaces g0/0 switchport` shows administrative and operational mode **static access**: it is **not a trunk**. `show interfaces trunk` shows nothing; `show interfaces g0/0 trunk` shows **not-trunking** (the "Vlans allowed on trunk" line always appears in that command, even on a non-trunk).
- The PCs' access VLAN is sometimes called the **data VLAN**.

### 2. Power over Ethernet (PoE)

- **PSE** (Power Sourcing Equipment, typically a switch) provides electric power to **PDs** (Powered Devices: IP phones, IP cameras, wireless access points) over **the same Ethernet cable** used for data. The switch receives **AC** power from the outlet, converts it to **DC**, and supplies it to the PDs.
- Too much current harms devices: the PSE first sends **low-power signals**, monitors the response, determines whether and how much power the PD needs, supplies power for boot, then keeps monitoring.
- **Power policing** prevents a PD from drawing too much power. PoE configuration is not an exam topic, but you should know the purpose of power policing.
  - `power inline police` = `power inline police action err-disable` (default): the port is **err-disabled** and a **Syslog** message is sent. Re-enable with `shutdown` then `no shutdown`.
  - `power inline police action log`: the port is not shut down; it **restarts** and sends a Syslog message; the PD loses power, restarts and re-negotiates its power needs.
  - `show power inline police g0/0`: power currently provided, capacity, and the configured action (err-disable by default even if not specified).
- Standards: originally **Cisco ILP** (Inline Power), proprietary, **7 watts** per port over **2 wire pairs** (wires 4, 5, 7, 8, the ones Ethernet/FastEthernet do not use for data, which use 1, 2, 3, 6). Then standardized: **PoE (802.3af, Type 1)** and **PoE+ (802.3at, Type 2)**, more power than ILP. Then Cisco's non-standard **UPoE** (Universal PoE), then **802.3bt** with **Type 3 (up to 60 W)** and **Type 4 (up to 100 W)**. You probably don't need to memorize the table; understand what PoE is and what it is used for.
- PCs still plug into a wall outlet; the phones get power over the Ethernet cable.

### 3. Introduction to QoS (Quality of Service)

- History: voice on the **PSTN**, data on IP networks (enterprise WAN, Internet): no competition for bandwidth, no need for QoS. Modern networks are **converged networks**: IP phones, video, web traffic share the same IP network (cost savings, integration with Cisco WebEx or Microsoft Teams), but traffic now competes for bandwidth. A busy network is a problem for delay-sensitive voice and video.
- **QoS** = a set of tools used by network devices to apply **different treatment to different packets**: higher priority for some traffic, lower for others.
- Four characteristics managed by QoS:
  1. **Bandwidth**: overall capacity of the link in bits per second (kbps, Mbps, Gbps). QoS lets you **reserve** part of the link for specific traffic: e.g. 20% voice, 30% important data, 50% everything else.
  2. **Delay**: **one-way delay** (source to destination) or **two-way delay** (there and back).
  3. **Jitter**: **variation in one-way delay** between packets of the same application (some in 10 ms, some in 100 ms = lots of jitter). IP phones have a **jitter buffer** that provides a fixed delay to audio packets; too much jitter overruns the buffer.
  4. **Loss**: percentage of packets that do not reach their destination. Causes: faulty cables, or **full packet queues** on a congested network.
- Recommended standards for acceptable **interactive audio** (phone call, Zoom call audio): **one-way delay 150 ms or less**, **jitter 30 ms or less**, **loss 1% or less**.

### 4. Queuing, tail drop, RED and WRED

- If a device receives messages faster than it can forward them out of the appropriate interface, they are placed in a **queue**. Default: **FIFO** (First In First Out), sent in the order received, no special treatment.
- Full queue: new packets are **dropped**: **tail drop**.
- Tail drop leads to **TCP global synchronization**. Recall the TCP **sliding window**: the sender increases its rate, reduces it when a packet is dropped, then gradually increases again. With tail drop, **all** TCP hosts slow down at once (network underutilized), then all speed up at once (congestion), in **waves**: congestion, global window decrease, underutilization, global window increase, congestion...
- **RED** (Random Early Detection): when the queue reaches a **threshold**, the device **randomly** drops packets from select TCP flows: only those flows slow down, avoiding global synchronization. Standard RED treats all traffic the same (global threshold).
- **WRED** (Weighted Random Early Detection): control which packets are dropped depending on **traffic class** (HTTP at one queue level, FTP at another); lower-priority traffic is dropped sooner. Traffic classes are covered in the next video.

### 5. Exam traps

- A port with `switchport voice vlan` carries two VLANs but is still an **access port** (static access), not a trunk.
- Without `switchport access vlan`, data traffic is in the **default VLAN 1** and arrives **untagged**; voice traffic is tagged in the voice VLAN learned via **CDP**.
- `power inline police` alone = default action **err-disable** (port disabled + Syslog); `action log` does not disable the port.
- The three interactive-audio thresholds: **150 ms / 30 ms / 1%**.
- The negative effect of tail drop is **TCP global synchronization**; the sliding window is just a TCP mechanic, and RED/WRED are **tools to avoid** tail drop, not effects of it.
- **FIFO** is the default way of **forwarding** queued packets; RED and WRED are ways of **dropping** queued packets, not forwarding them. CBWFQ comes in the next video.

### 6. IOS commands

```
SW1(config)# interface g0/0
SW1(config-if)# switchport mode access          ! regular access port
SW1(config-if)# switchport access vlan 10       ! data VLAN for the PC
SW1(config-if)# switchport voice vlan 11        ! voice VLAN: the phone tags its traffic in VLAN 11 (learned via CDP)
SW1(config-if)# power inline police             ! power policing, default action err-disable + Syslog
SW1(config-if)# power inline police action err-disable   ! same as the previous command
SW1(config-if)# power inline police action log  ! restart the interface and send a Syslog, no err-disable
SW1# show interfaces g0/0 switchport            ! admin/operational mode (static access), access VLAN, voice VLAN
SW1# show interfaces trunk                      ! nothing displayed: the port is not a trunk
SW1# show interfaces g0/0 trunk                 ! status not-trunking
SW1# show power inline police g0/0              ! power provided, capacity, policing action
```

### 7. The lab: Voice VLANs

- **Topology**: two PCs, each connected to an IP phone; the phones (phone1, phone2) connected to SW1 (G1/0/2 and G1/0/3); SW1 (a multilayer switch chosen because it supports **PoE**, Layer 3 not used) connected to R1 via G1/0/1; **router on a stick** between SW1 and R1. The phones' power cables are not connected: they are powered via PoE.
- **SW1**:

```
SW1(config)# interface range g1/0/2 - 3
SW1(config-if-range)# switchport mode access
SW1(config-if-range)# switchport access vlan 10     ! data VLAN
SW1(config-if-range)# switchport voice vlan 20      ! voice VLAN
SW1(config)# interface g1/0/1
SW1(config-if)# switchport trunk encapsulation dot1q
SW1(config-if)# switchport mode trunk
SW1(config-if)# switchport trunk allowed vlan 10,20   ! limit to the VLANs you need (all allowed by default)
```

- **R1** (telephony settings pre-configured on R1, beyond the CCNA; R1 tells the phones their phone numbers, IP addresses, etc.):

```
R1(config)# interface f0/0
R1(config-if)# no shutdown
R1(config)# interface f0/0.10
R1(config-subif)# encapsulation dot1q 10
R1(config-subif)# ip address 192.168.10.1 255.255.255.0   ! data VLAN
R1(config)# interface f0/0.20
R1(config-subif)# encapsulation dot1q 20
R1(config-subif)# ip address 192.168.20.1 255.255.255.0   ! voice VLAN
```

- **Verification**:
  - PC1 `ping 192.168.10.12` (PC2) works; in simulation mode, "Outbound PDU Details" shows **no 802.1Q tag** in the PC's frame. `ping 192.168.10.1` (R1) works too.
  - phone2's GUI tab: phone number **2010**, assigned by R1. SW1 told the phones their VLAN, R1 gave them phone numbers and IP addresses.
  - Call from phone1 to 2010 in simulation mode: an **SCCP** (Skinny Client Control Protocol, not on the CCNA) message. The IP header holds phone1's assigned IP; a **Dot1q header** is present: **TPID 8100** (dot1q) and in the **TCI** (Tag Control Information) the VLAN ID **0x0014 = 20**.
- **Conclusion**: PC traffic is not tagged, phone traffic is. This also applies to traffic sent by SW1: SW1 does not tag traffic to the PCs, but tags traffic to the phones.

### 8. The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| G0/0 configured with `switchport voice vlan 99` and no `switchport access vlan`: which statements are true? (select two) | **A**: voice traffic received by G0/0 should be tagged in VLAN 99; **D**: data traffic received by G0/0 should be untagged | The phone learns via CDP that it is in VLAN 99 and tags. With no `switchport access vlan`, the port is in default VLAN 1; the PC sends untagged and SW1 assumes VLAN 1. |
| You issue `power inline police` on a PoE port; what happens if the device draws too much power? | **C**: the interface is err-disabled and a Syslog message is generated | Default action is err-disable (equivalent to `power inline police action err-disable`). Re-enable with `shutdown` then `no shutdown`. |
| Recommended standards for acceptable interactive audio quality? (select three) | **B** delay 150 ms or less, **C** jitter 30 ms or less, **E** loss 1% or less | The other values are not the recommended thresholds; if these are not met, expect a noticeable reduction in quality. |
| Negative effect of tail drop? | **D**: TCP global synchronization | All TCP hosts slow down in unison, then speed up in unison, in waves. The TCP sliding window is merely a mechanic, not negative on its own; RED and WRED are tools to avoid tail drop. |
| Default manner of forwarding queued packets? | **A**: FIFO | First In First Out: order of arrival, higher-priority packets are not moved to the front. CBWFQ is mentioned in the next video; RED and WRED are methods of dropping, not forwarding. |
