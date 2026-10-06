# CCNA Day 55 : Wireless Fundamentals / Fondamentaux du sans-fil

> Source : Jeremy's IT Lab, « Free CCNA | Wireless Fundamentals | Day 55 » (36 min), vidéo n°113 de la playlist. Pas de lab pour ce jour. Fiche rédigée à partir de la transcription le 6 octobre 2026. Sujets d'examen : 1.1.d (access points), 1.11.a (canaux Wi-Fi non chevauchants), 1.11.b (SSID), 1.11.c (RF).

## 🇫🇷 Version française

### 1. Les réseaux locaux sans fil et la norme 802.11

- Les LAN sans fil sont définis dans **IEEE 802.11**, comme Ethernet filaire l'est dans **IEEE 802.3**.
- **Wi-Fi** est une marque de la **Wi-Fi Alliance**, organisme indépendant de l'IEEE, qui **teste et certifie** les équipements pour la conformité 802.11 et l'interopérabilité (logo « Wi-Fi certified »). Techniquement, « Wi-Fi » n'est pas le bon terme pour un LAN 802.11, mais c'est l'usage courant.

### 2. Les problèmes propres au sans-fil

- **Tous les appareils à portée reçoivent toutes les trames**, comme avec un **hub** Ethernet (un switch, lui, n'envoie la trame qu'au destinataire et permet le full-duplex). Le signal n'est pas contenu dans un câble : ondes électromagnétiques rayonnant depuis l'émetteur. Conséquences : **confidentialité** (il faut **chiffrer même dans le LAN**, contrairement au filaire où l'on ne chiffre en général que sur Internet) et **collisions**.
- **CSMA/CA** (*Carrier Sense Multiple Access with Collision Avoidance*) : évite les collisions **avant** qu'elles se produisent, pour une communication **half-duplex**. (En filaire, **CSMA/CD** détecte et récupère les collisions.) Déroulement simplifié : assembler la trame → écouter le canal → s'il n'est pas libre, attendre un temps aléatoire puis réécouter → s'il est libre, transmettre. Option non exigée pour l'examen : **RTS** (*request to send*) / **CTS** (*clear to send*).
- **Réglementation** : les communications sans fil sont régulées par des organismes internationaux et nationaux ; les canaux autorisés varient selon le pays. 802.11 précise les fréquences utilisables.
- **Zone de couverture** : portée du signal et facteurs qui l'altèrent :
  - **Absorption** : le signal traverse un matériau et se transforme en chaleur (un mur affaiblit le signal).
  - **Réflexion** (*reflection*) : le signal rebondit sur un matériau, par exemple le métal (mauvaise réception dans un ascenseur).
  - **Réfraction** (*refraction*) : l'onde est déviée en entrant dans un milieu où elle se propage à une vitesse différente (verre, eau ; la paille qui semble pliée dans un verre d'eau).
  - **Diffraction** : l'onde contourne un obstacle, ce qui crée des **zones d'ombre** (*blind spots*) derrière lui.
  - **Diffusion** (*scattering*) : le signal est dispersé dans toutes les directions par la poussière, le smog, les surfaces irrégulières.
- **Interférences** : d'autres appareils sur les mêmes canaux (le Wi-Fi du voisin).

### 3. Radiofréquence (RF) et ondes électromagnétiques

- L'émetteur applique un **courant alternatif à une antenne**, ce qui crée des champs électromagnétiques qui se propagent en ondes.
- **Amplitude** : force maximale des champs électrique et magnétique.
- **Fréquence** : nombre de cycles par unité de temps. **Hertz** = cycles par seconde ; kilohertz (milliers), mégahertz (millions), gigahertz (milliards), térahertz (billions). **Période** : durée d'un cycle (4 Hz → période de 0,25 s).
- Spectre visible : environ **400 THz à 790 THz**. **Radiofréquence : environ 30 Hz à 300 GHz**. Les LAN 802.11 utilisent des portions des plages **UHF** (*ultra high frequency*) et **SHF** (*super high frequency*).
- **Deux bandes principales** (à retenir, les plages exactes ne sont pas exigées) :
  - **Bande 2,4 GHz** : en réalité **2,4 GHz à 2,4835 GHz**. Portée plus grande en espace ouvert, meilleure pénétration des obstacles (murs), mais **plus d'appareils → plus d'interférences**.
  - **Bande 5 GHz** : en réalité **5,150 GHz à 5,825 GHz**, elle-même divisée en **quatre sous-bandes**.
  - **Wi-Fi 6 (802.11ax)** a étendu le spectre avec une bande dans les **6 GHz** (Jeremy n'est pas sûr que ce soit demandé à l'examen).

