# CCNA Day 34 : Standard ACLs / ACL standard

> Source : Jeremy's IT Lab, vidéo n°69 « Standard ACLs | Day 34 » (cours, 47 min) et vidéo n°70 « Standard ACLs | Day 34 Lab » (lab, 27 min) de la playlist. Fiche rédigée à partir des transcriptions le 6 octobre 2026. Les ACL affichées à l'écran dans les quiz Q1 à Q4 ne sont pas dans la transcription : seule la logique de la réponse est reprise.

## 🇫🇷 Version française

### 1. Qu'est-ce qu'une ACL ?

- Sujet d'examen **5.6** (*security fundamentals*) : configurer et vérifier des listes de contrôle d'accès (*Access Control Lists*). Seules les ACL **IPv4** sont exigées. Day 34 = ACL standard, Day 35 = ACL étendues.
- Usage principal (celui du cours) : **sécurité**, contrôler quels équipements accèdent à quelles parties du réseau. D'autres usages viendront plus tard.
- Une ACL agit comme un **filtre de paquets** (*packet filter*) : même si le routeur a une route vers la destination, l'ACL peut lui faire **jeter** le paquet. Critères : adresses IP source et destination, ports de couche 4 (pour le CCNA).
- Sur un schéma, un segment réseau peut être dessiné sans son switch : les PC sont bien reliés à un switch relié au routeur.

### 2. Logique de traitement

- Une ACL est configurée **en mode de configuration globale** et constituée d'une **séquence ordonnée d'ACE** (*Access Control Entries*). Créer l'ACL ne fait rien : il faut l'**appliquer à une interface**, **inbound** (paquets qui entrent) ou **outbound** (paquets qui sortent).
- Les entrées sont traitées **de haut en bas** ; **à la première correspondance, l'action est prise et le reste est ignoré**. L'ordre est donc essentiel : `permit 192.168.1.0/24` puis `deny 192.168.0.0/16` laisse passer 192.168.1.1 ; l'inverse le bloque.
- **Une seule ACL par interface et par direction** (une inbound + une outbound au maximum) ; en appliquer une seconde dans la même direction **remplace** la première.
- **Implicit deny** : un paquet qui ne correspond à aucune entrée est **jeté**, comme s'il y avait une entrée invisible `deny any` à la fin de **toute** ACL. Toujours y penser, sinon on bloque plus que prévu.
- Exemple de placement (ACL 1 : permit 192.168.1.0/24, deny 192.168.2.0/24, permit all) pour autoriser 192.168.1.0/24 et interdire 192.168.2.0/24 vers 10.0.1.0/24 :
  - **outbound sur G0/2 de R1** (côté 192.168.2.0/24) : inefficace, la requête de PC3 entre par G0/2 sans être vérifiée, et la réponse de SRV1 est permise.
  - **inbound sur G0/2 de R1** : bloque PC3 mais **trop restrictif** (192.168.2.0/24 ne joint plus aucun autre réseau).
  - **outbound sur G0/1 de R2** (vers 10.0.1.0/24) : **meilleur emplacement**, sans effet sur le reste du trafic.

### 3. Types d'ACL

| Type | Critères | Sous-types |
| :--- | :--- | :--- |
| **Standard** | **Adresse IP source uniquement** | Numérotées (**1 à 99** et **1300 à 1999**, plage « Standard IP »), nommées |
| **Extended** (Day 35) | IP source et/ou destination, ports source et/ou destination, etc. | Numérotées, nommées |

Le numéro 100, par exemple, n'est pas un numéro d'ACL standard. Les autres types d'ACL du tableau IOS ont chacun leur plage, pas à mémoriser.

### 4. ACL standard numérotées

