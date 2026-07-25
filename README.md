# Wave Generator — accès depuis le réseau local

Application web (`index.html`) diffusée sur ton réseau local pour l'ouvrir
depuis un téléphone, une tablette ou un autre ordinateur.

## Démarrer le serveur

Depuis le dossier du projet :

```bash
python3 server.py
```

Le serveur affiche alors quelque chose comme :

```
  Sur cet ordinateur  : http://localhost:8000
  Depuis un autre appareil du réseau, ouvre :
      http://192.168.1.42:8000
```

Sur l'autre ordinateur/téléphone, ouvre l'adresse en `http://192.168.x.x:8000`
(**pas** `localhost` — `localhost` désigne toujours l'appareil courant).

Changer de port si besoin :

```bash
python3 server.py 8080
```

## « Je n'arrive pas à atteindre le serveur depuis un autre ordinateur »

À vérifier dans l'ordre :

1. **N'utilise pas `localhost`.** Sur l'autre appareil, tape bien
   `http://<IP-de-la-machine-serveur>:8080`, l'IP affichée au démarrage.

2. **Les deux appareils sont sur le même réseau.** Même Wi-Fi (attention aux
   réseaux « invité » qui isolent les appareils entre eux), ou même box.

3. **Le pare-feu bloque le port.** C'est la cause la plus fréquente une fois
   que le serveur écoute bien sur `0.0.0.0`. Autorise le port (ex. 8000) :

   - **Windows** : au premier lancement, Windows Defender demande d'autoriser
     Python → coche **Réseaux privés** et « Autoriser l'accès ». Sinon :
     Panneau de configuration → Pare-feu Windows Defender → Autoriser une
     application → coche Python pour les réseaux privés.
   - **macOS** : Réglages Système → Réseau → Pare-feu → Options → autorise
     `python3` à accepter les connexions entrantes (ou désactive temporairement
     le pare-feu pour tester).
   - **Linux (ufw)** : `sudo ufw allow 8000/tcp`

4. **Tester rapidement.** Depuis l'autre machine :
   `ping <IP-du-serveur>`. Si le ping échoue → problème réseau/isolation Wi-Fi.
   Si le ping passe mais pas le navigateur → c'est le pare-feu (point 3).

## Note

Ce serveur écoute sur `0.0.0.0` (toutes les interfaces) : c'est ce qui rend
l'application accessible aux autres appareils. Un serveur qui n'écoute que sur
`127.0.0.1` / `localhost` n'est joignable que depuis la machine elle-même.
