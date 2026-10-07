# Fiche : mettre en marche la VM Ubuntu sur une nouvelle machine

> VM concernée : Ubuntu Server 22.04 LTS, nom d'hôte `ubnu`, utilisateur `naj`, créée sous VMware Workstation Pro, dossier `C:\Users\Najib\Documents\Virtual Machines\Ubuntu 64-bit\` (15,5 Go avec le snapshot « 30Sept »). Rédigée le 7 octobre 2026.

## 0. Avant de commencer : deux options

| Option | Quand | Durée |
| :--- | :--- | :--- |
| **A. Copier la VM** (ce guide) | Vous voulez retrouver exactement le même système, snapshot compris | 1 h, dont 30 à 45 min de copie |
| **B. Recréer une VM neuve** | PC de passage, ou disque externe indisponible | 20 min, voir section 6 |

Le contenu unique de la VM est encore petit : quelques réglages système et le dépôt `lab-notes`, qui est sur GitHub. L'option B est souvent aussi rapide.

## 1. Prérequis sur la nouvelle machine

- **Windows 10 64 bits version 20H1 ou plus récente, ou Windows 11.** Vérifier avec `winver`.
- **Processeur 64 bits de 2011 ou plus récent, virtualisation activée** (Intel VT-x ou AMD-V) dans le BIOS/UEFI. Vérifier dans le Gestionnaire des tâches > Performance > Processeur > « Virtualisation : Activé ». Si « Désactivé », l'activer dans le BIOS (menu Advanced ou CPU Configuration).
- **20 Go libres** sur le disque de destination.
- **VMware Workstation Pro 26H1u1**, fichier `VMware-Workstation-Full-26H1u1-25688693.exe`, gratuit pour usage personnel. Téléchargement sur support.broadcom.com (compte gratuit) : VMware Cloud Foundation > My Downloads > Free Software Downloads > Workstation > 26H1u1 for Windows. Installation avec les options par défaut, redémarrage, puis dans l'écran d'accueil choisir l'usage personnel.
- Si Hyper-V ou WSL2 sont actifs sur cette machine, c'est compatible : Workstation utilise alors la plateforme d'hyperviseur Windows. Un message sur les « atténuations de canal latéral » apparaîtra : voir section 4.

## 2. Préparer la copie sur le PC d'origine

1. Dans la VM : `sudo poweroff`. La VM doit être **éteinte**, pas suspendue.
2. Fermer VMware Workstation.
3. Facultatif, pour gagner de la place : rouvrir Workstation, sélectionner la VM, **VM > Manage > Clean Up Disks**, puis refermer.
4. Copier le dossier complet `C:\Users\Najib\Documents\Virtual Machines\Ubuntu 64-bit\` sur un disque externe ou une clé USB. Tout le dossier : les fichiers `.vmx`, `.vmxf`, `.nvram`, `.vmsd`, tous les `.vmdk` (y compris `-000001-*`, ce sont les deltas du snapshot) et `.vmsn`. Les `vmware*.log` peuvent être ignorés.
5. Facultatif : compresser en 7-Zip avant la copie (15,5 Go deviennent 6 à 9 Go).
6. Copier aussi, depuis le PC d'origine, la clé SSH `C:\Users\Najib\.ssh\id_ed25519` et `id_ed25519.pub`, ou prévoir d'en générer une nouvelle (section 5).

## 3. Mettre la VM en marche sur la nouvelle machine

1. Coller le dossier dans `C:\Users\<vous>\Documents\Virtual Machines\Ubuntu 64-bit\` (le chemin exact n'a pas d'importance, mais ce dossier est celui par défaut de Workstation).
2. Workstation > **File > Open** > `Ubuntu 64-bit.vmx`.
3. **Power on**. Workstation demande « This virtual machine may have been moved or copied » : répondre **I Copied It**. Il génère une nouvelle adresse MAC et un nouvel identifiant, ce qui évite tout conflit si les deux PC sont sur le même réseau.
4. Si un message signale un périphérique absent (lecteur CD, port USB) : **OK**, sans conséquence.
5. Le snapshot « 30Sept » est présent dans **VM > Snapshot > Snapshot Manager**. En prendre un nouveau tout de suite, nommé avec la date.

## 4. Réglages à refaire sur la nouvelle machine

Ces réglages sont dans le fichier `.vmx` et voyagent avec la VM, sauf un qui dépend de l'hôte :

- **VM > Settings > Options > Advanced** : décocher « Enable side channel mitigations for Hyper-V enabled hosts » si l'hôte a Hyper-V ou WSL2. Sinon la VM est ralentie pour rien.
- Vérifier **VM > Settings > Network Adapter** : NAT. C'est le mode d'origine ; il donne à la VM un accès Internet sans configuration et une adresse 192.168.x.x attribuée par VMware.
- Si la machine a peu de mémoire, réduire la RAM de la VM dans Settings > Memory (2 Go suffisent pour le curriculum).

## 5. Rétablir l'accès SSH

1. Dans la console de la VM, se connecter (`naj`) et relever l'adresse :

```bash
ip -br a
```

L'adresse NAT est différente de celle du PC d'origine (192.168.33.128 là-bas).

2. Sur le nouveau PC, Windows Terminal. Si la clé `id_ed25519` a été copiée dans `C:\Users\<vous>\.ssh\`, elle est déjà autorisée dans la VM. Sinon, générer une clé et l'ajouter :

```powershell
ssh-keygen -t ed25519
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh naj@ADRESSE "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys"
```

3. Créer ou compléter `C:\Users\<vous>\.ssh\config` :

```
Host ubnu
    HostName ADRESSE
    User naj
    IdentityFile ~/.ssh/id_ed25519