- `access-list <n> {deny | permit} <ip> <wildcard>` : **masque générique** (*wildcard*), jamais un masque de sous-réseau.
- Trois écritures équivalentes pour un hôte /32 : `access-list 1 deny 1.1.1.1 0.0.0.0`, `access-list 1 deny 1.1.1.1` (le routeur comprend /32), `access-list 1 deny host 1.1.1.1` (ancienne méthode, toujours valable). Pour un /24, le wildcard `0.0.0.255` est obligatoire.
- `access-list 1 permit any` ≡ `access-list 1 permit 0.0.0.0 255.255.255.255` (0.0.0.0/0, toutes les adresses).
- `access-list 1 remark <texte>` : commentaire sans effet, comme une description d'interface, visible seulement dans la configuration.
- Le routeur **convertit** automatiquement `1.1.1.1 0.0.0.0` en `1.1.1.1` et `0.0.0.0 255.255.255.255` en `any`, et numérote les entrées **10, 20, 30…**
- Règle de placement : **une ACL standard s'applique le plus près possible de la destination** (le réseau dont on contrôle l'accès), sinon on bloque plus de trafic que voulu. Exemple : permit 192.168.1.1, deny 192.168.1.0 0.0.0.255, permit any, appliquée **outbound sur G0/2** (vers 192.168.2.0/24) plutôt qu'inbound sur G0/1. La réponse de PC3 à PC1 passe car aucune ACL ne filtre le retour.

### 5. ACL standard nommées

- `ip access-list standard <NOM>` (noter le **ip** devant) ouvre le **mode de configuration d'ACL nommée** ; chaque entrée s'y configure avec `[n°] {deny | permit} ...`. Sans numéro : 10, 20, 30… ; avec numéro, on contrôle l'ordre (ex. 5 puis 10). `remark` possible.
- Vérification : `show access-lists` (toutes les ACL), `show ip access-lists` (ACL IP seulement, même sortie ici), `show running-config | section access-list` (toute la section ; avec `| include access-list` on ne verrait que le nom des ACL nommées). Les numéros d'entrée ne sont pas affichés dans la config.
- Exemple sur R2 : `TO_10.0.2.0/24` (deny 192.168.1.0 0.0.0.255, permit any, outbound G0/2) et `TO_10.0.1.0/24` (deny 192.168.2.1, permit 192.168.2.0 0.0.0.255, permit 192.168.1.1, deny 192.168.1.0 0.0.0.255, permit any, outbound G0/1). Un ping de PC2 (192.168.1.2) vers SRV1 correspond à l'entrée 40 → deny.
- Curiosité IOS (hors examen) : le routeur peut **réordonner les entrées /32** dans `show ip access-lists` pour traiter plus vite, sans changer l'effet ; Packet Tracer ne le fait pas.

### 6. Pièges d'examen

- **Implicit deny** à la fin de toute ACL : un paquet sans correspondance est **jeté** (pas transmis au gateway, pas vérifié par une autre ACL, pas de « correspondance la plus spécifique »).
- Traitement **du premier au dernier**, pas du plus spécifique au moins spécifique (bonus Boson).
- Appliquer : `ip access-group`, **pas** `access-list`.
- Deux ACL appliquées dans la même direction sur une interface : **la dernière remplace** la précédente (quiz Q3).
- Une ACL appliquée au mauvais endroit peut n'avoir **aucun effet** : inbound sur G0/0 de R1 côté WAN, les pings sortent sans vérification et les réponses de SRV2 sont permises par `permit any` (quiz Q4).
- Plages des ACL standard : **1-99, 1300-1999**.

### 7. Commandes IOS

