# Curriculum : Infrastructure & Code (Linux based)

> **Objectif :** devenir opérationnel sur l'infrastructure moderne (Linux, réseau, automatisation, conteneurs, cloud) en 12 mois, avec un portfolio de projets concrets et 2 à 3 certifications.
> **Base de départ :** le fichier `reponse.md` (feuille de route CCNA), corrigé et élargi.

---

## 0. Analyse de `reponse.md`

### Ce qui est bon
- Le choix des ressources CCNA est solide : Jeremy's IT Lab est effectivement la référence gratuite, Packet Tracer est l'outil adapté, Boson est le bon simulateur d'examen.
- La logique "réseau d'abord, puis automatisation, puis cloud" est cohérente.
- Le tableau de compétences réseau (VLAN, STP, OSPF, ACL, NAT) est correct pour le périmètre CCNA.

### Ce qui manque ou déséquilibre
| Problème | Impact |
| :--- | :--- |
| Linux n'apparaît qu'au mois 7, en une ligne | Or c'est le socle de tout le reste (serveurs, conteneurs, cloud, automatisation). Il doit être en **premier**. |
| Aucun scripting shell (Bash) | Impossible d'administrer Linux ou d'automatiser sans Bash. |
| Python arrive uniquement via Netmiko | Trop étroit. Python sert aussi aux APIs, au traitement de données, aux outils internes. |
| Ni Git, ni conteneurs (Docker), ni Infrastructure as Code (Terraform, Ansible) | Ce sont les compétences les plus demandées sur les postes infra actuels. |
| Pas de projets ni de livrables | Sans portfolio, la reconversion est difficile à prouver. |
| Pas de cadence hebdomadaire | Le plan reste théorique, difficile à suivre au quotidien. |
| Le "pourquoi l'IA" est marketing | Ne change rien au contenu à apprendre. Supprimé ici. |

### Ce qu'on change
1. **Linux et Bash passent en premier** (mois 1 à 3), le réseau CCNA vient juste après et se poursuit en parallèle.
2. On ajoute **Git, Python, Docker, Ansible, Terraform, un peu de Kubernetes et d'observabilité**.
3. Chaque bloc a un **projet livrable** versionné sur GitHub.
4. Une **semaine type** et une **checklist de validation** par bloc.

---

## 1. Principes de travail

- **Rythme cible :** 10 à 12 h/semaine. Si vous avez moins, allongez les blocs, ne sautez rien.
- **Règle 30/70 :** 30 % de théorie (vidéo, lecture), 70 % de pratique dans un terminal ou un lab.
- **Un seul carnet de notes** en Markdown, versionné sur GitHub. Chaque commande apprise y est notée avec un exemple.
- **Jamais de copier-coller sans comprendre.** Retapez les commandes.
- **Casser et réparer :** chaque semaine, cassez volontairement quelque chose dans votre VM et réparez-le.
- **Anki** (répétition espacée) pour les commandes, ports, protocoles, masques réseau. 10 min/jour.

---

## 2. Le lab (en place depuis le 30 septembre 2026)

