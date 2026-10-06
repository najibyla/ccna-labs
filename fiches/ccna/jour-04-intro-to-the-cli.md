# CCNA Day 4 : Intro to the CLI / Introduction à la CLI Cisco IOS

> Source : Jeremy's IT Lab, « Free CCNA | Intro to the CLI | Day 4 » (31 min), vidéo n°8 de la playlist (cours) ; « Basic Device Security | Day 4 Lab » (10 min), vidéo n°9 (lab Packet Tracer). Fiche rédigée à partir des transcriptions le 6 octobre 2026.

## 🇫🇷 Version française

### 1. Cisco IOS et la CLI

- **Cisco IOS** est le système d'exploitation des équipements Cisco (comme Windows sur un PC). **Aucun rapport avec l'iOS d'Apple.**
- **CLI** (*command-line interface*) : l'interface en ligne de commande pour configurer routeurs, switches et pare-feu. Il existe aussi des **GUI** (*graphical user interface*, par exemple **ASDM** pour les pare-feu Cisco), non couvertes ici : la plupart des ingénieurs réseau préfèrent la CLI.

### 2. Se connecter par le port console

- Première configuration : on apporte son portable à l'équipement et on se branche sur le **port console**. L'accès à distance sera vu plus tard.
- Un switch Catalyst a **deux ports console** : un **RJ-45** (même forme que les ports réseau) et un **USB mini-B**.
- Pour le RJ-45 : câble **RJ-45 vers DB9**, appelé **câble rollover**, plus un **adaptateur USB** car les portables n'ont plus de port série. Brochage : **1 ↔ 8, 2 ↔ 7, 3 ↔ 6, 4 ↔ 5** (différent du croisé Ethernet).
- Émulateur de terminal, par exemple **PuTTY** : choisir **Serial**, puis Open. Réglages par défaut (identiques aux valeurs par défaut Cisco, à retenir pour l'examen) : **9 600 bits/s** (*baud rate*), **8 bits de données**, **1 bit de stop**, **parité : aucune**, **contrôle de flux : aucun**.
- Au premier démarrage, répondre **no** à « enter the initial configuration dialog », puis Entrée.

### 3. Les modes de la CLI

| Mode | Invite | Accès | Ce qu'on y fait |
| :--- | :--- | :--- | :--- |
| **User EXEC** (ou *user mode*) | `Router>` | par défaut | très limité : regarder quelques choses, aucune modification |
| **Privileged EXEC** | `Router#` | `enable` | accès complet en lecture, redémarrage, changement d'heure, sauvegarde de la configuration ; pas la modification de la configuration |
| **Global configuration** | `Router(config)#` | `configure terminal` | modification de la configuration |

- Le texte avant `>` ou `#` est le **nom d'hôte** (*hostname*) ; par défaut **Router** sur un routeur Cisco.
- **Packet Tracer** est un **simulateur** : excellent et suffisant pour le CCNA, mais il ne supporte pas tout (un vrai équipement affiche plus de commandes).

### 4. Aides à la saisie

- **`?`** liste les commandes disponibles. **`e?`** (sans espace) liste les complétions possibles du mot (`enable`, `exit`). **`enable password ?`** (avec espace) liste les options suivantes. **`LINE`** en majuscules signifie « tapez votre propre texte » ; **`<cr>`** signifie qu'il ne reste qu'à appuyer sur Entrée.
- **Tab** complète le mot. Les commandes peuvent être **abrégées** tant qu'elles restent uniques : `en` suffit pour `enable`, mais `e` est **ambigu** (*ambiguous command*, enable ou exit) ; `ex` pour `exit` ; `con?` donne configure et connect, donc **`conf t`** pour `configure terminal` (terminal est la seule option en t).
- Connaître la **forme longue** des commandes, même si on utilise les raccourcis.

### 5. Protéger le mode privilégié

- **`enable password CCNA`** (mode config globale) : demande un mot de passe à la commande `enable`. **Sensible à la casse** (CCNA ≠ ccna). Le mot de passe **ne s'affiche pas** pendant la saisie. **3 erreurs** → accès refusé pour « *bad secrets* ».
- Test : `exit` revient en privileged EXEC, `exit` encore déconnecte ; Entrée ramène en user EXEC ; `enable` demande alors le mot de passe.

### 6. running-config et startup-config

- **running-config** : configuration **active** actuelle, modifiée au fur et à mesure des commandes.
- **startup-config** : configuration **chargée au redémarrage**. Tant qu'on n'a pas sauvegardé, `show startup-config` répond « *startup-config is not present* » et un redémarrage charge une configuration par défaut.
- Trois commandes équivalentes pour sauvegarder, toutes en privileged EXEC : **`write`**, **`write memory`**, **`copy running-config startup-config`**.

### 7. Chiffrer les mots de passe

- Dans `show running-config`, `enable password CCNA` apparaît **en clair** : risque de sécurité.
- **`service password-encryption`** chiffre tous les mots de passe affichés dans la configuration : CCNA devient `08026F6028`, précédé du chiffre **7** = algorithme **propriétaire Cisco**. Le mot de passe reste CCNA ; seul l'affichage change. **Faible** : un « type 7 password cracker » trouvé sur Google le casse en quelques secondes.
- **`enable secret Cisco`** : mot de passe **toujours chiffré**, type **5 = MD5**, bien plus sûr (pas invincible). Si `enable password` et `enable secret` sont tous deux configurés, **seul le secret est valide**, l'enable password est ignoré. **`service password-encryption` n'a aucun effet sur l'enable secret.** Conclusion : toujours utiliser `enable secret`.
- **`do`** devant une commande de privileged EXEC (`do show running-config`, abrégé `do sh run`) permet de l'exécuter depuis un mode de configuration.

### 8. Annuler une commande : `no`

`no service password-encryption` : les mots de passe **déjà chiffrés le restent**, les **nouveaux** seront en clair.

| | Activer `service password-encryption` | Désactiver |
| :--- | :--- | :--- |
| Mots de passe existants | chiffrés | restent chiffrés |
| Mots de passe futurs | chiffrés | en clair |
| enable secret | toujours chiffré | toujours chiffré |

### 9. Pièges d'examen

- **Rollover** (console, 1 ↔ 8…) ≠ **crossover** (Ethernet, 1 ↔ 3, 2 ↔ 6) ; le port console USB est un port **séparé** du RJ-45.
- Valeurs série par défaut : **9600, 8, 1, aucune parité, aucun contrôle de flux**.
- Mot de passe refusé ? Penser **Caps Lock** (sensible à la casse) ; `service password-encryption` ne change jamais le mot de passe lui-même.
- Le plus sûr : **`enable secret`** (MD5, type 5), pas `enable password` même avec `service password-encryption` (type 7, faible).
- Secret et password configurés : on saisit **le secret seulement**, jamais les deux.
- `conf t` = **`configure terminal`** (pas « configuration terminal »).
- `show running-config` se lance depuis **privileged EXEC** (ou avec `do` depuis la configuration). Dans la récapitulation, la transcription liste « run » devant les commandes à exécuter en mode configuration : erratum, il s'agit de **`do`**.

### 10. Commandes IOS

```text
Router> enable                                  ! passe en privileged EXEC (abrégé : en)
Router# configure terminal                      ! passe en configuration globale (abrégé : conf t)
Router(config)# hostname R1                     ! change le nom d'hôte (vu dans le lab)
Router(config)# enable password CCNA            ! mot de passe du mode privilégié, en clair dans la config
Router(config)# service password-encryption     ! chiffre (type 7, faible) les mots de passe affichés
Router(config)# enable secret Cisco             ! mot de passe toujours chiffré (type 5, MD5), prioritaire
Router(config)# no service password-encryption  ! annule une commande : les futurs mots de passe restent en clair
Router(config)# do show running-config          ! exécute une commande privileged EXEC depuis la config
Router(config)# exit                            ! retour au mode précédent (abrégé : ex)
Router# show running-config                     ! configuration active (abrégé : sh run)
Router# show startup-config                     ! configuration chargée au redémarrage
Router# write                                   ! sauvegarde running-config vers startup-config
Router# write memory                            ! idem
Router# copy running-config startup-config      ! idem
?                                               ! aide contextuelle : e? (complétions), enable ?  (options suivantes)
```

### 11. Le lab (Day 4 Lab, « Basic Device Security »)

**Objectif :** sur un petit réseau (PC, switch SW1, routeur R1), sécuriser l'accès à la CLI. Jeremy ne fait que le routeur ; **refaire aussi sur le switch** (la répétition est essentielle). Dans Packet Tracer, cliquer sur l'équipement puis l'onglet **CLI** ; en vrai, il faut un ordinateur relié au port console.

1. **Noms d'hôte** : `en`, `conf t`, `hostname R1` (l'invite passe de Router à R1). Faire `hostname SW1` sur le switch.
2. **Mot de passe enable non chiffré** : `enable password CCNA`.
3. **Tester** : `exit` deux fois jusqu'en user EXEC, `enable`, saisir CCNA (invisible). Trois mauvais mots de passe → « bad secrets », puis réessayer.
4. **Voir le mot de passe** : `show running-config` (ou `sh run`) en privileged EXEC : `enable password CCNA` en clair. Sans sauvegarde, un arrêt perd les changements.
5. **Activer le chiffrement** : `conf t`, `service password-encryption`.
6. **Revoir la config** : `show running-config` échoue en mode config ; utiliser **`do show running-config`**. Le mot de passe apparaît précédé de **7** (type de chiffrement) : protégé contre un regard par-dessus l'épaule, mais cassable.
7. **Enable secret** : `enable secret Cisco` (MD5).
8. **Retester** : `exit` jusqu'en user EXEC, `enable` : **CCNA ne marche plus**, **Cisco** fonctionne. Seul le secret est valide.
9. **Revoir la config** : enable password en type **7**, enable secret en type **5** (MD5).
10. **Sauvegarder** : `write`, `write memory`, `copy running-config startup-config` (les trois sont montrées). **Vérifier** avec `show startup-config` : les mots de passe y figurent, suivis des nombreux réglages par défaut.

