# CCNA Day 63 : Ansible, Puppet, Chef & Terraform / Outils de gestion de configuration et de provisionnement

> Source : Jeremy's IT Lab, « Free CCNA | Ansible, Puppet, & Chef | Day 63 (part 1) » (22 min, vidéo n°124 de la playlist) et « Terraform | CCNA 200-301 Day 63 (part 2) » (22 min, vidéo n°125). Pas de lab pour ce jour. Fiche rédigée à partir des transcriptions le 6 octobre 2026. Sujet d'examen : 6.6 (reconnaître les capacités des mécanismes de gestion de configuration « tels que » Ansible et Terraform ; Puppet et Chef restent dans le cours pour la comparaison agent/agentless).

## 🇫🇷 Version française

## Partie 1 : Ansible, Puppet et Chef

### 1. Pourquoi des outils de gestion de configuration

- **Dérive de configuration** (*configuration drift*) : des modifications individuelles accumulées au fil du temps éloignent la configuration d'un équipement du **standard** défini par l'entreprise. La plupart d'une configuration suit des **modèles standard** (SNMP, Syslog, AAA, une ou deux interfaces WAN et LAN…), seuls quelques éléments sont uniques (nom d'hôte, adresses IP). Les changements de dépannage ou de test, souvent non documentés, créent la dérive.
- Même sans outil, avoir des pratiques standard : Jeremy sauvegardait chaque configuration en fichier texte dans un dossier partagé, nommé `hostname_annéemoisjour`. Limites : un ingénieur peut oublier de déposer le fichier ; cela ne garantit pas la conformité au standard ; pas scalable à des centaines d'équipements.
- **Provisionnement de configuration** (*configuration provisioning*) : la façon d'appliquer les changements, y compris sur les nouveaux équipements. Traditionnellement un par un en SSH ou console : ne passe pas à l'échelle.
- Deux composants communs à tous ces outils : les **templates** (configuration sans valeurs pour hostname, IP, masque, process ID et area OSPF…) et les **variables** (fichier séparé par équipement, par exemple R1) ; template + variables → configuration générée et envoyée à l'équipement.
- Capacités : **générer des configurations** pour de nouveaux équipements à grande échelle, **appliquer des changements** (tous les équipements, un sous-ensemble ou un seul), **vérifier la conformité** aux standards (alerte ou correction automatique), **comparer** des configurations entre équipements ou entre versions.
- Popularité pour les équipements réseau : **Ansible, puis Puppet, puis Chef**. Ces outils ont été créés après l'essor des **VM**, pour que les administrateurs système automatisent la création, la configuration et la suppression de VM.

### 2. Ansible

