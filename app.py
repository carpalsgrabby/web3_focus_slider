#!/usr/bin/env python3
import argparse
from dataclasses import dataclass
from typing import Dict


@dataclass
class Web3Style:
    key: str
    name: str
    privacy: float     # 0–1
    soundness: float   # 0–1
    ux_speed: float    # 0–1
    note: str


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
    return max(0.0, min(1.0, x))


def score(style: Web3Style, priv: int, snd: int, speed: int) -> float:
    priv_n = clamp01(priv / 10.0)
    snd_n = clamp01(snd / 10.0)
    spd_n = clamp01(speed / 10.0)

    m_priv = 1.0 - abs(priv_n - style.privacy)
    m_snd = 1.0 - abs(snd_n - style.soundness)
    m_spd = 1.0 - abs(spd_n - style.ux_speed)

    return clamp01(0.4 * m_snd + 0.35 * m_priv + 0.25 * m_spd)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="web3_focus_slider",
        description="Tiny Web3 style slider inspired by Aztec, Zama and soundness-first designs.",
    )
    p.add_argument("--privacy", type=int, default=8, help="Privacy importance (0–10, default 8).")
    p.add_argument("--soundness", type=int, default=7, help="Soundness / proofs importance (0–10, default 7).")
    p.add_argument("--speed", type=int, default=6, help="UX speed importance (0–10, default 6).")
        p.add_argument(
        "--no-unicode",
        action="store_true",
        help="Disable Unicode symbols in output.",
    )

    return p.parse_args()


def label(score_val: float) -> str:
    if score_val >= 0.8:
        return "excellent"
    if score_val >= 0.65:
        return "good"
    if score_val >= 0.5:
        return "ok"
    return "weak"


def main() -> None:
    args = parse_args()

    priv = max(0, min(10, args.privacy))
    snd = max(0, min(10, args.soundness))
    spd = max(0, min(10, args.speed))

      title = "🎚  web3_focus_slider" if not args.no_unicode else "web3_focus_slider"
    print(title)
    print(f"Needs -> privacy: {priv}/10, soundness: {snd}/10, UX speed: {spd}/10")
    print("")
    print("Profiles:")
    for key, style in STYLES.items():
        s = score(style, priv, snd, spd)
        bar = "█" * int(s * 18)
        print(f"- {style.name:24s} ({key}): {s:.3f} [{label(s)}] {bar}")
        print(f"  {style.note}")
    print("")


if __name__ == "__main__":
    main()
