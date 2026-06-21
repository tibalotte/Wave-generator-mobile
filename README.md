# Wave Generator

**Générateur d'ondes web conçu pour l'électrostimulation (e‑stim), en particulier le *stereostim*.**

L'application synthétise un signal audio stéréo en temps réel (Web Audio API) qui, envoyé sur la sortie audio du téléphone ou de l'ordinateur, sert à piloter des électrodes. La séparation gauche/droite et l'auto‑panoramique permettent de créer des sensations de **déplacement** entre les électrodes, caractéristiques du stereostim.

C'est un **fichier HTML unique, autonome et 100 % côté client** : aucune dépendance, aucun serveur, aucune donnée envoyée. Il fonctionne dans le navigateur (optimisé mobile / iOS).

> ⚠️ **Usage responsable.** L'électrostimulation ne doit jamais traverser la cage thoracique ni le cœur : à n'utiliser que sous la ceinture. Commencez toujours à faible intensité. Cet outil est fourni à des fins expérimentales/récréatives, sans garantie ; vous êtes seul responsable de son usage.

---

## Fonctionnalités

### Formes d'onde
- **Sinus, Carré, Triangle, Dent de scie**
- **Rapport cyclique (PWM)** réglable sur le carré (5–95 %) — transforme le carré en train d'impulsions, synthèse band‑limited (PeriodicWave) sans offset continu (DC nul)

### Porteuse
- **Fréquence** 50–1200 Hz
- **Volume**

### Modulation rythmique (AM)
- **Rythm** — vitesse du LFO d'amplitude (tremolo)
- **Depth** — profondeur de la modulation
- **Ratio** — asymétrie de l'enveloppe (attaque/déclin via *phase warping*)

### Balayage de fréquence (Freq Sweep)
- Plage basse/haute réglable au double‑curseur
- **Inverser** et **Double** balayage

### Stéréo & panoramique
- **Balance L/R** — loi de panoramique à **puissance constante**
- **Auto‑Pan / Orbit** : oscillation de la position stéréo (les deux canaux varient en sens opposé)
  - Mode **Libre** ou **synchronisé au rythme** (÷2 / ×1 / ×2)
  - **Vitesse**, **Phase** (0–360°, 180° = inversé), **Largeur**, **Ratio** (asymétrie)
  - **Lier au ratio d'amplitude**

### Visualisation
- **Oscilloscope L/R** temps réel et **VU‑mètre**, intégrés dans le bandeau collant (toujours visibles)

### Préréglages
- Intégrés : Défaut, Delta, Theta, Alpha, Sweep ♭, Orbit
- **Sauvegarde de préréglages personnalisés**

### Confort & système
- **Play / Hold** (gel du signal)
- **Anti‑veille de l'écran** (Screen Wake Lock) pendant la lecture — empêche le téléphone de se mettre en veille et de couper le signal
- **Sections repliables** (accordéon), état mémorisé
- **Sélection du périphérique de sortie audio**
- **Persistance** des réglages (localStorage)
- Accessibilité : libellés ARIA, navigation clavier, cibles tactiles ≥ 44 px

---

## Utilisation

Ouvrir `index.html` dans un navigateur, ou le servir depuis un serveur web :

```bash
python3 -m http.server 8080
# puis http://localhost:8080
```

> Servez la page en **HTTPS** (ou `http://localhost`) : certaines API (sélection du périphérique de sortie, Wake Lock) sont bloquées sur du HTTP non‑local.
> Le Wake Lock nécessite **iOS 16.4+** (ou un navigateur récent).

---

## Technique
- **Web Audio API** : porteuse (`OscillatorNode` / `PeriodicWave`), modulation d'amplitude et balayage pilotés par des `AudioBufferSourceNode` (LFO en boucle), panoramique via `WaveShaper`, métrage L/R par `ChannelSplitter` + `AnalyserNode`.
- Aucune dépendance externe, un seul fichier `index.html`.