- Propriété de **Red Hat**, écrit en **Python**.
- **Agentless** : aucun logiciel spécial sur les équipements gérés ; Ansible se connecte en **SSH**. Grande polyvalence, d'où sa popularité pour le réseau.
- **Modèle push** : le serveur Ansible, appelé **control node**, pousse les configurations via SSH.
- Fichiers texte nécessaires : **playbooks** (le « plan » des tâches d'automatisation, logique et actions, en **YAML**), **inventory** (liste des équipements gérés et leurs caractéristiques, par exemple le rôle access switch, core switch, WAN router, firewall ; formats **INI** ou **YAML**), **templates** (configuration sans valeurs de variables, format **Jinja2**), **variable files** (variables et valeurs, en **YAML**). Inventaire + templates + variables alimentent le playbook qui pousse la configuration.

### 3. Puppet

- Écrit en **Ruby**. **Typiquement agent-based** : un **agent Puppet** doit être installé sur les équipements gérés ; **tous les équipements Cisco ne le prennent pas en charge**, raison majeure de la popularité d'Ansible. Peut fonctionner **agentless** via un **proxy agent** sur un hôte externe qui se connecte en SSH aux équipements.
- Le serveur s'appelle le **Puppet master**. **Modèle pull** : les clients tirent leur configuration. Port **TCP 8140** des clients vers le Puppet master.
- Fichiers dans un **langage propriétaire** (pas YAML) : le **Manifest** définit l'**état de configuration souhaité** d'un équipement ; des **templates** aident à générer les Manifests. Les agents fournissent une **API REST** pour communiquer avec l'équipement.

### 4. Chef

- Écrit en **Ruby**. **Agent-based** (agent Chef) ; **la plupart des équipements Cisco ne le prennent pas en charge** : le moins populaire des trois.
- **Modèle pull**. Le serveur Chef utilise le port **TCP 10002** pour envoyer les configurations (d'autres ports existent, retenir 10002).
- Fichiers dans un **DSL** (*Domain-Specific Language*) **basé sur Ruby** : **resources** (les ingrédients : objets de configuration gérés, par exemple un ensemble de commandes), **recipes** (logique et actions sur les ressources), **cookbooks** (ensembles de recettes liées), **run-lists** (liste ordonnée de recettes pour amener l'équipement à l'état souhaité). Architecture : **Chef workstation** (préparation des cookbooks) → **Chef server** → **Chef clients** (serveurs, stockage, plateformes virtuelles, clouds publics, équipements réseau).

### 5. Tableau comparatif (à mémoriser)

| | **Ansible** | **Puppet** | **Chef** |
| :--- | :--- | :--- | :--- |
| Langage de l'outil | **Python** | **Ruby** | **Ruby** |
| Agent | **Agentless** (SSH) | **Agent-based** (proxy agent possible) | **Agent-based** |
| Modèle | **Push** | **Pull** | **Pull** |
| Port | SSH | **TCP 8140** | **TCP 10002** |
| Communication | SSH | HTTP via **API REST** | HTTP via **API REST** |
| Fichiers | **YAML** (playbooks, variables), Jinja2 (templates), INI/YAML (inventory) | **Langage propriétaire** (Manifests) | **DSL basé sur Ruby** (resources, recipes, cookbooks, run-lists) |
| Serveur | Control node | Puppet master | Chef server |

### 6. Le quiz de la partie 1 (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quel outil se connecte aux équipements en SSH ? | **Ansible** | Agentless, le control node utilise SSH. Un proxy agent Puppet utilise aussi SSH, mais pas l'architecture Puppet standard : Ansible est la meilleure réponse. |
| Quels outils utilisent un modèle pull ? (toutes les réponses valables) | **Chef** et **Puppet** | Ansible utilise un modèle push. |
| Quels outils utilisent un modèle client-serveur ? | **Tous** | Jeremy ne l'a pas dit explicitement, mais il a décrit des serveurs et des clients pour chacun. |
| Quels outils sont écrits en Ruby ? (toutes les réponses valables) | **Chef** et **Puppet** | Ansible est écrit en Python. |
| Quel outil utilise des playbooks ? | **Ansible** | Les playbooks décrivent la logique et les actions des tâches. |

## Partie 2 : Terraform

### 7. Infrastructure as Code (IaC)

- **IaC** : provisionner et gérer l'infrastructure (serveurs, réseaux, ressources cloud) avec des **fichiers de configuration lisibles par la machine** (du code) au lieu d'une configuration manuelle en CLI ou GUI. Ansible, Puppet et Chef sont des outils IaC de **gestion de configuration** (Ansible gère les équipements via ses fichiers playbook, inventory, template, variables) ; **Terraform est un outil IaC de provisionnement**. Bénéfices : cohérence, scalabilité, répétabilité.

### 8. Gestion de configuration vs provisionnement

- **Gestion de configuration** (Ansible, Puppet, Chef) : gérer une infrastructure **existante** (installer des logiciels, configurer, maintenir l'état), appliquer et faire respecter les configurations sur de nombreux équipements.
- **Provisionnement d'infrastructure** (Terraform) : **créer, modifier, supprimer** des ressources (serveurs virtuels, routeurs sur un cloud comme AWS) ; accent sur la **mise en place initiale**.
- Les deux se combinent : **Terraform provisionne** (VM, réseau, stockage), **Ansible configure et maintient**. Chacun peut faire un peu de l'autre, mais leurs forces diffèrent.

### 9. Infrastructure mutable vs immutable

- **Mutable** (outils de gestion de configuration) : l'infrastructure **peut être modifiée après déploiement** (mises à jour, correctifs, changements de configuration), **sur place** ; comme modifier une configuration dans le CLI. Ansible met à jour la configuration de la VM en la laissant en place.
- **Immutable** (outils de provisionnement comme Terraform) : l'infrastructure **ne change pas après déploiement** ; tout changement = **remplacer la ressource** par une nouvelle (créer une nouvelle instance de VM avec la configuration mise à jour, puis détruire l'ancienne). Avantage : **pas de dérive de configuration**, chaque déploiement part d'un état prédéfini. (La dérive n'est pas un gros problème avec Ansible bien géré, mais Terraform l'élimine presque.)

### 10. Approche procédurale vs déclarative

- **Procédurale** (ou **impérative**) : l'outil suit des **étapes explicites dans un ordre précis** définies par l'ingénieur (`hostname R1`, `ip address` sur G0/1, `no shutdown`… et des étapes différentes sur un routeur Juniper). Plus de contrôle, plus exigeant.
- **Déclarative** : on définit l'**état final souhaité** (« un routeur R1 avec 192.168.1.1/24 sur G0/1, interface activée ») et l'outil trouve les étapes. Plus facile à maintenir, cohérence entre déploiements.
- Classement pour le CCNA : **Ansible et Chef = procéduraux** (Ansible a des éléments déclaratifs, mais Red Hat le qualifie de procédural) ; **Terraform et Puppet = déclaratifs**.

### 11. Terraform

- Outil IaC **open source** de **HashiCorp** (société américaine rachetée par **IBM en 2025**). Avant tout un **outil de provisionnement** sur des plateformes cloud et sur site appelées **providers** : **AWS, Azure, GCP, Kubernetes** et plus de **1000** autres, dont **Cisco Catalyst Center**, **ACI** et **IOS XE** (l'IOS des Catalyst modernes).
- Comme Ansible : **modèle push** et **agentless**.
- **Quatre composants** : **Terraform Core** (logiciel principal, typiquement sur un serveur Linux, traite les configurations et parle aux providers via leurs **API**), les **fichiers de configuration** (état final souhaité, écrits par l'ingénieur, **déclaratifs**), le **state file** (suit l'état actuel de l'infrastructure déployée ; par comparaison avec l'état souhaité, Terraform détermine les actions et leur ordre), les **providers**.
- **Workflow en trois étapes : write** (définir l'état souhaité dans les fichiers de configuration), **plan** (Terraform analyse et montre exactement les changements à venir, à vérifier avant application), **apply** (exécution du plan). Une quatrième étape possible : **destroy** (supprimer les ressources devenues inutiles).
- Langages : **Terraform Core est écrit en Go** ; les fichiers de configuration en **HCL** (*HashiCorp Configuration Language*), un **DSL** (comme le DSL de Puppet), plus simple qu'un langage généraliste comme Python ou Go mais à apprendre spécifiquement.

### 12. Pièges d'examen

- **Agentless + push : Ansible et Terraform** ; **agent-based + pull : Puppet et Chef**.
- **Ports : Puppet TCP 8140, Chef TCP 10002.**
- **Python : Ansible ; Ruby : Puppet, Chef ; Go : Terraform Core.** **YAML : Ansible ; HCL : Terraform.**
- **Gestion de configuration : Ansible, Puppet, Chef (mutable)** ; **provisionnement : Terraform (immutable)**.
- **Déclaratifs : Terraform, Puppet** ; **procéduraux : Ansible, Chef**.
- Workflow Terraform : **write, plan, apply**.

### 13. Le quiz de la partie 2 (3 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Caractéristiques de Terraform ? (deux réponses) | **Déclaratif** et **infrastructure immutable** | On spécifie l'état final et Terraform fait le reste ; une ressource ne change pas après provisionnement, elle est remplacée puis l'ancienne supprimée. |
| Les trois étapes principales du workflow Terraform ? | **Write, plan, apply** | Write : définir l'état souhaité ; plan : vérifier les changements avant application ; apply : appliquer les changements. |
| Quels outils IaC sont axés sur la gestion de configuration ? (trois réponses) | **Ansible**, **Chef** et **Puppet** | Terraform est un outil de provisionnement ; il est courant de combiner Terraform et Ansible. |

---

## 🇬🇧 English version

## Part 1: Ansible, Puppet and Chef

### 1. Why configuration management tools

- **Configuration drift**: individual changes made over time cause a device's configuration to deviate from the **standard** defined by the company. Most of a configuration follows **standard templates** (SNMP, Syslog, AAA, one or two WAN and LAN interfaces...); only a few parts are unique (hostname, IP addresses). Troubleshooting or test changes, often undocumented, create drift.
- Even without tools, have standard practices: Jeremy saved each config as a text file in a shared folder named `hostname_yearmonthday`. Flaws: an engineer may forget to save the file; it does not guarantee the config matches the standard; not scalable to hundreds of devices.
- **Configuration provisioning**: how configuration changes are applied, including to new devices. Traditionally one by one via SSH or console: does not scale.
- Two components common to all these tools: **templates** (configuration without values for hostname, IP, mask, OSPF process ID and area...) and **variables** (separate file per device, e.g. R1); template + variables → a config is generated and sent to the device.
- Capabilities: **generate configurations** for new devices at scale, **perform configuration changes** (all devices, a subset or one), **check compliance** with standards (alert or automated fix), **compare** configurations between devices or between versions.
- Popularity for network devices: **Ansible, then Puppet, then Chef**. These tools were created after the rise of **VMs**, for server sysadmins to automate creating, configuring and removing VMs.

### 2. Ansible

- Owned by **Red Hat**, written in **Python**.
- **Agentless**: no special software on managed devices; Ansible connects via **SSH**. Very versatile, hence its popularity for networking.
- **Push model**: the Ansible server, called the **control node**, pushes configurations via SSH.
- Required text files: **playbooks** (the "blueprint" of automation tasks, logic and actions, in **YAML**), **inventory** (list of managed devices and their characteristics, e.g. role such as access switch, core switch, WAN router, firewall; **INI** or **YAML** formats), **templates** (device configuration without variable values, **Jinja2** format), **variable files** (variables and values, in **YAML**). Inventory + templates + variables feed the playbook, which pushes the config.

### 3. Puppet

- Written in **Ruby**. **Typically agent-based**: a **Puppet agent** must be installed on managed devices; **not all Cisco devices support it**, a major reason Ansible is more popular. Can run **agentless** via a **proxy agent** on an external host that uses SSH to the devices.
- The server is called the **Puppet master**. **Pull model**: clients pull their configurations. Clients use **TCP 8140** to the Puppet master.
- Files in a **proprietary language** (not YAML): the **Manifest** defines the **desired configuration state** of a device; **templates** help generate Manifests. Agents provide a **REST API** to communicate with the device.

### 4. Chef

- Written in **Ruby**. **Agent-based** (Chef agent); **most Cisco devices do not support it**: the least popular of the three.
- **Pull model**. The Chef server uses **TCP 10002** to send configurations (other ports exist; remember 10002).
- Files use a **DSL** (Domain-Specific Language) **based on Ruby**: **resources** (the ingredients: configuration objects managed by Chef, e.g. a set of commands), **recipes** (logic and actions on resources), **cookbooks** (sets of related recipes), **run-lists** (ordered list of recipes to bring a device to the desired state). Architecture: **Chef workstation** (prepare cookbooks) → **Chef server** → **Chef clients** (servers, storage, virtual platforms, public clouds, network devices).

### 5. Comparison chart (memorize)

| | **Ansible** | **Puppet** | **Chef** |
| :--- | :--- | :--- | :--- |
| Tool language | **Python** | **Ruby** | **Ruby** |
| Agent | **Agentless** (SSH) | **Agent-based** (proxy agent possible) | **Agent-based** |
| Model | **Push** | **Pull** | **Pull** |
| Port | SSH | **TCP 8140** | **TCP 10002** |
| Communication | SSH | HTTP via **REST API** | HTTP via **REST API** |
| Files | **YAML** (playbooks, variables), Jinja2 (templates), INI/YAML (inventory) | **Proprietary language** (Manifests) | **Ruby-based DSL** (resources, recipes, cookbooks, run-lists) |
| Server | Control node | Puppet master | Chef server |

### 6. Part 1 quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which tool connects to devices using SSH? | **Ansible** | Agentless, the control node uses SSH. A Puppet proxy agent also uses SSH, but standard Puppet architecture does not: Ansible is the better answer. |
| Which tools use a pull model? (select all that apply) | **Chef** and **Puppet** | Ansible uses a push model. |
| Which tools use a client-server model? | **All of the above** | Jeremy did not state it explicitly, but described servers and clients for each. |
| Which tools are written in Ruby? (select all that apply) | **Chef** and **Puppet** | Ansible is written in Python. |
| Which tool uses playbooks? | **Ansible** | Playbooks outline the logic and actions of tasks. |

## Part 2: Terraform

### 7. Infrastructure as Code (IaC)

- **IaC**: provisioning and managing infrastructure (servers, networks, cloud resources) with **machine-readable configuration files** (code) instead of manual CLI or GUI configuration. Ansible, Puppet and Chef are IaC **configuration management** tools (Ansible manages devices through its playbook, inventory, template and variable files); **Terraform is an IaC provisioning tool**. Benefits: consistency, scalability, repeatability.

### 8. Configuration management vs provisioning

- **Configuration management** (Ansible, Puppet, Chef): manage **existing** infrastructure (install software, configure settings, maintain state), apply and enforce configurations across many devices.
- **Infrastructure provisioning** (Terraform): **create, modify, delete** resources (virtual servers, routers on a cloud platform like AWS); focus on **initial setup**.
- They combine: **Terraform provisions** (VMs, network, storage), **Ansible configures and maintains**. Each can do some of the other, but their strengths differ.

### 9. Mutable vs immutable infrastructure

- **Mutable** (configuration management tools): infrastructure **can be modified after deployment** (updates, patches, configuration changes), **in place**; like editing a config in the CLI. Ansible updates the VM's config while leaving the VM in place.
- **Immutable** (provisioning tools like Terraform): infrastructure **cannot be changed after deployment**; any change = **replace the resource** with a new one (create an updated VM instance with the changes applied, then destroy the old one). Benefit: **no configuration drift**, each deployment starts from a predefined state. (Drift is not a major issue with well-managed Ansible, but Terraform virtually eliminates it.)

### 10. Procedural vs declarative approach

- **Procedural** (or **imperative**): the tool follows **explicit steps in a specific order** defined by the engineer (`hostname R1`, `ip address` on G0/1, `no shutdown`... and different steps on a Juniper router). More control, more demanding.
- **Declarative**: you define the **desired end state** ("a router named R1 with 192.168.1.1/24 on G0/1, interface enabled") and the tool figures out the steps. Easier to maintain, consistent across deployments.
- Classification for the CCNA: **Ansible and Chef = procedural** (Ansible has declarative elements, but Red Hat calls it procedural); **Terraform and Puppet = declarative**.

### 11. Terraform

- **Open-source** IaC tool by **HashiCorp** (American company acquired by **IBM in 2025**). Primarily a **provisioning tool** for cloud and on-prem platforms called **providers**: **AWS, Azure, GCP, Kubernetes** and over **1000** more, including **Cisco Catalyst Center**, **ACI** and **IOS XE** (the IOS on modern Catalyst switches).
- Like Ansible: **push model** and **agentless**.
- **Four components**: **Terraform Core** (main software, typically on a Linux server, processes configurations and talks to providers via their **APIs**), the **configuration files** (desired end state, written by the engineer, **declarative**), the **state file** (tracks the current state of deployed infrastructure; by comparing it with the desired state, Terraform identifies which actions to take and in which order), the **providers**.
- **Three-step workflow: write** (define the desired state in configuration files), **plan** (Terraform analyzes and shows exactly what will change, to review before applying), **apply** (execute the plan). A possible fourth step: **destroy** (delete resources no longer needed).
- Languages: **Terraform Core is written in Go**; configuration files are in **HCL** (HashiCorp Configuration Language), a **DSL** (like Puppet's DSL), simpler than a general-purpose language like Python or Go but something extra to learn.

### 12. Exam traps

- **Agentless + push: Ansible and Terraform**; **agent-based + pull: Puppet and Chef**.
- **Ports: Puppet TCP 8140, Chef TCP 10002.**
- **Python: Ansible; Ruby: Puppet, Chef; Go: Terraform Core.** **YAML: Ansible; HCL: Terraform.**
- **Configuration management: Ansible, Puppet, Chef (mutable)**; **provisioning: Terraform (immutable)**.
- **Declarative: Terraform, Puppet**; **procedural: Ansible, Chef**.
- Terraform workflow: **write, plan, apply**.

### 13. Part 2 quiz (3 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Characteristics of Terraform? (select two) | **Declarative** and **immutable infrastructure** | You specify the end state and Terraform does the rest; a resource cannot change after provisioning, it is replaced and the old one deleted. |
| The three main steps of the Terraform workflow? | **Write, plan, apply** | Write: define the desired state; plan: verify the changes before applying; apply: apply the changes. |
| Which IaC tools are focused on configuration management? (select three) | **Ansible**, **Chef** and **Puppet** | Terraform is a provisioning tool; combining Terraform and Ansible is common. |
