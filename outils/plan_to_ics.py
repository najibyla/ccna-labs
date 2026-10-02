#!/usr/bin/env python3
"""Génère des calendriers .ics (Google Agenda, Outlook, Apple) à partir du plan d'étude.

Sorties (dossier agenda/) :
  ccna-fall-2026.ics      un événement par jour d'étude du plan NetworkChuck (PDF), avec
                          les leçons du jour, le nom du Skill, l'estimation de durée et les
                          ressources complémentaires en description ;
  linux-track-2026.ics    les 22 leçons du Linux Upskill Challenge le week-end, avec les
                          chapitres correspondants de The Linux Command Line ;
  ccna-revision-2027.ics  janvier 2027 : 2 semaines de révision par domaine (Jeremy's IT Lab),
                          2 semaines d'examens blancs Boson ;
  ccna-jalons-2027.ics    les 4 jalons : préparation (achat Boson, réservation), décision du
                          27 janvier, veille d'examen, examen cible le 2 février ;
  ccna-plan.json          le plan parsé, pour réutilisation.

Charge horaire encodée (modifiable ci-dessous) :
  CCNA      lundi à vendredi, 21h00, durée estimée par jour (1h30 à 2h30), 10 h/semaine
  Linux     samedi et dimanche, 10h00-12h00 (en journée), 4 h/semaine
  Fuseau    UTC (heure légale du Maroc depuis septembre 2026, sans heure d'été)
  Anki      10 min/jour, non mis au calendrier (à faire dans les transports ou au café)

Usage : python plan_to_ics.py [--pdf FICHIER] [--out DOSSIER]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
TZ = "UTC"  # Maroc : UTC depuis septembre 2026 (heure additionnelle supprimée). Horodatage en Z, sans TZID :
            # insensible à l'état de la base des fuseaux horaires de Google ou du téléphone.

# ---- réglages horaires ----
CCNA_START = (21, 0)          # heure de début en semaine (soir)
CCNA_MIN, CCNA_MAX = 90, 150  # bornes de durée (minutes)
LINUX_START, LINUX_MINUTES = (10, 0), 120
LINUX_FIRST_DAY = date(2026, 10, 3)  # premier samedi

# Source du calendrier CCNA :
#   "jeremy"       Jeremy's IT Lab, cours gratuit (YouTube), 63 jours -> 62 séances (gratuit, référence)
#   "networkchuck" plan du PDF NetworkChuck Academy (cours payant, 250 $), 62 journées
SOURCE = "jeremy"

# Décalage du plan : les journées d'étude (dans l'ordre) sont replacées sur les jours
# ouvrés à partir de START_DATE, en sautant SKIP_DATES. None = garder les dates du PDF.
START_DATE = date(2026, 10, 1)
SKIP_DATES = {date(2026, 11, 6), date(2026, 11, 18)}  # Marche verte, Fête de l'indépendance

# Rattrapage ponctuel : jour du plan (date d'origine du PDF) -> (date, heure, minute).
RESCHEDULE: dict[date, tuple[date, int, int]] = {}

# Jeremy's IT Lab, CCNA 200-301 v1.1 : la playlist YouTube réelle (126 vidéos, cours et labs entrelacés),
# relevée le 1er octobre 2026 avec yt-dlp dans outils/data/jeremy-playlist.txt (index|secondes|titre).
# Pour la rafraîchir : yt-dlp --flat-playlist --print "%(playlist_index)s|%(duration)s|%(title)s" <url playlist>
JEREMY_PLAYLIST = Path(__file__).resolve().parent / "data" / "jeremy-playlist.txt"
JEREMY_URL = "https://www.youtube.com/playlist?list=PLxbwE86jKRgMpuZuLBivzlM8s2Dk5lXBQ"
# Découpage en séances : par défaut un jour = une séance. Exceptions :
#   - Day 21 : la partie 2 de STP et son lab d'un côté, les 4 vidéos « STP Toolkit » de l'autre (2 h 20 de vidéo sinon)
#   - Days 62 et 63 : courts et sans lab, regroupés
JEREMY_SPLIT = {21: [lambda t: "Toolkit" not in t, lambda t: "Toolkit" in t]}
JEREMY_MERGE = [[62, 63]]
JEREMY_FACTOR, JEREMY_FIXED_MIN = 1.3, 10  # vidéo avec pauses et notes ; quiz + import Anki. Un lab refait seul = durée de sa vidéo.
SKILL_BY_DAY = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 6, 7: 7, 8: 7, 9: 8, 10: 7, 11: 9, 12: 9, 13: 11, 14: 11, 15: 11, 16: 12, 17: 12, 18: 12,
                19: 12, 20: 13, 21: 13, 22: 13, 23: 14, 24: 15, 25: 9, 26: 15, 27: 15, 28: 15, 29: 16, 30: 4, 31: 17, 32: 17, 33: 17,
                34: 18, 35: 18, 36: 21, 37: 22, 38: 22, 39: 22, 40: 23, 41: 23, 42: 22, 43: 22, 44: 10, 45: 10, 46: 24, 47: 24, 48: 19,
                49: 20, 50: 20, 51: 20, 52: 2, 53: 2, 54: 2, 55: 25, 56: 25, 57: 25, 58: 25, 59: 26, 60: 26, 61: 26, 62: 26, 63: 26}

# Estimation par type de tâche (minutes) : vidéo, quiz, lab guidé, lab de synthèse (SL)
EST = {"lesson": 12, "quiz": 5, "lab": 25, "skill_lab": 40}

SKILLS = {
    1: ("Packet Tracer : installation et premier réseau", "NetAcad Getting Started with Packet Tracer ; Jeremy's IT Lab J.1 (lab)"),
    2: ("Fondamentaux : LAN/WAN, clients/serveurs, switch, routeur, pare-feu", "Jeremy J.1, J.52, J.53 ; Practical Networking « Networking Fundamentals » ; PowerCert « Hub, Switch, Router »"),
    3: ("Standards, câblage cuivre et fibre, diagrammes", "Jeremy J.2 ; PowerCert « Ethernet cables », « Fiber optic » ; draw.io pour les schémas"),
    4: ("Modèle OSI / TCP-IP, architecture 3 tiers", "Jeremy J.3, J.52 ; Practical Networking « OSI Model » (7 vidéos) ; Formip « Modèle OSI »"),
    5: ("Cisco IOS : console, navigation, boot, configuration de base", "Jeremy J.4 ; Flackbox Lab Guide « IOS basics » ; fiche de config de base à retaper à chaque lab"),
    6: ("Adresses MAC, trames Ethernet, table CAM, fonctionnement du switch", "Jeremy J.5, J.6 ; Practical Networking « How a switch works », « ARP » ; Wireshark : capturer une trame"),
    7: ("Adressage IPv4, masques, IP privées et publiques", "Jeremy J.7, J.8 ; Practical Networking « Subnetting Mastery » parties 1-2 ; PowerCert « IP Address Explained »"),
    8: ("Interfaces switch et routeur, compteurs, vitesse et duplex", "Jeremy J.9 ; Flackbox Lab Guide « Interfaces » ; fiche des compteurs (CRC, runts, giants, collisions)"),
    9: ("Routage : local, statique, par défaut, dynamique (EIGRP), table de routage", "Jeremy J.11, J.12, J.25 ; Practical Networking « Packet Traveling » (à voir deux fois) ; Formip « Routage statique »"),
    10: ("NAT : statique, dynamique, PAT (overload)", "Jeremy J.44, J.45 ; Practical Networking « NAT » (4 vidéos) ; PowerCert « NAT Explained »"),
    11: ("Subnetting : binaire, classes, VLSM, reverse engineering", "Practical Networking « Subnetting Mastery » (14 vidéos) ; Jeremy J.13-J.15 ; 10 exercices/jour sur subnetipv4.com ; Formip « Subnetting », « VLSM »"),
    12: ("VLANs, trunks, routage inter-VLAN, DTP/VTP, VLAN natif", "Jeremy J.16-J.19 ; Sunny Classroom « VLAN », « Trunk », « Router on a stick » ; Flackbox labs VLAN"),
    13: ("Spanning Tree : root, ports, états, RSTP, PortFast, BPDU Guard", "Jeremy J.20-J.22 ; Sunny Classroom « STP » (5 vidéos) ; dessiner 5 topologies et élire root/ports à la main"),
    14: ("EtherChannel, LACP, répartition de charge", "Jeremy J.23 ; Sunny Classroom « EtherChannel » ; Flackbox lab EtherChannel"),
    15: ("Protocoles de routage, OSPF, dépannage et mise à l'échelle", "Jeremy J.24, J.26-J.28 ; Certbros « OSPF explained » ; Flackbox labs OSPF ; Formip « OSPF »"),
    16: ("FHRP : HSRP, VRRP, GLBP", "Jeremy J.29 ; Sunny Classroom « HSRP » ; Flackbox lab HSRP"),
    17: ("IPv6 : adressage, raccourcis, configuration", "Jeremy J.31-J.33 ; Practical Networking « IPv6 Addressing » ; PowerCert « IPv6 Explained » ; Formip « IPv6 »"),
    18: ("ACL standard et étendues", "Jeremy J.34, J.35 ; Sunny Classroom « ACL » ; Flackbox labs ACL ; règle : standard près de la destination, étendue près de la source"),
    19: ("Sécurité : vulnérabilités, menaces, attaques sur mots de passe, AAA", "Jeremy J.48 ; Sunny Classroom « Cyber attacks » ; Professor Messer Security+ « Threats »"),
    20: ("Sécurité couche 2 : port security, DHCP snooping, DAI", "Jeremy J.49-J.51 ; Sunny Classroom « Port security », « DHCP snooping », « ARP spoofing » ; Flackbox labs L2 security"),
    21: ("CDP et LLDP", "Jeremy J.36 ; Flackbox lab CDP/LLDP ; timers par défaut à retenir"),
    22: ("Services IP : horloge, NTP, DNS, DHCP, SSH", "Jeremy J.37, J.38, J.39, J.42 ; PowerCert « DNS », « DHCP » ; sur la VM Ubuntu : dnsmasq comme serveur DHCP/DNS"),
    23: ("SNMP et Syslog", "Jeremy J.40, J.41 ; PowerCert « SNMP » ; sur la VM Ubuntu : rsyslog et snmpd en récepteurs"),
    24: ("QoS : classification, marquage, queuing, shaping, policing", "Jeremy J.46, J.47 ; Sunny Classroom « QoS » ; Kevin Wallace « QoS Fundamentals »"),
    25: ("Wi-Fi : fonctionnement, canaux, association, sécurité", "Jeremy J.55-J.58 ; Sunny Classroom « Wireless » ; PowerCert « Wi-Fi standards », « WPA3 » ; Formip « Wi-Fi »"),
    26: ("Automatisation, SDN, REST API, Ansible/Puppet/Chef, JSON/YAML", "Jeremy J.59-J.63 ; Cisco DevNet Learning Labs ; Postman ; NetworkChuck « You need to learn Ansible » ; un vrai appel API avec curl depuis la VM"),
}

# Plan de révision CCNA, janvier 2027 : (date, heure, minute, durée, titre, lignes de description)
REV_START = (21, 0)
REVISION = [
    (date(2026, 12, 31), 21, 0, 30, "CCNA · Préparer janvier : acheter Boson, réserver l'examen",
     ["Acheter Boson ExSim-Max for CCNA 200-301 (~100 €).",
      "Réserver l'examen 200-301 chez Pearson VUE pour le mardi 2 février 2027 (centre ou en ligne surveillé). Report gratuit jusqu'à 24 h avant : réserver maintenant engage, sans risque.",
      "Télécharger les labs Packet Tracer et les decks Anki manquants de Jeremy's IT Lab.",
      "Lister les Skills où les quiz NetworkChuck ont été hésitants : ils orientent les deux semaines suivantes."]),
    # Semaine 1 : révision par domaine (Network Fundamentals 20 %, Network Access 20 %)
    (date(2027, 1, 4), 21, 0, 120, "CCNA révision 1 · Fondamentaux : OSI, câblage, Ethernet, IPv4",
     ["Jeremy's IT Lab J.1, J.2, J.3, J.5, J.6, J.7, J.8 en vitesse 1.5x, labs refaits sans la vidéo.",
      "Test chrono : 20 calculs de sous-réseau sur subnetipv4.com, noter le temps moyen.",
      "Anki : tout le deck réseau à jour."]),
    (date(2027, 1, 5), 21, 0, 120, "CCNA révision 1 · Subnetting, VLSM, IPv6",
     ["Jeremy J.13, J.14, J.15 (subnetting) et J.31, J.32, J.33 (IPv6).",
      "Objectif : moins de 30 s par calcul IPv4, EUI-64 et compression IPv6 sans hésiter.",
      "Lab : plan d'adressage VLSM complet pour la topologie PME du projet network-lab."]),
    (date(2027, 1, 6), 21, 0, 120, "CCNA révision 1 · VLANs, trunks, DTP/VTP, inter-VLAN",
     ["Jeremy J.16, J.17, J.18, J.19. Lab : configurer VLANs, trunk, router-on-a-stick et SVI de zéro, sans notes.",
      "Vérifier : show vlan brief, show interfaces trunk, show ip interface brief."]),
    (date(2027, 1, 7), 21, 0, 120, "CCNA révision 1 · STP, RSTP, EtherChannel",
     ["Jeremy J.20, J.21, J.22, J.23. Dessiner 3 topologies à 4 switches et élire root, root ports, designated ports à la main, puis vérifier avec show spanning-tree.",
      "Lab : PortFast, BPDU Guard, EtherChannel LACP."]),
    (date(2027, 1, 8), 21, 0, 120, "CCNA révision 1 · Routage statique, OSPF",
     ["Jeremy J.11, J.12, J.24, J.26, J.27, J.28. Lab : OSPF multi-routeurs avec routes statiques et défaut, puis casser une adjacence (zone, MTU, timers, masque) et la réparer.",
      "Savoir lire show ip route, show ip ospf neighbor, show ip ospf interface."]),
    (date(2027, 1, 9), 15, 0, 150, "CCNA révision 1 · Lab de synthèse : CCNA Mega Lab de Jeremy, partie 1",
     ["Jeremy's IT Lab « CCNA Mega Lab » (2 h 36 de vidéo, fichier .pkt gratuit) : faire la première moitié SEUL, en ne regardant la vidéo qu'après chaque section pour comparer.",
      "C'est le projet network-lab du curriculum : exporter les configs, dessiner le schéma, commit."]),
    # Semaine 2 : IP Connectivity 25 %, IP Services 10 %, Security 15 %, Automation 10 %
    (date(2027, 1, 11), 21, 0, 120, "CCNA révision 2 · FHRP, NAT",
     ["Jeremy J.29 (HSRP), J.44, J.45 (NAT). Lab : HSRP entre deux routeurs, NAT statique, dynamique et PAT vers un « Internet » simulé.",
      "Terminologie inside/outside local/global : 10 exemples écrits."]),
    (date(2027, 1, 12), 21, 0, 120, "CCNA révision 2 · Services IP : DHCP, DNS, NTP, SNMP, Syslog, SSH, FTP",
     ["Jeremy J.37 à J.43. Lab : routeur serveur DHCP et relais, NTP client/serveur, Syslog vers un serveur, SSH v2 uniquement.",
      "Fiche : ports et numéros à connaître (DHCP 67/68, DNS 53, NTP 123, SNMP 161/162, Syslog 514, SSH 22, FTP 20/21, TFTP 69)."]),
    (date(2027, 1, 13), 21, 0, 120, "CCNA révision 2 · Sécurité : ACL, port security, DHCP snooping, DAI, AAA",
     ["Jeremy J.34, J.35, J.48, J.49, J.50, J.51. Lab : ACL standard et étendues avec placement justifié, port security sticky, DHCP snooping et DAI sur les ports access.",
      "Concepts : AAA, 802.1X, VPN site-à-site vs accès distant, menaces courantes."]),
    (date(2027, 1, 14), 21, 0, 120, "CCNA révision 2 · Wi-Fi, QoS, architectures, cloud",
     ["Jeremy J.46, J.47 (QoS), J.52, J.53, J.54 (architectures LAN/WAN, virtualisation, cloud), J.55 à J.58 (Wi-Fi).",
      "Points d'examen : canaux 2,4 GHz non chevauchants, WPA2/WPA3, modes AP, WLC, marquage DSCP/CoS, queuing/shaping/policing."]),
    (date(2027, 1, 15), 21, 0, 120, "CCNA révision 2 · Automatisation : JSON, REST, SDN, Ansible",
     ["Jeremy J.59 à J.63. Lire et écrire du JSON/YAML, méthodes HTTP et codes de réponse, plan de contrôle vs données, Cisco DNA Center, Ansible/Puppet/Chef (push vs pull, agent ou non).",
      "Anki : passage complet du deck réseau, supprimer les cartes maîtrisées."]),
    (date(2027, 1, 16), 15, 0, 150, "CCNA révision 2 · Lab de synthèse : CCNA Mega Lab de Jeremy, partie 2",
     ["Seconde moitié du Mega Lab, même méthode. Puis casser 5 choses dans la topologie et les réparer en moins de 10 min chacune.",
      "Documenter dans network-lab : schéma final, configs, liste des pannes et solutions."]),
    # Semaines 3 et 4 : examens blancs Boson
    (date(2027, 1, 18), 21, 0, 150, "CCNA Boson · Examen blanc A",
     ["Boson ExSim-Max, examen A complet, 120 min, conditions réelles : pas de notes, pas de pause, téléphone éteint.",
      "Noter le score global et par domaine. Ne pas corriger ce soir."]),
    (date(2027, 1, 19), 21, 0, 120, "CCNA Boson · Correction de l'examen A",
     ["Pour chaque question fausse ou hésitante : lire l'explication Boson, écrire la règle en une phrase dans lab-notes, créer une carte Anki.",
      "Repérer les 2 domaines les plus faibles."]),
    (date(2027, 1, 20), 21, 0, 120, "CCNA Boson · Révision ciblée des domaines faibles (A)",
     ["Revoir les vidéos Jeremy et refaire les labs des 2 domaines les plus faibles de l'examen A.",
      "Subnetting chrono : 20 calculs."]),
    (date(2027, 1, 21), 21, 0, 150, "CCNA Boson · Examen blanc B",
     ["Boson ExSim-Max, examen B complet, 120 min, conditions réelles."]),
    (date(2027, 1, 22), 21, 0, 120, "CCNA Boson · Correction de l'examen B",
     ["Même méthode que pour A. Comparer les scores par domaine entre A et B."]),
    (date(2027, 1, 23), 15, 0, 150, "CCNA Boson · Labs de dépannage",
     ["Flackbox Lab Guide, section troubleshooting, et les labs de dépannage de Jeremy's IT Lab. Objectif : diagnostiquer avec show et debug avant de toucher à la config."]),
    (date(2027, 1, 25), 21, 0, 120, "CCNA Boson · Révision ciblée des domaines faibles (B)",
     ["Revoir et relaber les 2 domaines les plus faibles de B. Anki complet."]),
    (date(2027, 1, 26), 21, 0, 150, "CCNA Boson · Examen blanc C",
     ["Boson ExSim-Max, examen C complet, 120 min, conditions réelles."]),
    (date(2027, 1, 27), 21, 0, 120, "CCNA Boson · Correction de C et décision",
     ["Corriger C. Décision : score C supérieur à 85 % et A, B, C en progression = examen confirmé le 2 février.",
      "Sinon : reporter l'examen de deux semaines chez Pearson VUE (gratuit à plus de 24 h) et refaire un cycle révision ciblée + examen blanc."]),
    (date(2027, 1, 28), 21, 0, 120, "CCNA · Révision finale",
     ["Fiche des commandes show et de configuration par sujet, lue et retapée. Anki complet. Subnetting chrono.",
      "Pas de nouveau contenu."]),
    (date(2027, 1, 29), 21, 0, 60, "CCNA · Veille d'examen : logistique et repos",
     ["Vérifier la convocation Pearson VUE, la pièce d'identité (nom identique à la réservation), le trajet ou le test système OnVUE si en ligne.",
      "Lecture légère uniquement. Coucher tôt le lundi 1er."]),
    (date(2027, 2, 2), 10, 0, 180, "EXAMEN CCNA 200-301 (date cible)",
     ["Pearson VUE. Arriver 30 min avant. 120 min, environ 100 questions, labs de simulation inclus.",
      "Gestion du temps : marquer et passer toute question qui prend plus de 90 s, revenir à la fin. Les labs valent plusieurs points : ne pas les bâcler.",
      "Résultat affiché à la fin de l'examen."]),
]

LUC = [
    (0, "Creating Your Own Server", "Préparer la VM Ubuntu Server : SSH depuis Windows, utilisateur sudo, snapshot.", "TLCL ch. 1-2"),
    (1, "Get to know your server", "ssh, ls, uptime, free, df -h, uname -a. Clés SSH et fichier ~/.ssh/config.", "TLCL ch. 1-3"),
    (2, "Basic navigation", "man, hiérarchie des fichiers, cd, pwd, ls -la.", "TLCL ch. 3-4"),
    (3, "Power trip!", "sudo, fuseau horaire, hostname.", "TLCL ch. 9"),
    (4, "Installing software, exploring the file structure", "apt, mc, /etc/passwd, sshd_config, auth.log.", "TLCL ch. 14"),
    (5, "More or less...", "more, less, dotfiles, history, complétion, nano.", "TLCL ch. 5-6, 8"),
    (6, "Editing with vim", "vimtutor, le minimum vital de vim.", "TLCL ch. 12"),
    (7, "The server and its services", "Installer Apache2, systemctl start/stop, lire les logs.", "TLCL ch. 10"),
    (8, "The infamous grep and other text processors", "grep, cut, awk, tail, pipes, un peu de sed.", "TLCL ch. 19-20"),
    (9, "Diving into networking", "ss, nmap, ufw : ports ouverts, pare-feu.", "TLCL ch. 16"),
    (10, "Scheduling tasks", "cron, at, timers systemd.", "-"),
    (11, "Finding things...", "locate, find, grep -r, which.", "TLCL ch. 17"),
    (12, "Transferring files", "SFTP, scp, rsync.", "TLCL ch. 16"),
    (13, "Users and Groups", "adduser, visudo, un utilisateur restreint.", "TLCL ch. 9"),
    (14, "Who has permission?", "chmod, chown, umask ; ACL et SELinux en extension.", "TLCL ch. 9"),
    (15, "Deeper into repositories...", "Dépôts, multiverse, PPA.", "TLCL ch. 14"),
    (16, "Archiving and compressing", "tar, gzip, zip.", "TLCL ch. 18"),
    (17, "Build from the source", "wget, tar, ./configure, make, make install.", "TLCL ch. 23"),
    (18, "Logs, monitoring and troubleshooting", "journalctl, logrotate, top, htop.", "TLCL ch. 10"),
    (19, "Inodes, symlinks and other shortcuts", "Inodes, liens durs, liens symboliques, stat.", "TLCL ch. 4"),
    (20, "Scripting", "Shebang, permissions, $PATH, premiers scripts de filtrage de logs.", "TLCL ch. 24-27"),
    (21, "What's next?", "Bilan. Démarrer le projet server-toolkit du curriculum (bloc 1).", "TLCL ch. 28-36 en lecture continue"),
]

# ---------- parsing du PDF ----------

DATE_RE = re.compile(r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), (\w+) (\d{1,2}), (\d{4})$")
COUNT_RE = re.compile(r"^(\d+) tasks \| (\d+) due$")
TASK_RE = re.compile(r"^Skill (\d{2}) (Lesson [\d.]+|Lab) - (.+?)(?: \((S\d{2}-S?L\d{2}(?:\.\d+)?)\))?$")


def clean_text(s: str) -> str:
    """Répare les caractères mal encodés par l'export PDF (flèches, accents)."""
    for bad, good in (("â†”", "↔"), ("â ", "↔ "), ("Cafˆ'", "Café"), ("Caf'", "Café"), ("’?", "?"), ("Â·", ""), ("·", "")):
        s = s.replace(bad, good)
    return s