```
R1(config)# access-list 1 deny 1.1.1.1 0.0.0.0        ! ACL standard numérotée, un hôte (= deny 1.1.1.1 = deny host 1.1.1.1)
R1(config)# access-list 1 deny 192.168.1.0 0.0.0.255  ! un réseau /24 avec masque générique
R1(config)# access-list 1 permit any                  ! = permit 0.0.0.0 255.255.255.255
R1(config)# access-list 1 remark ## BLOCK BOB ##      ! commentaire, visible seulement dans la config
R2(config)# ip access-list standard BLOCK_BOB         ! ACL standard nommée, entre en mode de config d'ACL
R2(config-std-nacl)# 5 deny 1.1.1.1                   ! entrée avec numéro de séquence explicite
R2(config-std-nacl)# 10 permit any
R2(config-std-nacl)# remark ## BLOCK BOB ##
R1(config-if)# ip access-group 1 out                  ! applique l'ACL (numéro ou nom) in ou out
R1# show access-lists                                 ! toutes les ACL, numéros de séquence, compteurs de correspondances
R1# show ip access-lists                              ! ACL IP seulement
R1# show running-config | include access-list        ! lignes de config contenant access-list
R1# show running-config | section access-list        ! section complète (entrées des ACL nommées)
```

### 8. Le lab (vidéo n°70)

Objectif : OSPF entre R1 (172.16.1.0/24, 172.16.2.0/24) et R2 (192.168.1.0/24, 192.168.2.0/24) via 203.0.113.0/30, puis quatre ACL : numérotées sur R1, nommées sur R2.

1. **OSPF** : `router ospf 1`, `network 172.16.0.0 0.0.255.255 area 0`, `network 203.0.113.0 0.0.0.3 area 0` sur R1 (192.168.0.0 sur R2). Vérifier `show ip ospf interface`, `show ip ospf neighbor` (état FULL, tiret à la place du DR/BDR : lien série point-à-point), `show ip route`.
2. **R2, `TO_192.168.1.0/24`** (seuls PC1 et PC3 accèdent) : `permit 172.16.1.1`, `permit 172.16.2.1`, `deny any` (inutile vu l'implicit deny, mais bonne pratique pour la lisibilité) ; `interface g0/0`, `ip access-group TO_192.168.1.0/24 out`. Test : PC1 pinge SRV1 (les premiers pings peuvent échouer le temps d'ARP) ; PC2 reçoit **« destination host unreachable »** de 203.0.113.2 (R2).
3. **R2, `TO_192.168.2.0/24`** (172.16.2.0/24 interdit) : `deny 172.16.2.0 0.0.0.255`, `permit any` ; `interface g0/1`, `ip access-group TO_192.168.2.0/24 out`. PC1 → SRV2 OK, PC3 → SRV2 unreachable. `do show access-lists` affiche le **nombre de paquets correspondant** à chaque entrée.
4. **R1, ACL 1 et 2** (172.16.1.0/24 et 172.16.2.0/24 ne communiquent pas) : `access-list 1 deny 172.16.1.0 0.0.0.255`, `access-list 1 permit any` ; idem ACL 2 pour 172.16.2.0. `interface g0/1` → `ip access-group 1 out` ; `interface g0/0` → `ip access-group 2 out`.
5. Test avec `ping -t 172.16.2.1` sur PC1 (ping continu, `Ctrl+C` pour arrêter) et inversement : échec ; `do show access-lists` sur R1 montre les compteurs de deny qui augmentent.

Bonus NetSim (ACL practice lab 2) : 20 labs ACL dans NetSim. ACL 1 sur Router1, `access-list 1 deny 10.10.2.0 0.0.1.255` (couvre 10.10.2.0/24 et 10.10.3.0/24 en une entrée), `permit any`, appliquée **inbound** sur F0/0 (lien vers Router2) : Telnet et ping vers le loopback 1.1.1.1 fonctionnent depuis PC1, échouent depuis PC2 et PC3. ACL 2 `deny 10.10.1.0 0.0.0.255`, `permit any`, appliquée **outbound** sur F1/0 (côté VLAN1) : empêche un hôte distant d'**usurper** une adresse source de VLAN1 (anti-spoofing). Puis ACL 1 appliquée aussi **outbound** sur F0/0 pour empêcher les hôtes de Router1 de se faire passer pour VLAN2/VLAN3.

