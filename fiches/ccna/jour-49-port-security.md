# CCNA Day 49 : Port Security / Sécurité des ports

> Source : Jeremy's IT Lab, « Free CCNA | Port Security | Day 49 » (34 min, vidéo n°99 de la playlist, cours) et « Free CCNA | Port Security | Day 49 Lab » (17 min, vidéo n°100, lab). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

Sujet d'examen 5.7 : configurer les fonctions de sécurité de couche 2 : **DHCP snooping, ARP inspection, port security**. Cette vidéo couvre port security ; les deux autres suivent.

### 1. Qu'est-ce que port security ?

- Fonction de sécurité des switches Cisco qui permet de contrôler **quelles adresses MAC source** sont autorisées à entrer sur un port de switch, et **combien** d'adresses MAC sont autorisées. Configurée **par interface** (port et interface désignent la même chose).
- Si une trame avec une MAC source non autorisée entre sur le port, une **action** est prise. Action par défaut : placer l'interface en état **err-disabled**, l'équivalent d'un arrêt de l'interface : plus aucun trafic envoyé ou reçu.
- Exemple : PC1 (MAC A.A.A) sur G0/1 de SW1, seule A.A.A autorisée. L'utilisateur branche son portable PC2 (B.B.B) à la place : G0/1 passe en err-disabled. S'il rebranche PC1, l'interface reste err-disabled : PC1 ne communique plus non plus.
- Par défaut, **une seule adresse MAC** autorisée. On peut la configurer **manuellement** ; sinon le switch autorise la **première MAC source** qui entre sur l'interface (apprentissage dynamique). On peut augmenter le **maximum**.
- Cas où il faut plus d'une MAC : téléphone IP relié à SW1 et PC1 relié au téléphone : deux MAC source. Avec un maximum de 2 appris dynamiquement, phone1 puis PC1 sont ajoutés ; un troisième appareil déclenche l'arrêt du port. Une **combinaison** manuel + dynamique est possible (C.C.C configurée, A.A.A apprise).

### 2. Pourquoi utiliser port security ?

- Empêcher qu'un appareil non autorisé branché sur un port accède au réseau. Limite : l'**usurpation d'adresse MAC** (*MAC address spoofing*) est simple ; port security n'est pas une solution parfaite.
- Souvent plus utile : **limiter le nombre de MAC** par interface. Rappel de l'attaque DHCP starvation du lab du jour 48 : des milliers de MAC usurpées épuisent le pool DHCP ; de plus la **table MAC du switch** peut se remplir, et le switch, ne pouvant plus apprendre, **inonde** (*flood*) tous les paquets. Port security protège contre ces attaques.

### 3. Configuration de base et état par défaut

