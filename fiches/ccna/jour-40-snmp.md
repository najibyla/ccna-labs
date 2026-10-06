# CCNA Day 40 : SNMP / Simple Network Management Protocol

> Source : Jeremy's IT Lab, « Free CCNA | SNMP | Day 40 » (29 min, vidéo n°81 de la playlist, cours) et « Free CCNA | SNMP | Day 40 Lab » (14 min, vidéo n°82, lab Packet Tracer). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Vue d'ensemble

- Sujet d'examen **4.4** : expliquer la **fonction de SNMP dans l'exploitation du réseau**. Pas besoin de connaître le fonctionnement détaillé, la mise en place d'un serveur ni la configuration : seulement le **rôle et l'objectif**.
- SNMP est un **cadre et protocole standard de l'industrie**, publié en **1988**. On le voit comme un protocole, mais il s'inscrit dans un cadre plus large de gestion de réseau (*SNMP framework*). RFC d'origine (pas à mémoriser) : **RFC 1065, 1066, 1067** = SNMPv1 (RFC = *Request For Comments*, standards de l'IETF). Le « simple » du nom est trompeur : SNMPv3 est assez compliqué.
- SNMP sert à **surveiller l'état des équipements, modifier leur configuration**, etc.
- Deux types d'équipements :
  - **Équipements gérés** (*managed devices*) : routeurs, switches... surveillés via SNMP.
  - **NMS** (*Network Management Station*, ou *System*) : l'équipement qui gère les équipements gérés ; c'est le « serveur » SNMP, mais on dit **NMS** plutôt que serveur SNMP.
- **Trois opérations principales** (exemple : SRV1 = NMS, R1 et SW1 = équipements gérés) :
  1. L'équipement géré **notifie** le NMS d'un événement (ex. G0/1 de SW1 passe DOWN) ; le logiciel du NMS peut alors avertir l'administrateur.
  2. Le NMS **interroge** l'équipement géré sur son état (ex. « quelle est ton utilisation CPU ? », réponse « 50 % »).
  3. Le NMS **modifie** la configuration de l'équipement géré (ex. changer l'IP de G0/1 de 203.0.113.1/30 en 203.0.113.5/30 ; R1 change et confirme).

### 2. Composants

