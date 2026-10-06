# CCNA Day 19 : DTP / VTP

> Source : Jeremy's IT Lab, « Free CCNA | DTP/VTP | Day 19 » (38 min, vidéo n°35 de la playlist, cours) et « DTP/VTP | Day 19 Lab » (19 min, vidéo n°36, lab Packet Tracer avec aperçu Boson NetSim et complément sur le mot de passe VTP). Flashcards disponibles. Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 0. Avertissement

DTP et VTP sont deux protocoles **propriétaires Cisco** (ne tournent que sur des équipements Cisco), **retirés de la liste des sujets de l'examen CCNA 200-301**, mais on peut quand même avoir des questions dessus : connaître leur fonction au niveau de base suffit.

### 1. DTP (*Dynamic Trunking Protocol*)

- Permet aux switches Cisco de **négocier dynamiquement** si une interface est **access ou trunk**, sans configuration manuelle. **Activé par défaut** sur toutes les interfaces des switches Cisco.
- **Recommandation : configurer manuellement (`switchport mode access` / `switchport mode trunk`) et désactiver DTP sur tous les ports**, car il peut être exploité par des attaquants (sécurité vue plus tard).
- `switchport mode dynamic ?` : deux options, **auto** et **desirable**.

| Mode administratif | Comportement | Forme un trunk avec |
| :--- | :--- | :--- |
| **dynamic desirable** | Essaie **activement** de former un trunk | trunk, dynamic desirable, dynamic auto |
| **dynamic auto** | **Passif** : accepte un trunk si l'autre le demande, ne le propose pas | trunk, dynamic desirable |
| access | Jamais de trunk | – |
| trunk | Trunk forcé (envoie quand même des trames DTP) | – |

Tableau des résultats (mode opérationnel) :

| | access | dynamic auto | dynamic desirable | trunk |
| :--- | :--- | :--- | :--- | :--- |
| **access** | access | access | access | **misconfig** |
| **dynamic auto** | access | access | trunk | trunk |
| **dynamic desirable** | access | trunk | trunk | trunk |
| **trunk** | **misconfig** | trunk | trunk | trunk |

- access + trunk : les deux sont forcés, **mauvaise configuration**, erreur, le trafic ne passe pas. Ne jamais faire ça en vrai.
- Deux ports qui ne forment pas de trunk fonctionnent en ports d'accès dans le VLAN par défaut, **VLAN 1**.
- `show interfaces g0/0 switchport` : « Switchport: Enabled » (port de couche 2 ; différent avec `no switchport`) ; **Administrative Mode** = ce qu'on a configuré ; **Operational Mode** = trunk ou **static access** (port d'accès dont le VLAN ne change pas ; les ports « dynamic access », VLAN assigné par un serveur selon la MAC, sont hors programme) ; plus bas, **Negotiation of Trunking : On/Off** = DTP envoie ou non des trames.
- **DTP ne forme pas de trunk avec un routeur ou un PC** : pour router on a stick, le port vers le routeur doit être **trunk manuellement**.
- Mode par défaut : **dynamic desirable sur les vieux switches**, **dynamic auto sur les récents**.
- `switchport nonegotiate` désactive DTP (plus de trames DTP). **`switchport mode access` désactive aussi DTP** ; `switchport mode trunk` **ne** l'arrête **pas**, il faut ajouter `switchport nonegotiate`.
- **Négociation de l'encapsulation** : sur les switches supportant dot1q et ISL, défaut `switchport trunk encapsulation negotiate` ; pour configurer un trunk manuellement il faut d'abord choisir dot1q ou isl. **ISL est préféré à dot1q** si les deux switches le supportent (deux ports en dynamic desirable → « Operational Trunking Encapsulation: isl »). Les trames DTP sont envoyées **dans le VLAN 1 avec ISL, dans le VLAN natif avec dot1q** (VLAN 1 par défaut).

### 2. VTP (*VLAN Trunking Protocol*)

- Permet de configurer les VLAN sur un **switch serveur** central ; les **clients VTP** synchronisent leur **base de données de VLAN**. Conçu pour les grands réseaux avec beaucoup de VLAN. **Rarement utilisé, et déconseillé** (danger expliqué plus bas).
- **Trois versions** : 1, 2, 3 (les switches modernes supportent les trois, les vieux seulement 1 et 2). **Trois modes** : **server (défaut)**, client, transparent.

