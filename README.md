# Wave Generator

**A web-based wave generator built for electrostimulation (e‑stim), in particular *stereostim*.**

The app synthesizes a stereo audio signal in real time (Web Audio API). Sent to the audio output of a phone or computer, this signal is used to drive electrodes. The left/right separation and the auto‑pan make it possible to create sensations of **movement** between electrodes — the hallmark of stereostim.

It is a **single, self‑contained, 100 % client‑side HTML file**: no dependencies, no server, no data sent anywhere. It runs in the browser (mobile / iOS optimized).

> ⚠️ **Use responsibly.** Electrostimulation must never cross the chest or the heart — use below the waist only. Always start at low intensity. This tool is provided for experimental/recreational purposes, with no warranty; you are solely responsible for how you use it.

---

## Features

### Waveforms
- **Sine, Square, Triangle, Saw**
- **Pulse width (PWM)** adjustable on the square wave (5–95 %) — turns the square into a pulse train; band‑limited synthesis (PeriodicWave) with no DC offset

### Carrier
- **Frequency** 50–1200 Hz
- **Volume**

### Rhythmic modulation (AM)
- **Rhythm** — amplitude LFO rate (tremolo)
- **Depth** — modulation depth
- **Ratio** — envelope asymmetry (attack/decay via phase warping)

### Frequency sweep
- Low/high range set with a dual slider
- **Invert** and **Double** sweep

### Stereo & panning
- **Balance L/R** — **constant‑power** panning law
- **Auto‑Pan / Orbit**: oscillates the stereo position (both channels move in opposite directions)
  - **Free** mode or **synced to the rhythm** (÷2 / ×1 / ×2)
  - **Speed**, **Phase** (0–360°, 180° = inverted), **Width**, **Ratio** (asymmetry)
  - **Link to amplitude ratio**

### Visualization
- Real‑time **L/R oscilloscope** and **VU meter**, embedded in the sticky header (always visible)

### Presets
- Built‑in: Default, Delta, Theta, Alpha, Sweep ♭, Orbit
- **Save your own custom presets**

### Comfort & system
- **Play / Hold** (freeze the signal)
- **Screen Wake Lock** while playing — keeps the phone from sleeping and cutting the signal
- **Collapsible sections** (accordion), state remembered
- **Audio output device** selection
- **Settings persistence** (localStorage)
- Accessibility: ARIA labels, keyboard navigation, ≥ 44 px touch targets

---

## Usage

Open `index.html` in a browser, or serve it from a web server:

```bash
python3 -m http.server 8080
# then http://localhost:8080
```

> Serve the page over **HTTPS** (or `http://localhost`): some APIs (audio output selection, Wake Lock) are blocked on non‑local HTTP.
> Wake Lock requires **iOS 16.4+** (or a recent browser).

---

## Technical
- **Web Audio API**: carrier (`OscillatorNode` / `PeriodicWave`), amplitude modulation and sweep driven by looping `AudioBufferSourceNode` LFOs, panning via `WaveShaper`, L/R metering via `ChannelSplitter` + `AnalyserNode`.
- No external dependencies, a single `index.html` file.
