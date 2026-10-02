# Générateur de decks Anki

Deux scripts Python, sans dépendance à Anki lui-même :

| Script | Rôle |
| :--- | :--- |
| `md2anki.py` | Convertit des fichiers `.md`, `.txt`, `.csv` ou `.html` (TSOFA) en un paquet `.apkg` importable dans Anki. |
| `fetch_workbook_flashcards.py` | Télécharge les 24 jeux de flashcards du *Automate the Boring Stuff Workbook* et les convertit en un seul paquet Anki (1127 cartes, un sous-deck par chapitre). |

## Installation

Un environnement Python commun à tous les outils existe à la racine du projet (`C:\utils\ccna\.venv`). Pour le recréer :

```powershell
python -m venv C:\utils\ccna\.venv
C:\utils\ccna\.venv\Scripts\pip install -r C:\utils\ccna\outils\requirements.txt
```

Dans VS Code, sélectionnez cet interpréteur (Ctrl+Shift+P > « Python: Select Interpreter » > `.venv`) pour faire disparaître les avertissements de paquets manquants.

## Écrire ses propres cartes

Créez un fichier Markdown, par exemple `linux-bloc1.md` (voir `exemple.md`) :

```markdown
tags: linux, bloc1

# Fichiers et permissions

Q: Que signifie `chmod 750 script.sh` ?
A: Propriétaire : rwx (7). Groupe : r-x (5). Autres : rien (0).

Quelle commande change le propriétaire ? ;; `chown user:group fichier`

# systemd

Q: Comment voir les logs de `nginx` depuis le dernier boot ?
A: `journalctl -u nginx -b`
```

Règles :
- `Q:` / `A:` sur plusieurs lignes, une ligne vide termine la carte.
- Ou une carte par ligne avec ` ;; ` comme séparateur.
- `# Titre` crée un sous-deck.
- `tags:` en tête de fichier s'applique à toutes les cartes.
- Le Markdown inline `code` et **gras** est converti en HTML.

Puis :

```powershell
C:\utils\ccna\.venv\Scripts\python md2anki.py linux-bloc1.md -o ..\..\ressources\anki\linux-bloc1.apkg -d "Linux"
```

Plusieurs fichiers ou un dossier entier en entrée : chaque fichier devient un sous-deck.
Dans Anki : Fichier > Importer > choisir le `.apkg`.

## Mettre à jour un deck sans perdre sa progression

L'identifiant de chaque note est calculé à partir de la question et du fichier source.
Corriger une réponse puis réimporter le `.apkg` met la carte à jour dans Anki en conservant l'historique de révision.
Changer le texte de la question crée en revanche une nouvelle carte.

## Fichiers TSOFA

Les pages `flashcards-*.html` d'Al Sweigart (The Simple Offline Flashcard App) contiennent leurs cartes dans un tableau JavaScript `FLASHCARDS`.
`md2anki.py` sait les lire directement : le pied de page promotionnel des réponses est retiré.
Les fichiers HTML restent utilisables tels quels dans un navigateur, hors ligne.

## Où mettre les fichiers de cartes

Suggestion : un fichier par bloc du curriculum dans `..\..\cartes\` (à créer), versionné avec vos notes.
Les `.apkg` générés vont dans `..\..\ressources\anki\`.