### 12. Le quiz (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quel câble pour se connecter au port console RJ-45 d'un équipement Cisco ? | **Câble rollover** | Le crossover relie deux équipements en Ethernet. Un câble USB sert au port console USB, qui est un port distinct. |
| `enable` demande un mot de passe qui n'est pas accepté. Cause possible ? | **Caps Lock activé** | `service password-encryption` activé ou désactivé ne change pas le mot de passe, seulement son affichage. Les mots de passe sont sensibles à la casse. |
| Méthode la plus sûre pour protéger le mode privilégié ? | **`enable secret`** | `enable password` est en clair ; avec `service password-encryption` le chiffrement reste faible ; le secret est chiffré automatiquement en MD5. |
| enable password et enable secret tous deux configurés : que saisir à `enable` ? | **Le secret seulement** | Le secret a toujours priorité ; on ne demande jamais les deux. |
| Forme longue de `conf t` ? | **`configure terminal`** | « configuration time » et « configuration terminal » n'existent pas. |

---

## 🇬🇧 English version

### 1. Cisco IOS and the CLI

- **Cisco IOS** is the operating system on Cisco devices (like Windows on a PC). **Not related to Apple's iOS.**
- **CLI** (*command-line interface*): the interface used to configure routers, switches and firewalls. **GUIs** (*graphical user interfaces*, e.g. **ASDM** for Cisco firewalls) exist but are not covered: most network engineers prefer the CLI.