### 9. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quelle ACL, appliquée outbound sur G0/1 de R2, n'autorise que PC1 et PC4 vers 10.0.1.0/24 ? | **ACL 1** : entrée 10 permit PC1, entrée 20 permit PC4, implicit deny pour le reste | Les autres ACL affichées ne remplissent pas l'exigence. |
| Sur quelle interface et dans quel sens appliquer l'ACL pour contrôler l'accès à 10.0.2.0/24 ? | **G0/2 de R2, outbound** | Une ACL standard s'applique au plus près de la destination. |
| ACL 10 appliquée après une autre ACL sur la même interface, même sens : effet ? | **Le trafic de 10.0.0.0/24 est refusé** | Une seule ACL par interface et par direction ; la dernière appliquée remplace la précédente. |
| ACL (deny … puis permit any) appliquée inbound sur G0/0 de R1 : qui peut pinger SRV2 ? | **Tous les PC** | Les pings sortent par G0/0 sans vérification ; les réponses de SRV2 (10.0.2.100) entrent et correspondent à `permit any`. |
| Paquet sans correspondance dans l'ACL ? | **Il est jeté** | Implicit deny ; il n'est ni envoyé au gateway, ni vérifié par une autre ACL, ni traité par la correspondance la plus spécifique. |

Bonus Boson : les ACL sont traitées **de la première entrée à la dernière**, pas par spécificité.

---

## 🇬🇧 English version

### 1. What is an ACL?

- Exam topic **5.6** (security fundamentals): configure and verify Access Control Lists. Only **IPv4** ACLs are required. Day 34 = standard ACLs, Day 35 = extended ACLs.
- Main use (this course): **security**, controlling which devices can access which parts of the network. Other uses come later.
- An ACL acts as a **packet filter**: even if the router has a route to the destination, the ACL can make it **discard** the packet. Criteria: source and destination IP addresses, Layer 4 port numbers (for the CCNA).
- In a diagram, a network segment may be drawn without its switch: the PCs are really connected to a switch connected to the router.

### 2. ACL logic

- An ACL is configured in **global config mode** and made of an **ordered sequence of ACEs** (Access Control Entries). Creating it does nothing: it must be **applied to an interface**, **inbound** (packets entering) or **outbound** (packets exiting).
- Entries are processed **top to bottom**; **on the first match the action is taken and the rest is ignored**. Order is critical: `permit 192.168.1.0/24` then `deny 192.168.0.0/16` forwards 192.168.1.1; reversed, it is dropped.
- **One ACL per interface per direction** (one inbound + one outbound at most); applying a second one in the same direction **replaces** the first.
- **Implicit deny**: a packet that matches no entry is **dropped**, as if an invisible `deny any` sat at the end of **every** ACL. Always keep it in mind or you will block more than intended.
- Placement example (ACL 1: permit 192.168.1.0/24, deny 192.168.2.0/24, permit all) to allow 192.168.1.0/24 and block 192.168.2.0/24 toward 10.0.1.0/24:
  - **outbound on R1 G0/2** (192.168.2.0/24 side): useless, PC3's request enters G0/2 unchecked and SRV1's reply is permitted.
  - **inbound on R1 G0/2**: blocks PC3 but **too restrictive** (192.168.2.0/24 can no longer reach any other network).
  - **outbound on R2 G0/1** (toward 10.0.1.0/24): **best location**, no effect on other traffic.

### 3. ACL types

| Type | Criteria | Sub-types |
| :--- | :--- | :--- |
| **Standard** | **Source IP address only** | Numbered (**1 to 99** and **1300 to 1999**, "Standard IP" range), named |
| **Extended** (Day 35) | Source and/or destination IP, source and/or destination ports, etc. | Numbered, named |

Number 100, for instance, is not a standard ACL number. The other ACL types in the IOS chart each have their own range, no need to memorize.

### 4. Standard numbered ACLs

