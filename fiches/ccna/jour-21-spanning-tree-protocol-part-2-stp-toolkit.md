# CCNA Day 21 : Spanning Tree Protocol (Part 2) + STP Toolkit / STP partie 2 + boîte à outils STP

> Source : Jeremy's IT Lab, vidéos n°39 à 44 de la playlist. 039 « Spanning Tree Protocol (Part 2) | Day 21 » (cours, 42 min) ; 040 « PortFast (STP Toolkit) » (18 min), 041 « BPDU Guard & BPDU Filter » (24 min), 042 « Root Guard » (20 min), 043 « Loop Guard » (19 min) : les quatre vidéos « STP Toolkit » du Day 21 (parts 1 à 4) ; 044 « Configuring STP (PVST+) | Day 21 Lab » (17 min). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Les états de port STP (STP port states)

Deux états **stables** : **Blocking** (ports non désignés) et **Forwarding** (ports racine et désignés). Deux états **transitoires** : **Listening** et **Learning**, traversés quand une interface s'active ou quand un port Blocking doit passer en Forwarding après un changement de topologie. Un cinquième état, **Disabled**, désigne simplement une interface administrativement arrêtée (*shutdown*) ; il ne joue aucun rôle dans STP.

| État | Envoie/reçoit BPDU | Trafic normal | Apprend les MAC | Durée |
| :--- | :--- | :--- | :--- | :--- |
| **Blocking** | reçoit seulement (ne transmet pas) | non, trafic jeté | non | stable |
| **Listening** | oui (seulement des BPDU) | non, trames jetées | non | 15 s (Forward delay) |
| **Learning** | oui (seulement des BPDU) | non | **oui** (prépare la table MAC) | 15 s (Forward delay) |
| **Forwarding** | oui | oui | oui | stable |
| Disabled | interface shutdown | | | |

Seuls les ports **Root** ou **Designated** entrent en Listening : un port non désigné reste toujours Blocking, puisque Listening mène vers Forwarding. La différence Listening/Learning : en Learning, le port **apprend les adresses MAC** des trames reçues (sans les transmettre) pour construire sa table MAC avant de transmettre.

### 2. Les timers STP

- **Hello timer** : fréquence d'envoi des BPDU par le **root bridge**, **2 secondes** par défaut. Les autres switches n'émettent pas leurs propres BPDU : ils **transfèrent** celles du root, et **uniquement sur leurs ports désignés** (jamais sur les ports racine ni non désignés), en mettant à jour le coût vers la racine, l'ID du bridge émetteur, l'ID du port émetteur. (Au démarrage, chaque switch se croit root et envoie des BPDU sur toutes ses interfaces ; après convergence, seul le root en émet.)
- **Forward delay** : durée de **chacun** des états Listening et Learning, **15 secondes** par défaut, donc **30 secondes** au total pour atteindre Forwarding.
- **Max Age** : **20 secondes** par défaut. Temps qu'une interface attend avant de modifier la topologie après avoir cessé de recevoir des BPDU. Chaque port racine ou non désigné s'attend à recevoir des BPDU ; chaque BPDU reçue remet le compteur à 20. S'il atteint 0, le switch réévalue ses choix (root bridge, ports racine, désignés, non désignés). Un port non désigné qui devient désigné ou racine passe alors par Listening (15 s) et Learning (15 s) : **jusqu'à 50 secondes** entre la panne et la transmission.
- Un port Forwarding peut passer **directement** en Blocking (aucun risque de boucle), mais un port Blocking ne peut jamais passer directement en Forwarding.
- Les timers configurés sur le **root bridge** s'imposent à tous les switches du réseau, même s'ils sont configurés différemment.

### 3. La BPDU (Bridge Protocol Data Unit)

- Adresse MAC de destination des BPDU de **PVST+ (Cisco) : 0100.0ccc.cccd**. STP standard (non Cisco) : **0180.c200.0000**. Jeremy recommande de retenir les deux.
- PVST (ancien) ne supporte que l'encapsulation ISL ; **PVST+** supporte 802.1Q (quand Jeremy dit PVST, il veut dire PVST+).
- Champs : Protocol Identifier (toujours 0x0000), Protocol Version Identifier (0 pour STP classique, autre valeur pour Rapid STP au Day 22), BPDU Type (0x00 = *configuration BPDU*), Flags (signalent les changements de topologie), **Root Identifier** (priorité + extended system ID = VLAN ID + adresse MAC du root), **Root Path Cost** (0 sur le root), **Bridge Identifier** (identique au Root Identifier sur le root bridge), **Port Identifier** (ex. 0x8002 : 0x80 = 128 = priorité de port par défaut, 02 = numéro du port), **Message Age** (0 sur le root, +1 à chaque switch traversé, soustrait du Max Age à la réception), puis Max Age, Hello Time, Forward Delay.
- Pas besoin de mémoriser la BPDU champ par champ pour le CCNA, sauf les MAC de destination et la lecture du Port ID.

### 4. STP Toolkit (fonctions optionnelles)

Dans la vidéo 039, Jeremy présente PortFast et BPDU Guard, puis cite Root Guard et Loop Guard (et UplinkFast, BackboneFast, à ne pas étudier). Les quatre vidéos ci-dessous détaillent chaque outil ; Cisco attend qu'on connaisse PortFast, BPDU Guard, BPDU Filter, Root Guard et Loop Guard.

#### 4.1 PortFast (vidéo 040)

