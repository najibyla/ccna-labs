# CCNA Day 2 : Interfaces and Cables / Interfaces et câbles

> Source : Jeremy's IT Lab, « Free CCNA | Interfaces and Cables | Day 2 » (36 min), vidéo n°4 de la playlist (cours) ; « Connecting Devices | Day 2 Lab » (6 min), vidéo n°5 (lab Packet Tracer). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Ports RJ-45 et Ethernet

- Face avant d'un switch : **24 interfaces** (*ports*). L'étiquette au-dessus des ports (« 10/100/1000BASE-T ports (1–24), ports are Auto-MDIX ») sera entièrement comprise à la fin de la vidéo.
- Ces ports sont des **RJ-45** (*Registered Jack*). Le connecteur RJ-45 termine un **câble Ethernet en cuivre** ; il existe aussi des câbles Ethernet sans cuivre (fibre, vue plus loin).
- **Ethernet** n'est pas un protocole unique mais une **collection de protocoles et de normes** ; ce cours se concentre sur les types de câblage définis par ces normes.
- Pourquoi des normes ? Comme deux personnes qui ne parlent pas la même langue, deux équipements ont besoin d'un système convenu. Les normes sont **physiques** (forme du connecteur, câble) et **logiques** (IP).

### 2. Bits, octets et débits

- Un **bit** vaut 0 ou 1 ; un **octet** (*byte*) = **8 bits**.
- Les données circulent **un bit à la fois** ; le débit se mesure en **bits par seconde** (kbit/s, Mbit/s, Gbit/s), **jamais en octets par seconde**. Le stockage, lui, se compte en octets : un **gigaoctet = 8 × un gigabit**.
- 1 kilobit = 1 000 bits ; 1 mégabit = 1 million ; 1 gigabit = 1 milliard ; 1 térabit = 1 000 milliards. Au-delà (pétabit, exabit, zettabit, yottabit) : pas à mémoriser.

### 3. Normes Ethernet cuivre (IEEE 802.3)

Toutes définies par l'**IEEE** (*Institute of Electrical and Electronics Engineers*) dans la famille **802.3**.

| Débit | Nom courant | Nom informel | Longueur max |
| :--- | :--- | :--- | :--- |
| 10 Mbit/s | Ethernet | **10BASE-T** | 100 m |
| 100 Mbit/s | Fast Ethernet | **100BASE-T** | 100 m |
| 1 Gbit/s | Gigabit Ethernet | **1000BASE-T** | 100 m |
| 10 Gbit/s | 10 Gigabit Ethernet | **10GBASE-T** | 100 m |

- **BASE** = signalisation en bande de base (*baseband*, hors programme) ; **T** = paire torsadée (*twisted pair*).
- **100 mètres** est la longueur maximale de toute paire torsadée en Ethernet. La diapositive donne aussi la norme IEEE précise de chaque ligne (802.3 + suffixe) ; Jeremy conseille de mémoriser le tableau avec les flashcards.

### 4. Câble UTP et brochage

- **UTP** = *Unshielded Twisted Pair* : **sans blindage** métallique (donc sensible aux interférences électromagnétiques, **EMI**), **4 paires torsadées** = **8 fils** ; la torsade protège contre les EMI. Le connecteur RJ-45 a **8 broches**.
- **10BASE-T et 100BASE-T utilisent 2 paires (4 fils)** ; **1000BASE-T et 10GBASE-T utilisent les 4 paires (8 fils)**.
- Paires utilisées en 10/100 : broches **1-2** et **3-6** (pas 3-4 !).
- **PC, routeur et pare-feu : émettent (Tx) sur 1-2, reçoivent (Rx) sur 3-6. Switch : l'inverse, Rx sur 1-2, Tx sur 3-6.**
- **Full-duplex** : les deux équipements émettent en même temps sans collision, car ils utilisent des fils séparés pour Tx et Rx.

