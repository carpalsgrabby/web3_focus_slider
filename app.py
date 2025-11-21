#!/usr/bin/env python3
"""
web3_focus_slider

CLI toy for exploring Web3 tradeoffs between privacy, soundness, and UX speed,
inspired by Aztec-style zk rollups, Zama-style FHE, and soundness-first designs.

Example:
    python web3_focus_slider.py --privacy 9 --soundness 8 --speed 5
"""
__version__ = "0.1.0"
import argparse
from dataclasses import dataclass
from typing import Dict


@dataclass
class Web3Style:
    """
    A Web3 stack style profile with emphasis scores on privacy, soundness, and UX speed.
    """
    key: str
    name: str
    privacy: float     # 0–1
    soundness: float   # 0–1
    ux_speed: float    # 0–1
    note: str

# Built-in style profiles keyed by a short identifier for CLI use.
STYLES: Dict[str, Web3Style] = {
    "aztec": Web3Style(
        key="aztec",
        name="Aztec-style zk rollup",
        privacy=0.95,
        soundness=0.82,
        ux_speed=0.55,
        note="Encrypted balances and zk circuits; strong privacy, heavier UX.",
    ),
    "zama": Web3Style(
        key="zama",
        name="Zama-style FHE stack",
        privacy=0.92,
        soundness=0.86,
        ux_speed=0.40,
        note="Fully homomorphic encrypted compute; max privacy, slower UX.",
    ),
    "soundness": Web3Style(
        key="soundness",
        name="Soundness-first protocol",
        privacy=0.55,
        soundness=0.98,
        ux_speed=0.72,
        note="Formal specs and proofs; very strong correctness, decent UX.",
    ),
}


def clamp01(x: float) -> float:
    """
    Clamp a float value to the inclusive range [0.0, 1.0].
    """
    return max(0.0, min(1.0, x))


def score(style: Web3Style, priv: int, snd: int, speed: int) -> float:
    """
    Compute a normalized fit score (0–1) between user needs and a Web3 style.
    """
    priv_n = clamp01(priv / 10.0)
    snd_n = clamp01(snd / 10.0)
    spd_n = clamp01(speed / 10.0)


    m_priv = 1.0 - abs(priv_n - style.privacy)
    m_snd = 1.0 - abs(snd_n - style.soundness)
    m_spd = 1.0 - abs(spd_n - style.ux_speed)

        # Weigh soundness slightly more than privacy, and UX speed a bit less:
    # 40% soundness, 35% privacy, 25% UX speed.
    return clamp01(0.4 * m_snd + 0.35 * m_priv + 0.25 * m_spd)



def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for the web3_focus_slider CLI.
    """
    p = argparse.ArgumentParser(

        prog="web3_focus_slider",
        description="Tiny Web3 style slider inspired by Aztec, Zama and soundness-first designs.",
    )
     p.add_argument("-p", "--privacy", type=int, default=8, help="Privacy importance (0–10, default 8).")

    p.add_argument("--soundness", type=int, default=7, help="Soundness / proofs importance (0–10, default 7).")
    p.add_argument("--speed", type=int, default=6, help="UX speed importance (0–10, default 6).")
        p.add_argument(
        "--no-unicode",
        action="store_true",
        help="Disable Unicode symbols in output.",
    )
    p.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show version and exit.",
    )

    return p.parse_args()


def label(score_val: float) -> str:
    """
    Convert a numeric fit score into a qualitative label.
    """
    if score_val >= 0.8:
        return "excellent"
    if score_val >= 0.65:
        return "good"
    if score_val >= 0.5:
        return "ok"
    return "weak"

    scored_styles = []
    for key, style in STYLES.items():
        s = score(style, priv, snd, spd)
        scored_styles.append((key, style, s))

    best_score = max(s for _, _, s in scored_styles) if scored_styles else 0.0


    best_score = max(s for _, _, s in scored_styles) if scored_styles else 0.0


def main() -> int:
    args = parse_args()

      priv = args.privacy
    snd = args.soundness
    spd = args.speed

    if not (0 <= priv <= 10):
        print(f"WARNING: --privacy {priv} is out of range, clamping to [0,10].")
        priv = max(0, min(10, priv))
    if not (0 <= snd <= 10):
        print(f"WARNING: --soundness {snd} is out of range, clamping to [0,10].")
        snd = max(0, min(10, snd))
    if not (0 <= spd <= 10):
        print(f"WARNING: --speed {spd} is out of range, clamping to [0,10].")
        spd = max(0, min(10, spd))

      title = "🎚  web3_focus_slider" if not args.no_unicode else "web3_focus_slider"
    print(title)
    print(f"Needs -> privacy: {priv}/10, soundness: {snd}/10, UX speed: {spd}/10")
    print("")
    print("Profiles:")
    for key, style in STYLES.items():
        s = score(style, priv, snd, spd)
        bar = "█" * int(s * 18)
               lbl = label(s)
        print(f"- {style.name:24s} ({key}): {s:.3f} [{lbl}] {bar}")

        print(f"  {style.note}")
         print("-" * 40)
    print("")


if __name__ == "__main__":
    raise SystemExit(main())

