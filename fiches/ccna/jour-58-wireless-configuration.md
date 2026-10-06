# CCNA Day 58 : Wireless Configuration / Configuration d'un WLAN

> Source : Jeremy's IT Lab, « Free CCNA | Wireless Configuration | Day 58 » (47 min, cours, vidéo n°116 de la playlist) et « Free CCNA | Wireless LANs | Day 58 Lab » (17 min, lab, vidéo n°117). Fiche rédigée à partir des transcriptions le 6 octobre 2026. Sujets d'examen : 2.7, 2.8, 2.9 et 5.10 (configurer un WLAN en WPA2 PSK **via le GUI**).

## 🇫🇷 Version française

### 1. La topologie du cours (lab physique)

- Premier lab physique du cours : **un switch, un WLC, deux AP**. Packet Tracer offre un WLC et des AP suffisants pour le CCNA.
- Les AP sont alimentés par **PoE** (*Power over Ethernet*) : un seul câble pour les données et l'alimentation. Le WLC a aussi deux ports PoE.
- Le WLC est relié au switch par un **LAG** (*Link Aggregation Group*) = EtherChannel, mais on dit toujours LAG pour un WLC. **Les WLC ne supportent que le LAG statique**, pas PAgP ni LACP → `channel-group 1 mode on` (pas `active` ni `desirable`).
- Trois VLAN : **VLAN 10 Management** (192.168.1.0/24), **VLAN 100 Internal** (10.0.0.0/24), **VLAN 200 Guest** (10.1.0.0/24). Seuls 100 et 200 sont associés à un SSID. Le switch a une SVI **.1** dans chaque VLAN (passerelle), le WLC une adresse **.100** dans chaque VLAN. Les AP reçoivent leur adresse par **DHCP** dans le VLAN de gestion ; le switch est serveur **DHCP et NTP**.
- Split-MAC : les ports du switch vers les AP sont des **ports access** ; seul le WLC est en **trunk**. Trajet : client → tunnel CAPWAP → WLC → VLAN 100 → SW1 (passerelle) ; entre clients Internal et Guest : SW1 route vers VLAN 200 → WLC → tunnel → AP → client.

### 2. Configuration du switch

- VLAN 10, 100, 200 créés et nommés. **F0/6, F0/7, F0/8 en access VLAN 10** (F0/7 et F0/8 vers les AP, F0/6 pour le PC qui accédera au GUI : un GUI ne s'atteint pas par le port console, seulement par le réseau en HTTP/HTTPS).
- F0/1 et F0/2 en LAG statique ; **Port-channel en trunk**, VLAN 10, 100, 200 autorisés.
- Une **SVI par VLAN** (passerelle) ; un **pool DHCP par VLAN** avec `default-router` vers la SVI.
- Pool VLAN 10 : **`option 43 ip 192.168.1.100`** indique aux AP l'adresse du WLC. Pas nécessaire ici (AP et WLC dans le même sous-réseau, les AP envoient des **messages de découverte CAPWAP en broadcast**), mais indispensable si le WLC est ailleurs. **À retenir pour l'examen : DHCP option 43.**
- `ntp master` : le switch devient serveur NTP.

### 3. Configuration initiale du WLC (assistant en CLI, via console)

L'assistant pose des questions ; la valeur entre crochets est la **valeur par défaut** (entrée pour l'accepter ; quand deux options sont proposées, celle en **majuscules** est la valeur par défaut, par exemple `[yes][NO]`).

- Terminer l'**autoinstall** (téléchargement de la config depuis un serveur TFTP) : oui.
- Nom du système **WLC1**, nom d'utilisateur et mot de passe admin.
- **LAG** : yes (défaut NO).
- **Management interface** (interface virtuelle, pas un port physique) : IP **192.168.1.100**, masque /24, passerelle .1, **VLAN ID 10**, serveur DHCP .1.
- **Virtual gateway IP** (communication directe avec les clients, par exemple relais DHCP), **multicast IP** (adresse de **classe D**, transfert vers les AP), **mobility/RF group name** (plusieurs WLC travaillant ensemble) : au-delà du CCNA.
- Premier WLAN obligatoire : SSID **internal** ; **DHCP bridging mode** laissé désactivé (s'il est activé, le WLC devient transparent entre clients et serveur DHCP) ; **allow static IP addresses** : défaut accepté ; pas de serveur **RADIUS** (avertissement : la politique de sécurité par défaut en exige un, on passera en PSK).
- **Code pays** : FR. Le suffixe du modèle d'AP (**-E** Europe, **-A** USA/Canada) indique son **domaine réglementaire** ; s'il ne correspond pas au pays du WLC, **l'AP ne peut pas rejoindre le WLC** (Jeremy, au Japon, avait d'abord mis JP).
- Activer **802.11b, a, g** et **auto-RF** (choix automatique des canaux et de la puissance) ; NTP ; sauvegarde et redémarrage.

