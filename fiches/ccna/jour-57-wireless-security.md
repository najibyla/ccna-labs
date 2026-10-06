# CCNA Day 57 : Wireless Security / Sécurité des réseaux sans fil

> Source : Jeremy's IT Lab, « Free CCNA | Wireless Security | Day 57 » (34 min), vidéo n°115 de la playlist. Pas de lab pour ce jour. Fiche rédigée à partir de la transcription le 6 octobre 2026. Sujets d'examen : 1.11.d (encryption), 5.9 (WPA, WPA2, WPA3).

## 🇫🇷 Version française

### 1. Pourquoi la sécurité est plus critique en sans-fil

Tout appareil à portée du signal reçoit le trafic. En filaire on chiffre en général seulement sur les réseaux non fiables (Internet) ; en sans-fil il faut **chiffrer le trafic entre clients et AP**. Trois concepts : **authentification**, **chiffrement**, **intégrité**.

- **Authentification** : vérifier l'identité d'un utilisateur et/ou d'un appareil. Tout client doit être authentifié **avant** de s'associer à l'AP. En entreprise, seuls les utilisateurs et appareils de confiance accèdent au réseau ; un **SSID invité** séparé, moins strict, donne seulement accès à Internet. Idéalement le **client authentifie aussi l'AP** pour éviter un AP malveillant (attaque *man-in-the-middle*). Moyens : mot de passe, nom d'utilisateur + mot de passe, certificats numériques.
- **Chiffrement** (*encryption*) : brouiller le message pour que seuls l'émetteur et le destinataire puissent le lire. Émetteur et récepteur doivent utiliser le **même protocole**. Tous les appareils du WLAN utilisent le même protocole, mais **chaque client a une clé unique** ; seul l'AP peut déchiffrer son trafic. Une **clé de groupe** (*group key*) sert à l'AP pour chiffrer le trafic destiné à tous ses clients, qui en gardent une copie.
- **Intégrité** : le message n'est pas modifié en transit. Un **MIC** (*Message Integrity Check*) est ajouté : l'émetteur calcule le MIC, l'attache au message, chiffre le tout et l'envoie ; le récepteur déchiffre, recalcule le MIC avec le même protocole et compare. **Si les deux MIC diffèrent, le message est rejeté.** Le MIC sert donc à **détecter** une atteinte à l'intégrité.

### 2. Les méthodes d'authentification (7)

**Les deux méthodes de la norme 802.11 d'origine**

- **Open authentication** : le client envoie une requête d'authentification, l'AP **accepte sans condition**. Pas sécurisé seul, mais encore utilisé en combinaison avec d'autres méthodes (Wi-Fi public : association libre, puis authentification via une page web avant l'accès à Internet).
- **WEP** (*Wired Equivalent Privacy*) : authentification **et** chiffrement. Chiffrement par l'algorithme **RC4**. Protocole à **clé partagée** (*shared key*) : clés de **40 bits ou 104 bits**, combinées à un **vecteur d'initialisation de 24 bits** pour un total de **64 ou 128 bits**. **WEP n'est pas sécurisé et se casse facilement, quelle que soit la longueur de clé.** Authentification WEP : l'AP envoie une **challenge phrase**, le client la chiffre avec la clé WEP et la renvoie, l'AP compare avec sa propre version chiffrée. WEP peut servir au chiffrement seul (avec open authentication) ou aux deux.

**EAP** (*Extensible Authentication Protocol*) : pas un protocole unique mais un **cadre** (*framework*) définissant des fonctions d'authentification standard, utilisé par des **méthodes EAP**. EAP est intégré à **802.1X**, contrôle d'accès réseau **par port** : limite l'accès des clients (LAN filaire ou sans fil) jusqu'à leur authentification. Trois entités :

