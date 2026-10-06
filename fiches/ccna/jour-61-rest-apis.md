# CCNA Day 61 : REST APIs & REST API Authentication / API REST et authentification

> Source : Jeremy's IT Lab, « Free CCNA | REST APIs | Day 61 » (32 min, vidéo n°121 de la playlist) et « REST API Authentication | CCNA 200-301 Day 61 (part 2) » (29 min, vidéo n°122). Pas de lab Packet Tracer pour ce jour ; la partie 1 contient une démonstration avec Postman et Cisco DevNet. Fiche rédigée à partir des transcriptions le 6 octobre 2026. Sujet d'examen : 6.5 (caractéristiques des API REST), auquel Cisco a récemment ajouté l'authentification.

## 🇫🇷 Version française

## Partie 1 : les API REST

### 1. Rappel sur les API

- **API** (*Application Programming Interface*) : interface logicielle qui permet à **deux applications de communiquer**. En SDN, les API servent entre apps et contrôleur (**NBI**, en général **REST**) et entre contrôleur et équipements (**SBI**, par exemple **NETCONF, RESTCONF**, à voir au CCNP).

### 2. CRUD et HTTP

- **CRUD** = **Create, Read, Update, Delete** : créer une variable et sa valeur initiale (`ip_address` = `10.1.1.1`), lire sa valeur, la modifier (`10.2.3.4`), la supprimer.
- HTTP utilise des **verbes** (ou **méthodes**) qui correspondent aux opérations CRUD, raison pour laquelle les API REST utilisent le plus souvent **HTTP** comme protocole applicatif :

| Opération CRUD | Verbe HTTP |
| :--- | :--- |
| Create | **POST** |
| Read | **GET** |
| Update | **PUT** ou **PATCH** |
| Delete | **DELETE** |