| Mode | Peut ajouter/modifier/supprimer des VLAN | Base VLAN en NVRAM | Synchronisation | Annonces |
| :--- | :--- | :--- | :--- | :--- |
| **Server** (défaut) | Oui ; chaque changement **incrémente le numéro de révision** | Oui | **Se synchronise aussi** sur un autre serveur de révision plus élevée (« un serveur fonctionne aussi comme client ») | Annonce la base sur ses **trunks** (pas sur les ports d'accès) |
| **Client** | Non, commande rejetée | Non (sauf VTPv3) | Vers le serveur de révision la plus élevée du domaine | Annonce sa base et relaie les annonces sur ses trunks |
| **Transparent** | Oui, base **indépendante** en NVRAM, non annoncée | Oui | **Ne se synchronise pas** | **Relaie** les annonces reçues sur ses trunks **si le domaine correspond**, n'annonce pas sa propre base |

- Le **numéro de révision** détermine la version la plus récente de la base, celle vers laquelle tout le monde se synchronise.
- `show vtp status` (défauts) : versions supportées 1 à 3, version active **1** ; **domaine NULL** (vide) ; mode **server** ; **« Maximum VLANs supported locally: 1005 »** (v1 et v2 ne supportent pas les VLAN étendus 1006-4094, il faut **v3**) ; « Number of existing VLANs: 5 » (1 et 1002-1005) ; **« Configuration Revision: 0 »**.
- Démonstration : `vtp domain cisco`, puis `vlan 10` / `name engineering` → domaine cisco, 6 VLAN, révision 1. **Un switch sans domaine (NULL) qui reçoit une annonce rejoint automatiquement ce domaine** : SW2, SW3, SW4 adoptent le domaine cisco, la révision 1 et VLAN10 sans aucune configuration.
- **Danger** : un vieux switch branché avec le **même nom de domaine** et un **numéro de révision supérieur** (ex. révision 50, VLAN 1, 99, 220) écrase la base de tout le domaine (révision 5, VLAN 1, 10, 20, 30, 40) : **tous les hôtes des VLAN 10 à 40 perdent la connectivité**. C'est une raison majeure de ne pas utiliser VTP.
- Démonstration des modes : SW2 `vtp mode client` → `vlan 20` **rejeté** ; SW3 `vtp mode transparent` + domaine **juniper**. VLAN 20 « sales » créé sur SW1 (révision 4 après quelques essais) : SW2 l'a (révision 4) ; SW3 ne l'a pas et affiche **révision 0** ; SW4 ne l'a pas non plus (révision 3) car SW3, dans un autre domaine, ne relaie pas. Remettre SW3 dans le domaine cisco → il relaie, SW4 se synchronise (sans que SW3 lui-même se synchronise).
- **Remettre la révision à 0** : changer le domaine VTP pour un domaine inutilisé, **ou** passer en mode transparent. À faire avant de brancher un vieux switch dans un réseau VTP.
- `vtp version 2` : incrémente la révision et propage la version (SW4 passe en v2, révision 13). Citation Cisco : v2 apporte seulement le support des **VLAN Token Ring**, sinon aucune raison de l'utiliser. v3 : nombreuses nouveautés, hors programme.
- **VTP ne synchronise que la base de VLAN** : il faut toujours configurer les ports (`switchport access vlan 10`…) sur chaque switch.
- Complément du lab : **`vtp password`** : un switch **rejette** toute annonce dont le mot de passe ne correspond pas.

### 3. Pièges d'examen

- Vieux switches : défaut **dynamic desirable** ; récents : **dynamic auto**. auto + auto = access.
- `switchport mode access` coupe DTP ; `switchport mode trunk` **non** (ajouter `switchport nonegotiate`).
- Pas de trunk DTP vers un routeur/PC.
- Mode VTP par défaut = **server** ; un serveur se synchronise aussi (révision plus élevée).
- Transparent : relaie mais ne se synchronise pas, et ne diffuse pas sa base.
- Révision à 0 : domaine inutilisé ou mode transparent (pas de commande « vtp reset »).

### 4. Commandes IOS

```
Switch(config-if)# switchport mode dynamic desirable   ! DTP : cherche activement à former un trunk
Switch(config-if)# switchport mode dynamic auto        ! DTP : accepte un trunk sans le proposer (défaut récent)
Switch(config-if)# switchport mode trunk               ! trunk manuel (DTP toujours actif)
Switch(config-if)# switchport nonegotiate              ! désactive l'envoi de trames DTP
Switch(config-if)# switchport mode access              ! port d'accès, désactive aussi DTP
Switch(config-if)# switchport trunk encapsulation negotiate   ! défaut sur switches ISL+dot1q (ISL préféré)
Switch# show interfaces g0/0 switchport                ! Administrative/Operational Mode, encapsulation, Negotiation of Trunking
Switch# show vtp status                                ! version, domaine, mode, nb de VLAN, révision
Switch(config)# vtp domain cisco                       ! nom de domaine VTP
Switch(config)# vtp mode client                        ! mode client (ne peut plus créer de VLAN)
Switch(config)# vtp mode transparent                   ! mode transparent (révision remise à 0)
Switch(config)# vtp version 2                          ! change la version (incrémente la révision)
Switch(config)# vtp password cisco                     ! mot de passe VTP (lab)
Switch(config)# vlan 10                                ! sur un serveur : incrémente la révision
Switch(config-vlan)# name engineering
```

### 5. Le lab (vidéo n°36)

**Objectif** : 4 VLAN (10, 20, 30, 40) ; trunks manuels sans DTP entre switches (SW1 G0/1, SW2 G0/1 et G0/2, SW3 G0/1) ; VTP pour partager les VLAN ; SW2 transparent, SW3 client ; ports d'accès.

1. **Trunks sans DTP** : sur SW1, `do show interface g0/1 switchport` avant configuration : administratif **dynamic auto**, opérationnel **static access**, « Negotiation of Trunking: On ». En mode simulation on voit passer des trames **STP, CDP et DTP** (STP = Day 20). `switchport mode trunk` → les deux modes sont trunk mais la négociation est **encore On** → `switchport nonegotiate` → Off. SW2 : `interface range g0/1-2`, mêmes commandes ; SW3 : `interface g0/1`, idem. Vérifier chaque port avec `do show interface ... switchport`.
2. **VTP** : sur SW1, `do show vtp status` (version affichée 2 mais « VTP V2 Mode: Disabled », donc v1 ; domaine vide). `vtp domain CCNA`, `vlan 10`, `vlan 20`, `vlan 30` → 8 VLAN, révision **3** (+1 par VLAN créé). Sur SW2 et SW3, sans aucune configuration : domaine CCNA, révision 3, VLAN 10-20-30 présents dans `do show vlan brief`.
3. **SW2 transparent** : `vtp mode transparent`, `vlan 40` → révision **0**, 9 VLAN (il garde ceux synchronisés avant). SW1 et SW3 n'ont **pas** VLAN40 (un transparent n'annonce pas, mais relaie entre SW1 et SW3).
4. **SW3 client** : `vtp mode client`, puis `vlan 50` **refusé** : les nouveaux VLAN doivent être créés sur SW1.
5. **Ports d'accès** : SW3 F0/1 → VLAN10 (avant : « Negotiation of Trunking: On » même vers un PC ; après `switchport mode access` : **Off**), F0/2-3 → VLAN30, F0/4 → VLAN20 ; SW2 F0/1-2 → VLAN40 ; SW1 F0/1-2 → VLAN10, F0/3 → VLAN20.
6. **Mot de passe VTP** (après l'aperçu NetSim) : SW1 `vtp password cisco`, `vlan 50` → révision 4, 9 VLAN ; SW3 reste à révision 3 / 8 VLAN ; avec le mauvais mot de passe `vtp password CCNA` toujours rien ; avec `vtp password cisco` SW3 se synchronise.

**Aperçu Boson NetSim « Configuring VTP Client Mode on Switches »** : `hostname Switch1` ; F0/11-12 déjà en dynamic desirable et trunk opérationnel → `switchport mode trunk` pour qu'ils le soient toujours ; les deux switches ont déjà un domaine « bigdomain », il faut donc `vtp domain cisco` **sur les deux** (si le domaine avait été NULL, un seul aurait suffi) ; Switch1 reste serveur, Switch2 `vtp mode client`. Astuce : **Ctrl-A** ramène au début de la ligne pour ajouter `do` ou `no`.

### 6. Le quiz du Day 19 (3 questions + 1 question Boson ExSim)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| SW1 et SW2 neufs, ports en access. SW2 remplacé par un vieux switch réinitialisé : un trunk se forme. Cause ? A) vieux switches par défaut en mode trunk, B) vieux switches par défaut en dynamic desirable, C) les ports d'accès sont une nouveauté | **B** | Les récents sont en dynamic auto ; auto + desirable (vieux switch) forme un trunk. |
| SW1–SW2–SW3 : SW2 doit relayer la base de SW1 vers SW3 sans se synchroniser. Commande sur SW2 ? A) vtp mode transparent, B) vtp transparent mode, C) vlan mode transparent, D) vtp mode client | **A** | Le mode transparent relaie les annonces sans synchroniser ni annoncer sa propre base. |
| Deux méthodes pour remettre la révision VTP à 0 ? A) domaine inutilisé, B) mode server, C) mode transparent, D) commande vtp reset | **A et C** | Chacune remet la révision à 0, utile avant d'ajouter un switch à révision élevée. |
| Boson ExSim (glisser-déposer) : mode résultant selon les deux modes administratifs (access, dynamic auto, dynamic desirable, trunk). | Voir le tableau de la section 1 | access avec n'importe quoi = access, sauf access + trunk = **misconfig** ; auto + auto = access ; desirable ou trunk avec auto/desirable/trunk = trunk. |

