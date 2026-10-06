# CCNA Day 47 : QoS (Part 2) / QoS (partie 2)

> Source : Jeremy's IT Lab, « Free CCNA | QoS (Part 2) | Day 47 » (42 min, vidéo n°95 de la playlist, cours) et « Free CCNA | QoS | Day 47 Lab » (16 min, vidéo n°96, lab). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

Objectif de la vidéo : les termes du sujet d'examen 4.7 : **classification, marquage, files d'attente, congestion, policing, shaping**. La conception et la configuration de la QoS ne sont pas au programme du CCNA ; il faut comprendre les concepts.

### 1. Classification (*classification*)

- La **classification** organise le trafic (les paquets) en **classes de trafic**. C'est la base de la QoS : pour donner la priorité à certains trafics, il faut d'abord les identifier.
- Méthodes : une **ACL** (le trafic permis reçoit un traitement, comme pour le NAT dynamique : l'ACL sert à identifier, pas à filtrer) ; **NBAR** (*Network Based Application Recognition*), qui fait de l'**inspection profonde des paquets** (*deep packet inspection*) jusqu'à la couche 7 quand les ports TCP/UDP et les adresses IP ne suffisent pas.
- Champs dédiés dans les en-têtes : le **PCP** (*Priority Code Point*) de l'étiquette **802.1Q** (couche 2, utilisable seulement si une étiquette VLAN est présente) et le **DSCP** (*Differentiated Services Code Point*) de l'en-tête IP (couche 3).

### 2. Marquage de couche 2 : PCP / CoS

- Champ **PCP**, **3 bits** dans l'étiquette dot1q, aussi appelé **CoS** (*Class of Service*) : ne pas confondre CoS (ce champ) avec le concept général de QoS. Usage défini par **IEEE 802.1p**. 8 valeurs (0 à 7). À retenir : **0 = best effort**, **3 = applications critiques**, **4 = vidéo**, **5 = voix**.
- **Best effort** : aucune garantie de livraison ni de respect d'un standard QoS ; trafic ordinaire, valeur **0 par défaut**.
- Les téléphones IP marquent leur **signalisation d'appel** (*call signaling*, établissement des appels) en **PCP 3** et l'**audio** lui-même en **PCP 5**.
- **Marquer** (*mark*) = positionner la valeur du champ PCP ou DSCP ; les équipements lisent ces marquages pour classifier.
- **Limitation majeure du PCP** : il n'existe que là où il y a une étiquette dot1q : **liens trunk** (hors VLAN natif) et **liens d'accès avec VLAN voix** (trafic du téléphone). Le trafic des PC sur un port d'accès, et le trafic entre routeurs (R1-R2, R2-extérieur) n'ont pas d'étiquette : pas de marquage PCP possible. La classification de couche 3 n'a pas cette limite.

### 3. Marquage de couche 3 : octet ToS, IPP, DSCP

- Dans l'en-tête IPv4, l'octet **ToS** (*Type of Service*), le deuxième après version et IHL (IPv6 a un octet **Traffic Class**).
- **Ancien usage** : 3 bits **IPP** (*IP Precedence*, 8 valeurs, comme le PCP) et 5 bits peu utilisés. Marquages IPP : **6 et 7 réservés au network control** (par exemple messages OSPF entre routeurs), **5 voix interactive**, **4 vidéo interactive**, **3 signalisation voix**, **0 best effort**. Seules 6 valeurs restent utilisables, insuffisant pour les réseaux complexes.
- **Usage actuel** : **6 bits DSCP** (64 valeurs) + **2 bits ECN** (*Explicit Congestion Notification*). DSCP = IPP + 3 bits. Défini par la **RFC 2474 (1998)**, puis d'autres RFC **DiffServ** (*Differentiated Services*). Des marquages standard facilitent la conception et l'interopérabilité ISP/entreprise.

### 4. Les marquages DSCP standard

- **DF** (*Default Forwarding*) : best effort, **DSCP 0** (000000). Même valeur que CS0.
- **EF** (*Expedited Forwarding*) : trafic exigeant **faible perte, faible latence, faible gigue**, typiquement la **voix** : **DSCP 46** (**101110**).
- **AF** (*Assured Forwarding*) : ensemble de **12 valeurs**. **4 classes** (bits de gauche, 3 bits ; classe plus haute = meilleure priorité) et, dans chaque classe, **3 niveaux de drop precedence** (2 bits ; plus haut = plus de chances d'être jeté par WRED en cas de congestion) ; le dernier bit est toujours 0. Notation **AF XY** : X = classe, Y = drop precedence. **Formule : DSCP = 8X + 2Y**. Exemples de la vidéo : AF11 = 001010 = 10 ; AF12 = 001100 = 12 ; AF23 = 22 ; AF32 = 011100 = 28 ; AF43 = 38 (valeur AF la plus haute : pas de classe 5, 6, 7). **AF41** = meilleur traitement (classe la plus haute, drop precedence la plus basse), **AF13** = pire traitement.
- **CS** (*Class Selector*) : **8 valeurs** pour la **rétrocompatibilité avec IPP** : les 3 bits ajoutés sont à 0, les 3 bits IPP d'origine donnent CS0 à CS7. **DSCP = 8 × numéro CS** : CS0 = 0, CS1 = 8, CS2 = 16, CS3 = 24, CS4 = 32, CS5 = 40, CS6 = 48, CS7 = 56.
- Dans IOS, `class-map TEST` puis `match dscp ?` affiche : valeur décimale 0-63, les 12 valeurs AF (avec leur binaire, ex. AF11 = 001 010), 7 valeurs CS (CS0 = DF) et EF.
- **Recommandations de la RFC 4594** (développée avec Cisco) : **voix = EF** ; **vidéo interactive = AF4x** ; **vidéo en streaming = AF3x** ; **données haute priorité = AF2x** ; **best effort = DF**. Ce sont des recommandations : l'ingénieur décide de la politique.

### 5. Frontière de confiance (*trust boundary*)

- Définit où les équipements **font confiance** aux marquages reçus (transmis sans modification) ou **ne font pas confiance** (marquages modifiés selon la politique configurée).
- Exemple : frontière à SW1 : un message EF / CoS 5 du téléphone est remarqué DF / CoS 0 avant d'être transmis à R1, puis R2 (DF seulement, pas d'en-tête dot1q). Ce n'est pas idéal.
- Recommandation : si un téléphone IP est connecté, **déplacer la frontière de confiance vers le téléphone** (configuré sur le **port du switch**, pas sur le téléphone). Les marquages du téléphone sont conservés ; un PC qui marque son trafic EF (DSCP 46) voit son marquage changé en DF (DSCP 0). Les applications Zoom ou WebEx sur PC ont besoin de priorité, mais on marque alors au switch ou au routeur.

### 6. Files d'attente et gestion de la congestion

- Rappel : file pleine = **tail drop** ; **RED/WRED** jettent plus tôt pour l'éviter.
- L'essentiel de la QoS : **plusieurs files** (*multiple queues*). Le routeur classe le trafic (DSCP, etc.) et le place dans la file appropriée. Comme une seule trame sort à la fois, un **ordonnanceur** (*scheduler*) décide de quelle file part le prochain paquet ; la **priorisation** donne plus de poids à certaines files.
- Processus : trafic **entrant** (*ingress*), **routage** (choix de l'interface de sortie, NAT…), **classification**, **mise en file**, **ordonnancement**, **transmission**.
- **Weighted round-robin** : les paquets sont pris dans chaque file à tour de rôle (round-robin), et davantage de données sont prises dans les files prioritaires (weighted).
- **CBWFQ** (*Class-Based Weighted Fair Queuing*) : ordonnancement round-robin pondéré qui **garantit à chaque file un pourcentage minimal de bande passante** en période de congestion.
- Limite pour la voix/vidéo : même prioritaires, les files attendent leur tour, ce qui ajoute délai et gigue. Solution : **LLQ** (*Low Latency Queuing*) : une ou plusieurs files de **priorité stricte** (*strict priority*) : tant qu'il y a du trafic dedans, l'ordonnanceur le sert avant les autres. Inconvénient : risque d'**affamer** (*starve*) les autres files ; le **policing** limite le trafic admis dans la file prioritaire.
- Dans chaque file, RED ou WRED peuvent être utilisés contre le tail drop.
- Marquer un paquet EF ne fait rien en soi : il faut des outils comme CBWFQ et LLQ pour que les équipements le traitent en priorité.

### 7. Shaping et policing

- Les deux **contrôlent le débit** du trafic, à une valeur configurée inférieure à la capacité réelle du lien.
- **Shaping** : **met en file (bufferise)** le trafic qui dépasse le débit configuré.
- **Policing** : **jette** le trafic qui dépasse le débit configuré, mais tolère des **rafales** (*burst*) pendant un court moment, pour les applications « bursty » ; la taille de rafale est configurable. La classification permet des débits différents selon le trafic.
- Cas typique : client relié à un ISP par des interfaces Gigabit (1000 Mbps) mais abonné à **300 Mbps** : l'ISP configure du **policing entrant** à 300 Mbps sur son G0/0 ; le client configure du **shaping sortant** à 300 Mbps sur son G0/0 pour éviter que l'ISP ne jette son trafic.

### 8. Pièges d'examen

- **CoS = PCP** (3 bits du tag dot1q), pas la QoS entière ; marquages standard : 0 best effort, 3 applications critiques / signalisation, 4 vidéo, 5 voix.
- Le PCP n'existe que sur les **trunks** et les **ports d'accès avec VLAN voix** ; pas sur les liens entre routeurs.
- **EF = DSCP 46 = 101110** ; **DF = 0** ; **AF = 8X + 2Y** ; **CS = 8 × n**. AF n'a que les classes 1 à 4 : **AF51, AF61 n'existent pas**. **AF41** est le meilleur service AF.
- Bonne pratique : **faire confiance aux marquages des téléphones IP, pas à ceux des PC**.
- **LLQ** crée la file de priorité stricte pour le trafic à faible délai/gigue/perte ; CBWFQ garantit la bande passante mais sans priorité stricte.
- **Shaping = bufferise, policing = jette** (avec rafales tolérées).
- **PHB** (*per-hop behavior*, vu dans le lab) : la QoS configurée sur R1 ne s'applique qu'au saut vers R2 ; chaque routeur doit être configuré.

### 9. Commandes IOS

Configuration montrée à titre de démonstration (hors programme CCNA) : trois étapes : **class-map** (identifier le trafic), **policy-map** (actions), **service-policy** (appliquer à une interface).

```
R1(config)# class-map HTTPS_MAP                 ! identifie le trafic ; mode match-all par défaut (match-any : une seule condition suffit)
R1(config-cmap)# match protocol https           ! correspond au trafic HTTPS
R1(config)# class-map TEST
R1(config-cmap)# match dscp ?                   ! liste des valeurs : 0-63, AF11..AF43, CS1..CS7, EF
R1(config)# policy-map G0/0/0_OUT               ! actions à appliquer
R1(config-pmap)# class HTTPS_MAP
R1(config-pmap-c)# set ip dscp af31             ! marquer les paquets AF31
R1(config-pmap-c)# priority percent 10          ! file de priorité (LLQ) avec au moins 10 % de la bande passante
R1(config-pmap-c)# bandwidth percent 10         ! file garantie à 10 % (CBWFQ), sans priorité stricte
R1(config)# interface g0/0/0
R1(config-if)# service-policy output G0/0/0_OUT ! applique la policy-map au trafic sortant
R1# show running-config | section class-map     ! vérifier les class-maps
R1# show running-config | section policy-map    ! vérifier la policy-map
```

### 10. Le lab : configuration QoS de base

- **Topologie** : PC1 – SW1 – R1 – R2 – SW2 – SRV1 (10.0.0.100, aussi serveur DNS de PC1, qui résout jeremysitlab.com en 10.0.0.100). On suppose beaucoup de PC derrière R1 et un réseau congestionné.
- **Objectif** sur R1, trafic sortant de G0/0/0 : HTTPS marqué **AF31**, **≥ 10 %** de bande passante dans une **file prioritaire** ; HTTP marqué **AF32**, **≥ 10 %** sans file prioritaire ; ICMP marqué **CS2**, **≥ 5 %**. Valeurs arbitraires pour la démonstration (une file prioritaire pour HTTPS est inhabituelle, c'est normalement pour la voix).
- **PHB** : R1 priorise sur le saut vers R2 ; R2 traitera tout de la même façon s'il n'est pas configuré. La QoS doit être configurée partout où elle est nécessaire.
- **Avant configuration** : `ping jeremysitlab.com` depuis PC1 (requête DNS vers SRV1 puis ping) ; en mode simulation, « Outbound PDU Details » à R1 montre **DSCP 0x00** : les PC n'ont pas de marquage par défaut, switches et routeurs n'en ajoutent pas (Packet Tracer affiche le champ en hexadécimal et n'affiche pas l'ECN).
- **Configuration** :

```
R1(config)# class-map HTTPS_MAP
R1(config-cmap)# match protocol https
R1(config-cmap)# exit
R1(config)# class-map HTTP_MAP
R1(config-cmap)# match protocol http
R1(config-cmap)# exit
R1(config)# class-map ICMP_MAP
R1(config-cmap)# match protocol icmp
R1(config-cmap)# exit
R1(config)# do show run | section class-map
R1(config)# policy-map G0/0/0_OUT
R1(config-pmap)# class HTTPS_MAP
R1(config-pmap-c)# set ip dscp af31
R1(config-pmap-c)# priority percent 10
R1(config-pmap-c)# exit
R1(config-pmap)# class HTTP_MAP
R1(config-pmap-c)# set ip dscp af32
R1(config-pmap-c)# bandwidth percent 10
R1(config-pmap-c)# exit
R1(config-pmap)# class ICMP_MAP
R1(config-pmap-c)# set ip dscp cs2
R1(config-pmap-c)# bandwidth percent 5
R1(config-pmap-c)# exit
R1(config-pmap)# exit
R1(config)# do show running-config | section policy-map
R1(config)# interface g0/0/0
R1(config-if)# service-policy output G0/0/0_OUT
R1(config-if)# end
R1# show running-config
```

- Le trafic qui ne correspond à aucune classe n'est pas marqué et ne reçoit aucun traitement particulier.
- **Vérifications** en mode simulation, paquet arrivé à R1, onglets Inbound (DSCP 0) puis Outbound :
  - `ping 10.0.0.100` : DSCP **0x10** = CS2 = 010000 = 16.
  - Navigateur `http://10.0.0.100` : DSCP **0x1C** = AF32 = 011100 = 28 (16+8+4).
  - Navigateur `https://10.0.0.100` : DSCP **0x1A** = AF31 = 011010 = 26 (16+8+2).
- Résumé : les class-maps identifient le trafic, les policy-maps définissent les actions, les service-policies appliquent les policy-maps aux interfaces. Pas de lab QoS dans Boson NetSim (hors programme).

### 11. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quels marquages CoS correspondent à la pratique standard ? (trois réponses) | **B** CoS 0 best effort, **D** CoS 5 voix, **E** CoS 4 vidéo | Ce sont les valeurs PCP/CoS standard (802.1p). On n'est pas obligé de les suivre dans son réseau, mais c'est la pratique standard. |
| Motif de bits dans le champ DSCP d'un paquet marqué EF ? | **D** : 101 110 | EF (faible délai, gigue, perte) = DSCP 46 décimal = 101110. |
| Quel marquage AF offre le meilleur service ? | **B** : AF41 | Classe la plus haute et drop precedence la plus basse. AF43 est dans la même classe mais avec une drop precedence plus élevée. AF51 et AF61 n'existent pas (classes 1 à 4 seulement). |
| Bonne pratique générale en QoS ? | **A** : faire confiance aux marquages des téléphones IP, pas à ceux des PC | Les téléphones marquent la voix EF / CoS 5, à conserver. Le trafic des applications PC doit rester en basse priorité pour ne pas remplir les files réservées à la voix ; Zoom ou WebEx sur PC peuvent être marqués au switch ou au routeur. |
| Qu'est-ce qui crée une file de priorité stricte pour le trafic exigeant faible délai, gigue et perte ? | **B** : LLQ | Low Latency Queuing : si la file contient des paquets, l'ordonnanceur les envoie toujours avant ceux des autres files. |

---

## 🇬🇧 English version

Goal of the video: the terms of exam topic 4.7: **classification, marking, queuing, congestion, policing, shaping**. QoS design and configuration are not CCNA topics; understand the concepts.

### 1. Classification

- **Classification** organizes network traffic (packets) into **traffic classes**. It is fundamental to QoS: to prioritize certain traffic, you first have to identify it.
- Methods: an **ACL** (permitted traffic gets a certain treatment, like ACLs for dynamic NAT: the ACL identifies traffic, it does not filter); **NBAR** (Network Based Application Recognition), which performs **deep packet inspection** up to Layer 7 when TCP/UDP ports and IP addresses are not enough.
- Dedicated header fields: the **PCP** (Priority Code Point) of the **802.1Q** tag (Layer 2, only usable when a VLAN tag is present) and the **DSCP** (Differentiated Services Code Point) of the IP header (Layer 3).

### 2. Layer 2 marking: PCP / CoS

- **PCP** field, **3 bits** in the dot1q tag, also called **CoS** (Class of Service): don't confuse CoS (this field) with the whole concept of QoS. Its use is defined by **IEEE 802.1p**. 8 values (0 to 7). Remember: **0 = best effort**, **3 = critical applications**, **4 = video**, **5 = voice**.
- **Best effort**: no guarantee of delivery or of meeting any QoS standard; regular traffic, **default value 0**.
- IP phones mark **call signaling** traffic (used to establish calls) as **PCP 3** and the **audio** itself as **PCP 5**.
- To **mark** = to set the value of the PCP or DSCP field; devices read those markings to classify traffic.
- **Major limitation of PCP**: it only exists where there is a dot1q tag: **trunk links** (except native VLAN) and **access links with a voice VLAN** (phone traffic). PC traffic on an access port, and traffic between routers (R1-R2, R2 to external destinations) carry no tag: no PCP marking possible. Layer 3 classification does not have this limitation.

### 3. Layer 3 marking: ToS byte, IPP, DSCP

- In the IPv4 header, the **ToS** (Type of Service) byte, the second one after version and IHL (IPv6 has a **Traffic Class** byte).
- **Old use**: 3 bits **IPP** (IP Precedence, 8 values, like PCP) and 5 largely unused bits. IPP markings: **6 and 7 reserved for network control** (e.g. OSPF messages between routers), **5 interactive voice**, **4 interactive video**, **3 voice signaling**, **0 best effort**. Only 6 usable values, not enough for complex networks.
- **Current use**: **6 bits DSCP** (64 values) + **2 bits ECN** (Explicit Congestion Notification). DSCP = IPP + 3 bits. Defined by **RFC 2474 (1998)**, elaborated by later **DiffServ** (Differentiated Services) RFCs. Standard markings simplify QoS design and make it work better between ISPs and enterprises.

### 4. Standard DSCP markings

- **DF** (Default Forwarding): best effort, **DSCP 0** (000000). Same value as CS0.
- **EF** (Expedited Forwarding): traffic requiring **low loss, latency and jitter**, usually **voice**: **DSCP 46** (**101110**).
- **AF** (Assured Forwarding): a set of **12 values**. **4 classes** (left 3 bits; higher class = higher priority) and, within each class, **3 levels of drop precedence** (2 bits; higher = more likely to be dropped by WRED during congestion); the last bit is always 0. Written **AF XY**: X = class, Y = drop precedence. **Formula: DSCP = 8X + 2Y**. Examples from the video: AF11 = 001010 = 10; AF12 = 001100 = 12; AF23 = 22; AF32 = 011100 = 28; AF43 = 38 (highest AF value: no class 5, 6 or 7). **AF41** = best treatment (highest class, lowest drop precedence), **AF13** = worst.
- **CS** (Class Selector): **8 values** for **backward compatibility with IPP**: the 3 added bits are 0, the original 3 IPP bits give CS0 to CS7. **DSCP = 8 × CS number**: CS0 = 0, CS1 = 8, CS2 = 16, CS3 = 24, CS4 = 32, CS5 = 40, CS6 = 48, CS7 = 56.
- In IOS, `class-map TEST` then `match dscp ?` lists: decimal 0-63, the 12 AF values (with binary, e.g. AF11 = 001 010), 7 CS values (CS0 = DF) and EF.
- **RFC 4594 recommendations** (developed with Cisco's help): **voice = EF**; **interactive video = AF4x**; **streaming video = AF3x**; **high-priority data = AF2x**; **best effort = DF**. These are recommendations: the engineer designing the QoS policy decides.

### 5. Trust boundaries

- Defines where devices **trust** received QoS markings (forwarded unchanged) or **don't trust** them (markings changed according to the configured policy).
- Example: boundary at SW1: a message marked EF / CoS 5 from the phone is re-marked DF / CoS 0 before being forwarded to R1, then R2 (DF only, no dot1q header). Not ideal.
- Recommendation: if an IP phone is connected, **move the trust boundary to the IP phone** (configured on the **switch port**, not on the phone). Phone markings are kept; a PC marking its traffic EF (DSCP 46) gets re-marked DF (DSCP 0). Apps like Zoom or WebEx on a PC do need priority, but their packets can be marked at the switch or router.

### 6. Queuing and congestion management

- Review: full queue = **tail drop**; **RED/WRED** drop early to avoid it.
- An essential part of QoS: **multiple queues**. The router classifies traffic (DSCP, etc.) and places it in the appropriate queue. Only one frame can be forwarded at a time, so a **scheduler** decides which queue the next packet is taken from; **prioritization** gives some queues more weight.
- Process: **ingress** traffic, **routing** (choice of exit interface, NAT...), **classification**, **queuing**, **scheduling**, **transmission**.
- **Weighted round-robin**: packets are taken from each queue in turn, cyclically (round-robin), and more data is taken from high-priority queues (weighted).
- **CBWFQ** (Class-Based Weighted Fair Queuing): weighted round-robin scheduling that **guarantees each queue a percentage of the interface's bandwidth** during congestion.
- Limit for voice/video: even high-priority queues wait their turn, adding delay and jitter. Solution: **LLQ** (Low Latency Queuing): one or more **strict priority** queues: if there is traffic in it, the scheduler always takes the next packet from it until empty. Downside: it can **starve** other queues; **policing** limits the traffic allowed in the priority queue.
- Within each queue, RED or WRED can be used to avoid tail drop.
- Marking a packet EF does nothing on its own: tools like CBWFQ and LLQ make devices treat it as high priority.

### 7. Shaping and policing

- Both **control the rate of traffic**, limiting it to a configured rate below the link's actual capacity.
- **Shaping**: **buffers** traffic in a queue if the rate exceeds the configured rate.
- **Policing**: **drops** traffic over the configured rate, but allows **burst** traffic for a short time, for "bursty" data applications; the burst size is configurable. Classification allows different rates for different traffic.
- Common use: a customer connected to an ISP with Gigabit interfaces (1000 Mbps) but paying for **300 Mbps**: the ISP configures **inbound policing** at 300 Mbps on its G0/0; the customer configures **outbound shaping** at 300 Mbps on its G0/0 so the ISP does not drop its traffic.

### 8. Exam traps

- **CoS = PCP** (3 bits of the dot1q tag), not the whole of QoS; standard markings: 0 best effort, 3 critical applications / signaling, 4 video, 5 voice.
- PCP exists only on **trunks** and **access ports with a voice VLAN**; not on router-to-router links.
- **EF = DSCP 46 = 101110**; **DF = 0**; **AF = 8X + 2Y**; **CS = 8 × n**. AF only has classes 1 to 4: **AF51, AF61 do not exist**. **AF41** is the best AF service.
- Best practice: **trust markings from IP phones, don't trust markings from PCs**.
- **LLQ** creates the strict priority queue for low delay/jitter/loss traffic; CBWFQ guarantees bandwidth but without strict priority.
- **Shaping buffers, policing drops** (bursts allowed).
- **PHB** (per-hop behavior, from the lab): QoS configured on R1 only applies to the hop to R2; each router must be configured.

### 9. IOS commands

Shown as a demo only (not a CCNA exam topic): three steps: **class-map** (identify traffic), **policy-map** (actions), **service-policy** (apply to an interface).

```
R1(config)# class-map HTTPS_MAP                 ! identifies traffic; match-all by default (match-any: one match statement is enough)
R1(config-cmap)# match protocol https           ! match HTTPS traffic
R1(config)# class-map TEST
R1(config-cmap)# match dscp ?                   ! list of values: 0-63, AF11..AF43, CS1..CS7, EF
R1(config)# policy-map G0/0/0_OUT               ! actions to apply
R1(config-pmap)# class HTTPS_MAP
R1(config-pmap-c)# set ip dscp af31             ! mark packets AF31
R1(config-pmap-c)# priority percent 10          ! priority queue (LLQ) with at least 10% of bandwidth
R1(config-pmap-c)# bandwidth percent 10         ! queue guaranteed 10% (CBWFQ), no strict priority
R1(config)# interface g0/0/0
R1(config-if)# service-policy output G0/0/0_OUT ! apply the policy map outbound
R1# show running-config | section class-map     ! check the class maps
R1# show running-config | section policy-map    ! check the policy map
```

### 10. The lab: basic QoS configuration

- **Topology**: PC1 – SW1 – R1 – R2 – SW2 – SRV1 (10.0.0.100, also PC1's DNS server, resolving jeremysitlab.com to 10.0.0.100). Assume many more PCs behind R1 and a congested network.
- **Goal** on R1, traffic out of G0/0/0: HTTPS marked **AF31**, **at least 10%** bandwidth in a **priority queue**; HTTP marked **AF32**, **at least 10%**, no priority queue; ICMP marked **CS2**, **at least 5%**. Random values for demonstration (a priority queue for HTTPS is uncommon; usually it is for voice).
- **PHB**: R1 prioritizes over the hop to R2; R2 treats everything equally unless configured too. QoS must be configured all across the network wherever needed.
- **Before configuration**: `ping jeremysitlab.com` from PC1 (DNS query to SRV1, then ping); in simulation mode, "Outbound PDU Details" at R1 shows **DSCP 0x00**: PCs send unmarked traffic by default and switches/routers add no markings (Packet Tracer shows the field in hexadecimal and does not display ECN).
- **Configuration**:

```
R1(config)# class-map HTTPS_MAP
R1(config-cmap)# match protocol https
R1(config-cmap)# exit
R1(config)# class-map HTTP_MAP
R1(config-cmap)# match protocol http
R1(config-cmap)# exit
R1(config)# class-map ICMP_MAP
R1(config-cmap)# match protocol icmp
R1(config-cmap)# exit
R1(config)# do show run | section class-map
R1(config)# policy-map G0/0/0_OUT
R1(config-pmap)# class HTTPS_MAP
R1(config-pmap-c)# set ip dscp af31
R1(config-pmap-c)# priority percent 10
R1(config-pmap-c)# exit
R1(config-pmap)# class HTTP_MAP
R1(config-pmap-c)# set ip dscp af32
R1(config-pmap-c)# bandwidth percent 10
R1(config-pmap-c)# exit
R1(config-pmap)# class ICMP_MAP
R1(config-pmap-c)# set ip dscp cs2
R1(config-pmap-c)# bandwidth percent 5
R1(config-pmap-c)# exit
R1(config-pmap)# exit
R1(config)# do show running-config | section policy-map
R1(config)# interface g0/0/0
R1(config-if)# service-policy output G0/0/0_OUT
R1(config-if)# end
R1# show running-config
```

- Traffic matching none of the classes is not marked and gets no special QoS treatment.
- **Verification** in simulation mode, packet at R1, Inbound PDU details (DSCP 0) then Outbound:
  - `ping 10.0.0.100`: DSCP **0x10** = CS2 = 010000 = 16.
  - Browser `http://10.0.0.100`: DSCP **0x1C** = AF32 = 011100 = 28 (16+8+4).
  - Browser `https://10.0.0.100`: DSCP **0x1A** = AF31 = 011010 = 26 (16+8+2).
- Summary: class maps identify traffic, policy maps specify actions, service policies apply policy maps to interfaces. No QoS labs in Boson NetSim (not an exam topic).

### 11. The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which CoS markings are consistent with standard practice? (select three) | **B** CoS 0 best effort, **D** CoS 5 voice, **E** CoS 4 video | These are the standard PCP/CoS values (802.1p). You don't have to follow this scheme in your network, but it is standard practice. |
| Bit pattern in the DSCP field of a packet marked EF? | **D**: 101 110 | EF (low delay, jitter, loss) = decimal DSCP 46 = 101110. |
| Which AF marking provides the best service? | **B**: AF41 | Highest priority class with the lowest drop precedence. AF43 is in the same class but with higher drop precedence. AF51 and AF61 are not real AF markings (classes 1 to 4 only). |
| General best practice regarding QoS? | **A**: trust markings from IP phones, don't trust markings from PCs | Phones mark voice EF / CoS 5, which should be trusted. PC data applications should be low priority so they don't fill the queues reserved for voice; Zoom or WebEx on a PC can be marked at the switch or router. |
| What creates a strict priority queue for data requiring low delay, jitter and loss? | **B**: LLQ | Low Latency Queuing: if there are packets in that queue, the scheduler always forwards them next, before the other queues. |