- Une **requête HTTP** contient un verbe et un **URI** (*Uniform Resource Identifier*) qui identifie la ressource. Trois parties de l'URI : le **scheme** (protocole, HTTP ou HTTPS), l'**authority** (adresse ou nom d'hôte) et le **path** (la ressource). Un **URL** est un type d'URI.
- Les requêtes contiennent aussi des **en-têtes** (*headers*), par exemple **Accept** qui indique au serveur les types de données acceptés en retour (JSON, XML). Structure : en-tête IP, en-tête TCP, verbe + URI, en-têtes, données.
- **REST n'est pas obligé d'utiliser HTTP**, mais c'est le choix le plus courant ; pour le CCNA, supposer que les API REST utilisent HTTP (ou plus souvent **HTTPS**). HTTP = protocole de communication ; REST = cadre de conception d'API.

### 3. Les codes de réponse HTTP

Le **premier chiffre** indique la classe :

| Classe | Signification | Exemples |
| :--- | :--- | :--- |
| **1xx** Informational | Requête reçue, suite selon les deux autres chiffres | **102 Processing** (reçue, en cours, réponse pas encore disponible) |
| **2xx** Successful | Requête reçue, comprise et acceptée | **200 OK** (succès ; pour un GET, la ressource est dans le corps), **201 Created** (nouvelle ressource créée, par exemple après un POST) |
| **3xx** Redirection | Une action supplémentaire est nécessaire | **301 Moved Permanently** (le serveur indique le nouvel emplacement) |
| **4xx** Client error | Erreur dans la requête, impossible à satisfaire | **403 Unauthorized** (le client doit s'**authentifier** ; « unauthenticated » serait plus juste), **404 Not Found** (ressource inexistante, exemple google.com/jeremysitlab) |
| **5xx** Server error | Requête valide mais le serveur ne peut pas la satisfaire | **500 Internal Server Error** (situation inattendue) |

### 4. Les caractéristiques des API REST

- **REST** = *Representational State Transfer* ; API REST = REST-based = RESTful. REST n'est pas une API précise mais un **ensemble de règles** (un cadre). **Six contraintes** : **uniform interface**, **client-server**, **stateless**, **cacheable** (ou non), **layered system**, et optionnellement **code-on-demand** (le client télécharge et exécute du code du serveur). Trois à connaître :
  - **Client-serveur** : le client fait des **appels d'API** (requêtes HTTP) vers les ressources du serveur ; client et serveur **évoluent indépendamment** sans casser l'interface.
  - **Sans état** (*stateless*) : chaque échange est un **événement séparé**, indépendant des précédents ; le serveur ne garde pas d'information sur les requêtes passées ; **si l'authentification est requise, le client s'authentifie à chaque requête**. Comparaison : **TCP est stateful** (connexions, numéros de séquence et d'acquittement), **UDP est stateless**. Même si HTTP utilise TCP, **HTTP et REST ne sont pas stateful** : les couches sont indépendantes.
  - **Cacheable ou non** : le **cache** (stocker des données pour un usage futur, comme un navigateur) **doit être pris en charge**, mais toutes les ressources n'ont pas à être cacheables ; les ressources cacheables doivent être **déclarées comme telles** par le serveur.

### 5. Démonstration : Cisco DevNet et Postman

- **Cisco DevNet** : programme développeur de Cisco (cours, tutoriels, labs, **sandboxes** toujours actives, documentation), gratuit ; parcours de certification **DevNet** (DevNet Associate après le CCNA). **Postman** : plateforme pour construire et utiliser des API (app de bureau ou navigateur). Tutoriel suivi : « DevNet DNA Center getting started » ; **DNA Center** est un contrôleur SDN de Cisco.
- Appel 1 : **POST** vers l'URL du tutoriel, onglet Authorization > **Basic Auth**, utilisateur **devnetuser**, mot de passe **Cisco123!** → réponse **200 OK** avec un **jeton d'autorisation** (*authorization token*) en JSON ; copier la valeur sans les guillemets.
- Appel 2 : **GET** vers une autre URL, en-tête **`X-Auth-Token`** = le jeton → **200 OK** et l'**inventaire des équipements** en JSON : famille « switches or hubs », rôle **access**, hostname **leaf1.abc.com** (switch leaf en spine-leaf), platform ID **C9300-24U** (Catalyst 9300), uptime, etc.

### 6. Le quiz de la partie 1 (5 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Code attendu pour un GET sur une ressource inexistante ? | **404** | Not Found. |
| Laquelle n'est PAS une contrainte REST ? | **Stateful** | REST est stateless : chaque requête est unique et indépendante. Les cinq autres contraintes plus le code-on-demand optionnel sont REST. |
| Classe de réponse pour une requête réussie ? | **Code commençant par 2** | Par exemple 200 OK ou 201 Created. |
| PUT et PATCH équivalent à quelle opération CRUD ? | **U (Update)** | PUT est parfois classé Create car il peut créer des variables, mais il sert surtout à mettre à jour. |
| Qu'attend-on comme scheme d'un URI ? | **HTTPS** | Le scheme identifie le protocole, typiquement HTTP ou HTTPS. |

## Partie 2 : l'authentification des API REST

### 7. Pourquoi authentifier

- **Authentification** : valider l'identité d'un utilisateur ou système pour un accès légitime aux ressources (ici l'application et ses données). Sans elle, n'importe qui peut envoyer des **appels d'API** (*API calls*, *API requests*) et lire ou modifier des données sensibles. Certaines API sont volontairement **ouvertes** (données publiques).
- L'authentification sert aussi au **suivi d'usage** (analytique, facturation) : exemple de l'**API ChatGPT**, facturée aux **tokens** (morceaux de texte en entrée ou sortie).
- Termes techniques : **méthodes** ou **schémas** d'authentification.

### 8. Structure d'un message HTTP

- **Start line** : méthode (**POST**), URL (**api/v1/acl/rules**), version HTTP (**2**). Puis les **en-têtes** (métadonnées : authentification, type de contenu, client), une **ligne vide**, puis le **corps** du message. Le tout est encapsulé dans un segment TCP.
- L'authentification se trouve dans l'en-tête **`Authorization`** (son vrai rôle est d'authentifier, l'autorisation en découle).

### 9. Les quatre méthodes

| Méthode | Fonctionnement | Avantages | Inconvénients |
| :--- | :--- | :--- | :--- |
| **Basic authentication** | **Nom d'utilisateur et mot de passe dans chaque requête**, au format `username:password` **encodé en Base64** dans l'en-tête Authorization (`jeremy:ccna` → une chaîne Base64). **Encoder ≠ chiffrer** : Base64 se décode facilement (base64decode.org) | Simple à implémenter | Identifiants envoyés à chaque requête, volables si la connexion n'est pas protégée ; même avec HTTPS, un simple couple identifiant/mot de passe reste peu sûr (ingénierie sociale) |
| **Bearer authentication** | Authentification **par jeton** (*token-based*) : le client obtient d'abord un **bearer token** auprès d'un **serveur d'autorisation** (*auth server*, souvent distinct du serveur de ressources ; cette étape peut utiliser la basic auth), puis l'inclut dans chaque requête : **`Authorization: Bearer <token>`**. « Bearer » = **quiconque possède le jeton peut l'utiliser**, d'où des jetons qui **expirent** (de 15 minutes à des semaines ou mois) | Plus sûr que basic : pas de mot de passe à chaque appel ; un jeton volé n'est valide que temporairement | Jeton volé utilisable jusqu'à expiration ; rafraîchissement périodique = complexité pour les développeurs ; HTTPS obligatoire |
| **API key authentication** | **Clé statique** délivrée par le fournisseur de l'API, envoyée à chaque appel. **N'expire pas automatiquement**, valide jusqu'à **révocation**. Transport : en-tête **Authorization** (**recommandé**), paramètre dans l'**URL** (déconseillé : les URL sont journalisées par serveurs, proxies, navigateurs), ou **cookie** (API navigateur) | Plus facile à implémenter que bearer ; **suivi d'usage** par client (clé unique par client) ; courant dans le cloud et les **API tierces** (exemple : une app chatbot qui appelle l'API d'OpenAI ; utilisateurs = première partie, développeur = deuxième, OpenAI = troisième) | Clé volée = **accès complet jusqu'à révocation** ; **rotation manuelle** nécessaire |
| **OAuth 2.0** | Cadre d'**authentification sécurisé** pour la **délégation d'accès** : un **tiers** obtient un **accès limité** aux ressources **au nom du propriétaire**, **sans partager ses identifiants** (« Log in with Google » : le site ne voit jamais le mot de passe Google ; apps connectées aux réseaux sociaux ; intégration d'agenda). Défini dans la **RFC 6749** | Pas d'exposition des identifiants ; l'utilisateur contrôle les informations partagées ; **refresh tokens** pour continuer sans se reconnecter | (Non détaillé dans la vidéo) |

**OAuth 2.0 : quatre parties et six étapes**

- **Resource owner** (propriétaire du compte Google), **client app** (app tierce, par exemple un outil de planification), **auth server** (délivre les **access tokens**, le service OAuth de Google), **resource server** (héberge la ressource, les données Google Calendar).
- 1) Le client app demande l'autorisation au propriétaire ; 2) le propriétaire **accorde l'autorisation** (connexion à Google, permission) ; 3) le client app échange cet **authorization grant** contre un jeton auprès de l'auth server ; 4) l'auth server délivre un **access token** ; 5) le client app inclut le jeton dans sa requête au resource server ; 6) le resource server **valide le jeton** et fournit la ressource.
- L'**access token** fonctionne comme un bearer token, limité à une **portée** (*scope*, par exemple lecture seule) et **expire** rapidement ; un **refresh token** délivré par l'auth server permet d'obtenir un nouvel access token **sans interaction de l'utilisateur**.

