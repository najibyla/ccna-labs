# CCNA Day 59 : Intro to Network Automation, AI & Machine Learning / Automatisation réseau, IA et apprentissage automatique

> Source : Jeremy's IT Lab, « Intro to Network Automation | CCNA 200-301 Day 59 (part 1) » (33 min, vidéo n°118 de la playlist) et « AI & Machine Learning | CCNA 200-301 Day 59 (part 2) » (42 min, vidéo n°119). Pas de lab pour ce jour. Fiche rédigée à partir des transcriptions le 6 octobre 2026. Sujets d'examen : section 6.0 (10 % de l'examen), en particulier 6.1, 6.2, 6.3 ; l'IA et le ML sont un ajout récent.

## 🇫🇷 Version française

## Partie 1 : introduction à l'automatisation réseau

### 1. Pourquoi automatiser

- Section 6.0 = **10 % de l'examen** : il faut **expliquer, comparer, décrire, reconnaître, interpréter**, pas automatiser soi-même (CCNP, DevNet).
- **Modèle traditionnel** : les équipements sont gérés **un par un** via SSH (ou Telnet, console, parfois GUI). Exemple : ajouter une loopback sur des centaines de routeurs. Inconvénients : **fautes de frappe** fréquentes, **chronophage et inefficace** à grande échelle, difficile de garantir la **conformité aux configurations standard** de l'entreprise (dérive au fil des modifications individuelles).
- **Bénéfices de l'automatisation** : **réduction des erreurs humaines**, **scalabilité** (déploiements, changements et dépannage en une fraction du temps), **conformité des politiques** sur tout le réseau (configurations standard, versions logicielles), **réduction de l'OpEx** (*operating expenses*, moins d'heures-homme). Un **script Python** peut faire la tâche de la loopback en quelques secondes.
- Outils et méthodes : **SDN, Ansible, Puppet, scripts Python**, et bien d'autres.

### 2. Les plans logiques (*planes*) des fonctions réseau

Un routeur ne fait pas que router (OSPF, ARP, Syslog, SSH…), un switch ne fait pas que commuter (STP, table MAC, Syslog, SSH…). Ces fonctions se classent en trois plans :

- **Plan de données** (*data plane*, aussi **forwarding plane**) : tout ce qui concerne le **transfert des données utilisateur** d'une interface à l'autre. Routeur : recherche de la route la plus spécifique, désencapsulation/réencapsulation L2 vers le prochain saut. Switch : transfert selon la MAC destination ou flooding, **ajout/retrait des tags 802.1Q**. **NAT** (modification des adresses) et **décision de transférer ou rejeter** (ACL, port security) en font partie.
- **Plan de contrôle** (*control plane*) : les fonctions qui **construisent les tables** et influencent le plan de données : table de routage (OSPF), table MAC, table ARP, STP. C'est du **travail de surcharge** (*overhead*) : OSPF ne transfère pas les données mais indique au plan de données comment le faire. En réseau traditionnel, plan de données et plan de contrôle sont **distribués** : chaque équipement a les siens.
- **Plan de gestion** (*management plane*) : surcharge aussi, mais **sans effet direct sur le transfert**. Protocoles de gestion des équipements : **SSH, Telnet, Syslog, SNMP, NTP**.
- Matériel : plans de contrôle et de gestion traités par le **CPU** ; plan de données par un **ASIC** (*Application-Specific Integrated Circuit*), puce spécialisée, car le CPU est trop lent. La **table MAC** est stockée en **TCAM** (*Ternary Content-Addressable Memory*), recherche très rapide ; la table MAC est aussi appelée **table CAM**. L'ASIC donne la MAC destination à la TCAM, qui renvoie l'entrée correspondante. Les routeurs modernes font de même. Trafic de contrôle/gestion **destiné à l'équipement** → CPU ; trafic de données **traversant** l'équipement → ASIC (pas toujours, détails au niveau CCNP).

### 3. SDN (*Software-Defined Networking*)

- Approche qui **centralise le plan de contrôle** dans une application : le **contrôleur** (comme un WLC pour les AP). Aussi appelé **software-defined architecture** ou **controller-based networking**. La part de plan de contrôle centralisée **varie selon la solution**.
- Exemple : au lieu qu'R1 et R2 échangent des routes en OSPF, le contrôleur **programme leur plan de données**.
- **SBI** (*Southbound Interface*) : communication **contrôleur ↔ équipements** (le contrôleur est dessiné en haut, les équipements au sud). Interface logicielle, pas physique : protocole de communication + **API**. Exemples : **OpenFlow, Cisco OpFlex, Cisco onePK, NETCONF**.
- **NBI** (*Northbound Interface*) : permet aux **applications** d'interagir avec le contrôleur, de lire les données collectées (équipements, topologie, interfaces, configurations) et de demander des changements. Le contrôleur expose une **API REST** (*Representational State Transfer*, un **type** d'API, pas une API précise). L'app envoie par exemple un **GET** et reçoit les données dans un **format structuré** comme **JSON ou XML**, facile à exploiter par un programme.
- Automatisation possible aussi en réseau traditionnel : scripts **Python** qui se connectent en SSH et poussent des commandes, **expressions régulières** pour analyser les `show` (format lisible par l'humain, par exemple `BW 1000000 Kbit/sec` dans `show interfaces`). Mais le SDN apporte des **données centralisées et robustes** (vue de tout le réseau), des **API nord** en JSON/XML sans parsing, l'**analytique réseau globale**, et les bénéfices de l'automatisation **sans script ni app tierce** ni expertise en automatisation. Les API permettent néanmoins des apps tierces.
- **SDN ≠ automatisation** : le SDN est un aspect de l'automatisation qui la facilite grandement.

### 4. Pièges d'examen (partie 1)

- Classer une fonction dans le bon plan : **calcul de routes = contrôle**, **NTP/SSH/Syslog/SNMP = gestion**, **NAT, ACL, tags VLAN, transfert = données**.
- **SBI** = contrôleur ↔ équipements ; **NBI** = applications ↔ contrôleur.
- Mémoriser les noms des SBI : **OpenFlow, OpFlex, onePK, NETCONF**.
- Retenir **TCAM**.

### 5. Le quiz de la partie 1 (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Bénéfices de l'automatisation réseau ? (deux réponses) | **Réduction des erreurs humaines** et **réduction de l'OpEx** | Moins de saisie manuelle dans le CLI (fautes de frappe), tâches accomplies beaucoup plus vite. |
| Lesquels sont des SBI ? (deux réponses) | **OpenFlow** et **OpFlex** | Les autres SBI de la vidéo sont Cisco onePK et NETCONF. |
| Quelle fonction serait centralisée en SDN ? | **Le calcul des routes** | Les trois autres options sont des fonctions du plan de données (transfert) ; le calcul des routes est du plan de contrôle. |
| Rôle de la SBI en architecture SDN ? | **Échange de données entre le contrôleur et les équipements réseau** | L'échange entre le contrôleur et les apps est le rôle de la NBI, pas de la SBI. |
| Dans quel plan se situe NTP ? | **Plan de gestion** | NTP fournit l'heure ; il ne transfère pas de messages et ne contrôle pas le plan de données. |

## Partie 2 : IA et apprentissage automatique

### 6. Définitions

- **IA** (*Artificial Intelligence*) : utiliser des ordinateurs pour **simuler l'intelligence** (reconnaître des motifs, apprendre, décider, résoudre des problèmes). Exemples : assistants vocaux (Siri, Alexa, Google Assistant), systèmes de recommandation (Netflix, YouTube, Amazon), voitures autonomes et robotique (Tesla FSD, Waymo), chatbots (ChatGPT ; celui de cisco.com est un **virtual concierge**), jeux (Stockfish aux échecs, AlphaGo au go). Croissance due à la puissance de calcul, au big data et aux avancées de la recherche.
- **Apprentissage automatique** (*Machine Learning*, ML) : **sous-ensemble de l'IA** où l'ordinateur **apprend à partir des données** et s'améliore **sans programmation explicite**. Trois parties : **données d'entrée → entraînement du modèle (repérage de motifs) → prédictions ou décisions sur de nouvelles données**. Exemples : filtre anti-spam, recommandations, détection de fraude bancaire, traitement du langage naturel. Toute IA n'utilise pas le ML, mais ChatGPT serait impossible sans.

### 7. Les quatre types de ML à connaître

| Type | Principe | Avantages | Inconvénients |
| :--- | :--- | :--- | :--- |
| **Supervisé** (*supervised*) | Données **étiquetées** (photos « chat »/« chien ») ; le modèle apprend la relation données ↔ étiquettes puis classe de nouvelles données | **Très précis** si des données étiquetées existent ; simple à comprendre et à implémenter | Exige de **grands jeux de données étiquetés** (coûteux, long) ; sortie **limitée aux étiquettes** d'entraînement (un oiseau ne sera pas reconnu) |
| **Non supervisé** (*unsupervised*) | Données **non étiquetées** ; le modèle trouve seul des motifs et regroupe en **clusters** (cluster 1 = chats, cluster 2 = chiens) ; un humain nomme les clusters ; un oiseau crée un nouveau cluster | **Pas d'étiquetage** (temps, coût) ; révèle des **motifs cachés** (segmentation de clients) | **Interprétation humaine** encore nécessaire ; précision possiblement **inférieure** au supervisé pour une tâche donnée |
| **Par renforcement** (*reinforcement*) | Le modèle (**agent**) agit dans un **environnement** et reçoit **récompenses ou pénalités** ; voitures autonomes, jeux (échecs, go, jeux vidéo), robotique ; exemple MarI/O (SethBling) sur Super Mario World | Apprend des **comportements complexes** difficiles à programmer ; s'adapte aux **environnements dynamiques** | **Gourmand en ressources** ; si le système de récompenses est mal conçu, l'agent privilégie le **court terme** |
| **Profond** (*deep learning*) | Sous-ensemble du ML à **réseaux de neurones artificiels** inspirés du cerveau : **couche d'entrée, couches cachées** (parfois des milliers), **couche de sortie** ; peut être entraîné en supervisé, non supervisé ou renforcement | Excelle sur les **grands jeux de données non structurés** (images, audio, texte) ; performances de pointe (reconnaissance d'images, NLP, conduite autonome) | **Très gourmand** en calcul et en données ; **« boîte noire »** (difficile d'expliquer la décision) |

Ces types ne sont pas exclusifs et se combinent ; il existe aussi l'**apprentissage semi-supervisé** (données étiquetées + non étiquetées).

### 8. IA prédictive et IA générative

- **IA prédictive** : analyse des **données historiques** pour **prédire** des résultats ou tendances. Exemples : santé (progression de maladies, lecture de radios), **détection d'anomalies de sécurité réseau**, gestion du trafic (routier ou réseau : congestion, goulets d'étranglement), ventes, météo. Avantage : **meilleure prise de décision**, problèmes détectés avant qu'ils surviennent. Inconvénients : exige des **données historiques abondantes et de qualité** ; si le futur diffère beaucoup du passé, le modèle se trompe.
- **IA générative** : apprend des motifs et **crée du contenu nouveau** (texte, images, audio). Texte : ChatGPT, Gemini, Copilot (**LLM**, *large language models*) ; images : Midjourney, DALL-E ; vidéo : Sora (OpenAI), Veo 2 (Google). Avantages : tâches créatives, automatisation de la création de contenu (support client). Inconvénients : **mésusage** (deepfakes, plagiat), qualité dépendante des données et du modèle (« AI slop », cours CCNA entièrement générés), **droits d'auteur**, **hallucinations** (réponses inventées) : Jeremy déconseille les LLM pour réviser le CCNA.
- Les IA prédictives et génératives les plus puissantes reposent sur le deep learning, mais des IA plus simples existent hors deep learning.

### 9. Applications au réseau et Cisco Catalyst Center

- **Prédictive** : **prévision de trafic** (augmenter la bande passante avec EtherChannel, ajuster la QoS), **détection de menaces**, **maintenance prédictive** (remplacer le matériel avant la panne).
- **Générative** : **documentation** du réseau, **génération de configurations** à partir d'un schéma, **conception** réseau, **dépannage** à partir de logs ou messages d'erreur, **génération de scripts** d'automatisation (Python). **Toujours vérifier** ce que produit ChatGPT avant de l'utiliser en production.
- **Cisco Catalyst Center** (ex-**DNA Center**), fonctions IA (non listées explicitement dans les sujets d'examen) :
  - **AI Network Analytics** : terme englobant ; établit la **ligne de base** (*baseline*, le « normal » du réseau), fournit recommandations, prédit et détecte les anomalies (exemple : temps d'obtention d'un bail DHCP, d'authentification et d'association Wi-Fi, valeur prédite en vert, réelle en bleu).
  - **MRE** (*Machine Reasoning Engine*) : **analyse de cause racine** des problèmes, propose des résolutions ou applique des **actions correctives automatiques** (exemple : interface down).
  - **AI Endpoint Analytics** : identifie et classe les **terminaux**, détecte appareils non autorisés et comportements inhabituels, automatise le **profilage et la segmentation** à la connexion (politiques de sécurité appliquées selon le type d'appareil).
  - **AI-enhanced RRM** (*Radio Resource Management*) : Wi-Fi ; équilibrage de charge entre AP, choix des **canaux** pour réduire les interférences, ajustement de la **puissance d'émission**.

### 10. Pièges d'examen (partie 2)

- **ML ⊂ IA** ; supervisé, non supervisé, renforcement, profond ⊂ ML. **Deep learning = réseaux de neurones = imite le cerveau.**
- **Supervisé = données étiquetées** ; **non supervisé = non étiquetées, motifs cachés** ; **renforcement = récompense/pénalité**.
- Le deep learning **n'est pas obligatoire** pour une IA prédictive ou générative.
- **MRE** = cause racine + résolution.

### 11. Le quiz de la partie 2 (3 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quel type de ML imite le cerveau humain ? | **Deep learning** | Réseaux de neurones artificiels multicouches, traitement hiérarchique comme le cerveau. |
| Quelle fonction de Catalyst Center fait une analyse de cause racine et propose des résolutions ? | **MRE** (Machine Reasoning Engine) | Il peut aussi appliquer des actions correctives automatiques sans intervention humaine. |
| Affirmations vraies ? (trois réponses : A, D, F) | **Le renforcement repose sur récompenses/pénalités** ; **il est efficace pour les IA de jeux** ; **le non supervisé utilise des données non étiquetées pour trouver des motifs** | B faux : le supervisé travaille sur des données déjà étiquetées, pas pour découvrir des motifs cachés. C faux : le deep learning n'est pas une obligation stricte pour une IA prédictive ou générative. E faux : supervisé et non supervisé se complètent (semi-supervisé). |

---

## 🇬🇧 English version

## Part 1: Intro to network automation

### 1. Why automate

- Section 6.0 = **10% of the exam**: you must **explain, compare, describe, recognize, interpret**, not automate yourself (CCNP, DevNet).
- **Traditional model**: devices are managed **one at a time** via SSH (or Telnet, console, sometimes a GUI). Example: adding a loopback on hundreds of routers. Downsides: frequent **typos**, **time-consuming and inefficient** at scale, hard to ensure **adherence to standard configurations** (configurations drift as individual changes accumulate).
- **Benefits of automation**: **reduced human error**, **scalability** (deployments, changes and troubleshooting in a fraction of the time), **network-wide policy compliance** (standard configs, software versions), **reduced OpEx** (operating expenses, fewer man-hours). A **Python script** can do the loopback task in seconds.
- Tools and methods: **SDN, Ansible, Puppet, Python scripts**, and many more.

### 2. The logical planes of network functions

A router does more than route (OSPF, ARP, Syslog, SSH...), a switch more than switch (STP, MAC table, Syslog, SSH...). These functions fall into three planes:

- **Data plane** (also **forwarding plane**): everything involved in **forwarding user data** from one interface to another. Router: most specific route lookup, de-encapsulating/re-encapsulating the L2 header for the next hop. Switch: forwarding by destination MAC or flooding, **adding/removing 802.1Q tags**. **NAT** (changing addresses) and the **decision to forward or discard** (ACLs, port security) are part of it.
- **Control plane**: functions that **build the tables** and influence the data plane: routing table (OSPF), MAC table, ARP table, STP. This is **overhead work**: OSPF does not forward data but tells the data plane how to. In traditional networking, data and control planes are **distributed**: each device has its own.
- **Management plane**: overhead too, but **no direct effect on forwarding**. Device management protocols: **SSH, Telnet, Syslog, SNMP, NTP**.
- Hardware: control and management planes handled by the **CPU**; data plane by an **ASIC** (Application-Specific Integrated Circuit), a purpose-built chip, because the CPU is too slow. The **MAC address table** is stored in **TCAM** (Ternary Content-Addressable Memory), very fast lookups; the MAC table is also called the **CAM table**. The ASIC feeds the destination MAC into the TCAM, which returns the matching entry. Modern routers work similarly. Control/management traffic **destined to the device** → CPU; data traffic **passing through** → ASIC (not always; CCNP-level detail).

### 3. SDN (Software-Defined Networking)

- An approach that **centralizes the control plane** in an application: the **controller** (like a WLC for APs). Also called **software-defined architecture** or **controller-based networking**. How much of the control plane is centralized **varies by solution**.
- Example: instead of R1 and R2 exchanging routes with OSPF, the controller **programs their data planes**.
- **SBI** (Southbound Interface): communication **controller ↔ network devices** (the controller is drawn on top, devices to the south). A software interface, not physical: communication protocol + **API**. Examples: **OpenFlow, Cisco OpFlex, Cisco onePK, NETCONF**.
- **NBI** (Northbound Interface): lets **applications** interact with the controller, read the data it gathers (devices, topology, interfaces, configurations) and request changes. The controller exposes a **REST API** (Representational State Transfer, a **type** of API, not a specific one). The app sends e.g. a **GET** and receives data in a **structured format** such as **JSON or XML**, easy for programs to use.
- Automation is possible in traditional networks too: **Python** scripts that SSH to devices and push commands, **regular expressions** to parse `show` output (human-readable, e.g. `BW 1000000 Kbit/sec` in `show interfaces`). But SDN provides **robust, centralized data** (network-wide view), **northbound APIs** returning JSON/XML without parsing, **network-wide analytics**, and automation benefits **without third-party apps or scripts** or automation expertise. APIs still allow powerful third-party apps.
- **SDN ≠ automation**: SDN is one aspect of network automation that greatly facilitates it.

### 4. Exam traps (part 1)

- Put each function in the right plane: **calculating routes = control**, **NTP/SSH/Syslog/SNMP = management**, **NAT, ACLs, VLAN tags, forwarding = data**.
- **SBI** = controller ↔ devices; **NBI** = apps ↔ controller.
- Memorize the SBI names: **OpenFlow, OpFlex, onePK, NETCONF**.
- Remember **TCAM**.

### 5. Part 1 quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Benefits of network automation? (select two) | **Reduced human error** and **reduced OpEx** | Less manual CLI input (typos), tasks done much faster. |
| Which are SBIs? (select two) | **OpenFlow** and **OpFlex** | The other SBIs in the video are Cisco onePK and NETCONF. |
| Which function would be centralized in SDN? | **Calculating routes** | The other three options are data plane functions (forwarding); calculating routes is a control plane function. |
| Purpose of the SBI in SDN architecture? | **Data exchange between the controller and network devices** | Exchange between the controller and apps is the NBI's role, not the SBI's. |
| Which plane does NTP fit in? | **Management plane** | NTP provides accurate time; it does not forward messages or control the data plane. |

## Part 2: AI and machine learning

### 6. Definitions

- **AI** (Artificial Intelligence): using computers to **simulate intelligence** (recognizing patterns, learning, making decisions, solving problems). Examples: virtual assistants (Siri, Alexa, Google Assistant), recommendation systems (Netflix, YouTube, Amazon), self-driving cars and robotics (Tesla FSD, Waymo), chatbots (ChatGPT; the one on cisco.com is a **virtual concierge**), games (Stockfish in chess, AlphaGo in Go). Growth driven by computing power, big data and research breakthroughs.
- **Machine learning** (ML): a **subset of AI** where computers **learn from data** and improve **without explicit programming**. Three parts: **input data → model training (finding patterns) → predictions or decisions on new data**. Examples: spam filtering, recommendations, bank fraud detection, natural language processing. Not all AI uses ML, but ChatGPT would be impossible without it.

### 7. The four ML types to know

| Type | Principle | Advantages | Disadvantages |
| :--- | :--- | :--- | :--- |
| **Supervised** | **Labeled** data ("cat"/"dog" photos); the model learns the data ↔ label relationship, then classifies new data | **Highly accurate** when labeled data exists; straightforward to understand and implement | Requires **large labeled datasets** (expensive, time-consuming); output **limited to training labels** (a bird is not recognized) |
| **Unsupervised** | **Unlabeled** data; the model finds patterns on its own and groups data into **clusters** (cluster 1 = cats, cluster 2 = dogs); a human labels the clusters; a bird creates a new cluster | **No labeling** needed (time, cost); reveals **hidden patterns** (customer segmentation) | **Human interpretation** still required; accuracy may be **lower** than supervised for specific tasks |
| **Reinforcement** | The model (**agent**) acts in an **environment** and receives **rewards or penalties**; self-driving cars, games (chess, Go, video games), robotics; example MarI/O (SethBling) on Super Mario World | Learns **complex behaviors** hard to program manually; adapts to **dynamic environments** | **Resource-intensive**; a poorly designed reward system makes the agent favor **short-term** rewards |
| **Deep learning** | Subset of ML using **artificial neural networks** inspired by the brain: **input layer, hidden layers** (sometimes thousands), **output layer**; can be trained with supervised, unsupervised or reinforcement methods | Excels at **large unstructured datasets** (images, audio, text); state-of-the-art performance (image recognition, NLP, autonomous driving) | **Very resource-intensive** in compute and data; a **"black box"** (hard to explain decisions) |

These types are not exclusive and can be combined; **semi-supervised learning** (labeled + unlabeled data) also exists.

### 8. Predictive and generative AI

- **Predictive AI**: analyzes **historical data** to **forecast** outcomes or trends. Examples: healthcare (disease progression, reading X-rays), **network security anomaly detection**, traffic management (road or network: congestion, bottlenecks), sales, weather. Advantage: **better decision-making**, problems detected before they occur. Disadvantages: needs **high-quality, abundant historical data**; if the future differs from the past, the model struggles.
- **Generative AI**: learns patterns and **creates new content** (text, images, audio). Text: ChatGPT, Gemini, Copilot (**LLMs**, large language models); images: Midjourney, DALL-E; video: Sora (OpenAI), Veo 2 (Google). Advantages: creative tasks, automated content creation (customer service). Disadvantages: **misuse** (deepfakes, plagiarism), quality depends on training data and model ("AI slop", entirely AI-generated CCNA courses), **copyright** issues, **hallucinations** (made-up answers): Jeremy recommends avoiding LLMs when studying for the CCNA.
- The most powerful predictive and generative AIs rely on deep learning, but simpler ones exist outside deep learning.

### 9. Networking applications and Cisco Catalyst Center

- **Predictive**: **traffic forecasting** (add bandwidth with EtherChannel, tune QoS), **security threat detection**, **predictive maintenance** (replace hardware before failure).
- **Generative**: network **documentation**, **configuration generation** from a diagram, network **design**, **troubleshooting** from logs or error messages, **script generation** (Python). **Always verify** ChatGPT's output before using it in a real network.
- **Cisco Catalyst Center** (formerly **DNA Center**), AI features (not explicitly listed in the exam topics):
  - **AI Network Analytics**: umbrella term; establishes the **baseline** (what is "normal"), provides insights and recommendations, predicts and detects anomalies (example: DHCP lease, Wi-Fi authentication and association times, predicted range in green, actual value in blue).
  - **MRE** (Machine Reasoning Engine): **root-cause analysis** of issues, suggests resolutions or takes **automated corrective actions** (example: an interface down).
  - **AI Endpoint Analytics**: identifies and classifies **endpoints**, detects unauthorized devices and unusual behavior, automates **profiling and segmentation** on connection (security policies applied by device type).
  - **AI-enhanced RRM** (Radio Resource Management): Wi-Fi; load balancing among APs, **channel selection** to reduce interference, **transmit power** adjustment.

### 10. Exam traps (part 2)

- **ML ⊂ AI**; supervised, unsupervised, reinforcement, deep ⊂ ML. **Deep learning = neural networks = imitates the brain.**
- **Supervised = labeled data**; **unsupervised = unlabeled, hidden patterns**; **reinforcement = reward/penalty**.
- Deep learning is **not required** for predictive or generative AI.
- **MRE** = root cause + resolution.

### 11. Part 2 quiz (3 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which ML type imitates the human brain? | **Deep learning** | Multi-layer artificial neural networks, hierarchical processing like the brain. |
| Which Catalyst Center feature performs root-cause analysis and proposes resolutions? | **MRE** (Machine Reasoning Engine) | It can also take automated corrective actions without human intervention. |
| True statements? (select three: A, D, F) | **Reinforcement learning relies on rewards/penalties**; **it is effective for game AIs**; **unsupervised learning uses unlabeled data to find patterns** | B wrong: supervised learning works with already-labeled data, not suited to discovering hidden patterns. C wrong: deep learning is not a strict requirement for predictive or generative AI. E wrong: supervised and unsupervised can complement each other (semi-supervised). |