| Élément | Outil | État |
| :--- | :--- | :--- |
| Hyperviseur | VMware Workstation Pro 26H1u1 (gratuit pour usage personnel) | Installé, atténuations canal latéral désactivées. Hyper-V reste actif pour WSL2. |
| VM Linux principale | Ubuntu Server 22.04 LTS, hostname `ubnu`, utilisateur `naj`, NAT | En place, à jour, snapshot « 30Sept ». 22.04 suffit pour tout le curriculum (support jusqu'en avril 2027). |
| VM Linux secondaire | Ubuntu Server 24.04 (UEFI, Secure Boot) puis Rocky Linux 9 | À créer quand le bloc 1 arrive au réseau entre deux VM, puis au bloc 5 pour la famille Red Hat. |
| Terminal Windows | Windows Terminal, alias SSH `ubnu`, clé ed25519 | En place. WSL2 (Ubuntu 24.04) en complément pour le quotidien. |
| Simulateur réseau | Cisco Packet Tracer | Gratuit via NetAcad, à installer avant la séance J.1. |
| Versionnage | GitHub, dépôt `lab-notes` | Créé, premier commit poussé le 30 septembre. |
| Éditeur | VS Code + extension Remote-SSH | À connecter sur l'alias `ubnu`. |

**Livrable jour 1 (atteint) :** SSH vers la VM depuis Windows, premier commit sur GitHub.

### WSL ou VM ? Ubuntu ou Arch ?

Vous avez déjà trois distributions WSL sur cette machine (Ubuntu 24.04, Arch, Debian). Répartition recommandée :

| Environnement | Rôle | Pourquoi |
| :--- | :--- | :--- |
| **Ubuntu 24.04 sous WSL** | Terminal quotidien : Bash, Git, Python, Docker, Ansible, Terraform, lecture des cours | Rapide, intégré à VS Code et Windows Terminal. Tous les supports du curriculum (Linux Upskill Challenge, TLCL, LFCS, labs Ansible) supposent Debian/Ubuntu et `apt`. |
| **VM Ubuntu Server sous VMware Workstation** (déjà en place ; Hyper-V ferait aussi l'affaire) | Labs d'administration : réseau (netplan, ufw, IP fixe), services systemd, SSH serveur, "casser et réparer", cibles Ansible | WSL n'a ni vrai démarrage, ni pile réseau que vous contrôlez, ni disque à partitionner, ni GRUB à réparer. Une VM, si. Prenez des snapshots avant chaque séance "casser et réparer". |
| **Arch sous WSL** | Terrain de jeu secondaire, 1 h/semaine maximum | Excellent pour comprendre comment Linux est assemblé (pacman, wiki Arch, tout à la main). Mais aucun serveur d'entreprise ne tourne sous Arch : vous ne trouverez ni Ubuntu/Debian ni RHEL/Rocky en production remplacés par Arch. Ne pas en faire la base d'apprentissage. |

En résumé : **restez sur Ubuntu comme distribution principale**, ajoutez une VM Ubuntu Server pour les labs, et gardez Arch pour la curiosité. Quand vous arriverez au bloc 5, ajoutez une VM Rocky Linux pour découvrir la famille Red Hat (`dnf`, SELinux, firewalld), qui pèse autant qu'Ubuntu sur le marché de l'emploi.

---

## 3. Parcours en 6 blocs

Chaque bloc a un **focus principal** et un **fil de maintenance** (entretien de ce qui est déjà acquis).

### Bloc 1 : Linux fondamentaux + Bash (mois 1 à 2)

**Focus :** être à l'aise dans un terminal Linux, comprendre le système, écrire des scripts simples.

**Contenu :**
- Système de fichiers, permissions, utilisateurs et groupes, sudo, liens durs et symboliques, inodes
- Processus, services (systemd), journaux (journalctl, logs d'authentification), planification (cron, timers)
- Processus en profondeur : signaux (kill, SIGTERM vs SIGKILL), priorités (nice, renice), tâches en arrière-plan (jobs, fg, bg), limites (ulimit), notions de cgroups
- Disques et stockage : partitions, systèmes de fichiers (ext4, xfs), montage et fstab, ajout d'un disque à la VM, LVM, swap, surveillance de l'espace (df, du)
- Démarrage : séquence de boot, GRUB, initramfs, cibles systemd ; réparer un boot cassé depuis le snapshot
- Paquets (apt, dnf), mises à jour, dépôts, snap
- Réseau côté Linux : ip, ss, dig, ping, traceroute, curl, configuration netplan, pare-feu (ufw / nftables), capture avec tcpdump
- SSH avancé : clés, config, tunnels, agent
- Revue d'un serveur en 5 minutes : uptime et charge, mémoire, disque, services en échec, dernières connexions
- Éditeur : vim (les bases suffisent) ou nano
- Outils texte : grep, sed, awk, cut, sort, find, xargs, pipes
- Bash : variables, conditions, boucles, fonctions, codes de retour, gestion d'erreurs (`set -euo pipefail`)
- Git : init, commit, branch, merge, push, pull, .gitignore, résolution de conflits simples

**Ressources :**
- Livre gratuit : *The Linux Command Line* de William Shotts (linuxcommand.org) - référence principale
- Linux Journey, désormais hébergé par LabEx à labex.io/linuxjourney (linuxjourney.com y redirige) : parcours guidé court, toujours gratuit et open source. Le reste de LabEx (labs dans le navigateur, 3 lancements de VM par jour en gratuit) n'est pas nécessaire : vous avez une vraie VM et Boot.dev. Pas d'abonnement Pro.
- Linux Upskill Challenge (linuxupskillchallenge.org) - 20 jours d'exercices sur un serveur, excellent
- OverTheWire Bandit (overthewire.org/wargames/bandit) - jeu de terminal, très formateur
- MIT *The Missing Semester* - shell, vim, Git, en vidéo
- Pro Git (git-scm.com/book) - chapitres 1 à 3 seulement

**Projet livrable :**
Un dépôt GitHub `server-toolkit` contenant 4 scripts Bash :
1. `backup.sh` : sauvegarde d'un répertoire avec rotation et journalisation
2. `healthcheck.sh` : vérifie CPU, RAM, disque, services critiques, envoie un résumé
3. `user-onboard.sh` : crée un utilisateur avec clé SSH et groupe, de façon idempotente
4. `deploy-static-site.sh` : installe nginx et publie une page

**Checklist de validation :**
- [ ] Je navigue et manipule des fichiers sans chercher les commandes
- [ ] Je diagnostique un service qui ne démarre pas avec systemctl et journalctl
- [ ] Je configure une IP fixe et un pare-feu sur ma VM
- [ ] Mes 4 scripts tournent sans erreur et gèrent les cas d'échec
- [ ] Je fais un commit propre par fonctionnalité

---

### Bloc 2 : Réseau CCNA (mois 3 à 6)

**Focus :** comprendre et configurer un réseau d'entreprise. Préparer et passer le CCNA 200-301.

> **Colonne vertébrale du bloc : Jeremy's IT Lab, CCNA 200-301 Complete Course** (gratuit, YouTube, 63 jours, chacun avec vidéo, quiz, lab Packet Tracer et deck Anki téléchargeables sur jeremysitlab.com). Ses 63 jours (126 vidéos en v1.1, labs compris) sont répartis en **63 séances du jeudi 1er octobre au 30 décembre 2026**, un jour par soir de semaine (6 et 18 novembre sautés, J.21 coupé en deux, J.62 et J.63 regroupés). C'est le calendrier `agenda/ccna-fall-2026.ics`.
> Le PDF `2-Fall into CCNA Study Plan.pdf` (NetworkChuck Academy) sert de structure de référence en 26 Skills pour `ressources-ccna-13-semaines.md`, mais le cours NetworkChuck est payant (250 $) et n'est pas nécessaire. Le bloc 1 (Linux) se fait **en parallèle** à raison de 4 h/semaine le week-end.

**Contenu (les 26 Skills du PDF, regroupés) :**
- Modèle OSI/TCP-IP, Ethernet, câblage
- IPv4, subnetting (à maîtriser par cœur, exercices quotidiens), IPv6
- Switching : VLAN, trunk, STP, EtherChannel
- Routage : statique, OSPF, routage inter-VLAN
- Services : DHCP, DNS, NAT, NTP, SNMP, Syslog
- Sécurité : ACL, port security, DHCP snooping, AAA, VPN (notions)
- Wi-Fi, QoS (notions)
- Automatisation : REST API, JSON, SDN, Ansible/Puppet/Chef (notions CCNA)

**Fil de maintenance :** 2 h/semaine sur Linux. Mettez en pratique chaque notion réseau côté Linux (ex. : tcpdump, Wireshark, configuration de routes, serveur DHCP ou DNS avec dnsmasq).

**Ressources :**
- Jeremy's IT Lab - Free CCNA 200-301 Complete Course (YouTube) + ses labs Packet Tracer + ses cartes Anki
- Cisco Packet Tracer (NetAcad)
- Subnetting : subnettingpractice.com, 10 min/jour jusqu'à faire un calcul en moins de 30 secondes
- Wireshark : les vidéos de Chris Greer (YouTube) pour lire des captures
- Boson ExSim-Max (payant, ~100 €) : à acheter au mois 5. Passez l'examen quand vous dépassez 85 %.

**Projet livrable :**
Un dépôt `network-lab` avec :
1. Une topologie Packet Tracer "PME" : 2 sites, VLANs, routage inter-VLAN, OSPF, NAT, ACL, DHCP. Fichier `.pkt` + schéma + configs exportées.
2. Un lab Linux : 2 VMs sur des sous-réseaux différents, une VM Ubuntu qui fait routeur + pare-feu + DHCP. Documentation reproductible.

**Checklist de validation :**
- [ ] Je calcule un sous-réseau de tête en moins de 30 secondes
- [ ] Je configure VLAN, trunk, OSPF, NAT, ACL sans regarder de notes
- [ ] Je lis une capture Wireshark et j'explique un handshake TCP et une requête DNS
- [ ] Score Boson > 85 %
- [ ] **CCNA 200-301 obtenu** (mois 6 ou 7)

---

### Bloc 3 : Python pour l'infrastructure (mois 6 à 7)

**Focus :** écrire des outils Python propres qui manipulent des fichiers, des APIs et des équipements.

**Contenu :**
- Bases : types, fonctions, modules, gestion d'erreurs, fichiers, environnements virtuels (venv), pip
- Formats : JSON, YAML, CSV
- Bibliothèques : `requests` (APIs REST), `argparse`, `logging`, `pathlib`, `subprocess`
- Réseau : Netmiko, NAPALM (configuration d'équipements), `paramiko` (SSH)
- Bonnes pratiques : structure de projet, `README`, tests simples avec `pytest`, formatage avec `ruff`

**Ressources :**
- *Automate the Boring Stuff with Python* (automatetheboringstuff.com) - gratuit, chapitres 1 à 12
- Python for Network Engineers de Kirk Byers (cours gratuit par email, référence pour Netmiko)
- Documentation officielle Python (tutoriel)
- David Bombal - Python for Network Engineers (Udemy, déjà dans `reponse.md`, optionnel)

**Projet livrable :**
Dépôt `infra-tools` :
1. `inventory.py` : lit un inventaire YAML de serveurs et équipements, interroge chaque machine en SSH, produit un rapport JSON et Markdown
2. `net-backup.py` : sauvegarde les configs de vos routeurs/switches (Packet Tracer ne le permet pas, utilisez GNS3 ou Containerlab avec des images libres comme FRRouting ou Arista cEOS)
3. `api-client.py` : consomme une API publique et une API locale (nginx ou un petit service Flask que vous écrivez)

**Checklist de validation :**
- [ ] J'écris un script Python de 100 lignes structuré, avec gestion d'erreurs et logs
- [ ] Je lis et produis du JSON/YAML sans hésiter
- [ ] Je me connecte en SSH à 5 machines depuis Python et j'exécute des commandes
- [ ] Mon projet a un README, un `requirements.txt` et des tests

---

### Bloc 4 : Conteneurs, services et CI/CD (mois 8 à 9)

**Focus :** déployer des applications en conteneurs, comprendre les services web, automatiser les livraisons.

**Contenu :**
- Docker : images, conteneurs, volumes, réseaux, Dockerfile, Docker Compose
- Services : nginx en reverse proxy, TLS avec Let's Encrypt (ou certificats auto-signés en lab), bases de données (PostgreSQL) en conteneur
- Concepts à savoir expliquer : forward proxy vs reverse proxy, cache HTTP, load balancer (L4 vs L7), HTTP/HTTPS et handshake TLS
- DNS côté opérateur : enregistrements A, AAAA, CNAME, MX, TXT, TTL ; authentification du courrier (SPF, DKIM, DMARC), notions SMTP/IMAP. Lab : dnsmasq ou une zone sur un DNS public gratuit
- CI/CD : GitHub Actions (lint, tests, build d'image, déploiement sur la VM)
- Sécurité de base : images minimales, utilisateur non-root, scan d'images (Trivy), secrets hors du dépôt puis chiffrés dans le dépôt avec sops + age (Vault viendra plus tard)
- Observabilité : Prometheus + Grafana + node_exporter, logs centralisés (Loki ou simplement rsyslog)

**Fil de maintenance :** Anki réseau 10 min/jour, 1 script Python par semaine.

**Ressources :**
- Documentation officielle Docker (Get started) - la meilleure ressource
- KodeKloud : Docker for the Absolute Beginner (labs gratuits)
- Documentation GitHub Actions (Quickstart)
- Vidéos TechWorld with Nana (YouTube) : Docker, Prometheus, CI/CD
- Play with Docker (labs.play-with-docker.com) pour tester sans installer

**Projet livrable :**
Dépôt `app-stack` :
1. Une petite application (Flask ou FastAPI) + PostgreSQL + nginx, le tout en Docker Compose
2. Pipeline GitHub Actions : lint, tests, build, push de l'image, déploiement SSH sur la VM
3. Monitoring Prometheus/Grafana avec un dashboard et une alerte (disque > 80 %)

**Checklist de validation :**
- [ ] J'écris un Dockerfile propre et multi-étapes
- [ ] Je déploie une stack 3 services en Compose avec volumes persistants
- [ ] Un push sur `main` déclenche tests + déploiement automatiquement
- [ ] Je vois les métriques de ma VM dans Grafana

---

### Bloc 5 : Infrastructure as Code et configuration (mois 10 à 11)

**Focus :** décrire toute l'infrastructure en code, reproductible et versionnée.

**Contenu :**
- Ansible : inventaire, playbooks, rôles, variables, templates Jinja2, idempotence, Ansible Vault
- Terraform : providers, ressources, variables, state, modules. Appliqué au cloud (bloc 6) et en local (provider Docker ou libvirt)
- Bonnes pratiques : structure de dépôt, environnements (dev/prod), revue de code, documentation

**Ressources :**
- Documentation Ansible (Getting started) + Jeff Geerling *Ansible for DevOps* (livre, et sa série YouTube gratuite "Ansible 101")
- Documentation Terraform (tutoriels HashiCorp, gratuits)
- KodeKloud : Ansible et Terraform for Beginners

**Projet livrable :**
Dépôt `infra-as-code` :
1. Rôles Ansible qui reconstruisent entièrement vos VMs depuis zéro : durcissement SSH, utilisateurs, pare-feu, Docker, monitoring. Une seule commande : `ansible-playbook site.yml`.
2. Terraform qui crée vos conteneurs ou VMs de lab (provider Docker en local)
3. Réutilisation de `infra-tools` (bloc 3) comme module dynamique d'inventaire

**Checklist de validation :**
- [ ] Je reconstruis une VM neuve en état de production en une commande
- [ ] Mes playbooks sont idempotents (relancer ne change rien)
- [ ] Je comprends le state Terraform et je sais le protéger
- [ ] Aucun secret en clair dans mes dépôts

---

### Bloc 6 : Cloud et Kubernetes (mois 11 à 12)

**Focus :** transposer tout ce qui précède dans le cloud, et découvrir l'orchestration.

**Contenu :**
- AWS (ou Azure, choisissez un seul fournisseur) : IAM, VPC, sous-réseaux, groupes de sécurité, EC2, S3, load balancer. Tout en Terraform, jamais à la main sauf pour découvrir.
- Notions d'architecture : haute disponibilité (multi-AZ), sauvegardes et restauration, serverless (une fonction Lambda déclenchée par S3), patrons cloud courants
- Coûts : Free Tier, alertes de budget dès le premier jour.
- Kubernetes : pods, deployments, services, ingress, configmaps, secrets. En local avec k3s ou kind sur votre VM.
- Certification : préparation AWS Solutions Architect Associate (SAA-C03) ou Azure AZ-104.

**Ressources :**
- Stephane Maarek - AWS SAA (Udemy, déjà dans `reponse.md`) ou Adrian Cantrill (plus profond)
- Documentation Terraform AWS Provider
- Kubernetes : *Kubernetes The Hard Way* (Kelsey Hightower) pour comprendre, puis KodeKloud CKA labs
- TechWorld with Nana : Kubernetes complete course (YouTube)

**Projet livrable :**
Dépôt `cloud-deploy` :
1. VPC complet en Terraform avec sous-réseaux publics/privés, bastion, instance web derrière un load balancer
2. Votre `app-stack` (bloc 4) déployée sur cette infra via Ansible
3. La même application déployée sur un cluster k3s local avec manifests Kubernetes

**Checklist de validation :**
- [ ] Je crée et détruis une infra AWS complète en Terraform sans cliquer dans la console
- [ ] Je sais expliquer VPC, subnet, route table, security group et leur équivalent en réseau physique
- [ ] Je déploie une app sur Kubernetes et je débogue un pod qui ne démarre pas
- [ ] Certification cloud obtenue (fin mois 12 ou après)

---

## 4. Calendrier récapitulatif

Calendrier aligné sur le cours Jeremy's IT Lab (démarrage le 1er octobre 2026) :

| Période | Focus principal | En parallèle | Livrable | Certification |
| :--- | :--- | :--- | :--- | :--- |
| 1er oct - 30 déc 2026 | Réseau CCNA (Jeremy's IT Lab J.1 à J.63, 63 séances) + Practical Networking les week-ends d'octobre | Linux + Bash + Git, 4 h/sem | `network-lab`, `server-toolkit` | - |
| Janv 2027 | Révision par domaine (2 sem.) puis Boson ExSim A, B, C (2 sem.), calendriers `agenda/ccna-revision-2027.ics` et `ccna-jalons-2027.ics` | Linux | `network-lab` finalisé | **CCNA**, cible le 2 février 2027 |
| Fév - mars 2027 | Python infra | Anki réseau | `infra-tools` | - |
| Avr - mai 2027 | Docker, CI/CD, monitoring | Python 1 script/sem | `app-stack` | - |
| Juin - juil 2027 | Ansible (calendrier `agenda/ansible-101-2027.ics`), Terraform | Docker | `infra-as-code` | LFCS (optionnel) |
| Août - sept 2027 | Cloud, Kubernetes | Tout | `cloud-deploy` | **AWS SAA** ou AZ-104 |

**Ordre de priorité des certifications :** CCNA (socle, reconnu) > AWS SAA ou AZ-104 (employabilité) > LFCS (valide Linux, utile si vous visez sysadmin) > Terraform Associate (facile une fois le bloc 5 fait). **Optionnel, orientation sécurité :** CompTIA Security+ (SY0-701), vendor-neutral, reconnu par les RH, à préparer entre le CCNA et le bloc 4 avec le cours gratuit de Professor Messer. Pas en parallèle du plan CCNA.

### Au-delà du curriculum (repères roadmap.sh DevOps)

Sujets que la roadmap DevOps de roadmap.sh liste et que ce curriculum ne couvre pas, à aborder après le bloc 6, dans cet ordre : GitOps (ArgoCD ou Flux) ; traçage distribué et OpenTelemetry (avec Jaeger) ; gestion de secrets centralisée (HashiCorp Vault) ; service mesh (Istio ou Linkerd, seulement si Kubernetes devient votre quotidien) ; un second langage compilé (Go, le langage de Docker, Kubernetes et Terraform). PowerShell est utile si vous administrez aussi du Windows, mais hors périmètre ici.

---

## 5. Charge horaire et semaine type

### Pendant le cours CCNA (jusqu'au 30 décembre 2026) : 15 à 17 h par semaine

Le cours de Jeremy's IT Lab totalise 56 h de vidéo (126 vidéos : cours et labs). En comptant la vidéo de cours avec pauses et prise de notes (×1,3), chaque lab regardé puis refait seul (×2), et 10 min de quiz et d'import Anki, la charge réelle est de 93 h :

| Poste | Par jour | Par semaine |
| :--- | :--- | :--- |
| CCNA, lundi à vendredi, 21h00 | 1h30 à 2h30 selon le jour (médiane 1h33 de tâches + marge) | ~10 h |
| Linux Upskill Challenge, samedi et dimanche 10h00-12h00 | 2h | 4 h |
| Practical Networking, samedi et dimanche 15h00, du 3 au 31 octobre seulement (fondamentaux, puis subnetting) | 1h à 2h | 2 à 3 h en octobre |
| Anki (réseau) + subnetting, tous les jours | 10 à 15 min | ~1h30 |
| **Total** | | **~15 h** |

Les calendriers `.ics` du dossier `agenda/` encodent exactement ce rythme (générés par `outils/plan_to_ics.py`, horaires modifiables en tête du script). Le week-end est volontairement plus léger que dans une semaine type classique : le cours CCNA en semaine est dense.

Si 15 h ne sont pas tenables : gardez le CCNA intact (c'est un plan daté avec des lives) et réduisez Linux à une seule séance le samedi. Le bloc 1 durera alors jusqu'à fin janvier au lieu de mi-décembre.

### Après le CCNA (à partir de janvier 2027) : 12 h par semaine

| Jour | Durée | Activité |
| :--- | :--- | :--- |
| Lundi | 1h30 | Théorie : vidéo ou chapitre du bloc en cours, notes dans `lab-notes` |
| Mardi | 1h30 | Pratique : reproduire la théorie dans le lab |
| Mercredi | 1h30 | Théorie + Anki |
| Jeudi | 1h30 | Pratique : avancer le projet du bloc |
| Vendredi | 1h | Maintenance : fil secondaire (Linux, Python ou réseau selon le bloc) |
| Samedi | 3h | Projet du bloc : session longue, commit en fin de séance |
| Dimanche | 2h | Révision de la semaine, "casser et réparer", mise à jour des notes, planification de la semaine suivante |

Anki 10 min chaque jour en plus.

---

## 6. Ressources transverses

### Déjà disponibles hors ligne dans ce dossier

Voir `ressources/README.md` pour le détail et les licences.

| Ressource | Emplacement | Bloc |
| :--- | :--- | :--- |
| Linux Upskill Challenge (cours complet, 21 jours) | `ressources/linuxupskillchallenge/docs/` | 1 |
| The Linux Command Line, 7e édition (PDF, 596 p.) | `ressources/tlcl/TLCL-25.12A.pdf` | 1 |
| Automate the Boring Stuff 3e + Workbook (HTML et Markdown) | `ressources/automate-the-boring-stuff/` | 3 |
| Flashcards du workbook (1127 cartes) pour Anki | `ressources/anki/automate-workbook.apkg` | 3 |
| Générateur de decks Anki depuis Markdown/CSV/TSOFA | `outils/anki/md2anki.py` (voir son README) | tous |
| Fiche : historique et raccourcis Bash, sudo, motif conf.d | `fiches/bash-historique-raccourcis.md` + cartes `cartes/bash-historique.md` | 1 |
| Fiche : méthode Anki (séance, boutons, bonnes cartes, réglages, pièges) | `fiches/methode-anki.md` | tous |
| Ressources CCNA par Skill | `ressources-ccna-13-semaines.md` | 2 |
| Ansible 101 (Jeff Geerling, 15 épisodes YouTube) | lien dans `ressources/README.md` | 5 |

**Méthode Anki recommandée :** un fichier Markdown de cartes par sujet dans `cartes/`, régénéré avec `md2anki.py` à chaque fin de semaine. Les cartes existantes gardent leur historique de révision. Les fiches de synthèse vont dans `fiches/`, chaque fiche pointant vers son fichier de cartes.

### Banque d'exercices : le programme ALX (vault local `C:\utils\alx-se\vault`)

Énoncés de projets au format Holberton (objectifs, lectures, tâches à rendre), sans vidéo. À utiliser comme exercices corrigés par vous-même, un projet à la fois, dans un dépôt **privé** (contenu propriétaire ALX). Les énoncés absents du vault (0x09, 0x0B, 0x0C, 0x0F, 0x10, 0x13, 0x18 du parcours DevOps) se retrouvent sur GitHub par leur nom.

| Bloc | Projets ALX (`Projects/`) |
| :--- | :--- |
| 1 | 0x00 Shell basics, 0x01 permissions, 0x02 I/O redirections et filtres, 0x04 loops et parsing, 0x05 processes et signals, 0x06 regex, Command line for the win, 0x02 vi, 0x03 Git |
| 2 | 0x07 et 0x08 Networking basics ; en fin de CCNA, 0x11 « What happens when you type google.com » (article de synthèse dans lab-notes) |
| 3 | 0x00 à 0x0B Python, 0x10 et 0x11 Python Network, 0x0D et 0x0E SQL, 0x0F ORM |
| 4 | Web stack debugging 0 à 4 (conteneurs cassés à réparer), 0x1A Application server, 0x14 MySQL, 0x15 et 0x16 API, 0x19 Postmortem |
| 5 | 0x0A Configuration management, à refaire en Ansible plutôt qu'en Puppet |
| après 6 | 0x16 C - Simple Shell, pour comprendre fork, exec et les signaux de l'intérieur |

Hors périmètre : le reste du parcours C, AirBnB clone, JavaScript, onboarding et contenus de communauté.

### En ligne

- **roadmap.sh/devops** et **roadmap.sh/linux** : cartes de référence, pas des cours. Les blocs 1, 4 et 6 ont été complétés avec leurs sujets manquants (disques et LVM, boot, signaux, DNS et courrier, proxies, serverless). Cochez-y les sujets au fur et à mesure.
- **TryHackMe** (gratuit, premium ~14 €/mois) : labs Linux dans le navigateur. Salles "Linux Fundamentals 1 à 3" et "Network Fundamentals" en complément du bloc 1 ; parcours "Pre-Security" si la sécurité vous attire.
- **NextWork** (gratuit) : projets AWS guidés avec compte rendu de portfolio, dont le "7-day DevOps challenge" et les projets VPC. Pour le bloc 6, en refaisant ensuite chaque projet en Terraform. Activer les alertes de budget AWS avant.
- **Boot.dev** (abonnement en cours) : exercices interactifs dans le navigateur, avec un mentor IA. À utiliser comme complément quotidien de 20 à 30 min, jamais à la place des labs sur la VM. Répartition : cours Linux, Shell et Git pendant le bloc 1 (après la séance LUC du week-end) ; cours Python dès que le CCNA est passé, puis SQL pendant le bloc 4 ; cours Docker et CI/CD au bloc 4, Kubernetes au bloc 6 ; Go seulement après le bloc 6. Le parcours "DevOps" de la plateforme suit à peu près l'ordre de ce curriculum, cochez-y les cours au fil des blocs.
- **Linux Foundation Training** (training.linuxfoundation.org) : à utiliser pour les **certifications** (LFCS au bloc 5, CKA seulement après le bloc 6), pas pour les cours. Les cours gratuits sont textuels et datés, les payants chers pour le format ; KodeKloud prépare mieux les mêmes examens. Exception : LFS158 (Introduction to Kubernetes, gratuit) en deux soirées avant KodeKloud au bloc 6. Acheter le bon d'examen LFCS pendant les remises de fin novembre 2026 (40 à 50 %, valable 12 mois) pour un passage à l'été 2027. Certifications valables 2 ans.
- **Sadservers.com** : scénarios de pannes Linux à réparer, parfait pour le dimanche
- **KillerCoda** : labs interactifs gratuits (Linux, Kubernetes, Docker)
- **Julia Evans (wizardzines.com)** : fiches illustrées sur le réseau, le shell, les conteneurs
- **r/linuxadmin, r/networking, r/devops** : pour lire des problèmes réels
- **Documentation officielle** : toujours la référence avant les vidéos

---

## 7. État au 2 octobre 2026 et prochaines étapes

Fait : VM, SSH, dépôt `lab-notes`, Anki synchronisé (decks Bash et Python importés), les sept agendas Google importés avec leurs notifications, séance J.1 le 1er octobre.

À faire :

1. Ce soir 21h : séance J.2, Interfaces and Cables.
2. Samedi 3 octobre 10h : jour 0 du Linux Upskill Challenge (l'essentiel est déjà fait, enchaîner sur le jour 1). 15h : Practical Networking, séance 1.
3. Chaque soir de semaine à 21h : la séance CCNA de l'agenda.
4. Dimanche : cartes Anki de la semaine dans `cartes/`, regénérer avec `md2anki`, commit de `lab-notes`.
5. Fin décembre : checklist du bloc 1 (section 3) et jalon du 31 décembre (Boson, réservation de l'examen).

Les blocs 1 et 2 avancent en parallèle jusqu'à fin décembre. Le bloc 3 ne commence qu'après l'examen CCNA.