**Câble droit (*straight-through*)** : broche 1 vers broche 1, 2 vers 2, etc. Convient quand les deux côtés émettent sur des paires opposées : **PC–switch, routeur–switch**.

**Câble croisé (*crossover*)** : les paires sont inversées, **1 ↔ 3 et 2 ↔ 6**. Nécessaire entre équipements qui émettent sur les mêmes broches : **routeur–routeur, switch–switch, PC–PC, PC–routeur**. Avec un câble droit, l'équipement d'en face n'est pas prêt à recevoir sur 1-2 et rien ne passe.

**Auto MDI-X** : les équipements modernes **détectent sur quelles broches le voisin émet et s'adaptent**. Deux switches reliés par un câble droit communiquent normalement. Sauf matériel ancien, le choix droit/croisé n'est donc plus un souci, mais le concept reste à connaître pour l'examen.

**Gigabit et 10 Gigabit** : paires supplémentaires **4-5 et 7-8** ; **chaque paire est bidirectionnelle** (pas dédiée à Tx ou Rx), ce qui contribue aux débits plus élevés.

### 5. Fibre optique

- Sur un switch ou un routeur, certains ports reçoivent un **transceiver SFP** (*Small Form-factor Pluggable*) dans lequel on branche un **câble à fibre optique** : de la **lumière dans des fibres de verre** au lieu d'un signal électrique.
- **Deux connecteurs par extrémité** : un pour émettre, un pour recevoir (câbles séparés Tx/Rx, et non des paires de fils) ; Tx d'un côté va sur Rx de l'autre.
- Structure du câble, du centre vers l'extérieur : **1 cœur en fibre de verre**, **2 gaine réfléchissante** (*cladding*), **3 tampon protecteur** (*buffer*), **4 gaine extérieure** (*jacket*).

| | Multimode (*multimode fiber*) | Monomode (*single-mode fiber*) |
| :--- | :--- | :--- |
| Cœur | **plus large** | **plus étroit** |
| Lumière | **plusieurs angles** (modes) qui se réfléchissent sur la gaine | **un seul angle**, trajet rectiligne |
| Émetteur | **LED**, moins cher | **laser**, plus cher |
| Distance | plus que l'UTP, moins que le monomode | la plus longue |