- **Problème** : un hôte branché sur un port passe up/up mais ses trames sont jetées pendant **30 secondes** (15 s Listening + 15 s Learning). Sur un switch réel, le voyant (*link light*) clignote **ambre/orange** pendant ce temps, puis devient vert. Attente inutile : aucune boucle de couche 2 n'est possible entre un switch et un PC (seuls les switches inondent les trames).
- **Solution** : PortFast fait entrer le port **immédiatement en Forwarding** dès qu'il est activé, en sautant Listening et Learning.
- **À n'activer que sur les ports vers des hôtes finaux** (ou un routeur) : sur un port vers un autre switch, il peut causer une boucle temporaire. Message d'avertissement de l'IOS : « PortFast should only be enabled on ports connected to a single host. Connecting hubs, concentrators, switches, bridges... can cause temporary bridging loops. Use with CAUTION ».
- Deux méthodes : `spanning-tree portfast` sur l'interface (actif seulement en mode **non-trunk** : « will only have effect when the interface is in a non-trunking mode ») ; `spanning-tree portfast default` en global, qui active PortFast sur **tous les ports access** (pas les trunks, malgré le message qui dit « all interfaces »). On peut ensuite désactiver port par port avec `spanning-tree portfast disable`.
- **PortFast sur un trunk** : possible seulement par interface avec `spanning-tree portfast trunk`, utile pour un serveur de virtualisation (VM dans plusieurs VLAN) ou un routeur en *router-on-a-stick* (un routeur n'inonde pas les trames).
- **PortFast edge / network** : deux modes ; *edge* est celui du CCNA, *network* sert à Bridge Assurance (hors programme). Sur un IOS moderne, le mot-clé **EDGE** est ajouté automatiquement dans la running-config (`spanning-tree portfast edge`, `edge trunk`, `edge default`) ; les deux formes sont équivalentes. Exception : `spanning-tree portfast disable` n'utilise pas EDGE. Packet Tracer ne supporte pas le mot-clé EDGE.
- Vérification : `show spanning-tree interface g0/1 detail` affiche « The port is in the portfast edge mode » (« by default » si activé en global, « portfast edge trunk mode » pour un trunk). `show running-config interface g0/1` (pas dans Packet Tracer) montre la config de la seule interface.

#### 4.2 BPDU Guard et BPDU Filter (vidéo 041)

- Un port PortFast **continue d'envoyer des BPDU** toutes les 2 secondes (le PC les ignore) et STP n'est pas désactivé. S'il **reçoit** une BPDU, il redevient un port STP normal. Exemple « Bob de la comptabilité » : il branche son propre switch sur la prise murale ; si ce switch a un bridge ID plus bas, il devient root bridge et modifie la topologie (le lien SW1-SW2 se bloque, les chemins vers le routeur deviennent moins efficaces).
- **BPDU Guard** : le port continue d'envoyer des BPDU, mais s'il **en reçoit une**, il passe en **err-disabled** (plus aucune donnée ni BPDU). Configurable séparément de PortFast, mais généralement utilisés ensemble. Messages : « Received BPDU on port GigabitEthernet0/1 with BPDU Guard enabled. Disabling port. », « bpduguard error detected on G0/1, putting G0/1 in err-disable state ». Sur un switch réel, le voyant devient **ambre fixe** et reste allumé même câble débranché. ErrDisable est aussi déclenché par d'autres violations vues plus tard : power policing, Port Security, DAI (Dynamic ARP Inspection).
- Configuration : `spanning-tree bpduguard enable` sur l'interface ; `spanning-tree portfast bpduguard default` en global (mot-clé EDGE optionnel), qui l'active sur **tous les ports PortFast** (pas « tous les ports access » : différence testable à l'examen) ; `spanning-tree bpduguard disable` pour l'exclure d'un port.
- **Réactiver un port err-disabled** : d'abord **résoudre la cause** (sinon il est désactivé à nouveau). Manuel : `shutdown` puis `no shutdown`. Automatique : **ErrDisable Recovery**, désactivé par défaut, timer par défaut **300 secondes (5 minutes)**. `show errdisable recovery` liste les causes (arp-inspection, bpduguard...) et les ports en attente ; `errdisable recovery cause bpduguard` l'active pour BPDU Guard ; `errdisable recovery interval <s>` change le délai (il faut quand même activer la cause).
- **BPDU Filter** : un port vers un hôte envoie des BPDU inutilement (un peu de bande passante et de CPU, et surtout des infos sur la topologie STP envoyées à des équipements utilisateurs). BPDU Filter **empêche le port d'envoyer des BPDU** ; contrairement à BPDU Guard, il ne désactive pas le port s'il en reçoit. Son comportement **dépend de la méthode de configuration** :
  - `spanning-tree bpdufilter enable` sur l'interface : n'envoie pas de BPDU **et ignore celles reçues** = STP désactivé sur le port. **À utiliser avec prudence** : sur le mauvais port, boucle **permanente** et tempête de broadcast.
  - `spanning-tree portfast bpdufilter default` en global : activé sur tous les ports PortFast ; le port n'envoie pas de BPDU, mais **s'il en reçoit une, PortFast et BPDU Filter sont désactivés** et le port redevient un port STP normal (« le meilleur des deux mondes »). `spanning-tree bpdufilter disable` pour exclure un port.
- Recommandation de Jeremy : n'activer BPDU Filter **qu'en global**. Combinaison avec BPDU Guard sur le même port : si BPDU Filter est global et qu'une BPDU arrive, BPDU Filter se désactive et BPDU Guard err-disable le port ; si BPDU Filter est configuré sur l'interface, la BPDU est ignorée et **BPDU Guard n'a aucun effet**.

#### 4.3 Root Guard (vidéo 042)

- **Choix du root bridge** : pas au hasard. Critères : **flux de trafic optimal** (minimiser la latence et la congestion ; les PC parlent surtout au routeur/WAN, donc le root doit être le switch relié au routeur, ex. SW1) et **stabilité/fiabilité** (le switch le plus moderne et fiable). Avec un mauvais root (SW3), le trafic de SW2 fait un détour SW2→SW3→SW1 ; la latence ajoutée est négligeable (moins d'une milliseconde), le vrai problème est la **congestion** du lien SW3-SW1 (trames en attente, voire jetées).
- Dans son propre LAN, on contrôle le root en mettant sa **priorité à 0** (bridge ID = 0 + VLAN ID, PVST+ ajoute toujours le VLAN ID). Mais si l'on connecte son LAN à des switches hors de son contrôle (exemple : fournisseur de service Metro Ethernet relié à un client, dans un MAN), un switch avec priorité 0 et une **MAC plus basse** (SW6, 5254.0018... contre 5254.001a...) prend le rôle de root et casse la topologie du fournisseur (SW1-SW3 et SW2-SW3 bloqués, les trames font un détour par le LAN du client).
- **Root Guard** empêche un port d'accepter des **BPDU supérieures** (qui annoncent un meilleur root bridge ID) : le port passe dans l'état **broken (BKN), Root Inconsistent (ROOT_Inc)**, il ne transmet ni ne reçoit plus de trames (il reste up/up : c'est STP qui bloque). Message : « Root guard blocking port ». Les ports des deux côtés du lien sont alors tous « designated » (cas particulier : normalement un seul port désigné par lien).
- Configuration : `spanning-tree guard root` sur l'interface, **aucune commande globale** (ce n'est pas une fonction à activer partout). À configurer sur les ports **vers les switches hors de contrôle** (SW2 G0/2, SW3 G0/2 côté fournisseur). Le **client** ne doit pas le configurer sur ses ports vers le fournisseur, sinon ses liens seraient bloqués.
- **Récupération automatique** : rien à faire dans le CLI. Il faut que les BPDU supérieures cessent (le fournisseur demande au client de monter la priorité de SW6, par ex. à 4096 → 4097 avec le VLAN) ; après expiration de la BPDU (**Max Age 20 s**), le port est débloqué (« unblocked ») et le réseau converge avec SW1 root.

#### 4.4 Loop Guard (vidéo 043)

- Protège contre un port qui **cesse de recevoir des BPDU de manière inattendue** (bug logiciel sur un switch voisin, ou **lien unidirectionnel**).
- **Lien unidirectionnel** : données dans un seul sens. Cause de couche 1 : câble, connecteur ou transceiver (SFP, *small form-factor pluggable*) défectueux. Plus fréquent en **fibre optique** (deux fibres séparées Tx→Rx ; si une fibre est endommagée sans que les équipements le détectent, l'interface reste up/up alors que la communication ne marche que dans un sens ; la fibre casse d'un petit « snap » si on la plie trop). Si le problème est détecté, le lien tombe entièrement, pas de lien unidirectionnel.
- **Problème pour STP** : SW3 G0/1 est non désigné (Blocking) parce qu'il reçoit des BPDU supérieures de SW2. Si les BPDU de SW2 n'arrivent plus, à l'expiration du **Max Age**, SW3 G0/1 devient désigné et passe en Forwarding ; SW2 ignore les BPDU inférieures de SW3 ; les deux ports sont Forwarding → **boucle** SW1→SW3→SW2 pour les trames de broadcast.
- **Loop Guard** : quand le Max Age d'un port protégé atteint 0, au lieu de devenir désigné, le port passe en **broken (BKN), Loop Inconsistent (LOOP_Inc)**. Le port reste up/up. Récupération **automatique** dès que les BPDU reviennent (statut revient à Blocking).
- Configuration : `spanning-tree guard loop` sur l'interface ; `spanning-tree loopguard default` en global (tous les ports) puis `spanning-tree guard none` pour exclure un port. À activer sur les ports **racine et non désignés** (ceux qui doivent recevoir des BPDU).
- **Loop Guard et Root Guard sont mutuellement exclusifs** (rôles opposés : Root Guard empêche un port désigné de devenir racine, Loop Guard empêche un port racine/non désigné de devenir désigné). Configurer l'un sur un port désactive l'autre ; la **commande la plus spécifique l'emporte** (interface > global), règle générale de l'IOS, valable aussi pour PortFast, BPDU Guard, BPDU Filter.

### 5. Configuration STP de base (vidéo 039)

- **Mode** : `spanning-tree mode {mst | pvst | rapid-pvst}`. MST hors programme ; PVST = STP classique par VLAN ; Rapid-PVST = version améliorée (Day 22), **mode par défaut des switches Cisco modernes**.
- **Root bridge** : `spanning-tree vlan <n> root primary` fixe la priorité à **24576**, ou à **4096 de moins** que la plus basse priorité existante si un autre switch est déjà sous 24576. La running-config montre en réalité `spanning-tree vlan 1 priority 24576`. `spanning-tree vlan <n> root secondary` fixe la priorité à **28672** (prochain root si le primaire tombe). On peut aussi utiliser directement `spanning-tree vlan <n> priority <valeur>` (multiples de 4096) ; la commande `root` évite de retenir les incréments.
- **Load balancing** : avec PVST+, la configuration est **par VLAN**. Un root différent par VLAN bloque des liens différents dans chaque VLAN, au lieu de laisser le même lien inutilisé partout.
- **Réglages de port**, par VLAN : `spanning-tree vlan <n> cost <1-200000000>` (coût : FastEthernet 19, GigabitEthernet 4 ; critère principal du root port, tiebreaker pour désigné/non désigné) et `spanning-tree vlan <n> port-priority <0-224, par pas de 32>` (première moitié du Port ID, dernier tiebreaker du root port).

### 6. Pièges d'examen

- **Forward delay = 15 s pour chaque état**, pas 15 s au total : 30 s pour Listening + Learning, **50 s** avec le Max Age (20 s).
- Blocking **reçoit** les BPDU mais ne les transmet pas et n'apprend pas de MAC ; Learning apprend les MAC mais ne transmet pas le trafic.
- Les BPDU ne sont transférées que sur les **ports désignés**.
- MAC de destination : **0100.0ccc.cccd** (PVST+) vs **0180.c200.0000** (STP standard).
- Port ID 0x8002 → priorité **128** (0x80), port 2.
- `spanning-tree portfast default` → **tous les ports access** ; `spanning-tree portfast bpduguard default` → **tous les ports PortFast**. Noter la différence de syntaxe : `bpduguard enable` sur l'interface, mais `portfast bpduguard default` en global.
- BPDU Guard err-disable le port (récupération manuelle shut/no shut ou ErrDisable Recovery, 5 min par défaut) ; Root Guard et Loop Guard mettent le port en **broken** (BKN) avec récupération **automatique**.
- BPDU Filter par interface = STP désactivé sur le port (boucle permanente possible) ; BPDU Filter global = se désactive si une BPDU arrive.
- Root Guard : pas de commande globale. Root Guard et Loop Guard ne peuvent pas être actifs ensemble sur un port.
- `root primary` = 24576 (ou plus bas de 4096 que le minimum existant) ; `root secondary` = 28672.
- Jeremy recommande de **laisser les timers par défaut** : ils ont été choisis pour une raison.

### 7. Commandes IOS

```
Switch(config)# spanning-tree mode pvst                  ! STP classique par VLAN (défaut moderne : rapid-pvst)
Switch(config)# spanning-tree vlan 1 root primary        ! priorité 24576 (ou min existant - 4096)
Switch(config)# spanning-tree vlan 1 root secondary      ! priorité 28672
Switch(config)# spanning-tree vlan 1 priority 24576      ! ce qui est réellement écrit dans la running-config
Switch(config-if)# spanning-tree vlan 1 cost 100         ! coût du port dans ce VLAN (1 à 200000000)
Switch(config-if)# spanning-tree vlan 1 port-priority 240 ! priorité de port (0 à 224 par pas de 32 selon la vidéo 039 ; 240 accepté dans le lab)
Switch(config-if)# spanning-tree portfast                ! PortFast sur ce port (actif seulement en mode access ; = portfast edge)
Switch(config-if)# spanning-tree portfast trunk          ! PortFast sur un trunk (routeur ROAS, serveur de VM)
Switch(config-if)# spanning-tree portfast disable        ! exclure ce port après activation globale
Switch(config)# spanning-tree portfast default           ! PortFast sur tous les ports access
Switch(config-if)# spanning-tree bpduguard enable        ! BPDU Guard sur ce port
Switch(config-if)# spanning-tree bpduguard disable       ! exclure ce port
Switch(config)# spanning-tree portfast bpduguard default ! BPDU Guard sur tous les ports PortFast
Switch(config-if)# spanning-tree bpdufilter enable       ! BPDU Filter par port : STP désactivé sur le port (prudence)
Switch(config-if)# spanning-tree bpdufilter disable      ! exclure ce port
Switch(config)# spanning-tree portfast bpdufilter default ! BPDU Filter sur tous les ports PortFast (recommandé)
Switch(config-if)# spanning-tree guard root              ! Root Guard (pas de version globale)
Switch(config-if)# spanning-tree guard loop              ! Loop Guard sur ce port
Switch(config)# spanning-tree loopguard default          ! Loop Guard sur tous les ports
Switch(config-if)# spanning-tree guard none              ! retirer Root/Loop Guard du port
Switch(config)# errdisable recovery cause bpduguard      ! récupération automatique après BPDU Guard
Switch(config)# errdisable recovery interval 300         ! délai de récupération en secondes (défaut 300)
Switch(config-if)# shutdown                              ! puis no shutdown : réactivation manuelle d'un port err-disabled
Switch# show spanning-tree                               ! root, bridge ID, rôle/état de chaque port, BKN ROOT_Inc / LOOP_Inc
Switch# show spanning-tree vlan 1                        ! un seul VLAN
Switch# show spanning-tree interface g0/1 detail         ! PortFast, BPDU Guard, Loop Guard, BPDU envoyées/reçues
Switch# show errdisable recovery                         ! causes activées, timer, ports en attente
Switch# show interfaces g0/1                             ! statut err-disabled
Switch# show running-config interface g0/1               ! config de l'interface seule (pas dans Packet Tracer)
```

### 8. Le lab (vidéo 044, Configuring STP PVST+)

Objectif : vérifier la topologie STP, configurer le load balancing par VLAN, manipuler coût et priorité de port, activer PortFast et BPDU Guard. Quatre switches SW1-SW4, liens FastEthernet, VLAN 1 et 2.

1. **Topologie actuelle** : `show spanning-tree` sur chaque switch. SW1 n'est pas root (MAC du Root ID ≠ Bridge ID), son F0/3 est root port. SW2 : « This bridge is the root », tous ses ports désignés/Forwarding, dans VLAN 1 et VLAN 2 (sans configuration, même root et mêmes rôles dans chaque VLAN). SW3 : F0/2 root port (directement connecté, tous les liens FastEthernet), F0/1 désigné. SW4 : F0/1 root port, F0/2 Blocking avec le rôle **« Altn » (alternate = non désigné)**.
2. **Load balancing** : sur SW1, `spanning-tree vlan 1 root primary` et `spanning-tree vlan 2 root secondary` ; sur SW2, `spanning-tree vlan 1 root secondary` et `spanning-tree vlan 2 root primary`. Toujours indiquer le VLAN (PVST+ configure par VLAN). Vérifier avec `do show spanning-tree` : SW2 reste root dans VLAN 2, mais dans VLAN 1 son F0/3 devient root port ; SW1 est root dans VLAN 1 (tous ports désignés) et garde F0/3 root port dans VLAN 2.
3. **Coût** : sur SW4, `show spanning-tree vlan 1` confirme F0/2 root port (coût le plus bas). `interface f0/2`, `spanning-tree vlan 1 cost 100` (plus de 5 fois le coût actuel) : F0/2 passe en Blocking, **F0/1 devient root port** (le coût est le premier critère).
4. **Port-priority** : sur SW1, `interface f0/1`, `spanning-tree vlan 1 port-priority 240` (le plus grand nombre = la plus basse priorité). Sur SW1, la colonne Prio.Nbr affiche 240. Sur SW3, F0/1 **reste root port** : le Port ID émetteur est le **dernier** tiebreaker, après le coût (19 contre 38) et le bridge ID émetteur.
5. **PortFast + BPDU Guard** : activer « Show Link Lights » (Options, Preferences). Supprimer puis recréer le lien PC1-SW3 F0/3 : voyant **orange ~30 s**. `interface f0/3`, `spanning-tree portfast`, `spanning-tree bpduguard enable`. Reconnecter : voyant **vert immédiatement**. Relier F0/3 à SW4 avec un **câble croisé** : à la réception d'une BPDU, le port est désactivé, voyant **rouge**. Reconnecter PC1 (câble droit) puis `shutdown` / `no shutdown` pour réactiver. Même configuration sur SW4 F0/3.

Aperçu Boson NetSim (lab ENCOR « PVST Load Balancing », niveau CCNP car la configuration STP n'est pas dans la liste des sujets CCNA) : VTP, trunks, VLAN, root primaire/secondaire par groupes de VLAN (1-3 et 4-6), documentation des bridge ID, root ports, designated/alternate ports.

### 9. Le quiz (vidéo 039 : questions 7 à 10, suite des questions 1 à 6 du Day 20, plus une question Boson ExSim)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Q7. VLAN 10 et 20, SW3 root par défaut. SW1 primaire pour VLAN 10 et secondaire pour VLAN 20 ; SW2 l'inverse : quelles commandes ? | SW1 : `spanning-tree vlan 10 root primary`, `spanning-tree vlan 20 root secondary`. SW2 : `spanning-tree vlan 20 root primary`, `spanning-tree vlan 10 root secondary` | Chaque switch devient root d'un VLAN et root de secours (deuxième priorité la plus basse) de l'autre : load balancing entre les liens. |
| Q8. Un PC branché n'accède pas au réseau pendant une demi-minute. Deux solutions ? | **A** PortFast sur le port et **C** réduire le Forward delay | PortFast saute Listening/Learning ; le Forward delay fixe la durée de ces états. Hello (B) et Max Age (D) n'interviennent pas. Jeremy recommande de laisser les timers par défaut. |
| Q9. Port ID STP 0x8002 : priorité du port ? | **C, 128** | La première moitié du Port ID, 0x80, est la priorité = 128 en décimal. 80, 32 et 224 sont faux. |
| Q10. Éviter une boucle si un utilisateur branche un switch sur un port : quelle fonction ? | **D, BPDU Guard** | Il arrête l'interface dès réception d'une BPDU ; à activer sur les ports PortFast vers hôtes finaux. PortFast crée le risque, Loop Guard et Root Guard ont d'autres rôles. |
| Boson ExSim. `spanning-tree portfast default` en global sur SwitchA : quels ports utilisent PortFast ? | **D, tous les ports access** | PortFast peut être activé globalement (A faux) ; il ne s'active pas sur les trunks (B, C faux). Boson précise : 30 s par défaut, jusqu'à 50 s si PAgP est activé (Day 23). |

---

## 🇬🇧 English version

### 1. STP port states

Two **stable** states: **Blocking** (non-designated ports) and **Forwarding** (root and designated ports). Two **transitional** states: **Listening** and **Learning**, passed through when an interface is activated or when a Blocking port must move to Forwarding after a topology change. A fifth state, **Disabled**, is simply an administratively shut down interface; it plays no role in STP.

| State | Sends/receives BPDUs | Regular traffic | Learns MACs | Length |
| :--- | :--- | :--- | :--- | :--- |
| **Blocking** | receives only (does not forward) | no, dropped | no | stable |
| **Listening** | yes (BPDUs only) | no, frames discarded | no | 15 s (Forward delay) |
| **Learning** | yes (BPDUs only) | no | **yes** (builds the MAC table) | 15 s (Forward delay) |
| **Forwarding** | yes | yes | yes | stable |
| Disabled | shutdown interface | | | |

Only **Root** or **Designated** ports enter Listening: a non-designated port is always Blocking, since Listening leads to Forwarding. Listening vs Learning: in Learning the port **learns MAC addresses** from received frames (without forwarding them) to prepare its MAC table.

### 2. STP timers

- **Hello timer**: how often the **root bridge** sends BPDUs, **2 seconds** by default. Other switches do not originate BPDUs: they **forward** the root's BPDUs, and **only out of their designated ports** (never root or non-designated ports), updating root cost, sending bridge ID, sending port ID. (At start-up every switch assumes it is root and sends BPDUs out of all interfaces; after convergence only the root originates them.)
- **Forward delay**: length of **each** of the Listening and Learning states, **15 seconds** by default, so **30 seconds** in total to reach Forwarding.
- **Max Age**: **20 seconds** by default. How long an interface waits to change the topology after ceasing to receive BPDUs. Root and non-designated ports expect BPDUs; each received BPDU resets the timer to 20. If it reaches 0, the switch re-evaluates its choices (root bridge, root/designated/non-designated ports). A non-designated port that becomes designated or root then goes through Listening (15 s) and Learning (15 s): **up to 50 seconds** from failure to forwarding.
- A Forwarding port can move **directly** to Blocking (no loop risk), but a Blocking port can never move directly to Forwarding.
- The timers configured on the **root bridge** determine the timers for all switches, even if configured differently.

### 3. The BPDU (Bridge Protocol Data Unit)

- Destination MAC of **PVST+ (Cisco) BPDUs: 0100.0ccc.cccd**. Standard (non-Cisco) STP: **0180.c200.0000**. Jeremy recommends remembering both.
- PVST (older) only supports ISL trunk encapsulation; **PVST+** supports 802.1Q (when Jeremy says PVST he means PVST+).
- Fields: Protocol Identifier (always 0x0000), Protocol Version Identifier (0 for classic STP, another value for Rapid STP in Day 22), BPDU Type (0x00 = configuration BPDU), Flags (signal topology changes), **Root Identifier** (priority + extended system ID = VLAN ID + root MAC), **Root Path Cost** (0 on the root), **Bridge Identifier** (same as Root Identifier on the root bridge), **Port Identifier** (e.g. 0x8002: 0x80 = 128 = default port priority, 02 = port number), **Message Age** (0 at the root, +1 per switch it passes through, subtracted from Max Age on receipt), then Max Age, Hello Time, Forward Delay.
- No need to memorise the BPDU for the CCNA, apart from the destination MACs and reading the Port ID.

### 4. STP Toolkit (optional features)

In video 039 Jeremy presents PortFast and BPDU Guard, then names Root Guard and Loop Guard (and UplinkFast, BackboneFast, not to be studied). The four videos below detail each tool; Cisco expects you to know PortFast, BPDU Guard, BPDU Filter, Root Guard and Loop Guard.

#### 4.1 PortFast (video 040)

- **Problem**: a host connected to a port goes up/up but its frames are dropped for **30 seconds** (15 s Listening + 15 s Learning). On a real switch the link light blinks **amber** during that time, then turns green. The wait is unnecessary: no Layer 2 loop is possible between a switch and a PC (only switches flood frames).
- **Solution**: PortFast moves the port **immediately to Forwarding** when enabled, bypassing Listening and Learning.
- **Enable only on ports connected to end hosts** (or a router): on a port to another switch it can cause a temporary loop. IOS warning: "PortFast should only be enabled on ports connected to a single host. Connecting hubs, concentrators, switches, bridges... can cause temporary bridging loops. Use with CAUTION".
- Two methods: `spanning-tree portfast` on the interface (active only in **non-trunking mode**: "will only have effect when the interface is in a non-trunking mode"); `spanning-tree portfast default` globally, which enables PortFast on **all access ports** (not trunks, despite the warning saying "all interfaces"). You can then disable it per port with `spanning-tree portfast disable`.
- **PortFast on a trunk**: only per interface with `spanning-tree portfast trunk`, useful for a virtualisation server (VMs in different VLANs) or a router-on-a-stick (a router does not flood frames).
- **PortFast edge / network**: two modes; *edge* is the CCNA one, *network* is for Bridge Assurance (not a CCNA topic). Modern IOS automatically adds the **EDGE** keyword to the running-config (`spanning-tree portfast edge`, `edge trunk`, `edge default`); both forms are equivalent. Exception: `spanning-tree portfast disable` does not use EDGE. Packet Tracer does not support the EDGE keyword.
- Verification: `show spanning-tree interface g0/1 detail` shows "The port is in the portfast edge mode" ("by default" if enabled globally, "portfast edge trunk mode" on a trunk). `show running-config interface g0/1` (not in Packet Tracer) shows that interface's config only.

#### 4.2 BPDU Guard and BPDU Filter (video 041)

- A PortFast port **keeps sending BPDUs** every 2 seconds (the PC ignores them) and STP is not disabled. If it **receives** a BPDU it reverts to a regular STP port. "Bob from Accounting" example: he plugs his own switch into the wall jack; if it has a lower bridge ID it becomes root bridge and changes the topology (SW1-SW2 link blocked, less efficient paths to the router).
- **BPDU Guard**: the port keeps sending BPDUs, but if it **receives one** it enters the **err-disabled** state (no more data or BPDUs). Configurable separately from PortFast, but usually used together. Messages: "Received BPDU on port GigabitEthernet0/1 with BPDU Guard enabled. Disabling port.", "bpduguard error detected on G0/1, putting G0/1 in err-disable state". On a real switch the link light turns **solid amber** and stays on even with the cable unplugged. ErrDisable is also triggered by other violations seen later: power policing, Port Security, DAI (Dynamic ARP Inspection).
- Configuration: `spanning-tree bpduguard enable` on the interface; `spanning-tree portfast bpduguard default` globally (optional EDGE keyword), which enables it on **all PortFast-enabled ports** (not "all access ports": a difference that can be tested); `spanning-tree bpduguard disable` to exclude a port.
- **Re-enabling an err-disabled port**: first **fix the underlying issue** (otherwise it is disabled again). Manual: `shutdown` then `no shutdown`. Automatic: **ErrDisable Recovery**, disabled by default, default timer **300 seconds (5 minutes)**. `show errdisable recovery` lists the causes (arp-inspection, bpduguard...) and pending ports; `errdisable recovery cause bpduguard` enables it for BPDU Guard; `errdisable recovery interval <s>` changes the delay (you still have to enable the cause).
- **BPDU Filter**: a port to an end host sends BPDUs needlessly (a little bandwidth and CPU, and above all STP topology information sent to user devices). BPDU Filter **stops the port sending BPDUs**; unlike BPDU Guard it does not disable the port on receipt. Its behaviour **depends on how it is configured**:
  - `spanning-tree bpdufilter enable` on the interface: sends no BPDUs **and ignores received BPDUs** = STP disabled on the port. **Use with caution**: on the wrong port, **permanent** loop and broadcast storm.
  - `spanning-tree portfast bpdufilter default` globally: activated on all PortFast ports; the port sends no BPDUs, but **if it receives one, PortFast and BPDU Filter are disabled** and it operates as a normal STP port ("best of both worlds"). `spanning-tree bpdufilter disable` to exclude a port.
- Jeremy's recommendation: enable BPDU Filter **only globally**. Combined with BPDU Guard on the same port: if BPDU Filter is global and a BPDU arrives, BPDU Filter is disabled and BPDU Guard err-disables the port; if BPDU Filter is per-port, the BPDU is ignored and **BPDU Guard has no effect**.

#### 4.3 Root Guard (video 042)

- **Root bridge selection** should not be random. Criteria: **optimal traffic flow** (minimise latency and congestion; PCs mostly talk to the router/WAN, so the root should be the switch connected to the router, e.g. SW1) and **stability/reliability** (the most advanced, reliable switch). With a poor root (SW3), SW2's traffic detours SW2→SW3→SW1; added latency is negligible (under a millisecond), the real issue is **congestion** on the SW3-SW1 link (frames wait, some may be dropped).
- Within your own LAN you control the root by setting its **priority to 0** (bridge ID = 0 + VLAN ID, PVST+ always adds the VLAN ID). But if you connect to switches outside your control (example: a service provider offering Metro Ethernet to a customer, in a MAN), a switch with priority 0 and a **lower MAC** (SW6, 5254.0018... vs 5254.001a...) takes the root role and breaks the provider's topology (SW1-SW3 and SW2-SW3 blocked, frames detour through the customer LAN).
- **Root Guard** stops a port accepting **superior BPDUs** (claiming a better root bridge ID): the port enters the **broken (BKN), Root Inconsistent (ROOT_Inc)** state, it cannot forward or receive frames (it stays up/up: STP blocks it). Message: "Root guard blocking port". Both ends of the link are then "designated" (special case: normally only one designated port per link).
- Configuration: `spanning-tree guard root` on the interface, **no global command** (not a feature to enable everywhere). Configure on ports **toward switches outside your control** (SW2 G0/2, SW3 G0/2 on the provider side). The **customer** should not configure it on its ports toward the provider, or its links would be blocked.
- **Automatic recovery**: nothing to do in the CLI. The superior BPDUs must stop (the provider asks the customer to raise SW6's priority, e.g. to 4096 → 4097 with the VLAN); once the BPDU ages out (**Max Age 20 s**) the port is "unblocked" and the network converges with SW1 as root.

#### 4.4 Loop Guard (video 043)

- Protects against a port that **unexpectedly stops receiving BPDUs** (software bug on a neighbour, or a **unidirectional link**).
- **Unidirectional link**: data flows in one direction only. Layer 1 cause: damaged cable, faulty connector or transceiver (SFP, small form-factor pluggable). More common on **fiber optic** (two separate fibers Tx→Rx; if one fiber is damaged without the devices detecting it, the interface stays up/up while communication only works one way; fiber snaps if bent too far). If the problem is detected, the whole link goes down, no unidirectional link.
- **The STP problem**: SW3 G0/1 is non-designated (Blocking) because it receives superior BPDUs from SW2. If SW2's BPDUs stop arriving, when **Max Age** expires SW3 G0/1 becomes designated and starts forwarding; SW2 ignores SW3's inferior BPDUs; both ports Forwarding → **loop** SW1→SW3→SW2 for broadcast frames.
- **Loop Guard**: when a protected port's Max Age reaches 0, instead of becoming designated it enters **broken (BKN), Loop Inconsistent (LOOP_Inc)**. The port stays up/up. Recovery is **automatic** as soon as BPDUs return (status back to Blocking).
- Configuration: `spanning-tree guard loop` on the interface; `spanning-tree loopguard default` globally (all ports) then `spanning-tree guard none` to exclude a port. Enable on **root and non-designated ports** (those that should receive BPDUs).
- **Loop Guard and Root Guard are mutually exclusive** (opposite purposes: Root Guard stops a designated port becoming root, Loop Guard stops a root/non-designated port becoming designated). Configuring one on a port disables the other; the **more specific command takes effect** (interface over global), a general IOS rule also true for PortFast, BPDU Guard and BPDU Filter.

### 5. Basic STP configuration (video 039)

- **Mode**: `spanning-tree mode {mst | pvst | rapid-pvst}`. MST not a CCNA topic; PVST = classic per-VLAN STP; Rapid-PVST = improved version (Day 22), **default on modern Cisco switches**.
- **Root bridge**: `spanning-tree vlan <n> root primary` sets the priority to **24576**, or **4096 less** than the current lowest priority if another switch is already below 24576. The running-config actually shows `spanning-tree vlan 1 priority 24576`. `spanning-tree vlan <n> root secondary` sets the priority to **28672** (next root if the primary fails). You can also use `spanning-tree vlan <n> priority <value>` directly (increments of 4096); the `root` command saves remembering the increments.
- **Load balancing**: with PVST+ configuration is **per VLAN**. A different root per VLAN blocks different links in each VLAN instead of leaving the same link idle everywhere.
- **Port settings**, per VLAN: `spanning-tree vlan <n> cost <1-200000000>` (cost: FastEthernet 19, GigabitEthernet 4; main criterion for the root port, tiebreaker for designated/non-designated) and `spanning-tree vlan <n> port-priority <0-224, increments of 32>` (first half of the Port ID, final tiebreaker for the root port).

### 6. Exam traps

- **Forward delay = 15 s for each state**, not 15 s total: 30 s for Listening + Learning, **50 s** with Max Age (20 s).
- Blocking **receives** BPDUs but does not forward them and does not learn MACs; Learning learns MACs but does not forward traffic.
- BPDUs are only forwarded out of **designated ports**.
- Destination MAC: **0100.0ccc.cccd** (PVST+) vs **0180.c200.0000** (standard STP).
- Port ID 0x8002 → priority **128** (0x80), port 2.
- `spanning-tree portfast default` → **all access ports**; `spanning-tree portfast bpduguard default` → **all PortFast-enabled ports**. Note the syntax difference: `bpduguard enable` on the interface, but `portfast bpduguard default` globally.
- BPDU Guard err-disables the port (manual shut/no shut or ErrDisable Recovery, 5 min default); Root Guard and Loop Guard put the port in **broken** (BKN) with **automatic** recovery.
- Per-port BPDU Filter = STP disabled on the port (permanent loop possible); global BPDU Filter disables itself when a BPDU arrives.
- Root Guard: no global command. Root Guard and Loop Guard cannot be active together on a port.
- `root primary` = 24576 (or 4096 below the existing minimum); `root secondary` = 28672.
- Jeremy recommends **leaving the timers at default**: they were chosen for a reason.

### 7. IOS commands

```
Switch(config)# spanning-tree mode pvst                  ! classic per-VLAN STP (modern default: rapid-pvst)
Switch(config)# spanning-tree vlan 1 root primary        ! priority 24576 (or existing minimum - 4096)
Switch(config)# spanning-tree vlan 1 root secondary      ! priority 28672
Switch(config)# spanning-tree vlan 1 priority 24576      ! what is actually written to the running-config
Switch(config-if)# spanning-tree vlan 1 cost 100         ! port cost in this VLAN (1 to 200000000)
Switch(config-if)# spanning-tree vlan 1 port-priority 240 ! port priority (0-224 in steps of 32 per video 039; 240 accepted in the lab)
Switch(config-if)# spanning-tree portfast                ! PortFast on this port (active in access mode only; = portfast edge)
Switch(config-if)# spanning-tree portfast trunk          ! PortFast on a trunk (ROAS router, VM server)
Switch(config-if)# spanning-tree portfast disable        ! exclude this port after global enable
Switch(config)# spanning-tree portfast default           ! PortFast on all access ports
Switch(config-if)# spanning-tree bpduguard enable        ! BPDU Guard on this port
Switch(config-if)# spanning-tree bpduguard disable       ! exclude this port
Switch(config)# spanning-tree portfast bpduguard default ! BPDU Guard on all PortFast-enabled ports
Switch(config-if)# spanning-tree bpdufilter enable       ! per-port BPDU Filter: STP disabled on the port (caution)
Switch(config-if)# spanning-tree bpdufilter disable      ! exclude this port
Switch(config)# spanning-tree portfast bpdufilter default ! BPDU Filter on all PortFast-enabled ports (recommended)
Switch(config-if)# spanning-tree guard root              ! Root Guard (no global version)
Switch(config-if)# spanning-tree guard loop              ! Loop Guard on this port
Switch(config)# spanning-tree loopguard default          ! Loop Guard on all ports
Switch(config-if)# spanning-tree guard none              ! remove Root/Loop Guard from the port
Switch(config)# errdisable recovery cause bpduguard      ! automatic recovery after BPDU Guard
Switch(config)# errdisable recovery interval 300         ! recovery delay in seconds (default 300)
Switch(config-if)# shutdown                              ! then no shutdown: manual recovery of an err-disabled port
Switch# show spanning-tree                               ! root, bridge ID, role/state of each port, BKN ROOT_Inc / LOOP_Inc
Switch# show spanning-tree vlan 1                        ! one VLAN only
Switch# show spanning-tree interface g0/1 detail         ! PortFast, BPDU Guard, Loop Guard, BPDUs sent/received
Switch# show errdisable recovery                         ! enabled causes, timer, pending ports
Switch# show interfaces g0/1                             ! err-disabled status
Switch# show running-config interface g0/1               ! that interface's config only (not in Packet Tracer)
```

### 8. The lab (video 044, Configuring STP PVST+)

Goal: check the STP topology, configure per-VLAN load balancing, manipulate port cost and priority, enable PortFast and BPDU Guard. Four switches SW1-SW4, FastEthernet links, VLANs 1 and 2.

1. **Current topology**: `show spanning-tree` on each switch. SW1 is not root (Root ID MAC ≠ Bridge ID), its F0/3 is the root port. SW2: "This bridge is the root", all ports designated/Forwarding, in both VLAN 1 and VLAN 2 (without configuration, same root and same roles in each VLAN). SW3: F0/2 root port (directly connected, all links FastEthernet), F0/1 designated. SW4: F0/1 root port, F0/2 Blocking with role **"Altn" (alternate = non-designated)**.
2. **Load balancing**: on SW1, `spanning-tree vlan 1 root primary` and `spanning-tree vlan 2 root secondary`; on SW2, `spanning-tree vlan 1 root secondary` and `spanning-tree vlan 2 root primary`. Always include the VLAN (PVST+ configures per VLAN). Check with `do show spanning-tree`: SW2 remains root in VLAN 2, but in VLAN 1 its F0/3 becomes root port; SW1 is root in VLAN 1 (all ports designated) and keeps F0/3 as root port in VLAN 2.
3. **Cost**: on SW4, `show spanning-tree vlan 1` confirms F0/2 as root port (lowest cost). `interface f0/2`, `spanning-tree vlan 1 cost 100` (over 5 times the current cost): F0/2 goes Blocking, **F0/1 becomes root port** (cost is the first criterion).
4. **Port-priority**: on SW1, `interface f0/1`, `spanning-tree vlan 1 port-priority 240` (highest number = lowest priority). On SW1 the Prio.Nbr column shows 240. On SW3, F0/1 **remains root port**: sender Port ID is the **last** tiebreaker, after cost (19 vs 38) and sender bridge ID.
5. **PortFast + BPDU Guard**: enable "Show Link Lights" (Options, Preferences). Delete and recreate the PC1-SW3 F0/3 link: light **orange for ~30 s**. `interface f0/3`, `spanning-tree portfast`, `spanning-tree bpduguard enable`. Reconnect: light **green right away**. Connect F0/3 to SW4 with a **crossover cable**: on receiving a BPDU the port is shut down, light **red**. Reconnect PC1 (straight-through cable) then `shutdown` / `no shutdown` to re-enable. Same configuration on SW4 F0/3.

Boson NetSim preview (ENCOR lab "PVST Load Balancing", CCNP level because STP configuration is not in the CCNA exam topics list): VTP, trunks, VLANs, primary/secondary root per VLAN group (1-3 and 4-6), documenting bridge IDs, root ports, designated/alternate ports.

### 9. The quiz (video 039: questions 7 to 10, continuing Day 20's questions 1 to 6, plus one Boson ExSim question)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Q7. VLANs 10 and 20, SW3 root by default. SW1 primary for VLAN 10 and secondary for VLAN 20; SW2 the opposite: which commands? | SW1: `spanning-tree vlan 10 root primary`, `spanning-tree vlan 20 root secondary`. SW2: `spanning-tree vlan 20 root primary`, `spanning-tree vlan 10 root secondary` | Each switch is root for one VLAN and backup root (second-lowest priority) for the other: load balancing across links. |
| Q8. A PC connected to a switch cannot reach the network for about half a minute. Two fixes? | **A** PortFast on the port and **C** reduce the Forward delay timer | PortFast bypasses Listening/Learning; Forward delay sets the length of those states. Hello (B) and Max Age (D) play no part. Jeremy recommends leaving timers at default. |
| Q9. STP port ID 0x8002: port priority? | **C, 128** | The first half of the Port ID, 0x80, is the priority = 128 decimal. 80, 32 and 224 are wrong. |
| Q10. Make sure no Layer 2 loop occurs if a user connects a switch to a switch port: which feature? | **D, BPDU Guard** | It shuts the interface down on receiving a BPDU; enable it on PortFast ports to end hosts. PortFast creates the risk, Loop Guard and Root Guard have other roles. |
| Boson ExSim. `spanning-tree portfast default` in global config on SwitchA: which ports use PortFast? | **D, all access ports** | PortFast can be enabled globally (A wrong); it does not activate on trunks (B, C wrong). Boson adds: 30 s by default, up to 50 s if PAgP is enabled (Day 23). |