```

4. Tester : `ssh ubnu`. Puis dans la VM, vérifier que GitHub répond toujours (la clé SSH de la VM voyage avec elle) :

```bash
ssh -T git@github.com
cd ~/lab-notes && git pull
```

5. VS Code : extension Remote-SSH, se connecter à `ubnu`.

Si l'adresse change plus tard (DHCP du NAT VMware) : `ip -br a` dans la console et corriger `HostName` dans le fichier config.

## 6. Option B : recréer une VM neuve en 20 minutes

1. Télécharger l'ISO Ubuntu Server 24.04 LTS (autant prendre la version récente : UEFI, Secure Boot, support jusqu'en 2029).
2. Workstation > File > New Virtual Machine > Typical > l'ISO > 2 vCPU, 4 Go RAM, 30 Go disque, réseau NAT.
3. Installateur Ubuntu : clavier, réseau DHCP, disque entier, utilisateur `naj`, nom d'hôte `ubnu`, **cocher « Install OpenSSH server »**, pas de snaps supplémentaires.
4. Après le premier démarrage :

```bash
sudo apt update && sudo apt upgrade -y && sudo apt install -y git curl vim
sudo touch /etc/cloud/cloud-init.disabled
echo "\$nrconf{restart} = 'a';" | sudo tee /etc/needrestart/conf.d/50-auto.conf
echo 'shopt -s histverify' >> ~/.bashrc
git config --global user.name najibyla && git config --global user.email nlahkimyla@gmail.com
ssh-keygen -t ed25519
```

5. Ajouter la clé publique de la VM à GitHub (Settings > SSH keys), cloner `git@github.com:najibyla/lab-notes.git`, puis suivre la section 5 pour l'accès SSH depuis Windows.
6. Snapshot « neuve ».

Ces étapes sont exactement ce que le bloc 5 du curriculum automatisera avec Ansible.

## 7. Dépannage

| Symptôme | Cause probable | Correctif |
| :--- | :--- | :--- |
| « VT-x/AMD-V is not available » au démarrage | Virtualisation désactivée dans le BIOS | Activer Intel VT-x ou AMD SVM dans le BIOS, redémarrer |
| La VM démarre mais très lentement | Atténuations canal latéral actives sur un hôte Hyper-V | Section 4, premier point |
| Pas d'adresse IP dans la VM | Carte réseau non connectée | VM > Settings > Network Adapter > cocher « Connect at power on » et « Connected », mode NAT |
| `ssh ubnu` : Permission denied (publickey) | Clé du nouveau PC inconnue de la VM | Section 5, étape 2, en se connectant d'abord par mot de passe |
| `ssh ubnu` : Connection timed out | Adresse NAT changée | `ip -br a` dans la console, corriger le fichier config |
| Workstation refuse d'ouvrir le `.vmx` | Dossier copié incomplet (vmdk manquants) | Recopier tout le dossier depuis le PC d'origine |
| Message cloud-init au démarrage | Normal si la VM a été recréée sans l'étape 4 de la section 6 | `sudo touch /etc/cloud/cloud-init.disabled` |
