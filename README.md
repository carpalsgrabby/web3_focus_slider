# web3_focus_slider

A very small CLI helper that compares three conceptual Web3 styles and shows how well each fits your priorities:

- Aztec-style zk rollup (privacy-heavy, zk circuits over Ethereum)
- Zama-style FHE stack (encrypted compute with fully homomorphic encryption)
- Soundness-first protocol (formal proofs and high correctness)

The script does not connect to a blockchain and has no external dependencies. It is just a tiny scoring function that helps you think about where your project sits in the space between privacy, soundness, and UX speed.


Repository layout

This repo intentionally has only two files:

- app.py
- README.md


Concept

You provide three numbers between 0 and 10:

- privacy importance
- soundness / proofs importance
- UX speed importance

For each style, the script stores three floats between 0 and 1:

- privacy
- soundness
- ux_speed

It then computes a simple fit score between 0.0 and 1.0 by comparing your needs to each profile and prints a mini bar chart and label (excellent, good, ok, weak).


Installation

Requirements:

- Python 3.8 or newer
- No extra packages

Steps:

1. Create a new GitHub repository.
2. Place app.py and README.md in the root directory.
3. Ensure the python command is available in your shell.
4. Mark app.py as executable if you want (optional).


Usage

Run from the repository root.

Default run (uses built-in defaults):

python app.py

Example: strong privacy, strong soundness, moderate speed:

python app.py --privacy 9 --soundness 9 --speed 6

Example: high UX speed, moderate privacy, strong soundness:

python app.py --privacy 6 --soundness 8 --speed 9

Example: FHE-heavy, privacy-maximal project that accepts slower UX:

python app.py --privacy 10 --soundness 9 --speed 3


Output

The script prints:

- your stated needs for privacy, soundness, and UX speed
- one line per style with:
  - name and key
  - numeric fit score between 0.0 and 1.0
  - textual label (excellent, good, ok, weak)
  - a small bar made of █ characters
  - a short explanatory note

All numbers are illustrative and subjective. The tool is meant to help guide conversation about whether your design is closer to an Aztec-like zk rollup, a Zama-like FHE compute stack, or a soundness-first protocol approach. You can edit the style values in app.py to better match your own views.