### 10. Pièges d'examen

- **Base64 = encodage, pas chiffrement** ; **HTTPS** (HTTP + **TLS**) est indispensable pour **toutes** les méthodes.
- **Bearer token et access token OAuth expirent** ; une **clé d'API n'expire pas** (moins sûre, rotation manuelle).
- **Clé d'API dans l'en-tête Authorization**, jamais dans l'URL.
- Seules **bearer** et **OAuth 2.0** font intervenir un **auth server** qui délivre des jetons.
- **403** = il faut s'authentifier ; **404** = ressource introuvable ; **2xx** = succès.

### 11. Le quiz de la partie 2 (3 questions)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Quelles méthodes font intervenir un auth server qui délivre des jetons ? (deux réponses) | **OAuth 2.0** et **bearer authentication** | La basic auth n'a pas d'auth server (simple identifiant/mot de passe), ni l'API key (clé statique). |
| Comment OAuth 2.0 améliore-t-il la sécurité ? | **Les apps tierces accèdent aux ressources sans exposer les identifiants de l'utilisateur** | Le client app reçoit un access token de l'auth server (étape 4) et s'authentifie avec auprès du resource server (étape 5). |
| Affirmations vraies ? (trois réponses : B, C, E) | **La bearer auth exige un jeton** ; **OAuth 2.0 permet la délégation d'accès** ; **un refresh token obtient automatiquement un nouvel access token** | A faux : les clés d'API n'expirent pas automatiquement. D faux : la basic auth n'utilise pas de chiffrement, seulement Base64 réversible. F faux : les clés d'API ne doivent pas être dans l'URL mais dans l'en-tête Authorization. |