- `access-list <n> {deny | permit} <ip> <wildcard>`: a **wildcard mask**, never a subnet mask.
- Three equivalent ways for a /32 host: `access-list 1 deny 1.1.1.1 0.0.0.0`, `access-list 1 deny 1.1.1.1` (the router assumes /32), `access-list 1 deny host 1.1.1.1` (old method, still works). For a /24 the wildcard `0.0.0.255` is required.
- `access-list 1 permit any` ≡ `access-list 1 permit 0.0.0.0 255.255.255.255` (0.0.0.0/0, all addresses).
- `access-list 1 remark <text>`: a comment with no effect, like an interface description, shown only in the config.
- The router automatically **converts** `1.1.1.1 0.0.0.0` to `1.1.1.1` and `0.0.0.0 255.255.255.255` to `any`, and numbers entries **10, 20, 30…**
- Placement rule: **a standard ACL should be applied as close to the destination as possible** (the network whose access is controlled), otherwise more traffic than intended is blocked. Example: permit 192.168.1.1, deny 192.168.1.0 0.0.0.255, permit any, applied **outbound on G0/2** (toward 192.168.2.0/24) rather than inbound on G0/1. PC3's reply to PC1 passes because no ACL filters the return path.

### 5. Standard named ACLs

- `ip access-list standard <NAME>` (note the leading **ip**) enters **standard named ACL config mode**; each entry is configured there with `[seq] {deny | permit} ...`. Without a number: 10, 20, 30…; with a number you control the order (e.g. 5 then 10). `remark` is possible.
- Verification: `show access-lists` (all ACLs), `show ip access-lists` (IP ACLs only, same output here), `show running-config | section access-list` (whole section; `| include access-list` would only show the names of named ACLs). Entry numbers are not displayed in the config.
- Example on R2: `TO_10.0.2.0/24` (deny 192.168.1.0 0.0.0.255, permit any, outbound G0/2) and `TO_10.0.1.0/24` (deny 192.168.2.1, permit 192.168.2.0 0.0.0.255, permit 192.168.1.1, deny 192.168.1.0 0.0.0.255, permit any, outbound G0/1). A ping from PC2 (192.168.1.2) to SRV1 matches entry 40 → deny.
- IOS curiosity (not on the exam): the router may **re-order /32 entries** in `show ip access-lists` for faster processing, without changing the effect; Packet Tracer does not do this.

### 6. Exam traps

- **Implicit deny** at the end of every ACL: an unmatched packet is **dropped** (not forwarded to the gateway, not checked by another ACL, no "most specific match").
- Processed **first to last**, not most specific to least specific (Boson bonus).
- Apply with `ip access-group`, **not** `access-list`.
- Two ACLs applied in the same direction on one interface: **the last one replaces** the previous (quiz Q3).
- An ACL applied in the wrong place may have **no effect**: inbound on R1 G0/0 on the WAN side, pings exit unchecked and SRV2's replies are permitted by `permit any` (quiz Q4).
- Standard ACL ranges: **1-99, 1300-1999**.

### 7. IOS commands

```
R1(config)# access-list 1 deny 1.1.1.1 0.0.0.0        ! standard numbered ACL, one host (= deny 1.1.1.1 = deny host 1.1.1.1)
R1(config)# access-list 1 deny 192.168.1.0 0.0.0.255  ! a /24 network with wildcard mask
R1(config)# access-list 1 permit any                  ! = permit 0.0.0.0 255.255.255.255
R1(config)# access-list 1 remark ## BLOCK BOB ##      ! comment, shown only in the config
R2(config)# ip access-list standard BLOCK_BOB         ! standard named ACL, enters ACL config mode
R2(config-std-nacl)# 5 deny 1.1.1.1                   ! entry with explicit sequence number
R2(config-std-nacl)# 10 permit any
R2(config-std-nacl)# remark ## BLOCK BOB ##
R1(config-if)# ip access-group 1 out                  ! applies the ACL (number or name) in or out
R1# show access-lists                                 ! all ACLs, sequence numbers, match counters
R1# show ip access-lists                              ! IP ACLs only
R1# show running-config | include access-list        ! config lines containing access-list
R1# show running-config | section access-list        ! whole section (named ACL entries)
```

