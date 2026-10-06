# CCNA Day 48 : Security Fundamentals / Fondamentaux de la sécurité

> Source : Jeremy's IT Lab, « Free CCNA | Security Fundamentals | Day 48 » (39 min), vidéo n°97 de la playlist (cours) ; « Kali Linux Demo | Day 48 Lab » (10 min), vidéo n°98 (démonstration, pas de fichier Packet Tracer). Fiche rédigée à partir des transcriptions le 6 octobre 2026. Le CCNA n'est pas une certification de cybersécurité : il demande les fondamentaux nécessaires à tout professionnel IT, et beaucoup de vocabulaire à mémoriser.

## 🇫🇷 Version française

### 1. Pourquoi la sécurité : la triade CIA

| Lettre | Principe | Signification |
| :--- | :--- | :--- |
| **C** | **Confidentialité** (*confidentiality*) | Seuls les utilisateurs autorisés accèdent aux données. Il y a des degrés : public (site web), plus ou moins secret. |
| **I** | **Intégrité** (*integrity*) | Les données ne sont ni altérées ni modifiées par des utilisateurs non autorisés ; elles sont correctes et authentiques. |
| **A** | **Disponibilité** (*availability*) | Réseau et systèmes opérationnels et accessibles aux utilisateurs autorisés (ressources internes pour le personnel, site web pour les clients). |

Chaque attaque menace une ou plusieurs lettres de la triade.

### 2. Quatre termes définis dans les objectifs d'examen

- **Vulnérabilité** (*vulnerability*) : toute faiblesse potentielle pouvant compromettre la CIA d'un système. Une faiblesse seule n'est pas un problème : les fenêtres d'une maison sont des vulnérabilités, les maisons gardent des fenêtres.
- **Exploit** : ce qui peut potentiellement servir à exploiter la vulnérabilité. Une pierre peut casser la fenêtre ; une pierre seule n'est pas un problème.
- **Menace** (*threat*) : la possibilité réelle qu'une vulnérabilité soit exploitée. Le cambrioleur qui veut casser la fenêtre avec la pierre ; un pirate exploitant une faille de votre système.
- **Mitigation** (*mitigation technique*) : ce qui protège contre les menaces. Dépend de la menace. À appliquer partout où une vulnérabilité peut être exploitée : clients, serveurs, switches, routeurs, pare-feu, et aussi accès physique (baie fermée, porte sécurisée).

**Aucun système n'est parfaitement sûr.** Plus ou moins sûr, jamais garanti : même avec détection de malware sur le pare-feu et le meilleur antivirus, le risque n'est jamais zéro.

### 3. Les attaques courantes (catégories principales, il en existe bien d'autres)