---

## 🇬🇧 English version

## Part 1: REST APIs

### 1. API review

- **API** (Application Programming Interface): software interface that allows **two applications to communicate**. In SDN, APIs are used between apps and the controller (**NBI**, typically **REST**) and between the controller and devices (**SBI**, e.g. **NETCONF, RESTCONF**, CCNP material).

### 2. CRUD and HTTP

- **CRUD** = **Create, Read, Update, Delete**: create a variable with its initial value (`ip_address` = `10.1.1.1`), read its value, change it (`10.2.3.4`), delete it.
- HTTP uses **verbs** (or **methods**) that map to CRUD operations, which is why REST APIs typically use **HTTP** as their application-layer protocol:

| CRUD operation | HTTP verb |
| :--- | :--- |
| Create | **POST** |
| Read | **GET** |
| Update | **PUT** or **PATCH** |
| Delete | **DELETE** |

- An **HTTP request** includes a verb and a **URI** (Uniform Resource Identifier) indicating the resource. Three URI sections: the **scheme** (protocol, HTTP or HTTPS), the **authority** (address or hostname) and the **path** (the resource). A **URL** is a type of URI.
- Requests also carry **headers**, e.g. **Accept**, which tells the server which data types the client accepts back (JSON, XML). Structure: IP header, TCP header, verb + URI, headers, data.
- **REST does not have to use HTTP**, but it is the most common choice; for the CCNA, assume REST APIs use HTTP (or more often **HTTPS**). HTTP = a communication protocol; REST = a framework for building APIs.

### 3. HTTP response codes

The **first digit** indicates the class:

| Class | Meaning | Examples |
| :--- | :--- | :--- |
| **1xx** Informational | Request received; exact meaning depends on the other two digits | **102 Processing** (received, being processed, response not yet available) |
| **2xx** Successful | Request received, understood and accepted | **200 OK** (success; for a GET the resource is in the body), **201 Created** (new resource created, e.g. after a POST) |
| **3xx** Redirection | Further action required | **301 Moved Permanently** (server indicates the new location) |
| **4xx** Client error | Error in the request, cannot be fulfilled | **403 Unauthorized** (client must **authenticate**; "unauthenticated" would be a better name), **404 Not Found** (resource does not exist, e.g. google.com/jeremysitlab) |
| **5xx** Server error | Valid request but the server cannot fulfill it | **500 Internal Server Error** (unexpected situation) |

