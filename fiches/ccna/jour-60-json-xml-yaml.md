# CCNA Day 60 : JSON, XML & YAML / Sérialisation des données

> Source : Jeremy's IT Lab, « Free CCNA | JSON, XML, & YAML | Day 60 » (29 min), vidéo n°120 de la playlist. Pas de lab pour ce jour. Fiche rédigée à partir de la transcription le 6 octobre 2026. Sujet d'examen : 6.7 (interpréter des données encodées en JSON ; XML et YAML ne sont pas dans la liste).

## 🇫🇷 Version française

### 1. La sérialisation des données

- **Sérialisation** : convertir des données dans un **format standardisé** pour les **stocker** (fichier) ou les **transmettre** (réseau) puis les **reconstruire**, éventuellement par une autre application. Une app en Python et une app en Java stockent les données différemment : il leur faut un format commun.
- Les langages de sérialisation (JSON, XML, YAML) représentent des **variables** sous forme de texte. Une variable est un **conteneur qui stocke une valeur** : `interface_name` contient `gigabitethernet1/1`, `status` contient `up`, `ip_address` contient `192.168.1.1`, `netmask` contient `255.255.255.0`.
- Sans format standard : le client (une app) envoie un GET au serveur (un contrôleur SDN), reçoit les variables brutes et **ne les comprend pas**. Avec JSON : l'**API** du serveur convertit les variables en JSON, le client les reçoit et les convertit dans son format natif.

### 2. JSON (*JavaScript Object Notation*)

- Format de fichier et d'échange de données **ouvert**, en **texte lisible par l'humain** et facile à lire par les machines. Standardisé dans la **RFC 8259** (lecture recommandée). Dérivé de JavaScript mais **indépendant du langage**. **Les API REST utilisent souvent JSON**, d'où son importance pour le CCNA.
- **Les espaces blancs sont insignifiants** (*whitespace is insignificant*) : espaces et retours à la ligne ne changent pas le sens, ils servent seulement à la lisibilité.
- **Quatre types primitifs** :
  - **String** (chaîne) : valeur texte **entre guillemets doubles** : `"Hello"`, `"5"`, `"true"`, `"null"` sont des chaînes.
  - **Number** (nombre) : valeur numérique **sans guillemets** : `5`, `100`. `"5"` (chaîne) ≠ `5` (nombre).
  - **Boolean** : deux valeurs possibles, **`true` ou `false`, sans guillemets, en minuscules**. Exemple : `"passive": true` sur une interface OSPF passive.
  - **Null** : absence intentionnelle de valeur, écrit **`null` en minuscules, sans guillemets**.
- **Deux types structurés** :
  - **Object** (objet) : liste **non ordonnée** de **paires clé-valeur**, entre **accolades `{ }`**. La **clé est obligatoirement une chaîne** (guillemets doubles) ; la valeur peut être **n'importe quel type JSON** (chaîne, nombre, booléen, null, objet, tableau). **Deux-points** entre clé et valeur, **virgule** entre les paires, **pas de virgule après la dernière paire**. Un objet dans un objet est un **objet imbriqué** (*nested object*). Un objet est aussi appelé **dictionnaire**.
  - **Array** (tableau) : **série de valeurs** séparées par des virgules, entre **crochets `[ ]`** (pas des paires clé-valeur). Les valeurs **n'ont pas à être du même type** : `["Hi", 5]`.
- Exemple d'objet vu dans la vidéo : `"interface": "gigabitethernet1/1"` (chaîne), `"is_up": true` (booléen), `"speed": 1000` (nombre, dernière paire sans virgule). Objets imbriqués : `"device": {"name": "R1", "vendor": "Cisco", "model": "1101"}`. Tableau : `"interfaces": ["gigabitethernet1/1", "gigabitethernet1/2", "gigabitethernet1/3"]`.
- Comparaison : la sortie de `show ip interface brief` est lisible par l'humain mais pas facile pour un programme ; la même information en JSON est facile pour les machines et reste lisible.

### 3. XML

- Développé comme **langage de balisage** (*markup language*, comme HTML, qui sert à formater du texte), utilisé aujourd'hui comme langage de sérialisation général.
- **Moins lisible** que JSON mais pas difficile. **Espaces blancs insignifiants** comme JSON. **Souvent utilisé par les API REST**, comme JSON.
- Format : **`<clé>valeur</clé>`**. Sur Cisco IOS, `show ip interface brief | format` affiche la sortie en XML : chaque interface entre des balises **`<entry>`**, avec les clés **Interface, IP-address, OK, Method, Status, Protocol** (par exemple `<Interface>GigabitEthernet0/0</Interface>`).

### 4. YAML