---

## 🇬🇧 English version

### 0. Warning

DTP and VTP are two **Cisco proprietary** protocols (they only run on Cisco devices), **removed from the CCNA 200-301 exam topics list**, but you may still get questions about them: knowing their function at a basic level is enough.

### 1. DTP (Dynamic Trunking Protocol)

- Allows Cisco switches to **dynamically negotiate** whether an interface is **access or trunk**, without manual configuration. **Enabled by default** on all Cisco switch interfaces.
- **Recommendation: configure manually (`switchport mode access` / `switchport mode trunk`) and disable DTP on all switchports**, because it can be exploited by attackers (security covered later).
- `switchport mode dynamic ?`: two options, **auto** and **desirable**.

| Administrative mode | Behavior | Forms a trunk with |
| :--- | :--- | :--- |
| **dynamic desirable** | **Actively** tries to form a trunk | trunk, dynamic desirable, dynamic auto |
| **dynamic auto** | **Passive**: accepts a trunk if the other side asks, does not initiate | trunk, dynamic desirable |
| access | Never a trunk | – |
| trunk | Forced trunk (still sends DTP frames) | – |

Resulting operational mode:

| | access | dynamic auto | dynamic desirable | trunk |
| :--- | :--- | :--- | :--- | :--- |
| **access** | access | access | access | **misconfig** |
| **dynamic auto** | access | access | trunk | trunk |
| **dynamic desirable** | access | trunk | trunk | trunk |
| **trunk** | **misconfig** | trunk | trunk | trunk |