### 4. Les canaux

- Chaque bande est divisée en **canaux** ; un appareil émet et reçoit sur un ou plusieurs canaux (le **channel bonding** combine des canaux, non exigé).
- **Bande 2,4 GHz** : canaux de **22 MHz** chacun, liste variable selon le pays (le canal 14 au Japon est « 11b only », 802.11b étant une norme ancienne et lente). **Les canaux se chevauchent** : le canal 1 va de **2401 MHz à 2423 MHz** et chevauche les canaux 2, 3, 4 et 5.
- Un seul AP : n'importe quel canal. Plusieurs AP : les **AP adjacents ne doivent pas utiliser de canaux qui se chevauchent**, sinon performances réduites. **Recommandation 2,4 GHz : canaux 1, 6 et 11**, qui ne se chevauchent pas (hors Amérique du Nord d'autres combinaisons existent, mais pour le CCNA retenir 1-6-11).
- **Bande 5 GHz** : canaux **non chevauchants**, interférences entre AP plus faciles à éviter.
- Disposition en **nid d'abeille** (*honeycomb*) avec 1-6-11 : les **zones de couverture se chevauchent** pour une couverture complète, mais **pas les fréquences**.

### 5. Les normes 802.11

- De **802.11 original (1997)** à **802.11ax, Wi-Fi 6 (2019)**. Noms commerciaux : **802.11n = Wi-Fi 4**, **802.11ac = Wi-Fi 5**, **802.11ax = Wi-Fi 6** ; **pas de Wi-Fi 1, 2 ou 3 officiels**.
- Jeremy recommande de mémoriser pour l'examen **le nom de chaque norme, ses fréquences et son débit maximal théorique** (le tableau est sur une diapositive et n'apparaît pas dans la transcription ; utiliser les flashcards). Les débits maximaux sont **théoriques**, les débits réels sont bien inférieurs.
- Un appareil peut prendre en charge une, plusieurs ou toutes les normes : vérifier avant d'acheter. Exemple donné : l'iPhone X prend en charge **802.11a, b, g, n et ac**.

### 6. Les ensembles de services (*service sets*)

Trois types : **indépendant**, **infrastructure**, **maillé** (*mesh*). Tous les appareils d'un ensemble partagent le même **SSID** (*Service Set Identifier*), nom lisible qui identifie l'ensemble ; **il n'a pas à être unique**, mais c'est préférable.

- **IBSS** (*Independent Basic Service Set*) : deux appareils ou plus connectés **directement, sans AP** ; aussi appelé **réseau ad hoc** (exemple AirDrop). Pas évolutif au-delà de quelques appareils.
- **BSS** (*Basic Service Set*), type d'ensemble d'infrastructure : les clients communiquent **via un AP**, jamais directement entre eux, même à portée l'un de l'autre.
  - **BSSID** : identifie l'AP de façon **unique** = **adresse MAC de la radio de l'AP**. D'autres AP peuvent avoir le même SSID, pas le même BSSID.
  - Les appareils demandent à **s'associer** au BSS ; une fois associés, on les appelle **clients** ou **stations**.
  - **BSA** (*Basic Service Area*) : **zone physique** autour de l'AP où son signal est utilisable. BSS = groupe d'appareils ; BSA = zone.
- **ESS** (*Extended Service Set*), second type d'infrastructure : plusieurs BSS reliés par le **réseau filaire** (switch). **Même SSID**, **BSSID unique par BSS**, **canal différent par BSS** (BSS1 canal 1, BSS2 canal 6). **Roaming** : passer d'un AP à l'autre sans se reconnecter ; les BSA doivent se chevaucher d'environ **10 à 15 %**.
- **MBSS** (*Mesh Basic Service Set*) : quand il est difficile de tirer un câble Ethernet vers chaque AP. Les AP maillés ont **deux radios** : une pour le BSS des clients, une pour le **backhaul** entre AP. L'AP relié au réseau filaire est le **RAP** (*Root Access Point*), les autres sont des **MAP** (*Mesh Access Points*). Un protocole détermine le meilleur chemin dans le maillage (comme un protocole de routage).