- Signifiait *Yet Another Markup Language*, renommé **YAML Ain't Markup Language** (acronyme **récursif**) pour marquer son rôle de sérialisation et non de balisage.
- Utilisé par l'outil d'automatisation **Ansible** (vidéo ultérieure).
- **Très lisible** et **les espaces blancs sont significatifs** : l'**indentation compte**, contrairement à JSON et XML.
- Un fichier YAML commence par **trois tirets `---`** ; **un tiret `-`** indique un élément de liste ; paire clé-valeur = **`clé: valeur`**.

### 5. Pièges d'examen

- **Espaces blancs** : insignifiants en **JSON et XML**, **significatifs en YAML**.
- Les **clés JSON sont toujours des chaînes** ; « key » n'est **pas** un type de données.
- `true`/`false`/`null` **sans guillemets** = booléen/null ; **avec guillemets** = chaîne. Idem pour les nombres.
- Vérifier : **une virgule entre chaque paire et chaque valeur, aucune après la dernière** ; **deux-points seulement entre clé et valeur** ; **chaque `{` et `[` fermé**.
- **Objet** = `{ }` paires clé-valeur (aussi « dictionnaire ») ; **tableau** = `[ ]` valeurs.
- Jeremy insiste : il faut **s'entraîner à lire du JSON**, pas seulement écouter.

### 6. Commandes IOS

```
R1# show ip interface brief | format     ! affiche la sortie en XML (balises <entry>, <Interface>, <IP-address>...)
```

### 7. Le quiz (10 questions, les données JSON des questions 4 à 10 étaient à l'écran et ne figurent pas dans la transcription)

| Question | Réponse | Pourquoi |
| :--- | :--- | :--- |
| Dans quel langage les espaces blancs sont-ils significatifs ? | **YAML** | En JSON et XML ils n'ont pas de sens ; en YAML l'indentation est essentielle. |
| Quel langage écrit les paires clé-valeur `<clé>valeur</clé>` ? | **XML** | Balises de type HTML. |
| Lequel n'est PAS un type de données JSON ? | **key** | JSON définit des paires clé-valeur, mais « key » n'est pas un type ; toutes les clés sont des chaînes (string, type valide). |
| Examiner le JSON : affirmation vraie ? | **Il y a trop de virgules** | Une virgule sépare les paires, mais il ne faut pas de virgule après la dernière paire. |
| Examiner le JSON : affirmation vraie ? | **La valeur de `"ip_interfaces"` est un tableau** | Les crochets l'indiquent, même si le tableau contient plusieurs objets. |
| Lequel est du JSON valide ? | **D** | A : virgule après la clé `"interfaces"` au lieu d'un deux-points. B : deux-points après la valeur 5 (seulement entre clé et valeur). C : virgule manquante entre gigabitethernet1/1 et 1/2 dans le tableau. |
| Examiner le JSON : affirmation vraie ? | **La valeur de `"is_up"` est un booléen** | `true` sans guillemets ; les booléens sont `true` ou `false` sans guillemets. |
| Examiner le JSON : affirmation vraie ? | **C'est du JSON valide** | Aucune virgule ni accolade manquante ; les espaces blancs sont insignifiants. |
| Examiner le JSON : affirmation vraie ? | **Un crochet manque** | La valeur de `"routes"` est un tableau avec un crochet ouvrant mais sans crochet fermant. Vérifier chaque ouverture/fermeture. |
| Examiner le JSON : affirmation vraie ? | **C'est du JSON valide** | Aucune accolade ni crochet manquant ; la valeur de `"dhcp4"` est une chaîne, pas un booléen. |

---

## 🇬🇧 English version

### 1. Data serialization

- **Serialization**: converting data into a **standardized format** that can be **stored** (file) or **transmitted** (network) and then **reconstructed**, perhaps by a different application. A Python app and a Java app store data differently: they need a common format.
- Data serialization languages (JSON, XML, YAML) represent **variables** as text. A variable is a **container that stores a value**: `interface_name` contains `gigabitethernet1/1`, `status` contains `up`, `ip_address` contains `192.168.1.1`, `netmask` contains `255.255.255.0`.
- Without a standard format: the client (an app) sends a GET to the server (an SDN controller), receives raw variables and **does not understand them**. With JSON: the server's **API** converts the variables to JSON, the client receives them and converts them to its own native format.

### 2. JSON (JavaScript Object Notation)

- **Open** standard file and data interchange format, using **human-readable text**, also easily machine-readable. Standardized in **RFC 8259** (recommended reading). Derived from JavaScript but **language-independent**. **REST APIs often use JSON**, which is why Cisco expects it for the CCNA.
- **Whitespace is insignificant**: spaces and line breaks do not change the meaning; they only help readability.
- **Four primitive data types**:
  - **String**: text value **in double quotes**: `"Hello"`, `"5"`, `"true"`, `"null"` are all strings.
  - **Number**: numeric value **without quotes**: `5`, `100`. `"5"` (string) ≠ `5` (number).
  - **Boolean**: only two values, **`true` or `false`, no quotes, all lower-case**. Example: `"passive": true` on a passive OSPF interface.
  - **Null**: intentional absence of any value, written **`null` in lower case, no quotes**.
