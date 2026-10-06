# Fiches CCNA, une par jour du cours de Jeremy's IT Lab

Résumés bilingues (français puis anglais) rédigés à partir de la **transcription** de chaque vidéo (`ressources/jeremy-it-lab/transcripts/`, hors dépôt, récupérée avec `outils/fetch_transcripts.py`), pas de mémoire. Modèle : `jour-01-network-devices.md`.

## Convention

- Un fichier par jour : `jour-NN-<sujet-en-kebab-case>.md`. Un jour en plusieurs parties (11, 21, 54, 59, 61, 63) tient dans un seul fichier.
- En tête : source (numéros et durées des vidéos dans la playlist), date de rédaction.
- Structure, identique dans les deux langues :
  1. Les concepts, dans l'ordre de la vidéo, avec les termes anglais entre parenthèses dans la version française.
  2. **Pièges d'examen** : ce que Jeremy signale comme confusion fréquente ou point insisté.
  3. **Commandes IOS** vues dans la vidéo et le lab, en bloc de code, avec le mode (`#`, `(config)#`, `(config-if)#`) et une ligne d'explication.
  4. **Le lab** : objectif, étapes, commandes, ce qu'il faut vérifier (`show ...`). Absent si le jour n'a pas de lab.
  5. **Le quiz** : chaque question, la bonne réponse, pourquoi les autres sont fausses.
- Longueur : 1 à 2 pages par langue. Une fiche doit permettre de réviser le jour sans revoir la vidéo.
- Rien d'inventé : si une information n'est pas dans la transcription, elle n'est pas dans la fiche.

## Usage

Lire la fiche du jour **après** la vidéo, pas à la place. Relire les fiches de la semaine le dimanche, et toutes les fiches pendant les deux semaines de révision de janvier.

## Limites connues

Les sous-titres automatiques ne lisent pas ce qui est seulement affiché à l'écran. Les fiches le signalent chaque fois, sans reconstituer :

