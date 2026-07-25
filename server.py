#!/usr/bin/env python3
"""Serveur web minimal pour l'application Wave Generator.

Aucune dépendance : utilise uniquement la bibliothèque standard de Python 3.
Sert les fichiers statiques du dossier courant (dont index.html).

Le serveur écoute sur 0.0.0.0 (toutes les interfaces réseau), il est donc
accessible depuis les autres appareils du réseau local. Au démarrage il
affiche l'adresse à taper sur ces autres appareils.

Utilisation :
    python3 server.py            # port 8000 par défaut
    python3 server.py 9000       # port personnalisé

Sur cette machine     : http://localhost:8000
Sur un autre appareil : http://<IP-affichée>:8000  (surtout PAS localhost)
"""

import http.server
import socketserver
import sys
import os
import socket
import webbrowser
from functools import partial

DEFAULT_PORT = 8000
HOST = "0.0.0.0"  # écoute sur toutes les interfaces -> accessible sur le LAN


def local_ip_addresses():
    """Retourne les adresses IPv4 locales (192.168.x.x, 10.x.x.x, ...)."""
    addrs = set()

    # Méthode fiable pour l'IP de sortie principale : on "connecte" un socket
    # UDP vers une adresse externe (aucun paquet n'est réellement envoyé).
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        addrs.add(s.getsockname()[0])
        s.close()
    except OSError:
        pass

    # Complément : toutes les IP associées au nom d'hôte.
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ip = info[4][0]
            if not ip.startswith("127."):
                addrs.add(ip)
    except OSError:
        pass

    return sorted(addrs)


def main():
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Port invalide : {sys.argv[1]} — utilisation du port {DEFAULT_PORT}")

    # Sert le dossier où se trouve ce script (donc index.html à côté).
    root = os.path.dirname(os.path.abspath(__file__))

    handler = partial(http.server.SimpleHTTPRequestHandler, directory=root)

    # allow_reuse_address évite « Address already in use » après un redémarrage.
    socketserver.TCPServer.allow_reuse_address = True

    try:
        with socketserver.TCPServer((HOST, port), handler) as httpd:
            local_url = f"http://localhost:{port}"
            print("Wave Generator — serveur réseau local démarré")
            print(f"  Dossier servi       : {root}")
            print(f"  Sur cet ordinateur  : {local_url}")

            ips = local_ip_addresses()
            if ips:
                print("  Depuis un autre appareil du réseau, ouvre :")
                for ip in ips:
                    print(f"      http://{ip}:{port}")
            else:
                print("  (Aucune adresse réseau locale détectée — connecté au Wi-Fi/Ethernet ?)")

            print("  Si un autre appareil n'y arrive pas : vérifie le pare-feu (voir README.md).")
            print("  Arrêt               : Ctrl+C")

            # On n'ouvre le navigateur que sur la machine serveur.
            try:
                webbrowser.open(local_url)
            except Exception:
                pass
            httpd.serve_forever()
    except OSError as exc:
        print(f"Impossible de démarrer sur le port {port} : {exc}")
        print("Essayez un autre port, par ex. : python3 server.py 8080")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nServeur arrêté.")


if __name__ == "__main__":
    main()
