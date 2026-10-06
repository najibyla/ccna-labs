# CCNA Day 30 : TCP & UDP

> Source : Jeremy's IT Lab, vidéo n°61 « TCP & UDP | Day 30 » (cours, 34 min) et vidéo n°62 « Wireshark Demo (TCP/UDP) | Day 30 Lab » (démo Wireshark, 11 min) de la playlist. Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Les fonctions de la couche 4

- Sujet d'examen 1.5 : **comparer TCP à UDP**. Une compréhension de haut niveau suffit, pas la mécanique détaillée.
- **Transfert transparent des données entre hôtes finaux** (*transparent transfer of data*) : la couche transport encapsule les données avec un en-tête de couche 4 puis s'appuie sur les couches 3, 2 et 1 pour les livrer inchangées ; les hôtes ignorent les détails du réseau sous-jacent.
- **Services aux applications** (fournis par TCP, pas par UDP) : transfert fiable (*reliable data transfer*), récupération d'erreur (*error recovery*), séquencement (*data sequencing*), contrôle de flux (*flow control*).
- **Adressage de couche 4 : les numéros de port** (*port numbers*). Rien à voir avec les ports physiques d'un switch. Deux rôles :
  - **Identifier le protocole de couche application** : c'est le **port de destination** (TCP 80 = HTTP pour les pages web, TCP 21 = FTP pour transférer des fichiers).
  - **Multiplexage de sessions** (*session multiplexing*) : une session est un échange de données entre deux équipements ou plus. Le **port source est choisi aléatoirement** par l'hôte ; combiné au port de destination, il identifie la session. Dans la réponse du serveur, les ports source et destination sont **inversés** (80 → 50000). Deux connexions vers le même serveur utilisent des ports source différents.
- **Plages IANA** (*Internet Assigned Numbers Authority*) :
  - **Well-known** : **0 à 1023**, protocoles majeurs, très strictement réglementés.
  - **Registered** : **1024 à 49151**, enregistrement requis mais moins strict.
  - **Ephemeral** (privés, dynamiques) : **49152 à 65535**, utilisés par les hôtes pour le **port source aléatoire**.
- Les ports sont une fonction des **deux** protocoles, TCP et UDP.

### 2. TCP (*Transmission Control Protocol*)

- **Orienté connexion** (*connection-oriented*) : les hôtes établissent une connexion avant d'envoyer des données.
- **Communication fiable** : le destinataire doit **acquitter** chaque segment (le segment est le PDU de couche 4) ; un segment non acquitté est renvoyé.
- **Séquencement** : le champ *sequence number* permet de remettre les segments dans l'ordre.
- **Contrôle de flux** : le destinataire peut demander de ralentir ou d'accélérer l'envoi.
- **En-tête TCP**, champs à connaître : **ports source et destination (16 bits chacun, donc 65536 = 2^16 ports)**, **sequence number** et **acknowledgment number**, les drapeaux (*flags*) **ACK, SYN, FIN** (établissement et fin de connexion), **window size** (contrôle de flux). Pas besoin de mémoriser tout l'en-tête.
- **Three-way handshake** (établissement) : PC1 → **SYN** ; SRV1 → **SYN-ACK** ; PC1 → **ACK**. À retenir absolument.
- **Four-way handshake** (fin de connexion) : PC1 → **FIN** ; SRV1 → **ACK** ; SRV1 → **FIN** ; PC1 → **ACK**.
- **Séquence et acquittement** : chaque hôte choisit un **numéro de séquence initial aléatoire** (ex. PC1 = 10, PC2 = 50). **Acquittement anticipé** (*forward acknowledgment*) : le champ ACK indique le **numéro de séquence du prochain segment attendu** (le segment 10 est acquitté par ACK 11). Exemple : SYN seq 10 ; SYN-ACK seq 50, ack 11 ; ACK seq 11, ack 51 ; puis seq 51, ack 12.
- **Retransmission** : PC1 envoie seq 21, il n'arrive pas ; après un certain délai sans ACK, PC1 le renvoie ; SRV1 répond ACK 22.
- **Fenêtre** (*window size*) : acquitter chaque segment est inefficace ; la fenêtre permet d'envoyer plusieurs segments avant un ACK (seq 20, 21, 22 puis ACK 23). **Fenêtre glissante** (*sliding window*) : la taille augmente jusqu'à ce qu'un segment soit perdu, redescend à un niveau raisonnable, puis réaugmente lentement.
- En réalité, les numéros de séquence sont bien plus grands et n'augmentent pas de 1 à chaque message ; retenir le concept.