### 7. Système de distribution et modes d'AP

- **DS** (*Distribution System*) : nom 802.11 du **réseau filaire** en amont. L'AP traduit entre les deux supports. Chaque BSS/ESS est **associé à un VLAN** (SSID « Jeremy's Wi-Fi » → VLAN 10).
- Un AP peut diffuser **plusieurs WLAN**, chacun avec son SSID et son VLAN, relié au switch par un **trunk** (Jeremy's Wi-Fi → VLAN 10, Guest Wi-Fi → VLAN 11). Chaque WLAN a un **BSSID unique**, en général en **incrémentant le dernier chiffre** (…3456 et …3457).
- **Repeater** (répéteur) : retransmet le signal de l'AP pour étendre le BSS. Avec **une seule radio**, même canal que l'AP → **débit effectif divisé par deux (50 %)**. Avec **deux radios**, il reçoit sur un canal et réémet sur un autre.
- **Workgroup bridge (WGB)** : l'AP agit comme **client d'un autre AP** pour connecter des appareils filaires au réseau sans fil. **uWGB** (*universal*, norme 802.11) : **un seul** appareil ponté ; **WGB** (propriétaire Cisco) : **plusieurs** clients filaires.
- **Outdoor bridge** : relie des réseaux sur de longues distances sans câble, avec des **antennes directionnelles**. **Point à point** ou **point à multipoint** (hub-and-spoke).

### 8. Pièges d'examen

- **CSMA/CA** pour le sans-fil (évitement), **CSMA/CD** pour le filaire (détection).
- Retenir les **deux bandes 2,4 GHz et 5 GHz** et les **canaux 1, 6, 11** en 2,4 GHz.
- **SSID** = nom, pas forcément unique ; **BSSID** = MAC de l'AP, unique. Dans un ESS : même SSID, BSSID différents, canaux non chevauchants.
- **BSS** (groupe d'appareils) ≠ **BSA** (zone physique).
- Mémoriser normes, fréquences et débits ; Wi-Fi 4/5/6 = n/ac/ax.

### 9. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| En bande 2,4 GHz, quels canaux choisir avec plusieurs AP ? | **1, 6 et 11** | Ils ne se chevauchent pas, donc pas d'interférence entre AP proches. |
| Réseau d'entreprise surtout filaire : rôle d'un AP ? | **Connecter les appareils sans fil au réseau filaire** | Le réseau filaire est le DS (distribution system) ; c'est le rôle principal de l'AP. |
| Bandes couramment utilisées par les WLAN ? (deux réponses) | **2,4 GHz** et **5 GHz** | Ces bandes sont divisées en canaux utilisés pour émettre et recevoir. |
| Affirmations vraies sur un ESS ? (deux réponses) | **Chaque BSS a un BSSID unique** ; **le roaming permet une connectivité transparente entre AP** | Faux : chaque BSS d'un ESS doit utiliser le **même** SSID ; les AP adjacents doivent utiliser des canaux **non** chevauchants. |
| Affirmation fausse sur un AP qui offre plusieurs BSS ? | **« Chaque BSS partage le même BSSID »** | Ils peuvent partager le SSID (même si un SSID unique par BSS est la bonne pratique), mais les BSSID doivent être uniques. |

---

## 🇬🇧 English version

### 1. Wireless LANs and the 802.11 standard

- Wireless LANs are defined in **IEEE 802.11**, just as wired Ethernet is defined in **IEEE 802.3**.
- **Wi-Fi** is a trademark of the **Wi-Fi Alliance**, not directly connected to the IEEE. It **tests and certifies** equipment for 802.11 compliance and interoperability ("Wi-Fi certified" mark). Technically Wi-Fi is not the correct term for 802.11 WLANs, but it is the common one.

### 2. Issues specific to wireless

- **All devices within range receive all frames**, like devices on an Ethernet **hub** (a switch forwards only to the recipient and allows full-duplex). The signal is not contained in a wire: electromagnetic waves radiate from the transmitter. Consequences: **data privacy** (encrypt **even within the LAN**, unlike wired networks where only Internet traffic is usually encrypted) and **collisions**.
- **CSMA/CA** (Carrier Sense Multiple Access with Collision Avoidance): avoids collisions **before** they occur, for **half-duplex** communications. (Wired networks use **CSMA/CD** to detect and recover from collisions.) Simplified flow: assemble the frame → listen to the channel → if not free, wait a random time and listen again → if free, transmit. Optional feature not needed for the exam: **RTS** (request to send) / **CTS** (clear to send).
- **Regulation**: wireless is regulated by international and national bodies; allowed channels vary by country. 802.11 outlines usable frequencies.
- **Coverage area**: signal range and the factors that affect it:
  - **Absorption**: the signal passes through a material and is converted to heat (a wall weakens the signal).
  - **Reflection**: the signal bounces off a material such as metal (poor reception in elevators).
  - **Refraction**: the wave is bent when entering a medium where it travels at a different speed (glass, water; the straw that looks bent in a glass of water).
  - **Diffraction**: the wave travels around an obstacle, creating **blind spots** behind it.
  - **Scattering**: dust, smog, uneven surfaces scatter the signal in all directions.
- **Interference**: other devices on the same channels (the neighbor's WLAN).

### 3. Radio frequency (RF) and electromagnetic waves

- The sender applies an **alternating current to an antenna**, creating electromagnetic fields that propagate as waves.
- **Amplitude**: maximum strength of the electric and magnetic fields.
- **Frequency**: number of cycles per unit of time. **Hertz** = cycles per second; kilohertz (thousands), megahertz (millions), gigahertz (billions), terahertz (trillions). **Period**: time of one cycle (4 Hz → 0.25 s).
- Visible range: about **400 THz to 790 THz**. **Radio frequency: about 30 Hz to 300 GHz**. 802.11 WLANs use sections of the **UHF** (ultra high frequency) and **SHF** (super high frequency) ranges.
- **Two main bands** (remember these; exact ranges are not required):
  - **2.4 GHz band**: actually **2.4 GHz to 2.4835 GHz**. Further reach in open space, better penetration of obstacles such as walls, but **more devices use it → more interference**.
  - **5 GHz band**: actually **5.150 GHz to 5.825 GHz**, divided into **four smaller bands**.
  - **Wi-Fi 6 (802.11ax)** expanded the spectrum to include a band in the **6 GHz** range (Jeremy is not sure it is on the exam).

### 4. Channels

- Each band is divided into **channels**; devices transmit and receive on one or more channels (**channel bonding** combines channels, not needed for the CCNA).
- **2.4 GHz band**: channels of **22 MHz** each, list differs by country (channel 14 in Japan is "11b only"; 802.11b is an old, slow standard). **Channels overlap**: channel 1 is **2401 MHz to 2423 MHz** and overlaps channels 2, 3, 4 and 5.
- Single AP: any channel. Multiple APs: **adjacent APs must not use overlapping channels**, or performance drops. **2.4 GHz recommendation: channels 1, 6 and 11**, which do not overlap (other combinations exist outside North America, but remember 1-6-11 for the CCNA).
- **5 GHz band**: **non-overlapping** channels, so interference between adjacent APs is much easier to avoid.
- **Honeycomb** pattern with 1-6-11: **coverage areas overlap** for complete coverage, but **frequencies do not**.

### 5. 802.11 standards

- From the **original 802.11 (1997)** to **802.11ax, Wi-Fi 6 (2019)**. Marketing names: **802.11n = Wi-Fi 4**, **802.11ac = Wi-Fi 5**, **802.11ax = Wi-Fi 6**; **no official Wi-Fi 1, 2 or 3**.
- Jeremy recommends memorizing **each standard's name, frequencies and maximum theoretical data rate** for the exam (the table is on a slide and not in the transcript; use the flashcards). Maximum rates are **theoretical**; real rates are much lower.
- Devices may support one, some or all standards: check before buying. Example given: the iPhone X supports **802.11a, b, g, n and ac**.

### 6. Service sets

Three main types: **independent**, **infrastructure**, **mesh**. All devices in a service set share the same **SSID** (Service Set Identifier), a human-readable name; it **does not have to be unique**, but it is best to use unique SSIDs.

- **IBSS** (Independent Basic Service Set): two or more devices connect **directly, without an AP**; also called **ad hoc** networks (AirDrop). Not scalable beyond a few devices.
- **BSS** (Basic Service Set), a kind of infrastructure service set: clients connect **via an AP**, never directly, even if the other client is in range.
  - **BSSID**: **uniquely** identifies the AP = **MAC address of the AP's radio**. Other APs can use the same SSID but not the same BSSID.
  - Devices request to **associate** with the BSS; associated devices are called **clients** or **stations**.
  - **BSA** (Basic Service Area): the **physical area** around the AP where its signal is usable. BSS = group of devices; BSA = physical area.
- **ESS** (Extended Service Set), the second infrastructure type: several BSSs connected by the **wired network** (switch). **Same SSID**, **unique BSSID per BSS**, **different channel per BSS** (BSS1 channel 1, BSS2 channel 6). **Roaming**: moving between APs without reconnecting; BSAs should overlap by about **10 to 15 percent**.
- **MBSS** (Mesh Basic Service Set): when running Ethernet to every AP is difficult. Mesh APs use **two radios**: one for the clients' BSS, one for the **backhaul** network between APs. The AP connected to the wired network is the **RAP** (Root Access Point); the others are **MAPs** (Mesh Access Points). A protocol determines the best path through the mesh (like a dynamic routing protocol).

### 7. Distribution system and AP modes

- **DS** (Distribution System): the 802.11 term for the upstream **wired network**. The AP translates between the two mediums. Each BSS/ESS is **mapped to a VLAN** (SSID "Jeremy's Wi-Fi" → VLAN 10).
- An AP can provide **multiple WLANs**, each with its own SSID and VLAN, connected to the switch via a **trunk** (Jeremy's Wi-Fi → VLAN 10, Guest Wi-Fi → VLAN 11). Each WLAN uses a **unique BSSID**, usually by **incrementing the last digit** (…3456 and …3457).
- **Repeater**: retransmits the AP's signal to extend the BSS. With a **single radio**, same channel as the AP → **effective throughput cut by 50%**. With **two radios**, it receives on one channel and retransmits on another.
- **Workgroup bridge (WGB)**: the AP acts as a **wireless client of another AP** to connect wired devices to the wireless network. **uWGB** (universal, 802.11 standard): **one** device bridged; **WGB** (Cisco proprietary): **multiple** wired clients.
- **Outdoor bridge**: connects networks over long distances without a cable, using **directional antennas**. **Point-to-point** or **point-to-multipoint** (hub-and-spoke).

### 8. Exam traps

- **CSMA/CA** for wireless (avoidance), **CSMA/CD** for wired (detection).
- Remember the **two bands, 2.4 GHz and 5 GHz**, and **channels 1, 6, 11** in 2.4 GHz.
- **SSID** = name, not necessarily unique; **BSSID** = AP MAC, unique. In an ESS: same SSID, different BSSIDs, non-overlapping channels.
- **BSS** (group of devices) ≠ **BSA** (physical area).
- Memorize standards, frequencies and data rates; Wi-Fi 4/5/6 = n/ac/ax.

### 9. Quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| In the 2.4 GHz band, which channels with multiple APs? | **1, 6 and 11** | They do not overlap, so nearby APs avoid interference. |
| Mostly wired enterprise network: purpose of an AP? | **Connect wireless devices to the wired network** | The wired network is the DS (distribution system); that is the AP's main role. |
| Bands commonly used by WLANs? (select two) | **2.4 GHz** and **5 GHz** | These bands are divided into channels used to send and receive. |
| True statements about an ESS? (select two) | **Each BSS uses a unique BSSID**; **roaming provides seamless connectivity between APs** | Wrong: each BSS in an ESS should use the **same** SSID; adjacent APs should use **non**-overlapping channels. |
| Statement NOT true about an AP providing multiple BSSs? | **"Each BSS shares the same BSSID"** | They may share the SSID (though a unique SSID per BSS is best practice), but BSSIDs must be unique. |