- **Supplicant** : l'appareil qui veut se connecter (le portable).
- **Authenticator** : l'appareil qui donne l'accès au réseau (l'AP ; en split-MAC, c'est le **WLC** qui gère l'authentification).
- **Authentication server** : reçoit les identifiants et autorise ou refuse (en général un serveur **RADIUS**).

En WLAN : l'authentification 802.11 nécessaire pour s'associer est **open**, puis seul le trafic EAP est autorisé jusqu'à ce que le serveur d'authentification accorde l'accès.

**Quatre méthodes EAP**

- **LEAP** (*Lightweight EAP*, Cisco) : amélioration de WEP. Nom d'utilisateur + mot de passe, **authentification mutuelle** (client et serveur s'envoient chacun une challenge phrase), **clés WEP dynamiques** qui changent avec le temps. **Vulnérable, à ne plus utiliser.**
- **EAP-FAST** (*EAP Flexible Authentication via Secure Tunneling*, Cisco), trois phases : 1) un **PAC** (*Protected Access Credential*) est généré et transmis du serveur au client (comme une clé partagée) ; 2) le PAC sert à établir un **tunnel TLS sécurisé** client ↔ serveur d'authentification ; 3) le client est **authentifié dans le tunnel**.
- **PEAP** (*Protected EAP*) : tunnel TLS aussi, mais le serveur présente un **certificat numérique** (au lieu d'un PAC) que le client utilise pour authentifier le serveur et établir le tunnel. Seul le serveur a un certificat, donc le client est **encore authentifié dans le tunnel**, par exemple avec **MS-CHAP** (*Microsoft Challenge Handshake Authentication Protocol*).
- **EAP-TLS** (*EAP Transport Layer Security*) : certificat sur le **serveur ET sur chaque client**. **La plus sécurisée**, mais plus difficile à déployer (un certificat par client). Pas d'authentification du client dans le tunnel ; le tunnel TLS sert à échanger les informations de clés de chiffrement. Beaucoup d'entreprises préfèrent PEAP.

### 3. Les méthodes de chiffrement et d'intégrité

- **TKIP** (*Temporal Key Integrity Protocol*) : solution **temporaire basée sur WEP** (le matériel de l'époque était conçu pour WEP) avec des ajouts : **MIC**, **algorithme de mixage de clés** (clé WEP unique par trame), **vecteur d'initialisation doublé de 24 à 48 bits**, MIC incluant l'**adresse MAC de l'émetteur**, **horodatage** contre les attaques par rejeu (*replay*), **numéro de séquence TKIP**. Utilisé dans **WPA**.
- **CCMP** (*Counter/CBC-MAC Protocol*) : plus récent et plus sûr que TKIP, **doit être pris en charge par le matériel**. Deux algorithmes : chiffrement **AES counter mode** (AES = protocole le plus sûr actuellement, mode compteur pour la performance) et **CBC-MAC** (*Cipher Block Chaining Message Authentication Code*) comme MIC. Utilisé dans **WPA2**.
- **GCMP** (*Galois/Counter Mode Protocol*) : plus sûr et plus **efficace** que CCMP (débit plus élevé). Chiffrement **AES counter mode** et **GMAC** (*Galois Message Authentication Code*) comme MIC. Utilisé dans **WPA3**.

### 4. WPA, WPA2, WPA3 (certifications de la Wi-Fi Alliance)

Le premier s'appelle **WPA**, pas WPA1. Les appareils sont testés en laboratoires agréés. Les trois prennent en charge deux modes :

- **Mode personnel** : **PSK** (*pre-shared key*), le mot de passe du Wi-Fi domestique ; réseaux SOHO. La PSK n'est **pas envoyée dans les airs** : un **four-way handshake** sert à l'authentification et la PSK génère les clés de chiffrement.
- **Mode entreprise** : **802.1X avec serveur d'authentification** ; toutes les méthodes EAP sont possibles (PEAP, EAP-TLS…), WPA n'en impose aucune.

| Certification | Chiffrement et intégrité | Authentification | Remarques |
| :--- | :--- | :--- | :--- |
| **WPA** | **TKIP** | 802.1X/EAP ou PSK | Créé après la découverte des failles de WEP ; n'a pas duré |
| **WPA2** | **CCMP** | 802.1X/EAP ou PSK | Matériel plus récent |
| **WPA3** (2018) | **GCMP** | 802.1X/EAP ou PSK | **PMF** (*Protected Management Frames*, optionnel en WPA2, obligatoire en WPA3), **SAE** (*Simultaneous Authentication of Equals*, protège le four-way handshake en mode personnel), **forward secrecy** (empêche le déchiffrement ultérieur de trames capturées) |

### 5. Pièges d'examen

- **Supplicant / authenticator / authentication server** : à connaître absolument, 802.1X sert en filaire comme en sans-fil.
- Ne pas confondre **PEAP** (certificat serveur seulement) et **EAP-TLS** (certificat des deux côtés, le plus sûr). **EAP-FAST** utilise un **PAC**, PEAP un certificat.
- Ordre de développement et de sécurité : **WEP < TKIP < CCMP < GCMP**.
- **WPA = TKIP, WPA2 = CCMP, WPA3 = GCMP.**
- GMAC et CBC-MAC sont des **MIC** (intégrité), pas des chiffrements.

### 6. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Que fournit GMAC à une connexion sans fil sécurisée ? | **MIC** (message integrity check) | GMAC fait partie de GCMP (WPA3) et vérifie l'intégrité des messages. |
| Composants de l'architecture d'authentification 802.1X ? (trois réponses) | **Supplicant**, **authenticator**, **authentication server** | En 802.11 : le client est le supplicant, l'AP ou le WLC l'authenticator, un serveur RADIUS le serveur d'authentification. |
| Méthode de chiffrement/intégrité la plus sûre ? | **GCMP** | Ordre : WEP, TKIP, CCMP, GCMP ; GCMP est recommandé si le matériel le prend en charge. |
| Quelle méthode exige un certificat sur le supplicant ET sur l'AS ? | **EAP-TLS** | PEAP n'exige un certificat que sur l'AS ; EAP-TLS authentifie les deux côtés par certificat. |
| Quelle fonctionnalité WPA3 protège le four-way handshake en mode personnel ? | **SAE** | Simultaneous Authentication of Equals rend le four-way handshake plus sûr. |

---

## 🇬🇧 English version

### 1. Why security matters more in wireless

Any device within range of the signal receives the traffic. Wired networks usually encrypt only over untrusted networks (the Internet); wireless must **encrypt traffic between clients and the AP**. Three concepts: **authentication**, **encryption**, **integrity**.

- **Authentication**: verifying the identity of a user and/or device. All clients must authenticate **before** associating with the AP. In a corporate setting only trusted users and devices get access; a separate, less strict **guest SSID** gives Internet access only. Ideally **clients also authenticate the AP** to avoid a malicious AP (man-in-the-middle). Means: password, username + password, digital certificates.
- **Encryption**: scrambling the message so only sender and recipient can read it. Both must use the **same protocol**. All devices on the WLAN use the same protocol, but **each client has a unique key**; only the AP can decrypt its traffic. A **group key** is used by the AP to encrypt traffic sent to all its clients, who keep a copy.
- **Integrity**: the message is not modified in transit. A **MIC** (Message Integrity Check) is added: the sender calculates the MIC, attaches it, encrypts message and MIC, sends the frame; the recipient decrypts, independently calculates a MIC with the same protocol and compares. **If the two MICs differ, the message is discarded.** The MIC thus **identifies** whether integrity was compromised.

### 2. Authentication methods (7)

**The two methods in the original 802.11 standard**

- **Open authentication**: the client sends an authentication request, the AP **accepts it, no questions asked**. Not secure on its own, but still used combined with other methods (public Wi-Fi: free association, then web-page login before Internet access).
- **WEP** (Wired Equivalent Privacy): authentication **and** encryption. Encryption uses the **RC4** algorithm. **Shared-key** protocol: keys of **40 bits or 104 bits**, combined with a **24-bit initialization vector** for a total of **64 or 128 bits**. **WEP is NOT secure and is easily cracked regardless of key length.** WEP authentication: the AP sends a **challenge phrase**, the client encrypts it with the WEP key and sends it back, the AP compares with its own encrypted version. WEP can provide encryption only (with open authentication) or both.

**EAP** (Extensible Authentication Protocol): not a single protocol but a **framework** defining standard authentication functions used by **EAP methods**. EAP is integrated with **802.1X**, **port-based** network access control: limits access for clients (wired LAN or WLAN) until they authenticate. Three entities:

- **Supplicant**: the device that wants to connect (the laptop).
- **Authenticator**: the device that provides access to the network (the AP; in split-MAC it is the **WLC** that manages authentication).
- **Authentication server**: receives credentials and permits or denies (usually a **RADIUS** server).

In a WLAN: the 802.11 authentication needed to associate is **open**, then only EAP traffic is allowed until the authentication server grants access.

**Four EAP methods**

- **LEAP** (Lightweight EAP, Cisco): improvement over WEP. Username + password, **mutual authentication** (client and server each send a challenge phrase), **dynamic WEP keys** that change over time. **Vulnerable, should not be used.**
- **EAP-FAST** (EAP Flexible Authentication via Secure Tunneling, Cisco), three phases: 1) a **PAC** (Protected Access Credential) is generated and passed from server to client (like a shared key); 2) the PAC establishes a **secure TLS tunnel** between client and authentication server; 3) the client is **authenticated within the tunnel**.
- **PEAP** (Protected EAP): also a TLS tunnel, but the server has a **digital certificate** (instead of a PAC) that the client uses to authenticate the server and build the tunnel. Only the server has a certificate, so the client is **still authenticated inside the tunnel**, for example with **MS-CHAP** (Microsoft Challenge Handshake Authentication Protocol).
- **EAP-TLS** (EAP Transport Layer Security): certificate on the **server AND on every client**. **Most secure**, but harder to implement (a certificate per client). No client authentication inside the tunnel; the TLS tunnel is still used to exchange encryption key information. Many enterprises prefer PEAP.

