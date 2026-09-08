---
title: SoundSpectrum
colorFrom: green
colorTo: yellow
sdk: static
app_file: index.html
pinned: false
---

# SoundSpectrum

SoundSpectrum is a browser-based Track B audio project for the AI Solution Engineering assignment. It captures microphone audio, extracts live DSP features with the Web Audio API, visualizes the frequency spectrum, calculates a spike confidence score, and logs events that can be exported as CSV.

Live Space URL: https://huggingface.co/spaces/Sean-Lee-HuggingFace/SoundSpectrum

## Run locally

Open `index.html` in a modern browser. Microphone APIs require a secure context, so if direct file access is blocked, serve the folder locally:

```bash
python -m http.server 7860
```

Then open `http://localhost:7860/` and press **Start microphone**.

## Data and model

Audio stays in the browser and is not uploaded. The app uses DSP feature extraction rather than a hosted neural model:

- RMS loudness estimates the current microphone energy.
- FFT frequency bins identify the strongest peak frequency.
- A rolling baseline estimates normal room volume.
- The spike score compares current energy against the sensitivity-adjusted baseline.

This score is a heuristic confidence for sudden audio spikes. It is useful for live sound monitoring, but it is not a speech recognizer, speaker identifier, or trained audio classifier.

## Engineering features

- Permission and missing-device messages for microphone failures.
- Adjustable spike sensitivity, minimum volume, and analyser smoothing.
- Live spectrum visualization and latency estimate.
- Event log with timestamps, scores, volume, peak frequency, clear action, and CSV export.

## CI/CD

The workflow in `.github/workflows/deploy-huggingface.yml` verifies required files, installs `requirements.txt`, runs the static app verifier, and deploys to Hugging Face Spaces when pushes land on `main`.

Create a GitHub repository secret named `HF_TOKEN` with Hugging Face write access. The deploy target is configured as `Sean-Lee-HuggingFace/SoundSpectrum`.

## Create the Hugging Face Space

If the Space does not exist yet, create it once from the Hugging Face UI or CLI:

```bash
hf auth login
hf repo create Sean-Lee-HuggingFace/SoundSpectrum --type space --space-sdk static
```

After the GitHub repository is connected and the `HF_TOKEN` secret is set, every push to `main` will verify the app and deploy it to the Space automatically.