### 4. Characteristics of REST APIs

- **REST** = Representational State Transfer; REST APIs = REST-based = RESTful. REST is not a specific API but a **set of rules** (a framework). **Six constraints**: **uniform interface**, **client-server**, **stateless**, **cacheable** (or non-cacheable), **layered system**, and optionally **code-on-demand** (the client downloads and executes code from the server). Three to know:
  - **Client-server**: the client uses **API calls** (HTTP requests) to access resources on the server; client and server **evolve independently** without breaking the interface.
  - **Stateless**: each exchange is a **separate event**, independent of past exchanges; the server stores no information about previous requests; **if authentication is required, the client authenticates on every request**. Comparison: **TCP is stateful** (connections, sequence and acknowledgment numbers), **UDP is stateless**. Although HTTP uses TCP, **HTTP and REST are not stateful**: the layers are independent.
  - **Cacheable or non-cacheable**: **caching** (storing data for future use, like a browser) **must be supported**, but not every resource must be cacheable; cacheable resources must be **declared as such** by the server.

### 5. Demo: Cisco DevNet and Postman

- **Cisco DevNet**: Cisco's developer program (courses, tutorials, labs, always-on **sandboxes**, documentation), free; **DevNet** certification track (DevNet Associate after the CCNA). **Postman**: a platform for building and using APIs (desktop app or browser). Tutorial followed: "DevNet DNA Center getting started"; **DNA Center** is a Cisco SDN controller.
- Call 1: **POST** to the tutorial URL, Authorization tab > **Basic Auth**, username **devnetuser**, password **Cisco123!** → **200 OK** response with an **authorization token** in JSON; copy the value without the quotes.
- Call 2: **GET** to another URL, header **`X-Auth-Token`** = the token → **200 OK** and the **device inventory** in JSON: family "switches or hubs", role **access**, hostname **leaf1.abc.com** (a leaf switch in spine-leaf), platform ID **C9300-24U** (Catalyst 9300), uptime, etc.

### 6. Part 1 quiz (5 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Expected code for a GET on a resource that does not exist? | **404** | Not Found. |
| Which is NOT a constraint of RESTful architecture? | **Stateful** | REST is stateless: each request is a unique event independent of previous ones. The other five constraints plus optional code-on-demand are REST. |
| Response class for a successful request? | **Code beginning with 2** | E.g. 200 OK or 201 Created. |
| PUT and PATCH are equivalent to which CRUD operation? | **U (Update)** | PUT is sometimes categorized as Create since it can create variables, but it is usually an Update. |
| Expected scheme of a URI? | **HTTPS** | The scheme identifies the protocol, typically HTTP or HTTPS. |

## Part 2: REST API authentication

### 7. Why authenticate

- **Authentication**: validating the identity of a user or system to ensure legitimate access to resources (here the application and its data). Without it, anyone can send **API calls** (**API requests**) and read or modify sensitive data. Some APIs are intentionally **open** (public data).
- Authentication also enables **usage tracking** (analytics, billing): example of the **ChatGPT API**, billed by **tokens** (chunks of input or output text).
- Technical terms: authentication **methods** or **schemes**.

### 8. Structure of an HTTP message

- **Start line**: method (**POST**), URL (**api/v1/acl/rules**), HTTP version (**2**). Then the **headers** (metadata: authentication, content type, client), a **blank line**, then the **message body**. All encapsulated in a TCP segment.
- Authentication lives in the **`Authorization`** header (its real purpose is to authenticate; authorization follows).

### 9. The four methods