### 2. Connecting through the console port

- First-time configuration: bring your laptop to the device and plug into the **console port**. Remote access comes later.
- A Catalyst switch has **two console ports**: an **RJ-45** (same shape as network ports) and a **USB mini-B**.
- For RJ-45: an **RJ-45 to DB9** cable called a **rollover cable**, plus a **USB adapter** since laptops no longer have serial ports. Pinout: **1 ↔ 8, 2 ↔ 7, 3 ↔ 6, 4 ↔ 5** (different from an Ethernet crossover).
- Terminal emulator, e.g. **PuTTY**: select **Serial**, then Open. Default settings (match Cisco defaults, remember them for the exam): **9,600 bits per second** (baud rate), **8 data bits**, **1 stop bit**, **no parity**, **no flow control**.
- On first boot, answer **no** to "enter the initial configuration dialog", then press Enter.

### 3. CLI modes

| Mode | Prompt | Enter with | What you do there |
| :--- | :--- | :--- | :--- |
| **User EXEC** (or *user mode*) | `Router>` | default | very limited: look at a few things, no changes |
| **Privileged EXEC** | `Router#` | `enable` | full view of the configuration, restart, change the time, save the configuration; not changing the configuration |
| **Global configuration** | `Router(config)#` | `configure terminal` | change the configuration |