- access + trunk: both forced, a **misconfiguration**, error, traffic will not pass. Never do this in a real network.
- Two ports that do not form a trunk operate as access ports in the default VLAN, **VLAN 1**.
- `show interfaces g0/0 switchport`: "Switchport: Enabled" (Layer 2 port; different with `no switchport`); **Administrative Mode** = what you configured; **Operational Mode** = trunk or **static access** (an access port whose VLAN does not change; "dynamic access" ports, VLAN assigned by a server based on the MAC, are out of scope); further down, **Negotiation of Trunking: On/Off** = whether DTP frames are sent.
- **DTP will not form a trunk with a router or PC**: for router on a stick, the port to the router must be **manually configured as a trunk**.
- Default mode: **dynamic desirable on older switches**, **dynamic auto on newer switches**.
- `switchport nonegotiate` disables DTP (no more DTP frames). **`switchport mode access` also disables DTP**; `switchport mode trunk` does **not**, you must add `switchport nonegotiate`.
- **Encapsulation negotiation**: on switches supporting dot1q and ISL, default `switchport trunk encapsulation negotiate`; to manually configure a trunk you must first choose dot1q or isl. **ISL is favored over dot1q** if both switches support it (two dynamic desirable ports → "Operational Trunking Encapsulation: isl"). DTP frames are sent **in VLAN 1 with ISL, in the native VLAN with dot1q** (VLAN 1 by default).

### 2. VTP (VLAN Trunking Protocol)