- **Two structured data types**:
  - **Object**: **unordered** list of **key-value pairs**, surrounded by **curly brackets `{ }`**. The **key must be a string** (double quotes); the value can be **any valid JSON type** (string, number, boolean, null, object, array). **Colon** between key and value, **comma** between pairs, **no comma after the last pair**. An object inside an object is a **nested object**. An object is also called a **dictionary**.
  - **Array**: **series of values** separated by commas, in **square brackets `[ ]`** (not key-value pairs). Values **need not be the same type**: `["Hi", 5]`.
- Object example from the video: `"interface": "gigabitethernet1/1"` (string), `"is_up": true` (boolean), `"speed": 1000` (number, last pair with no comma). Nested objects: `"device": {"name": "R1", "vendor": "Cisco", "model": "1101"}`. Array: `"interfaces": ["gigabitethernet1/1", "gigabitethernet1/2", "gigabitethernet1/3"]`.
- Comparison: `show ip interface brief` output is human-readable but not easy for programs; the same data in JSON is easy for computers and still quite human-readable.

### 3. XML

- Developed as a **markup language** (like HTML, used to format text), now used as a general data serialization language.
- **Less human-readable** than JSON but not difficult. **Whitespace insignificant** like JSON. **Often used by REST APIs**, same as JSON.
- Format: **`<key>value</key>`**. On Cisco IOS, `show ip interface brief | format` displays the output in XML: each interface inside **`<entry>`** tags, with keys **Interface, IP-address, OK, Method, Status, Protocol** (e.g. `<Interface>GigabitEthernet0/0</Interface>`).

### 4. YAML

- Originally meant Yet Another Markup Language, repurposed to **YAML Ain't Markup Language** (a **recursive** acronym) to mark its role as data serialization rather than markup.
- Used by the automation tool **Ansible** (covered in a later video).
- **Very human-readable** and **whitespace is significant**: **indentation matters**, unlike JSON and XML.
- A YAML file starts with **three hyphens `---`**; **one hyphen `-`** indicates a list item; key-value pair = **`key: value`**.

### 5. Exam traps

- **Whitespace**: insignificant in **JSON and XML**, **significant in YAML**.
- **JSON keys are always strings**; "key" is **not** a data type.
- `true`/`false`/`null` **without quotes** = boolean/null; **with quotes** = string. Same for numbers.
- Check: **a comma between each pair and each value, none after the last**; **colon only between key and value**; **every `{` and `[` closed**.
- **Object** = `{ }` key-value pairs (also "dictionary"); **array** = `[ ]` values.
- Jeremy insists: you must **practice reading JSON**, not just listen.

### 6. IOS commands

```
R1# show ip interface brief | format     ! displays the output in XML (<entry>, <Interface>, <IP-address>... tags)
```

### 7. Quiz (10 questions; the JSON data for questions 4 to 10 was on screen and is not in the transcript)

| Question | Answer | Why |
| :--- | :--- | :--- |
| In which language is whitespace significant? | **YAML** | In JSON and XML it has no meaning; in YAML indentation is essential. |
| Which language formats key-value pairs as `<key>value</key>`? | **XML** | HTML-like tags. |
| Which is NOT a valid JSON data type? | **key** | JSON defines key-value pairs, but key is not a type; all keys are strings (string is a valid type). |
| Examine the JSON: true statement? | **There are too many commas** | A comma separates pairs, but there must be no comma after the last pair. |
| Examine the JSON: true statement? | **The value of `"ip_interfaces"` is an array** | The square brackets indicate it, even though the array contains objects. |
| Which is valid JSON? | **D** | A: comma after the `"interfaces"` key instead of a colon. B: colon after the value 5 (only between key and value). C: missing comma between gigabitethernet1/1 and 1/2 in the array. |
| Examine the JSON: true statement? | **The value of `"is_up"` is a boolean** | `true` without quotes; booleans are `true` or `false` without quotes. |
| Examine the JSON: true statement? | **It is valid JSON** | No missing comma or curly bracket; whitespace is insignificant. |
| Examine the JSON: true statement? | **A square bracket is missing** | The value of `"routes"` is an array with an opening bracket but no closing bracket. Check every opening/closing. |
| Examine the JSON: true statement? | **It is valid JSON** | No missing curly or square brackets; the value of `"dhcp4"` is a string, not a boolean. |