- les propositions de réponse incorrectes de certains quiz (seules la bonne réponse et l'explication orale de Jeremy sont reprises) ;
- jour 3 : la vidéo récente « How the TCP/IP Model Actually Works » n'a pas de quiz, la fiche reprend la récapitulation ;
- jour 7 : les écritures binaires du quiz ont été recalculées à partir des décimaux dits à l'oral, et l'erratum connu de la vidéo (221 en binaire) est consigné ;
- jour 15 : pas de quiz, Jeremy donne un devoir de subnetting sur trois sites à la place ;
- jour 20 : pas de quiz formel, les six exercices « pause the video » sont regroupés ;
- jour 31 : les exercices d'abréviation IPv6 et certaines options de quiz sont à l'écran ;
- jour 45 : la transcription du lab s'arrête avant le lab bonus Boson NetSim annoncé ;
- jour 55 : le tableau des normes 802.11 (fréquences, débits) est sur une diapositive non lue, à prendre dans le deck Anki du jour ;
- jour 60 : les extraits JSON des questions 4 à 10 sont à l'écran.

Quelques lapsus oraux de Jeremy, contredits par le reste de la vidéo, sont corrigés et signalés dans les fiches concernées (jours 2, 4, 15, 17, 24, 47).

## État (toutes rédigées et vérifiées contre la transcription le 6 octobre 2026)

| Jour | Fiche | Vérifiée |
| :--- | :--- | :--- |
| 01 | `jour-01-network-devices.md` | oui |
| 02 | `jour-02-interfaces-and-cables.md` | oui |
| 03 | `jour-03-tcp-ip-model.md` | oui |
| 04 | `jour-04-intro-to-the-cli.md` | oui |
| 05 | `jour-05-ethernet-lan-switching-part-1.md` | oui |
| 06 | `jour-06-ethernet-lan-switching-part-2.md` | oui |
| 07 | `jour-07-ipv4-addressing-part-1.md` | oui |
| 08 | `jour-08-ipv4-addressing-part-2.md` | oui |
| 09 | `jour-09-switch-interfaces.md` | oui |
| 10 | `jour-10-ipv4-header.md` | oui |
| 11 | `jour-11-routing-fundamentals-static-routing.md` | oui |
| 12 | `jour-12-life-of-a-packet.md` | oui |
| 13 | `jour-13-subnetting-part-1.md` | oui |
| 14 | `jour-14-subnetting-part-2.md` | oui |
| 15 | `jour-15-subnetting-part-3-vlsm.md` | oui |
| 16 | `jour-16-vlans-part-1.md` | oui |
| 17 | `jour-17-vlans-part-2.md` | oui |
| 18 | `jour-18-vlans-part-3.md` | oui |
| 19 | `jour-19-dtp-vtp.md` | oui |
| 20 | `jour-20-spanning-tree-protocol-part-1.md` | oui |
| 21 | `jour-21-spanning-tree-protocol-part-2-stp-toolkit.md` | oui |
| 22 | `jour-22-rapid-stp.md` | oui |
| 23 | `jour-23-etherchannel.md` | oui |
| 24 | `jour-24-dynamic-routing.md` | oui |
| 25 | `jour-25-rip-eigrp.md` | oui |
| 26 | `jour-26-ospf-part-1.md` | oui |
| 27 | `jour-27-ospf-part-2.md` | oui |
| 28 | `jour-28-ospf-part-3.md` | oui |
| 29 | `jour-29-first-hop-redundancy-protocols.md` | oui |
| 30 | `jour-30-tcp-udp.md` | oui |
| 31 | `jour-31-ipv6-part-1.md` | oui |
| 32 | `jour-32-ipv6-part-2.md` | oui |
| 33 | `jour-33-ipv6-part-3.md` | oui |
| 34 | `jour-34-standard-acls.md` | oui |
| 35 | `jour-35-extended-acls.md` | oui |
| 36 | `jour-36-cdp-lldp.md` | oui |
| 37 | `jour-37-ntp.md` | oui |
| 38 | `jour-38-dns.md` | oui |
| 39 | `jour-39-dhcp.md` | oui |
| 40 | `jour-40-snmp.md` | oui |
| 41 | `jour-41-syslog.md` | oui |
| 42 | `jour-42-ssh.md` | oui |
| 43 | `jour-43-ftp-tftp.md` | oui |
| 44 | `jour-44-nat-part-1.md` | oui |
| 45 | `jour-45-nat-part-2.md` | oui |
| 46 | `jour-46-qos-part-1-voice-vlans.md` | oui |
| 47 | `jour-47-qos-part-2.md` | oui |
| 48 | `jour-48-security-fundamentals.md` | oui |
| 49 | `jour-49-port-security.md` | oui |
| 50 | `jour-50-dhcp-snooping.md` | oui |
| 51 | `jour-51-dynamic-arp-inspection.md` | oui |
| 52 | `jour-52-lan-architectures.md` | oui |
| 53 | `jour-53-wan-architectures.md` | oui |
| 54 | `jour-54-virtualization-cloud.md` | oui |
| 55 | `jour-55-wireless-fundamentals.md` | oui |
| 56 | `jour-56-wireless-architectures.md` | oui |
| 57 | `jour-57-wireless-security.md` | oui |
| 58 | `jour-58-wireless-configuration.md` | oui |
| 59 | `jour-59-network-automation-ai-ml.md` | oui |
| 60 | `jour-60-json-xml-yaml.md` | oui |
| 61 | `jour-61-rest-apis.md` | oui |
| 62 | `jour-62-software-defined-networking.md` | oui |
| 63 | `jour-63-ansible-puppet-chef-terraform.md` | oui |

Le Mega Lab (vidéo n°126, 2 h 39) n'a pas de fiche : c'est l'examen blanc pratique de janvier, à ne pas lire avant.