Normes fibre (Jeremy doute que l'examen demande ces détails, mais les flashcards les couvrent) :

| Norme | IEEE | Fibre | Longueur max |
| :--- | :--- | :--- | :--- |
| 1000BASE-LX | 802.3z | mono ou multimode | 550 m (multimode), 5 km (monomode) |
| 10GBASE-SR | 802.3ae | multimode | 400 m |
| 10GBASE-LR | 802.3ae | monomode | 10 km |
| 10GBASE-ER | 802.3ae | monomode | 30 km |

### 6. UTP contre fibre

- **UTP** : moins cher ; **100 m max** ; **sensible aux EMI** (la torsade aide) ; ports RJ-45 moins chers que les SFP ; **émet un faible signal hors du câble**, risque de sécurité (copie de données possible).
- **Fibre** : plus chère ; **plus longues distances** ; ports SFP plus chers (monomode plus cher que multimode) ; **n'émet aucun signal** hors du câble.

### 7. Pièges d'examen

- Débit en **bits**/s, stockage en **octets** : 1 Go = 8 Gb.
- Deuxième paire 10/100 = broches **3 et 6**, pas 3 et 4.
- **Le switch est le seul** à recevoir sur 1-2 et émettre sur 3-6 ; routeur, pare-feu et PC se comportent pareil (Tx 1-2, Rx 3-6).
- Sans Auto MDI-X, deux équipements de même type reliés par un câble droit **ne communiquent pas du tout** (pas de débit réduit : rien).
- Dans une question « pour réduire les coûts », choisir le câble **le moins cher qui couvre la distance** : UTP ≤ 100 m, multimode au-delà, monomode pour les kilomètres.
- Les hôtes finaux se branchent au switch en **UTP** : ils n'ont généralement pas de port fibre et les switches n'ont pas assez de SFP.

### 8. Le lab (Day 2 Lab, « Connecting Devices »)

**Objectif :** relier les équipements du schéma avec le bon type de câble (Packet Tracer, choix en bas à gauche : cuivre droit, cuivre croisé, fibre). Hypothèse du lab : **Auto MDI-X désactivé ou non supporté**. Packet Tracer ne distingue pas mono et multimode : réfléchir quand même au bon type.

1. **PC et serveur vers switch, câble droit** : PC1–SW3, PC2–SW4, PC3–SW7, SRV1–SW8 (FastEthernet0 du PC vers n'importe quel FastEthernet du switch).
2. **Switch vers switch, câble croisé** (même type d'équipement) : SW3–SW1, SW1–SW2, SW4–SW2, SW7–SW5, SW5–SW6, SW8–SW6.
3. **Switch vers routeur, câble droit** (le routeur se comporte comme un PC) : SW1–R2, SW2–R2, SW5–R4, SW6–R4 (la fin de la phrase est coupée dans la transcription).
4. **Routeur vers routeur** : même type, donc croisé si cuivre.
   - R2–R1 : **50 m**, cuivre croisé (≤ 100 m).
   - R1–R3 : **3 km**, fibre ; multimode plafonne à 550 m, donc **monomode** (30 km, 40 km et plus). Le symbole fibre de Packet Tracer montre deux emplacements, Tx et Rx.
   - R3–R4 : **250 m**, trop long pour l'UTP, **multimode** suffit.

**Vérification :** tous les équipements connectés ; aucune commande dans ce lab.

### 9. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Deux vieux routeurs reliés par un câble UTP ne communiquent pas. Cause ? | **Câble droit** | Un croisé corrigerait le problème (les deux émettent sur 1-2). L'Auto MDI-X corrigerait aussi, mais de vieux routeurs ne l'ont probablement pas. |
| Relier des switches dans deux bâtiments à 150 m, à moindre coût : quel câble ? | **Fibre multimode** | L'UTP ne dépasse pas 100 m ; le monomode couvre mais coûte plus cher. |
| Relier deux bureaux à 3 km, à moindre coût : quel câble ? | **Fibre monomode** | UTP et multimode ne couvrent pas 3 km ; le monomode est plus cher mais nécessaire. |
| Un switch dont les ports sont « Auto MDI-X » est relié à un switch identique par un câble droit : résultat ? | **Fonctionnement normal** | Grâce à l'Auto MDI-X, droit ou croisé n'importe plus. Sans Auto MDI-X, ils ne fonctionneraient pas du tout (pas « à débit réduit »). |
| Relier beaucoup d'hôtes à un switch du même étage : quel câble ? | **UTP** | Les hôtes n'ont pas de port fibre et les switches n'ont pas assez de SFP ; le switch a beaucoup de ports RJ-45 et la carte réseau de l'hôte en a un. |

---

## 🇬🇧 English version

### 1. RJ-45 ports and Ethernet

- Front of a switch: **24 interfaces** (*ports*). The label above them ("10/100/1000BASE-T ports (1–24), ports are Auto-MDIX") will make full sense by the end of the video.
- The ports are **RJ-45** (*Registered Jack*). An RJ-45 connector ends a **copper Ethernet cable**; Ethernet cables without copper (fiber) also exist.
- **Ethernet** is not one protocol but a **collection of protocols and standards**; this lesson focuses on the cabling types those standards define.
- Why standards? Like two people who do not share a language, devices need an agreed system. Standards are **physical** (connector shape, cables) and **logical** (IP).

### 2. Bits, bytes and speeds

- A **bit** is a 0 or a 1; a **byte** = **8 bits**.
- Data travels **one bit at a time**; speed is measured in **bits per second** (kbps, Mbps, Gbps), **never bytes per second**. Storage is measured in bytes: a **gigabyte is 8 times a gigabit**.
- 1 kilobit = 1,000 bits; 1 megabit = 1 million; 1 gigabit = 1 billion; 1 terabit = 1 trillion. Beyond that (petabit, exabit, zettabit, yottabit): no need to memorize.

### 3. Copper Ethernet standards (IEEE 802.3)

All defined by the **IEEE** (*Institute of Electrical and Electronics Engineers*) in the **802.3** family.

| Speed | Common name | Informal name | Max length |
| :--- | :--- | :--- | :--- |
| 10 Mbps | Ethernet | **10BASE-T** | 100 m |
| 100 Mbps | Fast Ethernet | **100BASE-T** | 100 m |
| 1 Gbps | Gigabit Ethernet | **1000BASE-T** | 100 m |
| 10 Gbps | 10 Gigabit Ethernet | **10GBASE-T** | 100 m |

- **BASE** = baseband signalling (out of scope); **T** = twisted pair.
- **100 meters** is the maximum for any twisted-pair cable in Ethernet. The slide also lists each line's exact IEEE standard (802.3 + suffix); Jeremy recommends memorizing the table with the flashcards.

### 4. UTP cable and pinouts

- **UTP** = *Unshielded Twisted Pair*: **no metallic shield** (hence vulnerable to electromagnetic interference, **EMI**), **4 twisted pairs** = **8 wires**; the twist protects against EMI. The RJ-45 connector has **8 pins**.
- **10BASE-T and 100BASE-T use 2 pairs (4 wires)**; **1000BASE-T and 10GBASE-T use all 4 pairs (8 wires)**.
- Pairs used at 10/100: pins **1-2** and **3-6** (not 3-4!).
- **PCs, routers and firewalls transmit (Tx) on 1-2 and receive (Rx) on 3-6. Switches are the opposite: Rx on 1-2, Tx on 3-6.**
- **Full-duplex**: both devices send at the same time with no collisions, because they use separate wires to transmit and receive.

**Straight-through cable**: pin 1 to pin 1, 2 to 2, and so on. Works when the two sides transmit on opposite pairs: **PC–switch, router–switch**.

**Crossover cable**: pairs are reversed, **1 ↔ 3 and 2 ↔ 6**. Required between devices that transmit on the same pins: **router–router, switch–switch, PC–PC, PC–router**. With a straight-through cable, the far side is not prepared to receive on 1-2 and nothing gets through.

**Auto MDI-X**: modern devices **detect which pins the neighbor transmits on and adjust**. Two switches on a straight-through cable communicate normally. Unless the gear is quite old, straight-through vs crossover is no longer a worry, but know the concept for the exam.

**Gigabit and 10 Gigabit**: the extra pairs are **4-5 and 7-8**; **each pair is bidirectional** (not dedicated to Tx or Rx), part of why they are faster.

### 5. Fiber optics

- Some ports on a switch or router take an **SFP transceiver** (*Small Form-factor Pluggable*) into which you plug a **fiber-optic cable**: **light over glass fibers** instead of an electrical signal.
- **Two connectors on each end**: one to transmit, one to receive (separate cables for Tx and Rx rather than wire pairs); Tx on one side connects to Rx on the other.
- Cable structure, center to outside: **1 fiberglass core**, **2 reflective cladding**, **3 protective buffer**, **4 outer jacket**.

| | Multimode fiber | Single-mode fiber |
| :--- | :--- | :--- |
| Core | **wider** | **narrower** |
| Light | **multiple angles** (modes) reflecting off the cladding | **a single angle**, straight down the core |
| Transmitter | **LED-based**, cheaper | **laser-based**, more expensive |
| Distance | longer than UTP, shorter than single-mode | the longest |

Fiber standards (Jeremy doubts the exam asks these details, but the flashcards cover them):

| Standard | IEEE | Fiber | Max length |
| :--- | :--- | :--- | :--- |
| 1000BASE-LX | 802.3z | single- or multimode | 550 m (multimode), 5 km (single-mode) |
| 10GBASE-SR | 802.3ae | multimode | 400 m |
| 10GBASE-LR | 802.3ae | single-mode | 10 km |
| 10GBASE-ER | 802.3ae | single-mode | 30 km |

### 6. UTP versus fiber

- **UTP**: cheaper; **100 m max**; **vulnerable to EMI** (the twist helps); RJ-45 ports cheaper than SFPs; **leaks a faint signal outside the cable**, a possible security risk (data could be copied).
- **Fiber**: more expensive; **longer distances**; SFP ports more expensive (single-mode more than multimode); **emits no signal** outside the cable.

### 7. Exam traps

- Speed in **bits**/s, storage in **bytes**: 1 GB = 8 Gb.
- Second 10/100 pair is pins **3 and 6**, not 3 and 4.
- **The switch is the only one** that receives on 1-2 and transmits on 3-6; router, firewall and PC all behave the same (Tx 1-2, Rx 3-6).
- Without Auto MDI-X, two same-type devices on a straight-through cable **do not communicate at all** (not "reduced speed": nothing).
- In a "keep costs down" question, pick the **cheapest cable that covers the distance**: UTP up to 100 m, multimode beyond, single-mode for kilometers.
- End hosts connect to switches with **UTP**: they usually have no fiber port and switches lack enough SFPs.

### 8. The lab (Day 2 Lab, "Connecting Devices")

**Goal:** connect the devices in the diagram with the right cable type (Packet Tracer, choices bottom left: copper straight-through, copper crossover, fiber). Lab assumption: **Auto MDI-X disabled or unsupported**. Packet Tracer does not distinguish single-mode from multimode: still think about which one fits.

1. **PCs and server to switches, straight-through**: PC1–SW3, PC2–SW4, PC3–SW7, SRV1–SW8 (the PC's FastEthernet0 to any FastEthernet on the switch).
2. **Switch to switch, crossover** (same device type): SW3–SW1, SW1–SW2, SW4–SW2, SW7–SW5, SW5–SW6, SW8–SW6.
3. **Switch to router, straight-through** (routers behave like PCs): SW1–R2, SW2–R2, SW5–R4, SW6–R4 (the sentence is cut off in the transcript).
4. **Router to router**: same type, so crossover if copper.
   - R2–R1: **50 m**, copper crossover (within 100 m).
   - R1–R3: **3 km**, fiber; multimode tops out at 550 m, so **single-mode** (30 km, 40 km and more). Packet Tracer's fiber symbol shows two slots, Tx and Rx.
   - R3–R4: **250 m**, too long for UTP, **multimode** is enough.

**Check:** all devices connected; no commands in this lab.

### 9. The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Two old routers connected with a UTP cable cannot exchange data. Problem? | **Straight-through cable** | A crossover would likely fix it (both transmit on 1-2). Auto MDI-X would fix it too, but old routers may not have it. |
| Connect switches in two buildings 150 m apart, keeping costs down: which cable? | **Multimode fiber** | UTP cannot exceed 100 m; single-mode works but costs more. |
| Connect two offices 3 km apart, keeping costs down: which cable? | **Single-mode fiber** | UTP and multimode cannot cover 3 km; single-mode is pricier but necessary. |
| A switch whose ports are "Auto MDI-X" is connected to an identical switch with a straight-through cable: result? | **They operate normally** | With Auto MDI-X, straight-through or crossover does not matter. Without it they would not operate at all (not "at reduced speed"). |
| Connect many end hosts to a switch on the same office floor: which cable? | **UTP** | Hosts lack fiber ports and switches lack enough SFPs; switches have many RJ-45 ports and a host's NIC has one. |