def dedupe_key(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def non_ascii(s: str) -> int:
    return sum(ord(c) > 127 for c in s)


def parse_plan(pdf: Path) -> list[dict]:
    text = "\n".join(p.extract_text() for p in PdfReader(str(pdf)).pages)
    days: dict[date, dict] = {}
    current = None
    for raw in text.splitlines():
        line = clean_text(raw.strip())
        m = DATE_RE.match(line)
        if m:
            d = datetime.strptime(f"{m.group(2)} {m.group(3)} {m.group(4)}", "%B %d %Y").date()
            current = days.setdefault(d, {"date": d.isoformat(), "announced": None, "tasks": []})
            continue
        if current is None:
            continue
        m = COUNT_RE.match(line)
        if m and current["announced"] is None:
            current["announced"] = int(m.group(1))
            continue
        m = TASK_RE.match(line)
        if m:
            skill, kind, title, lab_id = int(m.group(1)), m.group(2), m.group(3).strip(), m.group(4)
            if kind == "Lab":
                ttype = "skill_lab" if lab_id and "-SL" in lab_id else "lab"
            elif title.lower().startswith("quiz"):
                ttype = "quiz"
            else:
                ttype = "lesson"
            entry = {"skill": skill, "kind": kind, "title": title, "lab_id": lab_id, "type": ttype, "text": line}
            key = dedupe_key(line)
            dup = next((t for t in current["tasks"] if dedupe_key(t["text"]) == key), None)
            if dup is None:
                current["tasks"].append(entry)
            elif non_ascii(line) < non_ascii(dup["text"]):  # garder la version la plus propre
                dup.update(entry)
    out = [days[d] for d in sorted(days)]
    for d in out:
        d["estimate_min"] = sum(EST[t["type"]] for t in d["tasks"])
        d["skills"] = sorted({t["skill"] for t in d["tasks"]})
        if d["announced"] is not None and d["announced"] != len(d["tasks"]):
            print(f"  attention {d['date']} : {len(d['tasks'])} tâches lues, {d['announced']} annoncées", file=sys.stderr)
    return out


# ---------- ICS ----------

def ics_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def fold(line: str) -> str:
    """Repliement RFC 5545 : lignes de 75 octets max, continuation par espace."""
    out, cur = [], ""
    for ch in line:
        if len((cur + ch).encode("utf-8")) > 75:
            out.append(cur)
            cur = " " + ch
        else:
            cur += ch
    out.append(cur)
    return "\r\n".join(out)


VTIMEZONE = ""  # inutile en UTC


def dt_prop(name: str, value: datetime) -> str:
    """DTSTART/DTEND : forme UTC (suffixe Z) ou locale avec TZID selon TZ."""
    if TZ == "UTC":
        return f"{name}:{value.strftime('%Y%m%dT%H%M%S')}Z"
    return f"{name};TZID={TZ}:{value.strftime('%Y%m%dT%H%M%S')}"


# Rappels par défaut : 15 min avant, et le matin même (12 h avant une séance de 21h).
ALARMS_SESSION = [("-PT15M", "Séance dans 15 min"), ("-PT12H", "Ce soir : séance d'étude")]
ALARMS_WEEKEND = [("-PT15M", "Séance dans 15 min"), ("-PT2H", "Séance dans 2 h")]
ALARMS_KEY = [("-P7D", "Dans une semaine"), ("-P1D", "Demain"), ("-PT2H", "Dans 2 h")]


def event(uid: str, start: datetime, minutes: int, summary: str, description: str, categories: str,
          alarms: list[tuple[str, str]] | None = None) -> str:
    end = start + timedelta(minutes=minutes)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{stamp}",
        dt_prop("DTSTART", start),
        dt_prop("DTEND", end),
        f"SUMMARY:{ics_escape(summary)}",
        f"DESCRIPTION:{ics_escape(description)}",
        f"CATEGORIES:{ics_escape(categories)}",
    ]
    for trigger, text in (alarms or ALARMS_SESSION):
        lines += ["BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:{ics_escape(text + ' : ' + summary)}", f"TRIGGER:{trigger}", "END:VALARM"]
    lines.append("END:VEVENT")
    return "\r\n".join(fold(l) for l in lines)