- The text before `>` or `#` is the **hostname**; default **Router** on a Cisco router.
- **Packet Tracer** is a **simulator**: excellent and sufficient for the CCNA, but it does not support everything (a real device shows more commands).

### 4. Typing helpers

- **`?`** lists available commands. **`e?`** (no space) lists possible completions of the word (`enable`, `exit`). **`enable password ?`** (with a space) lists the next options. **`LINE`** in capitals means "type your own text"; **`<cr>`** means the only option left is Enter.
- **Tab** completes the word. Commands can be **abbreviated** as long as they stay unique: `en` is enough for `enable`, but `e` is an **ambiguous command** (enable or exit); `ex` for `exit`; `con?` gives configure and connect, hence **`conf t`** for `configure terminal` (terminal is the only option starting with t).
- Know the **full-length** commands even if you use the shortcuts.

### 5. Protecting privileged EXEC mode

- **`enable password CCNA`** (global configuration): a password is requested at `enable`. **Case-sensitive** (CCNA is not ccna). The password **is not displayed** as you type. **3 wrong attempts** → access denied for "*bad secrets*".
- Test: `exit` returns to privileged EXEC, `exit` again logs out; Enter brings you back to user EXEC; `enable` now asks for the password.

### 6. running-config and startup-config

- **running-config**: the current, **active** configuration, edited as you enter commands.
- **startup-config**: the configuration **loaded on restart**. Until you save, `show startup-config` says "*startup-config is not present*" and a reload loads a default configuration.
- Three equivalent save commands, all from privileged EXEC: **`write`**, **`write memory`**, **`copy running-config startup-config`**.

### 7. Encrypting passwords

- In `show running-config`, `enable password CCNA` appears **in plain text**: a security risk.
- **`service password-encryption`** encrypts all passwords shown in the configuration: CCNA becomes `08026F6028`, preceded by **7** = Cisco's **proprietary** algorithm. The password is still CCNA; only the display changes. **Weak**: a "type 7 password cracker" found on Google breaks it in seconds.
- **`enable secret Cisco`**: a password that is **always encrypted**, type **5 = MD5**, much more secure (not invincible). If both `enable password` and `enable secret` are configured, **only the secret is valid**; the enable password is ignored. **`service password-encryption` has no effect on the enable secret.** Bottom line: always use `enable secret`.
- **`do`** in front of a privileged EXEC command (`do show running-config`, short `do sh run`) runs it from a configuration mode.

### 8. Removing a command: `no`

`no service password-encryption`: passwords **already encrypted stay encrypted**, **new** ones will be in clear text.

| | Enable `service password-encryption` | Disable it |
| :--- | :--- | :--- |
| Current passwords | encrypted | stay encrypted |
| Future passwords | encrypted | clear text |
| enable secret | always encrypted | always encrypted |

### 9. Exam traps