### 8. The lab (video 70)

Goal: OSPF between R1 (172.16.1.0/24, 172.16.2.0/24) and R2 (192.168.1.0/24, 192.168.2.0/24) over 203.0.113.0/30, then four ACLs: numbered on R1, named on R2.

1. **OSPF**: `router ospf 1`, `network 172.16.0.0 0.0.255.255 area 0`, `network 203.0.113.0 0.0.0.3 area 0` on R1 (192.168.0.0 on R2). Check `show ip ospf interface`, `show ip ospf neighbor` (FULL state, dash instead of DR/BDR: point-to-point serial link), `show ip route`.
2. **R2, `TO_192.168.1.0/24`** (only PC1 and PC3 allowed): `permit 172.16.1.1`, `permit 172.16.2.1`, `deny any` (unnecessary given the implicit deny, but good practice for clarity); `interface g0/0`, `ip access-group TO_192.168.1.0/24 out`. Test: PC1 pings SRV1 (the first pings may fail while ARP completes); PC2 gets **"destination host unreachable"** from 203.0.113.2 (R2).
3. **R2, `TO_192.168.2.0/24`** (172.16.2.0/24 blocked): `deny 172.16.2.0 0.0.0.255`, `permit any`; `interface g0/1`, `ip access-group TO_192.168.2.0/24 out`. PC1 → SRV2 OK, PC3 → SRV2 unreachable. `do show access-lists` shows **how many packets matched** each entry.
4. **R1, ACL 1 and 2** (172.16.1.0/24 and 172.16.2.0/24 must not communicate): `access-list 1 deny 172.16.1.0 0.0.0.255`, `access-list 1 permit any`; same for ACL 2 with 172.16.2.0. `interface g0/1` → `ip access-group 1 out`; `interface g0/0` → `ip access-group 2 out`.
5. Test with `ping -t 172.16.2.1` on PC1 (continuous ping, `Ctrl+C` to stop) and the reverse: fails; `do show access-lists` on R1 shows the deny counters increasing.

NetSim bonus (ACL practice lab 2): 20 ACL labs in NetSim. ACL 1 on Router1, `access-list 1 deny 10.10.2.0 0.0.1.255` (covers 10.10.2.0/24 and 10.10.3.0/24 in one entry), `permit any`, applied **inbound** on F0/0 (link to Router2): Telnet and ping to loopback 1.1.1.1 work from PC1, fail from PC2 and PC3. ACL 2 `deny 10.10.1.0 0.0.0.255`, `permit any`, applied **outbound** on F1/0 (VLAN1 side): prevents a remote host from **spoofing** a VLAN1 source address. Then ACL 1 also applied **outbound** on F0/0 to stop Router1's hosts from pretending to be on VLAN2/VLAN3.

### 9. The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which ACL, applied outbound on R2 G0/1, permits only PC1 and PC4 to access 10.0.1.0/24? | **ACL 1**: entry 10 permits PC1, entry 20 permits PC4, implicit deny for the rest | The other ACLs shown do not fulfill the requirement. |
| Which interface and direction for the ACL controlling access to 10.0.2.0/24? | **R2 G0/2, outbound** | Standard ACLs go as close to the destination as possible. |
| ACL 10 applied after another ACL on the same interface and direction: effect? | **Traffic from 10.0.0.0/24 is denied** | One ACL per interface per direction; the last one applied replaces the previous. |
| ACL (deny … then permit any) applied inbound on R1 G0/0: which PCs can ping SRV2? | **All PCs** | Pings exit G0/0 unchecked; SRV2's replies (10.0.2.100) enter and match `permit any`. |
| Packet matching no ACL entry? | **It is dropped** | Implicit deny; it is not sent to the gateway, not checked by another ACL, not handled by the most specific match. |

Boson bonus: ACLs are processed **from the first entry to the last**, not by specificity.