| Attaque | Mécanisme | Cible dans la triade |
| :--- | :--- | :--- |
| **Déni de service, DoS** (*denial-of-service*) | Exemple : **TCP SYN flood**. L'attaquant envoie d'innombrables SYN ; la cible répond SYN-ACK et attend un ACK qui n'arrive jamais ; les connexions incomplètes remplissent la table de connexions TCP (elles expirent, mais l'attaquant continue) ; la cible ne peut plus accepter de connexions légitimes. Les SYN-ACK ne reviennent pas à l'attaquant car il usurpe son adresse IP source. | **A** |
| **DDoS** (*distributed DoS*) | L'attaquant infecte de nombreux ordinateurs avec un malware : ce groupe est un **botnet**, qui lance ensemble le déni de service (par exemple un SYN flood). Bien plus puissant qu'un attaquant seul. | **A** |
| **Usurpation** (*spoofing*) | Utiliser une **fausse adresse source** (IP ou MAC). Ce n'est pas une attaque unique mais une technique commune à beaucoup. Exemple : **DHCP exhaustion** (ou *starvation*) : des DHCP Discover envoyés en masse avec des MAC usurpées ; le serveur réserve une adresse par Offer ; le pool (par exemple 250 adresses) se vide ; les vrais hôtes n'obtiennent plus d'adresse. Le SYN flood est aussi du spoofing. Toutes les usurpations ne sont pas des DoS. | **A** ici |
| **Réflexion** (*reflection*) | L'attaquant envoie du trafic à un **réflecteur** (par exemple un serveur DNS) en usurpant comme source l'adresse de la **cible** ; le réflecteur répond à la cible. Exemple : attaquant 1.2.3.4, source usurpée 5.6.7.8 (la cible), réflecteur 8.8.8.8. | **A** |
| **Amplification** | Réflexion où un **petit** trafic envoyé déclenche un **gros** trafic du réflecteur vers la cible. Vulnérabilités DNS et NTP connues (articles Cloudflare « DNS amplification attack », « NTP amplification attack »). | **A** |
| **Homme du milieu** (*man-in-the-middle*) | L'attaquant se place entre source et destination pour **écouter** ou **modifier** le trafic. Exemple : **ARP spoofing** / **ARP poisoning** (encore du spoofing). PC1 demande par ARP la MAC de 10.0.0.1 (SRV1) ; la requête est diffusée, SRV1 et l'attaquant la reçoivent ; SRV1 répond ; l'attaquant attend un peu puis envoie **sa** réponse ARP, qui arrive en dernier et **écrase** l'entrée légitime dans la table ARP de PC1. Le trafic PC1 → SRV1 passe par l'attaquant, qui le lit puis le relaie, ou le modifie avant de le relayer. | **C** et **I** |
| **Reconnaissance** | Pas une attaque en soi : collecte d'informations, souvent publiques, pour une attaque future. `nslookup` pour l'adresse IP d'un site, puis sondage des ports ouverts ; requête **WHOIS** pour e-mails, téléphones, adresses, qui alimentent ensuite l'ingénierie sociale. | préparation |
| **Malware** (*malicious software*) | **Virus** : infecte un programme hôte, se propage quand le logiciel est partagé ou téléchargé, puis corrompt ou modifie des fichiers. **Ver** (*worm*) : autonome, pas de programme hôte, se propage seul sans action de l'utilisateur ; la propagation congestionne le réseau et une **charge utile** (*payload*) peut faire d'autres dégâts. **Cheval de Troie** (*trojan horse*) : logiciel nuisible déguisé en logiciel légitime, propagé par l'utilisateur (pièce jointe, téléchargement). Ces types se définissent par **la façon d'infecter et de se propager**, pas par ce qu'ils font ensuite. | C, I ou A |
| **Ingénierie sociale** (*social engineering*) | Cible **les personnes**, la partie la plus vulnérable de tout système, par manipulation psychologique : faire révéler une information confidentielle ou faire exécuter une action. Aucune configuration de routeur ou de pare-feu n'y remédie. | C, I ou A |
| **Mots de passe** | Deviner (rare) ; **attaque par dictionnaire** : un programme essaie une liste de mots et mots de passe courants ; **force brute** (*brute force*) : toutes les combinaisons de lettres, chiffres et caractères spéciaux, demande une machine très puissante, quasi impossible si le mot de passe est fort. | **C** |

**Les formes d'ingénierie sociale citées :**