- **Rollover** (console, 1 ↔ 8…) is not **crossover** (Ethernet, 1 ↔ 3, 2 ↔ 6); the USB console port is **separate** from the RJ-45 one.
- Default serial settings: **9600, 8, 1, no parity, no flow control**.
- Password rejected? Think **Caps Lock** (case-sensitive); `service password-encryption` never changes the password itself.
- Most secure: **`enable secret`** (MD5, type 5), not `enable password` even with `service password-encryption` (type 7, weak).
- Secret and password both configured: you enter **the secret only**, never both.
- `conf t` = **`configure terminal`** (not "configuration terminal").
- `show running-config` runs from **privileged EXEC** (or with `do` from configuration). In the review slide the transcript lists "run" as the prefix for running commands in configuration mode: erratum, it is **`do`**.

### 10. IOS commands

```text
Router> enable                                  ! enter privileged EXEC (short: en)
Router# configure terminal                      ! enter global configuration (short: conf t)
Router(config)# hostname R1                     ! set the hostname (seen in the lab)
Router(config)# enable password CCNA            ! privileged EXEC password, clear text in the config
Router(config)# service password-encryption     ! encrypt (type 7, weak) the passwords shown in the config
Router(config)# enable secret Cisco             ! always-encrypted password (type 5, MD5), takes precedence
Router(config)# no service password-encryption  ! remove a command: future passwords stay in clear text
Router(config)# do show running-config          ! run a privileged EXEC command from configuration mode
Router(config)# exit                            ! back to the previous mode (short: ex)
Router# show running-config                     ! active configuration (short: sh run)
Router# show startup-config                     ! configuration loaded on restart
Router# write                                   ! save running-config to startup-config
Router# write memory                            ! same
Router# copy running-config startup-config      ! same
?                                               ! context-sensitive help: e? (completions), enable ? (next options)
```

### 11. The lab (Day 4 Lab, "Basic Device Security")

**Goal:** on a small network (PCs, switch SW1, router R1), secure CLI access. Jeremy only configures the router; **do the switch too** (repetition is essential). In Packet Tracer, click the device then the **CLI** tab; in real life you need a computer connected to the console port.

1. **Hostnames**: `en`, `conf t`, `hostname R1` (the prompt changes from Router to R1). Do `hostname SW1` on the switch.
2. **Unencrypted enable password**: `enable password CCNA`.
3. **Test**: `exit` twice down to user EXEC, `enable`, type CCNA (invisible). Three wrong passwords → "bad secrets", then try again.
4. **View the password**: `show running-config` (or `sh run`) from privileged EXEC: `enable password CCNA` in clear text. Without saving, powering off loses the changes.
5. **Enable encryption**: `conf t`, `service password-encryption`.
6. **View the config again**: `show running-config` fails in configuration mode; use **`do show running-config`**. The password now has a **7** in front (encryption type): safe from someone glancing over your shoulder, but crackable.
7. **Enable secret**: `enable secret Cisco` (MD5).
8. **Test again**: `exit` down to user EXEC, `enable`: **CCNA no longer works**, **Cisco** does. Only the secret is valid.
9. **View the config again**: enable password is type **7**, enable secret is type **5** (MD5).
10. **Save**: `write`, `write memory`, `copy running-config startup-config` (all three are shown). **Check** with `show startup-config`: the passwords are there, followed by lots of default settings.

### 12. The quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which cable connects to a Cisco device's RJ-45 console port? | **Rollover cable** | A crossover connects two devices over Ethernet. A USB cable goes to the USB console port, which is separate. |
| `enable` asks for a password that is not accepted. Possible problem? | **Caps Lock is on** | `service password-encryption`, enabled or disabled, does not change the password, only its display. Passwords are case-sensitive. |
| Most secure method to protect privileged EXEC? | **`enable secret`** | `enable password` is plain text; with `service password-encryption` the encryption is weak; the secret is automatically MD5-encrypted. |
| Both enable password and enable secret configured: what do you enter at `enable`? | **The enable secret only** | The secret always takes precedence; you are never asked for both. |
| Full-length version of `conf t`? | **`configure terminal`** | "configuration time" and "configuration terminal" do not exist. |