def calendar(name: str, events: list[str]) -> str:
    head = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//ccna-curriculum//plan_to_ics//FR", "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH", f"X-WR-CALNAME:{ics_escape(name)}", f"X-WR-TIMEZONE:{TZ}"]
    tz_block = VTIMEZONE.replace("\n", "\r\n") + "\r\n" if VTIMEZONE else ""
    return "\r\n".join(head) + "\r\n" + tz_block + "\r\n".join(events) + "\r\nEND:VCALENDAR\r\n"


def shifted_dates(plan: list[dict]) -> dict[str, date]:
    """Date réelle de chaque journée du plan : jours ouvrés consécutifs depuis START_DATE."""
    mapping, day = {}, START_DATE
    for d in plan:
        while day.weekday() >= 5 or day in SKIP_DATES:
            day += timedelta(days=1)
        mapping[d["date"]] = day
        day += timedelta(days=1)
    return mapping


def ccna_events(plan: list[dict]) -> list[str]:
    first = date.fromisoformat(plan[0]["date"])
    shifted = shifted_dates(plan) if START_DATE else {}
    events = []
    for d in plan:
        orig = date.fromisoformat(d["date"])
        week = (orig - first).days // 7 + 1  # numéro de semaine du plan NetworkChuck
        day = shifted.get(d["date"], orig)
        minutes = max(CCNA_MIN, min(CCNA_MAX, ((d["estimate_min"] + 29) // 30) * 30))
        skills = d["skills"]
        skill_names = " / ".join(f"Skill {s:02d} : {SKILLS[s][0]}" for s in skills)
        summary = f"CCNA S{week} · " + " + ".join(f"Skill {s:02d}" for s in skills) + " · " + SKILLS[skills[-1]][0].split(" :")[0].split(",")[0]
        plan_line = f"Plan NetworkChuck Academy « Fall into CCNA », semaine {week} du plan"
        if day != orig:
            plan_line += f" (journée du {orig.strftime('%d/%m')} dans le plan d'origine)"
        lines = [plan_line + ".", "", skill_names, "",
                 f"Durée estimée : {d['estimate_min']} min ({len(d['tasks'])} tâches). Bloc réservé : {minutes} min.", "",
                 "Tâches du jour :"]
        for t in d["tasks"]:
            mark = "  ☐ "
            label = t["text"]
            if t["type"] == "skill_lab":
                label += "  [lab de synthèse]"
            lines.append(mark + label)
        lines += ["", "Ressources complémentaires (voir ressources-ccna-13-semaines.md) :"]
        for s in skills:
            lines.append(f"  Skill {s:02d} : {SKILLS[s][1]}")
        lines += ["", "Ensuite : 10 min d'Anki (deck Jeremy's IT Lab du jour), 10 exercices de subnetting à partir de la semaine 5."]
        if orig in RESCHEDULE:
            new_day, hh, mm = RESCHEDULE[orig]
            lines.insert(1, f"Séance de rattrapage : contenu prévu le {day.strftime('%d/%m')}, fait le {new_day.strftime('%d/%m')}.")
            summary = summary.replace("CCNA ", "CCNA rattrapage ")
            start = datetime.combine(new_day, datetime.min.time()).replace(hour=hh, minute=mm)
        else:
            start = datetime.combine(day, datetime.min.time()).replace(hour=CCNA_START[0], minute=CCNA_START[1])
        events.append(event(f"ccna-{d['date']}@ccna-curriculum", start, minutes, summary, "\n".join(lines), "CCNA,Réseau"))
    return events


def study_days(n: int) -> list[date]:
    """n jours ouvrés consécutifs à partir de START_DATE, hors SKIP_DATES."""
    out, day = [], START_DATE
    while len(out) < n:
        if day.weekday() < 5 and day not in SKIP_DATES:
            out.append(day)
        day += timedelta(days=1)
    return out


def week_no(day: date) -> int:
    monday = lambda d: d - timedelta(days=d.weekday())
    return (monday(day) - monday(START_DATE)).days // 7 + 1


def load_playlist() -> list[dict]:
    """Vidéos de la playlist : index, minutes, titre court, jour, type (cours / lab / extra)."""
    videos = []
    for raw in JEREMY_PLAYLIST.read_text(encoding="utf-8-sig").splitlines():
        if raw.count("|") < 2:
            continue
        idx, secs, title = raw.split("|", 2)
        m = re.search(r"Day (\d+)", title)
        if not m:  # Mega Lab, utilisé dans le plan de révision
            continue
        short = re.sub(r"\s*\|\s*CCNA 200-301 Complete Course\s*$", "", title)
        short = re.sub(r"^Free CCNA \| ", "", short)
        short = re.sub(r"\s*\|\s*(CCNA 200-301 )?Day \d+( \([^)]*\))?( Lab( \d)?| Extra)?", "", short)
        kind = "lab" if " Lab" in title else ("extra" if "Extra" in title else "cours")
        videos.append({"idx": int(idx), "min": round(int(secs) / 60), "title": short.strip(), "day": int(m.group(1)), "kind": kind})
    return videos


def jeremy_sessions() -> list[list[dict]]:
    """Regroupe les vidéos en séances : un jour par séance, avec les découpages et regroupements déclarés."""
    videos = load_playlist()
    days = sorted({v["day"] for v in videos})
    sessions: list[list[dict]] = []
    merged = {d for grp in JEREMY_MERGE for d in grp}
    for d in days:
        vids = [v for v in videos if v["day"] == d]
        if d in JEREMY_SPLIT:
            for pred in JEREMY_SPLIT[d]:
                sessions.append([v for v in vids if pred(v["title"])])
        elif d in merged:
            grp = next(g for g in JEREMY_MERGE if d in g)
            if d == grp[0]:
                sessions.append([v for v in videos if v["day"] in grp])
        else:
            sessions.append(vids)
    return sessions


def session_estimate(vids: list[dict]) -> tuple[int, int, int]:
    """(minutes de cours, minutes de labs, estimation totale)."""
    cours = sum(v["min"] for v in vids if v["kind"] != "lab")
    labs = sum(v["min"] for v in vids if v["kind"] == "lab")
    return cours, labs, round(cours * JEREMY_FACTOR + labs * 2 + JEREMY_FIXED_MIN)


def jeremy_events() -> list[str]:
    events = []
    sessions = jeremy_sessions()
    for day, vids in zip(study_days(len(sessions)), sessions):
        cours, labs, est = session_estimate(vids)
        minutes = max(CCNA_MIN, min(CCNA_MAX, ((est + 29) // 30) * 30))
        day_nos = sorted({v["day"] for v in vids})
        label = " + ".join(f"J.{n}" for n in day_nos)
        main = [v for v in vids if v["kind"] == "cours"]
        titles = main[0]["title"] if len(main) == 1 else " + ".join(v["title"] for v in main[:3]) + (" …" if len(main) > 3 else "")
        if any("Toolkit" in v["title"] for v in vids):
            titles = "STP Toolkit : PortFast, BPDU Guard, Root Guard, Loop Guard"
        summary = f"CCNA S{week_no(day)} · {label} · {titles}"
        skills = sorted({SKILL_BY_DAY[n] for n in day_nos})
        n_labs = sum(1 for v in vids if v["kind"] == "lab")
        lines = [f"Jeremy's IT Lab, CCNA 200-301 Complete Course v1.1 (gratuit, YouTube), {label}.",
                 f"Playlist : {JEREMY_URL}", "",
                 f"Cours : {cours} min de vidéo. Labs : {n_labs} ({labs} min de vidéo, à refaire seul ensuite). Durée estimée : {est} min. Bloc réservé : {minutes} min.", "",
                 "Déroulé (n° = position dans la playlist) :"]
        for v in vids:
            if v["kind"] == "lab":
                lines.append(f"  ☐ n°{v['idx']} Lab « {v['title']} » ({v['min']} min) : télécharger le .pkt sur jeremysitlab.com, regarder, puis refaire seul sans la vidéo")
            elif v["kind"] == "extra":
                lines.append(f"  ☐ n°{v['idx']} Extra « {v['title']} » ({v['min']} min) : comment utiliser les decks Anki du cours")
            else:
                lines.append(f"  ☐ n°{v['idx']} Day {v['day']} « {v['title']} » ({v['min']} min) : vidéo avec prise de notes, quiz de fin de vidéo")
        lines.append("  ☐ Importer le deck Anki du jour (jeremysitlab.com, gratuit) et faire la première passe")
        lines += ["", "Thème NetworkChuck équivalent : " + ", ".join(f"Skill {s:02d} ({SKILLS[s][0]})" for s in skills), "",
                  "Si une notion reste floue (voir ressources-ccna-13-semaines.md) :"]
        for s in skills:
            lines.append(f"  {re.sub(r'^Jeremy[^;]*;\s*', '', SKILLS[s][1])}")
        lines += ["", "Ensuite : 10 min d'Anki (tous les decks importés). À partir du J.13 : 10 calculs de subnetting par jour sur subnetipv4.com."]
        start = datetime.combine(day, datetime.min.time()).replace(hour=CCNA_START[0], minute=CCNA_START[1])
        uid = "ccna-j" + "-".join(f"{v['idx']:03d}" for v in vids[:1]) + f"-{'-'.join(str(n) for n in day_nos)}@ccna-curriculum"
        events.append(event(uid, start, minutes, summary, "\n".join(lines), "CCNA,Réseau"))
    return events


def linux_events() -> list[str]:
    events, day = [], LINUX_FIRST_DAY
    for n, title, content, tlcl in LUC:
        while day.weekday() not in (5, 6):
            day += timedelta(days=1)
        summary = f"Linux · LUC jour {n} · {title}"
        desc = "\n".join([
            f"Linux Upskill Challenge, jour {n} : {title}", "", content, "",
            f"Leçon locale : ressources/linuxupskillchallenge/docs/{n:02d}.md",
            f"Lecture associée : {tlcl} (ressources/tlcl/TLCL-25.12A.pdf)", "",
            "Méthode : lire la leçon (20 min), faire tous les exercices sur la VM (60 min), noter chaque commande apprise dans lab-notes et créer 5 cartes Anki (20 min), commit.",
            "Dimanche : ajouter 20 min de « casser et réparer » sur la VM (snapshot avant).",
        ])
        start = datetime.combine(day, datetime.min.time()).replace(hour=LINUX_START[0], minute=LINUX_START[1])
        events.append(event(f"linux-luc-{n:02d}@ccna-curriculum", start, LINUX_MINUTES, summary, desc, "Linux", ALARMS_WEEKEND))
        day += timedelta(days=1)
    return events


def revision_events() -> tuple[list[str], list[str]]:
    """Retourne (séances de révision, jalons). Les jalons vont dans un calendrier séparé
    pour recevoir des rappels à une semaine et un jour."""
    sessions, milestones = [], []
    for i, (day, hh, mm, minutes, summary, desc) in enumerate(REVISION):
        start = datetime.combine(day, datetime.min.time()).replace(hour=hh, minute=mm)
        text = "\n".join(desc) + "\n\nPlan de révision CCNA, voir curriculum.md section 4 et ressources-ccna-13-semaines.md section 2."
        key = summary.startswith("EXAMEN") or "Préparer" in summary or "décision" in summary or "Veille" in summary
        if key:
            milestones.append(event(f"ccna-jalon-{i:02d}-{day.isoformat()}@ccna-curriculum", start, minutes, summary, text, "CCNA,Jalon", ALARMS_KEY))
        else:
            alarms = ALARMS_WEEKEND if day.weekday() >= 5 else ALARMS_SESSION
            sessions.append(event(f"ccna-rev-{i:02d}-{day.isoformat()}@ccna-curriculum", start, minutes, summary, text, "CCNA,Révision", alarms))
    return sessions, milestones


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", type=Path, default=ROOT / "2-Fall into CCNA Study Plan.pdf")
    ap.add_argument("--out", type=Path, default=ROOT / "agenda")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    plan = parse_plan(args.pdf)
    (args.out / "ccna-plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
    # écriture binaire : le mode texte de Windows transformerait les CRLF en CR CR LF
    if SOURCE == "jeremy":
        (args.out / "ccna-fall-2026.ics").write_bytes(calendar("CCNA 2026 (Jeremy's IT Lab)", jeremy_events()).encode("utf-8"))
    else:
        (args.out / "ccna-fall-2026.ics").write_bytes(calendar("CCNA Fall 2026 (NetworkChuck)", ccna_events(plan)).encode("utf-8"))
    (args.out / "linux-track-2026.ics").write_bytes(calendar("Linux Upskill Challenge 2026", linux_events()).encode("utf-8"))
    rev, jalons = revision_events()
    (args.out / "ccna-revision-2027.ics").write_bytes(calendar("CCNA Révision 2027", rev).encode("utf-8"))
    (args.out / "ccna-jalons-2027.ics").write_bytes(calendar("CCNA Jalons et examen", jalons).encode("utf-8"))

    total = sum(d["estimate_min"] for d in plan)
    weeks = (date.fromisoformat(plan[-1]["date"]) - date.fromisoformat(plan[0]["date"])).days // 7 + 1
    print(f"{len(plan)} jours d'étude, {sum(len(d['tasks']) for d in plan)} tâches, "
          f"{total / 60:.0f} h estimées soit {total / 60 / weeks:.1f} h/semaine CCNA sur {weeks} semaines")
    if SOURCE == "jeremy":
        sessions = jeremy_sessions()
        days = study_days(len(sessions))
        ests = [session_estimate(s)[2] for s in sessions]
        video = sum(v["min"] for s in sessions for v in s)
        print(f"Jeremy's IT Lab : {len(sessions)} séances du {days[0]} au {days[-1]}, {video / 60:.0f} h de vidéo, "
              f"{sum(ests) / 60:.0f} h estimées, par séance min {min(ests)} / médiane {sorted(ests)[len(ests) // 2]} / max {max(ests)} min")
    elif START_DATE:
        sh = shifted_dates(plan)
        print(f"plan décalé : du {min(sh.values())} au {max(sh.values())} (jours sautés : {sorted(SKIP_DATES)})")
    per_day = sorted(d["estimate_min"] for d in plan)
    print(f"par jour : min {per_day[0]} min, médiane {per_day[len(per_day) // 2]} min, max {per_day[-1]} min")
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()