### 3. Encryption and integrity methods

- **TKIP** (Temporal Key Integrity Protocol): a **temporary solution based on WEP** (hardware of the time was built for WEP) with added features: **MIC**, **key mixing algorithm** (unique WEP key per frame), **initialization vector doubled from 24 to 48 bits**, MIC includes the **sender MAC address**, **timestamp** against replay attacks, **TKIP sequence number**. Used in **WPA**.
- **CCMP** (Counter/CBC-MAC Protocol): newer and more secure than TKIP, **must be supported by hardware**. Two algorithms: **AES counter mode** encryption (AES = most secure encryption protocol available, counter mode for performance) and **CBC-MAC** (Cipher Block Chaining Message Authentication Code) as the MIC. Used in **WPA2**.
- **GCMP** (Galois/Counter Mode Protocol): more secure and more **efficient** than CCMP (higher throughput). **AES counter mode** encryption and **GMAC** (Galois Message Authentication Code) as the MIC. Used in **WPA3**.

### 4. WPA, WPA2, WPA3 (Wi-Fi Alliance certifications)

The first is called **WPA**, not WPA1. Devices are tested in authorized labs. All three support two modes:

- **Personal mode**: **PSK** (pre-shared key), the home Wi-Fi password; SOHO networks. The PSK is **not sent over the air**: a **four-way handshake** performs authentication and the PSK generates the encryption keys.
- **Enterprise mode**: **802.1X with an authentication server**; all EAP methods are supported (PEAP, EAP-TLS...), WPA does not specify one.