### 4. Accès au GUI, ports et interfaces du WLC

- PC sur F0/6 (VLAN 10), navigateur vers **https://192.168.1.100** ; avertissement de certificat non fiable (normal en local), puis connexion avec le compte admin. Le **dashboard** montre les interfaces up/down, les infos système et les AP ayant rejoint le WLC.
- Vocabulaire WLC : **port = port physique**, **interface = interface logique** (comme une SVI).
- **Ports** : **service port** (gestion **hors bande**, *out-of-band*, un seul VLAN donc port access du switch ; aussi pour le démarrage et la récupération), **distribution system ports** (ports réseau standard vers le DS, trafic des clients, en général vers des **ports trunk**, peuvent former un **LAG**), **console port** (RJ45 ou USB), **redundancy port** (relie deux WLC en paire **HA**, *high availability*). Sur un WLC moderne : port USB de transfert de fichiers, port DS multi-gigabit, bouton reset, LED.
- **Interfaces** : **management interface** (Telnet/SSH, HTTP/HTTPS, RADIUS, NTP, Syslog ; les **tunnels CAPWAP** se terminent ici), **redundancy management interface** (gérer le WLC standby d'une paire HA), **virtual interface** (relais DHCP, authentification web des clients), **service port interface** (liée au service port), **dynamic interfaces** (**associent un WLAN à un VLAN**).
- Onglet **Controller > Interfaces > New** : interface **Internal**, VLAN **100**, puis IP, masque, passerelle, serveur DHCP ; idem **Guest**, VLAN **200**.

### 5. Configuration des WLAN (onglet WLANs)

- Le WLAN Internal créé par l'assistant est associé à l'interface **management** et utilise **802.1X** : à corriger. Onglet **General** : profile name, SSID, statut **Enabled**, **interface = Internal**.
- Onglet **Security > Layer 2** : **Layer 2 security = WPA+WPA2** (ce WLC ne supporte pas WPA3, WPA2 suffit pour le CCNA). **Authentication key management** : décocher 802.1X, cocher **PSK** ; clé en **ASCII** ou **HEX** ; une PSK ASCII doit faire **au moins 8 caractères**.
- **Layer 3** : **Web Policy** avec **web authentication** (nom d'utilisateur + mot de passe après obtention d'une IP) ou **web passthrough** (accepter un message, sans identifiants) ; le Layer 2 peut alors être open (Wi-Fi de café). Conditional et splash page web redirect exigent 802.1X en plus. Onglet **AAA servers** inutile en PSK.
- **QoS** : **Platinum** = voix, **Gold** = vidéo, **Silver** = best effort (**défaut**), **Bronze** = background. À connaître pour l'examen.
- **Advanced** : nombre maximal de clients (0 = illimité), activation de FlexConnect, etc.
- Nouveau WLAN Guest : profile name, SSID, **ID** unique (2) ; **Enabled**, interface Guest, PSK.
- Vérification : **Monitor > Clients** liste IP, AP et SSID de chaque client ; **Wireless** liste les AP (IP, modèle, MAC) et permet de changer le **mode de l'AP** (local, FlexConnect, monitor, rogue detector…).

### 6. Gestion et sécurité du WLC

- **Management** : SNMPv1 désactivé, v2/v3 activés, Syslog désactivé, HTTP/HTTPS activés, **Telnet désactivé** (non sécurisé), SSH activé, **management via wireless désactivé** (un client Wi-Fi ne peut pas administrer le WLC ; case à cocher pour l'autoriser).
- **Security > Access Control Lists** : créer une ACL (nom MANAGEMENT_ACL, type IPv4) avec des règles (séquence, source, destination, protocole, DSCP, direction) ; puis **CPU Access Control Lists > Enable CPU ACL**. Une **CPU ACL** limite le trafic **destiné au WLC lui-même** (Telnet/SSH, HTTP/HTTPS, SNMP), pas le trafic qui le traverse.

### 7. Pièges d'examen

- **LAG statique uniquement** : `channel-group 1 mode on`.
- **DHCP option 43** pour indiquer le WLC aux AP.
- **Port ≠ interface** sur un WLC. **Dynamic interface** = WLAN ↔ VLAN. **Redundancy port** = paire HA. **Distribution system ports** = trafic de données, LAG.
- **QoS : Platinum voix, Gold vidéo, Silver défaut, Bronze background.**
- **Web authentication** = authentification de **couche 3**.
- Savoir **dans quel onglet** on crée les interfaces (Controller) et les WLAN (WLANs) : Cisco peut tester la familiarité avec le GUI.

### 8. Commandes IOS (switch)

```
SW1(config)# vlan 10                                   ! créer les VLAN 10, 100, 200 et les nommer
SW1(config-if)# switchport mode access                 ! F0/6-8 en access VLAN 10 (AP et PC d'administration)
SW1(config-if)# switchport access vlan 10
SW1(config-if)# channel-group 1 mode on                ! F0/1-2 : LAG statique vers le WLC (pas active/desirable)
SW1(config-if)# switchport mode trunk                  ! sur Port-channel 1
SW1(config-if)# switchport trunk allowed vlan 10,100,200
SW1(config)# interface vlan 100                        ! une SVI par VLAN, adresse .1 = passerelle
SW1(dhcp-config)# default-router 192.168.1.1           ! passerelle du pool DHCP
SW1(dhcp-config)# option 43 ip 192.168.1.100           ! pool VLAN 10 : adresse du WLC pour les AP
SW1(config)# ntp master                                ! le switch devient serveur NTP
SW1# show run                                          ! vérifier l'ensemble (lab)
```

### 9. Le lab (Packet Tracer, WLC 3504)

- **Pré-configuré** : le switch et la configuration initiale du WLC (le port console du WLC n'est pas accessible dans Packet Tracer ; pour refaire la configuration initiale, supprimer le WLC et en ajouter un nouveau).
- `show run` sur SW1 : **adresses exclues** du DHCP (bonne pratique pour réserver des IP statiques), pools VLAN 10 (AP et PC1, avec option 43 non nécessaire ici), VLAN 100 et 200 ; **VLAN 10 natif** sur G1/0/1 vers le WLC car le WLC n'étiquette pas le VLAN de gestion (**le tagging doit être identique des deux côtés**) ; G1/0/2-4 access VLAN 10 ; SVI par VLAN ; les commandes `mac-address` ont été ajoutées automatiquement par Packet Tracer.
- Depuis PC1, Desktop > Web Browser : **https://172.16.1.10** (ce modèle n'accepte pas HTTP), compte **admin / Cisco123**. Le dashboard montre le port 1 et les deux AP joints, 0 client.
- Étape 2 : explorer le GUI. **Monitor > Statistics > AP Join** montre les AP joints, les messages échangés et la « reason for last unsuccessful attempt » : utile pour dépanner un AP qui ne joint pas.
- Étape 3 : **Controller > Interfaces > New** : **Internal**, VLAN 100, **port 1**, IP **10.0.0.10**/24, passerelle **10.0.0.1**, DHCP 10.0.0.1 ; **Guest**, VLAN 200, port 1, IP **10.1.0.10**, masque 255.255.255.0, passerelle **10.1.0.1**, DHCP 10.1.0.1.
- Étape 4 : **WLANs > Create New > Go** : type WLAN, profile name et SSID **Internal**, ID 1. General : **Enabled**, interface Internal. Security : **WPA+WPA2**, **WPA2 policy**, **AES**, pas 802.1X, **PSK = Cisco123**. QoS non modifiable dans Packet Tracer ; Advanced : max clients **100**. Idem pour **Guest** (ne pas oublier **Enabled**, erreur facile).
- Étape 5 : ajouter un **smartphone**, Config > Wireless0 : SSID **Internal**, authentification **WPA2-PSK**, passphrase Cisco123, IP en DHCP. Il s'associe et reçoit une IP… **du pool VLAN 10** au lieu du VLAN 100 : **défaut de Packet Tracer**, pas de la configuration (vérifié sur matériel réel).

### 10. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quel port du WLC forme une paire HA avec un autre WLC ? | **Redundancy port** | Il relie deux WLC, l'un actif et l'autre standby prêt à prendre le relais. |
| Quel type d'interface du WLC associe un WLAN à un VLAN ? | **Dynamic interface** | Les interfaces Internal et Guest associent les WLAN aux VLAN 100 et 200. |
| Quel est un type d'authentification de couche 3 ? | **Web authentication** | Configurée sous l'onglet Layer 3 : nom d'utilisateur et mot de passe avant l'accès à Internet. |
| Quel réglage QoS du WLC pour le trafic vidéo ? | **Gold** | Silver (best effort) est le défaut ; Gold est recommandé pour la vidéo. |
| Quel type de port du WLC peut former un LAG pour le trafic de données standard ? | **Distribution system port** | Ports réseau standard pour le trafic de et vers les clients sans fil. |

---

## 🇬🇧 English version

### 1. Lecture topology (physical lab)

- First physical lab of the course: **one switch, one WLC, two APs**. Packet Tracer's WLC and APs are enough for the CCNA.
- APs are powered by **PoE** (Power over Ethernet): one cable for data and power. The WLC also has two PoE ports.
- The WLC connects to the switch via a **LAG** (Link Aggregation Group) = EtherChannel, but always called LAG for a WLC. **WLCs only support static LAG**, no PAgP or LACP → `channel-group 1 mode on` (not `active` or `desirable`).
- Three VLANs: **VLAN 10 Management** (192.168.1.0/24), **VLAN 100 Internal** (10.0.0.0/24), **VLAN 200 Guest** (10.1.0.0/24). Only 100 and 200 are mapped to SSIDs. The switch has a **.1** SVI in each VLAN (gateway), the WLC a **.100** address in each VLAN. APs get their address via **DHCP** in the management VLAN; the switch is the **DHCP and NTP** server.
- Split-MAC: switch ports to the APs are **access ports**; only the WLC is on a **trunk**. Path: client → CAPWAP tunnel → WLC → VLAN 100 → SW1 (gateway); between Internal and Guest clients: SW1 routes to VLAN 200 → WLC → tunnel → AP → client.

### 2. Switch configuration

- VLANs 10, 100, 200 created and named. **F0/6, F0/7, F0/8 as access ports in VLAN 10** (F0/7 and F0/8 to the APs, F0/6 for the PC that will access the GUI: a GUI cannot be reached via the console port, only over the network with HTTP/HTTPS).
- F0/1 and F0/2 as a static LAG; **Port-channel as a trunk** allowing VLANs 10, 100, 200.
- One **SVI per VLAN** (gateway); one **DHCP pool per VLAN** with `default-router` set to the SVI.
- VLAN 10 pool: **`option 43 ip 192.168.1.100`** tells the APs the WLC's address. Not necessary here (APs and WLC in the same subnet, APs send **broadcast CAPWAP discovery messages**), but required if the WLC cannot hear the broadcasts. **Remember for the exam: DHCP option 43.**
- `ntp master`: the switch becomes an NTP server.

### 3. WLC initial setup (CLI wizard, via console)

The wizard asks questions; the value in square brackets is the **default** (press Enter to accept; with two options, the one in **upper case** is the default, e.g. `[yes][NO]`).

- Terminate **autoinstall** (download the config from a TFTP server): yes.
- System name **WLC1**, admin username and password.
- **LAG**: yes (default NO).
- **Management interface** (virtual interface, not a physical port): IP **192.168.1.100**, /24 netmask, gateway .1, **VLAN ID 10**, DHCP server .1.
- **Virtual gateway IP** (direct communication with clients, e.g. relaying DHCP), **multicast IP** (**class D** address, forwarding to APs), **mobility/RF group name** (multiple WLCs working together): beyond the CCNA.
- One mandatory WLAN: SSID **internal**; **DHCP bridging mode** left disabled (if enabled, the WLC becomes transparent between clients and the DHCP server); **allow static IP addresses**: default accepted; no **RADIUS** server (warning: the default WLAN security policy requires one; we will switch to PSK).
- **Country code**: FR. The AP model suffix (**-E** Europe, **-A** US/Canada) indicates its **regulatory domain**; if it does not match the WLC's country, **the AP cannot join the WLC** (Jeremy, in Japan, first entered JP).
- Enable **802.11b, a, g** and **auto-RF** (automatic channel and transmit power selection); NTP; save and reset.

### 4. GUI access, WLC ports and interfaces

- PC on F0/6 (VLAN 10), browser to **https://192.168.1.100**; untrusted certificate warning (normal on a local network), then log in with the admin account. The **dashboard** shows up/down interfaces, system info and joined APs.
- WLC vocabulary: **port = physical port**, **interface = logical interface** (like an SVI).
- **Ports**: **service port** (**out-of-band** management, one VLAN only so a switch access port; also for boot-up and system recovery), **distribution system ports** (standard network ports to the DS, client data traffic, usually to **trunk ports**, can form a **LAG**), **console port** (RJ45 or USB), **redundancy port** (connects two WLCs as an **HA** pair, high availability). On a modern WLC: USB port for file transfer, multi-gigabit DS port, reset button, status LEDs.
- **Interfaces**: **management interface** (Telnet/SSH, HTTP/HTTPS, RADIUS, NTP, Syslog; **CAPWAP tunnels** terminate here), **redundancy management interface** (manage the standby WLC of an HA pair), **virtual interface** (DHCP relay, client web authentication), **service port interface** (bound to the service port), **dynamic interfaces** (**map a WLAN to a VLAN**).
- **Controller > Interfaces > New**: interface **Internal**, VLAN **100**, then IP, netmask, gateway, DHCP server; same for **Guest**, VLAN **200**.

### 5. WLAN configuration (WLANs tab)

- The Internal WLAN created by the wizard is mapped to the **management** interface and uses **802.1X**: must be fixed. **General** tab: profile name, SSID, status **Enabled**, **interface = Internal**.
- **Security > Layer 2**: **Layer 2 security = WPA+WPA2** (this WLC does not support WPA3; WPA2 is what the CCNA requires). **Authentication key management**: uncheck 802.1X, check **PSK**; key in **ASCII** or **HEX**; an ASCII PSK must be **at least 8 characters**.
- **Layer 3**: **Web Policy** with **web authentication** (username + password after getting an IP) or **web passthrough** (accept a statement, no credentials); Layer 2 can then be open (cafe Wi-Fi). Conditional and splash page web redirect additionally require 802.1X. **AAA servers** tab not needed with PSK.
- **QoS**: **Platinum** = voice, **Gold** = video, **Silver** = best effort (**default**), **Bronze** = background. Know these for the exam.
- **Advanced**: maximum clients (0 = no maximum), FlexConnect enablement, etc.
- New Guest WLAN: profile name, SSID, unique **ID** (2); **Enabled**, Guest interface, PSK.
- Verification: **Monitor > Clients** lists each client's IP, AP and SSID; **Wireless** lists APs (IP, model, MAC) and lets you change the **AP mode** (local, FlexConnect, monitor, rogue detector...).

### 6. WLC management and security

- **Management**: SNMPv1 disabled, v2/v3 enabled, Syslog disabled, HTTP/HTTPS enabled, **Telnet disabled** (not secure), SSH enabled, **management via wireless disabled** (a Wi-Fi client cannot manage the WLC; a checkbox allows it).
- **Security > Access Control Lists**: create an ACL (name MANAGEMENT_ACL, type IPv4) with rules (sequence, source, destination, protocol, DSCP, direction); then **CPU Access Control Lists > Enable CPU ACL**. A **CPU ACL** limits traffic **destined to the WLC itself** (Telnet/SSH, HTTP/HTTPS, SNMP), not traffic passing through it.

### 7. Exam traps

- **Static LAG only**: `channel-group 1 mode on`.
- **DHCP option 43** to point APs to the WLC.
- **Port ≠ interface** on a WLC. **Dynamic interface** = WLAN ↔ VLAN. **Redundancy port** = HA pair. **Distribution system ports** = data traffic, LAG.
- **QoS: Platinum voice, Gold video, Silver default, Bronze background.**
- **Web authentication** = **Layer 3** authentication.
- Know **which tab** creates interfaces (Controller) and WLANs (WLANs): Cisco may test GUI familiarity.

### 8. IOS commands (switch)

```
SW1(config)# vlan 10                                   ! create VLANs 10, 100, 200 and name them
SW1(config-if)# switchport mode access                 ! F0/6-8 as access ports in VLAN 10 (APs and admin PC)
SW1(config-if)# switchport access vlan 10
SW1(config-if)# channel-group 1 mode on                ! F0/1-2: static LAG to the WLC (not active/desirable)
SW1(config-if)# switchport mode trunk                  ! on Port-channel 1
SW1(config-if)# switchport trunk allowed vlan 10,100,200
SW1(config)# interface vlan 100                        ! one SVI per VLAN, .1 address = gateway
SW1(dhcp-config)# default-router 192.168.1.1           ! DHCP pool gateway
SW1(dhcp-config)# option 43 ip 192.168.1.100           ! VLAN 10 pool: WLC address for the APs
SW1(config)# ntp master                                ! the switch becomes an NTP server
SW1# show run                                          ! verify everything (lab)
```

### 9. The lab (Packet Tracer, WLC 3504)

- **Pre-configured**: the switch and the WLC initial setup (the WLC console port is not accessible in Packet Tracer; to redo the initial setup, delete the WLC and add a new one).
- `show run` on SW1: **excluded addresses** in DHCP (good practice to reserve static IPs), VLAN 10 pool (APs and PC1, option 43 not necessary here), VLAN 100 and 200 pools; **VLAN 10 native** on G1/0/1 to the WLC because the WLC does not tag the management VLAN (**tagging must match on both sides**); G1/0/2-4 access in VLAN 10; SVI per VLAN; the `mac-address` commands were added automatically by Packet Tracer.
- From PC1, Desktop > Web Browser: **https://172.16.1.10** (this model does not allow HTTP), account **admin / Cisco123**. The dashboard shows port 1 and the two joined APs, 0 clients.
- Step 2: explore the GUI. **Monitor > Statistics > AP Join** shows joined APs, exchanged messages and the "reason for last unsuccessful attempt": handy to troubleshoot an AP that cannot join.
- Step 3: **Controller > Interfaces > New**: **Internal**, VLAN 100, **port 1**, IP **10.0.0.10**/24, gateway **10.0.0.1**, DHCP 10.0.0.1; **Guest**, VLAN 200, port 1, IP **10.1.0.10**, netmask 255.255.255.0, gateway **10.1.0.1**, DHCP 10.1.0.1.
- Step 4: **WLANs > Create New > Go**: type WLAN, profile name and SSID **Internal**, ID 1. General: **Enabled**, interface Internal. Security: **WPA+WPA2**, **WPA2 policy**, **AES**, no 802.1X, **PSK = Cisco123**. QoS cannot be changed in Packet Tracer; Advanced: max clients **100**. Same for **Guest** (do not forget **Enabled**, an easy mistake).
- Step 5: add a **smartphone**, Config > Wireless0: SSID **Internal**, authentication **WPA2-PSK**, passphrase Cisco123, IP via DHCP. It associates and gets an IP... **from the VLAN 10 pool** instead of VLAN 100: a **Packet Tracer inaccuracy**, not a configuration problem (confirmed on real hardware).

### 10. Quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which WLC port forms an HA pair with another WLC? | **Redundancy port** | It connects two WLCs, one active and one standby ready to take over. |
| Which WLC interface type maps a WLAN to a VLAN? | **Dynamic interface** | The Internal and Guest interfaces map the WLANs to VLANs 100 and 200. |
| Which is a type of Layer 3 authentication? | **Web authentication** | Configured under the Layer 3 tab: username and password before Internet access. |
| Which WLC QoS setting for video traffic? | **Gold** | Silver (best effort) is the default; Gold is recommended for video. |
| Which WLC port type can form a LAG to pass standard data traffic? | **Distribution system port** | Standard network ports for traffic to and from wireless clients. |
