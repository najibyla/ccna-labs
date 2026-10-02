# Ressources par chapitre : les 26 Skills du CCNA

> **Structure :** les 26 Skills du PDF `2-Fall into CCNA Study Plan.pdf` (NetworkChuck Academy), utilisés ici comme **plan de chapitres**. Le cours NetworkChuck lui-même est payant (250 $) et n'est pas utilisé.
> **Cours principal :** Jeremy's IT Lab, gratuit. Dans chaque Skill ci-dessous, la ressource principale est le ou les jours Jeremy (J.x) correspondants ; c'est ce que suit le calendrier `agenda/ccna-fall-2026.ics`, un jour par soir.
> **Usage :** une ressource principale + une pratique suffit par chapitre ; les compléments servent quand une notion reste floue.
> **Prix :** indicatifs, en euros, relevés fin septembre 2026. Udemy est presque toujours en promotion (15 à 20 € au lieu de 100+).

---

## 0. Le socle commun (à installer une fois, sert pour les 26 Skills)

### Gratuit
| Ressource | Pourquoi | Lien |
| :--- | :--- | :--- |
| **Jeremy's IT Lab - CCNA 200-301 Complete Course** (63 jours, YouTube) | La référence gratuite. Chaque vidéo a un lab Packet Tracer et un deck Anki. Les numéros de jour sont indiqués dans chaque Skill ci-dessous. | [Playlist YouTube](https://www.youtube.com/playlist?list=PLxbwE86jKRgMpuZuLBivzlM8s2Dk5lXBQ) |
| **Formip - Parcours Administrateur Réseau** (170 vidéos, en français) | Capsules animées courtes, très pédagogiques, en français. Idéal quand une notion ne passe pas en anglais. | [Cours gratuits Formip](https://www.formip.com/pages/cours-gratuits) |
| **Practical Networking** (Ed Harmoush, YouTube) | Le meilleur pour *comprendre* : OSI, ARP, subnetting, NAT, "packet traveling". Animations claires. | [Chaîne YouTube](https://www.youtube.com/@PracticalNetworking) et [site](https://www.practicalnetworking.net/) |
| **Flackbox - Free CCNA Lab Guide** (Neil Anderson, PDF) | 350 pages de labs Packet Tracer avec solutions, couvre tout le programme. | [Lab Guide](https://www.flackbox.com/cisco-ccna-lab-guide) |
| **Cisco Packet Tracer** + cours NetAcad *Getting Started with Packet Tracer* | Le simulateur officiel, gratuit avec un compte NetAcad. | [NetAcad](https://www.netacad.com/courses/packet-tracer) |
| **Cisco Learning Network - CCNA Exam Topics** | La liste officielle des objectifs de l'examen. À cocher au fur et à mesure. | [Exam topics](https://learningnetwork.cisco.com/s/ccna-exam-topics) |
| **Anki** (logiciel gratuit) | Répétition espacée. Importez les decks de Jeremy's IT Lab. 10 min/jour. | [apps.ankiweb.net](https://apps.ankiweb.net/) |
| **PowerCert Animated Videos** (YouTube) | Vidéos de 5 à 10 min, 100 % animées. Parfait comme premier contact sur un sujet. | [Chaîne YouTube](https://www.youtube.com/@PowerCertAnimatedVideos) |
| **Sunny Classroom** (YouTube) | Très visuel, courtes explications sur STP, VLAN, sécurité, Wi-Fi. | [Chaîne YouTube](https://www.youtube.com/@sunnyclassroom24) |

### Payant
| Ressource | Prix indicatif | Pourquoi |
| :--- | :--- | :--- |
| **Neil Anderson - Cisco CCNA 200-301 Complete Course with labs** (Udemy) | 15 à 20 € en promo | Le cours vidéo payant le plus pédagogique : 42 h, labs, notes, Anki, quiz. Le meilleur rapport qualité/prix. [Udemy](https://www.udemy.com/course/ccna-complete/) |
| **Flackbox CCNA Gold Bootcamp** (Neil Anderson) | voir site | Même contenu que Udemy + quiz par sujet + 150 pages de labs de dépannage. [Flackbox](https://www.flackbox.com/cisco-ccna-course) |
| **Wendell Odom - CCNA 200-301 Official Cert Guide Library** (2 volumes, Cisco Press) | 80 à 100 € | Le livre de référence. Dense, exhaustif. À lire en parallèle des vidéos, pas à la place. Inclut un simulateur d'examen. |
| **Boson ExSim-Max for CCNA** | ~100 € | Simulateur d'examen. Questions plus dures que le vrai examen, explications détaillées. À acheter en semaine 10. [Boson](https://www.boson.com/practice-exam/200-301-ccna-cisco-practice-exam) |
| **Boson NetSim for CCNA** | ~180 € | Simulateur d'IOS avec labs guidés, plus réaliste que Packet Tracer. Optionnel. |
| **CBT Nuggets - CCNA avec Keith Barker** | ~60 €/mois | Keith Barker est l'un des formateurs les plus pédagogiques du marché. Cher, à prendre 2 mois maximum sur les sujets difficiles (STP, OSPF, subnetting). |
| **Formip - Bootcamp CCNA** (en français) | éligible CPF | 20 semaines, en français, avec accompagnement. Pertinent si vous voulez du français et un financement CPF. [Formip](https://www.formip.com/courses/Cisco-CCNA) |
| **NetworkChuck Academy - Fall into CCNA** | 250 $, inscriptions closes au 1er octobre 2026 | Le cours dont vient le PDF. Non utilisé et non nécessaire : Jeremy's IT Lab couvre le même programme gratuitement. Pour le groupe et l'entraide : Discord de Jeremy's IT Lab et r/ccna, gratuits. |

---

## 1. Ressources par Skill

Légende : **J.x** = jour x de Jeremy's IT Lab. **PN** = Practical Networking. **OCG** = Odom Official Cert Guide (volume et chapitre).

### Semaine 1

#### Skill 01 - Packet Tracer (installation, premier réseau)
- **Gratuit, principal :** NetAcad *Getting Started with Cisco Packet Tracer* (2 h, avec labs) - [lien](https://www.netacad.com/courses/getting-started-cisco-packet-tracer)
- **Gratuit :** J.1 lab (Network Devices) pour votre premier réseau.
- **Gratuit :** Flackbox Lab Guide, section 1 (prise en main).
- **Payant :** rien de nécessaire.
- **Astuce :** apprenez dès maintenant les raccourcis : Ctrl+Shift+Z (annuler), Alt+drag pour déplacer, le mode Simulation pour voir les paquets.

#### Skill 02 - Fondamentaux : LAN/WAN, clients/serveurs, switch, routeur, pare-feu
- **Gratuit, principal :** J.1 Network Devices + J.52 LAN Architectures + J.53 WAN Architectures.
- **Gratuit :** PowerCert *Hub, Switch, Router Explained* et *Firewall Explained*.
- **Gratuit :** PN *Networking Fundamentals* (playlist "How data moves through the Internet") - la meilleure introduction qui existe.
- **Gratuit, français :** Formip module "Introduction aux réseaux".
- **Payant :** Neil Anderson sections 1 à 3. OCG vol.1 ch.1-2.

#### Skill 03 - Standards, bits/bytes, câblage cuivre et fibre, diagrammes
- **Gratuit, principal :** J.2 Interfaces and Cables.
- **Gratuit :** PowerCert *Ethernet cables, UTP vs STP*, *Fiber optic cables*, *Straight-through vs crossover*.
- **Gratuit :** Pour les diagrammes : draw.io (diagrams.net) avec la bibliothèque d'icônes Cisco intégrée. Dessinez chaque topologie avant de la construire.
- **Payant :** OCG vol.1 ch.2 (Fundamentals of Ethernet LANs).

### Semaine 2

#### Skill 04 - Modèle OSI vs TCP/IP, architecture 3 tiers
- **Gratuit, principal :** J.3 OSI Model & TCP/IP Suite.
- **Gratuit :** PN *OSI Model* (série de 7 vidéos, une par couche, la plus claire).
- **Gratuit :** PowerCert *OSI Model Explained*.
- **Gratuit :** J.52 LAN Architectures pour le 3 tiers (core, distribution, access).
- **Gratuit, français :** Formip module "Modèle OSI".
- **Payant :** OCG vol.1 ch.1. Neil Anderson section 4.
- **Astuce :** mémorisez les 7 couches avec un moyen mnémotechnique et, surtout, sachez placer un protocole (ARP, TCP, HTTP, Ethernet) sur sa couche.

#### Skill 05 - Cisco IOS : console, navigation, boot, config de base, sauvegarde
- **Gratuit, principal :** J.4 Intro to the CLI.
- **Gratuit :** Flackbox Lab Guide, labs "IOS basics".
- **Gratuit :** Cisco *IOS Command Reference* en ligne pour vérifier une commande.
- **Payant :** Neil Anderson section 5 (Cisco IOS). OCG vol.1 ch.4 et 8.
- **Astuce :** créez une fiche "configuration de base" (hostname, enable secret, banner, ligne console/vty, no ip domain-lookup, write memory) et retapez-la sur chaque nouvel équipement.

### Semaine 3

#### Skill 06 - Adresses MAC, trames, table CAM, fonctionnement du switch
- **Gratuit, principal :** J.5 et J.6 Ethernet LAN Switching parties 1 et 2.
- **Gratuit :** PN *How a switch works* et *ARP explained* (inclus dans "Packet Traveling").
- **Gratuit :** Wireshark : capturez une trame sur votre PC et identifiez MAC source/destination. Tutoriel Chris Greer *Wireshark for Beginners* (YouTube).
- **Payant :** OCG vol.1 ch.5 (Analyzing Ethernet LAN Switching).

#### Skill 07 - Adressage IP, masques, IP privées/publiques
- **Gratuit, principal :** J.7 et J.8 IPv4 Addressing parties 1 et 2.
- **Gratuit :** PN *Subnetting Mastery* parties 1 et 2 (comprendre le masque avant de subnetter).
- **Gratuit :** PowerCert *IP Address Explained*, *Public vs Private IP*.
- **Payant :** OCG vol.1 ch.11-12.

### Semaine 4

#### Skill 08 - Interfaces switch/routeur, compteurs, vitesse
- **Gratuit, principal :** J.9 Switch Interfaces.
- **Gratuit :** Flackbox Lab Guide, labs "Interfaces".
- **Gratuit :** Cisco doc *Troubleshooting Ethernet* (input errors, CRC, collisions, runts, giants). Faites une fiche des compteurs et de ce qu'ils signifient.
- **Payant :** OCG vol.1 ch.7 (Configuring and Verifying Switch Interfaces).

#### Skill 09 - Routage : local, statique, par défaut, dynamique (EIGRP), table de routage
- **Gratuit, principal :** J.11 Routing Fundamentals + J.12 Life of a Packet + J.25 RIP & EIGRP.
- **Gratuit :** PN *Packet Traveling* (la série complète, 5 vidéos). À regarder deux fois. C'est le chapitre le plus important du CCNA.
- **Gratuit, français :** Formip module "Routage statique".
- **Payant :** Neil Anderson sections 10-11. OCG vol.1 ch.15-16.

### Semaine 5

#### Skill 10 - NAT : statique, dynamique, overload (PAT)
- **Gratuit, principal :** J.44 et J.45 NAT parties 1 et 2.
- **Gratuit :** PN *NAT explained* (série de 4 vidéos : static, dynamic, PAT, et "NAT in depth"). La meilleure explication de la terminologie inside/outside local/global.
- **Gratuit :** PowerCert *NAT Explained*.
- **Payant :** OCG vol.2 ch.10.

#### Skill 11 - Subnetting : binaire, classes, VLSM, reverse engineering
- **Gratuit, principal :** PN *Subnetting Mastery* (14 vidéos, méthode de la "cheat sheet" pour résoudre tout problème en moins de 60 s) - [playlist](https://www.youtube.com/playlist?list=PLIFyRwBY_4bQUE4IB5c4VPRyDoLgOdExE)
- **Gratuit :** J.13, J.14, J.15 Subnetting parties 1 à 3 (inclut VLSM).
- **Gratuit, pratique quotidienne :** [subnetipv4.com](https://subnetipv4.com) (recommandé par PN), [subnettingpractice.com](https://subnettingpractice.com), [subnetting.org](https://subnetting.org). Objectif : 10 exercices par jour jusqu'à la fin du plan.
- **Gratuit, français :** Formip module "Subnetting" et "VLSM".
- **Payant :** OCG vol.1 ch.12-14 (excellent sur le subnetting, avec beaucoup d'exercices). Neil Anderson section 12.
- **Astuce :** c'est le chapitre à ne pas négliger. Sans subnetting rapide, vous perdez du temps sur toutes les questions de l'examen.

### Semaine 6

#### Skill 12 - VLANs, trunks, routage inter-VLAN, DTP/VTP, VLAN natif
- **Gratuit, principal :** J.16, J.17, J.18 VLANs parties 1 à 3 + J.19 DTP & VTP.
- **Gratuit :** Sunny Classroom *VLAN*, *Trunk*, *Native VLAN*, *Router on a stick*.
- **Gratuit :** Flackbox Lab Guide, labs VLAN et inter-VLAN routing (les plus complets).
- **Gratuit, français :** Formip modules "VLAN" et "Routage inter-VLAN".
- **Payant :** Neil Anderson sections 15-16. OCG vol.1 ch.8-9.

### Semaine 7

#### Skill 13 - Spanning Tree : concepts, sélection des ports, états, RSTP, PortFast, BPDU Guard
- **Gratuit, principal :** J.20, J.21 STP parties 1 et 2 + J.22 RSTP.
- **Gratuit :** Sunny Classroom *STP* (série de 5 vidéos, la plus visuelle sur l'élection du root et des ports).
- **Gratuit :** PN *Spanning Tree Protocol* (explication du "pourquoi").
- **Gratuit, français :** Formip module "Spanning Tree".
- **Payant :** CBT Nuggets Keith Barker sur STP (si vous prenez l'abonnement, c'est ici qu'il est le plus utile). OCG vol.1 ch.9-10.
- **Astuce :** dessinez 5 topologies à 3 ou 4 switches et déterminez à la main root bridge, root ports, designated ports, blocked ports. Vérifiez ensuite dans Packet Tracer avec `show spanning-tree`.

#### Skill 14 - EtherChannel, LACP, load balancing
- **Gratuit, principal :** J.23 EtherChannel.
- **Gratuit :** Sunny Classroom *EtherChannel*.
- **Gratuit :** Flackbox Lab Guide, lab EtherChannel.
- **Payant :** OCG vol.1 ch.10.

### Semaine 8

#### Skill 15 - Protocoles de routage, OSPF, dépannage, mise à l'échelle
- **Gratuit, principal :** J.24 Dynamic Routing + J.26, J.27, J.28 OSPF parties 1 à 3.
- **Gratuit :** PN *OSPF* et Certbros *OSPF explained* (YouTube, très clair sur les états de voisinage et les DR/BDR).
- **Gratuit :** Flackbox Lab Guide, labs OSPF (y compris multi-area).
- **Gratuit, français :** Formip module "OSPF".
- **Payant :** Neil Anderson sections 18-19. OCG vol.1 ch.19-21. CBT Nuggets Keith Barker sur OSPF.
- **Astuce :** apprenez à lire `show ip ospf neighbor`, `show ip ospf interface`, `show ip route ospf`. Le dépannage OSPF à l'examen se résume à 5 causes : zone, timers, MTU, masque de réseau, type de réseau.

### Semaine 9

#### Skill 16 - FHRP : HSRP, VRRP, GLBP
- **Gratuit, principal :** J.29 FHRP.
- **Gratuit :** Sunny Classroom *HSRP*.
- **Gratuit :** Flackbox Lab Guide, lab HSRP.
- **Payant :** OCG vol.2 ch.16 (partie FHRP). Neil Anderson section 21.

#### Skill 17 - IPv6 : adressage, raccourcis, configuration
- **Gratuit, principal :** J.31, J.32, J.33 IPv6 parties 1 à 3.
- **Gratuit :** PN *IPv6 Addressing* (compression, types d'adresses, EUI-64, SLAAC).
- **Gratuit :** PowerCert *IPv6 Explained*.
- **Gratuit, français :** Formip module "IPv6".
- **Payant :** OCG vol.1 ch.22-25 (4 chapitres, très complet). Neil Anderson section 24.

### Semaine 10

#### Skill 18 - ACL standard et étendues
- **Gratuit, principal :** J.34 Standard ACLs + J.35 Extended ACLs.
- **Gratuit :** PN *Access Control Lists* et Sunny Classroom *ACL*.
- **Gratuit :** Flackbox Lab Guide, labs ACL (nombreux scénarios de placement).
- **Gratuit, français :** Formip module "ACL".
- **Payant :** OCG vol.2 ch.2-3. Neil Anderson section 25.
- **Astuce :** règle d'or à mémoriser : standard près de la destination, étendue près de la source. Et le wildcard mask est l'inverse du masque.

#### Skill 19 - Sécurité : vulnérabilités, menaces, attaques sur mots de passe, AAA
- **Gratuit, principal :** J.48 Security Fundamentals.
- **Gratuit :** Professor Messer *Security+* (YouTube) sections "Threats and Vulnerabilities" : au-delà du CCNA mais très pédagogique et gratuit.
- **Gratuit :** Sunny Classroom *Cyber attacks* (série de courtes vidéos : DoS, MITM, spoofing, phishing).
- **Payant :** OCG vol.2 ch.4-5 (Security Architectures, Securing Network Devices).

### Semaine 11

#### Skill 20 - Sécurité couche 2 : port security, DHCP snooping, DAI
- **Gratuit, principal :** J.49 Port Security + J.50 DHCP Snooping + J.51 Dynamic ARP Inspection.
- **Gratuit :** Sunny Classroom *Port security*, *DHCP snooping*, *ARP spoofing*.
- **Gratuit :** Flackbox Lab Guide, labs Layer 2 security.
- **Payant :** OCG vol.2 ch.6-8. Neil Anderson section 27.

#### Skill 21 - CDP et LLDP
- **Gratuit, principal :** J.36 CDP & LLDP.
- **Gratuit :** Flackbox Lab Guide, lab CDP/LLDP.
- **Payant :** OCG vol.2 ch.9.
- **Astuce :** chapitre court. Apprenez les timers par défaut et sachez désactiver CDP sur une interface exposée.

#### Skill 22 - Services IP : horloge, NTP, DNS, DHCP, SSH
- **Gratuit, principal :** J.37 NTP + J.38 DNS + J.39 DHCP + J.42 SSH.
- **Gratuit :** PowerCert *DNS explained*, *DHCP explained*, *NTP*.
- **Gratuit :** PN *DHCP* et *DNS* (fonctionnement des échanges DORA et de la résolution).
- **Gratuit, français :** Formip modules "DHCP", "DNS", "NTP".
- **Payant :** OCG vol.2 ch.6 (DHCP), ch.9-10 (NTP, DNS, SSH).
- **Astuce :** faites le lien avec Linux : configurez un serveur DHCP et DNS avec dnsmasq sur votre VM Ubuntu, puis faites-y pointer vos équipements Packet Tracer (via le mode "Cloud" ou GNS3).

### Semaine 12

#### Skill 23 - SNMP et Syslog
- **Gratuit, principal :** J.40 SNMP + J.41 Syslog.
- **Gratuit :** PowerCert *SNMP explained*.
- **Gratuit :** Sur Linux : installez rsyslog et snmpd sur votre VM et envoyez-y les logs et traps de vos routeurs. Meilleur exercice possible.
- **Payant :** OCG vol.2 ch.9.

### Semaine 13

#### Skill 24 - QoS : classification, marquage, queuing, shaping, policing
- **Gratuit, principal :** J.46 et J.47 QoS parties 1 et 2.
- **Gratuit :** Sunny Classroom *QoS*.
- **Gratuit :** Kevin Wallace *QoS Fundamentals* (YouTube, gratuit, très pédagogique). Kevin Wallace est une référence QoS.
- **Payant :** OCG vol.2 ch.11.

#### Skill 25 - Wi-Fi : fonctionnement, canaux, association, sécurité
- **Gratuit, principal :** J.55, J.56, J.57, J.58 Wireless (fondamentaux, architectures, sécurité, configuration).
- **Gratuit :** Sunny Classroom *Wireless* (série : canaux, 2.4 vs 5 GHz, WPA2/WPA3, 802.1X).
- **Gratuit :** PowerCert *Wi-Fi standards*, *WPA3*.
- **Gratuit, français :** Formip module "Wi-Fi".
- **Payant :** OCG vol.1 ch.26-29. Neil Anderson section 30.

#### Skill 26 - Automatisation, SDN, REST APIs, Ansible/Puppet/Chef, JSON/YAML
- **Gratuit, principal :** J.59 Network Automation + J.60 JSON/XML/YAML + J.61 REST APIs + J.62 SDN + J.63 Ansible/Puppet/Chef.
- **Gratuit :** Cisco DevNet *Learning Labs* (gratuit avec compte DevNet) : "Coding & APIs Fundamentals", "Introduction to Ansible". - [developer.cisco.com/learning](https://developer.cisco.com/learning/)
- **Gratuit :** Postman *Learning Center* pour manipuler une API REST à la main.
- **Gratuit :** NetworkChuck *You need to learn Ansible* et *Python for network engineers* (YouTube).
- **Payant :** OCG vol.2 ch.16-19. Neil Anderson section 33.
- **Astuce :** c'est la passerelle vers le reste du curriculum (Python, Ansible, Terraform). Ne vous contentez pas des notions : faites un vrai appel API avec `curl` depuis votre VM Linux.

---

## 2. Après le cours : validation et examen (calendriers `agenda/ccna-revision-2027.ics` et `ccna-jalons-2027.ics`)

| Étape | Ressource | Quand |
| :--- | :--- | :--- |
| Achat et réservation | **Boson ExSim-Max** (~100 €) ; Pearson VUE, examen 200-301 (~300 € HT, centre ou en ligne surveillé), report gratuit à plus de 24 h | Jeudi 31 décembre 2026 |
| Révision par domaine | Vidéos et labs Jeremy's IT Lab des Skills hésitants, decks Anki complets, deux samedis sur le *CCNA Mega Lab* | 4 au 16 janvier 2027 |
| Examens blancs | Boson A, B, C en conditions réelles, chacun suivi d'une correction et d'une révision ciblée. Objectif : > 85 % et progression | 18 au 27 janvier 2027 |
| Labs de dépannage | Flackbox Lab Guide, section "Troubleshooting", et labs de dépannage de Jeremy | Samedi 23 janvier 2027 |
| Fiche officielle | Cisco Learning Network *Exam Topics* : cochez chaque objectif | Continu |
| Décision | Score C > 85 % : examen confirmé ; sinon report de deux semaines | Mercredi 27 janvier 2027 |
| Examen | 200-301, 120 min, ~100 questions, labs de simulation | Mardi 2 février 2027, 10h (cible) |

---

## 3. Comment choisir sans se disperser

1. **Regardez la vidéo Jeremy's IT Lab du jour** (J.x, c'est votre plan), en prenant des notes, et répondez au quiz de fin de vidéo.
2. **Faites le lab du jour** : téléchargez le fichier .pkt sur jeremysitlab.com, regardez la vidéo du lab, puis refaites-le seul sans la vidéo. Importez le deck Anki du jour.
3. **Si ce n'est pas clair :** Practical Networking (pour le "pourquoi") ou Formip (en français), listés dans le Skill concerné ci-dessus.
4. **Si ça ne passe toujours pas :** le chapitre Odom correspondant, ou Neil Anderson.
5. **Pour la pratique :** Flackbox Lab Guide, toujours.
6. **Payant seulement si :** vous voulez un second cours complet (Neil Anderson, 15 à 20 €) ou le livre de référence (Odom). Boson ExSim est le seul achat vraiment indispensable, en fin de parcours.

Budget minimal réaliste : **0 €** jusqu'à fin décembre, puis **~100 €** (Boson) + **~300 €** (examen).
Budget confortable : ajoutez Neil Anderson (20 €) et l'OCG Library (90 €).