| Certification | Encryption and integrity | Authentication | Notes |
| :--- | :--- | :--- | :--- |
| **WPA** | **TKIP** | 802.1X/EAP or PSK | Developed after WEP was proven vulnerable; did not last long |
| **WPA2** | **CCMP** | 802.1X/EAP or PSK | Newer hardware |
| **WPA3** (2018) | **GCMP** | 802.1X/EAP or PSK | **PMF** (Protected Management Frames, optional in WPA2, mandatory in WPA3), **SAE** (Simultaneous Authentication of Equals, protects the four-way handshake in personal mode), **forward secrecy** (prevents decryption of captured frames later) |

### 5. Exam traps

- **Supplicant / authenticator / authentication server**: must know; 802.1X is used in wired and wireless networks.
- Do not mix up **PEAP** (server certificate only) and **EAP-TLS** (certificates on both sides, most secure). **EAP-FAST** uses a **PAC**, PEAP a certificate.
- Development and security order: **WEP < TKIP < CCMP < GCMP**.
- **WPA = TKIP, WPA2 = CCMP, WPA3 = GCMP.**
- GMAC and CBC-MAC are **MICs** (integrity), not encryption.

### 6. Quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| What does GMAC provide to a secure wireless connection? | **MIC** (message integrity check) | GMAC is part of GCMP (WPA3) and verifies message integrity. |
| Parts of the 802.1X authentication architecture? (select three) | **Supplicant**, **authenticator**, **authentication server** | In 802.11: the client is the supplicant, the AP or WLC the authenticator, a RADIUS server the authentication server. |
| Most secure encryption and integrity method? | **GCMP** | Order: WEP, TKIP, CCMP, GCMP; use GCMP whenever hardware supports it. |
| Which method requires a certificate on both the supplicant and the AS? | **EAP-TLS** | PEAP only requires a certificate on the AS; EAP-TLS authenticates both sides with certificates. |
| Which WPA3 feature protects the four-way handshake in personal mode? | **SAE** | Simultaneous Authentication of Equals makes the four-way handshake more secure. |