- **Phishing** (hameçonnage) : e-mails frauduleux imitant une entreprise légitime (Amazon, banque, carte de crédit) avec un lien vers un faux site identique à la page de connexion réelle ; l'utilisateur y saisit ses identifiants. Exemple montré : « votre compte Amazon est verrouillé suite à une connexion suspecte, vérifiez vos informations ».
- **Spear phishing** : phishing ciblé, par exemple les employés d'une entreprise précise.
- **Whaling** : phishing visant des personnes de haut profil, par exemple un président de société.
- **Vishing** (*voice phishing*) : par téléphone (« bonjour, Jeremy du service informatique, nous devons réinitialiser votre mot de passe, pouvez-vous me donner l'actuel ? »).
- **Smishing** (*SMS phishing*) : par SMS.
- **Watering hole** (point d'eau) : compromettre un site que la cible visite souvent et y placer un lien malveillant ; la confiance dans le site fait cliquer sans réfléchir.
- **Tailgating** (talonnage) : entrer dans une zone restreinte en suivant une personne autorisée, qui tient poliment la porte.

Résumé de Jeremy : l'ingénierie sociale n'exploite pas les systèmes informatiques, elle exploite les employés.

### 4. Mots de passe forts et authentification multifacteur

**Mot de passe fort :** au moins **8 caractères**, de préférence plus (plus c'est long, plus la force brute est longue) ; mélange de **majuscules et minuscules**, de **lettres et chiffres**, un ou plusieurs **caractères spéciaux** (?, !) ; **changé régulièrement**. Le nom d'utilisateur est souvent facile à deviner (l'adresse e-mail) : toute la sécurité repose sur le mot de passe.

**Authentification multifacteur (MFA) :** prouver son identité avec plus qu'un couple identifiant/mot de passe. Avec deux facteurs, on parle d'**authentification à deux facteurs**. Les trois catégories :

| Catégorie | Exemples |
| :--- | :--- |
| **Quelque chose que vous savez** (*something you know*) | identifiant et mot de passe, code PIN |
| **Quelque chose que vous avez** (*something you have*) | notification à valider dans une application d'authentification sur le téléphone, badge scanné |
| **Quelque chose que vous êtes** (*something you are*) | biométrie : visage, paume, empreinte, rétine |

Même si l'attaquant obtient le mot de passe, il ne peut pas se connecter.

**Certificats numériques :** prouvent l'identité du détenteur, surtout pour les sites web. L'entité envoie une **CSR** (*certificate signing request*) à une **CA** (*certificate authority*) qui génère et signe le certificat. Le navigateur affiche un symbole indiquant un certificat valide ; c'est ainsi qu'on sait que le site est bien jeremysitlab.com et non une copie.

### 5. AAA : Authentication, Authorization, Accounting

Cadre pour contrôler et surveiller les utilisateurs d'un système.

| A | Définition | Exemple |
| :--- | :--- | :--- |
| **Authentification** | Vérifier l'**identité** de l'utilisateur | Connexion, idéalement en MFA |
| **Autorisation** | Accorder les **accès et permissions** appropriés | Accès à certains fichiers et services, pas à d'autres |
| **Comptabilisation** (*accounting*) | **Enregistrer les activités** de l'utilisateur | Journaliser une modification de fichier, une connexion, une déconnexion |

Les entreprises utilisent un **serveur AAA** ; celui de Cisco est **ISE** (*Identity Services Engine*). Deux protocoles :

| Protocole | Standard | Transport |
| :--- | :--- | :--- |
| **RADIUS** | ouvert | **UDP 1812 et 1813** |
| **TACACS+** | propriétaire Cisco | **TCP 49** |

Pour le CCNA : connaître les noms, les ports, et surtout **la différence entre les trois A**, citée telle quelle dans les objectifs d'examen.

### 6. Éléments d'un programme de sécurité

Un programme de sécurité est l'ensemble des politiques et procédures de l'entreprise. Trois éléments à connaître :

- **Programmes de sensibilisation** (*user awareness*) : rendre les employés conscients des menaces. Exemple : envoyer de faux e-mails de phishing ; ceux qui cliquent sont informés qu'il s'agissait d'un exercice.
- **Programmes de formation** (*user training*) : plus formels, sessions dédiées sur les politiques de sécurité, les mots de passe forts, les menaces ; à l'arrivée dans l'entreprise puis à intervalles réguliers.
- **Contrôle d'accès physique** : n'autoriser que les personnes habilitées dans les locaux techniques et salles serveurs, y compris en interne. Serrures multifacteur (badge + empreinte = quelque chose que vous avez + quelque chose que vous êtes). Les badges sont flexibles : les droits se retirent de façon centralisée, badge rendu ou non.

### 7. Pièges d'examen

- **Vulnérabilité ≠ exploit ≠ menace** : la menace est la possibilité réelle que la vulnérabilité soit exploitée ; la mitigation réduit cette possibilité.
- **DoS/DDoS, spoofing, réflexion/amplification visent la disponibilité (A)** ; l'homme du milieu (ARP spoofing) vise la **confidentialité et l'intégrité (C, I)**.
- Les catégories d'attaques se recoupent : un SYN flood est à la fois DoS et spoofing ; une DHCP exhaustion est spoofing et DoS.
- **MFA = au moins deux catégories différentes.** Rétine + empreinte n'est pas du multifacteur (deux fois « quelque chose que vous êtes »).
- **Authentification = qui vous êtes ; autorisation = ce que vous pouvez faire ; comptabilisation = ce que vous avez fait.** Journaliser une connexion est de la comptabilisation, pas de l'authentification.
- RADIUS **UDP 1812/1813**, ouvert ; TACACS+ **TCP 49**, Cisco.
- Les types de malware se définissent par leur mode de propagation, pas par leurs effets.

### 8. Le lab : démonstration de l'attaque DHCP exhaustion (vidéo n°98)

Pas de fichier Packet Tracer ce jour : la vidéo de cours n'a montré aucune configuration. Jeremy fait une démonstration dans **EVE-NG** d'une attaque présentée en cours, et la vidéo suivante (Day 49, port security) montre comment l'empêcher sur un switch Cisco.

**Topologie :** R1 est le serveur DHCP ; une machine attaquante sous **Kali Linux** (distribution utilisée en test d'intrusion, avec des outils préinstallés) ; PC1 à connecter ensuite.

1. Sur R1, état initial :

```text
R1# show run | section dhcp        ! pool 192.168.1.0/24, passerelle 192.168.1.1, DNS 8.8.8.8
R1# show ip dhcp pool              ! 254 adresses disponibles (253 réellement, R1 garde la sienne), 0 louée
R1# show ip dhcp binding           ! table vide
```

2. Sur Kali, l'outil **Yersinia** (`yersinia -G` pour l'interface graphique) : menu Attack > DHCP > « sending DISCOVER packet », marqué comme causant un **DoS**. Le compteur de paquets DHCP monte rapidement ; l'attaque continue tant qu'on ne l'arrête pas.

3. Sur R1 :

```text
R1# show ip dhcp pool              ! 253 adresses louées sur 254 : le pool entier est pris
R1# show ip dhcp binding           ! 192.168.1.2 à .254 toutes attribuées, chacune à une MAC différente
```

Chaque adresse a une MAC unique : l'attaquant **usurpe la MAC source** de chaque Discover, R1 croit voir des hôtes différents.

4. PC1 connecté au switch (`ipconfig /all` : DHCP activé) n'obtient qu'une adresse **APIPA 169.254.x.x/16**, l'adresse lien-local IPv4, l'équivalent de la lien-local IPv6 : pas d'adresse du serveur, `ping 192.168.1.1` échoue, `ipconfig /renew` échoue.

5. Fin de l'attaque : lien de l'attaquant supprimé, puis sur R1 :

```text
R1# clear ip dhcp binding *        ! vide la table des baux (commande vue au Day 39)
```

PC1 refait `ipconfig /renew`, obtient une adresse, et accède à Internet.

### 9. Le quiz (5 questions, plus une question bonus Boson ExSim non transcrite)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quelle partie de la triade CIA garantit que les systèmes fonctionnent et sont accessibles ? | **Disponibilité** (D) | Confidentialité = données accessibles aux seuls autorisés ; intégrité = données modifiables par les seuls autorisés ; les autres options (C, E, F) sont des éléments de AAA, pas de la triade. |
| Quel terme désigne la possibilité réelle qu'une faiblesse soit exploitée pour attaquer un système ? | **Menace** (A) | La menace est la possibilité qu'une vulnérabilité soit exploitée ; la mitigation réduit cette possibilité. |
| Des serrures exigeant un badge scanné et un code : exemple de quoi ? (deux réponses) | **Contrôle d'accès physique** (C) et **authentification multifacteur** (D) | Badge = quelque chose que vous avez, code = quelque chose que vous savez. |
| Lequel n'est PAS un exemple de MFA ? | **Scan rétinien puis empreinte digitale** (C) | Deux actions, mais une seule catégorie, « quelque chose que vous êtes » ; le MFA exige au moins deux catégories différentes. |
| Qu'est-ce qui relève de la comptabilisation (accounting) dans AAA ? | **Journaliser la date et l'heure de connexion d'un utilisateur** (D) | A et C sont de l'autorisation, B de l'authentification. |

---

## 🇬🇧 English version

### 1. Why security: the CIA triad

| Letter | Principle | Meaning |
| :--- | :--- | :--- |
| **C** | **Confidentiality** | Only authorized users can access data. There are degrees: public (company website), more or less secret. |
| **I** | **Integrity** | Data is not tampered with or modified by unauthorized users; it is correct and authentic. |
| **A** | **Availability** | Network and systems are operational and accessible to authorized users (internal resources for staff, website for customers). |

Every attack threatens one or more letters of the triad.

### 2. Four terms explicitly in the exam topics

- **Vulnerability:** any potential weakness that can compromise the CIA of a system. A weakness alone is not a problem: a house's windows are vulnerabilities, houses keep having windows.
- **Exploit:** something that can potentially be used to exploit the vulnerability. A rock can break the window; a rock alone is not a problem.
- **Threat:** the real potential of a vulnerability being exploited. A robber who wants to break the window with the rock; a hacker exploiting a flaw in your system.
- **Mitigation technique:** something that protects against threats. Depends on the threat. Implement it everywhere a vulnerability can be exploited: clients, servers, switches, routers, firewalls, and physical access too (secure rack, secure door).

**No system is perfectly secure.** More or less secure, never guaranteed: even with malware detection on the firewall and the best antivirus, the chance of infection is never 0.

### 3. Common attacks (main categories, many more exist)

| Attack | Mechanism | Triad target |
| :--- | :--- | :--- |
| **Denial-of-service, DoS** | Example: **TCP SYN flood**. The attacker sends countless SYNs; the target replies SYN-ACK and waits for an ACK that never comes; incomplete connections fill the TCP connection table (they time out, but the attacker keeps going); the target can no longer accept legitimate connections. The SYN-ACKs never reach the attacker because the source IP is spoofed. | **A** |
| **DDoS** (distributed DoS) | The attacker infects many computers with malware: this group is a **botnet**, which launches the DoS together (e.g. a SYN flood). Far more powerful than a single attacker. | **A** |
| **Spoofing** | Using a **fake source address** (IP or MAC). Not a single attack but a technique common to many. Example: **DHCP exhaustion** (or *starvation*): a flood of DHCP Discover messages with spoofed MACs; the server reserves one address per Offer; the pool (say 250 addresses) empties; real hosts cannot get an address. The SYN flood is spoofing too. Not all spoofing attacks are DoS. | **A** here |
| **Reflection** | The attacker sends traffic to a **reflector** (e.g. a DNS server) with the **target's** address spoofed as source; the reflector replies to the target. Example: attacker 1.2.3.4, spoofed source 5.6.7.8 (the target), reflector 8.8.8.8. | **A** |
| **Amplification** | A reflection attack where a **small** amount of traffic sent triggers a **large** amount from the reflector to the target. Known DNS and NTP vulnerabilities (Cloudflare articles "DNS amplification attack", "NTP amplification attack"). | **A** |
| **Man-in-the-middle** | The attacker sits between source and destination to **eavesdrop** or **modify** traffic. Example: **ARP spoofing** / **ARP poisoning** (spoofing again). PC1 sends an ARP request for 10.0.0.1 (SRV1); it is broadcast, SRV1 and the attacker receive it; SRV1 replies; the attacker waits briefly then sends **its own** ARP reply, which arrives last and **overwrites** the legitimate entry in PC1's ARP table. PC1's traffic to SRV1 goes through the attacker, who reads then forwards it, or modifies it before forwarding. | **C** and **I** |
| **Reconnaissance** | Not an attack itself: gathering information, often public, for a future attack. `nslookup` for a site's IP, then probing open ports; a **WHOIS** query for emails, phone numbers, addresses, which then feed social engineering. | preparation |
| **Malware** (malicious software) | **Virus:** infects a host program, spreads as software is shared or downloaded, then corrupts or modifies files. **Worm:** standalone, no host program, spreads on its own without user interaction; the spread congests the network and a **payload** can do further harm. **Trojan horse:** harmful software disguised as legitimate, spread by user interaction (email attachment, download). These types are defined by **how they infect and spread**, not by what they do afterwards. | C, I or A |
| **Social engineering** | Targets **people**, the most vulnerable part of any system, through psychological manipulation: making the target reveal confidential information or perform an action. No router or firewall configuration fixes this. | C, I or A |
| **Password attacks** | Guessing (rare); **dictionary attack:** a program tries a list of common words and passwords; **brute force:** every combination of letters, numbers and special characters, needs a very powerful computer, nearly hopeless against a strong password. | **C** |

**Social engineering forms mentioned:**

- **Phishing:** fraudulent emails imitating a legitimate business (Amazon, bank, credit card) with a link to a fake site identical to the real login page; the user enters their credentials. Example shown: "your Amazon account has been locked due to a suspicious login, verify your account information".
- **Spear phishing:** targeted phishing, e.g. employees of a specific company.
- **Whaling:** phishing aimed at high-profile individuals, e.g. a company president.
- **Vishing** (voice phishing): over the phone ("Hi, this is Jeremy from IT, we need to reset your password, could you tell me the current one?").
- **Smishing** (SMS phishing): via text messages.
- **Watering hole:** compromise a site the target visits frequently and place a malicious link there; trust in the site makes them click without thinking.
- **Tailgating:** entering a restricted area by walking in behind an authorized person, who politely holds the door.

Jeremy's summary: social engineering does not exploit IT systems, it exploits employees.

### 4. Strong passwords and multi-factor authentication

**Strong password:** at least **8 characters**, preferably more (longer means harder to brute force); a mix of **upper and lower case**, of **letters and numbers**, one or more **special characters** (?, !); **changed regularly**. The username is often easy to guess (the email address): all the security rests on the password.

**Multi-factor authentication (MFA):** proving identity with more than a username and password. With two factors it is called **two-factor authentication**. The three categories:

| Category | Examples |
| :--- | :--- |
| **Something you know** | username and password, PIN |
| **Something you have** | approving a notification in an authenticator app on your phone, a scanned badge |
| **Something you are** | biometrics: face, palm, fingerprint, retina |

Even if the attacker learns the password, they cannot log in.

**Digital certificates:** prove the identity of the holder, mainly for websites. The entity sends a **CSR** (certificate signing request) to a **CA** (certificate authority), which generates and signs the certificate. The browser shows a symbol for a valid certificate; that is how you know the site really is jeremysitlab.com and not a fake.

### 5. AAA: Authentication, Authorization, Accounting

A framework for controlling and monitoring users of a system.

| A | Definition | Example |
| :--- | :--- | :--- |
| **Authentication** | Verifying the user's **identity** | Logging in, ideally with MFA |
| **Authorization** | Granting the appropriate **access and permissions** | Access to some files and services, not others |
| **Accounting** | **Recording the user's activities** | Logging a file change, a login, a logout |

Enterprises use a **AAA server**; Cisco's is **ISE** (Identity Services Engine). Two protocols:

| Protocol | Standard | Transport |
| :--- | :--- | :--- |
| **RADIUS** | open | **UDP 1812 and 1813** |
| **TACACS+** | Cisco proprietary | **TCP 49** |

For the CCNA: know the names, the ports, and above all **the difference between the three A's**, stated directly in the exam topics.

### 6. Security program elements

A security program is the enterprise's set of security policies and procedures. Three elements to know:

- **User awareness programs:** make employees aware of threats. Example: sending fake phishing emails; those who click are told it was part of an awareness program.
- **User training programs:** more formal, dedicated sessions on security policies, strong passwords, avoiding threats; when employees join and at regular intervals.
- **Physical access control:** only authorized users in network closets and data center floors, including from inside the company. Multifactor locks (badge + fingerprint = something you have + something you are). Badge systems are flexible: permissions are removed centrally, badge returned or not.

### 7. Exam traps

- **Vulnerability ≠ exploit ≠ threat:** the threat is the real possibility that the vulnerability is exploited; mitigation reduces that possibility.
- **DoS/DDoS, spoofing, reflection/amplification target availability (A)**; man-in-the-middle (ARP spoofing) targets **confidentiality and integrity (C, I)**.
- Attack categories overlap: a SYN flood is both DoS and spoofing; DHCP exhaustion is spoofing and DoS.
- **MFA = at least two different categories.** Retina + fingerprint is not multi-factor (twice "something you are").
- **Authentication = who you are; authorization = what you may do; accounting = what you did.** Logging a login is accounting, not authentication.
- RADIUS **UDP 1812/1813**, open; TACACS+ **TCP 49**, Cisco.
- Malware types are defined by how they spread, not by their effects.

### 8. The lab: DHCP exhaustion attack demo (video n°98)

No Packet Tracer file this day: the lecture showed no configuration. Jeremy demonstrates in **EVE-NG** one of the attacks from the lecture; the next video (Day 49, port security) shows how to prevent it on a Cisco switch.

**Topology:** R1 is the DHCP server; an attacker machine running **Kali Linux** (a distribution used in penetration testing, with preinstalled tools); PC1 to be connected afterwards.

1. On R1, initial state:

```text
R1# show run | section dhcp        ! pool 192.168.1.0/24, gateway 192.168.1.1, DNS 8.8.8.8
R1# show ip dhcp pool              ! 254 available addresses (really 253, R1 keeps its own), 0 leased
R1# show ip dhcp binding           ! empty table
```

2. On Kali, the **Yersinia** tool (`yersinia -G` for the GUI): Attack > DHCP > "sending DISCOVER packet", flagged as causing a **DoS**. The DHCP packet counter rises rapidly; the attack continues until stopped.

3. On R1:

```text
R1# show ip dhcp pool              ! 253 of 254 addresses leased: the whole pool is taken
R1# show ip dhcp binding           ! 192.168.1.2 to .254 all assigned, each to a different MAC
```

Each address has a unique MAC: the attacker **spoofs the source MAC** of every Discover, so R1 thinks each comes from a different host.

4. PC1 connected to the switch (`ipconfig /all`: DHCP enabled) only gets an **APIPA 169.254.x.x/16** address, the IPv4 link-local range, equivalent to the IPv6 link-local address: no address from the server, `ping 192.168.1.1` fails, `ipconfig /renew` fails.

5. End of attack: attacker's link deleted, then on R1:

```text
R1# clear ip dhcp binding *        ! clears the binding table (command from Day 39)
```

PC1 runs `ipconfig /renew` again, gets an address, and reaches the Internet.

### 9. The quiz (5 questions, plus a Boson ExSim bonus question not transcribed)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which part of the CIA triad ensures systems are running and accessible by users? | **Availability** (D) | Confidentiality = data accessible only by authorized users; integrity = data modified only by authorized users; options C, E, F are aspects of AAA, not the triad. |
| Which term refers to the real possibility that a potential weakness is taken advantage of to attack a system? | **Threat** (A) | A threat is the possibility that a vulnerability is exploited; mitigation techniques reduce that possibility. |
| Door locks requiring a badge scan and a pass code: an example of what? (two answers) | **Physical access control** (C) and **multi-factor authentication** (D) | Badge = something you have, pass code = something you know. |
| Which is NOT an example of multi-factor authentication? | **A retina scan then a fingerprint scan** (C) | Two actions, but one category, "something you are"; MFA needs at least two different categories. |
| Which is considered Accounting in the AAA model? | **Logging the date and time a user logged in** (D) | A and C are authorization, B is authentication. |