- Côté **NMS** (pas forcément une machine dédiée : peut être le PC de l'admin) :
  - **SNMP Manager** : logiciel qui interagit avec les équipements gérés (reçoit les notifications, envoie les demandes d'information et les changements de configuration).
  - **SNMP Application** : interface pour l'administrateur (alertes, statistiques, graphiques ; exemple SolarWinds).
- Côté **équipement géré** (*SNMP entity*) :
  - **SNMP Agent** : logiciel qui interagit avec le Manager (envoie des notifications, reçoit des messages).
  - **MIB** (*Management Information Base*) : structure contenant les **variables** gérées par SNMP, chacune identifiée par un **Object ID (OID)** : état des interfaces, débit, utilisation CPU, température...
- Les **OID** sont organisés **hiérarchiquement**. Exemple : iso → identified-organization → dod → internet → mgmt → mib-2 → system → **sysName** (nom d'hôte). Le NMS demande « quelle valeur as-tu pour cet OID ? », SW1 répond avec son hostname. (Référence de Jeremy : oid-info.com.)

### 3. Les versions

Seules **trois** versions sont largement utilisées :

| Version | Caractéristiques |
| :--- | :--- |
| **SNMPv1** | Version d'origine. |
| **SNMPv2c** | La plus répandue des v2. Ajoute un type de message permettant de récupérer **de grandes quantités d'informations en une seule requête** (plus efficace, moins de trafic). Le **« c »** = **community strings**, mots de passe présents dans v1, retirés de v2, remis dans v2c. |
| **SNMPv3** | La meilleure : **beaucoup plus sûre**, **chiffrement fort et authentification** ; seuls les équipements visés peuvent lire les messages. |

### 4. Les messages

| Classe | Message | Rôle |
| :--- | :--- | :--- |
| **Read** (NMS → équipement) | **Get** | Demande la valeur d'une ou plusieurs variables (OID) ; l'agent répond par un **Response**. |
| | **GetNext** | « Donne-moi l'OID suivant » : découvrir les variables disponibles dans la MIB. |
| | **GetBulk** | Version plus efficace de GetNext, introduite dans **SNMPv2**. |
| **Write** (NMS → équipement) | **Set** | Change la valeur d'une ou plusieurs variables (ex. hostname SW1 → SW10) ; l'agent répond par un Response avec les nouvelles valeurs. |
| **Notification** (équipement → NMS) | **Trap** | Notification **sans Response** du manager : **non fiable** (et SNMP utilise **UDP**, pas de retransmission TCP). |
| | **Inform** | Comme Trap mais **acquitté par un Response** : fiabilité intégrée au message. À l'origine entre managers ; les agents peuvent maintenant en envoyer. |
| **Response** | **Response** | Réponse à un Get, Set ou Inform. |

**Ports** (déjà vus au Day 30) : **l'agent écoute sur UDP 161, le manager (NMS) sur UDP 162.** À retenir absolument.

### 5. Configuration de base (SNMPv2c, R1 géré, PC1 = NMS)

- `snmp-server contact ...` et `snmp-server location ...` : informations optionnelles.
- `snmp-server community Jeremy1 ro` : community string en **lecture seule** (*read only*) : Get possible, pas de Set.
- `snmp-server community Jeremy2 rw` : **lecture/écriture** (*read/write*) : Get et Set.
- Community strings **par défaut** : **`public`** (RO) et **`private`** (RW), à ne pas garder (moins sûr).
- `snmp-server host 192.168.1.1 version 2c Jeremy1` : adresse du NMS, version, community à utiliser avec ce serveur (ici RO : PC1 ne pourra pas faire de Set ; Jeremy2 n'est pas utilisé).
- `snmp-server enable traps linkdown linkup` et `snmp-server enable traps config` : traps envoyés quand une interface change d'état ou que la configuration change.
- Capture Wireshark d'un Trap **linkDown** (R1 → PC1) : version 2c, community Jeremy1 **en clair**. **SNMPv1 et v2c n'ont aucun chiffrement** : community et contenu en texte clair, facilement capturables. D'où la préférence pour **SNMPv3** (configuration plus compliquée, non montrée).

### 6. Pièges d'examen

- **UDP 161 = agent (équipement géré), UDP 162 = manager (NMS).** Trap et Inform vont vers **162** ; Get et Set vers **161**.
- **Trap = sans Response, non fiable** (jamais renvoyé en cas de perte). **Inform = acquitté.**
- **GetBulk** = introduit en **SNMPv2**, récupération en masse ; « SetBulk » n'existe pas.
- Le **SNMP Manager** tourne sur le NMS ; le **SNMP Agent** et la **MIB** sur l'équipement géré.
- Get, GetNext, GetBulk : **extraire** ; Set : **modifier** (question Boson).
- v1 et v2c : **community strings en clair** ; v3 : **chiffrement et authentification**.

### 7. Commandes IOS

```text
R1(config)# snmp-server contact Jeremy             ! optionnel
R1(config)# snmp-server location Tokyo             ! optionnel
R1(config)# snmp-server community Jeremy1 ro       ! community lecture seule (défaut : public)
R1(config)# snmp-server community Jeremy2 rw       ! community lecture/écriture (défaut : private)
R1(config)# snmp-server host 192.168.1.1 version 2c Jeremy1 ! NMS, version, community
R1(config)# snmp-server enable traps linkdown linkup ! traps d'état d'interface
R1(config)# snmp-server enable traps config        ! traps de changement de configuration
R1# show snmp                                      ! vue d'ensemble (NetSim)
R1# show snmp community                            ! communities (NetSim)
R1# show snmp host                                 ! NMS, UDP 162, community, version (NetSim)
R1# show snmp location / show snmp contact         ! (NetSim)
```

### 8. Le lab (vidéo n°82)

SNMP est **très limité dans Packet Tracer** : `snmp-server ?` ne propose que `community`, pas de `host` (impossible d'indiquer un serveur pour les traps).

1. **R1** : `snmp-server community Cisco1 ro`, `snmp-server community Cisco2 rw`.
2. **PC1 (NMS)** : Desktop → **MIB Browser**. Adresse 192.168.1.254 (R1) ; Advanced : Read community Cisco1, Write community Cisco2, version SNMPv1. Arbre MIB : router_std MIBs → iso → org → dod → internet → mgmt → mib-2 → system → **sysUpTime**, opération **Get**, GO : OID et valeur (temps de fonctionnement). **sysName** → R1. Dans *interfaces* : **ifNumber** = 4 ; ifTable → ifEntry → **ifDescr** (Vlan1, G0/0, G0/1, G0/2), **ifType** (cuivre, pas fibre), **ifAdminStatus** (seule G0/0 up).
3. **Set** : Get sur sysName, puis opération **Set**, type de données **OctetString**, nouvelle valeur R11, GO : la valeur change ; dans le CLI de R1 l'invite devient `R11`, `do show run | include host` confirme.

Bonus Boson NetSim (lab ENCOR 350-401, pas de lab SNMP dans NetSim CCNA car hors programme) : `snmp-server community Boson ro`, `snmp-server contact snmp@boson.com`, `snmp-server location R1_SNMP`, `snmp-server host 10.10.0.2 snmp_logs` (la version 2 n'était pas acceptée dans NetSim) ; vérification `show snmp`, `show snmp community` (une community par défaut apparaît, absente de la config), `show snmp location`, `show snmp contact`, `show snmp host` (**UDP port 162**, traps activés par défaut, security model version 1).

### 9. Le quiz (5 questions + 1 Boson)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quels messages SNMP servent au NMS à « lire » des informations des équipements gérés ? (tous ceux qui s'appliquent) | **Get** (D) et **GetNext** (G) | GetBulk sert aussi à lire mais n'est pas dans les options ; **SetBulk** (F) n'existe pas. |
| Quels messages SNMP sont envoyés au port UDP 162 ? (tous ceux qui s'appliquent) | **Inform** (A) et **Trap** (B) | Le NMS écoute sur UDP 162 ; Inform et Trap vont de l'équipement géré vers le NMS. Set et Get vont vers l'équipement géré, qui écoute sur 161. |
| Quel message, introduit dans SNMPv2, permet la récupération en masse d'informations ? | **GetBulk** (D) | Version optimisée de GetNext pour découvrir les variables de la MIB. |
| Quel logiciel tourne sur un NMS SNMP ? | **SNMP Manager** (C) | Il interagit avec l'Agent des équipements gérés, envoie et reçoit les messages. |
| Quel message SNMP est envoyé sans attendre de Response ? | **Trap** (D) | Non acquitté, donc non fiable ; en cas de perte, l'équipement ne le renvoie pas. |
| Boson : quelles actions SNMP un NMS utilise-t-il pour extraire des informations d'un agent ? (deux) | **GetNext** (C) et **Get** (E) | Inform et Trap vont de l'agent vers le NMS ; Set modifie une variable, il n'extrait pas. |

---

## 🇬🇧 English version

### 1. Overview

- Exam topic **4.4**: explain the **function of SNMP in network operations**. No need to know its detailed workings, how to set up a server or configure it: just its **role and purpose**.
- SNMP is an **industry-standard framework and protocol**, originally released in **1988**. Usually seen as a single protocol, it actually fits into a larger network management framework (the SNMP framework). Original RFCs (no need to memorize): **RFC 1065, 1066, 1067** = SNMPv1 (RFC = Request For Comments, IETF standards). Don't let "simple" fool you: SNMPv3 is fairly complicated.
- SNMP is used to **monitor device status, make configuration changes**, etc.
- Two main device types:
  - **Managed devices**: routers, switches... monitored with SNMP.
  - **NMS** (Network Management Station, or System): the device managing the managed devices; the SNMP "server", though the term **NMS** is used instead.
- **Three main operations** (example: SRV1 = NMS, R1 and SW1 = managed devices):
  1. The managed device **notifies** the NMS of an event (e.g. SW1's G0/1 goes DOWN); the NMS software may then notify the admin.
  2. The NMS **asks** the managed device for status information (e.g. "what is your CPU usage?", reply "50%").
  3. The NMS **tells** the managed device to change its configuration (e.g. change G0/1's IP from 203.0.113.1/30 to 203.0.113.5/30; R1 changes it and confirms).

### 2. Components

- On the **NMS** (not necessarily a dedicated machine: could be the admin's PC):
  - **SNMP Manager**: software that interacts with the managed devices (receives notifications, sends information requests and configuration changes).
  - **SNMP Application**: the admin's interface (alerts, statistics, charts; e.g. SolarWinds).
- On the **managed device** (SNMP entity):
  - **SNMP Agent**: software that interacts with the Manager (sends notifications, receives messages).
  - **MIB** (Management Information Base): the structure holding the **variables** managed by SNMP, each identified by an **Object ID (OID)**: interface status, throughput, CPU usage, temperature...
- **OIDs** are organized **hierarchically**. Example: iso → identified-organization → dod → internet → mgmt → mib-2 → system → **sysName** (host name). The NMS asks "what value do you have for this OID?", SW1 replies with its hostname. (Jeremy's reference: oid-info.com.)

### 3. Versions

Only **three** versions achieved widespread use:

| Version | Characteristics |
| :--- | :--- |
| **SNMPv1** | The original. |
| **SNMPv2c** | Most widely used v2. Adds a message type that retrieves **large amounts of information in a single request** (more efficient, less traffic). The **"c"** = **community strings**, passwords used in v1, removed from v2, added back in v2c. |
| **SNMPv3** | The best so far: **much more secure**, **strong encryption and authentication**; only the intended devices can read the messages. |

### 4. Messages

| Class | Message | Role |
| :--- | :--- | :--- |
| **Read** (NMS → device) | **Get** | Requests the value of one or more variables (OIDs); the agent sends a **Response**. |
| | **GetNext** | "Tell me the next OID": discover the variables available in the MIB. |
| | **GetBulk** | More efficient version of GetNext, introduced in **SNMPv2**. |
| **Write** (NMS → device) | **Set** | Changes the value of one or more variables (e.g. hostname SW1 → SW10); the agent sends a Response with the new values. |
| **Notification** (device → NMS) | **Trap** | Notification **without a Response** from the manager: **unreliable** (and SNMP uses **UDP**, no TCP retransmissions). |
| | **Inform** | Like a Trap but **acknowledged with a Response**: reliability built into the message. Originally between managers; later updates let agents send them too. |
| **Response** | **Response** | Reply to a Get, Set or Inform. |

**Ports** (from Day 30): **agents listen on UDP 161, managers (NMS) listen on UDP 162.** Make sure you remember them.

### 5. Basic configuration (SNMPv2c, R1 managed, PC1 = NMS)

- `snmp-server contact ...` and `snmp-server location ...`: optional information.
- `snmp-server community Jeremy1 ro`: **read-only** community string: Get allowed, no Set.
- `snmp-server community Jeremy2 rw`: **read/write**: Get and Set.
- **Default** community strings: **`public`** (RO) and **`private`** (RW), best not to use them (less secure).
- `snmp-server host 192.168.1.1 version 2c Jeremy1`: NMS address, version, community to use with this server (RO here: PC1 cannot Set; Jeremy2 is unused).
- `snmp-server enable traps linkdown linkup` and `snmp-server enable traps config`: traps sent when an interface changes state or the configuration changes.
- Wireshark capture of a **linkDown** Trap (R1 → PC1): version 2c, community Jeremy1 **in plain text**. **SNMPv1 and v2c have no encryption**: community and contents in plain text, easily captured. Hence **SNMPv3** is preferred (more complex configuration, not shown).

### 6. Exam traps

- **UDP 161 = agent (managed device), UDP 162 = manager (NMS).** Trap and Inform go to **162**; Get and Set go to **161**.
- **Trap = no Response, unreliable** (never resent if lost). **Inform = acknowledged.**
- **GetBulk** = introduced in **SNMPv2**, mass retrieval; "SetBulk" does not exist.
- The **SNMP Manager** runs on the NMS; the **SNMP Agent** and **MIB** on the managed device.
- Get, GetNext, GetBulk: **extract**; Set: **change** (Boson question).
- v1 and v2c: **community strings in plain text**; v3: **encryption and authentication**.

### 7. IOS commands

```text
R1(config)# snmp-server contact Jeremy             ! optional
R1(config)# snmp-server location Tokyo             ! optional
R1(config)# snmp-server community Jeremy1 ro       ! read-only community (default: public)
R1(config)# snmp-server community Jeremy2 rw       ! read/write community (default: private)
R1(config)# snmp-server host 192.168.1.1 version 2c Jeremy1 ! NMS, version, community
R1(config)# snmp-server enable traps linkdown linkup ! interface state traps
R1(config)# snmp-server enable traps config        ! configuration change traps
R1# show snmp                                      ! overview (NetSim)
R1# show snmp community                            ! communities (NetSim)
R1# show snmp host                                 ! NMS, UDP 162, community, version (NetSim)
R1# show snmp location / show snmp contact         ! (NetSim)
```

### 8. The lab (video #82)

SNMP is **very limited in Packet Tracer**: `snmp-server ?` only offers `community`, no `host` (no way to specify a trap receiver).

1. **R1**: `snmp-server community Cisco1 ro`, `snmp-server community Cisco2 rw`.
2. **PC1 (NMS)**: Desktop → **MIB Browser**. Address 192.168.1.254 (R1); Advanced: Read community Cisco1, Write community Cisco2, version SNMPv1. MIB tree: router_std MIBs → iso → org → dod → internet → mgmt → mib-2 → system → **sysUpTime**, **Get** operation, GO: OID and value (uptime). **sysName** → R1. Under *interfaces*: **ifNumber** = 4; ifTable → ifEntry → **ifDescr** (Vlan1, G0/0, G0/1, G0/2), **ifType** (copper, not fiber), **ifAdminStatus** (only G0/0 up).
3. **Set**: Get on sysName, then **Set** operation, data type **OctetString**, new value R11, GO: the value changes; in R1's CLI the prompt becomes `R11`, `do show run | include host` confirms.

Boson NetSim bonus (ENCOR 350-401 lab, no SNMP lab in NetSim for CCNA since it's not an exam topic): `snmp-server community Boson ro`, `snmp-server contact snmp@boson.com`, `snmp-server location R1_SNMP`, `snmp-server host 10.10.0.2 snmp_logs` (version 2 was not accepted in NetSim); verify with `show snmp`, `show snmp community` (a default community appears, absent from the config), `show snmp location`, `show snmp contact`, `show snmp host` (**UDP port 162**, traps enabled by default, security model version 1).

### 9. The quiz (5 questions + 1 Boson)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which SNMP messages are used by the NMS to "read" information from managed devices? (select all that apply) | **Get** (D) and **GetNext** (G) | GetBulk also reads but is not among the options; **SetBulk** (F) is not a real message. |
| Which SNMP messages are sent to UDP port 162? (select all that apply) | **Inform** (A) and **Trap** (B) | The NMS listens on UDP 162; Informs and Traps go from managed devices to the NMS. Set and Get go to managed devices, which listen on 161. |
| Which message, introduced in SNMPv2, allows mass retrieval of information? | **GetBulk** (D) | Optimized version of GetNext for discovering variables in the MIB. |
| Which software runs on an SNMP NMS? | **SNMP Manager** (C) | It interacts with the Agent on managed devices, sending and receiving messages. |
| Which SNMP message is sent without expecting a Response? | **Trap** (D) | Not acknowledged, hence unreliable; if lost, the device won't send it again. |
| Boson: which SNMP actions does an NMS use to extract information from an agent? (two) | **GetNext** (C) and **Get** (E) | Inform and Trap go from the agent to the NMS; Set changes a variable, it doesn't extract. |