### 3. UDP (*User Datagram Protocol*)

- **Sans connexion** (*connectionless*) : les données sont simplement envoyées.
- **Pas de fiabilité** : pas d'acquittement, pas de retransmission, envoi **au mieux** (*best-effort*), aucune garantie de livraison.
- **Pas de séquencement** : pas de champ de séquence.
- **Pas de contrôle de flux**.
- **En-tête UDP : 4 champs** seulement : port source, port destination, longueur (*length*), somme de contrôle (*checksum*).

### 4. Comparaison et choix

- TCP offre plus de fonctions mais avec plus de **surcharge** (*overhead*) : en-tête plus gros, acquittements et retransmissions ralentissent le transfert.
- **TCP** pour les applications qui exigent la fiabilité : téléchargement de fichier (un PDF sans page manquante).
- **UDP** pour la voix et la vidéo en temps réel (VoIP, Zoom, Skype), sensibles au délai.
- Certaines applications utilisent UDP mais assurent la fiabilité elles-mêmes (**TFTP**). Un appel Skype où le son coupe : on demande de répéter, une « retransmission » humaine.
- **DNS** utilise les deux : UDP en général, TCP dans certaines situations.

### 5. Ports bien connus à mémoriser (tag Anki `portnumbers`)

| Protocole | Transport | Port |
| :--- | :--- | :--- |
| FTP (*File Transfer Protocol*) | TCP | **20, 21** |
| SSH (*Secure Shell*, accès CLI) | TCP | **22** |
| Telnet (accès CLI) | TCP | **23** |
| SMTP (*Simple Mail Transfer Protocol*, envoi d'e-mail) | TCP | **25** |
| HTTP | TCP | **80** |
| POP3 (*Post Office Protocol 3*, récupération d'e-mail) | TCP | **110** |
| HTTPS | TCP | **443** |
| DHCP (*Dynamic Host Configuration Protocol*) | UDP | **67, 68** |
| TFTP (*Trivial File Transfer Protocol*) | UDP | **69** |
| SNMP (*Simple Network Management Protocol*) | UDP | **161, 162** |
| Syslog | UDP | **514** |
| DNS (*Domain Name System*) | **TCP et UDP** | 53 (vu dans la démo Wireshark) |

Révision Anki : *Custom study* → *Study by card state or tag* → *All cards in random order (don't reschedule)* → *Choose tags* → cocher *Require one or more of these tags* avec `portnumbers`.

### 6. Pièges d'examen

- **Adressage de couche 4 (ports) et multiplexage de sessions** sont fournis par **TCP et UDP** ; seuls **error recovery, flow control, sequencing** (et fiabilité) sont propres à TCP.
- Le port **source** est choisi dans la plage **éphémère** ; « reserved » n'est pas une plage IANA.
- **Forward acknowledgment** : un segment seq 27 est acquitté par **ACK 28** (avec une fenêtre de 1). Un ACK 27 ferait renvoyer le segment 27.
- **SYN, SYN-ACK, ACK** : à connaître par cœur.
- Savoir quel protocole applicatif utilise TCP ou UDP, et son port : « you'll definitely need to know some of them for the test ».

### 7. Le lab : démo Wireshark (vidéo n°62)

Pas de lab Packet Tracer ce jour. Wireshark (wireshark.org, gratuit) est un logiciel de **capture de paquets** (*packet capture*) : il capture la trame entière, pas seulement le PDU de couche 3, sur du trafic réel, contrairement au mode simulation de Packet Tracer.

Observations de Jeremy, capture filtrée par port TCP pendant la lecture d'une vidéo YouTube :

- Colonne *Info* : ports **62652 → 443** puis inversés dans la réponse. 62652 = port source éphémère aléatoire ; 443 = HTTPS.
- Les trois premiers messages : **SYN, SYN-ACK, ACK**, le three-way handshake. Les colonnes montrent aussi seq, ack et *window length*.
- Le numéro de séquence affiché « 0 » est un numéro **relatif** ; Wireshark le fait pour faciliter la lecture. Le vrai numéro (ex. 1 224 315 781) apparaît dans le détail du segment. Seq 0 acquitté par 1 : forward acknowledgment.
- L'échange de données affiche **SSL** dans la colonne protocole (SSL sécurise HTTPS, TCP est toujours utilisé dessous).
- À la fin : échange de **FIN** et **ACK**. Les drapeaux réels diffèrent un peu du cours (ACK supplémentaire dans les messages 1 et 3) : retenir simplement FIN, ACK, FIN, ACK.
- Détail d'un SYN : encapsulé dans une trame Ethernet et un paquet IP ; sous *Flags*, seul le bit **SYN = 1** ; la *window size* est visible.
- Segment **UDP** : requête **DNS** du PC vers un serveur DNS, port source éphémère, **port de destination 53**, message DNS (*query*) encapsulé dedans.

Devoir facultatif : installer Wireshark, capturer le trafic du PC en visitant des sites, arrêter la capture, retrouver un **three-way handshake** et un **four-way handshake**.

### 8. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Lequel est un port well-known selon l'IANA : 1010, 2001, 4023, 65000 ? | **1010** | Well-known = 0 à 1023 ; 2001 et 4023 sont dans la plage registered ; 65000 dans la plage éphémère. |
| Dans quelle plage un hôte choisit-il son port source aléatoire ? | **Ephemeral** | Le port de destination dépend du protocole applicatif ; « reserved » n'est pas une plage IANA. |
| Fonctions de TCP mais pas d'UDP (trois réponses) ? | **Error recovery, flow control, sequencing** | L'adressage de couche 4 et le multiplexage de sessions sont communs aux deux. |
| Protocoles applicatifs utilisant TCP (trois réponses) : SMTP, SNMP, HTTPS, DHCP, Syslog, SSH ? | **SMTP, HTTPS, SSH** | SNMP, DHCP et Syslog utilisent UDP. |
| SRV1 reçoit un segment seq 27 (fenêtre 1) : valeur du champ Acknowledgment ? | **28** | Forward acknowledgment : on indique le prochain segment attendu. ACK 27 ferait croire que le segment 27 n'est pas arrivé. |

Bonus Boson (glisser-déposer) : DNS → TCP et UDP ; DHCP → UDP ; FTP → TCP ; HTTP → TCP ; SMTP → TCP ; SNMP → UDP ; TFTP → UDP.

---

## 🇬🇧 English version

### 1. Layer 4 functions

- Exam topic 1.5: **compare TCP to UDP**. A high-level understanding is enough, not the detailed mechanics.
- **Transparent transfer of data between end hosts**: the Transport Layer encapsulates data with a Layer 4 header and uses Layers 3, 2 and 1 to deliver it unchanged; the hosts are not aware of the underlying network.
- **Services to applications** (provided by TCP, not UDP): reliable data transfer, error recovery, data sequencing, flow control.
- **Layer 4 addressing: port numbers**. Not the physical ports of a switch. Two functions:
  - **Identify the Application Layer protocol**: the **destination port** (TCP 80 = HTTP for web pages, TCP 21 = FTP for file transfer).
  - **Session multiplexing**: a session is an exchange of data between two or more communicating devices. The **source port is randomly selected** by the host; combined with the destination port it identifies the session. In the server's reply, source and destination ports are **reversed** (80 → 50000). Two connections to the same server use different source ports.
- **IANA (Internet Assigned Numbers Authority) ranges**:
  - **Well-known**: **0 to 1023**, major protocols, very strictly regulated.
  - **Registered**: **1024 to 49151**, registration required but less strict.
  - **Ephemeral** (private, dynamic): **49152 to 65535**, used by hosts for the **random source port**.
- Port numbers are a function of **both** TCP and UDP.

### 2. TCP (Transmission Control Protocol)

- **Connection-oriented**: the hosts establish a connection before sending data.
- **Reliable communication**: the destination must **acknowledge** each segment (segment = Layer 4 PDU); an unacknowledged segment is sent again.
- **Sequencing**: the sequence number field lets the destination put segments in the correct order.
- **Flow control**: the destination can tell the source to increase or decrease the sending rate.
- **TCP header**, fields to know: **source and destination ports (16 bits each, so 65536 = 2^16 port numbers)**, **sequence number** and **acknowledgment number**, the **ACK, SYN, FIN** flags (connection establishment and termination), **window size** (flow control). No need to memorize the whole header.
- **Three-way handshake** (establishment): PC1 → **SYN**; SRV1 → **SYN-ACK**; PC1 → **ACK**. Must remember.
- **Four-way handshake** (termination): PC1 → **FIN**; SRV1 → **ACK**; SRV1 → **FIN**; PC1 → **ACK**.
- **Sequence and acknowledgment**: each host sets a **random initial sequence number** (e.g. PC1 = 10, PC2 = 50). **Forward acknowledgment**: the ACK field states the **sequence number of the next segment expected** (segment 10 is acknowledged with ACK 11). Example: SYN seq 10; SYN-ACK seq 50, ack 11; ACK seq 11, ack 51; then seq 51, ack 12.
- **Retransmission**: PC1 sends seq 21, it does not arrive; after a certain time with no ACK, PC1 resends it; SRV1 replies ACK 22.
- **Window size**: acknowledging every segment is inefficient; the window lets more data be sent before an ACK is required (seq 20, 21, 22 then ACK 23). **Sliding window**: the size is increased until a segment is dropped, backs down to a reasonable level, then slowly increases again.
- Real sequence numbers are much larger and do not increase by 1 per message; understand the concept.

### 3. UDP (User Datagram Protocol)

- **Connectionless**: data is simply sent.
- **Not reliable**: no acknowledgments, no retransmission, segments are sent **best-effort**, no delivery guarantee.
- **No sequencing**: no sequence field.
- **No flow control**.
- **UDP header: only 4 fields**: source port, destination port, length, checksum.

### 4. Comparison and use cases

- TCP provides more features but at the cost of **overhead**: larger header, acknowledgments and retransmissions slow down the transfer.
- **TCP** for applications requiring reliability: downloading a file (a PDF with no missing page).
- **UDP** for real-time voice and video (VoIP, Zoom, Skype), which are delay-sensitive.
- Some applications use UDP but provide reliability inside the application (**TFTP**). A Skype call where audio cuts out: you ask the other person to repeat, a human "retransmission".
- **DNS** uses both: usually UDP, TCP in some situations.

### 5. Well-known port numbers to memorize (Anki tag `portnumbers`)

| Protocol | Transport | Port |
| :--- | :--- | :--- |
| FTP (File Transfer Protocol) | TCP | **20, 21** |
| SSH (Secure Shell, CLI access) | TCP | **22** |
| Telnet (CLI access) | TCP | **23** |
| SMTP (Simple Mail Transfer Protocol, sending email) | TCP | **25** |
| HTTP | TCP | **80** |
| POP3 (Post Office Protocol 3, retrieving email) | TCP | **110** |
| HTTPS | TCP | **443** |
| DHCP (Dynamic Host Configuration Protocol) | UDP | **67, 68** |
| TFTP (Trivial File Transfer Protocol) | UDP | **69** |
| SNMP (Simple Network Management Protocol) | UDP | **161, 162** |
| Syslog | UDP | **514** |
| DNS (Domain Name System) | **TCP and UDP** | 53 (seen in the Wireshark demo) |

Anki review: *Custom study* → *Study by card state or tag* → *All cards in random order (don't reschedule)* → *Choose tags* → check *Require one or more of these tags* with `portnumbers`.

### 6. Exam traps

- **Layer 4 addressing (ports) and session multiplexing** are provided by **both TCP and UDP**; only **error recovery, flow control, sequencing** (and reliability) are TCP-only.
- The **source** port is selected from the **ephemeral** range; "reserved" is not an IANA range.
- **Forward acknowledgment**: a segment with seq 27 is acknowledged with **ACK 28** (window size 1). ACK 27 would cause segment 27 to be resent.
- **SYN, SYN-ACK, ACK**: know it by heart.
- Know which Application Layer protocols use TCP or UDP and their port numbers: "you'll definitely need to know some of them for the test".

### 7. The lab: Wireshark demo (video 62)

No Packet Tracer lab today. Wireshark (wireshark.org, free) is **packet capture** software: it captures the entire frame, not only the Layer 3 PDU, on real traffic, unlike Packet Tracer's simulation mode.

Jeremy's observations, capture filtered by TCP port while watching a YouTube video:

- *Info* column: ports **62652 → 443**, reversed in the reply. 62652 = random ephemeral source port; 443 = HTTPS.
- First three messages: **SYN, SYN-ACK, ACK**, the three-way handshake. The columns also show seq, ack and *window length*.
- The displayed sequence number "0" is a **relative** number; Wireshark does this to make analysis easier. The real number (e.g. 1,224,315,781) appears in the segment details. Seq 0 acknowledged with 1: forward acknowledgment.
- The data exchange shows **SSL** in the protocol column (SSL gives HTTPS its security, TCP is still used underneath).
- At the end: exchange of **FINs** and **ACKs**. The real flags differ slightly from the lecture (extra ACK in messages 1 and 3): just remember FIN, ACK, FIN, ACK.
- Inside a SYN: encapsulated in an Ethernet frame and IP packet; under *Flags*, only the **SYN bit = 1**; the *window size* is visible.
- **UDP** segment: a **DNS** query from the PC to a DNS server, ephemeral source port, **destination port 53**, a DNS query message encapsulated inside.

Optional homework: install Wireshark, capture your PC's traffic while visiting websites, stop the capture, find a **three-way handshake** and a **four-way handshake**.

### 8. The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which is a well-known port number per IANA: 1010, 2001, 4023, 65000? | **1010** | Well-known = 0 to 1023; 2001 and 4023 are registered; 65000 is ephemeral. |
| From which range should hosts randomly select a source port? | **Ephemeral** | The destination port depends on the Application Layer protocol; "reserved" is not an IANA range. |
| Features of TCP but not UDP (select three)? | **Error recovery, flow control, sequencing** | Layer 4 addressing and session multiplexing are features of both. |
| Application Layer protocols using TCP (select three): SMTP, SNMP, HTTPS, DHCP, Syslog, SSH? | **SMTP, HTTPS, SSH** | SNMP, DHCP and Syslog use UDP. |
| SRV1 receives a segment with seq 27 (window size 1): value of the Acknowledgment field? | **28** | Forward acknowledgment: state the next expected segment. ACK 27 would make PC1 assume segment 27 was not received. |

Boson bonus (drag and drop): DNS → TCP and UDP; DHCP → UDP; FTP → TCP; HTTP → TCP; SMTP → TCP; SNMP → UDP; TFTP → UDP.