- Lets you configure VLANs on a central **server switch**; **VTP clients** synchronize their **VLAN database** to it. Designed for large networks with many VLANs. **Rarely used, and not recommended** (danger explained below).
- **Three versions**: 1, 2, 3 (modern switches support all three, older ones only 1 and 2). **Three modes**: **server (default)**, client, transparent.

| Mode | Can add/modify/delete VLANs | VLAN database in NVRAM | Synchronization | Advertisements |
| :--- | :--- | :--- | :--- | :--- |
| **Server** (default) | Yes; every change **increments the revision number** | Yes | **Also syncs** to another server with a higher revision ("VTP servers also function as VTP clients") | Advertises the database on its **trunks** (not on access ports) |
| **Client** | No, command rejected | No (except VTPv3) | To the server with the highest revision in the domain | Advertises its database and forwards advertisements on its trunks |
| **Transparent** | Yes, **independent** database in NVRAM, not advertised | Yes | **Does not sync** | **Forwards** received advertisements on its trunks **if the domain matches**, does not advertise its own database |

- The **revision number** determines the newest version of the database, the one all switches sync to.
- `show vtp status` (defaults): versions 1 to 3 capable, running version **1**; **domain NULL** (empty); mode **server**; **"Maximum VLANs supported locally: 1005"** (v1 and v2 do not support extended VLANs 1006-4094, **v3** needed); "Number of existing VLANs: 5" (1 and 1002-1005); **"Configuration Revision: 0"**.
- Demonstration: `vtp domain cisco`, then `vlan 10` / `name engineering` → domain cisco, 6 VLANs, revision 1. **A switch with no domain (NULL) that receives an advertisement automatically joins that domain**: SW2, SW3, SW4 adopt domain cisco, revision 1 and VLAN10 without any configuration.
- **Danger**: an old switch plugged in with the **same domain name** and a **higher revision number** (e.g. revision 50, VLANs 1, 99, 220) overwrites the whole domain's database (revision 5, VLANs 1, 10, 20, 30, 40): **all hosts in VLANs 10 to 40 instantly lose connectivity**. A major reason VTP is not used in modern networks.
- Mode demonstration: SW2 `vtp mode client` → `vlan 20` **rejected**; SW3 `vtp mode transparent` + domain **juniper**. VLAN 20 "sales" created on SW1 (revision 4 after some other changes): SW2 has it (revision 4); SW3 does not and shows **revision 0**; SW4 does not either (revision 3) because SW3, in a different domain, does not forward. Set SW3 back to domain cisco → it forwards, SW4 syncs (while SW3 itself does not).
- **Reset the revision to 0**: change the VTP domain to an unused domain, **or** change to transparent mode. Do this before plugging an old switch into a VTP network.
- `vtp version 2`: increments the revision and propagates the version (SW4 runs v2, revision 13). Cisco quote: v2 only adds support for **Token Ring VLANs**, otherwise there is no reason to use it. v3: many new features, beyond the CCNA.
- **VTP only syncs the VLAN database**: you still configure the ports (`switchport access vlan 10`...) on each switch.
- Lab extra: **`vtp password`**: a switch **rejects** any advertisement whose password does not match.

### 3. Exam traps

- Older switches: default **dynamic desirable**; newer: **dynamic auto**. auto + auto = access.
- `switchport mode access` turns DTP off; `switchport mode trunk` does **not** (add `switchport nonegotiate`).
- No DTP trunk with a router/PC.
- Default VTP mode = **server**; a server also syncs (higher revision).
- Transparent: forwards but does not sync, and does not advertise its own database.
- Revision to 0: unused domain or transparent mode (there is no "vtp reset" command).

### 4. IOS commands

```
Switch(config-if)# switchport mode dynamic desirable   ! DTP: actively tries to form a trunk
Switch(config-if)# switchport mode dynamic auto        ! DTP: accepts a trunk without initiating (newer default)
Switch(config-if)# switchport mode trunk               ! manual trunk (DTP still running)
Switch(config-if)# switchport nonegotiate              ! stops sending DTP frames
Switch(config-if)# switchport mode access              ! access port, also disables DTP
Switch(config-if)# switchport trunk encapsulation negotiate   ! default on ISL+dot1q switches (ISL favored)
Switch# show interfaces g0/0 switchport                ! Administrative/Operational Mode, encapsulation, Negotiation of Trunking
Switch# show vtp status                                ! version, domain, mode, number of VLANs, revision
Switch(config)# vtp domain cisco                       ! VTP domain name
Switch(config)# vtp mode client                        ! client mode (can no longer create VLANs)
Switch(config)# vtp mode transparent                   ! transparent mode (revision reset to 0)
Switch(config)# vtp version 2                          ! changes the version (increments the revision)
Switch(config)# vtp password cisco                     ! VTP password (lab)
Switch(config)# vlan 10                                ! on a server: increments the revision
Switch(config-vlan)# name engineering
```