- `switchport port-security` sur une interface est **rejeté** si le port est **dynamique** (`Command rejected: GigabitEthernet0/1 is a dynamic port`). Par défaut le mode administratif est **dynamic auto** (DTP). Port security s'active sur des ports **access ou trunk configurés statiquement** (`switchport mode access` ou `switchport mode trunk`) ; dynamic auto et dynamic desirable ne sont pas permis.
- `show port-security interface g0/1` : Port Security **Enabled**, Port Status **Secure-up** (activé et interface up), Violation Mode **Shutdown** (défaut), Aging Time **0 mins** (les adresses n'expirent jamais), Aging Type **Absolute**, SecureStatic Address Aging **Disabled**, Maximum MAC Addresses **1**, Total 0, Configured 0, Sticky 0, Last Source Address:Vlan 0000.0000.0000:0, Security Violation Count 0.
- Après un ping de PC1 : Total MAC Addresses 1 (maximum atteint), Last Source Address = MAC de PC1, VLAN 1.
- Après un ping de PC2 : Port Status **Secure-shutdown** (`show interfaces status` indique **err-disabled**), Total MAC Addresses remis à **0** (l'adresse apprise dynamiquement est effacée à l'arrêt du port), Last Source Address = B.B.B, Security Violation Count **1**.

### 4. Réactiver une interface désactivée par port security

- **Étape 1, toujours : débrancher l'appareil non autorisé.** Sinon : avec une MAC configurée manuellement, l'interface retombe en err-disabled ; avec une MAC apprise dynamiquement (effacée à l'arrêt), la MAC de l'intrus peut devenir la nouvelle adresse sécurisée.
- **Manuellement** : `shutdown` puis `no shutdown` sur l'interface. Le port revient en secure-up, la dernière adresse source est effacée et le compteur de violations est **remis à 0** (en mode shutdown, le compteur ne dépasse donc pas 1).
- **ErrDisable recovery** : réactivation automatique après un délai. `show errdisable recovery` liste toutes les causes possibles d'err-disable (longue liste) ; par défaut la récupération est **désactivée pour toutes**. La cause de port security est **psecure-violation** ; timer par défaut **300 secondes** (toutes les 5 minutes, les interfaces err-disabled dont la cause est activée sont réactivées). `errdisable recovery cause psecure-violation` l'active ; `errdisable recovery interval 180` règle le délai (la vidéo montre une interface qui sera réactivée dans 149 secondes).

### 5. Les trois modes de violation

| Mode | Trafic non autorisé | Interface | Syslog / SNMP | Compteur de violations |
| :--- | :--- | :--- | :--- | :--- |
| **Shutdown** (défaut) | Port en **err-disabled** | Désactivée | **Un seul** message Syslog et/ou SNMP à la désactivation, pas d'autres ensuite | Mis à **1**, remis à 0 à la réactivation |
| **Restrict** | **Jeté** (*discarded*) | Reste up ; les MAC autorisées continuent de passer | Message Syslog et/ou SNMP **à chaque** MAC non autorisée détectée | **+1 par trame** non autorisée |
| **Protect** | **Jeté silencieusement** | Reste up | **Aucun** message | **Non incrémenté** |

- Démonstration restrict : `switchport port-security mac-address <MAC PC1>` + `switchport port-security violation restrict` ; pings de PC2 : messages Syslog de violation, violation count **12**, port status secure-up.
- Démonstration protect : même configuration avec `violation protect` ; pings de PC2 échouent, pas de Syslog, compteur **0**, secure-up.

### 6. Vieillissement des adresses MAC sécurisées (*secure MAC address aging*)

- **Adresses MAC sécurisées** (*secure MAC addresses*) : apprises dynamiquement ou configurées statiquement sur un port avec port security. Par défaut **pas de vieillissement** (aging time 0) : permanentes sauf suppression manuelle ou arrêt/réactivation du port.
- `switchport port-security aging time <minutes>` configure le timer. Type par défaut : **absolute** : le timer démarre à l'apprentissage et l'adresse est supprimée à expiration **même si des trames continuent d'arriver** ; elle peut être réapprise immédiatement.
- Type **inactivity** : le timer est **réinitialisé à chaque trame** reçue de cette MAC (comme le vieillissement MAC classique). `switchport port-security aging type {absolute | inactivity}`.
- Par défaut seules les adresses **dynamiques** vieillissent. `switchport port-security aging static` fait aussi vieillir les adresses **statiques** (la commande est retirée de la running-config et l'adresse de la table MAC).
- Exemple vidéo : aging time 30, type inactivity, aging static ; `show port-security interface g0/1` affiche Aging Time 30 mins, Aging Type Inactivity, SecureStatic Address Aging Enabled.
- `show port-security` : vue d'ensemble : interfaces avec port security, max et nombre courant d'adresses sécurisées, compteur de violations, action.

### 7. Adresses MAC sécurisées « sticky »

- `switchport port-security mac-address sticky` : les MAC apprises dynamiquement sont **ajoutées à la running-config** sous la forme `switchport port-security mac-address sticky <MAC>`.
- Elles **ne vieillissent jamais**, même avec aging static. Mais elles sont dans la **running-config**, pas la startup-config : il faut sauvegarder (`write memory`) sinon elles sont perdues au redémarrage.
- À l'activation, toutes les MAC dynamiques courantes sont **converties en sticky** ; à la désactivation, les sticky redeviennent dynamiques. Sticky = façon de configurer des adresses statiques sans les taper.
- **Table MAC** : les adresses sécurisées y figurent comme les autres. Sticky et statiques ont le type **STATIC** ; les dynamiques non sticky ont le type **DYNAMIC**. `show mac address-table secure` affiche les adresses sécurisées.

### 8. Pièges d'examen

- `switchport port-security` est **rejeté sur un port dynamic auto** : erreur fréquente. Configurer d'abord `switchport mode access` ou `trunk`.
- **Shutdown** est le mode par défaut ; apprendre les actions de chaque mode (restrict = jette + Syslog/SNMP + compteur ; protect = jette seulement).
- Débrancher l'intrus **ne réactive pas** l'interface : il faut `shutdown`/`no shutdown` ou errdisable recovery. Mais le débrancher est toujours la première étape.
- Les adresses **sticky** sont de type STATIC dans la table MAC et dans la running-config, mais elles ont été **apprises dynamiquement**.
- En mode restrict, un **SNMP trap** est envoyé, pas un **SNMP Get** (le Get va du manager vers l'agent).
- Maximum par défaut **1** ; aging time par défaut **0** ; type par défaut **absolute** ; errdisable recovery par défaut **désactivé**, intervalle **300 s**.

### 9. Commandes IOS

```
SW1(config)# interface g0/1
SW1(config-if)# switchport mode access                       ! obligatoire (access ou trunk statique) avant port security
SW1(config-if)# switchport port-security                     ! active port security avec les réglages par défaut
SW1(config-if)# switchport port-security maximum 4           ! nombre maximal d'adresses MAC autorisées (défaut 1)
SW1(config-if)# switchport port-security mac-address aaaa.aaaa.aaaa   ! adresse MAC sécurisée statique
SW1(config-if)# switchport port-security mac-address sticky  ! apprentissage sticky : MAC apprises ajoutées à la running-config
SW1(config-if)# switchport port-security violation {shutdown | restrict | protect}   ! mode de violation (défaut shutdown)
SW1(config-if)# switchport port-security aging time 30       ! vieillissement en minutes (défaut 0 = jamais)
SW1(config-if)# switchport port-security aging type {absolute | inactivity}   ! type de vieillissement (défaut absolute)
SW1(config-if)# switchport port-security aging static        ! fait aussi vieillir les adresses statiques
SW1(config-if)# shutdown
SW1(config-if)# no shutdown                                  ! réactivation manuelle d'un port err-disabled
SW1(config)# errdisable recovery cause psecure-violation     ! récupération automatique des violations port security
SW1(config)# errdisable recovery interval 180                ! intervalle de récupération en secondes (défaut 300)
SW1# show interfaces g0/1 switchport                         ! mode administratif (dynamic auto / static access)
SW1# show port-security interface g0/1                       ! état, mode de violation, timers, compteurs, dernière MAC source
SW1# show port-security                                      ! vue d'ensemble des ports avec port security
SW1# show errdisable recovery                                ! causes, état de la récupération, timer, interfaces en attente
SW1# show interfaces status                                  ! statut err-disabled
SW1# show mac address-table secure                           ! adresses MAC sécurisées (sticky/statique = STATIC)
SW1# write memory                                            ! sauvegarder les adresses sticky
```

### 10. Le lab : Port Security

- **Topologie** : PC1, PC2, PC3 sur F0/1-3 de SW1 ; SW1 relié à SW2 (G0/1 de SW2) ; R1 en 10.0.0.254. Un seul VLAN (VLAN 1). Certaines commandes du cours ne sont pas supportées dans Packet Tracer (errdisable recovery notamment).
- **SW1, F0/1-3** : mode shutdown (défaut), 1 MAC (défaut), sticky désactivé (défaut), aging time 1 heure :

```
SW1(config)# interface range f0/1 - 3
SW1(config-if-range)# switchport port-security aging time 60
SW1(config-if-range)# switchport port-security        ! rejeté : port dynamic auto (erreur fréquente)
SW1(config-if-range)# do show interfaces f0/1 switchport   ! Administrative Mode: dynamic auto
SW1(config-if-range)# switchport mode access
SW1(config-if-range)# switchport port-security        ! accepté
SW1(config-if-range)# do show port-security interface f0/1   ! Enabled, Shutdown, Aging Time 60 mins
```

- **SW2, G0/1** : mode restrict, maximum **4** (3 PC + SW1, dont la MAC est apprise via ses messages **CDP**), sticky :

```
SW2(config)# interface g0/1
SW2(config-if)# switchport port-security violation restrict
SW2(config-if)# switchport port-security maximum 4
SW2(config-if)# switchport port-security mac-address sticky
SW2(config-if)# switchport mode access                 ! trunk possible aussi, un seul VLAN ici
SW2(config-if)# switchport port-security
SW2(config-if)# do show port-security interface g0/1   ! Enabled, Restrict, Maximum 4
```

- **Vérifications** : `ping 10.0.0.254` depuis PC1, PC2, PC3. Sur SW2 : `do show port-security interface g0/1` : Total 4, Sticky 4 ; `do show run` : quatre lignes `switchport port-security mac-address sticky <MAC>` sur G0/1 ; `do show mac address-table` : les 4 adresses en type **STATIC** (sticky) ; `do show port-security` : max 4, courant 4, 0 violation, action restrict.
- **Violation sur SW2 (restrict)** : sur SW1, `interface vlan1`, `ip address 10.0.0.10 255.255.255.0`, `no shutdown`, puis `do ping 10.0.0.254` : échec, car la MAC source est celle de la SVI VLAN 1, inconnue de SW2. `show port-security interface g0/1` sur SW2 : toujours **secure-up**, compteur de violations incrémenté (pas de Syslog affiché : limite de Packet Tracer).
- **Violation sur SW1 (shutdown)** : changer la MAC de PC1 (onglet Config, FastEthernet0, dernier « 1 » remplacé par « A ») puis `ping 10.0.0.254` : échec. Sur SW1, messages Syslog d'arrêt de F0/1 ; `do show port-security interface f0/1` : **secure-shutdown**, violation count 1. Réactivation manuelle obligatoire (pas d'errdisable recovery dans Packet Tracer).

### 11. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| D'après `show port-security interface` (Total 4, Configured 1, Sticky 3), combien d'adresses sécurisées ont été apprises dynamiquement ? | **C** : 3 | 1 configurée n'est pas dynamique. Les 3 sticky sont dans la running-config et de type STATIC dans la table MAC, mais elles ont bien été **apprises dynamiquement**. |
| Que se passe-t-il lors d'une violation en mode restrict ? (deux réponses) | **B** : le trafic non autorisé est jeté ; **E** : le compteur de violations est incrémenté | Un message Syslog et un trap SNMP sont aussi envoyés, mais pas un SNMP **Get** (D) : les Get vont du manager vers l'agent. |
| Mode de violation protect : que fait SW1 à l'arrivée d'une trame non autorisée sur G0/1 ? | **A** : le trafic non autorisé est jeté | Pas d'err-disable, les trames autorisées passent, pas de Syslog/SNMP, compteur non incrémenté. |
| Qu'est-ce qui réactive une interface désactivée par port security ? (deux réponses) | **A** : `shutdown` puis `no shutdown` ; **B** : `errdisable recovery cause psecure-violation` en config globale | Débrancher l'appareil (C) est nécessaire avant, mais ne réactive pas l'interface à lui seul. |
| Que se passe-t-il à la saisie de `switchport port-security` sur G0/1 en mode administratif static access ? | **A** : la commande est acceptée | En dynamic auto elle serait rejetée. Port security exige un port access ou trunk configuré statiquement. |

---

## 🇬🇧 English version

Exam topic 5.7: configure Layer 2 security features: **DHCP snooping, ARP inspection, port security**. This video covers port security; the other two follow.

### 1. What is port security?

- A security feature of Cisco switches that controls **which source MAC addresses** are allowed to enter a switch port, and **how many**. Configured **per interface** (port and interface mean the same thing).
- If a frame with an unauthorized source MAC enters the port, an **action** is taken. Default action: place the interface in the **err-disabled** state, effectively shutting it down: no traffic sent or received.
- Example: PC1 (MAC A.A.A) on SW1's G0/1, only A.A.A allowed. The user plugs in his laptop PC2 (B.B.B) instead: G0/1 goes err-disabled. If he plugs PC1 back in, the interface is still err-disabled: PC1 cannot communicate either.
- By default, **one MAC address** is allowed. It can be configured **manually**; otherwise the switch allows the **first source MAC** that enters the interface (dynamic learning). The **maximum** can be increased.
- Case needing more than one MAC: an IP phone connected to SW1 with PC1 behind it: two source MACs. With a maximum of 2 learned dynamically, phone1 then PC1 are added; a third device triggers the shutdown. A **combination** of manual and dynamic is possible (C.C.C configured, A.A.A learned).

### 2. Why use port security?

- Prevent an unauthorized device plugged into a switch port from accessing the network. Limit: **MAC address spoofing** is simple; port security is not a perfect solution.
- Often more useful: **limiting the number of MACs** per interface. Recall the DHCP starvation attack of the Day 48 lab: thousands of spoofed MACs exhaust the DHCP pool; also the switch's **MAC address table** can fill up, and the switch, unable to learn, **floods** every packet. Port security protects against such attacks.

### 3. Basic configuration and defaults

- `switchport port-security` on an interface is **rejected** if the port is **dynamic** (`Command rejected: GigabitEthernet0/1 is a dynamic port`). Default administrative mode is **dynamic auto** (DTP). Port security works on **statically configured access or trunk** ports (`switchport mode access` or `switchport mode trunk`); dynamic auto and dynamic desirable are not allowed.
- `show port-security interface g0/1`: Port Security **Enabled**, Port Status **Secure-up** (enabled and interface up), Violation Mode **Shutdown** (default), Aging Time **0 mins** (addresses never age out), Aging Type **Absolute**, SecureStatic Address Aging **Disabled**, Maximum MAC Addresses **1**, Total 0, Configured 0, Sticky 0, Last Source Address:Vlan 0000.0000.0000:0, Security Violation Count 0.
- After a ping from PC1: Total MAC Addresses 1 (maximum reached), Last Source Address = PC1's MAC, VLAN 1.
- After a ping from PC2: Port Status **Secure-shutdown** (`show interfaces status` shows **err-disabled**), Total MAC Addresses reset to **0** (the dynamically learned address is cleared when the port is shut down), Last Source Address = B.B.B, Security Violation Count **1**.

### 4. Re-enabling an interface disabled by port security

- **Step 1, always: disconnect the unauthorized device.** Otherwise: with a manually configured MAC, the interface is disabled again; with a dynamically learned MAC (cleared on shutdown), the intruder's MAC may become the new secure MAC.
- **Manually**: `shutdown` then `no shutdown` on the interface. The port returns to secure-up, the last source address is erased and the violation counter is **reset to 0** (so in shutdown mode the counter never goes above 1).
- **ErrDisable recovery**: automatic re-enabling after a period. `show errdisable recovery` lists all possible err-disable reasons (a long list); by default recovery is **disabled for all**. The port security reason is **psecure-violation**; default timer **300 seconds** (every 5 minutes, err-disabled interfaces whose cause is enabled are re-enabled). `errdisable recovery cause psecure-violation` enables it; `errdisable recovery interval 180` sets the timer (the video shows an interface to be re-enabled in 149 seconds).

### 5. The three violation modes

| Mode | Unauthorized traffic | Interface | Syslog / SNMP | Violation counter |
| :--- | :--- | :--- | :--- | :--- |
| **Shutdown** (default) | Port placed in **err-disabled** | Disabled | **One** Syslog and/or SNMP message when disabled, none after | Set to **1**, reset to 0 when re-enabled |
| **Restrict** | **Discarded** | Stays up; authorized MACs keep working | Syslog and/or SNMP message **each time** an unauthorized MAC is detected | **+1 per** unauthorized frame |
| **Protect** | **Silently discarded** | Stays up | **No** messages | **Not incremented** |

- Restrict demo: `switchport port-security mac-address <PC1 MAC>` + `switchport port-security violation restrict`; pings from PC2: Syslog violation messages, violation count **12**, port status secure-up.
- Protect demo: same with `violation protect`; PC2's pings fail, no Syslog, counter **0**, secure-up.

### 6. Secure MAC address aging

- **Secure MAC addresses**: dynamically learned or statically configured on a port-security-enabled port. By default **no aging** (aging time 0): permanent unless manually deleted or the port is disabled then re-enabled.
- `switchport port-security aging time <minutes>` sets the timer. Default type: **absolute**: the timer starts when the address is learned and the address is removed when it expires **even if frames keep arriving**; it can be re-learned immediately.
- **Inactivity** type: the timer is **reset every time a frame** from that MAC is received (like regular MAC aging). `switchport port-security aging type {absolute | inactivity}`.
- By default only **dynamic** addresses age out. `switchport port-security aging static` makes **static** ones age too (the command is removed from the running-config and the address from the MAC table).
- Video example: aging time 30, type inactivity, aging static; `show port-security interface g0/1` shows Aging Time 30 mins, Aging Type Inactivity, SecureStatic Address Aging Enabled.
- `show port-security`: overview: interfaces with port security, max and current secure addresses, violation count, security action.

### 7. Sticky secure MAC addresses

- `switchport port-security mac-address sticky`: dynamically learned MACs are **added to the running-config** as `switchport port-security mac-address sticky <MAC>`.
- They **never age out**, even with static aging enabled. But they are in the **running-config**, not the startup-config: save (`write memory`) or they are lost on restart.
- When enabled, all current dynamic secure MACs are **converted to sticky**; when removed, sticky addresses become regular dynamic ones. Sticky = a way to configure static secure MACs without typing them.
- **MAC address table**: secure MACs appear like any other. Sticky and static ones have type **STATIC**; non-sticky dynamic ones have type **DYNAMIC**. `show mac address-table secure` shows the secure addresses.

### 8. Exam traps

- `switchport port-security` is **rejected on a dynamic auto port**: a common mistake. Configure `switchport mode access` or `trunk` first.
- **Shutdown** is the default mode; learn each mode's actions (restrict = discard + Syslog/SNMP + counter; protect = discard only).
- Unplugging the intruder **does not re-enable** the interface: `shutdown`/`no shutdown` or errdisable recovery is needed. But unplugging is always step 1.
- **Sticky** addresses are type STATIC in the MAC table and in the running-config, but they were **dynamically learned**.
- In restrict mode an **SNMP trap** is sent, not an **SNMP Get** (Get goes from manager to agent).
- Default maximum **1**; default aging time **0**; default type **absolute**; errdisable recovery **disabled** by default, interval **300 s**.

### 9. IOS commands

```
SW1(config)# interface g0/1
SW1(config-if)# switchport mode access                       ! required (static access or trunk) before port security
SW1(config-if)# switchport port-security                     ! enable port security with default settings
SW1(config-if)# switchport port-security maximum 4           ! maximum allowed MAC addresses (default 1)
SW1(config-if)# switchport port-security mac-address aaaa.aaaa.aaaa   ! static secure MAC address
SW1(config-if)# switchport port-security mac-address sticky  ! sticky learning: learned MACs added to running-config
SW1(config-if)# switchport port-security violation {shutdown | restrict | protect}   ! violation mode (default shutdown)
SW1(config-if)# switchport port-security aging time 30       ! aging in minutes (default 0 = never)
SW1(config-if)# switchport port-security aging type {absolute | inactivity}   ! aging type (default absolute)
SW1(config-if)# switchport port-security aging static        ! static addresses age out too
SW1(config-if)# shutdown
SW1(config-if)# no shutdown                                  ! manually re-enable an err-disabled port
SW1(config)# errdisable recovery cause psecure-violation     ! automatic recovery for port security violations
SW1(config)# errdisable recovery interval 180                ! recovery interval in seconds (default 300)
SW1# show interfaces g0/1 switchport                         ! administrative mode (dynamic auto / static access)
SW1# show port-security interface g0/1                       ! status, violation mode, timers, counters, last source MAC
SW1# show port-security                                      ! overview of port-security-enabled ports
SW1# show errdisable recovery                                ! reasons, recovery state, timer, interfaces waiting
SW1# show interfaces status                                  ! err-disabled status
SW1# show mac address-table secure                           ! secure MAC addresses (sticky/static = STATIC)
SW1# write memory                                            ! save sticky addresses
```

### 10. The lab: Port Security

- **Topology**: PC1, PC2, PC3 on SW1's F0/1-3; SW1 connected to SW2 (SW2's G0/1); R1 at 10.0.0.254. One VLAN (VLAN 1). Some lecture commands are not supported in Packet Tracer (errdisable recovery in particular).
- **SW1, F0/1-3**: shutdown mode (default), 1 MAC (default), sticky disabled (default), aging time 1 hour:

```
SW1(config)# interface range f0/1 - 3
SW1(config-if-range)# switchport port-security aging time 60
SW1(config-if-range)# switchport port-security        ! rejected: dynamic auto port (common mistake)
SW1(config-if-range)# do show interfaces f0/1 switchport   ! Administrative Mode: dynamic auto
SW1(config-if-range)# switchport mode access
SW1(config-if-range)# switchport port-security        ! accepted
SW1(config-if-range)# do show port-security interface f0/1   ! Enabled, Shutdown, Aging Time 60 mins
```

- **SW2, G0/1**: restrict mode, maximum **4** (3 PCs + SW1, whose MAC is learned from its **CDP** messages), sticky:

```
SW2(config)# interface g0/1
SW2(config-if)# switchport port-security violation restrict
SW2(config-if)# switchport port-security maximum 4
SW2(config-if)# switchport port-security mac-address sticky
SW2(config-if)# switchport mode access                 ! trunk is an option too, only one VLAN here
SW2(config-if)# switchport port-security
SW2(config-if)# do show port-security interface g0/1   ! Enabled, Restrict, Maximum 4
```

- **Verification**: `ping 10.0.0.254` from PC1, PC2, PC3. On SW2: `do show port-security interface g0/1`: Total 4, Sticky 4; `do show run`: four `switchport port-security mac-address sticky <MAC>` lines on G0/1; `do show mac address-table`: the 4 addresses with type **STATIC** (sticky); `do show port-security`: max 4, current 4, 0 violations, action restrict.
- **Violation on SW2 (restrict)**: on SW1, `interface vlan1`, `ip address 10.0.0.10 255.255.255.0`, `no shutdown`, then `do ping 10.0.0.254`: fails, because the source MAC is the VLAN 1 SVI's, unknown to SW2. `show port-security interface g0/1` on SW2: still **secure-up**, violation counter incremented (no Syslog shown: a Packet Tracer limitation).
- **Violation on SW1 (shutdown)**: change PC1's MAC (Config tab, FastEthernet0, last "1" changed to "A") then `ping 10.0.0.254`: fails. On SW1, Syslog messages for F0/1 going down; `do show port-security interface f0/1`: **secure-shutdown**, violation count 1. Manual re-enable required (no errdisable recovery in Packet Tracer).

### 11. The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| From `show port-security interface` output (Total 4, Configured 1, Sticky 3), how many secure MACs were dynamically learned? | **C**: 3 | The 1 configured is not dynamic. The 3 sticky ones are in the running-config and type STATIC in the MAC table, but they were **dynamically learned**. |
| What occurs on a violation in restrict mode? (select two) | **B**: unauthorized traffic is discarded; **E**: the violation counter is incremented | A Syslog message and SNMP trap are also sent, but not an SNMP **Get** (D): Gets go from manager to agent. |
| Protect violation mode: what does SW1 do when an unauthorized frame arrives on G0/1? | **A**: unauthorized traffic is dropped | No err-disable, authorized frames are forwarded, no Syslog/SNMP, counter not incremented. |
| What re-enables an interface disabled by port security? (select two) | **A**: `shutdown` then `no shutdown`; **B**: `errdisable recovery cause psecure-violation` in global config | Unplugging the device (C) should be done first, but alone it does not re-enable the interface. |
| What happens when `switchport port-security` is issued on G0/1 with administrative mode static access? | **A**: the command is accepted | With dynamic auto it would be rejected. Port security requires a statically configured access or trunk port. |