| Method | How it works | Advantages | Disadvantages |
| :--- | :--- | :--- | :--- |
| **Basic authentication** | **Username and password in every request**, as `username:password` **encoded in Base64** in the Authorization header (`jeremy:ccna` → a Base64 string). **Encoding ≠ encryption**: Base64 is easily decoded (base64decode.org) | Simple, easy to implement | Credentials sent in every request, stealable if the connection is not secured; even with HTTPS, a username/password alone is not very secure (social engineering) |
| **Bearer authentication** | **Token-based**: the client first obtains a **bearer token** from an **authorization server** ("auth server", usually separate from the resource server; this step may use basic auth), then includes it in each request: **`Authorization: Bearer <token>`**. "Bearer" = **anyone who possesses the token can use it**, hence tokens that **expire** (15 minutes to weeks or months) | More secure than basic: no password on every call; a stolen token is only temporarily valid | Stolen token usable until expiry; periodic refresh adds complexity for developers; HTTPS required |
| **API key authentication** | **Static key** issued by the API provider, sent with each call. **Does not expire automatically**, valid until **revoked**. Transport: **Authorization** header (**recommended**), parameter in the **URL** (not recommended: URLs are logged by servers, proxies, browsers), or **cookie** (browser-based APIs) | Easier to implement than bearer; **usage tracking** per client (unique key per customer); common in cloud services and **third-party APIs** (e.g. a chatbot app calling OpenAI's API; users = first party, developer = second, OpenAI = third) | Stolen key = **full access until revoked**; **manual rotation** required |
| **OAuth 2.0** | **Secure authentication framework** for **access delegation**: a **third party** gets **limited access** to resources **on behalf of the owner**, **without sharing the owner's credentials** ("Log in with Google": the website never sees your Google password; apps connected to social media; calendar integration). Defined in **RFC 6749** | No credential exposure; the user controls what is shared; **refresh tokens** maintain access without re-login | (Not detailed in the video) |

**OAuth 2.0: four parties and six steps**

- **Resource owner** (the Google account owner), **client app** (third-party app, e.g. a scheduling tool), **auth server** (issues **access tokens**; Google's OAuth service), **resource server** (hosts the resource; the Google Calendar data).
- 1) The client app requests authorization from the resource owner; 2) the owner **grants authorization** (logs into Google, gives permission); 3) the client app exchanges this **authorization grant** for a token from the auth server; 4) the auth server issues an **access token**; 5) the client app includes the token in its request to the resource server; 6) the resource server **validates the token** and provides the resource.
- The **access token** works like a bearer token, limited to a **scope** (e.g. read-only) and **expires** after a short period; a **refresh token** from the auth server obtains a new access token **without user interaction**.

### 10. Exam traps

- **Base64 = encoding, not encryption**; **HTTPS** (HTTP + **TLS**) is essential for **all** methods.
- **Bearer tokens and OAuth access tokens expire**; an **API key does not** (less secure, manual rotation).
- **API key in the Authorization header**, never in the URL.
- Only **bearer** and **OAuth 2.0** involve an **auth server** issuing tokens.
- **403** = must authenticate; **404** = not found; **2xx** = success.

### 11. Part 2 quiz (3 questions)

| Question | Answer | Why |
| :--- | :--- | :--- |
| Which methods involve an auth server issuing tokens? (select two) | **OAuth 2.0** and **bearer authentication** | Basic auth has no auth server (simple username/password), nor does API key (static key). |
| How does OAuth 2.0 improve security? | **Third-party apps access resources without exposing user credentials** | The client app receives an access token from the auth server (step 4) and authenticates with it to the resource server (step 5). |
| True statements? (select three: B, C, E) | **Bearer auth requires a token**; **OAuth 2.0 enables access delegation**; **a refresh token automatically obtains a new access token** | A wrong: API keys do not expire automatically. D wrong: basic auth uses no encryption, only reversible Base64. F wrong: API keys should not be in URLs but in the Authorization header. |
