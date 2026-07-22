"""Genera audios de test de musica ambiental relajante.

Sintetiza acordes de ondas senoidales suaves con una modulacion lenta
(sensacion de "respiracion"), fundidos de entrada/salida y un ligero
detune para dar calidez. No es musica "real", solo pads ambientales
utiles para probar los reproductores.

Uso:  python scripts/gen_test_audio.py
Requiere: numpy y ffmpeg en el PATH (para exportar a mp3).
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

SR = 44100  # sample rate
OUT = Path(__file__).resolve().parent.parent / "audio"


def note(freq: float, dur: float, *, detune: float = 0.5, harmonics=(1, 2, 3)) -> np.ndarray:
    """Un tono calido: fundamental + armonicos suaves + ligero detune."""
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    wave_sum = np.zeros_like(t)
    for i, h in enumerate(harmonics):
        amp = 1.0 / (h * h)  # armonicos superiores mas flojos
        wave_sum += amp * np.sin(2 * np.pi * freq * h * t)
        wave_sum += amp * 0.6 * np.sin(2 * np.pi * (freq * h + detune) * t)
    return wave_sum


def breathe(signal: np.ndarray, rate: float = 0.12, depth: float = 0.35) -> np.ndarray:
    """Modulacion de amplitud muy lenta, como una respiracion."""
    t = np.linspace(0, len(signal) / SR, len(signal), endpoint=False)
    lfo = (1 - depth) + depth * (0.5 + 0.5 * np.sin(2 * np.pi * rate * t))
    return signal * lfo


def fades(signal: np.ndarray, fade: float = 4.0) -> np.ndarray:
    n = int(SR * fade)
    env = np.ones_like(signal)
    ramp = np.linspace(0, 1, n)
    env[:n] = ramp
    env[-n:] = ramp[::-1]
    return signal * env


def normalize(signal: np.ndarray, peak: float = 0.6) -> np.ndarray:
    m = np.max(np.abs(signal))
    return signal * (peak / m) if m > 0 else signal


def chord(freqs, dur: float) -> np.ndarray:
    mix = sum(note(f, dur) for f in freqs)
    return fades(normalize(breathe(mix)), fade=min(4.0, dur / 4))


def write_wav(path: Path, signal: np.ndarray) -> None:
    data = (np.clip(signal, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(path), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


def to_mp3(wav: Path, mp3: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-b:a", "128k", str(mp3)],
        check=True,
    )
    wav.unlink()


# Nota base A2 = 110 Hz. Acordes distintos por pista para dar variedad.
TRACKS = {
    # Respiracion consciente: La mayor (A-C#-E), sereno y claro.
    "respiracion-consciente": ([110.0, 138.59, 164.81], 40.0),
    # Body scan: Re add9 (D-F#-A-E), calido y envolvente.
    "body-scan": ([98.0, 123.47, 146.83, 164.81], 45.0),
    # Dormir: Do grave (C-G-E), muy bajo y suave.
    "dormir": ([65.41, 98.0, 130.81], 50.0),
}


def main() -> None:
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg no encontrado en el PATH.")
    OUT.mkdir(exist_ok=True)
    for name, (freqs, dur) in TRACKS.items():
        wav = OUT / f"{name}.wav"
        mp3 = OUT / f"{name}.mp3"
        write_wav(wav, chord(freqs, dur))
        to_mp3(wav, mp3)
        print(f"generado {mp3.name} ({dur:.0f}s)")

    # Check minimo: los 3 mp3 existen y no estan vacios.
    for name in TRACKS:
        f = OUT / f"{name}.mp3"
        assert f.exists() and f.stat().st_size > 1000, f"fallo al generar {f.name}"
    print("OK: 3 audios de test generados en", OUT)


if __name__ == "__main__":
    main()