### 5. The lab (video 36)

**Objective**: 4 VLANs (10, 20, 30, 40); manual trunks with DTP disabled between switches (SW1 G0/1, SW2 G0/1 and G0/2, SW3 G0/1); VTP to share VLANs; SW2 transparent, SW3 client; access ports.

1. **Trunks without DTP**: on SW1, `do show interface g0/1 switchport` before configuring: administrative **dynamic auto**, operational **static access**, "Negotiation of Trunking: On". In simulation mode you can see **STP, CDP and DTP** frames (STP = Day 20). `switchport mode trunk` → both modes trunk but negotiation **still On** → `switchport nonegotiate` → Off. SW2: `interface range g0/1-2`, same commands; SW3: `interface g0/1`, same. Check each port with `do show interface ... switchport`.
2. **VTP**: on SW1, `do show vtp status` (version displays 2 but "VTP V2 Mode: Disabled", so v1 running; blank domain). `vtp domain CCNA`, `vlan 10`, `vlan 20`, `vlan 30` → 8 VLANs, revision **3** (+1 per VLAN created). On SW2 and SW3, with no configuration: domain CCNA, revision 3, VLANs 10-20-30 present in `do show vlan brief`.
3. **SW2 transparent**: `vtp mode transparent`, `vlan 40` → revision **0**, 9 VLANs (it keeps those synced earlier). SW1 and SW3 do **not** have VLAN40 (a transparent switch does not advertise, but forwards between SW1 and SW3).
4. **SW3 client**: `vtp mode client`, then `vlan 50` **refused**: new VLANs must be created on SW1.
5. **Access ports**: SW3 F0/1 → VLAN10 (before: "Negotiation of Trunking: On" even toward a PC; after `switchport mode access`: **Off**), F0/2-3 → VLAN30, F0/4 → VLAN20; SW2 F0/1-2 → VLAN40; SW1 F0/1-2 → VLAN10, F0/3 → VLAN20.
6. **VTP password** (after the NetSim preview): SW1 `vtp password cisco`, `vlan 50` → revision 4, 9 VLANs; SW3 stays at revision 3 / 8 VLANs; with the wrong password `vtp password CCNA` still nothing; with `vtp password cisco` SW3 syncs.

**Boson NetSim preview "Configuring VTP Client Mode on Switches"**: `hostname Switch1`; F0/11-12 already dynamic desirable and operationally trunk → `switchport mode trunk` so they always are; both switches already have domain "bigdomain", so `vtp domain cisco` is needed **on both** (had the domain been NULL, one would have been enough); Switch1 stays server, Switch2 `vtp mode client`. Tip: **Ctrl-A** returns to the beginning of the line to add `do` or `no`.

### 6. Day 19 quiz (3 questions + 1 Boson ExSim question)

| Question | Answer | Why |
| :--- | :--- | :--- |
| SW1 and SW2 are new, ports in access mode. SW2 replaced by an old, reset spare switch: a trunk forms. Cause? A) old switches default to trunk mode, B) old switches default to dynamic desirable, C) access ports are a newer feature | **B** | Newer switches default to dynamic auto; auto + desirable (old switch) forms a trunk. |
| SW1–SW2–SW3: SW2 must forward SW1's VLAN database to SW3 without syncing. Command on SW2? A) vtp mode transparent, B) vtp transparent mode, C) vlan mode transparent, D) vtp mode client | **A** | Transparent mode forwards advertisements without syncing or advertising its own database. |
| Two methods to reset the VTP revision number to 0? A) unused domain name, B) server mode, C) transparent mode, D) vtp reset command | **A and C** | Either resets the revision to 0, useful before adding a switch with a higher revision. |
| Boson ExSim (drag-and-drop): resulting mode for each pair of administrative modes (access, dynamic auto, dynamic desirable, trunk). | See the table in section 1 | access with anything = access, except access + trunk = **misconfig**; auto + auto = access; desirable or trunk with auto/desirable/trunk = trunk. |
